from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db, allow_super_admin
from app.crud.audit import get_audit_logs
from app.schemas.audit import AuditLogResponse

router = APIRouter(
    prefix="/audit",
    tags=["Audit"],
)

@router.get("/", response_model=List[AuditLogResponse], dependencies=[Depends(allow_super_admin)])
def read_audit_logs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Obtener logs de auditoría (Solo Super Admin)
    """
    return get_audit_logs(db, skip=skip, limit=limit)
