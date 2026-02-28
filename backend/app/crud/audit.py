from sqlalchemy.orm import Session
from app.models.audit import AuditLog
from typing import List, Optional, Dict, Any

def create_audit_log(
    db: Session,
    user_id: int,
    action: str,
    entity_name: str,
    entity_id: int,
    old_values: Optional[Dict[str, Any]] = None,
    new_values: Optional[Dict[str, Any]] = None,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None
) -> AuditLog:
    db_audit = AuditLog(
        user_id=user_id,
        action=action,
        entity_name=entity_name,
        entity_id=entity_id,
        old_values=old_values,
        new_values=new_values,
        ip_address=ip_address,
        user_agent=user_agent
    )
    db.add(db_audit)
    db.commit()
    db.refresh(db_audit)
    return db_audit

def get_audit_logs(db: Session, skip: int = 0, limit: int = 100) -> List[AuditLog]:
    return db.query(AuditLog).order_by(AuditLog.created_at.desc()).offset(skip).limit(limit).all()
