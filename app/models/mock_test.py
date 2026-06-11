from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from app.core.database import Base


class MockTest(Base):
    __tablename__ = "mock_tests"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    exam_type = Column(String(50), nullable=False, index=True)
    test_name = Column(String(100))
    duration_minutes = Column(Integer, nullable=False)
    total_questions = Column(Integer, nullable=False)
    topic_distribution = Column(JSONB)  # {topic_id: question_count}
    passing_score = Column(Integer)
    max_score = Column(Integer)
    is_official = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    attempts = relationship("MockTestAttempt", back_populates="mock_test")
    
    def __repr__(self):
        return f"<MockTest {self.test_name}>"


class MockTestAttempt(Base):
    __tablename__ = "mock_test_attempts"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    mock_test_id = Column(UUID(as_uuid=True), ForeignKey("mock_tests.id"), nullable=False)
    start_time = Column(DateTime, nullable=False, default=datetime.utcnow)
    end_time = Column(DateTime)
    score = Column(Integer)
    max_score = Column(Integer)
    percentile = Column(Float)
    time_taken_minutes = Column(Integer)
    answers = Column(JSONB)  # {question_id: user_answer}
    detailed_analysis = Column(JSONB)  # topic-wise breakdown
    completed = Column(Boolean, default=False)
    
    # Relationships
    user = relationship("User", back_populates="mock_test_attempts")
    mock_test = relationship("MockTest", back_populates="attempts")
    
    def __repr__(self):
        return f"<MockTestAttempt user={self.user_id} completed={self.completed}>"
