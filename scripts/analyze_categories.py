"""
Phase 3 / 5: Categorization quality analysis.

Usage:
    python scripts/analyze_categories.py --user-id 1 --output evaluation_results/

Reads the current database state and writes:
    evaluation_results/CATEGORY_ANALYSIS.md
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import app.database.base_all  # noqa: F401
from app.database.session import SessionLocal
from app.models.intent_category import IntentCategory
from app.models.note_intent_assignment import NoteIntentAssignment
from app.models.notes import Note
from sqlalchemy import func
from sqlalchemy.orm import Session

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("analyze_categories")


# ---------------------------------------------------------------------------
# Data collection
# ---------------------------------------------------------------------------

def collect(db: Session, user_id: int) -> dict:
    cats = db.query(IntentCategory).filter(IntentCategory.user_id == user_id).all()

    notes_per_cat: dict[int, int] = {}
    for cat in cats:
        count = (
            db.query(func.count(NoteIntentAssignment.id))
            .filter(NoteIntentAssignment.intent_category_id == cat.id)
            .scalar()
        )
        notes_per_cat[cat.id] = count

    # Assignment method distribution
    method_counts: dict[str, int] = defaultdict(int)
    assignments = db.query(NoteIntentAssignment).filter(NoteIntentAssignment.user_id == user_id).all()
    for a in assignments:
        method_counts[a.assignment_method or "unknown"] += 1

    # Intent type distribution
    intent_dist: dict[str, list[str]] = defaultdict(list)
    for cat in cats:
        intent_dist[cat.intent_type].append(cat.name)

    # Duplicate detection (name stems)
    name_stems: dict[str, list[str]] = defaultdict(list)
    for cat in cats:
        stem = (
            cat.name.lower()
            .replace("-", " ").replace("_", " ")
            .replace("study ", "").replace("reference ", "")
            .strip()
        )
        name_stems[stem].append(cat.name)
    duplicates = {stem: names for stem, names in name_stems.items() if len(names) > 1}

    # Suspicious categories (generic, overly broad)
    SUSPICIOUS_STEMS = {
        "study", "study notes", "learning", "learning notes",
        "database", "databases", "postgres", "postgresql",
        "general", "misc", "miscellaneous", "note", "notes",
        "todo", "task", "tasks", "reference", "info",
    }
    suspicious = [
        cat.name for cat in cats
        if cat.name.strip().lower() in SUSPICIOUS_STEMS
        or any(cat.name.strip().lower() == s for s in SUSPICIOUS_STEMS)
    ]

    total_notes = db.query(func.count(Note.id)).filter(Note.user_id == user_id).scalar()
    organized = db.query(func.count(Note.id)).filter(
        Note.user_id == user_id, Note.organization_status == "organized"
    ).scalar()
    failed = db.query(func.count(Note.id)).filter(
        Note.user_id == user_id, Note.organization_status == "failed"
    ).scalar()

    counts = list(notes_per_cat.values())
    total_cats = len(cats)
    singleton_cats = sum(1 for c in counts if c == 1)
    empty_cats = sum(1 for c in counts if c == 0)
    avg_notes = sum(counts) / total_cats if total_cats else 0
    max_notes = max(counts) if counts else 0
    min_notes = min(counts) if counts else 0
    fragmentation_rate = singleton_cats / total_cats if total_cats else 0

    # Category cap check
    at_cap = total_cats >= 50

    # Top 10 largest categories
    cat_by_id = {cat.id: cat for cat in cats}
    top_cats = sorted(notes_per_cat.items(), key=lambda x: -x[1])[:15]

    return {
        "total_notes": total_notes,
        "organized": organized,
        "failed": failed,
        "total_categories": total_cats,
        "singleton_categories": singleton_cats,
        "empty_categories": empty_cats,
        "avg_notes_per_category": round(avg_notes, 2),
        "max_notes_in_category": max_notes,
        "min_notes_in_category": min_notes,
        "fragmentation_rate": round(fragmentation_rate, 4),
        "category_cap_used": at_cap,
        "category_reuse_rate": round(1 - fragmentation_rate, 4),
        "duplicates": duplicates,
        "suspicious_categories": suspicious,
        "intent_distribution": {k: v for k, v in sorted(intent_dist.items())},
        "method_distribution": dict(method_counts),
        "top_categories": [
            {
                "id": cat_id,
                "name": cat_by_id[cat_id].name,
                "intent_type": cat_by_id[cat_id].intent_type,
                "notes": count,
            }
            for cat_id, count in top_cats
        ],
        "all_categories": [
            {
                "id": cat.id,
                "name": cat.name,
                "intent_type": cat.intent_type,
                "notes": notes_per_cat.get(cat.id, 0),
                "actor": cat.actor,
            }
            for cat in sorted(cats, key=lambda c: c.name)
        ],
    }


# ---------------------------------------------------------------------------
# Report writing
# ---------------------------------------------------------------------------

def write_markdown(data: dict, path: Path) -> None:
    lines = []

    def h(n, text):
        lines.append(f"\n{'#' * n} {text}\n")

    def p(text=""):
        lines.append(text)

    def table(headers: list[str], rows: list[list]):
        lines.append("| " + " | ".join(headers) + " |")
        lines.append("| " + " | ".join(["---"] * len(headers)) + " |")
        for row in rows:
            lines.append("| " + " | ".join(str(c) for c in row) + " |")

    h(1, "KnowledgeVault — Category Analysis Report")
    p(f"> Generated after ingesting {data['total_notes']} notes through the production pipeline.")
    p()

    h(2, "1. Overall Statistics")
    table(
        ["Metric", "Value"],
        [
            ["Total Notes", data["total_notes"]],
            ["Organized", data["organized"]],
            ["Failed", data["failed"]],
            ["Processing Success Rate", f"{data['organized'] / max(1, data['total_notes']):.1%}"],
            ["Total Categories", data["total_categories"]],
            ["Category Cap (50) Reached", "YES ⚠️" if data["category_cap_used"] else "No"],
            ["Singleton Categories", data["singleton_categories"]],
            ["Empty Categories", data["empty_categories"]],
            ["Avg Notes per Category", data["avg_notes_per_category"]],
            ["Max Notes in One Category", data["max_notes_in_category"]],
            ["Fragmentation Rate", f"{data['fragmentation_rate']:.1%}"],
            ["Category Reuse Rate", f"{data['category_reuse_rate']:.1%}"],
        ],
    )

    h(3, "Fragmentation Rate Interpretation")
    frag = data["fragmentation_rate"]
    if frag < 0.20:
        interp = "**Excellent** — most categories absorb multiple notes. Strong reuse."
    elif frag < 0.35:
        interp = "**Good** — moderate reuse with some singletons. Normal for diverse content."
    elif frag < 0.50:
        interp = "**Fair** — notable fragmentation. Many single-note categories. Review naming thresholds."
    else:
        interp = "**Poor** — over half of categories hold only one note. Category naming is too specific."
    p(f"{frag:.1%} fragmentation — {interp}")

    h(2, "2. Assignment Method Distribution")
    methods = data["method_distribution"]
    total_assign = sum(methods.values())
    table(
        ["Method", "Count", "Percentage", "Explanation"],
        [
            [
                method,
                count,
                f"{count / max(1, total_assign):.1%}",
                {
                    "canonical_name": "Exact name match — highest confidence reuse",
                    "exact_rule": "Rule-based match (intent type + actor) — reliable for communication",
                    "vector": "Semantic embedding similarity — approximate reuse",
                    "created": "New category created — no suitable existing category found",
                    "cap_fallback": "Category cap (50) reached — forced into nearest category",
                }.get(method, "Other")
            ]
            for method, count in sorted(methods.items(), key=lambda x: -x[1])
        ],
    )

    h(2, "3. Intent Type Distribution")
    table(
        ["Intent Type", "Categories", "Category Names"],
        [
            [
                intent,
                len(names),
                ", ".join(f"`{n}`" for n in names[:5]) + ("..." if len(names) > 5 else "")
            ]
            for intent, names in sorted(data["intent_distribution"].items(), key=lambda x: -len(x[1]))
        ],
    )

    h(2, "4. Top 15 Categories by Note Count")
    table(
        ["Rank", "Category Name", "Intent Type", "Notes"],
        [
            [i + 1, cat["name"], cat["intent_type"], cat["notes"]]
            for i, cat in enumerate(data["top_categories"])
        ],
    )

    h(2, "5. Duplicate Category Detection")
    dups = data["duplicates"]
    if dups:
        p(f"**{len(dups)} duplicate name patterns detected.** These indicate categories that should have been reused but weren't.\n")
        table(
            ["Stem / Key", "Duplicate Category Names"],
            [[stem, " / ".join(f"`{n}`" for n in names)] for stem, names in list(dups.items())[:20]],
        )
        p()
        p("**Why this happens:** The category naming system generates a string from intent metadata. If the LLM extracts slightly different topics for two similar notes (e.g., 'PostgreSQL' vs 'Postgres'), the canonical name match fails and a new category is created. This is the system's primary fragmentation mechanism.")
    else:
        p("No exact duplicate category names detected.")

    h(2, "6. Suspicious Categories")
    sus = data["suspicious_categories"]
    if sus:
        p(f"**{len(sus)} suspiciously generic categories detected:**\n")
        for name in sus:
            p(f"- `{name}`")
        p()
        p("**Why they exist:** When the intent classifier cannot extract a meaningful topic, the category name falls back to a broad intent-type label (e.g., 'Study', 'General', 'Tasks'). These categories absorb notes that couldn't be more specifically classified.")
    else:
        p("No suspiciously generic categories detected.")

    h(2, "7. Category Cap Analysis")
    if data["category_cap_used"]:
        p(f"⚠️ **The 50-category cap has been reached.** All subsequent notes are assigned to the nearest existing category using `cap_fallback` method, regardless of semantic compatibility.")
        p()
        p("**Impact:** Notes that would have created new specific categories are now lumped into the closest existing one. This **inflates** category reuse metrics while **reducing** categorization precision. The effective reuse rate after cap is not genuine reuse — it is forced assignment.")
        p()
        p("**Recommendation:** If the dataset has grown significantly beyond 50 natural topic clusters, raise `MAX_CATEGORIES_PER_USER` in `IntentCategoryService`. The current limit was set for personal use (50 notes), not for 1000+ notes.")
    else:
        p("Category cap (50) has not been reached. All categories were created genuinely.")

    h(2, "8. Complete Category Listing")
    table(
        ["ID", "Category Name", "Intent Type", "Notes", "Has Actor"],
        [
            [cat["id"], cat["name"], cat["intent_type"], cat["notes"], "Yes" if cat["actor"] else "No"]
            for cat in data["all_categories"]
        ],
    )

    h(2, "9. Recommendations")
    recs = []

    if data["fragmentation_rate"] > 0.40:
        recs.append("**High fragmentation**: Lower `CATEGORY_INGEST_THRESHOLD` from 0.40 to 0.35 to encourage more category reuse. Run backfill after changing.")

    if data["category_cap_used"]:
        recs.append("**Category cap hit**: Raise `MAX_CATEGORIES_PER_USER` to 100 for large datasets. Current cap forces misclassification via `cap_fallback`.")

    if len(dups) > 3:
        recs.append(f"**{len(dups)} duplicate stems**: Review topic synonym mappings in `IntentCategoryService.TOPIC_SYNONYMS`. Common culprit: 'postgres' vs 'postgresql', 'redis cache' vs 'redis'.")

    if data["failed"] > 0:
        fail_rate = data["failed"] / max(1, data["total_notes"])
        recs.append(f"**{data['failed']} failed notes ({fail_rate:.1%})**: Review worker logs for Gemini API failures or DB connection errors. Failed notes may need a backfill run.")

    if data["avg_notes_per_category"] < 5:
        recs.append(f"**Low avg notes/category ({data['avg_notes_per_category']})**: Categories are too granular. Consider raising the semantic reuse threshold.")

    if not recs:
        recs.append("No critical issues detected. Categorization quality is acceptable for this dataset size.")

    for i, rec in enumerate(recs, 1):
        p(f"{i}. {rec}")

    path.write_text("\n".join(lines), encoding="utf-8")
    logger.info("CATEGORY_ANALYSIS.md written: %s", path)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--user-id", type=int, default=1)
    parser.add_argument("--output", type=str, default="evaluation_results")
    return parser.parse_args()


def main():
    args = parse_args()
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)

    db = SessionLocal()
    try:
        data = collect(db, args.user_id)
    finally:
        db.close()

    json_path = out / "category_analysis.json"
    json_path.write_text(json.dumps(data, indent=2, default=str))

    md_path = out / "CATEGORY_ANALYSIS.md"
    write_markdown(data, md_path)

    logger.info("Total categories: %d", data["total_categories"])
    logger.info("Fragmentation rate: %.1f%%", data["fragmentation_rate"] * 100)
    logger.info("Avg notes/category: %.1f", data["avg_notes_per_category"])
    logger.info("Duplicates detected: %d", len(data["duplicates"]))


if __name__ == "__main__":
    main()
