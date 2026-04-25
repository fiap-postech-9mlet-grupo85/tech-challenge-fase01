#!/bin/bash

# Define a URL base. Usa o primeiro argumento passado, ou http://localhost:8000 como padrão
BASE_URL=${1:-http://localhost:8000}

echo "=========================================================="
echo "🚀 Iniciando testes WGET contra a API: $BASE_URL"
echo "=========================================================="
echo ""

# 1. Teste de Health Check
echo "----------------------------------------------------------"
echo "🟢 1. Teste de Health Check (GET /health)"
echo "----------------------------------------------------------"
wget -qO- "$BASE_URL/health" | jq || wget -qO- "$BASE_URL/health"
echo -e "\n"

# 2. Teste de Predição de Churn (Payload Válido)
echo "----------------------------------------------------------"
echo "🔵 2. Predição de Churn - Payload Válido (POST /predict)"
echo "----------------------------------------------------------"
wget -qO- "$BASE_URL/predict" \
  --header="Content-Type: application/json" \
  --post-data='{
    "gender": "Female",
    "SeniorCitizen": 0,
    "Partner": "Yes",
    "Dependents": "No",
    "tenure": 1,
    "PhoneService": "No",
    "MultipleLines": "No phone service",
    "InternetService": "DSL",
    "OnlineSecurity": "No",
    "OnlineBackup": "Yes",
    "DeviceProtection": "No",
    "TechSupport": "No",
    "StreamingTV": "No",
    "StreamingMovies": "No",
    "Contract": "Month-to-month",
    "PaperlessBilling": "Yes",
    "PaymentMethod": "Electronic check",
    "MonthlyCharges": 29.85,
    "TotalCharges": "29.85"
  }' | jq || wget -qO- "$BASE_URL/predict" \
  --header="Content-Type: application/json" \
  --post-data='{
    "gender": "Female",
    "SeniorCitizen": 0,
    "Partner": "Yes",
    "Dependents": "No",
    "tenure": 1,
    "PhoneService": "No",
    "MultipleLines": "No phone service",
    "InternetService": "DSL",
    "OnlineSecurity": "No",
    "OnlineBackup": "Yes",
    "DeviceProtection": "No",
    "TechSupport": "No",
    "StreamingTV": "No",
    "StreamingMovies": "No",
    "Contract": "Month-to-month",
    "PaperlessBilling": "Yes",
    "PaymentMethod": "Electronic check",
    "MonthlyCharges": 29.85,
    "TotalCharges": "29.85"
  }'
echo -e "\n"

# 3. Teste de Predição de Churn (Payload Inválido - Erro 422)
echo "----------------------------------------------------------"
echo "🔴 3. Validação de Erro - Falta 'MonthlyCharges' (POST /predict)"
echo "----------------------------------------------------------"
# Usamos --content-on-error no wget para que ele printe a mensagem de erro HTTP (ex: 422 Unprocessable Entity)
wget -qO- --content-on-error "$BASE_URL/predict" \
  --header="Content-Type: application/json" \
  --post-data='{
    "gender": "Female",
    "SeniorCitizen": 0,
    "Partner": "Yes",
    "Dependents": "No",
    "tenure": 1,
    "PhoneService": "No",
    "MultipleLines": "No phone service",
    "InternetService": "DSL",
    "OnlineSecurity": "No",
    "OnlineBackup": "Yes",
    "DeviceProtection": "No",
    "TechSupport": "No",
    "StreamingTV": "No",
    "StreamingMovies": "No",
    "Contract": "Month-to-month",
    "PaperlessBilling": "Yes",
    "PaymentMethod": "Electronic check",
    "TotalCharges": "29.85"
  }' | jq || wget -qO- --content-on-error "$BASE_URL/predict" \
  --header="Content-Type: application/json" \
  --post-data='{
    "gender": "Female",
    "SeniorCitizen": 0,
    "Partner": "Yes",
    "Dependents": "No",
    "tenure": 1,
    "PhoneService": "No",
    "MultipleLines": "No phone service",
    "InternetService": "DSL",
    "OnlineSecurity": "No",
    "OnlineBackup": "Yes",
    "DeviceProtection": "No",
    "TechSupport": "No",
    "StreamingTV": "No",
    "StreamingMovies": "No",
    "Contract": "Month-to-month",
    "PaperlessBilling": "Yes",
    "PaymentMethod": "Electronic check",
    "TotalCharges": "29.85"
  }'
echo -e "\n"
echo "=========================================================="
echo "✅ Testes concluídos!"
echo "=========================================================="
