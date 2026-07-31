"""
Throughput Study — instrumented annotation session.

Presents 30 representative benchmark candidates for human annotation,
records per-query timing, and writes a results JSON for analysis.

Usage:
    python scripts/throughput_study.py

Results are saved to:
    evaluation_results/throughput_study_results.json

After completion, re-run with --analyze to print summary statistics.
    python scripts/throughput_study.py --analyze
"""

from __future__ import annotations

import argparse
import json
import statistics
import sys
import time
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

CANDIDATES_PATH = ROOT / "app/evaluation/benchmark/throughput_study_candidates.json"
RESULTS_PATH = ROOT / "evaluation_results/throughput_study_results.json"


# ---------------------------------------------------------------------------
# Note title lookup (same logic as human_eval.py)
# ---------------------------------------------------------------------------

def _get_note_preview(note_id: int) -> str:
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


# ---------------------------------------------------------------------------
# Single-entry annotation (mirrors human_eval.py logic)
# ---------------------------------------------------------------------------

def annotate_entry(entry: dict, index: int, total: int) -> tuple[str, dict | None, float]:
    """
    Annotate one entry interactively.

    Returns:
        (action, modified_entry_or_none, elapsed_seconds)
        action ∈ {"approved", "skipped", "quit"}
    """
    t0 = time.time()

    note_ids = entry.get("relevant_note_ids", [])
    n_notes = len(note_ids)
    difficulty = entry.get("difficulty", "?")
    challenge = entry.get("retrieval_challenge") or "untagged"

    print(f"\n{'='*70}")
    print(f"[{index}/{total}]  difficulty={difficulty}  challenge={challenge}  notes={n_notes}")
    print(f"QUERY: {entry['query']}")
    print()

    graded: dict[str, int] = {}

    # Negative query path
    if challenge == "negative":
        print("  NEGATIVE query — no relevant notes expected.")
        answer = input("  Confirm negative? [y / s=skip / q=quit]: ").strip().lower()
        elapsed = time.time() - t0
        if answer in ("y", "yes"):
            modified = dict(entry)
            modified["graded_relevance"] = {}
            modified["labeled_at"] = datetime.utcnow().date().isoformat()
            return ("approved", modified, elapsed)
        elif answer == "q":
            return ("quit", None, elapsed)
        else:
            return ("skipped", None, elapsed)

    # Normal annotation
    if not note_ids:
        print("  No relevant notes listed — will be treated as negative if approved.")

    for nid in note_ids:
        preview = _get_note_preview(nid)
        print(f"\n  Note {nid}: {preview[:120]}")
        while True:
            answer = input("  [2=high / 1=partial / 0=not / s=skip / q=quit]: ").strip().lower()
            if answer in ("0", "1", "2"):
                graded[str(nid)] = int(answer)
                break
            elif answer in ("s", "skip"):
                elapsed = time.time() - t0
                return ("skipped", None, elapsed)
            elif answer == "q":
                elapsed = time.time() - t0
                return ("quit", None, elapsed)
            else:
                print("  Please enter 0, 1, 2, s, or q.")

    labeling_note = input("\n  Note (optional): ").strip()

    elapsed = time.time() - t0

    new_relevant = [int(k) for k, v in graded.items() if v > 0]
    modified = dict(entry)
    modified["relevant_note_ids"] = new_relevant
    modified["graded_relevance"] = graded
    modified["labeled_at"] = datetime.utcnow().date().isoformat()
    modified["labeling_notes"] = labeling_note
    return ("approved", modified, elapsed)


# ---------------------------------------------------------------------------
# Main annotation loop
# ---------------------------------------------------------------------------

def run_study() -> None:
    candidates_raw = json.loads(CANDIDATES_PATH.read_text(encoding="utf-8"))

    # Load existing results (resume support)
    RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    existing: list[dict] = []
    if RESULTS_PATH.exists():
        try:
            existing = json.loads(RESULTS_PATH.read_text(encoding="utf-8"))
        except Exception:
            existing = []

    reviewed_ids = {r["id"] for r in existing}
    pending = [c for c in candidates_raw if c["id"] not in reviewed_ids]

    print("\nThroughput Study — Instrumented Annotation Session")
    print(f"Candidates : {len(candidates_raw)}")
    print(f"Already done: {len(existing)}")
    print(f"Remaining  : {len(pending)}")
    print()
    print("Keys: 2=highly relevant  1=partial  0=not relevant  s=skip  q=quit")
    input("Press Enter to begin...")

    session_start = time.time()
    results = list(existing)
    approved = 0
    skipped = 0

    for i, entry in enumerate(pending, start=len(existing) + 1):
        action, modified, elapsed = annotate_entry(entry, i, len(candidates_raw))

        record = {
            "id": entry["id"],
            "query": entry["query"],
            "difficulty": entry.get("difficulty"),
            "retrieval_challenge": entry.get("retrieval_challenge"),
            "n_candidate_notes": len(entry.get("relevant_note_ids", [])),
            "elapsed_seconds": round(elapsed, 2),
            "action": action,
        }
        if modified:
            gr = modified.get("graded_relevance") or {}
            record["n_relevant_approved"] = sum(1 for v in gr.values() if v > 0)

        results.append(record)
        RESULTS_PATH.write_text(json.dumps(results, indent=2), encoding="utf-8")

        if action == "approved":
            approved += 1
            print(f"  [{elapsed:.0f}s] approved")
        elif action == "skipped":
            skipped += 1
            print(f"  [{elapsed:.0f}s] skipped")
        elif action == "quit":
            print(f"\nQuitting. Progress saved to {RESULTS_PATH}")
            break

    session_elapsed = time.time() - session_start
    print(f"\n{'='*70}")
    print(f"Session complete: {approved} approved, {skipped} skipped in {session_elapsed/60:.1f} min")
    print(f"Results saved to {RESULTS_PATH}")
    print(f"\nRun with --analyze to see throughput statistics.")


