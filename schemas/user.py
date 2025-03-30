from pydantic import BaseModel, EmailStr, ConfigDict
from uuid import UUID
from typing import Optional
from datetime import datetime

# ✅ Shared base user
class UserBase(BaseModel):
    email: EmailStr
    name: Optional[str] = None

# ✅ When user registers or completes profile
class UserRegister(BaseModel):
    name: Optional[str] = None
    username: Optional[str] = None
    avatar_url: Optional[str] = None
    team: Optional[str] = None

# ❌ REMOVE this - not needed with Google login
# class UserCreate(UserBase):
#     password: str

# ❌ REMOVE this too - no login with password
# class UserLogin(BaseModel):
#     email: EmailStr
#     password: str

# ✅ Response sent to frontend
class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    username: Optional[str] = None
    avatar_url: Optional[str] = None
    team: Optional[str] = None
    created_at: datetime

    @staticmethod
    def serialize_datetime(dt: datetime) -> str:
        return dt.isoformat()
