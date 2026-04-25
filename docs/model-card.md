# Model Card: Telco Churn Predictor

## 1. Detalhes do Modelo
* **Nome do Modelo:** Telco Churn MLP (PyTorch)
* **Desenvolvedores:** Grupo 32 (FIAP Pós Tech)
* **Tipo do Modelo:** Rede Neural Densa (Feed-Forward Neural Network) para Classificação Binária.
* **Arquitetura (Camadas):** `Input Dim -> Linear(64) -> ReLU -> Dropout(p=0.3) -> Linear(32) -> ReLU -> Dropout(p=0.3) -> Linear(1)`
* **Função de Perda (Loss):** `BCEWithLogitsLoss` (Binary Cross Entropy) com parâmetro `pos_weight` calculado dinamicamente para compensar o desbalanceamento de classes nativo.
* **Otimizador & Hiperparâmetros:** Algoritmo `Adam` com Learning Rate de `0.001` e Batch Size de `64` (definidos via Grid Search). Treinamento regularizado com Early Stopping (Patience = 10 épocas).
* **Versão:** 1.0.0
* **Data da Modelagem:** Abril de 2026
* **Licença:** MIT

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
    * *Justificativa:* Definido no ML Canvas. O custo de perder o cliente (R$ 1.000) é 20x maior que o custo de tentar retê-lo (R$ 50). Um threshold baixo aumenta a abrangência defensiva da operadora, penalizando precisão em favor do recall.
* **Métricas de Performance (Resultados do Grid Search no Test Set):**
    * **AUC-ROC:** `0.8459`
    * **F1-Score Máximo:** `0.6311`
    * **Recall (no limiar ótimo):** `0.8075` (80.75% dos clientes prestes a cancelar foram identificados corretamente).

## 5. Dados de Treinamento e Avaliação
* **Origem dos Dados:** IBM Telco Customer Churn Dataset.
* **Volume:** 7.043 instâncias originais.
* **Divisão de Validação:** Stratified Holdout (80% Treino / 20% Teste). O parâmetro `stratify=y` do Scikit-Learn garantiu a mesma proporção de Churn (~27%) em ambos os conjuntos, vital para a estabilidade da métrica AUC.
* **Engenharia de Features e Pipeline de Pré-Processamento:** 
    * Tratamento de anomalias: Coluna `TotalCharges` convertida para numérico com coerção de *blank strings* para nulo, sendo posteriormente imputada.
    * Orquestração via `ColumnTransformer`: Todas as features numéricas (`tenure`, `MonthlyCharges`, `TotalCharges`) sofreram padronização via `StandardScaler`. Todas as categóricas (ex: `Contract`, `InternetService`) foram binadas via `OneHotEncoder(drop='first')` para evitar colinearidade.
    * A estrutura final alimentou a rede neural PyTorch (instanciada dinamicamente com `input_dim` igual ao formato gerado pós-OneHotEncoder).
* **Desbalanceamento:** O dataset possui desbalanceamento severo (~73% No Churn / 27% Yes Churn). Ao invés de usar técnicas artificiais (SMOTE), o PyTorch utilizou o cálculo dinâmico estatístico inserido na matriz da `BCEWithLogitsLoss` (`pos_weight`) para atribuir maior peso no gradiente aos Falsos Negativos durante a retropropagação.

## 6. Advertências e Recomendações
* **Revisão de Limiar:** Caso o ticket médio da operadora suba ou o custo de retenção mude, a matriz de custos descrita no ML Canvas se tornará obsoleta, e o Threshold de `0.30` no `predict_model.py` deve ser recalibrado.
* **Falsos Positivos:** Com o threshold baixo, o modelo vai errar prevendo Churn para clientes que não pretendiam sair. A equipe de marketing deve garantir que a "ação de retenção" oferecida não cause perda injustificada de receita (Cannibalization).
