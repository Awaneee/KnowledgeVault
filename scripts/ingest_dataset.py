"""
Phase 1-3: Dataset ingestion and categorization monitoring.

Usage:
    python scripts/ingest_dataset.py --user-id 1 [--batch-size 100] [--timeout 600] [--start-batch 0]

What this does:
  1. Loads 1000 notes from scripts/data/notes.py
  2. Ingests them in batches through the production pipeline:
       NoteService.create_note() -> Redis queue -> background worker ->
       intent extraction -> category assignment -> embeddings -> chunks
  3. After each batch: polls organization_status until all notes are processed
  4. Reports categorization stats after each batch
  5. Writes a categorization report to evaluation_results/categorization/

The script does NOT call the HTTP API — it uses the same service layer that
the API uses so the production pipeline runs identically.

Safety: if any batch has >10% failures, the script stops and reports.
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
import time
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import app.database.base_all  # noqa: F401 — registers all ORM models

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database.session import SessionLocal
from app.models.notes import Note
from app.models.intent_category import IntentCategory
from app.models.note_intent_assignment import NoteIntentAssignment
from app.schemas.note import NoteCreate
from app.services.note_service import NoteService
from data.notes import NOTES

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("ingest_dataset")

BATCH_FAILURE_THRESHOLD = 0.10  # stop if >10% of batch fails


# ---------------------------------------------------------------------------
# Ingestion helpers
# ---------------------------------------------------------------------------

def create_batch(note_contents: list[str], user_id: int, db: Session) -> list[int]:
    """Create notes via NoteService (which queues them for the worker)."""
    service = NoteService(db)
    note_ids = []
    for content in note_contents:
        try:
            result = service.create_note(NoteCreate(content=content), user_id=user_id)
            note_ids.append(result.id)
        except Exception as exc:
            logger.error("Failed to create note: %s | content=%.60r", exc, content)
    return note_ids


def wait_for_batch(
    note_ids: list[int],
    db: Session,
    timeout: int = 600,
    poll_interval: int = 5,
) -> dict:
    """
    Poll organization_status until all notes in the batch are terminal
    (organized or failed). Returns a summary dict.
    """
    deadline = time.monotonic() + timeout
    terminal_statuses = {"organized", "failed"}

    logger.info("Waiting for %d notes to process (timeout=%ds)...", len(note_ids), timeout)

    while time.monotonic() < deadline:
        rows = (
            db.query(Note.id, Note.organization_status)
            .filter(Note.id.in_(note_ids))
            .all()
        )
        status_map = {r.id: r.organization_status for r in rows}
        pending = [nid for nid in note_ids if status_map.get(nid) not in terminal_statuses]

        organized = sum(1 for s in status_map.values() if s == "organized")
        failed = sum(1 for s in status_map.values() if s == "failed")
        processing = sum(1 for s in status_map.values() if s == "processing")
        still_pending = sum(1 for s in status_map.values() if s == "pending")

        logger.info(
            "  Progress: organized=%d  failed=%d  processing=%d  pending=%d",
            organized, failed, processing, still_pending,
        )

        if not pending:
            return {
                "organized": organized,
                "failed": failed,
                "total": len(note_ids),
                "timed_out": False,
            }

        time.sleep(poll_interval)

    # Timed out — return current state
    rows = db.query(Note.id, Note.organization_status).filter(Note.id.in_(note_ids)).all()
    status_map = {r.id: r.organization_status for r in rows}
    return {
        "organized": sum(1 for s in status_map.values() if s == "organized"),
        "failed": sum(1 for s in status_map.values() if s == "failed"),
        "total": len(note_ids),
        "timed_out": True,
    }


# ---------------------------------------------------------------------------
# Categorization analysis
# ---------------------------------------------------------------------------

def analyze_categories(db: Session, user_id: int, batch_num: int, batch_note_ids: list[int]) -> dict:
    """Compute categorization metrics for the current state of the DB."""

    all_cats = db.query(IntentCategory).filter(IntentCategory.user_id == user_id).all()

    # Notes per category
    notes_per_cat = {}
    for cat in all_cats:
        count = (
            db.query(func.count(NoteIntentAssignment.id))
            .filter(NoteIntentAssignment.intent_category_id == cat.id)
            .scalar()
        )
        notes_per_cat[cat.id] = count

    total_cats = len(all_cats)
    singleton_cats = sum(1 for c in notes_per_cat.values() if c == 1)
    empty_cats = sum(1 for c in notes_per_cat.values() if c == 0)
    avg_notes = (
        sum(notes_per_cat.values()) / total_cats if total_cats else 0
    )

    # New categories for this batch: categories whose first assignment was a note in this batch
    batch_set = set(batch_note_ids)
    new_cats_this_batch = []
    reused_cats_this_batch = 0
    for cat in all_cats:
        assignments = (
            db.query(NoteIntentAssignment.note_id)
            .filter(NoteIntentAssignment.intent_category_id == cat.id)
            .all()
        )
        assigned_ids = {a.note_id for a in assignments}
        batch_assigned = assigned_ids & batch_set
        non_batch_assigned = assigned_ids - batch_set
        if batch_assigned and not non_batch_assigned:
            new_cats_this_batch.append(cat.name)
        elif batch_assigned and non_batch_assigned:
            reused_cats_this_batch += 1

    # Duplicate detection: categories with similar names (case-insensitive stem)
    from collections import defaultdict
    name_stems: dict[str, list[str]] = defaultdict(list)
    for cat in all_cats:
        stem = cat.name.lower().replace("-", " ").replace("_", " ").strip()
        name_stems[stem].append(cat.name)

    duplicates = {
        stem: names for stem, names in name_stems.items() if len(names) > 1
    }

    # Intent type distribution
    intent_dist: dict[str, int] = {}
    for cat in all_cats:
        intent_dist[cat.intent_type] = intent_dist.get(cat.intent_type, 0) + 1

    # Fragmentation: proportion of singleton categories
    fragmentation_rate = singleton_cats / total_cats if total_cats else 0

    total_notes = db.query(func.count(Note.id)).filter(Note.user_id == user_id).scalar()

    return {
        "batch_num": batch_num,
        "total_notes_in_db": total_notes,
        "total_categories": total_cats,
        "new_categories_this_batch": len(new_cats_this_batch),
        "new_category_names": new_cats_this_batch[:20],  # cap for readability
        "reused_categories_this_batch": reused_cats_this_batch,
        "singleton_categories": singleton_cats,
        "empty_categories": empty_cats,
        "avg_notes_per_category": round(avg_notes, 2),
        "fragmentation_rate": round(fragmentation_rate, 3),
        "duplicate_names": len(duplicates),
        "duplicate_examples": {k: v for k, v in list(duplicates.items())[:5]},
        "intent_type_distribution": intent_dist,
        "category_cap_used": total_cats >= 50,
    }


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------

def format_cat_report(stats: dict) -> str:
    lines = [
        f"\n{'='*60}",
        f"  BATCH {stats['batch_num']} — CATEGORIZATION REPORT",
        f"{'='*60}",
        f"  Total notes in DB    : {stats['total_notes_in_db']}",
        f"  Total categories     : {stats['total_categories']}",
        f"  New this batch       : {stats['new_categories_this_batch']}",
        f"  Reused this batch    : {stats['reused_categories_this_batch']}",
        f"  Singleton categories : {stats['singleton_categories']}",
        f"  Avg notes/category   : {stats['avg_notes_per_category']}",
        f"  Fragmentation rate   : {stats['fragmentation_rate']:.1%}",
        f"  Duplicate names      : {stats['duplicate_names']}",
        f"  Category cap (50)    : {'HIT' if stats['category_cap_used'] else 'OK'}",
        f"",
        f"  Intent type distribution:",
    ]
    for intent, count in sorted(stats["intent_type_distribution"].items(), key=lambda x: -x[1]):
        lines.append(f"    {intent:<16}: {count}")

    if stats["new_category_names"]:
        lines.append(f"\n  New categories created:")
        for name in stats["new_category_names"][:15]:
            lines.append(f"    - {name!r}")

    if stats["duplicate_examples"]:
        lines.append(f"\n  Duplicate name examples:")
        for stem, names in stats["duplicate_examples"].items():
            lines.append(f"    {stem!r} → {names}")

    lines.append(f"{'='*60}\n")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def parse_args():
    parser = argparse.ArgumentParser(description="Ingest 1000 notes in batches.")
    parser.add_argument("--user-id", type=int, default=1)
    parser.add_argument("--batch-size", type=int, default=100)
    parser.add_argument("--timeout", type=int, default=600, help="Seconds to wait per batch")
    parser.add_argument("--start-batch", type=int, default=0, help="Resume from batch N (0-indexed)")
    parser.add_argument("--output", type=str, default="evaluation_results/categorization")
    return parser.parse_args()


def main():
    args = parse_args()
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    logger.info("Dataset: %d notes, batch size: %d", len(NOTES), args.batch_size)
    logger.info("User ID: %d", args.user_id)
    logger.info("Starting from batch: %d", args.start_batch)

    batches = [
        NOTES[i:i + args.batch_size]
        for i in range(0, len(NOTES), args.batch_size)
    ]
    logger.info("Total batches: %d", len(batches))

    all_batch_stats = []
    all_ingested_ids = []

    for batch_idx, batch_notes in enumerate(batches):
        if batch_idx < args.start_batch:
            logger.info("Skipping batch %d (start-batch=%d)", batch_idx, args.start_batch)
            continue

        logger.info("\n" + "=" * 60)
        logger.info("BATCH %d/%d — ingesting %d notes", batch_idx + 1, len(batches), len(batch_notes))
        logger.info("=" * 60)

        db = SessionLocal()
        try:
            # Phase 1: create notes (queues them for the worker)
            t0 = time.monotonic()
            note_ids = create_batch(batch_notes, args.user_id, db)
            create_elapsed = time.monotonic() - t0
            logger.info(
                "Created %d/%d notes in %.1fs (queued for processing)",
                len(note_ids), len(batch_notes), create_elapsed,
            )

            if not note_ids:
                logger.error("No notes created in batch %d — stopping.", batch_idx)
                break

            # Phase 2: wait for worker to process
            wait_result = wait_for_batch(
                note_ids=note_ids,
                db=db,
                timeout=args.timeout,
            )

            logger.info(
                "Batch %d complete: organized=%d  failed=%d  timed_out=%s",
                batch_idx + 1,
                wait_result["organized"],
                wait_result["failed"],
                wait_result["timed_out"],
            )

            if wait_result["timed_out"]:
                logger.error(
                    "Batch %d timed out after %ds. "
                    "Only %d/%d notes processed. Stopping.",
                    batch_idx + 1, args.timeout,
                    wait_result["organized"] + wait_result["failed"],
                    len(note_ids),
                )
                break

            failure_rate = wait_result["failed"] / max(1, wait_result["total"])
            if failure_rate > BATCH_FAILURE_THRESHOLD:
                logger.error(
                    "Batch %d failure rate %.1f%% exceeds threshold %.1f%%. Stopping.",
                    batch_idx + 1,
                    failure_rate * 100,
                    BATCH_FAILURE_THRESHOLD * 100,
                )
                break

            # Phase 3: categorization analysis
            stats = analyze_categories(db, args.user_id, batch_idx + 1, note_ids)
            stats["batch_note_ids"] = note_ids
            stats["wait_result"] = wait_result
            all_batch_stats.append(stats)
            all_ingested_ids.extend(note_ids)

            print(format_cat_report(stats))

            # Save per-batch JSON
            batch_file = output_dir / f"batch_{batch_idx + 1:02d}.json"
            batch_file.write_text(json.dumps(stats, indent=2, default=str))
            logger.info("Batch stats saved: %s", batch_file)

        finally:
            db.close()

    # Final summary
    logger.info("\n" + "=" * 60)
    logger.info("INGESTION COMPLETE")
    logger.info("=" * 60)
    logger.info("Total notes ingested: %d", len(all_ingested_ids))
    logger.info("Total batches completed: %d", len(all_batch_stats))

    # Save full run summary
    summary = {
        "run_timestamp": datetime.utcnow().isoformat(),
        "user_id": args.user_id,
        "batch_size": args.batch_size,
        "total_notes_ingested": len(all_ingested_ids),
        "all_ingested_note_ids": all_ingested_ids,
        "batches_completed": len(all_batch_stats),
        "final_stats": all_batch_stats[-1] if all_batch_stats else {},
        "batch_history": [
            {
                "batch": s["batch_num"],
                "total_notes": s["total_notes_in_db"],
                "total_categories": s["total_categories"],
                "new_categories": s["new_categories_this_batch"],
                "fragmentation": s["fragmentation_rate"],
            }
            for s in all_batch_stats
        ],
    }
    summary_file = output_dir / "ingestion_summary.json"
    summary_file.write_text(json.dumps(summary, indent=2, default=str))
    logger.info("Full summary saved: %s", summary_file)

    if all_batch_stats:
        final = all_batch_stats[-1]
        logger.info("Final category count: %d", final["total_categories"])
        logger.info("Fragmentation rate: %.1f%%", final["fragmentation_rate"] * 100)
        logger.info("Avg notes/category: %.1f", final["avg_notes_per_category"])


if __name__ == "__main__":
    main()
