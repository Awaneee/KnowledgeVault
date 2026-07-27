"""
Note processing worker.

Polls the Redis queue for note-processing jobs, runs the full pipeline
(embedding → chunking → intent extraction → category assignment), and
acknowledges the job on success.

Startup: recovers any in-flight jobs left over from a previous crash.
"""

import logging
import sys
import time

import redis

import app.database.base_all  # noqa: F401 — registers all ORM models
from app.database.session import SessionLocal
from app.services.note_processing_service import NoteProcessingService
from app.services.queue_service import QueueService


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

logger = logging.getLogger("note_worker")


def main() -> None:
    logger.info("WORKER STARTED — waiting for jobs")

    recovered = QueueService.recover_inflight_jobs()
    if recovered:
        logger.info("WORKER RECOVERED inflight_jobs=%d", recovered)

    while True:
        try:
            try:
                job = QueueService.dequeue_note_processing(timeout=5)
            except redis.exceptions.TimeoutError:
                continue

            if not job:
                continue

            note_id, user_id = job

            logger.info(
                "JOB DEQUEUED note_id=%d user_id=%d", note_id, user_id
            )

            t0 = time.monotonic()
            db = SessionLocal()

            try:
                service = NoteProcessingService(db)
                service.process_note(note_id=note_id, user_id=user_id)

                QueueService.ack_job(note_id, user_id)

                elapsed = time.monotonic() - t0
                logger.info(
                    "JOB DONE note_id=%d user_id=%d elapsed=%.2fs",
                    note_id,
                    user_id,
                    elapsed,
                )

            except Exception:
                elapsed = time.monotonic() - t0
                logger.exception(
                    "JOB FAILED note_id=%d user_id=%d elapsed=%.2fs",
                    note_id,
                    user_id,
                    elapsed,
                )

            finally:
                db.close()

        except KeyboardInterrupt:
            logger.info("WORKER SHUTDOWN requested")
            break

        except Exception as exc:
            logger.exception("WORKER UNEXPECTED ERROR error=%s", exc)
            time.sleep(1)


if __name__ == "__main__":
    main()