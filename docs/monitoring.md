# Plano de Monitoramento Pós-Deploy

A implementação de Machine Learning não termina no Deploy. Com o tempo, os dados de produção mudam, alterando o comportamento do modelo. Este documento estabelece as diretrizes de governança e as métricas vitais a serem monitoradas (Observabilidade MLOps) para o modelo de Churn.

## 1. Monitoramento de Qualidade de Serviço (System Health)
Monitorar se a infraestrutura da API (`src/main.py`) está de pé e responsiva.
* **Latency (P99):** O tempo de resposta do endpoint `/predict` deve se manter abaixo de `200ms` para não gerar timeout no sistema de CRM.
* **Error Rate (HTTP 5xx):** Monitorar exceções de código ou quebras no carregamento dos tensores PyTorch. Tolerância: `< 0.1%`.
* **Validation Rejections (HTTP 422):** Alta taxa de erros do Pydantic/Pandera indica que o *upstream* (sistema que envia os dados para a API) mudou o formato do JSON sem nos avisar. **Ação:** Disparar alerta imediato no Slack da Engenharia de Dados.

## 2. Monitoramento de Qualidade de Dados (Data Drift)
As características dos novos clientes estão mudando em relação ao dataset de treinamento original da IBM?
* **Distribuição de Contratos (`Contract`):** Se a proporção de contratos "Month-to-month" subir drasticamente, a distribuição da base mudou, e o modelo pode tender a sobreestimar o Churn.
* **Distribuição de Custo (`MonthlyCharges`):** Testes estatísticos contínuos (ex: Kolmogorov-Smirnov) para avaliar se o ticket médio mudou. Inflação ou mudança nos planos de celular afetam fortemente esse número.
* **Taxa de Nulos Imputados (`TotalCharges`):** Monitorar se a quantidade de novos clientes com zero de tempo de casa (`tenure=0`) cresceu desproporcionalmente.

## 3. Monitoramento de Conceito (Concept Drift)
O padrão que define o que é um Churn mudou?
* **Taxa de Predição vs Churn Real:** 
    * Se o modelo prevê mensalmente que 30% da base sofrerá Churn, mas ao final do mês apenas 10% efetivamente cancela (após cruzar com a base de *Ground Truth* do negócio), o limite de decisão do modelo ou o comportamento social mudou.
* **Erosão do Recall:** O negócio precisa que o modelo retenha seu Recall em no mínimo ~80%. Mensalmente, deve-se gerar uma matriz de confusão real usando os dados consolidados do faturamento. Se o Recall cair abaixo de 75%, deve-se disparar o gatilho de **Retreinamento Automatizado**.

## 4. Arquitetura de Monitoramento Sugerida
Para habilitar esta observabilidade corporativa nas próximas fases do projeto, a stack sugerida é:
* **Log Ingestion:** Exportar o `logging` nativo do FastAPI para ferramentas como Datadog ou ELK Stack (Elasticsearch, Logstash, Kibana).
* **Drift Detection:** Instalação do framework `Evidently AI` acoplado ao MLflow para desenhar relatórios visuais automáticos de Data Drift e Model Drift comparando a base de teste vs base de produção mensal.
* **Alerting:** PagerDuty integrado ao Grafana para contatar o Cientista de Dados de plantão em caso de degradação da performance.
