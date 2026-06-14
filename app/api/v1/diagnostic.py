from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from datetime import datetime
from typing import List
import uuid
import random

from app.core.database import get_db
from app.dependencies import get_current_active_user
from app.services.token_service import get_token_payload
from app.schemas.user import TokenPayload
from app.models.user import User
from app.models.topic import Topic, UserTopicMastery
from app.models.question import Question
from app.models.diagnostic import DiagnosticTest
from app.schemas.diagnostic import (
    DiagnosticStartResponse,
    DiagnosticSubmitRequest,
    DiagnosticResultResponse,
    DiagnosticTopicQuestions,
    DiagnosticQuestion,
    TopicScore,
    DiagnosticHistoryItem,
    DiagnosticHistoryResponse,
)

router = APIRouter()

QUESTIONS_PER_TOPIC = 4  # 3-5, we use 4 as default
TIME_PER_QUESTION_MINUTES = 2


@router.post("/start", response_model=DiagnosticStartResponse, status_code=status.HTTP_201_CREATED)
async def start_diagnostic(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Start a diagnostic test for the current user's exam type.

    - Picks 3-5 questions per topic (mixed difficulty)
    - Creates a timed diagnostic session
    - Returns questions grouped by topic
    """
    if not current_user.exam_type:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Set your exam_type in profile before starting a diagnostic.",
        )

    exam_type = current_user.exam_type

    # Check for existing in-progress diagnostic
    result = await db.execute(
        select(DiagnosticTest).where(
            DiagnosticTest.user_id == current_user.id,
            DiagnosticTest.status == "in_progress",
        )
    )
    existing = result.scalar_one_or_none()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="You already have a diagnostic test in progress. Submit or complete it first.",
        )

    # Fetch all topics for this exam
    result = await db.execute(
        select(Topic).where(Topic.exam_type == exam_type).order_by(Topic.name)
    )
    topics = result.scalars().all()

    if not topics:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No topics found for exam type {exam_type}. Run the seed script first.",
        )

    # For each topic, pick random questions
    all_question_ids: list[str] = []
    topic_question_groups: list[DiagnosticTopicQuestions] = []

    for topic in topics:
        result = await db.execute(
            select(Question).where(
                Question.topic_id == topic.id,
                Question.exam_type == exam_type,
            )
        )
        available_questions = result.scalars().all()

        if not available_questions:
            continue

        # Pick up to QUESTIONS_PER_TOPIC, sampling across difficulties
        count = min(QUESTIONS_PER_TOPIC, len(available_questions))
        selected = random.sample(available_questions, count)

        diagnostic_questions = []
        for q in selected:
            all_question_ids.append(str(q.id))
            diagnostic_questions.append(
                DiagnosticQuestion(
                    id=q.id,
                    question_text=q.question_text,
                    question_type=q.question_type,
                    options=q.options,
                    difficulty=q.difficulty,
                    tags=q.tags,
                )
            )

        topic_question_groups.append(
            DiagnosticTopicQuestions(
                topic_id=topic.id,
                topic_name=topic.name,
                questions=diagnostic_questions,
            )
        )

    total_questions = len(all_question_ids)
    if total_questions == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No questions available for this exam. Run the seed script first.",
        )

    time_limit = total_questions * TIME_PER_QUESTION_MINUTES

    # Create diagnostic record
    diagnostic = DiagnosticTest(
        id=uuid.uuid4(),
        user_id=current_user.id,
        exam_type=exam_type,
        status="in_progress",
        started_at=datetime.utcnow(),
        time_limit_minutes=time_limit,
        total_questions=total_questions,
        question_ids=all_question_ids,
    )
    db.add(diagnostic)
    await db.flush()

    return DiagnosticStartResponse(
        diagnostic_id=diagnostic.id,
        exam_type=exam_type,
        time_limit_minutes=time_limit,
        total_questions=total_questions,
        topics=topic_question_groups,
    )


@router.post("/submit", response_model=DiagnosticResultResponse)
async def submit_diagnostic(
    submission: DiagnosticSubmitRequest,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Submit all answers for a diagnostic test.

    - Scores each answer
    - Computes per-topic mastery
    - Classifies topics as strong / moderate / weak
    - Updates UserTopicMastery records
    """
    # Fetch the diagnostic
    result = await db.execute(
        select(DiagnosticTest).where(
            DiagnosticTest.id == submission.diagnostic_id,
            DiagnosticTest.user_id == current_user.id,
        )
    )
    diagnostic = result.scalar_one_or_none()

    if not diagnostic:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Diagnostic test not found.",
        )

    if diagnostic.status != "in_progress":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This diagnostic test has already been completed.",
        )

    # Fetch all questions that were part of this diagnostic
    question_uuids = [uuid.UUID(qid) for qid in diagnostic.question_ids]
    result = await db.execute(
        select(Question).where(Question.id.in_(question_uuids))
    )
    questions = {str(q.id): q for q in result.scalars().all()}

    # Group questions by topic for scoring
    topic_results: dict[str, dict] = {}  # topic_id -> {topic_name, correct, total}

    total_correct = 0

    for qid_str, q in questions.items():
        topic_id_str = str(q.topic_id)

        if topic_id_str not in topic_results:
            # Fetch topic name
            topic_result = await db.execute(
                select(Topic).where(Topic.id == q.topic_id)
            )
            topic = topic_result.scalar_one_or_none()
            topic_results[topic_id_str] = {
                "topic_name": topic.name if topic else "Unknown",
                "correct": 0,
                "total": 0,
            }

        topic_results[topic_id_str]["total"] += 1

        # Check answer
        user_answer = submission.answers.get(qid_str, "").strip().upper()
        correct_answer = q.correct_answer.strip().upper()

        if user_answer == correct_answer:
            topic_results[topic_id_str]["correct"] += 1
            total_correct += 1

    # Calculate scores and classify topics
    topic_breakdown: list[TopicScore] = []
    topic_scores_json: dict = {}

    for topic_id_str, data in topic_results.items():
        score_pct = (data["correct"] / data["total"]) * 100 if data["total"] > 0 else 0

        if score_pct >= 70:
            strength = "strong"
        elif score_pct >= 40:
            strength = "moderate"
        else:
            strength = "weak"

        topic_breakdown.append(
            TopicScore(
                topic_id=uuid.UUID(topic_id_str),
                topic_name=data["topic_name"],
                correct=data["correct"],
                total=data["total"],
                score_percent=round(score_pct, 1),
                strength_level=strength,
            )
        )

        topic_scores_json[topic_id_str] = {
            "topic_name": data["topic_name"],
            "correct": data["correct"],
            "total": data["total"],
            "score": round(score_pct, 1),
            "strength_level": strength,
        }

        # Update UserTopicMastery
        mastery_result = await db.execute(
            select(UserTopicMastery).where(
                UserTopicMastery.user_id == current_user.id,
                UserTopicMastery.topic_id == uuid.UUID(topic_id_str),
            )
        )
        mastery = mastery_result.scalar_one_or_none()

        if mastery:
            mastery.total_questions_attempted += data["total"]
            mastery.correct_answers += data["correct"]
            mastery.mastery_score = score_pct
            mastery.last_practiced = datetime.utcnow()
        else:
            mastery = UserTopicMastery(
                id=uuid.uuid4(),
                user_id=current_user.id,
                topic_id=uuid.UUID(topic_id_str),
                total_questions_attempted=data["total"],
                correct_answers=data["correct"],
                mastery_score=score_pct,
                last_practiced=datetime.utcnow(),
            )
            db.add(mastery)

    # Update diagnostic record
    overall_score = (total_correct / diagnostic.total_questions) * 100 if diagnostic.total_questions > 0 else 0

    diagnostic.status = "completed"
    diagnostic.completed_at = datetime.utcnow()
    diagnostic.correct_answers = total_correct
    diagnostic.overall_score = round(overall_score, 1)
    diagnostic.topic_scores = topic_scores_json

    await db.flush()

    # Sort breakdown: weak first (they need most attention)
    strength_order = {"weak": 0, "moderate": 1, "strong": 2}
    topic_breakdown.sort(key=lambda t: strength_order.get(t.strength_level, 1))

    return DiagnosticResultResponse(
        diagnostic_id=diagnostic.id,
        exam_type=diagnostic.exam_type,
        status=diagnostic.status,
        overall_score=round(overall_score, 1),
        total_correct=total_correct,
        total_questions=diagnostic.total_questions,
        time_limit_minutes=diagnostic.time_limit_minutes,
        started_at=diagnostic.started_at,
        completed_at=diagnostic.completed_at,
        topic_breakdown=topic_breakdown,
    )


