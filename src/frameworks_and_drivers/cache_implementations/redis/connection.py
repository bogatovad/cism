from redis.asyncio import Redis

from src.frameworks_and_drivers.cache_implementations.redis.settings import (
    redis_settings,
)

_redis_client: Redis | None = None


async def init_redis_connection() -> Redis:
    global _redis_client
    if _redis_client is None:
        _redis_client = Redis.from_url(redis_settings.url, decode_responses=True)
    return _redis_client


async def close_redis_connection() -> None:
    global _redis_client
    if _redis_client is not None:
        await _redis_client.aclose()
    _redis_client = None


def get_redis_client() -> Redis:
    if _redis_client is None:
        raise RuntimeError("Redis connection is not initialized")
    return _redis_client
