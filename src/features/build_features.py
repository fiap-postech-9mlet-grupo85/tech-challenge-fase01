import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

def clean_raw_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Realiza a limpeza inicial dos dados.
    Converte TotalCharges para numérico (preenchendo os casos 'tenure=0' com 0.0).
    """
    df = df.copy()
    
    # Tratamento do TotalCharges (Conversão de String Vazia para Float)
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
    df['TotalCharges'] = df['TotalCharges'].fillna(0.0)
    
    return df

def get_preprocessor(feature_columns: list) -> ColumnTransformer:
    """
    Retorna a instância configurada do ColumnTransformer para aplicar StandardScaler
    e OneHotEncoder.
    """
    numeric_features = ['tenure', 'MonthlyCharges', 'TotalCharges']
    categorical_features = [col for col in feature_columns if col not in numeric_features]
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numeric_features),
            ('cat', OneHotEncoder(handle_unknown='ignore', drop='first'), categorical_features)
        ])
        
    return preprocessor
