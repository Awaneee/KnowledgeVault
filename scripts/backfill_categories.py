"""
scripts/backfill_categories.py
-------------------------------
One-shot migration script: renames existing intent_categories that were
created with the old verbose naming scheme to the new concise names
(≤ 4 words, e.g. "Communication - Sid", "Study - PostgreSQL").

Safety:
- Dry-run by default (pass --apply to write).
- Skips categories whose name is already ≤ 4 words.
- Skips if the new name would conflict with an existing category.
- Prints a summary at the end.

Usage:
  # Preview what would change:
  python scripts/backfill_categories.py

  # Apply the renames:
  python scripts/backfill_categories.py --apply

Run from the project root with the .env loaded (the script reads DATABASE_URL).
"""

import argparse
import sys
import os

# Allow running from project root without installing the package.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database.session import SessionLocal  # noqa: E402
from app.models.intent_category import IntentCategory  # noqa: E402
from app.services.intent_category_service import IntentCategoryService  # noqa: E402


def _words(name: str) -> int:
    return len(name.split())


def main(apply: bool) -> None:
    db = SessionLocal()
    service = IntentCategoryService(db)

    try:
        categories: list[IntentCategory] = (
            db.query(IntentCategory)
            .filter(IntentCategory.status == "active")
            .order_by(IntentCategory.user_id, IntentCategory.id)
            .all()
        )

        print(f"Found {len(categories)} active categories.")
        renamed = 0
        skipped_short = 0
        skipped_conflict = 0
        errors = 0

        for cat in categories:
            if _words(cat.name) <= 4:
                skipped_short += 1
                continue

            # Build a minimal fake intent so we can call _generate_category_name.
            fake_intent = {
                "intent_type": cat.intent_type,
                "actor": cat.actor,
                "action": cat.action,
                "topic": None,
                "subtopic": None,
                "object": None,
                "category_hint": None,
                "source_text": cat.description or "",
            }
            new_name = service._generate_category_name(fake_intent)

            if new_name == cat.name:
                skipped_short += 1
                continue

            # Check for conflict.
            conflict = (
                db.query(IntentCategory)
                .filter(
                    IntentCategory.user_id == cat.user_id,
                    IntentCategory.name == new_name,
                    IntentCategory.id != cat.id,
                    IntentCategory.status == "active",
                )
                .first()
            )
            if conflict:
                print(
                    f"  SKIP (conflict) [{cat.id}] {cat.name!r} "
                    f"→ {new_name!r} (conflicts with id={conflict.id})"
                )
                skipped_conflict += 1
                continue

            print(f"  RENAME [{cat.id}] {cat.name!r} → {new_name!r}")

            if apply:
                try:
                    cat.name = new_name
                    db.commit()
                    renamed += 1
                except Exception as exc:
                    db.rollback()
                    print(f"    ERROR renaming id={cat.id}: {exc}")
                    errors += 1
            else:
                renamed += 1

        print(
            f"\n{'APPLIED' if apply else 'DRY RUN'} SUMMARY\n"
            f"  Would rename / renamed : {renamed}\n"
            f"  Skipped (already short): {skipped_short}\n"
            f"  Skipped (conflict)     : {skipped_conflict}\n"
            f"  Errors                 : {errors}\n"
        )
        if not apply:
            print("Run with --apply to apply changes.")

    finally:
        db.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Backfill intent_categories to new concise naming scheme."
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Write changes to the database (default: dry run).",
    )
    args = parser.parse_args()
    main(apply=args.apply)
