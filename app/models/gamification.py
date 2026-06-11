from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from app.core.database import Base


class UserStats(Base):
    __tablename__ = "user_stats"
    
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)
    total_xp = Column(Integer, default=0)
    level = Column(Integer, default=1)
    current_streak = Column(Integer, default=0)
    longest_streak = Column(Integer, default=0)
    last_activity_date = Column(DateTime)
    total_study_hours = Column(Integer, default=0)
    total_questions_attempted = Column(Integer, default=0)
    total_correct_answers = Column(Integer, default=0)
    mock_tests_taken = Column(Integer, default=0)
    topics_mastered = Column(Integer, default=0)
    rank = Column(Integer)
    percentile = Column(Float)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="stats")
    
    def __repr__(self):
        return f"<UserStats user={self.user_id} level={self.level} xp={self.total_xp}>"


class UserAchievement(Base):
    __tablename__ = "user_achievements"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    achievement_type = Column(String(50), nullable=False)  # badge, milestone, streak
    achievement_name = Column(String(100), nullable=False)
    achievement_description = Column(String(255))
    xp_reward = Column(Integer, default=0)
    earned_at = Column(DateTime, default=datetime.utcnow)
    achievement_metadata = Column(JSONB)
    
    # Relationships
    user = relationship("User", back_populates="achievements")
    
    def __repr__(self):
        return f"<UserAchievement {self.achievement_name}>"
