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

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()