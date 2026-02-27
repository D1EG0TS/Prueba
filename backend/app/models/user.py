""" 
Modelo de base de datos para los Usuarios del sistema. 
""" 
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime 
from sqlalchemy.orm import relationship 
from app.core.database import Base 
from datetime import datetime, timezone 

class User(Base): 
    __tablename__ = "users" 

    id = Column(Integer, primary_key=True, index=True) 
    email = Column(String(255), unique=True, index=True, nullable=False) 
    hashed_password = Column(String(255), nullable=False) 
    
    # Nuevos campos de perfil 
    first_name = Column(String(50), nullable=False) 
    last_name = Column(String(50), nullable=False) 
    phone_number = Column(String(20), nullable=True) 
    # Guarda la ruta local o URL de la nube, no el archivo binario (Regla 14) 
    profile_picture = Column(String(255), nullable=True) 
    
    is_active = Column(Boolean, default=True) 
    
    # Llave foránea conectada a roles.id. Nivel 5 (Visitante) por defecto (PoLP) 
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False, default=5) 
    
    # Trazabilidad básica 
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc)) 
    updated_at = Column( 
        DateTime, 
        default=lambda: datetime.now(timezone.utc), 
        onupdate=lambda: datetime.now(timezone.utc) 
    ) 

    # Relación bidireccional con el modelo Role 
    role = relationship("Role", back_populates="users") 
    
    # Relación con Sesiones
    sessions = relationship("UserSession", back_populates="user", cascade="all, delete-orphan")
