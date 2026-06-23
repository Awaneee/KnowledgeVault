import logging
import sys
import time

import app.database.base_all
from app.database.session import SessionLocal
from app.services.queue_service import QueueService
from app.services.note_processing_service import NoteProcessingService

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("note_worker")


def main():
    # Recover any jobs that were in-flight when the previous worker
    # instance died. Without this, a worker crash mid-job means the
    # job is silently lost - the note stays stuck at "processing"
    # status forever with no way to retry it automatically.
    recovered = QueueService.recover_inflight_jobs()
    if recovered:
        logger.info(f"Recovered {recovered} inflight job(s) from previous worker session")

    logger.info("Worker started, waiting for jobs...")

    while True:
        try:
            job = QueueService.dequeue_note_processing(timeout=5)
            if not job:
                continue

            note_id, user_id = job
            logger.info(f"PROCESSING NOTE {note_id}")

            db = SessionLocal()
            try:
                processing_service = NoteProcessingService(db)
                processing_service.process_note(note_id, user_id)
                # ACK only on success - job is removed from inflight queue.
                # On failure the job stays in inflight for recovery on
                # next worker restart, rather than being silently dropped.
                QueueService.ack_job(note_id, user_id)
                logger.info(f"NOTE ORGANIZED {note_id}")
            except Exception:
                logger.exception(f"NOTE FAILED {note_id} - job remains in inflight queue for recovery")
            finally:
                db.close()

        except KeyboardInterrupt:
            logger.info("Worker shutting down...")
            break
        except Exception as e:
            logger.exception(f"Worker encountered unexpected error: {e}")
            time.sleep(1)


if __name__ == "__main__":
    main()
