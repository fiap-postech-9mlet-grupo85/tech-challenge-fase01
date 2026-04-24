import logging
import os
from typing import Any, Dict

import joblib
import pandas as pd
import torch

from src.models.churn_mlp import ChurnMLP
from src.schemas.data_schema import CustomerSchema

# Configuração Padrão Corporativa de Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Limiar de Negócio definido na Etapa 2 (Custo Financeiro Ótimo)
BUSINESS_THRESHOLD = 0.30

# Variáveis Globais de Estado (Lazy Loading)
_preprocessor = None
_model = None

def load_artifacts():
    """
    Carrega o preprocessor (Scikit-Learn) e os pesos (PyTorch) do disco.
    Utiliza Lazy Loading para carregar apenas uma vez na inicialização da API.
    """
    global _preprocessor, _model

    if _preprocessor is None:
        logger.info("Carregando Preprocessor do disco...")
        preprocessor_path = 'models/preprocessor.joblib'
        if not os.path.exists(preprocessor_path):
            logger.error(f"Artefato {preprocessor_path} não encontrado.")
            raise FileNotFoundError(f"Artefato {preprocessor_path} não encontrado. Execute train_model.py primeiro.")
        _preprocessor = joblib.load(preprocessor_path)

    if _model is None:
        logger.info("Carregando Pesos da Rede Neural do disco...")
        model_path = 'models/churn_mlp.pth'
        if not os.path.exists(model_path):
            logger.error(f"Artefato {model_path} não encontrado.")
            raise FileNotFoundError(f"Artefato {model_path} não encontrado. Execute train_model.py primeiro.")

        # Recupera o número de features pós-OneHotEncoder (do preprocessor fitado)
        state_dict = torch.load(model_path, map_location=torch.device('cpu'), weights_only=True)
        input_dim = state_dict['fc1.weight'].shape[1]

        _model = ChurnMLP(input_dim=input_dim)
        _model.load_state_dict(state_dict)
        _model.eval()

def predict_churn(raw_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Função de inferência end-to-end.
    Recebe um dicionário JSON com os dados do cliente, valida com Pandera, processa e aplica o threshold.
    """
    load_artifacts()

    # 0. Converte para DataFrame
    df = pd.DataFrame([raw_data])

    # 1. Validação de Contrato (Pandera)
    try:
        CustomerSchema.validate(df)
        logger.info("Validação do Schema Pandera passou com sucesso.")
    except Exception as e:
        logger.error(f"Falha na validação do Schema dos dados de entrada: {e}")
        raise ValueError(f"Dados de entrada inválidos segundo o Schema. Detalhe: {e}")

    # Tratamento específico que fizemos na fase de limpeza (TotalCharges missing)
    if 'TotalCharges' in df.columns:
        df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
        df['TotalCharges'] = df['TotalCharges'].fillna(0.0)

    # 2. Pipeline do Scikit-Learn
    try:
        X_tf = _preprocessor.transform(df)
    except ValueError as e:
        logger.error(f"Erro no ColumnTransformer: {e}")
        raise ValueError(f"Erro no pré-processamento. Detalhe: {e}")

    # 3. PyTorch Inference
    X_tensor = torch.tensor(X_tf, dtype=torch.float32)

    with torch.no_grad():
        logits = _model(X_tensor)
        probability = torch.sigmoid(logits).item()

    # 4. Regra de Negócio (Threshold)
    is_churn = bool(probability >= BUSINESS_THRESHOLD)

    logger.info(f"Inferência concluída. Probabilidade: {probability:.4f} | Churn: {is_churn}")

    return {
        "churn_prediction": is_churn,
        "probability": round(probability, 4),
        "threshold_used": BUSINESS_THRESHOLD
    }
