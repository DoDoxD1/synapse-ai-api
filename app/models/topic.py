from sqlalchemy import Column, String, Integer, Float, Text, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from app.core.database import Base


class Topic(Base):
    __tablename__ = "topics"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    exam_type = Column(String(50), nullable=False, index=True)
    name = Column(String(100), nullable=False)
    parent_topic_id = Column(UUID(as_uuid=True), ForeignKey("topics.id"), nullable=True)
    difficulty_level = Column(Integer)  # 1-5
    exam_weight = Column(Float)  # percentage weight in exam
    description = Column(Text)
    learning_resources = Column(JSONB)  # links to videos, articles
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    parent = relationship("Topic", remote_side=[id], backref="subtopics")
    questions = relationship("Question", back_populates="topic")
    user_mastery = relationship("UserTopicMastery", back_populates="topic")
    
    def __repr__(self):
        return f"<Topic {self.name}>"


class UserTopicMastery(Base):
    __tablename__ = "user_topic_mastery"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    topic_id = Column(UUID(as_uuid=True), ForeignKey("topics.id"), nullable=False)
    mastery_score = Column(Float, default=0.0)  # 0-100
    total_questions_attempted = Column(Integer, default=0)
    correct_answers = Column(Integer, default=0)
    time_spent_minutes = Column(Integer, default=0)
    last_practiced = Column(DateTime)
    
    # Spaced Repetition fields
    next_review_date = Column(DateTime)
    repetition_count = Column(Integer, default=0)
    easiness_factor = Column(Float, default=2.5)  # SM-2 algorithm
    interval_days = Column(Integer, default=0)
    
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="topic_mastery")
    topic = relationship("Topic", back_populates="user_mastery")
    
    def __repr__(self):
        return f"<UserTopicMastery user={self.user_id} topic={self.topic_id} score={self.mastery_score}>"
