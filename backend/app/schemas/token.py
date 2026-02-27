from pydantic import BaseModel
from datetime import datetime

class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str

class TokenPayload(BaseModel):
    sub: str | None = None

class SessionResponse(BaseModel):
    id: int
    user_id: int
    refresh_token: str
    device_info: str | None
    ip_address: str | None
    expires_at: datetime
    is_revoked: bool
    created_at: datetime

    class Config:
        from_attributes = True
