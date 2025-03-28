from pydantic import BaseModel, EmailStr
from uuid import UUID
from typing import Optional
from datetime import datetime

class UserRegister(BaseModel):
    name: str
    username: str
    avatar_url: str
    team: str


# ✅ User Login Schema
class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: UUID
    name: str
    username: str
    email: EmailStr
    avatar_url: str
    team: str
    created_at: str  # ✅ Change this to string

    class Config:
        orm_mode = True  # ✅ Enables ORM support
        from_attributes = True  # ✅ Ensure correct serialization

        @staticmethod
        def serialize_datetime(dt: datetime) -> str:
            return dt.isoformat()  # ✅ Converts to string (ISO 8601)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

