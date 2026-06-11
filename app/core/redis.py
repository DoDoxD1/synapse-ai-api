import redis.asyncio as redis
from app.config import settings
from typing import Optional

redis_client: Optional[redis.Redis] = None


async def get_redis() -> redis.Redis:
    """Get Redis client instance"""
    return redis_client


async def init_redis():
    """Initialize Redis connection"""
    global redis_client
    redis_client = await redis.from_url(
        settings.REDIS_URL,
        encoding="utf-8",
        decode_responses=settings.REDIS_DECODE_RESPONSES
    )


async def close_redis():
    """Close Redis connection"""
    if redis_client:
        await redis_client.close()
