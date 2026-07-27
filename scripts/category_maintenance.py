"""
scripts/category_maintenance.py
---------------------------------
Category lifecycle maintenance job (ADR-002).

Operations (all idempotent, all reported before applying):

  merge     — merge near-duplicate categories whose centroids are within
               MERGE_THRESHOLD (default 0.20) AND share the same intent_type
               AND neither has an actor.  Smaller category absorbs into larger.

  archive   — set status='archived' on categories with 0 assignments that
               have not been used for more than IDLE_DAYS (default 90) days.

  rename    — apply _sanitize_category_name() to all active categories whose
               current name would be rejected by the sanitizer.  Catches
               malformed names that predate Phase 1.

  centroids — for categories whose centroid_note_count > CENTROID_RECOMPUTE_ABOVE
               (default 100), recompute the centroid from all member note
               embeddings stored in the DB.  Corrects incremental mean drift.

  report    — print fragmentation stats and exit (no writes).

Usage
-----
  python scripts/category_maintenance.py --user-id 1                  # dry run
  python scripts/category_maintenance.py --user-id 1 --apply          # apply all
  python scripts/category_maintenance.py --user-id 1 --apply merge    # merge only
  python scripts/category_maintenance.py --user-id 1 report           # stats only

Safety
------
  - Dry-run is the default.  Pass --apply to write.
  - Merges archive the secondary category (status='merged') — never hard-delete.
  - All operations are logged at INFO level.
  - The script is safe to run repeatedly; every operation is idempotent.
"""

from __future__ import annotations

import argparse
import logging
import sys
import time
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import app.database.base_all  # noqa: F401

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.embedding_model import embedding_model
from app.database.session import SessionLocal
from app.models.intent_category import IntentCategory
from app.models.intent_category_embedding import IntentCategoryEmbedding
from app.models.note_intent_assignment import NoteIntentAssignment
from app.repositories.intent_category_repository import IntentCategoryRepository
from app.services.intent_category_service import IntentCategoryService

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("category_maintenance")

MERGE_THRESHOLD: float = 0.20       # cosine distance for near-duplicate detection
IDLE_DAYS: int = 90                 # days of zero usage before archiving
CENTROID_RECOMPUTE_ABOVE: int = 100 # recompute centroid when note_count exceeds this


# ---------------------------------------------------------------------------
# Helper: cosine distance (pure Python, no extra dependencies)
# ---------------------------------------------------------------------------

