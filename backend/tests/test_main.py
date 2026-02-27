"""
Pruebas unitarias para los endpoints base de la API.
"""
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check() -> None:
    """Valida que el endpoint health-check devuelva un status 200 y JSON correcto."""
    response = client.get("/api/v1/health-check")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "ok"
    assert "version" in data