# Tech Challenge - Fase 1: ML Engineering (FIAP)

## 📌 Visão Geral
Este projeto consiste no desenvolvimento de uma solução end-to-end para a previsão de **Churn** (cancelamento de clientes) de uma operadora de telecomunicações. O objetivo é construir desde o entendimento do problema de negócio até a disponibilização de uma API de inferência robusta e testada.

### 🛠️ Tecnologias Principais
* **Modelagem:** PyTorch (Redes Neurais MLP) e Scikit-Learn (Baselines).
* **Métricas & Tracking:** MLflow.
* **Engenharia & API:** FastAPI e Pydantic.
* **Qualidade:** Pytest (Testes), Ruff (Linting) e Pandera (Schema).

---

## 🗺️ Guia da Documentação
Abaixo está a ordem sugerida para explorar o projeto, seguindo o ciclo de vida de ML:

### 1. Entendimento de Negócio
Documentação estratégica sobre o problema e as decisões técnicas iniciais.
* [**ML Canvas**](docs/ml-canvas.md): Stakeholders, métricas de negócio e SLOs.

### 2. Análise e Experimentação
Exploração dos dados e definição do ponto de partida.
* [**Dicionário de Dados**](docs/data-dictionary.md): Schema e metadados detalhados sobre as variáveis (features) do dataset.
* [**Notebook de EDA & Baselines**](notebooks/01_eda_baselines.ipynb): Análise exploratória completa e modelos simples (Logistic Regression) registrados no MLflow.

### 3. Modelagem Avançada
Desenvolvimento da solução principal.
* [**Rede Neural (PyTorch)**](notebooks/02_neural_network_training.ipynb): Arquitetura da MLP, treinamento com Early Stopping e comparação de métricas.

### 4. Engenharia e Operação
A estrutura de software que suporta o modelo em produção.
* [**API de Inferência**](src/main.py): Implementação do FastAPI com endpoints de predição e saúde.
* [**Model Card**](docs/model-card.md): Documentação técnica sobre performance, vieses e limitações do modelo.
* [**Plano de Monitoramento**](docs/monitoring.md): Estratégia de alertas e métricas pós-deploy.

---

## 📂 Estrutura do Repositório
* `data/`: Armazenamento local do dataset (ignorado pelo Git).
* `docs/`: Documentos de arquitetura, Canvas e Model Card.
* `models/`: Artefatos dos modelos treinados e serializados.
* `notebooks/`: Experimentos iniciais e análise exploratória.
* `src/`: Código fonte modularizado (API, pipelines, transformadores).
* `tests/`: Suíte de testes automatizados (unitários, schema e smoke tests).

---

## 🚀 Como Executar
1.  **Criar Ambiente Virtual (Recomendado):** `python3 -m venv .venv`
2.  **Ativar o Ambiente:** 
    - Mac/Linux: `source .venv/bin/activate`
    - Windows: `.venv\Scripts\activate`
3.  **Setup de Dependências:** Com o ambiente ativado, rode `make install`.
4.  **Baixar os Dados:** Execute o script `make download-data` (ou `bash tools/scripts/download_data.sh`) para buscar o dataset da IBM.
5.  **Análise Exploratória:** O notebook está em `notebooks/01-eda-baselines.ipynb`.


---

## 📺 Entrega Final
* **Vídeo STAR:** [Link para o vídeo de 5 minutos explicando o projeto].
* **Deploy (Opcional):** .