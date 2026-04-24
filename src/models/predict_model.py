import os
import joblib
import pandas as pd
import torch
import torch.nn as nn
from typing import Dict, Any

from src.models.churn_mlp import ChurnMLP

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
        preprocessor_path = 'models/preprocessor.joblib'
        if not os.path.exists(preprocessor_path):
            raise FileNotFoundError(f"Artefato {preprocessor_path} não encontrado. Execute train_model.py primeiro.")
        _preprocessor = joblib.load(preprocessor_path)
        
    if _model is None:
        model_path = 'models/churn_mlp.pth'
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Artefato {model_path} não encontrado. Execute train_model.py primeiro.")
        
        # Recupera o número de features pós-OneHotEncoder (do preprocessor fitado)
        # O preprocessor tem a lista de features geradas se precisarmos, mas podemos inferir
        # O ideal é extrair do modelo treinado, porém hardcodar a leitura dos pesos requer instanciar o modelo vazio.
        # Vamos ler o state_dict para ver a shape da camada 1 (Input dimension)
        state_dict = torch.load(model_path, map_location=torch.device('cpu'), weights_only=True)
        input_dim = state_dict['fc1.weight'].shape[1]
        
        _model = ChurnMLP(input_dim=input_dim)
        _model.load_state_dict(state_dict)
        _model.eval()

def predict_churn(raw_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Função de inferência end-to-end.
    Recebe um dicionário JSON com os dados do cliente, processa e aplica o threshold.
    """
    load_artifacts()
    
    # Converte o Dicionário Único para um DataFrame (formato esperado pelo Pipeline)
    df = pd.DataFrame([raw_data])
    
    # Tratamento específico que fizemos na fase de limpeza (TotalCharges missing)
    if 'TotalCharges' in df.columns:
        df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
        df['TotalCharges'] = df['TotalCharges'].fillna(0.0)
    
    # 1. Pipeline do Scikit-Learn
    try:
        X_tf = _preprocessor.transform(df)
    except ValueError as e:
        raise ValueError(f"Erro no pré-processamento. Verifique se os nomes das colunas e tipos batem. Detalhe: {e}")
        
    # 2. PyTorch Inference
    X_tensor = torch.tensor(X_tf, dtype=torch.float32)
    
    with torch.no_grad():
        logits = _model(X_tensor)
        # Como o modelo não tem Sigmoid na última camada (usamos BCEWithLogitsLoss),
        # precisamos aplicar a Sigmoid agora para obter a probabilidade real [0, 1].
        probability = torch.sigmoid(logits).item()
        
    # 3. Regra de Negócio (Threshold)
    is_churn = bool(probability >= BUSINESS_THRESHOLD)
    
    return {
        "churn_prediction": is_churn,
        "probability": round(probability, 4),
        "threshold_used": BUSINESS_THRESHOLD
    }
