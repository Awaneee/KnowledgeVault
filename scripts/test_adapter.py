"""
Single-adapter smoke tester.

Runs one query through a single production retrieval adapter and prints
the result.  Used for quick regression checks after code changes without
running the full 50-query benchmark.

Usage:
    python scripts/test_adapter.py \\
        --strategy hybrid \\
        --query "Things I need to tell Sid" \\
        --user-id 1

Exit code 0 = adapter returned ≥ 1 result.
Exit code 1 = adapter returned empty results or raised an exception.
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Smoke-test a single retrieval adapter.")
    p.add_argument("--strategy", choices=["semantic", "intent", "hybrid", "rerank"],
                   default="hybrid")
    p.add_argument("--query", type=str, required=True)
    p.add_argument("--user-id", type=int, default=1)
    p.add_argument("--k", type=int, default=5)
    return p.parse_args()


def main() -> None:
    args = parse_args()

    import app.database.base_all  # noqa: F401
    from app.database.session import SessionLocal
    from app.evaluation.models import BenchmarkQuery, RetrievalStrategy
    from app.evaluation.adapters.semantic import SemanticAdapter
    from app.evaluation.adapters.intent import IntentAdapter
    from app.evaluation.adapters.hybrid import HybridAdapter
    from app.evaluation.adapters.rerank import RerankAdapter

    db = SessionLocal()
    try:
        adapter_cls = {
            "semantic": SemanticAdapter,
            "intent": IntentAdapter,
            "hybrid": HybridAdapter,
            "rerank": RerankAdapter,
        }[args.strategy]

        adapter = adapter_cls(db=db, user_id=args.user_id)

        dummy_query = BenchmarkQuery(
            id="smoke_test",
            query=args.query,
            expected_intent="general",
            expected_category="General",
            relevant_note_ids=[],
            difficulty="medium",
        )

        print(f"\nAdapter  : {args.strategy.upper()}")
        print(f"Query    : {args.query!r}")
        print(f"User ID  : {args.user_id}")
        print()

        t0 = time.perf_counter()
        result = adapter.run(dummy_query)
        elapsed_ms = (time.perf_counter() - t0) * 1000

        print(f"Latency  : {elapsed_ms:.1f}ms")
        print(f"Results  : {len(result.retrieved_note_ids)} note(s)")
        print()

        if result.retrieved_note_ids:
            print("Retrieved note IDs (ordered):")
            for rank, nid in enumerate(result.retrieved_note_ids, 1):
                print(f"  [{rank}] note_id={nid}")
        else:
            print("No results returned.")

        if result.predicted_intent:
            print(f"\nPredicted intent   : {result.predicted_intent}")
        if result.predicted_category:
            print(f"Predicted category : {result.predicted_category}")

        if result.error:
            print(f"\nERROR: {result.error}")
            sys.exit(1)

        if not result.retrieved_note_ids:
            print("\n⚠  Zero results returned.")
            sys.exit(1)

        print("\n✓ Adapter is functioning correctly.\n")
        sys.exit(0)

    finally:
        db.close()


if __name__ == "__main__":
    main()
