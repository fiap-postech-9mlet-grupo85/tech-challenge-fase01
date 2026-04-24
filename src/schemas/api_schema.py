from typing import Optional

from pydantic import BaseModel, Field


class CustomerRequest(BaseModel):
    """
    Schema Pydantic para a porta de entrada do FastAPI.
    Valida a tipagem básica do JSON submetido no endpoint /predict.
    Se o cliente esquecer de mandar uma coluna obrigatória, o FastAPI
    rejeitará a requisição automaticamente (HTTP 422 Unprocessable Entity).
    """

    gender: str = Field(..., description="Gênero do cliente (Female/Male)")
    SeniorCitizen: int = Field(..., description="Se é idoso (1) ou não (0)")
    Partner: str = Field(..., description="Se possui parceiro (Yes/No)")
    Dependents: str = Field(..., description="Se possui dependentes (Yes/No)")
    tenure: int = Field(..., description="Meses de permanência na empresa")
    PhoneService: str = Field(..., description="Possui serviço de telefone? (Yes/No)")
    MultipleLines: str = Field(..., description="Possui múltiplas linhas?")
    InternetService: str = Field(..., description="Tipo de serviço de internet")
    OnlineSecurity: str = Field(..., description="Possui segurança online?")
    OnlineBackup: str = Field(..., description="Possui backup online?")
    DeviceProtection: str = Field(..., description="Possui proteção de dispositivo?")
    TechSupport: str = Field(..., description="Possui suporte técnico?")
    StreamingTV: str = Field(..., description="Possui streaming de TV?")
    StreamingMovies: str = Field(..., description="Possui streaming de filmes?")
    Contract: str = Field(..., description="Tipo de contrato")
    PaperlessBilling: str = Field(..., description="Possui fatura digital? (Yes/No)")
    PaymentMethod: str = Field(..., description="Método de pagamento")
    MonthlyCharges: float = Field(..., description="Cobrança mensal")
    TotalCharges: Optional[str] = Field(
        None,
        description="Cobrança total acumulada (pode ser enviada como string ou nula)",
    )
