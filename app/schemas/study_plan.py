from pydantic import BaseModel
from typing import Dict, Any, Optional
from datetime import datetime
import uuid

from app.schemas.exam_config import ExamType


class StudyPlanCreate(BaseModel):
    start_date: datetime
    end_date: datetime
    daily_hours: float
    target_topics: Optional[list[uuid.UUID]] = None


class StudyPlanResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    plan_name: Optional[str] = None
    start_date: datetime
    end_date: datetime
    daily_hours: float
    is_active: bool
    generated_at: datetime
    plan_data: Optional[Dict[str, Any]] = None
    
    class Config:
        from_attributes = True


class StudySessionCreate(BaseModel):
    topic_id: Optional[uuid.UUID] = None
    session_type: str


class StudySessionEnd(BaseModel):
    session_id: uuid.UUID


class StudySessionResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    topic_id: Optional[uuid.UUID] = None
    session_type: str
    start_time: datetime
    end_time: Optional[datetime] = None
    duration_minutes: Optional[int] = None
    questions_attempted: int
    correct_answers: int
    xp_earned: int
    
    class Config:
        from_attributes = True


class AssessmentRequest(BaseModel):
    exam_type: ExamType
    topics: Optional[list[str]] = None


class AssessmentResult(BaseModel):
    weak_topics: list[Dict[str, Any]]
    strong_topics: list[Dict[str, Any]]
    recommended_study_plan: Dict[str, Any]
