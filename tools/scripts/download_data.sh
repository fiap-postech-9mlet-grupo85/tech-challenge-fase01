#!/bin/bash

# Este script realiza o download da base sugerida (Telco Customer Churn - IBM)
# e aloca o arquivo CSV dentro da pasta data/raw.

URL="https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv"
OUTPUT_DIR="data/raw"
OUTPUT_FILE="${OUTPUT_DIR}/dataset.csv"

echo "Criando diretório ${OUTPUT_DIR} se não existir..."
mkdir -p "${OUTPUT_DIR}"

echo "Iniciando download do dataset Telco Customer Churn..."
curl -sS -L "${URL}" -o "${OUTPUT_FILE}"

if [ -f "${OUTPUT_FILE}" ]; then
    echo "Download concluído com sucesso!"
    echo "Arquivo salvo em: ${OUTPUT_FILE}"
else
    echo "Erro: falha no download do dataset."
    exit 1
fi
