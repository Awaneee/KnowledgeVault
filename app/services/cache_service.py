import json

from app.core.redis_client import redis_client


class CacheService:

    @staticmethod
    def get(key: str):
        value = redis_client.get(key)

        if value:
            return json.loads(value)

        return None

    @staticmethod
    def set(
        key: str,
        value,
        expire_seconds: int = 3600
    ):
        redis_client.setex(
            key,
            expire_seconds,
            json.dumps(value)
        )