from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, Any
from datetime import datetime

class AuditLogResponse(BaseModel):
    id: int
    user_id: int
    action: str
    entity_name: str
    entity_id: int
    old_values: Optional[Dict[str, Any]] = None
    new_values: Optional[Dict[str, Any]] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
