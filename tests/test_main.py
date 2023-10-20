"""Test main"""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_hello():
    """Test welcome endpoint"""
    response = client.get('/')
    assert response.status_code == 200
    assert 'application/json' in response.headers['content-type']
    assert response.json()["message"] == "Hello! This is the Iris predictor."


def test_predict():
    """Test prediction"""
    response = client.post("/predict", json={
        "sepal_length": 0,
        "sepal_width": 0,
        "petal_length": 0,
        "petal_width": 0
    })

    assert response.status_code == 200
    assert response.json()["result"] == 0
