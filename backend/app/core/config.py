"""
Módulo de configuración central.
Carga las variables de entorno utilizando Pydantic.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Clase para manejar las configuraciones de la aplicación."""
    project_name: str = "Sistema de Inventario API"
    version: str = "1.0.0"
    database_url: str
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    refresh_token_expire_days: int = 7

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
