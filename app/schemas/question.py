from pydantic import BaseModel
from typing import Optional, Dict, List, Any
from datetime import datetime
import uuid


class QuestionBase(BaseModel):
    question_text: str
    question_type: str
    difficulty: str


class QuestionCreate(QuestionBase):
    topic_id: uuid.UUID
    exam_type: str
    options: Optional[Dict[str, str]] = None
    correct_answer: str
    explanation: Optional[str] = None
    tags: Optional[List[str]] = None


class QuestionResponse(QuestionBase):
    id: uuid.UUID
    topic_id: uuid.UUID
    exam_type: str
    options: Optional[Dict[str, str]] = None
    explanation: Optional[str] = None
    difficulty: str
    source: str
    tags: Optional[List[str]] = None
    times_attempted: int
    avg_accuracy: Optional[float] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class QuestionWithoutAnswer(BaseModel):
    """Question without correct answer for practice"""
    id: uuid.UUID
    topic_id: uuid.UUID
    question_text: str
    question_type: str
    options: Optional[Dict[str, str]] = None
    difficulty: str
    tags: Optional[List[str]] = None
    
    class Config:
        from_attributes = True


class QuestionAttemptCreate(BaseModel):
    question_id: uuid.UUID
    user_answer: str
    time_taken_seconds: Optional[int] = None
    hints_used: int = 0
    session_id: Optional[uuid.UUID] = None


class QuestionAttemptResponse(BaseModel):
    id: uuid.UUID
    question_id: uuid.UUID
    user_answer: str
    is_correct: bool
    time_taken_seconds: Optional[int] = None
    attempted_at: datetime
    explanation: Optional[str] = None
    
    class Config:
        from_attributes = True


class AnswerSubmission(BaseModel):
    question_id: uuid.UUID
    answer: str
    time_taken_seconds: Optional[int] = None


class AnswerResponse(BaseModel):
    is_correct: bool
    correct_answer: str
    explanation: str
    xp_earned: int
