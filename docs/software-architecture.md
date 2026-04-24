# Arquitetura de Software (Pacote Python)

Este documento detalha a arquitetura do nosso pacote fonte (`src/`), construído durante a Etapa 3 do Tech Challenge, marcando a evolução de um modelo analítico (Jupyter Notebook) para um ecossistema corporativo de MLOps.

## 🎯 Princípios de Design
A arquitetura foi desenhada seguindo o princípio **Separation of Concerns (SoC)**. A API de inferência não deve conhecer detalhes sobre como o modelo foi treinado ou quais bibliotecas matemáticas rodam por baixo dos panos. Ela deve apenas injetar um JSON e receber uma resposta.

## 📁 Estrutura de Diretórios (`src/`)

### 1. `src/features/`
Responsável pela transformação bruta dos dados.
* **`build_features.py`**:
    * `clean_raw_data(df)`: Regras hardcoded de limpeza de banco de dados (ex: imputação de valores `TotalCharges` em branco).
    * `get_preprocessor()`: Instancia e retorna a fábrica exata do Scikit-Learn (`ColumnTransformer` com `StandardScaler` e `OneHotEncoder`).

### 2. `src/models/`
Encapsula o coração algorítmico do Churn e as lógicas de I/O.
* **`churn_mlp.py`**:
    * Contém estritamente a classe PyTorch (`nn.Module`). Define as camadas ocultas, neurônios, ativações (ReLU) e funções de regularização (Dropout).
* **`train_model.py` (Orquestrador de Treino)**:
    * Script automatizado que roda ponta a ponta. Ele pega os dados de `data/raw/`, treina os preprocessors, constrói os tensores, treina a rede neural (`ChurnMLP`) com `EarlyStopping` e **exporta os pesos** para a pasta `models/` em formato `.joblib` e `.pth`.
* **`predict_model.py` (Orquestrador de Inferência)**:
    * O módulo de "leitura". Ele utiliza *Lazy Loading* (padrão Singleton) para carregar os pesos pesados de `.joblib` e `.pth` apenas uma vez na memória RAM.
    * Expõe a função limpa `predict_churn(raw_dict)`, que converte o JSON em Tensor, avalia na Rede Neural, e aplica a rígida **Regra de Negócio de 30% (Business Threshold)** para classificar o churn, baseada na matriz de custos financeiros desenhada no ML Canvas.

## 🚀 Fluxo de Vida (Ciclo Operacional)
1. O Cientista de Dados roda a pesquisa nos cadernos (pasta `notebooks/`).
2. O Cientista/Engenheiro formaliza as descobertas atualizando o arquivo `train_model.py` e executa:
   ```bash
   PYTHONPATH=. python src/models/train_model.py
   ```
3. O script gera os artefatos seriais físicos.
4. A API FastAPI importa a função mágica `predict_churn` e consome os arquivos gerados no disco.
