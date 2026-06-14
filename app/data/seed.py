"""
Database seed script for topics and questions.
Run with: python -m app.data.seed

Idempotent — skips already-seeded data.
"""

import asyncio
import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.config import settings
from app.core.database import Base
# Import ALL models so SQLAlchemy can resolve relationships
from app.models.user import User  # noqa: F401
from app.models.topic import Topic
from app.models.question import Question
from app.models.study_session import StudySession, StudyPlan  # noqa: F401
from app.models.mock_test import MockTest, MockTestAttempt  # noqa: F401
from app.models.gamification import UserStats, UserAchievement  # noqa: F401
from app.models.diagnostic import DiagnosticTest  # noqa: F401
from app.data.exam_topics import EXAM_TOPICS
from app.data.seed_questions import EXAM_QUESTIONS


async def seed_topics(session: AsyncSession) -> dict[str, uuid.UUID]:
    """Seed topics and return a mapping of (exam_type, topic_name) -> topic_id."""
    topic_map: dict[str, uuid.UUID] = {}
    created = 0
    skipped = 0

    for exam_type, topics in EXAM_TOPICS.items():
        for topic_data in topics:
            # Check if topic already exists
            result = await session.execute(
                select(Topic).where(
                    Topic.exam_type == exam_type.value,
                    Topic.name == topic_data["name"],
                )
            )
            existing = result.scalar_one_or_none()

            if existing:
                topic_map[f"{exam_type.value}::{topic_data['name']}"] = existing.id
                skipped += 1
                continue

            topic = Topic(
                id=uuid.uuid4(),
                exam_type=exam_type.value,
                name=topic_data["name"],
                difficulty_level=topic_data["difficulty_level"],
                exam_weight=topic_data["exam_weight"],
                description=topic_data["description"],
            )
            session.add(topic)
            topic_map[f"{exam_type.value}::{topic_data['name']}"] = topic.id
            created += 1

    await session.flush()
    print(f"  Topics: {created} created, {skipped} skipped (already exist)")
    return topic_map


async def seed_questions(session: AsyncSession, topic_map: dict[str, uuid.UUID]) -> None:
    """Seed questions linked to topics."""
    created = 0
    skipped = 0

    for exam_type, topics_questions in EXAM_QUESTIONS.items():
        for topic_name, questions in topics_questions.items():
            key = f"{exam_type.value}::{topic_name}"
            topic_id = topic_map.get(key)

            if not topic_id:
                print(f"  ⚠ Topic not found: {key}, skipping questions")
                continue

            for q_data in questions:
                # Check if question already exists (by text + topic)
                result = await session.execute(
                    select(Question).where(
                        Question.topic_id == topic_id,
                        Question.question_text == q_data["question_text"],
                    )
                )
                if result.scalar_one_or_none():
                    skipped += 1
                    continue

                question = Question(
                    id=uuid.uuid4(),
                    topic_id=topic_id,
                    exam_type=exam_type.value,
                    question_text=q_data["question_text"],
                    question_type="mcq",
                    options=q_data["options"],
                    correct_answer=q_data["correct_answer"],
                    explanation=q_data["explanation"],
                    difficulty=q_data["difficulty"],
                    source="curated",
                    tags=q_data.get("tags", []),
                )
                session.add(question)
                created += 1

    await session.flush()
    print(f"  Questions: {created} created, {skipped} skipped (already exist)")


async def run_seed():
    """Main seed function."""
    print("=" * 50)
    print("🌱 Synapse AI — Database Seeder")
    print("=" * 50)

    engine = create_async_engine(settings.DATABASE_URL, echo=False)

    # Create tables if they don't exist
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        async with session.begin():
            print("\n📚 Seeding topics...")
            topic_map = await seed_topics(session)

            print("\n❓ Seeding questions...")
            await seed_questions(session, topic_map)

        print("\n✅ Seed complete!")

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(run_seed())
