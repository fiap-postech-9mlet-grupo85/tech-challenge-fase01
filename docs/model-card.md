# Model Card: Telco Churn Predictor

## 1. Detalhes do Modelo
* **Nome do Modelo:** Telco Churn MLP (PyTorch)
* **Desenvolvedores:** Grupo 32 (FIAP Pós Tech)
* **Tipo do Modelo:** Rede Neural Densa (Feed-Forward Neural Network) para Classificação Binária.
* **Versão:** 1.0.0
* **Data da Modelagem:** Abril de 2026
* **Licença:** MIT
* **Dúvidas Técnicas:** Repositório do projeto

## 2. Uso Pretendido (Intended Use)
* **Uso Primário:** Identificar se um cliente de telefonia/internet tem alto risco de cancelar sua assinatura (Churn = Yes). 
* **Caso de Uso de Negócio:** A saída deste modelo alimenta diretamente o sistema de CRM da operadora. Clientes classificados como alto risco receberão ações de retenção automatizadas (ex: e-mail oferecendo desconto de R$ 50).
* **Uso Fora de Escopo:** Este modelo não prevê o *Life-Time Value (LTV)* do cliente, tampouco deve ser usado para aprovação de crédito.

## 3. Fatores e Grupos
* **Variáveis Demográficas Sensíveis:** O modelo utiliza as colunas `gender` (Gênero) e `SeniorCitizen` (Se é idoso). O uso de dados demográficos exige atenção para garantir que a política de descontos e retenção não seja discriminatória.
* **Viés Potencial:** Clientes com `Contract = Month-to-month` têm probabilidade de churn naturalmente inflada pelo histórico de dados, o que pode gerar viés de predição em detrimento a clientes fidelizados de longo prazo.

## 4. Métricas e Limiares (Thresholds)
A validação do modelo foi focada no custo financeiro do negócio.
* **Métrica Principal Otimizada:** `Recall` (Sensibilidade). Escolhida para mitigar Falsos Negativos (deixar um cliente cancelar sem oferecer retenção).
* **Limiar de Negócio (Business Threshold):** `0.30` (30%). 
    * *Justificativa:* Definido no ML Canvas. O custo de perder o cliente (R$ 1.000) é 20x maior que o custo de tentar retê-lo (R$ 50). Um threshold baixo aumenta a abrangência defensiva da operadora.
* **Métricas de Performance (Validação Cruzada):**
    * **AUC-ROC:** ~0.84
    * **PR-AUC:** ~0.65
    * **Recall (no limiar ótimo):** ~0.80

## 5. Dados de Treinamento e Avaliação
* **Origem dos Dados:** IBM Telco Customer Churn Dataset.
* **Volume:** 7.043 instâncias originais.
* **Divisão de Validação:** Stratified Holdout (80% Treino / 20% Teste). O `stratify=y` garantiu a mesma proporção de Churn em ambos os conjuntos.
* **Pré-Processamento:** 
    * `TotalCharges`: Conversão de *blank strings* para `0.0`.
    * Imputação via `ColumnTransformer` (StandardScaler para numéricas e OneHotEncoder para categóricas).
    * `pos_weight`: O dataset possui desbalanceamento severo (~73% No Churn / 27% Yes Churn). O PyTorch utiliza o cálculo dinâmico de `pos_weight` na `BCEWithLogitsLoss` para compensar as classes.

## 6. Advertências e Recomendações
* **Revisão de Limiar:** Caso o ticket médio da operadora suba ou o custo de retenção mude, a matriz de custos descrita no ML Canvas se tornará obsoleta, e o Threshold de `0.30` no `predict_model.py` deve ser recalibrado.
* **Falsos Positivos:** Com o threshold baixo, o modelo vai errar prevendo Churn para clientes que não pretendiam sair. A equipe de marketing deve garantir que a "ação de retenção" oferecida não cause perda injustificada de receita (Cannibalization).
