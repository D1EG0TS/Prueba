"""
Router para la gestión de usuarios (Admin).
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_active_user, allow_admin
from app.crud.user import (
    get_user,
    get_user_by_email,
    get_users,
    create_user,
    update_user,
)
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.models.user import User

router = APIRouter(
    dependencies=[Depends(allow_admin)]
)

@router.get("/", response_model=List[UserResponse])
def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Obtiene la lista de usuarios.
    """
    users = get_users(db, skip=skip, limit=limit)
    return users

@router.get("/{user_id}", response_model=UserResponse)
def read_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Obtiene un usuario por ID.
    """
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
        )
    return db_user

@router.post("/", response_model=UserResponse)
def create_new_user(
    user: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Crea un nuevo usuario.
    """
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="El email ya está registrado"
        )
    
    # REGLA DE NEGOCIO: Un Admin (2) no puede crear un Super Admin (1)
    if current_user.role_id == 2 and user.role_id == 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Un Admin no puede crear un Super Admin"
        )
        
    return create_user(db=db, user=user)

@router.put("/{user_id}", response_model=UserResponse)
def update_existing_user(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Actualiza un usuario existente.
    """
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
        )
    
    # REGLA DE NEGOCIO: Si current_user.role_id == 2 y el usuario a editar tiene role_id == 1
    # o se intenta enviar un role_id == 1, lanza 403.
    if current_user.role_id == 2:
        if db_user.role_id == 1:
             raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para modificar a un Super Admin"
            )
        if user_update.role_id == 1:
             raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para asignar el rol de Super Admin"
            )

    return update_user(db=db, db_user=db_user, update_data=user_update)

@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Realiza un borrado lógico (Soft Delete) de un usuario.
    """
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
        )
    
    # REGLA DE NEGOCIO: Rol 2 no borra Rol 1
    if current_user.role_id == 2 and db_user.role_id == 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para eliminar a un Super Admin"
        )

    db_user.is_active = False
    db.commit()
    return {"message": "Usuario eliminado exitosamente"}
