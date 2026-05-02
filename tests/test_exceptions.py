from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

import src.models.train_model as tm
from src.main import app
from src.models import predict_model
from src.models.predict_model import predict_churn

client = TestClient(app)


# ==========================================
# 1. Testes de Exceção em predict_model.py
# ==========================================
@patch("src.models.predict_model.os.path.exists")
def test_predict_model_missing_preprocessor(mock_exists):
    mock_exists.return_value = False
    predict_model._preprocessor = None
    predict_model._model = None

    with pytest.raises(FileNotFoundError, match="preprocessor.joblib"):
        predict_model.load_artifacts()


@patch("src.models.predict_model.os.path.exists")
def test_predict_model_missing_model(mock_exists):
    # Simula que apenas o preprocessor existe
    def side_effect(path):
        if "preprocessor" in path:
            return True
        return False

    mock_exists.side_effect = side_effect

    predict_model._preprocessor = None
    predict_model._model = None

    with patch("src.models.predict_model.joblib.load"):
        with pytest.raises(FileNotFoundError, match="churn_mlp.pth"):
            predict_model.load_artifacts()


def test_predict_churn_pandera_validation_failure():
    bad_data = {"gender": "Female"}  # Campos faltando
    with pytest.raises(ValueError, match="Dados de entrada inválidos"):
        predict_churn(bad_data)


@patch("src.models.predict_model.CustomerSchema.validate")
def test_predict_churn_transform_failure(mock_validate):
    with patch("src.models.predict_model._preprocessor") as mock_prep:
        mock_prep.transform.side_effect = ValueError("Transform Error")
        with pytest.raises(ValueError, match="Erro no pré-processamento"):
            predict_churn({"TotalCharges": "29.85"})  # Mock validation to pass


# ==========================================
# 2. Testes de Exceção e Borda em train_model.py
# ==========================================
@patch("src.models.train_model.os.path.exists")
@patch("src.models.train_model.mlflow.get_experiment_by_name")
@patch("src.models.train_model.mlflow.create_experiment")
def test_train_model_missing_dataset(mock_create_exp, mock_get_exp, mock_exists):
    mock_get_exp.return_value = None  # Força cair no bloco create_experiment
    mock_exists.return_value = False

    with pytest.raises(FileNotFoundError, match="dataset.csv"):
        tm.main()

    assert mock_create_exp.called, "Deveria ter criado um experimento novo"


@patch("src.models.train_model.pd.read_csv")
@patch("src.models.train_model.clean_raw_data")
@patch("src.models.train_model.get_preprocessor")
@patch("src.models.train_model.joblib.dump")
@patch("src.models.train_model.torch.save")
@patch("src.models.train_model.mlflow")
def test_train_model_early_stopping_and_logger(
    mock_mlflow, mock_tsave, mock_jdump, mock_get_prep, mock_clean, mock_read
):
    import numpy as np
    import pandas as pd

    # Mocking basic dataframe
    mock_df = pd.DataFrame(
        {"customerID": [str(i) for i in range(10)], "Churn": ["Yes", "No"] * 5}
    )
    mock_read.return_value = mock_df
    mock_clean.return_value = mock_df

    # Mock preprocessor (Dynamic size matching train/test split)
    mock_prep = MagicMock()
    mock_prep.fit_transform.side_effect = lambda X: np.array([[1.0]] * len(X))
    mock_prep.transform.side_effect = lambda X: np.array([[1.0]] * len(X))
    mock_get_prep.return_value = mock_prep

    # Teste 1: Disparar Logger na Época 10
    with patch.object(tm, "EPOCHS", 10), patch.object(tm, "PATIENCE", 20):
        tm.main()  # Roda sem quebrar para bater na linha if (epoch+1) % 10 == 0

    # Teste 2: Disparar Early Stopping na Época 2
    # Para fazer a validation loss subir artificialmente, mockamos o critério de erro
    import torch

    class MockLoss:
        def __init__(self, *args, **kwargs):
            self.val = 1.0

        def __call__(self, *args, **kwargs):
            self.val += 10.0  # Perda cresce exorbitantemente a cada batch
            return torch.tensor(self.val, requires_grad=True)

    with patch("src.models.train_model.nn.BCEWithLogitsLoss", return_value=MockLoss()):
        with patch.object(tm, "EPOCHS", 5), patch.object(tm, "PATIENCE", 1):
            tm.main()  # Deve dar early stop no segundo passo (época 2)


# ==========================================
# 3. Testes de Tratamento em main.py
# ==========================================
@patch("src.main.load_artifacts")
def test_main_lifespan_exception(mock_load):
    # Simula falha ao iniciar os modelos na subida da API
    mock_load.side_effect = Exception("Load Failed")
    with TestClient(app):
        pass  # Executa o lifespan context manager


# Payload base para requisição válida
VALID_PAYLOAD = {
    "gender": "Female",
    "SeniorCitizen": 0,
    "Partner": "Yes",
    "Dependents": "No",
    "tenure": 1,
    "PhoneService": "No",
    "MultipleLines": "No phone service",
    "InternetService": "DSL",
    "OnlineSecurity": "No",
    "OnlineBackup": "Yes",
    "DeviceProtection": "No",
    "TechSupport": "No",
    "StreamingTV": "No",
    "StreamingMovies": "No",
    "Contract": "Month-to-month",
    "PaperlessBilling": "Yes",
    "PaymentMethod": "Electronic check",
    "MonthlyCharges": 29.85,
    "TotalCharges": "29.85",
}


@patch("src.main.predict_churn")
def test_main_predict_value_error(mock_predict):
    mock_predict.side_effect = ValueError("Pandera Validation")
    response = client.post("/v1/predict", json=VALID_PAYLOAD)
    assert response.status_code == 422


@patch("src.main.predict_churn")
def test_main_predict_generic_error(mock_predict):
    mock_predict.side_effect = Exception("Internal Error")
    response = client.post("/v1/predict", json=VALID_PAYLOAD)
    assert response.status_code == 500
