# Tech Challenge - Fase 1: ML Engineering (FIAP)

**Curso:** FIAP Pós Tech - Machine Learning Engineering  
**Turma:** 9MLET  
**Autores (Grupo 32):**
* Bruno Machado Abreu (RM372965)
* Renan Prado Gonzalez (RM374089)
* Davi Coene Rosa (RM371466)

---

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
* [**Notebook de EDA & Baselines**](notebooks/01-eda-baselines.ipynb): Análise exploratória completa e modelos simples (Logistic Regression) registrados no MLflow.

### 3. Modelagem Avançada
Desenvolvimento da solução principal.
* [**Rede Neural (PyTorch)**](notebooks/02-neural-network-training.ipynb): Arquitetura da MLP, treinamento com Early Stopping e comparação de métricas.

### 4. Engenharia e Operação
A estrutura de software que suporta o modelo em produção.
* **Refatoração MLOps (Pacote Python)**:
    * [**Arquitetura de Software**](docs/software-architecture.md): Documentação detalhada sobre as camadas de features e modelagem na pasta `src/`.
* **Serviço**:
    * [**API de Inferência**](src/main.py): Implementação do FastAPI com endpoints de predição e saúde.
* **Governança Pós-Deploy**:
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

## 💻 Requisitos do Sistema
Para executar este projeto localmente, garanta que sua máquina possua:
* **Python 3.10+**: O projeto utiliza recursos de tipagem modernos que exigem pelo menos o Python 3.10.
* **Make**: Utilitário de automação para rodar os atalhos do `Makefile`. Nativo no Linux/Mac. No Windows, recomenda-se o uso do WSL ou Git Bash.
* **Git**: Para clonar o repositório.

---

## 🚀 Como Executar

### 🔧 Preparação do Ambiente
1.  **Criar Ambiente Virtual:** `python3 -m venv .venv`
2.  **Ativar o Ambiente:** 
    - Mac/Linux: `source .venv/bin/activate`
    - Windows: `.venv\Scripts\activate`
3.  **Setup de Dependências:** Com o ambiente ativado, rode `make install`.
4.  **Baixar os Dados:** Execute o script `make download-data` (ou `bash tools/scripts/download_data.sh`) para buscar o dataset da IBM.

### 🧠 Execução da Modelagem
5.  **Fase 1 (EDA e Baselines Lineares):** Execute o notebook `notebooks/01-eda-baselines.ipynb` para limpar os dados e treinar os modelos iniciais do Scikit-Learn.
6.  **Fase 2 (Redes Neurais PyTorch):** Execute o notebook `notebooks/02-neural-network-training.ipynb` para treinar a MLP e executar o Grid Search (Otimização de Hiperparâmetros).

### 🏗️ Treinamento Modular (Engenharia de Machine Learning)
7.  **Exportação de Artefatos (Fase 3):** A lógica isolada na pasta `src/` precisa ser treinada fora dos notebooks para gerar os arquivos binários pesados de produção. Execute:
    ```bash
    make train
    ```
    Isso povoará a pasta `models/` com os artefatos `preprocessor.joblib` e `churn_mlp.pth` que serão sugados pela API. Além disso, o treinamento espelhará os dados em formato de log no **MLflow**.

### 🛡️ Engenharia de Qualidade (Testes Unitários)
Para garantir a saúde do software desenvolvido, a suíte de testes do Pytest cobre desde o tratamento de anomalias no dataset até a arquitetura dos tensores da Rede Neural.
8. **Rodar a Suíte de Testes:** Execute o comando abaixo na raiz do repositório:
   ```bash
   make test
   ```
   A barra verde assegurará que o pacote Python Modular está pronto para ir a Produção.

### 🌐 Disponibilização da API (FastAPI)
9. **Iniciar o Servidor Local:** Para expor a nossa inteligência via HTTP e interagir com o Swagger UI, basta rodar:
   ```bash
   make run-api
   ```
   A API subirá na porta 8000. Acesse [http://localhost:8000/docs](http://localhost:8000/docs) para enviar predições em tempo real pela interface gráfica.

### 📊 Acompanhamento de Experimentos (MLflow UI)
O MLflow é o nosso repositório de governança. Para visualizar o comparativo de métricas, os hiperparâmetros campeões e acessar os artefatos serializados (tanto da Fase 1 quanto da Fase 2):
1. Com o ambiente virtual ativado, suba o servidor a partir da raiz do repositório:
   ```bash
   mlflow ui --backend-store-uri sqlite:///mlflow.db
   ```
2. Abra o navegador em: [http://localhost:5000](http://localhost:5000)
3. Na interface, você encontrará três grandes experimentos:
   * **`churn_baselines`**: Contém o histórico da Etapa 1 (Regressão Logística e Dummy).
   * **`churn_mlp_pytorch`**: Contém o histórico da Etapa 2 (A Rede Neural inicial e as Sub-Runs aninhadas do Grid Search).
   * **`churn_mlp_pytorch_modular`**: Contém o rastreio da automação corporativa (Etapa 3), gravando logs isolados do script `train_model.py`.


---

## 📺 Entrega Final
* **Vídeo STAR:** [Link para o vídeo de 5 minutos explicando o projeto].
* **Deploy (Opcional):** .