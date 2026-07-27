"""
scripts/reassign_categories.py
-------------------------------
Phase 1 validation: wipe existing intent_categories and note_intent_assignments
for a user, then replay category assignment from cached note_intents records.

WHY: This tests the Phase 1 changes (cap_hit, centroid embedding, malformed
name sanitization) without re-running LLM intent extraction.  The existing
note_intents rows were produced by the original Gemini calls; we only replay
the category-assignment step, which is what Phase 1 changed.

Usage:
    python scripts/reassign_categories.py --user-id 1
    python scripts/reassign_categories.py --user-id 1 --dry-run   # no writes

Run from project root with .env loaded.
"""

from __future__ import annotations

import argparse
import logging
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import app.database.base_all  # noqa: F401

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database.session import SessionLocal
from app.models.intent_category import IntentCategory
from app.models.intent_category_embedding import IntentCategoryEmbedding
from app.models.note_intent import NoteIntent
from app.models.note_intent_assignment import NoteIntentAssignment
from app.services.intent_category_service import IntentCategoryService

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("reassign_categories")


def _intent_dict(ni: NoteIntent) -> dict:
    """Reconstruct a process_note-compatible intent dict from a stored NoteIntent row."""
    return {
        "intent_type": ni.intent_type or "general",
        "action": ni.action,
        "actor": ni.actor,
        "topic": ni.topic,
        "subtopic": ni.subtopic,
        "object": ni.object,
        "due_date": ni.due_date,
        "temporal_text": ni.temporal_text,
        "urgency": ni.urgency or "medium",
        "confidence": ni.confidence or 0.5,
        "category_hint": None,
        "source_text": "",
        "raw_llm_json": ni.raw_llm_json,
        "model_name": ni.model_name,
        "prompt_version": ni.prompt_version,
        "reasoning_summary": ni.reasoning_summary,
    }


def wipe_categories(db: Session, user_id: int) -> tuple[int, int]:
    """Delete all category assignments and categories for user. Returns (cats, assignments) deleted."""
    assignments_deleted = (
        db.query(NoteIntentAssignment)
        .filter(NoteIntentAssignment.user_id == user_id)
        .delete(synchronize_session=False)
    )
    categories_deleted = (
        db.query(IntentCategory)
        .filter(IntentCategory.user_id == user_id)
        .delete(synchronize_session=False)
    )
    db.commit()
    return categories_deleted, assignments_deleted


def reassign(db: Session, user_id: int) -> dict:
    """
    For every existing note_intent row (cached LLM output), run the Phase 1
    category-assignment logic and create fresh categories + assignments.
    """
    service = IntentCategoryService(db)

    note_intents: list[NoteIntent] = (
        db.query(NoteIntent)
        .filter(NoteIntent.user_id == user_id)
        .order_by(NoteIntent.note_id)
        .all()
    )

    total = len(note_intents)
    stats = {
        "total": total,
        "assigned": 0,
        "cap_hit": 0,
        "created": 0,
        "reused_canonical": 0,
        "reused_rule": 0,
        "reused_vector": 0,
        "errors": 0,
    }

    t0 = time.monotonic()

    for i, ni in enumerate(note_intents, 1):
        try:
            intent = _intent_dict(ni)
            intent = service._normalize_intent_fields(intent)

            category, method, score = service._find_or_create_category(
                user_id=user_id,
                intent=intent,
            )

            if category is None:
                stats["cap_hit"] += 1
                if i % 50 == 0 or i == total:
                    logger.info(
                        "Progress %d/%d  categories=%d  cap_hit=%d",
                        i, total,
                        service.category_repo.count_by_user(user_id),
                        stats["cap_hit"],
                    )
                continue

            service.intent_repo.create_or_update_assignment(
                note_id=ni.note_id,
                user_id=user_id,
                intent_category_id=category.id,
                confidence=intent["confidence"],
                assignment_method=method,
            )

            service.category_repo.touch_after_assignment(category_id=category.id)
            service._refresh_category_embedding(category=category, intent=intent)

            stats["assigned"] += 1
            if method == "created":
                stats["created"] += 1
            elif method == "canonical_name":
                stats["reused_canonical"] += 1
            elif method == "exact_rule":
                stats["reused_rule"] += 1
            elif method == "vector":
                stats["reused_vector"] += 1

            if i % 100 == 0 or i == total:
                elapsed = time.monotonic() - t0
                cats = service.category_repo.count_by_user(user_id)
                logger.info(
                    "Progress %d/%d  categories=%d  created=%d  cap_hit=%d  elapsed=%.1fs",
                    i, total, cats,
                    stats["created"], stats["cap_hit"], elapsed,
                )

        except Exception as exc:
            logger.exception("FAILED note_id=%d: %s", ni.note_id, exc)
            db.rollback()
            stats["errors"] += 1

    stats["elapsed_seconds"] = round(time.monotonic() - t0, 1)
    stats["final_category_count"] = service.category_repo.count_by_user(user_id)
    return stats


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--user-id", type=int, default=1)
    parser.add_argument("--dry-run", action="store_true",
                        help="Print what would happen without touching the DB.")
    args = parser.parse_args()

    db = SessionLocal()
    try:
        if args.dry_run:
            cats = db.query(func.count(IntentCategory.id)).filter(
                IntentCategory.user_id == args.user_id
            ).scalar()
            assigns = db.query(func.count(NoteIntentAssignment.id)).filter(
                NoteIntentAssignment.user_id == args.user_id
            ).scalar()
            intents = db.query(func.count(NoteIntent.id)).filter(
                NoteIntent.user_id == args.user_id
            ).scalar()
            logger.info("DRY RUN: would delete %d categories, %d assignments", cats, assigns)
            logger.info("DRY RUN: would reassign %d notes from cached note_intents", intents)
            return

        logger.info("=== STEP 1: Wiping existing categories and assignments ===")
        cats_del, assigns_del = wipe_categories(db, args.user_id)
        logger.info("Deleted: %d categories, %d assignments", cats_del, assigns_del)

        logger.info("=== STEP 2: Replaying category assignment from cached intents ===")
        stats = reassign(db, args.user_id)

        logger.info("=== DONE ===")
        logger.info("Total note_intents processed : %d", stats["total"])
        logger.info("Assigned to a category       : %d (%.1f%%)",
                    stats["assigned"], 100 * stats["assigned"] / max(1, stats["total"]))
        logger.info("Uncategorized (cap_hit)      : %d (%.1f%%)",
                    stats["cap_hit"], 100 * stats["cap_hit"] / max(1, stats["total"]))
        logger.info("New categories created        : %d", stats["created"])
        logger.info("Reused canonical_name        : %d", stats["reused_canonical"])
        logger.info("Reused exact_rule            : %d", stats["reused_rule"])
        logger.info("Reused vector                : %d", stats["reused_vector"])
        logger.info("Errors                       : %d", stats["errors"])
        logger.info("Final category count         : %d", stats["final_category_count"])
        logger.info("Elapsed                      : %.1fs", stats["elapsed_seconds"])

    finally:
        db.close()


if __name__ == "__main__":
    main()
