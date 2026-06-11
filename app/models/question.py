from sqlalchemy import Column, String, Integer, Float, Text, Boolean, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSONB, ARRAY
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from app.core.database import Base


class Question(Base):
    __tablename__ = "questions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    topic_id = Column(UUID(as_uuid=True), ForeignKey("topics.id"), nullable=False)
    exam_type = Column(String(50), nullable=False, index=True)
    question_text = Column(Text, nullable=False)
    question_type = Column(String(50), nullable=False)  # mcq, numeric, descriptive
    options = Column(JSONB)  # for MCQs: {"A": "...", "B": "...", ...}
    correct_answer = Column(Text, nullable=False)
    explanation = Column(Text)
    difficulty = Column(String(20), nullable=False, index=True)  # easy, medium, hard
    source = Column(String(50), default="curated")  # curated, ai_generated, community
    tags = Column(ARRAY(String))
    times_attempted = Column(Integer, default=0)
    avg_accuracy = Column(Float)
    avg_time_seconds = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    topic = relationship("Topic", back_populates="questions")
    attempts = relationship("QuestionAttempt", back_populates="question")
    
    def __repr__(self):
        return f"<Question {self.id} difficulty={self.difficulty}>"


class QuestionAttempt(Base):
    __tablename__ = "question_attempts"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    question_id = Column(UUID(as_uuid=True), ForeignKey("questions.id"), nullable=False)
    session_id = Column(UUID(as_uuid=True), ForeignKey("study_sessions.id"))
    user_answer = Column(Text)
    is_correct = Column(Boolean, nullable=False)
    time_taken_seconds = Column(Integer)
    hints_used = Column(Integer, default=0)
    attempted_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="question_attempts")
    question = relationship("Question", back_populates="attempts")
    session = relationship("StudySession", back_populates="question_attempts")
    
    def __repr__(self):
        return f"<QuestionAttempt correct={self.is_correct}>"
