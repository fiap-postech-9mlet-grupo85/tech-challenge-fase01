import pandera.pandas as pa
from pandera.typing import Series


class CustomerSchema(pa.DataFrameModel):
    """
    Contrato rigoroso de dados para o modelo de Churn.
    Garante que qualquer JSON injetado na API possua os tipos e colunas exatos que a
    Rede Neural espera.
    """

    gender: Series[str] = pa.Field(isin=["Female", "Male"])
    SeniorCitizen: Series[int] = pa.Field(isin=[0, 1])
    Partner: Series[str] = pa.Field(isin=["Yes", "No"])
    Dependents: Series[str] = pa.Field(isin=["Yes", "No"])
    tenure: Series[int] = pa.Field(ge=0)
    PhoneService: Series[str] = pa.Field(isin=["Yes", "No"])
    MultipleLines: Series[str]
    InternetService: Series[str]
    OnlineSecurity: Series[str]
    OnlineBackup: Series[str]
    DeviceProtection: Series[str]
    TechSupport: Series[str]
    StreamingTV: Series[str]
    StreamingMovies: Series[str]
    Contract: Series[str]
    PaperlessBilling: Series[str] = pa.Field(isin=["Yes", "No"])
    PaymentMethod: Series[str]
    MonthlyCharges: Series[float] = pa.Field(ge=0.0)
    TotalCharges: Series[str] = pa.Field(
        nullable=True
    )  # Aceita string pois tratamos no pipeline

    class Config:
        coerce = True
        strict = False  # Permite que o dicionário venha com "customerID", mas nós o ignoraremos.
