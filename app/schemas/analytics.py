from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime


class UserStatsResponse(BaseModel):
    total_xp: int
    level: int
    current_streak: int
    longest_streak: int
    total_study_hours: int
    total_questions_attempted: int
    total_correct_answers: int
    mock_tests_taken: int
    topics_mastered: int
    accuracy_rate: float
    rank: Optional[int] = None
    percentile: Optional[float] = None
    
    class Config:
        from_attributes = True


class ProgressAnalytics(BaseModel):
    daily_activity: List[Dict[str, Any]]
    topic_performance: List[Dict[str, Any]]
    accuracy_trend: List[Dict[str, Any]]
    study_time_distribution: Dict[str, int]


class LeaderboardEntry(BaseModel):
    rank: int
    user_name: str
    total_xp: int
    level: int
    is_current_user: bool = False


class LeaderboardResponse(BaseModel):
    leaderboard: List[LeaderboardEntry]
    current_user_rank: int
    total_users: int


class AchievementResponse(BaseModel):
    achievement_type: str
    achievement_name: str
    achievement_description: Optional[str] = None
    xp_reward: int
    earned_at: datetime
    
    class Config:
        from_attributes = True
