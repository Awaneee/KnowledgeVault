"""
Human evaluation CLI — interactive relevance review tool.

Reads benchmark/candidates.json (auto-generated) and presents each entry
for human review.  Accepted entries are written to benchmark/verified.json.

The reviewer assigns one of:
  2 = highly relevant (note directly and completely answers the query)
  1 = partially relevant (note contains related information)
  0 = not relevant (skip this note from the relevant set)
  s = skip this entry entirely (goes to benchmark/uncertain.json)
  q = quit and save progress

Progress is checkpointed: already-reviewed entries are not re-shown on resume.

Usage:
    python scripts/human_eval.py \\
        --input app/evaluation/benchmark/candidates.json \\
        --verified app/evaluation/benchmark/verified.json \\
        --uncertain app/evaluation/benchmark/uncertain.json \\
        [--auto-approve]   # non-interactive: auto-approve all candidates (for CI testing)
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
1

def _load_json(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))


def _save_json(path: Path, data: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def _get_note_title(note_id: int) -> str:
    """Best-effort: fetch note title from DB for display."""
    try:
        import app.database.base_all  # noqa: F401
        from app.database.session import SessionLocal
        from app.models.notes import Note
        db = SessionLocal()
        try:
            row = db.query(Note.id, Note.title, Note.content).filter(Note.id == note_id).first()
            if row:
                preview = (row.content or "")[:200].strip()
                return f"{row.title or 'Untitled'} — {preview}"
            return f"note_id={note_id} (not found)"
        finally:
            db.close()
    except Exception:
        return f"note_id={note_id}"


def review_entry(entry: dict, auto_approve: bool) -> tuple[str, dict | None]:
    """
    Present a single candidate entry for review.

    Returns:
      ("approved", modified_entry) — entry accepted with graded relevance
      ("skipped", None)            — reviewer chose to skip
      ("quit", None)               — reviewer wants to stop
    """
    print(f"\n{'='*70}")
    print(f"ID      : {entry['id']}")
    print(f"QUERY   : {entry['query']}")
    print(f"Intent  : {entry.get('expected_intent', '?')} / {entry.get('expected_category', '?')}")
    print(f"Diff    : {entry.get('difficulty', '?')}  Challenge: {entry.get('retrieval_challenge') or 'untagged'}")
    print(f"Tags    : {', '.join(entry.get('tags', []))}")
    print()

    note_ids = entry.get("relevant_note_ids", [])
    if not note_ids and entry.get("retrieval_challenge") != "negative":
        print("  ⚠  No relevant notes — will be treated as negative query if approved.")

    graded: dict[str, int] = {}

    if auto_approve:
        # Non-interactive mode.
        # Grade assignment heuristic:
        #   - Single-note entries: grade 2 (it IS the answer)
        #   - Multi-note entries: try to parse the primary note from the stable ID
        #     format "{primary_note_id}_{query_type}_{hash}"; primary gets grade 2,
        #     secondary notes get grade 1.
        #   - Fallback (unrecognisable ID): all notes get grade 1.
        primary_id: int | None = None
        try:
            primary_id = int(entry.get("id", "").split("_")[0])
        except (ValueError, IndexError, AttributeError):
            pass

        for nid in note_ids:
            if len(note_ids) == 1 or nid == primary_id:
                graded[str(nid)] = 2
            else:
                graded[str(nid)] = 1

        modified = dict(entry)
        modified["graded_relevance"] = graded
        modified["labeled_at"] = datetime.utcnow().date().isoformat()
        modified["labeling_notes"] = (
            "auto-approved: grade 2 = primary/sole relevant note, "
            "grade 1 = secondary relevant note. Pending human verification."
        )
        return ("approved", modified)

    if entry.get("retrieval_challenge") == "negative":
        print("  ⚠  This is a NEGATIVE query — no relevant notes should be found.")
        answer = input("  Confirm negative? [y/approve / s=skip / q=quit]: ").strip().lower()
        if answer in ("y", "approve", "yes"):
            modified = dict(entry)
            modified["graded_relevance"] = {}
            modified["labeled_at"] = datetime.utcnow().date().isoformat()
            return ("approved", modified)
        elif answer == "q":
            return ("quit", None)
        else:
            return ("skipped", None)

    for nid in note_ids:
        title_preview = _get_note_title(nid)
        print(f"\n  Note {nid}: {title_preview[:120]}")
        while True:
            answer = input(
                "  Relevance? [2=high / 1=partial / 0=not / s=skip entry / q=quit]: "
            ).strip().lower()
            if answer in ("0", "1", "2"):
                graded[str(nid)] = int(answer)
                break
            elif answer in ("s", "skip"):
                return ("skipped", None)
            elif answer == "q":
                return ("quit", None)
            else:
                print("  Please enter 0, 1, 2, s, or q.")

    # Remove grade-0 notes from relevant_note_ids but keep them in graded_relevance
    new_relevant = [int(k) for k, v in graded.items() if v > 0]

    labeling_note = input(
        "\n  Labeling note (optional — why are these grades correct?): "
    ).strip()

    modified = dict(entry)
    modified["relevant_note_ids"] = new_relevant
    modified["graded_relevance"] = graded
    modified["labeled_at"] = datetime.utcnow().date().isoformat()
    modified["labeling_notes"] = labeling_note

    print(f"\n  → Approved: {len(new_relevant)} relevant note(s)")
    return ("approved", modified)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Interactive relevance review CLI.")
    p.add_argument("--input", type=Path,
                   default=Path("app/evaluation/benchmark/candidates.json"),
                   help="Candidates JSON to review.")
    p.add_argument("--verified", type=Path,
                   default=Path("app/evaluation/benchmark/verified.json"),
                   help="Output path for approved entries.")
    p.add_argument("--uncertain", type=Path,
                   default=Path("app/evaluation/benchmark/uncertain.json"),
                   help="Output path for skipped (uncertain) entries.")
    p.add_argument("--auto-approve", action="store_true",
                   help="Non-interactive mode: approve all entries at grade 1.")
    return p.parse_args()


def main() -> None:
    args = parse_args()

    candidates = _load_json(args.input)
    if not candidates:
        print(f"No candidates found at {args.input}.")
        print("Run generate_benchmarks.py first.")
        sys.exit(1)

    verified: list[dict] = _load_json(args.verified)
    uncertain: list[dict] = _load_json(args.uncertain)

    already_reviewed_ids: set[str] = {
        e["id"] for e in (*verified, *uncertain)
    }
    pending = [c for c in candidates if c["id"] not in already_reviewed_ids]

    print(f"\nHuman Evaluation CLI")
    print(f"Input     : {args.input}")
    print(f"Verified  : {args.verified} ({len(verified)} entries)")
    print(f"Uncertain : {args.uncertain} ({len(uncertain)} entries)")
    print(f"Pending   : {len(pending)} / {len(candidates)} candidates")

    if not pending:
        print("\nAll candidates have been reviewed.")
        sys.exit(0)

    if not args.auto_approve:
        print("\nKeys: 2=highly relevant  1=partial  0=not relevant  s=skip  q=quit")
        input("Press Enter to begin…")

    approved_count = 0
    skipped_count = 0

    for i, entry in enumerate(pending):
        print(f"\n[{i+1}/{len(pending)}]")
        t0 = time.time()
        action, modified = review_entry(entry, auto_approve=args.auto_approve)

        if action == "approved":
            verified.append(modified)
            approved_count += 1
            # Checkpoint: save after every approved entry
            _save_json(args.verified, verified)

        elif action == "skipped":
            uncertain.append(entry)
            skipped_count += 1
            _save_json(args.uncertain, uncertain)

        elif action == "quit":
            print(f"\nSaved progress. {approved_count} approved, {skipped_count} skipped.")
            break

        elapsed = time.time() - t0
        if not args.auto_approve:
            print(f"  [{elapsed:.0f}s]")

    print(f"\n{'='*70}")
    print(f"Session complete.")
    print(f"  Approved : {approved_count}")
    print(f"  Skipped  : {skipped_count}")
    print(f"  Verified : {len(verified)} total in {args.verified}")
    print()


if __name__ == "__main__":
    main()
