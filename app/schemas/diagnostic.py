from pydantic import BaseModel
from typing import Optional, Dict, List, Any
from datetime import datetime
import uuid

from app.schemas.exam_config import ExamType


# --- Nested models for diagnostic responses ---

class DiagnosticQuestion(BaseModel):
    """A single question (without correct answer) for the diagnostic test."""
    id: uuid.UUID
    question_text: str
    question_type: str
    options: Optional[Dict[str, str]] = None
    difficulty: str
    tags: Optional[List[str]] = None


class DiagnosticTopicQuestions(BaseModel):
    """A group of questions under one topic."""
    topic_id: uuid.UUID
    topic_name: str
    questions: List[DiagnosticQuestion]


# --- Request / Response schemas ---

class DiagnosticStartResponse(BaseModel):
    """Returned when a diagnostic test is started."""
    diagnostic_id: uuid.UUID
    exam_type: ExamType
    time_limit_minutes: int
    total_questions: int
    topics: List[DiagnosticTopicQuestions]


class DiagnosticSubmitRequest(BaseModel):
    """Submit all answers for a diagnostic test."""
    diagnostic_id: uuid.UUID
    answers: Dict[str, str]  # {question_id_str: user_answer}


class TopicScore(BaseModel):
    """Per-topic breakdown in the result."""
    topic_id: uuid.UUID
    topic_name: str
    correct: int
    total: int
    score_percent: float
    strength_level: str  # "strong", "moderate", "weak"


class DiagnosticResultResponse(BaseModel):
    """Full diagnostic result with per-topic analysis."""
    diagnostic_id: uuid.UUID
    exam_type: ExamType
    status: str
    overall_score: float
    total_correct: int
    total_questions: int
    time_limit_minutes: int
    started_at: datetime
    completed_at: Optional[datetime] = None
    topic_breakdown: List[TopicScore]

    class Config:
        from_attributes = True


class DiagnosticHistoryItem(BaseModel):
    """Summary of a single past diagnostic test — used in history list."""
    diagnostic_id: uuid.UUID
    exam_type: ExamType
    status: str
    overall_score: Optional[float] = None
    total_correct: Optional[int] = None
    total_questions: int
    time_limit_minutes: int
    started_at: datetime
    completed_at: Optional[datetime] = None
    topic_breakdown: Optional[List[TopicScore]] = None

    class Config:
        from_attributes = True


class DiagnosticHistoryResponse(BaseModel):
    """Paginated history of diagnostic tests for the current user."""
    total: int
    items: List[DiagnosticHistoryItem]
