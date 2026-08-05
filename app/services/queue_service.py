import json
import logging

from app.core.redis_client import redis_client

logger = logging.getLogger(__name__)

QUEUE_NAME = "note_processing_queue"
PROCESSING_QUEUE = "note_processing_inflight"


class QueueService:

    @staticmethod
    def enqueue_note_processing(note_id: int, user_id: int) -> bool:
        """Enqueue a note for background processing. Returns False if Redis is unavailable."""
        job_data = {
            "note_id": note_id,
            "user_id": user_id
        }
        try:
            redis_client.lpush(QUEUE_NAME, json.dumps(job_data))
            return True
        except Exception as exc:
            logger.error(
                "Failed to enqueue note_id=%s user_id=%s: %s",
                note_id, user_id, exc
            )
            return False

    @staticmethod
    def dequeue_note_processing(timeout: int = 0) -> tuple[int, int] | None:
        # brpoplpush atomically moves the job from the main queue to the
        # inflight queue in a single operation. If the worker crashes
        # mid-job, the job stays in PROCESSING_QUEUE and is recovered
        # on the next worker startup via recover_inflight_jobs(), rather
        # than being silently lost as it would be with a plain brpop.
        result = redis_client.brpoplpush(
            QUEUE_NAME,
            PROCESSING_QUEUE,
            timeout=timeout
        )

        if result:
            job_data = json.loads(result)
            return job_data["note_id"], job_data["user_id"]

        return None

    @staticmethod
    def ack_job(note_id: int, user_id: int):
        """
        Remove a completed job from the inflight queue.
        Call this after successful processing - not on failure, so that
        failed jobs remain in the inflight queue for inspection/recovery.
        """
        job_data = json.dumps({"note_id": note_id, "user_id": user_id})
        redis_client.lrem(PROCESSING_QUEUE, 1, job_data)

    @staticmethod
    def recover_inflight_jobs():
        """
        On worker startup, move any jobs left in the inflight queue back
        to the main queue. These are jobs that were dequeued by a previous
        worker instance that crashed before completing them.
        """
        recovered = 0
        while True:
            job = redis_client.rpoplpush(PROCESSING_QUEUE, QUEUE_NAME)
            if not job:
                break
            recovered += 1

        return recovered
