"""
Punto de entrada de FastAPI y endpoints base.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.routers import auth
from app.api.routers import users

app = FastAPI(
    title=settings.project_name,
    version=settings.version,
    description="API para el Sistema de Control de Inventario"
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todos los orígenes en desarrollo
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, etc.)
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])

@app.get("/api/v1/health-check", tags=["System"])
def health_check() -> dict[str, str]:
    """Endpoint para verificar el estado del servidor."""
    return {
        "status": "ok",
        "message": "Servidor funcionando correctamente",
        "version": settings.version
    }
