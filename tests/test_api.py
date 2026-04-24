from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)

# JSON de cliente perfeito
valid_payload = {
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
    "TotalCharges": "29.85",
}


def test_health_endpoint():
    """Garante que a rota de monitoramento responde 200 OK."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "service": "telco-churn-api"}


def test_predict_success():
    """Garante que um payload correto retorna a predição da Rede Neural com código 200."""
    response = client.post("/predict", json=valid_payload)

    assert response.status_code == 200
    data = response.json()
    assert "churn_prediction" in data
    assert "probability" in data
    assert "threshold_used" in data
    assert data["threshold_used"] == 0.30


def test_predict_validation_error():
    """Garante que o Pydantic intercepta requisições faltando campos vitais (HTTP 422)."""
    invalid_payload = valid_payload.copy()
    del invalid_payload["MonthlyCharges"]  # Remove campo numérico obrigatório

    response = client.post("/predict", json=invalid_payload)

    # 422 Unprocessable Entity é a resposta padrão do FastAPI/Pydantic
    assert response.status_code == 422
    assert "detail" in response.json()
