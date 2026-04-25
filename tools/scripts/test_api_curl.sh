#!/bin/bash

# Define a URL base. Usa o primeiro argumento passado, ou http://localhost:8000 como padrão
BASE_URL=${1:-http://localhost:8000}

echo "=========================================================="
echo "🚀 Iniciando testes cURL contra a API: $BASE_URL"
echo "=========================================================="
echo ""

# 1. Teste de Health Check
echo "----------------------------------------------------------"
echo "🟢 1. Teste de Health Check (GET /health)"
echo "----------------------------------------------------------"
curl -s -X GET "$BASE_URL/health" | jq || curl -s -X GET "$BASE_URL/health"
echo -e "\n"

# 2. Teste de Predição de Churn (Payload Válido)
echo "----------------------------------------------------------"
echo "🔵 2. Predição de Churn - Payload Válido (POST /v1/predict)"
echo "----------------------------------------------------------"
curl -s -X POST "$BASE_URL/v1/predict" \
  -H "Content-Type: application/json" \
  -d '{
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
  }' | jq || curl -s -X POST "$BASE_URL/v1/predict" \
  -H "Content-Type: application/json" \
  -d '{
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
echo "🔴 3. Validação de Erro - Falta 'MonthlyCharges' (POST /v1/predict)"
echo "----------------------------------------------------------"
curl -s -X POST "$BASE_URL/v1/predict" \
  -H "Content-Type: application/json" \
  -d '{
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
  }' | jq || curl -s -X POST "$BASE_URL/v1/predict" \
  -H "Content-Type: application/json" \
  -d '{
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
