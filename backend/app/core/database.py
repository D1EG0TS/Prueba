"""
Configuración de SQLAlchemy y conexión a PostgreSQL.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.core.config import settings

engine = create_engine(settings.database_url, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db() -> getattr(SessionLocal, "__class__"): # type: ignore
    """Generador para obtener y cerrar de forma segura la sesión de BD."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()