@router.get("/history", response_model=DiagnosticHistoryResponse)
async def get_diagnostic_history(
    limit: int = Query(20, ge=1, le=100, description="Max results to return"),
    offset: int = Query(0, ge=0, description="Pagination offset"),
    payload: TokenPayload = Depends(get_token_payload),
    db: AsyncSession = Depends(get_db),
):
    """
    Get the current user's diagnostic test history.

    - Ordered by most recent first
    - User identity is extracted directly from the JWT (no extra DB call)
    - Supports pagination via `limit` and `offset`
    """
    user_id = uuid.UUID(payload.sub)

    # Total count
    count_result = await db.execute(
        select(func.count()).where(DiagnosticTest.user_id == user_id)
    )
    total = count_result.scalar()

    # Paginated records, newest first
    result = await db.execute(
        select(DiagnosticTest)
        .where(DiagnosticTest.user_id == user_id)
        .order_by(DiagnosticTest.started_at.desc())
        .limit(limit)
        .offset(offset)
    )
    diagnostics = result.scalars().all()

    items = [
        DiagnosticHistoryItem(
            diagnostic_id=d.id,
            exam_type=d.exam_type,
            status=d.status,
            overall_score=d.overall_score,
            total_correct=d.correct_answers,
            total_questions=d.total_questions,
            time_limit_minutes=d.time_limit_minutes,
            started_at=d.started_at,
            completed_at=d.completed_at,
        )
        for d in diagnostics
    ]

    return DiagnosticHistoryResponse(total=total, items=items)


