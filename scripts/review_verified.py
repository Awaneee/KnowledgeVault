"""
Benchmark v2.0.0 quality-review tool.

Loads entries from human_review_checklist.json filtered by --tier,
cross-references verified.json, fetches note content from PostgreSQL,
and lets you interactively accept/edit each entry.

Commands per note-id:
    a        accept as-is
    r <id>   remove a note id from the relevant set
    d <id>   downgrade grade for a note id  (2→1, 1→0 removes)
    u <id>   upgrade grade for a note id    (1→2)
    n <id>   add a new note id (prompted for grade)
    s        skip this entry (do not mark reviewed)
    q        save and quit

Progress is tracked via a "reviewed_by_v2" field written into verified.json
after each accepted entry, so the session can be resumed at any time.

Usage:
    python scripts/review_verified.py [--tier HIGH|MEDIUM|LOW]
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

VERIFIED_PATH = ROOT / "app/evaluation/benchmark/verified.json"
CHECKLIST_PATH = ROOT / "evaluation_results/human_review_checklist.json"

GRADE_LABEL = {2: "HIGH", 1: "partial", 0: "not-relevant"}

# ──────────────────────────── DB helpers ─────────────────────────────────────

def _fetch_notes(note_ids: list[int]) -> dict[int, dict]:
    """Return {note_id: {title, category, content}} for each id."""
    try:
        import app.database.base_all  # noqa: F401
        from app.database.session import SessionLocal
        from app.models.notes import Note

        db = SessionLocal()
        try:
            rows = (
                db.query(Note)
                .filter(Note.id.in_(note_ids))
                .all()
            )
            result: dict[int, dict] = {}
            for row in rows:
                cat_name = ""
                try:
                    cat_name = row.category.name if row.category else ""
                except Exception:
                    pass
                result[row.id] = {
                    "title": row.title or "Untitled",
                    "category": cat_name,
                    "content": (row.content or "")[:400],
                }
            return result
        finally:
            db.close()
    except Exception as exc:
        print(f"  [DB error: {exc}]")
        return {}


# ──────────────────────────── I/O helpers ────────────────────────────────────

def _load_json(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))


def _save_json(path: Path, data: list[dict]) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def _sep(char: str = "─", width: int = 72) -> None:
    print(char * width)


# ──────────────────────────── display ────────────────────────────────────────

def _display_entry(
    entry: dict,
    note_data: dict[int, dict],
    checklist_item: dict,
) -> None:
    _sep("═")
    print(f"  ID        : {entry['id']}")
    print(f"  Query     : {entry['query']}")
    print(f"  Difficulty: {entry.get('difficulty', '?')}  "
          f"Challenge: {entry.get('retrieval_challenge') or 'untagged'}")
    print(f"  Priority  : {checklist_item['priority']}  "
          f"Reason: {'; '.join(checklist_item.get('reasons', []))}")
    _sep()

    graded: dict[str, int] = entry.get("graded_relevance", {})
    note_ids: list[int] = entry.get("relevant_note_ids", [])

    if not note_ids:
        print("  (no relevant notes)")
        return

    print(f"  {'ID':>6}  {'Grd':>3}  {'Title / Category / Preview'}")
    _sep()
    for nid in note_ids:
        grade = graded.get(str(nid), "?")
        nd = note_data.get(nid)
        if nd:
            preview = nd["content"].replace("\n", " ").strip()
            print(f"  {nid:>6}  [{grade}]  {nd['title']}  [{nd['category']}]")
            print(f"         {preview[:380]}")
        else:
            print(f"  {nid:>6}  [{grade}]  (not found in DB)")
        print()


# ──────────────────────────── command parsing ─────────────────────────────────

def _parse_cmd(raw: str) -> tuple[str, int | None]:
    """Return (command, optional_note_id)."""
    parts = raw.strip().lower().split()
    if not parts:
        return ("", None)
    cmd = parts[0]
    nid: int | None = None
    if len(parts) >= 2:
        try:
            nid = int(parts[1])
        except ValueError:
            pass
    return cmd, nid


# ──────────────────────────── review loop ────────────────────────────────────

def review_entry(
    entry: dict,
    note_data: dict[int, dict],
    checklist_item: dict,
    index: int,
    total: int,
) -> tuple[str, dict | None]:
    """
    Returns:
        ("accepted", modified_entry)
        ("skipped",  None)
        ("quit",     None)
    """
    print(f"\n[{index}/{total}]")
    _display_entry(entry, note_data, checklist_item)

    working = dict(entry)
    working["graded_relevance"] = dict(entry.get("graded_relevance", {}))
    working["relevant_note_ids"] = list(entry.get("relevant_note_ids", []))

    print("  Commands: a=accept  r <id>=remove  d <id>=downgrade  u <id>=upgrade")
    print("            n <id>=add note  s=skip  q=save&quit")

    while True:
        raw = input("\n  > ").strip()
        cmd, nid = _parse_cmd(raw)

        if cmd == "a":
            working["reviewed_by_v2"] = datetime.now(timezone.utc).date().isoformat()
            return ("accepted", working)

        elif cmd == "s":
            return ("skipped", None)

        elif cmd == "q":
            return ("quit", None)

        elif cmd == "r":
            if nid is None:
                print("  Usage: r <note_id>")
                continue
            sid = str(nid)
            if nid in working["relevant_note_ids"]:
                working["relevant_note_ids"].remove(nid)
                working["graded_relevance"].pop(sid, None)
                print(f"  Removed note {nid}.")
            else:
                print(f"  Note {nid} not in relevant set.")

        elif cmd == "d":
            if nid is None:
                print("  Usage: d <note_id>")
                continue
            sid = str(nid)
            cur = working["graded_relevance"].get(sid)
            if cur is None:
                print(f"  Note {nid} not in graded_relevance.")
            elif cur == 2:
                working["graded_relevance"][sid] = 1
                print(f"  Downgraded {nid}: 2 → 1")
            elif cur == 1:
                working["graded_relevance"][sid] = 0
                working["relevant_note_ids"] = [
                    n for n in working["relevant_note_ids"] if n != nid
                ]
                print(f"  Downgraded {nid}: 1 → 0 (removed from relevant set)")
            else:
                print(f"  Note {nid} is already grade 0.")

        elif cmd == "u":
            if nid is None:
                print("  Usage: u <note_id>")
                continue
            sid = str(nid)
            cur = working["graded_relevance"].get(sid, 0)
            if cur == 2:
                print(f"  Note {nid} is already grade 2.")
            elif cur == 1:
                working["graded_relevance"][sid] = 2
                print(f"  Upgraded {nid}: 1 → 2")
            else:
                working["graded_relevance"][sid] = 1
                if nid not in working["relevant_note_ids"]:
                    working["relevant_note_ids"].append(nid)
                print(f"  Upgraded {nid}: 0 → 1 (added to relevant set)")

        elif cmd == "n":
            if nid is None:
                print("  Usage: n <note_id>")
                continue
            # Fetch the note from DB on demand
            extra = _fetch_notes([nid])
            nd = extra.get(nid)
            if nd:
                print(f"  {nd['title']}  [{nd['category']}]")
                print(f"  {nd['content'][:380]}")
            else:
                print(f"  Note {nid} not found in DB — add anyway?")
            grade_raw = input("  Grade for this note [2/1/0/cancel]: ").strip()
            if grade_raw in ("2", "1", "0"):
                g = int(grade_raw)
                working["graded_relevance"][str(nid)] = g
                if g > 0 and nid not in working["relevant_note_ids"]:
                    working["relevant_note_ids"].append(nid)
                print(f"  Added note {nid} at grade {g}.")
            else:
                print("  Cancelled.")

        elif cmd == "":
            pass  # blank line, re-show prompt

        else:
            print(f"  Unknown command '{cmd}'. Try: a r d u n s q")


# ──────────────────────────── main ───────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(description="Benchmark v2 quality review")
    parser.add_argument(
        "--tier",
        choices=["HIGH", "MEDIUM", "LOW"],
        default="HIGH",
        help="Which priority tier to review (default: HIGH)",
    )
    args = parser.parse_args()

    checklist: list[dict] = _load_json(CHECKLIST_PATH)
    verified: list[dict] = _load_json(VERIFIED_PATH)

    # Build fast lookup: id → index in verified list
    id_to_idx: dict[str, int] = {e["id"]: i for i, e in enumerate(verified)}

    # Filter checklist to the requested tier
    tier_items = [c for c in checklist if c["priority"] == args.tier]

    # Skip already-reviewed entries (resume support)
    todo = [
        c for c in tier_items
        if not verified[id_to_idx[c["id"]]].get("reviewed_by_v2")
        if c["id"] in id_to_idx
    ]
    done_count = len(tier_items) - len(todo)

    print(f"\nBenchmark v2 Quality Review — tier={args.tier}")
    print(f"Total {args.tier}: {len(tier_items)}  Already reviewed: {done_count}  Remaining: {len(todo)}")

    if not todo:
        print("Nothing left to review in this tier.")
        return

    for progress_i, checklist_item in enumerate(todo, start=done_count + 1):
        entry_id = checklist_item["id"]
        entry = verified[id_to_idx[entry_id]]

        note_ids = entry.get("relevant_note_ids", [])
        note_data = _fetch_notes(note_ids) if note_ids else {}

        outcome, modified = review_entry(
            entry,
            note_data,
            checklist_item,
            index=progress_i,
            total=len(tier_items),
        )

        if outcome == "accepted":
            verified[id_to_idx[entry_id]] = modified
            _save_json(VERIFIED_PATH, verified)
            print(f"  Saved. ({progress_i}/{len(tier_items)} done)")

        elif outcome == "skipped":
            print("  Skipped.")

        elif outcome == "quit":
            print(f"\nSaved and quit. Progress: {progress_i - 1}/{len(tier_items)} reviewed.")
            break

    else:
        print(f"\nAll {args.tier} entries reviewed.")


if __name__ == "__main__":
    main()
