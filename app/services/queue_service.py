import json
from app.core.redis_client import redis_client

QUEUE_NAME = "note_processing_queue"


class QueueService:
    @staticmethod
    def enqueue_note_processing(note_id: int, user_id: int):
        job_data = {
            "note_id": note_id,
            "user_id": user_id
        }
        redis_client.lpush(QUEUE_NAME, json.dumps(job_data))

    @staticmethod
    def dequeue_note_processing(timeout: int = 0) -> tuple[int, int] | None:
        result = redis_client.brpop(QUEUE_NAME, timeout=timeout)
        if result:
            _, value = result
            job_data = json.loads(value)
            return job_data["note_id"], job_data["user_id"]
        return None
