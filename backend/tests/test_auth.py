from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_login_access_token_success() -> None:
    """Prueba de inicio de sesión exitoso y obtención de token."""
    response = client.post(
        "/api/v1/auth/login/access-token",
        data={"username": "admin@empresa.com", "password": "AdminSystem_2024!"}
    )
    assert response.status_code == 200
    content = response.json()
    assert "access_token" in content
    assert content["token_type"] == "bearer"

def test_login_access_token_failure() -> None:
    """Prueba de inicio de sesión fallido con credenciales incorrectas."""
    response = client.post(
        "/api/v1/auth/login/access-token",
        data={"username": "admin@empresa.com", "password": "wrongpassword"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Email o contraseña incorrectos"
