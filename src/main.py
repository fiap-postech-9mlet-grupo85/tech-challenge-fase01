import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, APIRouter
from fastapi.responses import JSONResponse

from src.models.predict_model import load_artifacts, predict_churn
from src.schemas.api_schema import CustomerRequest

# Instancia o logger configurado na Etapa 3
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    O Lifespan Events do FastAPI nos permite executar código ANTES de aceitar a primeira requisição.
    Isso é crítico em MLOps (Cold Start). Vamos carregar as pesadas matrizes do PyTorch (.pth)
    e o Scikit-Learn (.joblib) diretamente na RAM do servidor aqui.
    """
    logger.info(
        "Iniciando FastAPI... Puxando pesos do PyTorch para a RAM (Cold Start Optimization)"
    )
    try:
        load_artifacts()
        logger.info("Artefatos de Inteligência Artificial carregados com sucesso!")
    except Exception as e:
        logger.error(f"Falha Crítica ao carregar os modelos: {e}")
        # A API pode subir mesmo falhando, mas o /health alertará sobre o erro.

    yield  # O servidor passa a aceitar requisições

    logger.info("Desligando API. Liberando memória RAM.")


# Instancia a aplicação FastAPI injetando o Lifespan
app = FastAPI(
    title="Telco Churn API",
    description="API de Inferência de Churn baseada em Redes Neurais Densa (PyTorch)",
    version="1.0.0",
    lifespan=lifespan,
)


# Cria o Router da Versão 1 (v1)
v1_router = APIRouter(prefix="/v1")

@app.get("/health", tags=["Monitoring"])
def health_check():
    """
    Rota de monitoramento de saúde do microsserviço.
    Utilizada por Load Balancers e Kubernetes para atestar se a API está viva.
    """
    return {"status": "healthy", "service": "telco-churn-api"}


@v1_router.post("/predict", tags=["Inference"])
def predict(customer: CustomerRequest):
    """
    Rota de Predição em Tempo Real (Versão 1).
    Recebe o JSON do cliente (validado pelo Pydantic), injeta no modelo (Pandera + PyTorch),
    e retorna o booleano de churn considerando o Custo Financeiro (Threshold 30%).
    """
    try:
        # Pydantic converte a entrada em dicionário python nativo
        raw_dict = customer.model_dump()

        # Envia para o motor de inferência que desenhamos na Etapa 3.1
        resultado = predict_churn(raw_dict)
        return JSONResponse(content=resultado)

    except ValueError as ve:
        # Erros mapeados (ex: Schema Pandera falhou) viram Bad Request ou Unprocessable Entity
        logger.warning(f"Requisição rejeitada por validação do Motor ML: {ve}")
        raise HTTPException(status_code=422, detail=str(ve))
    except Exception as e:
        # Erros não mapeados (ex: PyTorch quebrou a matriz) viram Internal Server Error 500
        logger.error(f"Internal Server Error no Forward Pass: {e}")
        raise HTTPException(status_code=500, detail="Erro interno no Motor de Predição")

# Registra o Router v1 no App Principal
app.include_router(v1_router)
