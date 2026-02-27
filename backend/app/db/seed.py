from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.role import Role
from app.models.user import User
from app.core.security import get_password_hash

def init_db(db: Session) -> None:
    # 1. Crear Roles Base
    roles_data = [
        {"id": 1, "name": "Super Administrador", "level": 1, "description": "Acceso total al sistema"},
        {"id": 2, "name": "Administrador", "level": 2, "description": "Gestión administrativa"},
        {"id": 3, "name": "Moderador", "level": 3, "description": "Supervisión de contenido"},
        {"id": 4, "name": "Operativo", "level": 4, "description": "Operaciones diarias"},
        {"id": 5, "name": "Visitante", "level": 5, "description": "Solo lectura"},
    ]

    for role_data in roles_data:
        role = db.query(Role).filter(Role.id == role_data["id"]).first()
        if not role:
            role = Role(**role_data)
            db.add(role)
            print(f"Rol creado: {role.name}")
        else:
            print(f"Rol ya existe: {role.name}")
    
    db.commit()

    # 2. Crear Super Admin
    admin_email = "admin@empresa.com"
    user = db.query(User).filter(User.email == admin_email).first()
    if not user:
        user = User(
            email=admin_email,
            hashed_password=get_password_hash("AdminSystem_2024!"),
            first_name="Super",
            last_name="Admin",
            role_id=1,  # Super Administrador
            is_active=True,
            profile_picture=None,
            phone_number=None
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        print(f"Super Admin creado: {user.email}")
    else:
        print(f"Super Admin ya existe: {user.email}")

if __name__ == "__main__":
    db = SessionLocal()
    try:
        init_db(db)
    finally:
        db.close()
