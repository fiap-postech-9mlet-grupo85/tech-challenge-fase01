import torch
import torch.nn as nn

class ChurnMLP(nn.Module):
    """
    Arquitetura de Rede Neural Densa (Feed-Forward) para classificação binária de Churn.
    A rede possui Input -> 64 -> 32 -> 1, com funções de ativação ReLU e Dropout de 30% 
    para prevenção de overfitting.
    """
    def __init__(self, input_dim: int):
        super(ChurnMLP, self).__init__()
        self.fc1 = nn.Linear(input_dim, 64)
        self.relu1 = nn.ReLU()
        self.dropout1 = nn.Dropout(0.3)
        
        self.fc2 = nn.Linear(64, 32)
        self.relu2 = nn.ReLU()
        self.dropout2 = nn.Dropout(0.3)
        
        # A última camada não tem ativação Sigmoid no forward pois usaremos BCEWithLogitsLoss
        self.fc3 = nn.Linear(32, 1)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.fc1(x)
        x = self.relu1(x)
        x = self.dropout1(x)
        
        x = self.fc2(x)
        x = self.relu2(x)
        x = self.dropout2(x)
        
        x = self.fc3(x)
        return x