# ---------------------------------------------------------------------------
# Analysis
# ---------------------------------------------------------------------------

def run_analysis() -> None:
    if not RESULTS_PATH.exists():
        print(f"No results file found at {RESULTS_PATH}. Run the study first.")
        sys.exit(1)

    results = json.loads(RESULTS_PATH.read_text(encoding="utf-8"))
    approved = [r for r in results if r["action"] == "approved"]
    skipped = [r for r in results if r["action"] == "skipped"]

    print(f"\n{'='*70}")
    print("THROUGHPUT STUDY — RESULTS")
    print(f"{'='*70}")
    print(f"Total annotated : {len(results)}")
    print(f"Approved        : {len(approved)}")
    print(f"Skipped         : {len(skipped)}")

    if not approved:
        print("No approved entries to analyze.")
        return

    times = [r["elapsed_seconds"] for r in approved]
    print(f"\n--- Timing (approved entries only) ---")
    print(f"Mean    : {statistics.mean(times):.1f}s")
    print(f"Median  : {statistics.median(times):.1f}s")
    p90_idx = int(len(times) * 0.9)
    p90 = sorted(times)[min(p90_idx, len(times) - 1)]
    print(f"P90     : {p90:.1f}s")
    print(f"Min/Max : {min(times):.1f}s / {max(times):.1f}s")

    mean_s = statistics.mean(times)
    throughput_per_hour = 3600 / mean_s
    print(f"\nThroughput: {throughput_per_hour:.1f} queries/hour  ({mean_s:.1f}s/query mean)")

    # By difficulty
    print(f"\n--- By Difficulty ---")
    for diff in ("easy", "medium", "hard"):
        subset = [r for r in approved if r.get("difficulty") == diff]
        if subset:
            t = [r["elapsed_seconds"] for r in subset]
            print(f"  {diff:6s}: n={len(subset):2d}  mean={statistics.mean(t):.1f}s  median={statistics.median(t):.1f}s")

    # By challenge
    print(f"\n--- By Retrieval Challenge ---")
    challenges = sorted({r.get("retrieval_challenge") or "untagged" for r in approved})
    for ch in challenges:
        subset = [r for r in approved if (r.get("retrieval_challenge") or "untagged") == ch]
        if subset:
            t = [r["elapsed_seconds"] for r in subset]
            print(f"  {ch:14s}: n={len(subset):2d}  mean={statistics.mean(t):.1f}s")

    # Note count distribution
    note_counts = [r.get("n_relevant_approved", 0) for r in approved]
    if note_counts:
        print(f"\n--- Relevant notes per approved query ---")
        print(f"  Mean   : {statistics.mean(note_counts):.2f}")
        print(f"  Median : {statistics.median(note_counts):.1f}")
        dist = {}
        for n in note_counts:
            dist[n] = dist.get(n, 0) + 1
        print(f"  Distribution: {dict(sorted(dist.items()))}")

    # Effort projections
    print(f"\n--- Effort Projections (at {mean_s:.1f}s/query mean) ---")
    # Account for overhead: breaks, setup, skips. Use 80% efficiency.
    efficiency = 0.80
    effective_rate = throughput_per_hour * efficiency
    print(f"  Assuming 80% efficiency ({effective_rate:.0f} net queries/hour):")
    for target in (100, 200, 300):
        # Subtract already-verified count
        already = 98  # verified.json current count
        needed = max(0, target - already)
        hours = needed / effective_rate
        print(f"  → {target:3d} verified queries: need {needed} more = {hours:.1f}h ({hours*60:.0f} min)")

    print(f"\n{'='*70}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    p = argparse.ArgumentParser(description="Throughput study for benchmark annotation.")
    p.add_argument("--analyze", action="store_true", help="Print analysis of existing results.")
    args = p.parse_args()

    if args.analyze:
        run_analysis()
    else:
        run_study()


if __name__ == "__main__":
    main()
