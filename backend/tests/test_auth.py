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
    assert "refresh_token" in content
    assert content["token_type"] == "bearer"

def test_login_access_token_failure() -> None:
    """Prueba de inicio de sesión fallido con credenciales incorrectas."""
    response = client.post(
        "/api/v1/auth/login/access-token",
        data={"username": "admin@empresa.com", "password": "wrongpassword"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Email o contraseña incorrectos"

def test_get_user_sessions() -> None:
    """Prueba para obtener las sesiones activas del usuario."""
    # 1. Login para obtener el token
    login_response = client.post(
        "/api/v1/auth/login/access-token",
        data={"username": "admin@empresa.com", "password": "AdminSystem_2024!"}
    )
    assert login_response.status_code == 200
    token_data = login_response.json()
    access_token = token_data["access_token"]
    
    # 2. Consultar sesiones
    response = client.get(
        "/api/v1/auth/sessions",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    sessions = response.json()
    assert isinstance(sessions, list)
    assert len(sessions) > 0
    assert "refresh_token" in sessions[0]
    assert "ip_address" in sessions[0]
