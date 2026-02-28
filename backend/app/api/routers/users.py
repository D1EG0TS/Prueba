"""
Router para la gestión de usuarios (Admin).
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_active_user, allow_admin
from app.crud.user import (
    get_user,
    get_user_by_email,
    get_users,
    create_user,
    update_user,
    delete_user as crud_delete_user,
    update_user_me,
)
from app.schemas.user import UserCreate, UserResponse, UserUpdate, UserUpdateMe
from app.models.user import User
from app.crud.audit import create_audit_log

router = APIRouter()

@router.get("/", response_model=List[UserResponse], dependencies=[Depends(allow_admin)])
def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Obtiene la lista de usuarios.
    """
    users = get_users(db, current_user=current_user, skip=skip, limit=limit)
    return users

@router.get("/{user_id}", response_model=UserResponse, dependencies=[Depends(allow_admin)])
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

@router.post("/", response_model=UserResponse, dependencies=[Depends(allow_admin)])
def create_new_user(
    request: Request,
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
        
    new_user = create_user(db=db, user=user)
    
    create_audit_log(
        db,
        user_id=current_user.id,
        action="CREATE",
        entity_name="User",
        entity_id=new_user.id,
        new_values={"email": new_user.email, "role": new_user.role_id},
        ip_address=request.client.host,
        user_agent=request.headers.get("user-agent")
    )
    
    return new_user

@router.get("/me", response_model=UserResponse)
def read_user_me(
    current_user: User = Depends(get_current_active_user),
):
    """
    Obtiene el perfil del usuario autenticado.
    """
    return current_user

@router.put("/me", response_model=UserResponse)
def update_user_profile(
    request: Request,
    user_in: UserUpdateMe,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Actualiza el perfil del usuario autenticado.
    """
    # Capture old values
    old_values = {
        "first_name": current_user.first_name,
        "last_name": current_user.last_name,
        "phone_number": current_user.phone_number,
        "profile_picture": current_user.profile_picture,
        "date_of_birth": current_user.date_of_birth,
        "gender": current_user.gender,
    }

    updated_user = update_user_me(db=db, db_user=current_user, user_in=user_in)

    create_audit_log(
        db,
        user_id=current_user.id,
        action="UPDATE",
        entity_name="User",
        entity_id=current_user.id,
        old_values=old_values,
        new_values=user_in.model_dump(exclude_unset=True),
        ip_address=request.client.host,
        user_agent=request.headers.get("user-agent")
    )

    return updated_user

@router.put("/{user_id}", response_model=UserResponse, dependencies=[Depends(allow_admin)])
def update_existing_user(
    request: Request,
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

    # Capture old values
    old_values = {
        "email": db_user.email,
        "first_name": db_user.first_name,
        "last_name": db_user.last_name,
        "phone_number": db_user.phone_number,
        "role_id": db_user.role_id,
        "is_active": db_user.is_active
    }

    updated_user = update_user(db=db, db_user=db_user, update_data=user_update)

    create_audit_log(
        db,
        user_id=current_user.id,
        action="UPDATE",
        entity_name="User",
        entity_id=updated_user.id,
        old_values=old_values,
        new_values=user_update.model_dump(exclude_unset=True),
        ip_address=request.client.host,
        user_agent=request.headers.get("user-agent")
    )
    
    return updated_user

@router.delete("/{user_id}", dependencies=[Depends(allow_admin)])
def delete_user(
    request: Request,
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

    crud_delete_user(db, user_id=user_id)

    create_audit_log(
        db,
        user_id=current_user.id,
        action="DELETE",
        entity_name="User",
        entity_id=user_id,
        ip_address=request.client.host,
        user_agent=request.headers.get("user-agent")
    )

    return {"message": "Usuario eliminado exitosamente"}
