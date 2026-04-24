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
* [**ML Canvas**](docs/ML_CANVAS.md): Stakeholders, métricas de negócio e SLOs.

### 2. Análise e Experimentação
Exploração dos dados e definição do ponto de partida.
* [**Notebook de EDA & Baselines**](notebooks/01_eda_baselines.ipynb): Análise exploratória completa e modelos simples (Logistic Regression) registrados no MLflow.

### 3. Modelagem Avançada
Desenvolvimento da solução principal.
* [**Rede Neural (PyTorch)**](notebooks/02_neural_network_training.ipynb): Arquitetura da MLP, treinamento com Early Stopping e comparação de métricas.

### 4. Engenharia e Operação
A estrutura de software que suporta o modelo em produção.
* [**API de Inferência**](src/main.py): Implementação do FastAPI com endpoints de predição e saúde.
* [**Model Card**](docs/MODEL_CARD.md): Documentação técnica sobre performance, vieses e limitações do modelo.
* [**Plano de Monitoramento**](docs/MONITORING.md): Estratégia de alertas e métricas pós-deploy.

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
1.  **Setup do Ambiente:** `pip install -r requirements.txt` (ou via `pyproject.toml`).
2.  **Executar Testes:** `make test` ou `pytest`.
3.  **Rodar API:** `make run` ou `uvicorn src.main:app`.

---

## 📺 Entrega Final
* **Vídeo STAR:** [Link para o vídeo de 5 minutos explicando o projeto].
* **Deploy (Opcional):** .