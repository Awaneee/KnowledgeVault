"""
Re-compute extraction_quality_score for all existing note_intents rows.

Run after applying migration d4e5f6a7b8c9_add_extraction_quality_score.

Usage:
    python scripts/backfill_quality_score.py [--user-id N]

The script processes rows where extraction_quality_score IS NULL.
It is safe to re-run — already-scored rows are skipped.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import app.database.base_all  # noqa: F401 — register all ORM models

from app.database.session import SessionLocal
from app.models.note_intent import NoteIntent
from app.services.intent_extraction_service import IntentExtractionService

BATCH_SIZE = 100


def run(user_id: int | None = None) -> None:
    db = SessionLocal()
    try:
        q = db.query(NoteIntent).filter(NoteIntent.extraction_quality_score.is_(None))
        if user_id is not None:
            q = q.filter(NoteIntent.user_id == user_id)

        rows = q.all()
        total = len(rows)
        print(f"Rows to backfill: {total}")

        updated = 0
        for row in rows:
            payload = {
                "intent_type": row.intent_type,
                "topic":       row.topic,
                "actor":       row.actor,
                "object":      row.object,
                "confidence":  row.confidence,
                "model_name":  row.model_name,
            }
            row.extraction_quality_score = IntentExtractionService.compute_extraction_quality(payload)
            updated += 1

            if updated % BATCH_SIZE == 0:
                db.commit()
                print(f"  Updated {updated}/{total}")

        db.commit()
        print(f"Done. Updated {updated} rows.")
    finally:
        db.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Backfill extraction_quality_score.")
    parser.add_argument("--user-id", type=int, default=None,
                        help="Limit to a specific user (default: all users).")
    args = parser.parse_args()
    run(user_id=args.user_id)
