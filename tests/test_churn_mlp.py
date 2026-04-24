import torch

from src.models.churn_mlp import ChurnMLP


def test_churn_mlp_forward_pass():
    """
    Testa se a rede neural feed-forward respeita o formato de saída do Batch.
    Para N clientes processados, deve cuspir N predições.
    """
    input_dim = 20
    model = ChurnMLP(input_dim=input_dim)

    # Simula um batch de 4 clientes, cada um com 20 features numéricas/OHE
    dummy_input = torch.randn(4, input_dim)

    output = model(dummy_input)

    # Garante que a saída é (Batch_Size, 1), exigido pela BCEWithLogitsLoss
    assert output.shape == (4, 1)
