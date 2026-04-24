# Dicionário de Dados: Telco Customer Churn (IBM)

Este documento descreve o schema e os metadados do dataset de Churn (`dataset.csv`), originalmente fornecido pela IBM como `Telco-Customer-Churn.csv`. O dataset possui 21 colunas no total, representando o perfil e o histórico de uma base de clientes de telecomunicações.

## 1. Informações Demográficas
- **customerID**: Identificador único alfanumérico para cada cliente (ex: `7590-VHVEG`).
- **gender**: Gênero do cliente (`Male`, `Female`).
- **SeniorCitizen**: Indica se o cliente é um cidadão idoso (`1` para sim, `0` para não).
- **Partner**: Indica se o cliente tem um parceiro/cônjuge (`Yes`, `No`).
- **Dependents**: Indica se o cliente tem dependentes (`Yes`, `No`).

## 2. Serviços Contratados (Telefonia e Internet)
- **tenure**: Número de meses que o cliente permaneceu na empresa.
- **PhoneService**: Indica se o cliente assina serviço telefônico (`Yes`, `No`).
- **MultipleLines**: Indica se o cliente possui múltiplas linhas telefônicas (`Yes`, `No`, `No phone service`).
- **InternetService**: Provedor de serviço de internet do cliente (`DSL`, `Fiber optic`, `No`).
- **OnlineSecurity**: Possui segurança online adicional (`Yes`, `No`, `No internet service`).
- **OnlineBackup**: Possui backup online (`Yes`, `No`, `No internet service`).
- **DeviceProtection**: Possui proteção de dispositivo (`Yes`, `No`, `No internet service`).
- **TechSupport**: Possui suporte técnico (`Yes`, `No`, `No internet service`).
- **StreamingTV**: Assina streaming de TV (`Yes`, `No`, `No internet service`).
- **StreamingMovies**: Assina streaming de filmes (`Yes`, `No`, `No internet service`).

## 3. Informações de Conta e Financeiras
- **Contract**: O termo de contrato atual do cliente (`Month-to-month`, `One year`, `Two year`).
- **PaperlessBilling**: Indica se o cliente optou por faturamento sem papel/digital (`Yes`, `No`).
- **PaymentMethod**: Forma de pagamento do cliente (`Electronic check`, `Mailed check`, `Bank transfer (automatic)`, `Credit card (automatic)`).
- **MonthlyCharges**: O valor (em dólar) cobrado do cliente mensalmente.
- **TotalCharges**: O valor total acumulado já cobrado do cliente durante todo o `tenure`.

## 4. Variável Alvo (Target)
- **Churn**: Indica se o cliente cancelou os serviços (churned) no último mês (`Yes`, `No`). Esta é a variável que será prevista pela nossa Rede Neural.

## 5. Observações da Análise Exploratória (Data Readiness)
Durante a execução do nosso EDA (`01-eda-baselines.ipynb`), mapeamos as seguintes características vitais para a modelagem:
* **Problema de Tipagem:** A coluna `TotalCharges` sofre de um erro clássico de exportação. Clientes no primeiro mês (`tenure = 0`) possuem essa coluna vazia (com espaços em branco), o que faz o Pandas tipificá-la como `object`. Nós a convertemos forçadamente para numérica e preenchemos esses espaços com `0`.
* **Desbalanceamento:** A variável alvo `Churn` é desbalanceada. A grande maioria dos clientes está retida (`No`). Isso reforça a necessidade de usarmos métricas como F1-Score ou PR-AUC ao invés de apenas Acurácia.
* **Correlações Iniciais:** Identificamos bivariadamente que clientes com **menor tempo de casa**, contratos **Mês a Mês** e **maiores cobranças mensais** possuem um risco muito mais alto de cancelamento.

## 6. Referências e Fontes
* **Dataset Original (Raw CSV):** [Download Direto via GitHub (IBM)](https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv)
* **Repositório da IBM:** [IBM / telco-customer-churn-on-icp4d](https://github.com/IBM/telco-customer-churn-on-icp4d)
* **Documentação da Comunidade:** [Telco Customer Churn (Kaggle)](https://www.kaggle.com/datasets/blastchar/telco-customer-churn)
