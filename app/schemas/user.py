from pydantic import BaseModel, EmailStr, Field, model_validator
from typing import Optional
from datetime import datetime, date
import uuid

from app.schemas.exam_config import ExamType, EXAM_MAX_SCORES


class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    exam_type: ExamType
    target_score: Optional[int] = Field(None, ge=0)
    exam_date: Optional[date] = None

    @model_validator(mode="after")
    def validate_and_default_target_score(self):
        max_score = EXAM_MAX_SCORES[self.exam_type]
        if self.target_score is None:
            self.target_score = max_score
        elif self.target_score > max_score:
            raise ValueError(
                f"target_score for {self.exam_type.value} cannot exceed {max_score}"
            )
        return self


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    exam_type: Optional[ExamType] = None
    target_score: Optional[int] = Field(None, ge=0)
    exam_date: Optional[date] = None

    @model_validator(mode="after")
    def validate_target_score(self):
        if self.target_score is not None and self.exam_type is not None:
            max_score = EXAM_MAX_SCORES[self.exam_type]
            if self.target_score > max_score:
                raise ValueError(
                    f"target_score for {self.exam_type.value} cannot exceed {max_score}"
                )
        return self


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
