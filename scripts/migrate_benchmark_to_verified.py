"""
Migrate benchmark.json (v1.0.0 binary relevance) to verified.json (graded relevance).

Grade assignment for the 50 existing queries:
  - All relevant_note_ids receive grade 1 (partial relevance).
    Rationale: the original benchmark did not distinguish primary from secondary
    relevance within the relevant set.  Grade 2 requires inspecting actual note
    content, which will be done in the Sprint 3 annotation pass.
  - Entries with a single relevant note are promoted to grade 2 because a sole
    relevant note is, by definition, the complete answer.

This migration is a one-time bootstrap.  The resulting verified.json should be
reviewed and graded notes upgraded from 1 to 2 during the Sprint 3 annotation.

Usage:
    python scripts/migrate_benchmark_to_verified.py
"""

from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

BENCHMARK_PATH = ROOT / "app" / "evaluation" / "benchmark" / "benchmark.json"
VERIFIED_PATH  = ROOT / "app" / "evaluation" / "benchmark" / "verified.json"
TODAY = datetime.utcnow().date().isoformat()


def migrate() -> None:
    source = json.loads(BENCHMARK_PATH.read_text(encoding="utf-8"))

    verified: list[dict] = []
    single_note_count = 0
    multi_note_count = 0

    for entry in source:
        nids = entry.get("relevant_note_ids", [])

        # Grade assignment heuristic
        graded: dict[str, int] = {}
        if len(nids) == 1:
            # Single relevant note = definitive answer = grade 2
            graded[str(nids[0])] = 2
            single_note_count += 1
        else:
            # Multi-note: all grade 1 pending detailed review
            for nid in nids:
                graded[str(nid)] = 1
            multi_note_count += 1

        verified.append({
            **entry,
            "graded_relevance": graded,
            "retrieval_challenge": entry.get("retrieval_challenge"),
            "labeling_notes": (
                "Migrated from benchmark.json v1.0.0 (binary relevance). "
                "Single-note entries promoted to grade 2; multi-note entries "
                "set to grade 1 pending manual review of note content."
            ),
            "labeled_at": TODAY,
        })

    if VERIFIED_PATH.exists():
        existing = json.loads(VERIFIED_PATH.read_text(encoding="utf-8"))
        existing_ids = {e["id"] for e in existing}
        new_entries = [e for e in verified if e["id"] not in existing_ids]
        merged = existing + new_entries
        print(f"verified.json already exists with {len(existing)} entries.")
        print(f"Merging {len(new_entries)} new entries (skipping {len(verified) - len(new_entries)} duplicates).")
        VERIFIED_PATH.write_text(json.dumps(merged, indent=2), encoding="utf-8")
        print(f"verified.json now has {len(merged)} entries.")
    else:
        VERIFIED_PATH.write_text(json.dumps(verified, indent=2), encoding="utf-8")
        print(f"Created verified.json with {len(verified)} entries.")

    print(f"  Single-note entries (grade 2): {single_note_count}")
    print(f"  Multi-note entries (grade 1):  {multi_note_count}")


if __name__ == "__main__":
    migrate()
