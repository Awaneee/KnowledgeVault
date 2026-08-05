import json
import logging

from app.core.redis_client import redis_client

logger = logging.getLogger(__name__)


class CacheService:

    @staticmethod
    def get(key: str):
        try:
            value = redis_client.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as exc:
            logger.warning("Cache get failed (key=%s): %s", key, exc)
            return None

    @staticmethod
    def set(
        key: str,
        value,
        expire_seconds: int = 3600
    ):
        try:
            redis_client.setex(
                key,
                expire_seconds,
                json.dumps(value)
            )
        except Exception as exc:
            logger.warning("Cache set failed (key=%s): %s", key, exc)

    @staticmethod
    def delete_pattern(pattern: str) -> int:
        """Delete all keys matching glob pattern. Returns count deleted."""
        try:
            keys = list(redis_client.scan_iter(pattern))
            if keys:
                return redis_client.delete(*keys)
            return 0
        except Exception as exc:
            logger.warning("Cache delete_pattern failed (pattern=%s): %s", pattern, exc)
            return 0