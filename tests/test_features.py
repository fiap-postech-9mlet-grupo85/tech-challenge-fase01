import pandas as pd

from src.features.build_features import clean_raw_data


def test_clean_raw_data_handles_blank_spaces():
    """
    Testa se a função clean_raw_data converte corretamente strings em branco (" ")
    na coluna TotalCharges para valores numéricos preenchidos (0.0),
    sem alterar o DataFrame original.
    """
    # Dado um DataFrame "sujo" (como o que vem do dataset original da IBM)
    dirty_df = pd.DataFrame(
        {
            "customerID": ["1", "2", "3", "4"],
            "TotalCharges": ["29.85", " ", "56.95", ""],
        }
    )

    # Quando rodamos a função de limpeza
    cleaned_df = clean_raw_data(dirty_df)

    # Então a coluna TotalCharges deve ser transformada em tipo Float
    assert pd.api.types.is_numeric_dtype(
        cleaned_df["TotalCharges"]
    ), "TotalCharges deveria ser numérico."

    # E os valores vazios (" " e "") devem ter sido substituídos por 0.0
    assert (
        cleaned_df["TotalCharges"].iloc[1] == 0.0
    ), "Espaço em branco ' ' deveria virar 0.0"
    assert (
        cleaned_df["TotalCharges"].iloc[3] == 0.0
    ), "String vazia '' deveria virar 0.0"

    # E os valores normais devem ter sido mantidos corretamente
    assert cleaned_df["TotalCharges"].iloc[0] == 29.85
    assert cleaned_df["TotalCharges"].iloc[2] == 56.95

    # E o mais importante: o DataFrame original NÃO pode ter sido modificado (mutação isolada)
    assert (
        dirty_df["TotalCharges"].iloc[1] == " "
    ), "O DataFrame original foi corrompido!"