@router.get("/me", response_model=TokenPayload)
async def get_current_user_info(
    payload: TokenPayload = Depends(get_token_payload),
):
    """
    Return current user info decoded from the JWT — no database call.

    Useful for the frontend to get user identity (email, exam_type, etc.)
    without a separate profile API call.
    """
    return payload


@router.get("/{diagnostic_id}/result", response_model=DiagnosticResultResponse)
async def get_diagnostic_result(
    diagnostic_id: uuid.UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Get result of a completed diagnostic test."""
    result = await db.execute(
        select(DiagnosticTest).where(
            DiagnosticTest.id == diagnostic_id,
            DiagnosticTest.user_id == current_user.id,
        )
    )
    diagnostic = result.scalar_one_or_none()

    if not diagnostic:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Diagnostic test not found.",
        )

    if diagnostic.status != "completed":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Diagnostic test is not yet completed.",
        )

    # Build topic breakdown from stored JSON
    topic_breakdown: list[TopicScore] = []
    if diagnostic.topic_scores:
        for topic_id_str, data in diagnostic.topic_scores.items():
            topic_breakdown.append(
                TopicScore(
                    topic_id=uuid.UUID(topic_id_str),
                    topic_name=data["topic_name"],
                    correct=data["correct"],
                    total=data["total"],
                    score_percent=data["score"],
                    strength_level=data["strength_level"],
                )
            )

    strength_order = {"weak": 0, "moderate": 1, "strong": 2}
    topic_breakdown.sort(key=lambda t: strength_order.get(t.strength_level, 1))

    return DiagnosticResultResponse(
        diagnostic_id=diagnostic.id,
        exam_type=diagnostic.exam_type,
        status=diagnostic.status,
        overall_score=diagnostic.overall_score or 0,
        total_correct=diagnostic.correct_answers or 0,
        total_questions=diagnostic.total_questions,
        time_limit_minutes=diagnostic.time_limit_minutes,
        started_at=diagnostic.started_at,
        completed_at=diagnostic.completed_at,
        topic_breakdown=topic_breakdown,
    )
