from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime, date
import uuid


class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    exam_type: Optional[str] = None
    target_score: Optional[int] = None
    exam_date: Optional[date] = None


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    exam_type: Optional[str] = None
    target_score: Optional[int] = None
    exam_date: Optional[date] = None


class UserResponse(UserBase):
    id: uuid.UUID
    created_at: datetime
    last_active: datetime
    is_active: bool
    is_verified: bool
    
    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenRefresh(BaseModel):
    refresh_token: str
