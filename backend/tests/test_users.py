"""
Pruebas para los endpoints de usuarios.
"""
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_users_unauthorized():
    """Valida que un usuario no autenticado no pueda acceder a la lista de usuarios."""
    response = client.get("/api/v1/users/")
    assert response.status_code == 401
    # El mensaje exacto puede variar según la implementación de OAuth2PasswordBearer, 
    # pero normalmente es "Not authenticated".
    # En app/api/deps.py lanzamos 403 "Could not validate credentials" si el token es invalido,
    # pero si no se envia token, FastAPI lanza 401.
    assert response.json() == {"detail": "Not authenticated"}
