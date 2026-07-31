"""
Benchmark v2.0.0 — interactive relevance review.

Works through human_review_checklist.json (HIGH → MEDIUM → LOW), fetches
the referenced notes from PostgreSQL, and lets you approve or edit each
entry's relevant_note_ids and grades before moving on.

Edits are written to verified.json immediately after each approval.
Progress is checkpointed to evaluation_results/review_progress.json.

Usage:
    python scripts/review_benchmark.py                    # all tiers
    python scripts/review_benchmark.py --priority HIGH    # one tier only
    python scripts/review_benchmark.py --entry <id>       # jump to entry

Commands during review:
    a              approve as-is and advance
    r <id>         remove note from relevant set
    + <id>         fetch note from DB and add to relevant set (prompts grade)
    g <id> <0-2>   change a note's grade (0=not relevant, 1=partial, 2=primary)
    ? <id>         show full note content
    s              skip (revisit later)
    q              quit and save progress
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import textwrap
from pathlib import Path

# Force UTF-8 output on Windows consoles
os.environ.setdefault("PYTHONIOENCODING", "utf-8")
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

CHECKLIST_PATH  = ROOT / "evaluation_results" / "human_review_checklist.json"
VERIFIED_PATH   = ROOT / "app" / "evaluation" / "benchmark" / "verified.json"
PROGRESS_PATH   = ROOT / "evaluation_results" / "review_progress.json"

PRIORITY_ORDER = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
W = 72  # display width


# ---------------------------------------------------------------------------
# DB helpers
# ---------------------------------------------------------------------------

def _open_db():
    import app.database.base_all  # noqa: F401
    from app.database.session import SessionLocal
    return SessionLocal()


def fetch_notes(db, note_ids: list[int]) -> dict[int, dict]:
    """Return {note_id: {title, content}} for all requested IDs."""
    from app.models.notes import Note
    rows = (
        db.query(Note.id, Note.title, Note.content)
        .filter(Note.id.in_(note_ids))
        .all()
    )
    return {
        r.id: {"title": r.title or "(no title)", "content": r.content or ""}
        for r in rows
    }


# ---------------------------------------------------------------------------
# File I/O
# ---------------------------------------------------------------------------

def load_json(path: Path) -> list | dict:
    if not path.exists():
        return [] if path.suffix == ".json" else {}
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def load_verified() -> dict[str, dict]:
    entries = load_json(VERIFIED_PATH)
    return {str(e["id"]): e for e in entries}


def save_verified(by_id: dict[str, dict]) -> None:
    save_json(VERIFIED_PATH, list(by_id.values()))


def load_progress() -> set[str]:
    data = load_json(PROGRESS_PATH)
    if isinstance(data, dict):
        return set(data.get("reviewed_ids", []))
    return set()


def save_progress(reviewed: set[str]) -> None:
    save_json(PROGRESS_PATH, {"reviewed_ids": sorted(reviewed)})


# ---------------------------------------------------------------------------
# Display helpers
# ---------------------------------------------------------------------------

def hr(char="─"):
    print(char * W)


def banner(text: str, char="═"):
    print(char * W)
    print(text)
    print(char * W)


def _grade_badge(grade: int) -> str:
    return {2: " ★ ", 1: "   ", 0: " ✗ "}.get(grade, "   ")


def display_entry(
    item: dict,
    v_entry: dict,
    notes: dict[int, dict],
    index: int,
    total: int,
) -> None:
    """Render the full review panel for one checklist entry."""
    challenge = item["retrieval_challenge"]
    priority  = item["priority"]
    difficulty = item["difficulty"]
    gr: dict[str, int] = v_entry.get("graded_relevance") or {}
    relevant_ids: list[int] = v_entry.get("relevant_note_ids") or []

    print()
    banner(
        f"[{priority} {index}/{total}]  {challenge.upper()}  |  {difficulty}"
        f"  |  {len(relevant_ids)} note(s)"
    )
    print(f"QUERY : {item['query']}")
    print()

    # Concern line (strip the leading tag for readability)
    for reason in item["reasons"]:
        concern = reason.split(":", 1)[1].strip() if ":" in reason else reason
        print("CONCERN:", textwrap.fill(concern, W - 9, subsequent_indent=" " * 9))
    print()

    hr()

    if not relevant_ids:
        print("  (no relevant notes — marked as negative / empty)")
    else:
        for nid in relevant_ids:
            grade = gr.get(str(nid), 1)
            badge = _grade_badge(grade)
            note  = notes.get(nid)
            if note is None:
                print(f"  {badge}Note {nid:>5}  [NOT FOUND IN DB]")
                continue

            title   = note["title"].strip()
            content = note["content"].strip()

            # If content is essentially the title, show only title
            body = content if content.lower() != title.lower() else ""
            if body and len(body) > 220:
                body = body[:220].rstrip() + "…"

            grade_label = {2: "grade-2", 1: "grade-1", 0: "grade-0"}.get(grade, f"grade-{grade}")
            print(f"  {badge}Note {nid:>5}  [{grade_label}]  {title}")
            if body:
                for line in body.splitlines():
                    line = line.strip()
                    if line:
                        print(f"           {textwrap.fill(line, W - 12, subsequent_indent=' ' * 11)}")

    hr()


def display_commands(priority: str) -> None:
    if priority == "LOW":
        print("  a          approve as-is (all grade-1 is valid)")
        print("  g <id> 2   promote note to grade-2 (primary answer)")
        print("  s          skip  |  q  quit")
    else:
        print("  a            approve as-is")
        print("  r <id>       remove note from relevant set")
        print("  + <id>       add note by ID (fetches from DB)")
        print("  g <id> <0-2> change grade")
        print("  ? <id>       show full note content")
        print("  s            skip  |  q  quit")
    print()


# ---------------------------------------------------------------------------
# Command handling
# ---------------------------------------------------------------------------

def handle_command(
    raw: str,
    v_entry: dict,
    notes: dict[int, dict],
    db,
) -> str | None:
    """
    Process one command string.

    Returns:
        "approved" — entry accepted, advance
        "skipped"  — skip without saving
        "quit"     — save and exit
        None       — command handled, stay on this entry
    """
    raw = raw.strip()
    if not raw or raw.lower() == "a":
        return "approved"

    if raw.lower() == "s":
        return "skipped"

    if raw.lower() == "q":
        return "quit"

    parts = raw.split()
    cmd   = parts[0].lower()

    gr: dict[str, int] = v_entry.setdefault("graded_relevance", {})
    rel: list[int]     = v_entry.setdefault("relevant_note_ids", [])

    # r <id> — remove
    if cmd == "r" and len(parts) == 2:
        try:
            nid = int(parts[1])
        except ValueError:
            print("  Usage: r <note_id>")
            return None
        if nid in rel:
            rel.remove(nid)
            gr.pop(str(nid), None)
            print(f"  Removed note {nid}.")
        else:
            print(f"  Note {nid} is not in the relevant set.")
        return None

    # + <id> — add
    if cmd in ("+", "add") and len(parts) == 2:
        try:
            nid = int(parts[1])
        except ValueError:
            print("  Usage: + <note_id>")
            return None
        # Fetch from DB
        fetched = fetch_notes(db, [nid])
        if nid not in fetched:
            print(f"  Note {nid} not found in DB.")
            return None
        note = fetched[nid]
        print(f"\n  Note {nid}: {note['title']}")
        body = note["content"].strip()
        if body and body.lower() != note["title"].lower().strip():
            print("  " + body[:400])
        while True:
            g = input("  Grade for this note [2=primary / 1=partial / 0=skip]: ").strip()
            if g in ("0", "1", "2"):
                grade = int(g)
                break
            elif g == "":
                grade = 1
                break
            print("  Enter 0, 1, or 2.")
        if grade > 0:
            if nid not in rel:
                rel.append(nid)
            gr[str(nid)] = grade
            notes[nid] = fetched[nid]  # update local cache
            print(f"  Added note {nid} with grade-{grade}.")
        return None

    # g <id> <grade> — change grade
    if cmd == "g" and len(parts) == 3:
        try:
            nid   = int(parts[1])
            grade = int(parts[2])
        except ValueError:
            print("  Usage: g <note_id> <0|1|2>")
            return None
        if grade not in (0, 1, 2):
            print("  Grade must be 0, 1, or 2.")
            return None
        if grade == 0:
            if nid in rel:
                rel.remove(nid)
            gr.pop(str(nid), None)
            print(f"  Note {nid} removed (grade-0).")
        else:
            if nid not in rel:
                rel.append(nid)
            gr[str(nid)] = grade
            print(f"  Note {nid} → grade-{grade}.")
        return None

    # ? <id> — expand
    if cmd == "?" and len(parts) == 2:
        try:
            nid = int(parts[1])
        except ValueError:
            print("  Usage: ? <note_id>")
            return None
        note = notes.get(nid)
        if note is None:
            fetched = fetch_notes(db, [nid])
            note = fetched.get(nid)
            if note:
                notes[nid] = note
        if note is None:
            print(f"  Note {nid} not found.")
            return None
        print(f"\n  {'─'*66}")
        print(f"  Note {nid}: {note['title']}")
        print(f"  {'─'*66}")
        body = note["content"].strip()
        if body:
            for line in body.splitlines():
                print("  " + line)
        else:
            print("  (empty content)")
        print(f"  {'─'*66}\n")
        return None

    print(f"  Unknown command: {raw!r}. Type 'a' to approve or 'q' to quit.")
    return None


# ---------------------------------------------------------------------------
# Main review loop
# ---------------------------------------------------------------------------

def review_entries(
    items: list[dict],
    verified_by_id: dict[str, dict],
    reviewed: set[str],
    db,
) -> tuple[int, int]:
    """
    Interactive review of checklist items.

    Returns (approved_count, skipped_count).
    """
    pending = [it for it in items if it["id"] not in reviewed]
    approved_count = 0
    skipped_count  = 0

    # Group by priority for the counter display
    priority_totals = {}
    for it in items:
        p = it["priority"]
        priority_totals[p] = priority_totals.get(p, 0) + 1
    priority_done = {p: sum(1 for it in items if it["priority"] == p and it["id"] in reviewed)
                     for p in priority_totals}

    if not pending:
        print("All checklist entries already reviewed.")
        return 0, 0

    print(f"\n{len(pending)} entries remaining (of {len(items)} total).")
    print("Keys: a=approve  r=remove  +=add  g=grade  ?=expand  s=skip  q=quit")
    input("Press Enter to begin…")

    for item in pending:
        v_entry = verified_by_id.get(str(item["id"]))
        if v_entry is None:
            print(f"\n[WARN] Entry {item['id']!r} not found in verified.json — skipping.")
            continue

        priority = item["priority"]
        p_done   = priority_done.get(priority, 0)
        p_total  = priority_totals.get(priority, 0)
        index    = p_done + 1

        # Pre-fetch all note IDs
        note_ids = list(v_entry.get("relevant_note_ids") or [])
        notes    = fetch_notes(db, note_ids) if note_ids else {}

        while True:
            display_entry(item, v_entry, notes, index, p_total)
            display_commands(priority)

            raw = input("> ").strip()
            result = handle_command(raw, v_entry, notes, db)

            if result is None:
                # Command handled, re-render
                continue

            if result == "approved":
                # Sync relevant_note_ids from graded_relevance (remove grade-0)
                gr = v_entry.get("graded_relevance") or {}
                v_entry["relevant_note_ids"] = [int(k) for k, v in gr.items() if v > 0]
                v_entry["labeling_notes"] = (
                    (v_entry.get("labeling_notes") or "") + " [v2-reviewed]"
                ).strip()

                save_verified(verified_by_id)
                reviewed.add(item["id"])
                save_progress(reviewed)
                priority_done[priority] = priority_done.get(priority, 0) + 1
                approved_count += 1
                print("  ✓ Approved and saved.\n")
                break

            elif result == "skipped":
                skipped_count += 1
                print("  → Skipped.\n")
                break

            elif result == "quit":
                print(f"\nProgress saved. {approved_count} approved, {skipped_count} skipped.")
                return approved_count, skipped_count

    return approved_count, skipped_count


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Interactive benchmark review for Benchmark v2.0.0."
    )
    p.add_argument(
        "--priority",
        choices=["HIGH", "MEDIUM", "LOW"],
        help="Review only entries of this priority tier.",
    )
    p.add_argument(
        "--entry",
        help="Jump directly to a specific entry ID.",
    )
    return p.parse_args()


def main() -> None:
    args = parse_args()

    if not CHECKLIST_PATH.exists():
        print(f"Checklist not found: {CHECKLIST_PATH}")
        print("Run the checklist generator first.")
        sys.exit(1)

    checklist: list[dict] = load_json(CHECKLIST_PATH)
    verified_by_id = load_verified()
    reviewed = load_progress()

    # Sort HIGH → MEDIUM → LOW, alphabetical within tier
    checklist.sort(key=lambda x: (PRIORITY_ORDER.get(x["priority"], 9), x["query"]))

    # Filter
    if args.priority:
        checklist = [it for it in checklist if it["priority"] == args.priority]

    if args.entry:
        checklist = [it for it in checklist if str(it["id"]) == str(args.entry)]
        if not checklist:
            print(f"Entry {args.entry!r} not found in checklist.")
            sys.exit(1)
        # Force it to be reviewable even if already done
        reviewed.discard(str(args.entry))

    print()
    print("Benchmark v2.0.0 — Review CLI")
    print(f"Checklist  : {len(checklist)} entries")
    print(f"Already done: {sum(1 for it in checklist if it['id'] in reviewed)}")

    from collections import Counter
    pc = Counter(it["priority"] for it in checklist if it["id"] not in reviewed)
    for p in ("HIGH", "MEDIUM", "LOW"):
        if pc.get(p):
            print(f"  {p:<6} pending: {pc[p]}")

    db = _open_db()
    try:
        approved, skipped = review_entries(checklist, verified_by_id, reviewed, db)
    finally:
        db.close()

    remaining = sum(1 for it in checklist if it["id"] not in reviewed)
    print(f"\nSession summary:")
    print(f"  Approved : {approved}")
    print(f"  Skipped  : {skipped}")
    print(f"  Remaining: {remaining}")
    if remaining == 0:
        print("\nAll checklist entries complete. Ready to regenerate metrics.")
        print("  python scripts/evaluate.py")
        print("  python scripts/generate_dashboard.py")


if __name__ == "__main__":
    main()
