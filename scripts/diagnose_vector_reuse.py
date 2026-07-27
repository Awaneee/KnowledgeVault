"""
scripts/diagnose_vector_reuse.py
---------------------------------
Investigates why vector reuse never activates during category ingest.

READ-ONLY: does not write to the database.

What it does
------------
For every note_intent record, it replays the _find_or_create_category
decision tree with full instrumentation:

  Step 1  canonical_name match    — does the computed name already exist?
  Step 2  rule match              — does a generic bucket exist?
  Step 3  vector scan             — for ALL 50 categories, record distances
                                     and compatibility verdicts
  Step 4  cap / create            — what actually happened

For each note it records:
  - which step decided the outcome
  - nearest category distance (regardless of threshold)
  - nearest COMPATIBLE category distance
  - why compatible check failed for the nearest category
  - whether _compatible and distance BOTH pass at threshold 0.28
  - same at thresholds 0.30, 0.35, 0.40, 0.45, 0.50

Outputs
-------
  evaluation_results/vector_reuse_diagnosis/
    diagnosis.json          — per-note records
    histogram.txt           — ASCII distance histogram
    threshold_simulation.md — reuse/purity estimates at each threshold
    summary.md              — root cause analysis

Usage
-----
  python scripts/diagnose_vector_reuse.py --user-id 1
"""

from __future__ import annotations

import json
import logging
import sys
import time
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import app.database.base_all  # noqa: F401

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.embedding_model import embedding_model
from app.core.config import settings
from app.database.session import SessionLocal
from app.models.intent_category import IntentCategory
from app.models.intent_category_embedding import IntentCategoryEmbedding
from app.models.note_intent import NoteIntent
from app.services.intent_category_service import IntentCategoryService

logging.basicConfig(
    level=logging.WARNING,          # suppress service noise
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("diagnose_vector_reuse")
logging.getLogger("sentence_transformers").setLevel(logging.ERROR)

THRESHOLDS = [0.25, 0.28, 0.30, 0.35, 0.40, 0.45, 0.50]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _intent_dict(ni: NoteIntent) -> dict:
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
        "raw_llm_json": None,
        "model_name": ni.model_name,
        "prompt_version": ni.prompt_version,
        "reasoning_summary": None,
    }


def _cosine_distance(a: list[float], b: list[float]) -> float:
    """Pure-Python cosine distance for cross-check."""
    dot = sum(x * y for x, y in zip(a, b))
    mag_a = sum(x * x for x in a) ** 0.5
    mag_b = sum(x * x for x in b) ** 0.5
    if mag_a == 0 or mag_b == 0:
        return 1.0
    return 1.0 - dot / (mag_a * mag_b)


def _compatible_reason(
    svc: IntentCategoryService,
    category: IntentCategory,
    intent: dict,
) -> tuple[bool, str]:
    """
    Returns (is_compatible, reason_if_not).
    Mirrors _compatible() exactly but captures the reason.
    """
    if category.intent_type != intent["intent_type"]:
        return False, f"intent_type_mismatch ({category.intent_type!r} vs {intent['intent_type']!r})"

    cat_actor = category.actor
    note_actor = intent.get("actor")
    if cat_actor and note_actor:
        if cat_actor.lower() != note_actor.lower():
            return False, f"actor_mismatch ({cat_actor!r} vs {note_actor!r})"
    elif bool(cat_actor) != bool(note_actor):
        return False, f"actor_presence_mismatch (cat={cat_actor!r} note={note_actor!r})"

    intent_topic = svc._normalize_topic(svc._resolve_topic_label(intent))
    category_topic = svc._normalize_topic(
        svc._get_topic_from_category_name(category.name, category.intent_type)
    )
    it = (intent_topic or "").lower().strip()
    ct = (category_topic or "").lower().strip()

    if it != ct:
        return False, f"topic_mismatch ({it!r} vs {ct!r})"

    return True, "ok"


# ---------------------------------------------------------------------------
# Core per-note probe
# ---------------------------------------------------------------------------