def _cosine_distance(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    mag_a = sum(x * x for x in a) ** 0.5
    mag_b = sum(x * x for x in b) ** 0.5
    if mag_a == 0 or mag_b == 0:
        return 1.0
    return 1.0 - dot / (mag_a * mag_b)


# ---------------------------------------------------------------------------
# Operation: merge near-duplicates
# ---------------------------------------------------------------------------

def find_merge_candidates(
    db: Session, user_id: int, threshold: float
) -> list[tuple[IntentCategory, IntentCategory, float]]:
    """
    Return (primary, secondary, distance) tuples where:
    - same intent_type, neither has an actor
    - centroid cosine distance < threshold
    - primary has >= notes as secondary (larger absorbs smaller)
    """
    cats = (
        db.query(IntentCategory)
        .filter(
            IntentCategory.user_id == user_id,
            IntentCategory.status == "active",
            IntentCategory.actor.is_(None),
        )
        .all()
    )

    embeddings: dict[int, list[float]] = {}
    for emb in db.query(IntentCategoryEmbedding).filter(
        IntentCategoryEmbedding.intent_category_id.in_([c.id for c in cats])
    ).all():
        embeddings[emb.intent_category_id] = list(emb.embedding_vector)

    # Group by intent_type
    by_type: dict[str, list[IntentCategory]] = defaultdict(list)
    for c in cats:
        if c.id in embeddings:
            by_type[c.intent_type].append(c)

    candidates = []
    for intent_type, group in by_type.items():
        for i, c1 in enumerate(group):
            for c2 in group[i + 1:]:
                dist = _cosine_distance(embeddings[c1.id], embeddings[c2.id])
                if dist < threshold:
                    # Primary = larger note count
                    primary, secondary = (
                        (c1, c2) if (c1.note_count or 0) >= (c2.note_count or 0)
                        else (c2, c1)
                    )
                    candidates.append((primary, secondary, dist))

    return sorted(candidates, key=lambda x: x[2])


def apply_merge(
    db: Session,
    user_id: int,
    primary: IntentCategory,
    secondary: IntentCategory,
    apply: bool,
    svc: IntentCategoryService,
) -> None:
    logger.info(
        "MERGE %s '%s' (id=%d, %d notes) <- '%s' (id=%d, %d notes) dist=COMPUTED",
        "APPLY" if apply else "DRY",
        primary.name, primary.id, primary.note_count or 0,
        secondary.name, secondary.id, secondary.note_count or 0,
    )
    if not apply:
        return

    # Reassign all assignments from secondary to primary
    assignments = (
        db.query(NoteIntentAssignment)
        .filter(NoteIntentAssignment.intent_category_id == secondary.id)
        .all()
    )
    for a in assignments:
        a.intent_category_id = primary.id
    db.flush()

    # Archive the secondary
    secondary.status = "merged"
    secondary.updated_at = datetime.utcnow()

    # Update primary note_count
    count = (
        db.query(func.count(NoteIntentAssignment.id))
        .filter(NoteIntentAssignment.intent_category_id == primary.id)
        .scalar()
    )
    primary.note_count = count
    primary.last_used_at = datetime.utcnow()
    primary.updated_at = datetime.utcnow()

    db.commit()

    # Recompute centroid for primary from all member assignments
    _recompute_centroid(db, primary, svc)
    logger.info("MERGE DONE primary_id=%d new_note_count=%d", primary.id, primary.note_count)


# ---------------------------------------------------------------------------
# Operation: archive idle categories
# ---------------------------------------------------------------------------

def find_archive_candidates(
    db: Session, user_id: int, idle_days: int
) -> list[IntentCategory]:
    cutoff = datetime.utcnow() - timedelta(days=idle_days)
    cats = (
        db.query(IntentCategory)
        .filter(
            IntentCategory.user_id == user_id,
            IntentCategory.status == "active",
            IntentCategory.note_count == 0,
        )
        .all()
    )
    return [
        c for c in cats
        if c.last_used_at is None or c.last_used_at < cutoff
    ]


def apply_archive(
    db: Session, category: IntentCategory, apply: bool
) -> None:
    logger.info(
        "ARCHIVE %s '%s' (id=%d) last_used=%s",
        "APPLY" if apply else "DRY",
        category.name, category.id,
        category.last_used_at.date() if category.last_used_at else "never",
    )
    if not apply:
        return
    category.status = "archived"
    category.updated_at = datetime.utcnow()
    db.commit()


# ---------------------------------------------------------------------------
# Operation: rename malformed categories
# ---------------------------------------------------------------------------

def find_rename_candidates(
    db: Session, user_id: int, svc: IntentCategoryService
) -> list[tuple[IntentCategory, str]]:
    """Return (category, new_name) for categories whose name would be sanitized."""
    cats = (
        db.query(IntentCategory)
        .filter(
            IntentCategory.user_id == user_id,
            IntentCategory.status == "active",
        )
        .all()
    )
    result = []
    for cat in cats:
        sanitized = svc._sanitize_category_name(cat.name)
        if sanitized != cat.name:
            result.append((cat, sanitized))
    return result


def apply_rename(
    db: Session, category: IntentCategory, new_name: str, apply: bool
) -> None:
    logger.info(
        "RENAME %s '%s' -> '%s' (id=%d)",
        "APPLY" if apply else "DRY",
        category.name, new_name, category.id,
    )
    if not apply:
        return
    # Check for name conflict
    existing = (
        db.query(IntentCategory)
        .filter(
            IntentCategory.user_id == category.user_id,
            IntentCategory.name == new_name,
            IntentCategory.status == "active",
            IntentCategory.id != category.id,
        )
        .first()
    )
    if existing:
        logger.warning(
            "RENAME SKIPPED conflict: '%s' already exists (id=%d)",
            new_name, existing.id,
        )
        return
    category.name = new_name
    category.updated_at = datetime.utcnow()
    db.commit()


# ---------------------------------------------------------------------------
# Operation: recompute centroids for large categories
# ---------------------------------------------------------------------------

def _recompute_centroid(
    db: Session, category: IntentCategory, svc: IntentCategoryService
) -> None:
    """
    Full centroid recompute: fetch note_intents for all assigned notes,
    re-embed each intent signature, average the vectors.
    Replaces the incremental mean that may have drifted.
    """
    from app.models.note_intent import NoteIntent

    assignments = (
        db.query(NoteIntentAssignment)
        .filter(NoteIntentAssignment.intent_category_id == category.id)
        .all()
    )
    if not assignments:
        return

    note_ids = [a.note_id for a in assignments]
    note_intents = (
        db.query(NoteIntent)
        .filter(NoteIntent.note_id.in_(note_ids))
        .all()
    )
    if not note_intents:
        return

    vectors = []
    for ni in note_intents:
        intent_dict = {
            "intent_type": ni.intent_type or "general",
            "action": ni.action, "actor": ni.actor, "topic": ni.topic,
            "subtopic": ni.subtopic, "object": ni.object,
            "due_date": None, "temporal_text": ni.temporal_text,
            "urgency": ni.urgency or "medium", "confidence": ni.confidence or 0.5,
            "category_hint": None, "source_text": "",
        }
        sig = svc._intent_signature(intent_dict)
        vectors.append(embedding_model.encode(sig).tolist())

    dim = len(vectors[0])
    centroid = [sum(v[d] for v in vectors) / len(vectors) for d in range(dim)]

    svc.category_repo.upsert_embedding(
        intent_category_id=category.id,
        embedding_model=IntentCategoryService.EMBEDDING_MODEL,
        embedding_vector=centroid,
        centroid_note_count=len(vectors),
    )
    logger.info(
        "CENTROID RECOMPUTED category='%s' id=%d notes=%d",
        category.name, category.id, len(vectors),
    )


def find_centroid_recompute_candidates(
    db: Session, user_id: int, above: int
) -> list[IntentCategory]:
    return (
        db.query(IntentCategory)
        .filter(
            IntentCategory.user_id == user_id,
            IntentCategory.status == "active",
            IntentCategory.note_count > above,
        )
        .all()
    )


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------

def print_report(db: Session, user_id: int) -> None:
    cats = (
        db.query(IntentCategory)
        .filter(IntentCategory.user_id == user_id)
        .all()
    )
    active = [c for c in cats if c.status == "active"]
    archived = [c for c in cats if c.status == "archived"]
    merged = [c for c in cats if c.status == "merged"]

    total_assigned = (
        db.query(func.count(NoteIntentAssignment.id))
        .filter(NoteIntentAssignment.user_id == user_id)
        .scalar()
    ) or 0

    note_counts = [c.note_count or 0 for c in active]
    singletons = sum(1 for n in note_counts if n <= 1)
    empty = sum(1 for n in note_counts if n == 0)
    max_notes = max(note_counts) if note_counts else 0
    avg_notes = sum(note_counts) / len(note_counts) if note_counts else 0

    print()
    print("=" * 60)
    print("CATEGORY MAINTENANCE REPORT")
    print("=" * 60)
    print(f"Active categories   : {len(active)}")
    print(f"Archived            : {len(archived)}")
    print(f"Merged              : {len(merged)}")
    print(f"Total assignments   : {total_assigned}")
    print(f"Avg notes/category  : {avg_notes:.1f}")
    print(f"Max notes/category  : {max_notes}")
    print(f"Singleton categories: {singletons} ({100*singletons/max(1,len(active)):.1f}%)")
    print(f"Empty categories    : {empty}")
    print()

    by_type = defaultdict(int)
    for c in active:
        by_type[c.intent_type] += 1
    print("By intent type:")
    for t, n in sorted(by_type.items()):
        print(f"  {t:<20s}: {n:3d}")
    print()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Category lifecycle maintenance.")
    parser.add_argument("--user-id", type=int, default=1)
    parser.add_argument("--apply", action="store_true",
                        help="Write changes (default: dry run).")
    parser.add_argument("--merge-threshold", type=float, default=MERGE_THRESHOLD)
    parser.add_argument("--idle-days", type=int, default=IDLE_DAYS)
    parser.add_argument("--centroid-above", type=int, default=CENTROID_RECOMPUTE_ABOVE)
    parser.add_argument(
        "ops", nargs="*", default=["merge", "archive", "rename", "centroids"],
        help="Operations to run (default: all). Options: merge archive rename centroids report",
    )
    args = parser.parse_args()

    db = SessionLocal()
    try:
        svc = IntentCategoryService(db)
        repo = IntentCategoryRepository(db)

        if "report" in args.ops or not args.ops:
            print_report(db, args.user_id)
            if args.ops == ["report"]:
                return

        t0 = time.monotonic()

        # ---- Merge -------------------------------------------------------
        if "merge" in args.ops:
            logger.info("--- MERGE (threshold=%.2f) ---", args.merge_threshold)
            candidates = find_merge_candidates(db, args.user_id, args.merge_threshold)
            logger.info("Found %d merge candidate pairs.", len(candidates))
            for primary, secondary, dist in candidates:
                apply_merge(db, args.user_id, primary, secondary, args.apply, svc)

        # ---- Archive -----------------------------------------------------
        if "archive" in args.ops:
            logger.info("--- ARCHIVE (idle_days=%d) ---", args.idle_days)
            candidates = find_archive_candidates(db, args.user_id, args.idle_days)
            logger.info("Found %d archive candidates.", len(candidates))
            for cat in candidates:
                apply_archive(db, cat, args.apply)

        # ---- Rename ------------------------------------------------------
        if "rename" in args.ops:
            logger.info("--- RENAME ---")
            candidates = find_rename_candidates(db, args.user_id, svc)
            logger.info("Found %d rename candidates.", len(candidates))
            for cat, new_name in candidates:
                apply_rename(db, cat, new_name, args.apply)

        # ---- Centroids ---------------------------------------------------
        if "centroids" in args.ops:
            logger.info("--- CENTROID RECOMPUTE (above=%d notes) ---", args.centroid_above)
            candidates = find_centroid_recompute_candidates(
                db, args.user_id, args.centroid_above
            )
            logger.info("Found %d categories needing centroid recompute.", len(candidates))
            for cat in candidates:
                if args.apply:
                    _recompute_centroid(db, cat, svc)
                else:
                    logger.info(
                        "DRY would recompute centroid: '%s' (id=%d, %d notes)",
                        cat.name, cat.id, cat.note_count,
                    )

        elapsed = time.monotonic() - t0
        logger.info(
            "Maintenance %s in %.1fs",
            "APPLIED" if args.apply else "DRY RUN (pass --apply to write)",
            elapsed,
        )

        if args.apply:
            print_report(db, args.user_id)

    finally:
        db.close()


if __name__ == "__main__":
    main()
