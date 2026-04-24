import os
import joblib
import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from sklearn.model_selection import train_test_split

from src.features.build_features import clean_raw_data, get_preprocessor
from src.models.churn_mlp import ChurnMLP

# Constantes do Campeão (Grid Search)
LEARNING_RATE = 0.001
BATCH_SIZE = 64
EPOCHS = 100
PATIENCE = 10

class ChurnDataset(Dataset):
    def __init__(self, X, y):
        self.X = torch.tensor(X, dtype=torch.float32)
        self.y = torch.tensor(y, dtype=torch.float32).unsqueeze(1)
        
    def __len__(self):
        return len(self.X)
    
    def __getitem__(self, idx):
        return self.X[idx], self.y[idx]

def main():
    print("Iniciando Treinamento Modular do Telco Churn PyTorch MLP...")
    
    # 1. Carregamento e Limpeza
    data_path = 'data/raw/dataset.csv'
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Dataset não encontrado em {data_path}. Rode o download primeiro.")
        
    df = pd.read_csv(data_path)
    df = clean_raw_data(df)
    
    # Separação
    X = df.drop(columns=['Churn', 'customerID'])
    y = df['Churn'].map({'Yes': 1, 'No': 0}).values
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
    
    # 2. Pré-processamento
    print("Processando features...")
    preprocessor = get_preprocessor(list(X.columns))
    
    X_train_tf = preprocessor.fit_transform(X_train)
    X_test_tf = preprocessor.transform(X_test)
    
    # Salva o Preprocessor fitado
    os.makedirs('models', exist_ok=True)
    joblib.dump(preprocessor, 'models/preprocessor.joblib')
    print("Preprocessor salvo em models/preprocessor.joblib")
    
    # 3. Preparação para PyTorch
    train_dataset = ChurnDataset(X_train_tf, y_train)
    test_dataset = ChurnDataset(X_test_tf, y_test)
    
    train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=BATCH_SIZE, shuffle=False)
    
    # 4. Inicialização do Modelo
    input_dim = X_train_tf.shape[1]
    model = ChurnMLP(input_dim=input_dim)
    
    # Cálculo do pos_weight para balanceamento
    num_positives = np.sum(y_train == 1)
    num_negatives = np.sum(y_train == 0)
    pos_weight_val = num_negatives / num_positives
    criterion = nn.BCEWithLogitsLoss(pos_weight=torch.tensor([pos_weight_val], dtype=torch.float32))
    
    optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)
    
    # 5. Loop de Treinamento com Early Stopping
    print("Iniciando treinamento da Rede Neural...")
    best_val_loss = float('inf')
    epochs_no_improve = 0
    
    for epoch in range(EPOCHS):
        model.train()
        train_loss = 0.0
        
        for batch_X, batch_y in train_loader:
            optimizer.zero_grad()
            outputs = model(batch_X)
            loss = criterion(outputs, batch_y)
            loss.backward()
            optimizer.step()
            train_loss += loss.item() * batch_X.size(0)
            
        train_loss /= len(train_loader.dataset)
        
        # Validação
        model.eval()
        val_loss = 0.0
        with torch.no_grad():
            for batch_X, batch_y in test_loader:
                outputs = model(batch_X)
                loss = criterion(outputs, batch_y)
                val_loss += loss.item() * batch_X.size(0)
                
        val_loss /= len(test_loader.dataset)
        
        # Early Stopping Check
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            epochs_no_improve = 0
            # Salva o melhor modelo em memória/disco
            torch.save(model.state_dict(), 'models/churn_mlp.pth')
        else:
            epochs_no_improve += 1
            
        if (epoch+1) % 10 == 0:
            print(f"Epoch {epoch+1}/{EPOCHS} | Train Loss: {train_loss:.4f} | Val Loss: {val_loss:.4f}")
            
        if epochs_no_improve >= PATIENCE:
            print(f"Early Stopping acionado na Época {epoch+1}!")
            break
            
    print("Treinamento concluído. Pesos da Rede Neural salvos em models/churn_mlp.pth")

if __name__ == "__main__":
    main()
