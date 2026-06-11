from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.topic import Topic, UserTopicMastery
from app.repositories.base import BaseRepository
from typing import List, Optional
import uuid


class TopicRepository(BaseRepository[Topic]):
    def __init__(self, db: AsyncSession):
        super().__init__(Topic, db)
    
    async def get_by_exam_type(self, exam_type: str) -> List[Topic]:
        """Get all topics for exam type"""
        result = await self.db.execute(
            select(Topic).where(Topic.exam_type == exam_type)
        )
        return result.scalars().all()
    
    async def get_user_mastery(self, user_id: uuid.UUID, topic_id: uuid.UUID) -> Optional[UserTopicMastery]:
        """Get user's mastery for specific topic"""
        result = await self.db.execute(
            select(UserTopicMastery).where(
                UserTopicMastery.user_id == user_id,
                UserTopicMastery.topic_id == topic_id
            )
        )
        return result.scalar_one_or_none()
    
    async def get_all_user_mastery(self, user_id: uuid.UUID) -> List[UserTopicMastery]:
        """Get all mastery records for a user"""
        result = await self.db.execute(
            select(UserTopicMastery).where(UserTopicMastery.user_id == user_id)
        )
        return result.scalars().all()
