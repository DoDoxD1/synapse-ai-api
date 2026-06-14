from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from app.core.database import Base


class DiagnosticTest(Base):
    __tablename__ = "diagnostic_tests"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    exam_type = Column(String(50), nullable=False, index=True)
    status = Column(String(20), nullable=False, default="in_progress")  # in_progress | completed
    started_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    time_limit_minutes = Column(Integer, nullable=False)
    total_questions = Column(Integer, nullable=False, default=0)
    correct_answers = Column(Integer, nullable=True)
    overall_score = Column(Float, nullable=True)  # percentage 0-100
    topic_scores = Column(JSONB, nullable=True)
    # Format: {topic_id: {topic_name, correct, total, score, strength_level}}
    question_ids = Column(JSONB, nullable=True)
    # List of question IDs served in this diagnostic (to score on submit)

    # Relationships
    user = relationship("User", back_populates="diagnostic_tests")

    def __repr__(self):
        return f"<DiagnosticTest user={self.user_id} exam={self.exam_type} status={self.status}>"
