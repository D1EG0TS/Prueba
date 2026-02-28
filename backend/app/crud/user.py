"""
Lógica CRUD para el modelo User.
"""
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserUpdateMe
from app.core.security import get_password_hash

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_users(db: Session, current_user: User, skip: int = 0, limit: int = 100):
    query = db.query(User)
    if current_user.role_id == 2:
        query = query.filter(User.role_id != 1)
    return query.offset(skip).limit(limit).all()

def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        hashed_password=hashed_password,
        first_name=user.first_name,
        last_name=user.last_name,
        phone_number=user.phone_number,
        profile_picture=user.profile_picture,
        date_of_birth=user.date_of_birth,
        gender=user.gender,
        role_id=user.role_id,
        is_active=user.is_active
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.is_active = False
        db.commit()
        db.refresh(user)
    return user

def update_user(db: Session, db_user: User, update_data: UserUpdate):
    user_data = update_data.model_dump(exclude_unset=True)
    if "password" in user_data:
        password = user_data["password"]
        hashed_password = get_password_hash(password)
        user_data["hashed_password"] = hashed_password
        del user_data["password"]

    for key, value in user_data.items():
        setattr(db_user, key, value)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user_me(db: Session, db_user: User, user_in: UserUpdateMe):
    user_data = user_in.model_dump(exclude_unset=True)
    
    for field in user_data:
        if field in user_data:
            setattr(db_user, field, user_data[field])

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
