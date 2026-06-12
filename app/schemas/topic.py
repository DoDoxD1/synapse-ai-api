from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
import uuid

from app.schemas.exam_config import ExamType


class TopicBase(BaseModel):
    exam_type: ExamType
    name: str
    parent_topic_id: Optional[uuid.UUID] = None
    difficulty_level: Optional[int] = None
    exam_weight: Optional[float] = None
    description: Optional[str] = None
    learning_resources: Optional[Dict[str, Any]] = None


class TopicCreate(TopicBase):
    pass


class TopicResponse(TopicBase):
    id: uuid.UUID
    created_at: datetime
    
    class Config:
        from_attributes = True


class UserTopicMasteryResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    topic_id: uuid.UUID
    mastery_score: float
    total_questions_attempted: int
    correct_answers: int
    time_spent_minutes: int
    last_practiced: Optional[datetime] = None
    next_review_date: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class TopicWithMastery(TopicResponse):
    mastery: Optional[UserTopicMasteryResponse] = None
