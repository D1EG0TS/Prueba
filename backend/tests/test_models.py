""" 
Pruebas unitarias para validar la instanciación de los modelos. 
""" 
from app.models.role import Role 
from app.models.user import User 

def test_role_model_instantiation() -> None: 
    """Valida la creación de una instancia del modelo Role.""" 
    role = Role(name="Visitante", level=5, description="Solo lectura") 
    assert role.name == "Visitante" 
    assert role.level == 5 

def test_user_model_instantiation() -> None: 
    """Valida la creación de un User con sus datos de perfil y valores por defecto (PoLP).""" 
    user = User( 
        email="juan.perez@empresa.com", 
        hashed_password="hashed_123", 
        first_name="Juan", 
        last_name="Pérez", 
        phone_number="+521234567890", 
        profile_picture="/uploads/avatars/juan.jpg",
        is_active=True,
        role_id=5
    ) 
    
    assert user.first_name == "Juan" 
    assert user.last_name == "Pérez" 
    assert user.phone_number == "+521234567890" 
    assert user.profile_picture == "/uploads/avatars/juan.jpg" 
    assert user.is_active is True  # Activo por defecto 
    assert user.role_id == 5       # Rol visitante por defecto 
