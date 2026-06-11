from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.dependencies import get_current_active_user
from app.models.user import User
from app.models.mock_test import MockTest, MockTestAttempt
from app.schemas.mock_test import MockTestResponse, MockTestAttemptCreate, MockTestAttemptResponse, MockTestAttemptSubmit
from typing import List
from datetime import datetime

router = APIRouter()


@router.get("/", response_model=List[MockTestResponse])
async def get_mock_tests(
    exam_type: str = None,
    db: AsyncSession = Depends(get_db)
):
    """Get available mock tests"""
    query = select(MockTest)
    
    if exam_type:
        query = query.where(MockTest.exam_type == exam_type)
    
    result = await db.execute(query.order_by(MockTest.created_at.desc()))
    tests = result.scalars().all()
    
    return tests


@router.get("/{test_id}", response_model=MockTestResponse)
async def get_mock_test(
    test_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Get mock test by ID"""
    import uuid
    
    result = await db.execute(
        select(MockTest).where(MockTest.id == uuid.UUID(test_id))
    )
    test = result.scalar_one_or_none()
    
    if not test:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mock test not found"
        )
    
    return test


@router.post("/attempts", response_model=MockTestAttemptResponse, status_code=status.HTTP_201_CREATED)
async def start_mock_test(
    attempt_data: MockTestAttemptCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Start a mock test attempt"""
    # Check if test exists
    result = await db.execute(
        select(MockTest).where(MockTest.id == attempt_data.mock_test_id)
    )
    test = result.scalar_one_or_none()
    
    if not test:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mock test not found"
        )
    
    # Create attempt
    attempt = MockTestAttempt(
        user_id=current_user.id,
        mock_test_id=test.id,
        start_time=datetime.utcnow(),
        max_score=test.max_score,
        completed=False
    )
    db.add(attempt)
    await db.flush()
    await db.refresh(attempt)
    
    return attempt


@router.post("/attempts/submit", response_model=MockTestAttemptResponse)
async def submit_mock_test(
    submission: MockTestAttemptSubmit,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Submit mock test answers"""
    result = await db.execute(
        select(MockTestAttempt).where(
            MockTestAttempt.id == submission.attempt_id,
            MockTestAttempt.user_id == current_user.id
        )
    )
    attempt = result.scalar_one_or_none()
    
    if not attempt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attempt not found"
        )
    
    if attempt.completed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Test already submitted"
        )
    
    # Calculate score (simplified)
    # TODO: Implement proper scoring logic
    score = len(submission.answers) * 10
    
    # Update attempt
    attempt.end_time = datetime.utcnow()
    attempt.answers = submission.answers
    attempt.score = score
    attempt.completed = True
    attempt.time_taken_minutes = int((attempt.end_time - attempt.start_time).total_seconds() / 60)
    
    await db.flush()
    await db.refresh(attempt)
    
    return attempt


@router.get("/attempts/my", response_model=List[MockTestAttemptResponse])
async def get_my_attempts(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get user's mock test attempts"""
    result = await db.execute(
        select(MockTestAttempt)
        .where(MockTestAttempt.user_id == current_user.id)
        .order_by(MockTestAttempt.start_time.desc())
    )
    attempts = result.scalars().all()
    
    return attempts
