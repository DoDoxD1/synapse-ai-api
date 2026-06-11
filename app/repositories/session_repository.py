from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.study_session import StudySession, StudyPlan
from app.repositories.base import BaseRepository
from typing import List, Optional
import uuid


class StudySessionRepository(BaseRepository[StudySession]):
    def __init__(self, db: AsyncSession):
        super().__init__(StudySession, db)
    
    async def get_user_sessions(self, user_id: uuid.UUID, limit: int = 50) -> List[StudySession]:
        """Get user's study sessions"""
        result = await self.db.execute(
            select(StudySession)
            .where(StudySession.user_id == user_id)
            .order_by(StudySession.start_time.desc())
            .limit(limit)
        )
        return result.scalars().all()


class StudyPlanRepository(BaseRepository[StudyPlan]):
    def __init__(self, db: AsyncSession):
        super().__init__(StudyPlan, db)
    
    async def get_active_plan(self, user_id: uuid.UUID) -> Optional[StudyPlan]:
        """Get user's active study plan"""
        result = await self.db.execute(
            select(StudyPlan)
            .where(
                StudyPlan.user_id == user_id,
                StudyPlan.is_active == True
            )
            .order_by(StudyPlan.generated_at.desc())
        )
        return result.scalar_one_or_none()
