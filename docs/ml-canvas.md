# Machine Learning Canvas: Previsão de Churn Telco

Este documento descreve a estratégia de Machine Learning para a redução da taxa de cancelamento (churn) da operadora, conectando o modelo aos objetivos de negócio e servindo como fundação para a Fase 1 do Tech Challenge.

## 1. Proposta de Valor (Value Proposition)
A operadora de telecomunicações está sofrendo com uma alta taxa de evasão de clientes (Churn). 
* **Objetivo:** Identificar proativamente os clientes com alto risco de cancelamento.
* **Impacto esperado:** Permitir que a equipe atue de forma direcionada com ofertas e incentivos, reduzindo a perda de receita (aumentando o LTV).

## 2. Stakeholders e Usuários
* **Diretoria Executiva (Patrocinadores):** Focada em ROI, redução de custos e na saúde financeira/redução do churn rate.
* **Equipe de Retenção e Marketing (Usuários Finais):** Utilizarão as predições para direcionar campanhas e aplicar ofertas de retenção.
* **Equipe de ML Engineering:** Responsáveis pelo desenvolvimento, deploy e manutenção do pipeline preditivo.

## 3. Tarefa de ML e Variável Alvo
* **Tipo:** Classificação Binária (Prever a probabilidade de 0 a 100% de um cliente cancelar o serviço - `Churn=Yes`).
* **Método Central:** Rede Neural MLP (PyTorch) comparada com baselines mais simples (Scikit-Learn).

## 4. Fontes de Dados (Data Collection)
* **Dataset:** IBM Telco Customer Churn (público).
* **Características:** Arquivo `dataset.csv` com 21 features e ~7000 registros, englobando dados demográficos, serviços assinados e informações financeiras/contratuais.

## 5. Decisões e Ações
* **Ação de Negócio:** Os clientes serão rankeados pela probabilidade de evasão. Se a probabilidade superar um limiar de decisão (*threshold*), o cliente entra automaticamente no fluxo de retenção.
* **Trade-off:** O threshold será otimizado minimizando *Falsos Negativos* (perder o cliente sem tentar intervir) e *Falsos Positivos* (dar descontos para quem não ia cancelar, perdendo apenas a margem do desconto).
* **Integração:** O modelo será servido via API (FastAPI) para consumo pelo CRM da operadora.

## 6. Métricas de Avaliação
### 6.1 Métricas de Negócio
* **Custo de Churn Evitado:** Receita mantida menos o custo das campanhas de retenção proativa.
* **Taxa de Retenção:** Porcentagem de clientes "em risco" que não cancelaram após a intervenção.

### 6.2 Métricas Técnicas
* **AUC-ROC:** Métrica principal de separabilidade (capacidade do modelo rankear os clientes de maior risco corretamente).
* **PR-AUC e F1-Score:** Importantes devido ao provável desbalanceamento de classes na base real.

## 7. SLOs - Objetivos de Nível de Serviço
* **Latência de Inferência:** Resposta da API em menos de 200ms por requisição.
* **Disponibilidade (Uptime):** API funcional 99.5% do tempo.
* **Frequência de Retreinamento:** Inicialmente mensal, ou de forma reativa conforme degradação da performance detectada no monitoramento.

## 8. Coleta e Pré-processamento
* **Limpeza:** Tratamento de valores ausentes e outliers detectados na análise exploratória (EDA).
* **Feature Engineering:** Codificação de variáveis categóricas (OneHot/Label Encoding) e normalização (Scaling) de numéricas.
* **Split:** Separação estratificada (Treino, Validação e Teste) para garantir representatividade do churn.

## 9. Avaliação Offline e Tracking
* **Ferramenta:** MLflow para registro completo de experimentos, parâmetros e métricas.
* **Baseline:** Comparação obrigatória com a "Régua de Corte" (DummyClassifier e LogisticRegression).
* **Validação:** Validação cruzada estratificada (Stratified CV) para atestar a generalização do modelo.
