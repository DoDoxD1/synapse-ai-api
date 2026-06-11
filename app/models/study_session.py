from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from app.core.database import Base


class StudySession(Base):
    __tablename__ = "study_sessions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    topic_id = Column(UUID(as_uuid=True), ForeignKey("topics.id"))
    session_type = Column(String(50), nullable=False)  # practice, review, mock_test, tutoring
    start_time = Column(DateTime, nullable=False, default=datetime.utcnow)
    end_time = Column(DateTime)
    duration_minutes = Column(Integer)
    questions_attempted = Column(Integer, default=0)
    correct_answers = Column(Integer, default=0)
    xp_earned = Column(Integer, default=0)
    
    # Relationships
    user = relationship("User", back_populates="study_sessions")
    topic = relationship("Topic")
    question_attempts = relationship("QuestionAttempt", back_populates="session")
    
    def __repr__(self):
        return f"<StudySession user={self.user_id} type={self.session_type}>"


class StudyPlan(Base):
    __tablename__ = "study_plans"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    plan_name = Column(String(100))
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    daily_hours = Column(Float, nullable=False)
    is_active = Column(Boolean, default=True)
    generated_at = Column(DateTime, default=datetime.utcnow)
    plan_data = Column(JSONB)  # weekly breakdown: {week_1: [...], week_2: [...]}
    
    # Relationships
    user = relationship("User", back_populates="study_plans")
    
    def __repr__(self):
        return f"<StudyPlan user={self.user_id} active={self.is_active}>"
