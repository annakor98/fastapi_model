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