def probe_note(
    svc: IntentCategoryService,
    ni: NoteIntent,
    categories: list[IntentCategory],
    cat_embeddings: dict[int, list[float]],   # category_id → vector
) -> dict:
    """
    Replay the full decision tree for one note, recording every decision point.
    Returns a dict of diagnostic data.  Does NOT touch the DB.
    """
    intent = svc._normalize_intent_fields(_intent_dict(ni))
    intent_type = intent["intent_type"]
    has_topic = svc._has_meaningful_topic(intent)
    canonical_name = svc._generate_category_name(intent)
    intent_sig = svc._intent_signature(intent)
    note_vector = embedding_model.encode(intent_sig).tolist()
    topic_label = svc._resolve_topic_label(intent)

    # ---- Step 1: canonical name match -----------------------------------
    canonical_hit = any(
        c.name == canonical_name and c.intent_type == intent_type
        for c in categories
    )

    # ---- Step 2: rule match (only when canonical missed) ----------------
    skip_rule = intent_type in svc.TOPIC_INTENT_TYPES and has_topic
    rule_hit = False
    if not canonical_hit and not skip_rule:
        generic_names = {
            "communication", "study", "reference", "ideas", "tasks",
            "reminders", "questions", "meetings", "general",
            "shopping", "bills", "appointments", "errands",
            "health", "finance", "travel",
        }
        for c in categories:
            if (
                c.intent_type == intent_type
                and (c.actor or "").lower() == (intent.get("actor") or "").lower()
                and c.name.strip().lower() in generic_names
            ):
                rule_hit = True
                break

    # ---- Step 3: full distance scan over ALL categories -----------------
    distances: list[dict] = []
    for cat in categories:
        vec = cat_embeddings.get(cat.id)
        if vec is None:
            continue
        dist = _cosine_distance(note_vector, vec)
        compat, compat_reason = _compatible_reason(svc, cat, intent)
        distances.append({
            "cat_id": cat.id,
            "cat_name": cat.name,
            "cat_intent_type": cat.intent_type,
            "distance": round(dist, 6),
            "compatible": compat,
            "compat_reason": compat_reason,
        })

    distances.sort(key=lambda x: x["distance"])

    nearest = distances[0] if distances else None
    nearest_compatible = next((d for d in distances if d["compatible"]), None)

    # For each threshold: would this note reuse via vector?
    threshold_sim: dict[str, dict] = {}
    for T in THRESHOLDS:
        # with compat check (current behaviour, but threshold varies)
        with_compat = next(
            (d for d in distances if d["distance"] <= T and d["compatible"]),
            None,
        )
        # without compat check (relaxed)
        without_compat = next(
            (d for d in distances if d["distance"] <= T),
            None,
        )
        threshold_sim[str(T)] = {
            "would_reuse_with_compat": with_compat is not None,
            "target_with_compat": with_compat["cat_name"] if with_compat else None,
            "would_reuse_without_compat": without_compat is not None,
            "target_without_compat": without_compat["cat_name"] if without_compat else None,
            # purity: does the reuse target share the same intent_type+topic?
            "purity_ok_with_compat": True if with_compat else None,
            "purity_ok_without_compat": (
                without_compat["cat_intent_type"] == intent_type
                if without_compat else None
            ),
        }

    # Final decision under current code at threshold=0.28
    if canonical_hit:
        outcome = "canonical_name"
    elif rule_hit:
        outcome = "rule_match"
    else:
        # Check if any compatible candidate within 0.28 exists
        c28 = next(
            (d for d in distances if d["distance"] <= 0.28 and d["compatible"]),
            None,
        )
        if c28:
            outcome = "vector_reuse"    # would fire, but we know it never does
        else:
            outcome = "cap_hit_or_create"  # depends on cap

    # Root cause for no vector reuse (when applicable)
    vector_failure_reason = None
    if outcome == "cap_hit_or_create" and distances:
        nd = nearest["distance"]
        if nd > 0.28 and (nearest_compatible is None or nearest_compatible["distance"] > 0.28):
            vector_failure_reason = "threshold"  # distance too large
        elif nd <= 0.28 and not nearest["compatible"]:
            vector_failure_reason = "compatibility"  # close enough but incompatible
        elif nd <= 0.28 and nearest["compatible"]:
            vector_failure_reason = "none"  # would have reused (edge case)
        else:
            vector_failure_reason = "threshold_and_compatibility"
    elif outcome == "canonical_name":
        vector_failure_reason = "not_needed_canonical"
    elif outcome == "rule_match":
        vector_failure_reason = "not_needed_rule"

    return {
        "note_id": ni.note_id,
        "intent_type": intent_type,
        "topic": topic_label,
        "actor": intent.get("actor"),
        "canonical_name": canonical_name,
        "has_topic": has_topic,
        "skip_rule": skip_rule,
        "outcome": outcome,
        "canonical_hit": canonical_hit,
        "rule_hit": rule_hit,
        "nearest_distance": nearest["distance"] if nearest else None,
        "nearest_name": nearest["cat_name"] if nearest else None,
        "nearest_compatible": nearest["compatible"] if nearest else None,
        "nearest_compat_reason": nearest["compat_reason"] if nearest else None,
        "nearest_compatible_distance": nearest_compatible["distance"] if nearest_compatible else None,
        "nearest_compatible_name": nearest_compatible["cat_name"] if nearest_compatible else None,
        "vector_failure_reason": vector_failure_reason,
        "top3_distances": distances[:3],
        "threshold_sim": threshold_sim,
    }


