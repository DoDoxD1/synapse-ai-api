from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.question import Question, QuestionAttempt
from app.repositories.base import BaseRepository
from typing import List
import uuid


class QuestionRepository(BaseRepository[Question]):
    def __init__(self, db: AsyncSession):
        super().__init__(Question, db)
    
    async def get_by_topic(self, topic_id: uuid.UUID, difficulty: str = None) -> List[Question]:
        """Get questions by topic and optional difficulty"""
        query = select(Question).where(Question.topic_id == topic_id)
        
        if difficulty:
            query = query.where(Question.difficulty == difficulty)
        
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def get_by_exam_type(self, exam_type: str, difficulty: str = None) -> List[Question]:
        """Get questions by exam type and optional difficulty"""
        query = select(Question).where(Question.exam_type == exam_type)
        
        if difficulty:
            query = query.where(Question.difficulty == difficulty)
        
        result = await self.db.execute(query)
        return result.scalars().all()


class QuestionAttemptRepository(BaseRepository[QuestionAttempt]):
    def __init__(self, db: AsyncSession):
        super().__init__(QuestionAttempt, db)
    
    async def get_user_attempts(self, user_id: uuid.UUID, limit: int = 100) -> List[QuestionAttempt]:
        """Get user's question attempts"""
        result = await self.db.execute(
            select(QuestionAttempt)
            .where(QuestionAttempt.user_id == user_id)
            .order_by(QuestionAttempt.attempted_at.desc())
            .limit(limit)
        )
        return result.scalars().all()
