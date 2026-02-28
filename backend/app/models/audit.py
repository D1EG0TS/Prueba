from sqlalchemy import Column, Integer, String, JSON, DateTime, ForeignKey
from app.core.database import Base
from datetime import datetime, timezone

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    action = Column(String(50), nullable=False)  # CREATE, UPDATE, DELETE
    entity_name = Column(String(100), nullable=False)
    entity_id = Column(Integer, nullable=False)
    old_values = Column(JSON, nullable=True)
    new_values = Column(JSON, nullable=True)
    ip_address = Column(String(50), nullable=True)
    user_agent = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
