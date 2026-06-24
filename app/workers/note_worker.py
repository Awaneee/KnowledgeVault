import logging
import sys
import time
import app.database.base_all
import redis

from app.database.session import SessionLocal
from app.services.note_processing_service import NoteProcessingService
from app.services.queue_service import QueueService

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger("note_worker")


def main():
    logger.info("Worker started, waiting for jobs...")

    recovered = QueueService.recover_inflight_jobs()

    if recovered:
        logger.info(f"Recovered {recovered} inflight jobs")

    while True:
        try:
            try:
                job = QueueService.dequeue_note_processing(
                    timeout=5
                )
            except redis.exceptions.TimeoutError:
                continue

            if not job:
                continue

            note_id, user_id = job

            logger.info(
                f"PROCESSING NOTE {note_id}"
            )

            db = SessionLocal()

            try:
                processing_service = NoteProcessingService(
                    db
                )

                processing_service.process_note(
                    note_id,
                    user_id
                )

                QueueService.ack_job(
                    note_id,
                    user_id
                )

                logger.info(
                    f"NOTE ORGANIZED {note_id}"
                )

            except Exception:
                logger.exception(
                    f"NOTE FAILED {note_id}"
                )

            finally:
                db.close()

        except KeyboardInterrupt:
            logger.info(
                "Worker shutting down..."
            )
            break

        except Exception as e:
            logger.exception(
                f"Worker encountered unexpected error: {e}"
            )
            time.sleep(1)


if __name__ == "__main__":
    main()