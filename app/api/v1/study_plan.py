from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.dependencies import get_current_active_user
from app.repositories.session_repository import StudyPlanRepository, StudySessionRepository
from app.repositories.topic_repository import TopicRepository
from app.schemas.study_plan import (
    StudyPlanCreate, StudyPlanResponse, StudySessionCreate, 
    StudySessionResponse, StudySessionEnd
)
from app.models.user import User
from datetime import datetime
from typing import List

router = APIRouter()


@router.post("/", response_model=StudyPlanResponse, status_code=status.HTTP_201_CREATED)
async def create_study_plan(
    plan_data: StudyPlanCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new study plan"""
    plan_repo = StudyPlanRepository(db)
    
    # Deactivate any existing active plans
    existing_plan = await plan_repo.get_active_plan(current_user.id)
    if existing_plan:
        await plan_repo.update(existing_plan.id, is_active=False)
    
    # Create new plan
    total_days = (plan_data.end_date - plan_data.start_date).days
    
    plan = await plan_repo.create(
        user_id=current_user.id,
        plan_name=f"Study Plan ({plan_data.start_date.date()})",
        start_date=plan_data.start_date,
        end_date=plan_data.end_date,
        daily_hours=plan_data.daily_hours,
        is_active=True,
        plan_data={
            "total_days": total_days,
            "total_hours": total_days * plan_data.daily_hours,
            "target_topics": [str(t) for t in (plan_data.target_topics or [])]
        }
    )
    
    return plan


@router.get("/active", response_model=StudyPlanResponse)
async def get_active_plan(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get active study plan"""
    plan_repo = StudyPlanRepository(db)
    plan = await plan_repo.get_active_plan(current_user.id)
    
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active study plan found"
        )
    
    return plan


@router.post("/sessions", response_model=StudySessionResponse, status_code=status.HTTP_201_CREATED)
async def start_study_session(
    session_data: StudySessionCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Start a new study session"""
    session_repo = StudySessionRepository(db)
    
    session = await session_repo.create(
        user_id=current_user.id,
        topic_id=session_data.topic_id,
        session_type=session_data.session_type,
        start_time=datetime.utcnow()
    )
    
    return session


@router.post("/sessions/end", response_model=StudySessionResponse)
async def end_study_session(
    end_data: StudySessionEnd,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """End a study session"""
    session_repo = StudySessionRepository(db)
    
    session = await session_repo.get_by_id(end_data.session_id)
    if not session or session.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    
    end_time = datetime.utcnow()
    duration = int((end_time - session.start_time).total_seconds() / 60)
    
    updated_session = await session_repo.update(
        session.id,
        end_time=end_time,
        duration_minutes=duration
    )
    
    return updated_session


@router.get("/sessions", response_model=List[StudySessionResponse])
async def get_study_sessions(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get user's study sessions"""
    session_repo = StudySessionRepository(db)
    sessions = await session_repo.get_user_sessions(current_user.id)
    
    return sessions
