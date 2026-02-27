"""
Punto de entrada de FastAPI y endpoints base.
"""
from fastapi import FastAPI
from app.core.config import settings
from app.api.routers import auth

app = FastAPI(
    title=settings.project_name,
    version=settings.version,
    description="API para el Sistema de Control de Inventario"
)

app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])

@app.get("/api/v1/health-check", tags=["System"])
def health_check() -> dict[str, str]:
    """Endpoint para verificar el estado del servidor."""
    return {
        "status": "ok",
        "message": "Servidor funcionando correctamente",
        "version": settings.version
    }
