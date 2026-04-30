from unittest.mock import patch

import pandas as pd

import src.models.train_model as tm


@patch("src.models.train_model.pd.read_csv")
@patch("src.models.train_model.joblib.dump")
@patch("src.models.train_model.torch.save")
@patch("src.models.train_model.mlflow")
def test_train_model_pipeline(
    mock_mlflow, mock_torch_save, mock_joblib_dump, mock_read_csv
):
    """
    Testa a orquestração do pipeline de treinamento end-to-end (Limpeza -> Pré-Processamento ->
    PyTorch Training -> MLflow Logging) utilizando um dataset mockado minúsculo para evitar
    custo computacional durante a esteira de CI/CD.
    """
    # DataFrame fictício mínimo (10 linhas) cobrindo os cenários das features
    mock_df = pd.DataFrame(
        {
            "customerID": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"],
            "gender": ["Male", "Female"] * 5,
            "SeniorCitizen": [0, 1] * 5,
            "Partner": ["Yes", "No"] * 5,
            "Dependents": ["Yes", "No"] * 5,
            "tenure": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            "PhoneService": ["Yes", "No"] * 5,
            "MultipleLines": ["No phone service", "No"] * 5,
            "InternetService": ["DSL", "Fiber optic"] * 5,
            "OnlineSecurity": ["No", "Yes"] * 5,
            "OnlineBackup": ["Yes", "No"] * 5,
            "DeviceProtection": ["No", "Yes"] * 5,
            "TechSupport": ["No", "No"] * 5,
            "StreamingTV": ["No", "Yes"] * 5,
            "StreamingMovies": ["No", "No"] * 5,
            "Contract": ["Month-to-month", "One year"] * 5,
            "PaperlessBilling": ["Yes", "No"] * 5,
            "PaymentMethod": ["Electronic check", "Mailed check"] * 5,
            "MonthlyCharges": [29.85, 56.95] * 5,
            "TotalCharges": ["29.85", " "]
            * 5,  # Inserindo um 'blank' intencional para testar limpeza
            "Churn": ["Yes", "No", "Yes", "No", "Yes", "No", "Yes", "No", "Yes", "No"],
        }
    )

    mock_read_csv.return_value = mock_df

    # Sobrescrevendo constantes de hiperparâmetros para o teste durar < 1 segundo
    tm.EPOCHS = 2
    tm.BATCH_SIZE = 2

    # Executa o pipeline
    tm.main()

    # Verificações de Asserção (garante que os componentes vitais foram chamados)
    assert mock_read_csv.called, "Deveria ter lido o CSV"
    assert mock_joblib_dump.called, "Deveria ter salvo o Preprocessor do Sklearn"
    assert mock_torch_save.called, "Deveria ter salvo os pesos da rede PyTorch"
    assert mock_mlflow.start_run.called, "Deveria ter iniciado o Tracking no MLflow"
