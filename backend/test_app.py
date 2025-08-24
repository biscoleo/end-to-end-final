from fastapi.testclient import TestClient
from app import app
from dotenv import load_dotenv

load_dotenv()

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_predict():
    data = {"text": "you're so cool", "true_label": "0"}
    response = client.post("/predict", json=data)
    assert response.status_code == 200
    assert "prediction" in response.json()
