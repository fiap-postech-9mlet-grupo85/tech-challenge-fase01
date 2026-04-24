# Machine Learning Canvas: Previsão de Churn Telco

Este documento descreve a estratégia de Machine Learning para a redução da taxa de cancelamento (churn) da operadora, conforme os requisitos da Fase 1 do Tech Challenge.

## 1. Proposta de Valor (Value Proposition)
* **Problema de Negócio:** A operadora está perdendo clientes em ritmo acelerado.
* **Objetivo:** Identificar clientes com alta probabilidade de cancelamento para permitir ações proativas de retenção.
* **Impacto esperado:** Redução do churn e aumento do LTV (Lifetime Value) do cliente.

## 2. Stakeholders e Usuários
* **Diretoria:** Interessada na redução de custos e saúde financeira da empresa.
* **Equipe de Marketing/Retenção:** Usuários finais que aplicarão as ofertas nos clientes listados pelo modelo.
* **Equipe de ML Engineering:** Responsáveis pelo desenvolvimento, deploy e manutenção do pipeline.

## 3. Tarefa de ML (ML Task)
* **Tipo:** Classificação Binária (Churn: Sim ou Não).
* **Método:** Rede Neural MLP (PyTorch) comparada com baselines de Scikit-Learn.

## 4. Dados (Data Sources)
* **Dataset:** IBM Telco Customer Churn (público).
* **Características:** Dados tabulares com ≥ 5.000 registros e ≥ 10 features (demográficos, serviços contratados e informações financeiras).

## 5. Decisões e Ações (Decisions)
* **Ação de Negócio:** Se a probabilidade de churn superar um limiar de decisão (*threshold*) — que será otimizado na Etapa 2 com base na análise de trade-off entre o custo financeiro de Falsos Positivos (dar descontos desnecessários) vs. Falsos Negativos (perder o cliente) —, o cliente entra automaticamente em uma lista para receber uma oferta de retenção personalizada, como descontos ou upgrades.
* **Integração:** O modelo será servido via API (FastAPI) para que o sistema de CRM da operadora possa consumir as predições em tempo real ou em lote.

## 6. Métricas de Avaliação
### Métricas Técnicas
* **AUC-ROC:** Para avaliar a capacidade de separação entre as classes.
* **PR-AUC:** Importante devido ao possível desbalanceamento de classes no churn.
* **F1-Score:** Equilíbrio entre precisão e sensibilidade (Recall).
### Métricas de Negócio
* **Custo de Churn Evitado:** Receita mantida menos o custo das campanhas de retenção.
* **Taxa de Retenção:** Porcentagem de clientes "em risco" que não cancelaram após a intervenção.

## 7. SLOs - Objetivos de Nível de Serviço
* **Latência de Inferência:** Resposta da API em menos de 200ms por requisição.
* **Disponibilidade (Uptime):** API funcional 99.5% do tempo.
* **Frequência de Retreinamento:** Inicialmente mensal ou conforme degradação da performance detectada.

## 8. Coleta e Pré-processamento
* **Limpeza:** Tratamento de valores ausentes e outliers detectados na EDA.
* **Feature Engineering:** Codificação de variáveis categóricas (OneHot/Label Encoding) e normalização de variáveis numéricas.
* **Split:** Separação estratificada entre treino, validação e teste.

## 9. Avaliação Offline e Tracking
* **Ferramenta:** MLflow para registro de experimentos, parâmetros e métricas.
* **Baseline:** Comparação obrigatória com `DummyClassifier` e Regressão Logística.
* **Validação:** Validação cruzada estratificada para garantir robustez.