# ---------------------------------------------------------------------------
# Analysis and reporting
# ---------------------------------------------------------------------------

def build_histogram(distances: list[float], bins: int = 20) -> str:
    if not distances:
        return "(no data)"
    lo, hi = 0.0, 1.0
    width = (hi - lo) / bins
    counts = [0] * bins
    for d in distances:
        idx = min(int((d - lo) / width), bins - 1)
        counts[idx] += 1
    max_count = max(counts) if counts else 1
    bar_width = 40
    lines = ["distance        count  bar"]
    for i, count in enumerate(counts):
        lo_b = lo + i * width
        hi_b = lo_b + width
        bar = "█" * int(count / max_count * bar_width)
        lines.append(f"[{lo_b:.2f}–{hi_b:.2f}]  {count:5d}  {bar}")
    return "\n".join(lines)


def simulate_thresholds(records: list[dict]) -> str:
    # Only consider notes that reached step 3 (no canonical/rule hit)
    step3_records = [r for r in records if not r["canonical_hit"] and not r["rule_hit"]]
    total_step3 = len(step3_records)
    total = len(records)

    lines = [
        "# Threshold Simulation",
        "",
        f"Total notes processed: {total}",
        f"Reached vector step (no canonical/rule hit): {total_step3} ({100*total_step3/max(1,total):.1f}%)",
        "",
        "## With current _compatible() check (exact topic-string match required)",
        "",
        "| Threshold | Would reuse | % of step3 | % of total | Purity OK | Notes |",
        "|-----------|-------------|------------|------------|-----------|-------|",
    ]

    for T in THRESHOLDS:
        ts = str(T)
        reuse = [r for r in step3_records if r["threshold_sim"][ts]["would_reuse_with_compat"]]
        purity_ok = sum(1 for r in reuse if r["threshold_sim"][ts]["purity_ok_with_compat"])
        purity_pct = 100 * purity_ok / len(reuse) if reuse else 0
        note = ""
        if T == 0.28:
            note = "← current"
        lines.append(
            f"| {T:.2f} | {len(reuse)} | "
            f"{100*len(reuse)/max(1,total_step3):.1f}% | "
            f"{100*len(reuse)/max(1,total):.1f}% | "
            f"{purity_pct:.0f}% | {note} |"
        )

    lines += [
        "",
        "## Without _compatible() check (distance-only gating)",
        "",
        "| Threshold | Would reuse | % of step3 | % of total | Same intent_type% | Notes |",
        "|-----------|-------------|------------|------------|-------------------|-------|",
    ]

    for T in THRESHOLDS:
        ts = str(T)
        reuse = [r for r in step3_records if r["threshold_sim"][ts]["would_reuse_without_compat"]]
        purity_ok = sum(
            1 for r in reuse
            if r["threshold_sim"][ts]["purity_ok_without_compat"]
        )
        purity_pct = 100 * purity_ok / len(reuse) if reuse else 0
        note = ""
        if T == 0.28:
            note = "← current"
        lines.append(
            f"| {T:.2f} | {len(reuse)} | "
            f"{100*len(reuse)/max(1,total_step3):.1f}% | "
            f"{100*len(reuse)/max(1,total):.1f}% | "
            f"{purity_pct:.0f}% | {note} |"
        )

    # Breakdown of wrong-type merges at T=0.40 without compat
    lines += ["", "## Cross-intent merges at T=0.40 (without _compatible)", ""]
    T = 0.40
    ts = str(T)
    cross_type = [
        r for r in step3_records
        if r["threshold_sim"][ts]["would_reuse_without_compat"]
        and not r["threshold_sim"][ts]["purity_ok_without_compat"]
    ]
    if cross_type:
        lines.append(f"{len(cross_type)} notes would merge into wrong intent_type category:")
        by_pair = defaultdict(int)
        for r in cross_type:
            tgt = r["threshold_sim"][ts]["target_without_compat"]
            by_pair[(r["intent_type"], tgt)] += 1
        for (src_type, tgt_name), cnt in sorted(by_pair.items(), key=lambda x: -x[1])[:15]:
            lines.append(f"  - {src_type!r} note → `{tgt_name}` × {cnt}")
    else:
        lines.append("None — no cross-intent merges detected.")

    return "\n".join(lines)


