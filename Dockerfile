# Usar imagem base leve e estável (Debian slim)
FROM python:3.10-slim

# Define o diretório de trabalho no container
WORKDIR /app

# Variáveis de ambiente para o Python (não gerar arquivos .pyc e não bufferizar stdout/stderr)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instala dependências do sistema necessárias para compilar pacotes (como pandas/torch)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copia os arquivos de dependência primeiro para aproveitar o cache de layers do Docker
COPY pyproject.toml setup.py /app/

# Instala as dependências via pip
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -e .

# Copia o código-fonte e os modelos binários
# A pasta models/ é OBRIGATÓRIA pois contém preprocessor.joblib e churn_mlp.pth
COPY src/ /app/src/
COPY models/ /app/models/

# Expor a porta que o FastAPI vai rodar
EXPOSE 8000

# Comando para iniciar o servidor Uvicorn usando o código empacotado no src/main.py
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
