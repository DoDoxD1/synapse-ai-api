from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.dependencies import get_current_active_user
from app.repositories.question_repository import QuestionRepository, QuestionAttemptRepository
from app.repositories.topic_repository import TopicRepository
from app.schemas.question import QuestionWithoutAnswer, AnswerSubmission, AnswerResponse, QuestionAttemptResponse
from app.models.user import User
from app.algorithms.adaptive_difficulty import AdaptiveDifficultyEngine
from app.ai.question_generator import QuestionGenerator
from typing import List
import random

router = APIRouter()


@router.get("/questions", response_model=List[QuestionWithoutAnswer])
async def get_practice_questions(
    topic_id: str = Query(...),
    count: int = Query(10, ge=1, le=50),
    difficulty: str = Query(None),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get practice questions for a topic"""
    import uuid
    
    question_repo = QuestionRepository(db)
    topic_repo = TopicRepository(db)
    
    # Get user's mastery for adaptive difficulty
    mastery = await topic_repo.get_user_mastery(current_user.id, uuid.UUID(topic_id))
    
    if not difficulty and mastery:
        # Calculate adaptive difficulty
        recent_accuracy = mastery.correct_answers / max(mastery.total_questions_attempted, 1)
        difficulty = AdaptiveDifficultyEngine.calculate_difficulty(
            mastery.mastery_score,
            recent_accuracy,
            mastery.total_questions_attempted
        )
    
    # Get questions
    questions = await question_repo.get_by_topic(uuid.UUID(topic_id), difficulty)
    
    if not questions:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No questions found for this topic"
        )
    
    # Randomly select questions
    selected = random.sample(questions, min(count, len(questions)))
    
    return [
        QuestionWithoutAnswer(
            id=q.id,
            topic_id=q.topic_id,
            question_text=q.question_text,
            question_type=q.question_type,
            options=q.options,
            difficulty=q.difficulty,
            tags=q.tags
        )
        for q in selected
    ]


@router.post("/submit-answer", response_model=AnswerResponse)
async def submit_answer(
    submission: AnswerSubmission,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Submit answer for a question"""
    question_repo = QuestionRepository(db)
    attempt_repo = QuestionAttemptRepository(db)
    
    # Get question
    question = await question_repo.get_by_id(submission.question_id)
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found"
        )
    
    # Check if answer is correct
    is_correct = submission.answer.strip().lower() == question.correct_answer.strip().lower()
    
    # Calculate XP
    xp_earned = 0
    if is_correct:
        difficulty_multiplier = {"easy": 10, "medium": 15, "hard": 25}
        xp_earned = difficulty_multiplier.get(question.difficulty, 10)
    
    # Create attempt record
    await attempt_repo.create(
        user_id=current_user.id,
        question_id=question.id,
        user_answer=submission.answer,
        is_correct=is_correct,
        time_taken_seconds=submission.time_taken_seconds
    )
    
    return AnswerResponse(
        is_correct=is_correct,
        correct_answer=question.correct_answer,
        explanation=question.explanation or "",
        xp_earned=xp_earned
    )


@router.get("/attempts", response_model=List[QuestionAttemptResponse])
async def get_user_attempts(
    limit: int = Query(50, ge=1, le=200),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get user's question attempts"""
    attempt_repo = QuestionAttemptRepository(db)
    attempts = await attempt_repo.get_user_attempts(current_user.id, limit)
    
    return attempts
