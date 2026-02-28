from fastapi.testclient import TestClient
from app.main import app
import random
import string

client = TestClient(app)

def random_string(length=10):
    return ''.join(random.choices(string.ascii_lowercase, k=length))

def test_register_user() -> None:
    """Prueba de registro de usuario exitoso."""
    email = f"{random_string()}@example.com"
    password = "TestPassword123!"
    first_name = "Test"
    last_name = "User"
    
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "password": password,
            "first_name": first_name,
            "last_name": last_name,
            "role_id": 1 # Intentamos ser Super Admin
        }
    )
    
    assert response.status_code == 200
    content = response.json()
    assert content["email"] == email
    assert content["first_name"] == first_name
    assert content["last_name"] == last_name
    assert content["role_id"] == 5 # Debe ser forzado a 5 (Visitante)
    assert "id" in content

def test_register_existing_email() -> None:
    """Prueba de registro con email existente."""
    # Primero registramos uno
    email = f"{random_string()}@example.com"
    password = "TestPassword123!"
    
    response1 = client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "password": password,
            "first_name": "Test",
            "last_name": "User"
        }
    )
    assert response1.status_code == 200
    
    # Intentamos registrar de nuevo
    response2 = client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "password": password,
            "first_name": "Test",
            "last_name": "User"
        }
    )
    assert response2.status_code == 400
    assert response2.json()["detail"] == "El email ya está registrado"
