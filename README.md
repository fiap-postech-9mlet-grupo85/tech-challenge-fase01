# Tech Challenge - Fase 1: ML Engineering (FIAP)

[![Coverage](https://fiap-postech-9mlet-grupo32.github.io/tech-challenge-fase01/coverage.svg)](https://fiap-postech-9mlet-grupo32.github.io/tech-challenge-fase01/)

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
* **Infraestrutura Cloud**:
    * [**Arquitetura AWS**](docs/infrastructure.md): Diagrama e detalhes do deploy em produção via Terraform.

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

10. **Testando via Postman:** Há uma coleção pré-configurada na pasta `tools/postman/Telco_Churn_API.postman_collection.json`.
    * Abra o Postman e clique em **Import** (ou arraste o arquivo).
    * A coleção possui uma variável chamada `base_url` que por padrão vem como `http://localhost:8000`. Teste os requests localmente.
    * **Testando na AWS:** Quando a sua nuvem estiver de pé (veja a próxima seção), basta você clicar na aba *Variables* da coleção no Postman e trocar o valor de `base_url` de `http://localhost:8000` para a URL gerada do seu **CloudFront** (ex: `https://d3v3l0p3r.cloudfront.net`). Com uma única troca, os três testes já poderão acessar a API na nuvem!

11. **Testando via Shell Script (cURL e WGET):** Existem scripts Bash interativos (`test_api_curl.sh` e `test_api_wget.sh`) desenvolvidos para estressar a API via linha de comando. Ambos executam a mesma suíte de três baterias:
    * **Bateria 1:** Dispara um `GET /health` garantindo que o servidor subiu sem Cold Start.
    * **Bateria 2:** Dispara um `POST /v1/predict` com o JSON do "cliente ideal", retornando o Score de probabilidade formatado via `jq`.
    * **Bateria 3:** Dispara um `POST /v1/predict` forçando uma anomalia (removendo a chave `MonthlyCharges`), garantindo que o Pydantic barre o Request com um HTTP 422.
    
    **Como usar localmente (porta 8000):**
    ```bash
    ./tools/scripts/test_api_curl.sh
    # ou
    ./tools/scripts/test_api_wget.sh
    ```
    **Como testar na Nuvem AWS:** Passe a URL gerada pelo seu CloudFront como argumento!
    ```bash
    ./tools/scripts/test_api_curl.sh "https://seu-dominio.cloudfront.net"
    # ou
    ./tools/scripts/test_api_wget.sh "https://seu-dominio.cloudfront.net"
    ```

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


### ☁️ Deploy na Nuvem AWS (Produção)
O projeto conta com Infraestrutura como Código (Terraform) para criar um ambiente grátis (Free-Tier) na AWS do Brasil (`sa-east-1`). A arquitetura engloba uma máquina EC2 executando o Docker com proteção HTTPS via CloudFront.

**Domínio Customizado (AWS ACM + ClouDNS):**
Para entregar uma experiência profissional, implementamos um domínio limpo e seguro: `https://api.telcochurn.cloud-ip.cc/docs`. O Terraform gera automaticamente um certificado de segurança via AWS ACM e engata esse domínio no CloudFront, mediante a criação de registros CNAME no painel gratuito do ClouDNS.

**Versionamento Semântico (v1):**
Visando aderência a padrões arquiteturais corporativos, a API implementa roteamento versionado (`/v1`). Isso garante que futuras reestruturações do modelo de predição possam ser introduzidas como `/v2` sem quebrar contratos (Backward Compatibility) de consumidores que dependem do `/v1`. Apenas rotas de infraestrutura (como o `/health`) residem na raiz.

Você tem duas opções para subir a API:

**Opção A: Via Github Actions (Recomendado)**
1. Cadastre os Secrets `AWS_ACCESS_KEY_ID` e `AWS_SECRET_ACCESS_KEY` no seu repositório.
2. Acesse a aba **Actions** > **IaC - Terraform AWS Deploy**.
3. Clique em *Run workflow* com o parâmetro `apply` para criar, ou `destroy` para destruir. A URL da API aparecerá nos logs finais do Job.

**Opção B: Via Terminal Local (Makefile)**
1. Exporte suas credenciais da AWS no terminal:
   ```bash
   export AWS_ACCESS_KEY_ID="sua_chave"
   export AWS_SECRET_ACCESS_KEY="seu_segredo"
   ```
2. Inicialize o projeto e suba a infraestrutura:
   ```bash
   make tf-init
   make tf-apply
   ```
3. A URL segura do CloudFront (HTTPS) será cuspida na tela do terminal.
4. Para desligar e evitar custos residuais, rode: `make tf-destroy`.

---

## 📺 Entrega Final
* **Vídeo STAR:** [Coloque aqui o Link para o seu vídeo no YouTube].

### 🔗 Endpoints Oficiais (Produção AWS)
A API está pública, respondendo via HTTPS e protegida contra ataques volumétricos pelo CloudFront:

* **Swagger UI (Documentação Interativa):** [GET /docs](https://api.telcochurn.cloud-ip.cc/docs)
* **ReDoc (Documentação Alternativa):** [GET /redoc](https://api.telcochurn.cloud-ip.cc/redoc)
* **Health Check (Monitoramento):** [GET /health](https://api.telcochurn.cloud-ip.cc/health)
* **Inferência de Churn:** `POST https://api.telcochurn.cloud-ip.cc/v1/predict`
  * *Headers:* `Content-Type: application/json`
  * *Body:* JSON com os dados demográficos e contratuais do cliente (veja o Swagger para o schema exato).