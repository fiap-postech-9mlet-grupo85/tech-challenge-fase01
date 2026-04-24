import pandas as pd

from src.features.build_features import clean_raw_data


def test_clean_raw_data_converts_total_charges():
    """
    Testa se a função de limpeza lida corretamente com a anomalia do dataset da IBM:
    espaços em branco na coluna TotalCharges devem ser convertidos para 0.0 (float).
    """
    data = {'TotalCharges': [' ', '100.5']}
    df = pd.DataFrame(data)

    cleaned_df = clean_raw_data(df)

    assert cleaned_df['TotalCharges'].dtype == float
    assert cleaned_df['TotalCharges'].iloc[0] == 0.0
    assert cleaned_df['TotalCharges'].iloc[1] == 100.5
