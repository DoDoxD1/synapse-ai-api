from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.core.database import get_db
from app.dependencies import get_current_active_user
from app.schemas.analytics import UserStatsResponse, ProgressAnalytics, LeaderboardResponse, LeaderboardEntry
from app.models.user import User
from app.models.gamification import UserStats
from typing import List

router = APIRouter()


@router.get("/stats", response_model=UserStatsResponse)
async def get_user_stats(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get user statistics"""
    result = await db.execute(
        select(UserStats).where(UserStats.user_id == current_user.id)
    )
    stats = result.scalar_one_or_none()
    
    if not stats:
        # Create default stats if not exists
        stats = UserStats(user_id=current_user.id)
        db.add(stats)
        await db.flush()
    
    accuracy_rate = 0.0
    if stats.total_questions_attempted > 0:
        accuracy_rate = (stats.total_correct_answers / stats.total_questions_attempted) * 100
    
    return UserStatsResponse(
        total_xp=stats.total_xp,
        level=stats.level,
        current_streak=stats.current_streak,
        longest_streak=stats.longest_streak,
        total_study_hours=stats.total_study_hours,
        total_questions_attempted=stats.total_questions_attempted,
        total_correct_answers=stats.total_correct_answers,
        mock_tests_taken=stats.mock_tests_taken,
        topics_mastered=stats.topics_mastered,
        accuracy_rate=accuracy_rate,
        rank=stats.rank,
        percentile=stats.percentile
    )


@router.get("/progress", response_model=ProgressAnalytics)
async def get_progress_analytics(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get detailed progress analytics"""
    # TODO: Implement detailed analytics queries
    
    return ProgressAnalytics(
        daily_activity=[],
        topic_performance=[],
        accuracy_trend=[],
        study_time_distribution={}
    )


@router.get("/leaderboard", response_model=LeaderboardResponse)
async def get_leaderboard(
    limit: int = 50,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get leaderboard"""
    # Get top users
    result = await db.execute(
        select(UserStats, User)
        .join(User, UserStats.user_id == User.id)
        .where(User.is_active == True)
        .order_by(UserStats.total_xp.desc())
        .limit(limit)
    )
    
    leaderboard_data = []
    current_user_rank = None
    
    for rank, (stats, user) in enumerate(result.all(), start=1):
        entry = LeaderboardEntry(
            rank=rank,
            user_name=user.full_name or user.email.split('@')[0],
            total_xp=stats.total_xp,
            level=stats.level,
            is_current_user=(user.id == current_user.id)
        )
        leaderboard_data.append(entry)
        
        if user.id == current_user.id:
            current_user_rank = rank
    
    # Get total users count
    total_result = await db.execute(
        select(func.count(User.id)).where(User.is_active == True)
    )
    total_users = total_result.scalar()
    
    return LeaderboardResponse(
        leaderboard=leaderboard_data,
        current_user_rank=current_user_rank or 0,
        total_users=total_users
    )