def build_summary(records: list[dict]) -> str:
    total = len(records)
    canonical = sum(1 for r in records if r["canonical_hit"])
    rule = sum(1 for r in records if not r["canonical_hit"] and r["rule_hit"])
    step3 = [r for r in records if not r["canonical_hit"] and not r["rule_hit"]]

    # Vector failure reasons for notes that reached step 3
    reason_counts = defaultdict(int)
    for r in step3:
        reason_counts[r["vector_failure_reason"] or "unknown"] += 1

    # Distance distribution for nearest category (ALL notes that reached step 3)
    nearest_dists = [r["nearest_distance"] for r in step3 if r["nearest_distance"] is not None]
    compat_dists = [r["nearest_compatible_distance"] for r in step3 if r["nearest_compatible_distance"] is not None]

    median_nearest = sorted(nearest_dists)[len(nearest_dists) // 2] if nearest_dists else None
    median_compat = sorted(compat_dists)[len(compat_dists) // 2] if compat_dists else None

    pct_near_028 = sum(1 for d in nearest_dists if d <= 0.28) / max(1, len(nearest_dists))
    pct_near_040 = sum(1 for d in nearest_dists if d <= 0.40) / max(1, len(nearest_dists))
    pct_near_050 = sum(1 for d in nearest_dists if d <= 0.50) / max(1, len(nearest_dists))

    compat_reason_counts = defaultdict(int)
    for r in step3:
        if r["nearest_distance"] is not None and r["nearest_distance"] <= 0.28:
            compat_reason_counts[r["nearest_compat_reason"] or "ok"] += 1

    lines = [
        "# Vector Reuse Diagnosis — Summary",
        "",
        "## Decision tree breakdown",
        "",
        f"| Step | Notes | % of total |",
        f"|------|-------|------------|",
        f"| 1. canonical_name hit | {canonical} | {100*canonical/max(1,total):.1f}% |",
        f"| 2. rule match hit | {rule} | {100*rule/max(1,total):.1f}% |",
        f"| 3. vector search (step3) | {len(step3)} | {100*len(step3)/max(1,total):.1f}% |",
        f"| 3a. → vector_reuse fired | {reason_counts['none']} | {100*reason_counts['none']/max(1,total):.1f}% |",
        f"| 3b. → failed threshold | {reason_counts['threshold']} | {100*reason_counts['threshold']/max(1,total):.1f}% |",
        f"| 3c. → failed compatibility | {reason_counts['compatibility']} | {100*reason_counts['compatibility']/max(1,total):.1f}% |",
        f"| 3d. → failed both | {reason_counts['threshold_and_compatibility']} | {100*reason_counts['threshold_and_compatibility']/max(1,total):.1f}% |",
        "",
        "## Distance statistics (notes that reached step 3)",
        "",
        f"| Metric | Nearest any | Nearest compatible |",
        f"|--------|------------|-------------------|",
        f"| Count  | {len(nearest_dists)} | {len(compat_dists)} |",
        f"| Median | {median_nearest:.4f} | {median_compat:.4f if median_compat else 'N/A'} |",
        f"| % ≤ 0.28 | {100*pct_near_028:.1f}% | — |",
        f"| % ≤ 0.40 | {100*pct_near_040:.1f}% | — |",
        f"| % ≤ 0.50 | {100*pct_near_050:.1f}% | — |",
        "",
        "## Why _compatible() fails for nearest category within 0.28",
        "",
        f"(Only for notes where nearest distance ≤ 0.28)",
        "",
    ]

    if compat_reason_counts:
        lines += [
            "| Reason | Count |",
            "|--------|-------|",
        ]
        for reason, count in sorted(compat_reason_counts.items(), key=lambda x: -x[1]):
            lines.append(f"| {reason} | {count} |")
    else:
        lines.append("No notes had nearest distance ≤ 0.28.")

    lines += [
        "",
        "## Root cause diagnosis",
        "",
    ]

    # Determine primary root cause
    total_step3 = len(step3)
    if total_step3 == 0:
        lines.append("All notes were handled by canonical or rule match — vector path never reached.")
    else:
        threshold_only = reason_counts["threshold"]
        compat_only = reason_counts["compatibility"]
        both = reason_counts["threshold_and_compatibility"]

        if threshold_only + both > compat_only:
            lines += [
                "**PRIMARY CAUSE: Threshold too strict.**",
                "",
                f"Of {total_step3} notes reaching the vector step:",
                f"- {threshold_only} ({100*threshold_only/total_step3:.0f}%): nearest category is beyond 0.28 (distance-only failure)",
                f"- {compat_only} ({100*compat_only/total_step3:.0f}%): within 0.28 but _compatible() rejects",
                f"- {both} ({100*both/total_step3:.0f}%): both threshold and compatibility fail",
            ]
        elif compat_only > threshold_only + both:
            lines += [
                "**PRIMARY CAUSE: _compatible() overly strict.**",
                "",
                f"Of {total_step3} notes reaching the vector step:",
                f"- {compat_only} ({100*compat_only/total_step3:.0f}%): within 0.28 but _compatible() rejects",
                f"- {threshold_only} ({100*threshold_only/total_step3:.0f}%): threshold-only failure",
                f"- {both} ({100*both/total_step3:.0f}%): both fail",
            ]
        else:
            lines += [
                "**MIXED CAUSE: Both threshold and _compatible() contribute equally.**",
            ]

        # Structural analysis
        lines += [
            "",
            "## Structural analysis: why _compatible() kills vector reuse",
            "",
            "_compatible() requires topic_str == category_topic_str (exact string equality).",
            "",
            "_generate_category_name() uses the same topic normalization to build the canonical name.",
            "",
            "Therefore:",
            "- If topics match exactly → canonical name matches → step 1 fires, step 3 never reached",
            "- If topics don't match exactly → _compatible() returns False → vector reuse blocked",
            "",
            "**Consequence: vector reuse is logically unreachable for topic-bearing intents.**",
            "",
            "The ONLY theoretical path: notes with no topic, where no generic rule-match bucket exists.",
            "In practice, generic buckets ('Tasks', 'General') are created early and catch those notes via rule match.",
            "",
            "**_compatible() makes vector reuse dead code for the current category naming scheme.**",
        ]

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--user-id", type=int, default=1)
    parser.add_argument("--output", type=str, default="evaluation_results/vector_reuse_diagnosis")
    parser.add_argument("--max-notes", type=int, default=None,
                        help="Process at most N notes (default: all)")
    args = parser.parse_args()

    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)

    db = SessionLocal()
    try:
        svc = IntentCategoryService(db)

        # Load all categories and their embeddings up front
        categories: list[IntentCategory] = (
            db.query(IntentCategory)
            .filter(IntentCategory.user_id == args.user_id, IntentCategory.status == "active")
            .all()
        )
        embeddings_rows: list[IntentCategoryEmbedding] = (
            db.query(IntentCategoryEmbedding)
            .filter(
                IntentCategoryEmbedding.intent_category_id.in_(
                    [c.id for c in categories]
                )
            )
            .all()
        )
        cat_embeddings: dict[int, list[float]] = {
            e.intent_category_id: list(e.embedding_vector)
            for e in embeddings_rows
        }

        print(f"Loaded {len(categories)} categories, {len(cat_embeddings)} with embeddings.")

        # Load note_intent records
        note_intents: list[NoteIntent] = (
            db.query(NoteIntent)
            .filter(NoteIntent.user_id == args.user_id)
            .order_by(NoteIntent.note_id)
            .all()
        )
        if args.max_notes:
            note_intents = note_intents[: args.max_notes]

        total = len(note_intents)
        print(f"Processing {total} notes...")

        records = []
        t0 = time.monotonic()

        for i, ni in enumerate(note_intents, 1):
            try:
                rec = probe_note(svc, ni, categories, cat_embeddings)
                records.append(rec)
            except Exception as exc:
                print(f"ERROR note_id={ni.note_id}: {exc}")
                records.append({
                    "note_id": ni.note_id,
                    "error": str(exc),
                })

            if i % 100 == 0 or i == total:
                elapsed = time.monotonic() - t0
                print(f"  {i}/{total}  elapsed={elapsed:.1f}s", end="\r")

        print(f"\nDone in {time.monotonic() - t0:.1f}s")

        # ---- Save raw diagnosis records
        diag_path = out / "diagnosis.json"
        diag_path.write_text(
            json.dumps(records, indent=2, default=str),
            encoding="utf-8",
        )
        print(f"Saved {len(records)} records → {diag_path}")

        # ---- Build histogram of nearest distances (notes reaching step 3)
        step3_recs = [r for r in records if "nearest_distance" in r and r.get("nearest_distance") is not None and not r.get("canonical_hit") and not r.get("rule_hit")]
        nearest_dists = [r["nearest_distance"] for r in step3_recs]
        compat_dists = [r["nearest_compatible_distance"] for r in step3_recs if r.get("nearest_compatible_distance") is not None]

        hist_text = (
            "# Cosine Distance Histograms\n\n"
            "## Nearest category (any) — notes reaching vector step\n\n"
            f"n = {len(nearest_dists)}\n\n"
        )
        hist_text += build_histogram(nearest_dists)
        hist_text += "\n\n## Nearest COMPATIBLE category — notes reaching vector step\n\n"
        hist_text += f"n = {len(compat_dists)}\n\n"
        hist_text += build_histogram(compat_dists)

        # Also histogram for ALL notes (including canonical hits)
        all_nearest = [r["nearest_distance"] for r in records if r.get("nearest_distance") is not None]
        hist_text += "\n\n## Nearest category (any) — ALL notes\n\n"
        hist_text += f"n = {len(all_nearest)}\n\n"
        hist_text += build_histogram(all_nearest)

        hist_path = out / "histogram.md"
        hist_path.write_text(hist_text, encoding="utf-8")
        print(f"Saved histogram → {hist_path}")

        # ---- Threshold simulation
        sim_text = simulate_thresholds(records)
        sim_path = out / "threshold_simulation.md"
        sim_path.write_text(sim_text, encoding="utf-8")
        print(f"Saved threshold simulation → {sim_path}")

        # ---- Summary
        summary_text = build_summary(records)
        summary_path = out / "summary.md"
        summary_path.write_text(summary_text, encoding="utf-8")
        print(f"Saved summary → {summary_path}")

        # ---- Print key numbers immediately
        print("\n" + "=" * 60)
        print("KEY FINDINGS")
        print("=" * 60)
        canonical = sum(1 for r in records if r.get("canonical_hit"))
        rule = sum(1 for r in records if not r.get("canonical_hit") and r.get("rule_hit"))
        step3 = [r for r in records if not r.get("canonical_hit") and not r.get("rule_hit")]

        print(f"Total notes          : {total}")
        print(f"canonical_name hit   : {canonical} ({100*canonical/total:.1f}%)")
        print(f"rule_match hit       : {rule} ({100*rule/total:.1f}%)")
        print(f"Reached vector step  : {len(step3)} ({100*len(step3)/total:.1f}%)")

        if nearest_dists:
            print(f"\nNearest category distances (notes reaching step 3):")
            print(f"  min    = {min(nearest_dists):.4f}")
            print(f"  median = {sorted(nearest_dists)[len(nearest_dists)//2]:.4f}")
            print(f"  p75    = {sorted(nearest_dists)[int(len(nearest_dists)*0.75)]:.4f}")
            print(f"  p90    = {sorted(nearest_dists)[int(len(nearest_dists)*0.90)]:.4f}")
            print(f"  max    = {max(nearest_dists):.4f}")
            print(f"  % ≤ 0.28 : {100*sum(1 for d in nearest_dists if d<=0.28)/len(nearest_dists):.1f}%")
            print(f"  % ≤ 0.35 : {100*sum(1 for d in nearest_dists if d<=0.35)/len(nearest_dists):.1f}%")
            print(f"  % ≤ 0.40 : {100*sum(1 for d in nearest_dists if d<=0.40)/len(nearest_dists):.1f}%")

        # Compat failure reasons for notes within 0.28
        within_028 = [r for r in step3 if r.get("nearest_distance") is not None and r["nearest_distance"] <= 0.28]
        print(f"\nNotes within 0.28 of some category: {len(within_028)}")
        reasons = defaultdict(int)
        for r in within_028:
            reasons[r.get("nearest_compat_reason", "??")] += 1
        for reason, cnt in sorted(reasons.items(), key=lambda x: -x[1]):
            print(f"  {reason}: {cnt}")

        # Threshold sim printout
        print(f"\nThreshold simulation (with _compatible check):")
        for T in THRESHOLDS:
            ts = str(T)
            reuse = sum(1 for r in step3 if r.get("threshold_sim", {}).get(ts, {}).get("would_reuse_with_compat"))
            marker = " ← current" if T == 0.28 else ""
            print(f"  T={T:.2f}: {reuse:4d} notes would reuse ({100*reuse/max(1,len(step3)):.1f}% of step3){marker}")

        print(f"\nThreshold simulation (WITHOUT _compatible check):")
        for T in THRESHOLDS:
            ts = str(T)
            reuse = sum(1 for r in step3 if r.get("threshold_sim", {}).get(ts, {}).get("would_reuse_without_compat"))
            purity = sum(1 for r in step3 if r.get("threshold_sim", {}).get(ts, {}).get("purity_ok_without_compat"))
            marker = " ← current" if T == 0.28 else ""
            purity_pct = 100 * purity / max(1, reuse)
            print(f"  T={T:.2f}: {reuse:4d} notes would reuse ({100*reuse/max(1,len(step3)):.1f}% of step3), intent_type purity={purity_pct:.0f}%{marker}")

    finally:
        db.close()


if __name__ == "__main__":
    main()
