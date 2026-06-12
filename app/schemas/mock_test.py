from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime
import uuid

from app.schemas.exam_config import ExamType


class MockTestCreate(BaseModel):
    exam_type: ExamType
    test_name: str
    duration_minutes: int
    total_questions: int
    topic_distribution: Optional[Dict[str, int]] = None


class MockTestResponse(BaseModel):
    id: uuid.UUID
    exam_type: ExamType
    test_name: str
    duration_minutes: int
    total_questions: int
    topic_distribution: Optional[Dict[str, Any]] = None
    passing_score: Optional[int] = None
    max_score: Optional[int] = None
    is_official: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class MockTestAttemptCreate(BaseModel):
    mock_test_id: uuid.UUID


class MockTestAttemptSubmit(BaseModel):
    attempt_id: uuid.UUID
    answers: Dict[str, str]


class MockTestAttemptResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    mock_test_id: uuid.UUID
    start_time: datetime
    end_time: Optional[datetime] = None
    score: Optional[int] = None
    max_score: Optional[int] = None
    percentile: Optional[float] = None
    time_taken_minutes: Optional[int] = None
    completed: bool
    detailed_analysis: Optional[Dict[str, Any]] = None
    
    class Config:
        from_attributes = True
