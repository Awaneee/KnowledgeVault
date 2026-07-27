"""
CLI entry point for Ask endpoint evaluation.

Usage:
    python scripts/evaluate_ask.py --user-id 1 --output evaluation_results/

Options:
    --user-id     DB user ID whose notes are queried (default: 1)
    --dataset     Path to gold_dataset.json (default: built-in dataset)
    --output      Output directory for reports (default: evaluation_results/)
    --no-artifacts
                  Skip writing per-query debug JSON artifacts
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

# Ensure project root is on the path when running directly.
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.evaluation.ask.reports import AskCSVReport, AskMarkdownReport
from app.evaluation.ask.runner import AskEvaluationRunner


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s — %(message)s",
)
logger = logging.getLogger(__name__)

_DEFAULT_DATASET = (
    Path(__file__).parent.parent
    / "app" / "evaluation" / "ask_benchmark" / "gold_dataset.json"
)
_DEFAULT_OUTPUT = Path("evaluation_results")


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the KnowledgeVault Ask endpoint evaluation."
    )
    parser.add_argument(
        "--user-id", type=int, default=1,
        help="DB user ID whose notes are evaluated (default: 1)",
    )
    parser.add_argument(
        "--dataset", type=Path, default=_DEFAULT_DATASET,
        help=f"Path to gold_dataset.json (default: {_DEFAULT_DATASET})",
    )
    parser.add_argument(
        "--output", type=Path, default=_DEFAULT_OUTPUT,
        help="Output directory for MD and CSV reports (default: evaluation_results/)",
    )
    parser.add_argument(
        "--no-artifacts", action="store_true",
        help="Skip writing per-query debug JSON artifacts",
    )
    parser.add_argument(
        "--limit", type=int, default=None,
        help="Optional maximum number of queries to evaluate",
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()

    if not args.dataset.exists():
        logger.error("Dataset not found: %s", args.dataset)
        sys.exit(1)

    # Connect to database
    print(f"Database: {settings.DATABASE_URL}")
    print(f"Dataset:  {args.dataset}")
    print(f"Output:   {args.output}")
    if args.limit:
        print(f"Limit:    {args.limit}")
    print()

    engine = create_engine(settings.DATABASE_URL)
    Session = sessionmaker(bind=engine)
    db = Session()

    try:
        artifact_dir = (
            None if args.no_artifacts
            else args.output / "ask_debug"
        )

        runner = AskEvaluationRunner(db)
        report = runner.run(
            user_id=args.user_id,
            dataset_path=args.dataset,
            artifact_dir=artifact_dir,
            limit=args.limit,
        )
    finally:
        db.close()

    # Print summary to console
    print("=" * 60)
    print("ASK EVALUATION RESULTS")
    print("=" * 60)
    print(f"Run ID:          {report.run_id}")
    print(f"Total Queries:   {report.total_queries}")
    print(f"Overall Score:   {report.avg_overall:.3f}")
    print()
    print("AVERAGES:")
    print(f"  Correctness:   {report.avg_correctness:.3f}")
    print(f"  Groundedness:  {report.avg_groundedness:.3f}")
    print(f"  Faithfulness:  {report.avg_faithfulness:.3f}")
    print(f"  Hallucination: {report.avg_hallucination:.3f}")
    print(f"  Completeness:  {report.avg_completeness:.3f}")
    print()
    print("LATENCY:")
    print(f"  Avg Retrieval: {report.avg_retrieval_ms:.1f}ms")
    print(f"  Avg LLM:       {report.avg_llm_ms:.1f}ms")
    print(f"  Avg Total:     {report.avg_total_ms:.1f}ms")
    print()
    print(f"Estimated Cost:  ${report.total_estimated_cost_usd:.6f} USD")
    print()

    if report.root_cause_counts:
        print("ROOT CAUSE DISTRIBUTION:")
        for cause, count in sorted(
            report.root_cause_counts.items(), key=lambda x: -x[1]
        ):
            print(f"  {cause}: {count}")
        print()

    print("PER-CATEGORY:")
    for cat in report.category_summaries:
        print(
            f"  {cat.category:<25} n={cat.query_count}  "
            f"overall={cat.avg_overall:.3f}  "
            f"correct={cat.avg_correctness:.3f}  "
            f"ground={cat.avg_groundedness:.3f}"
        )
    print()

    # Write reports
    md_path  = args.output / "ask_evaluation_report.md"
    csv_path = args.output / "ask_evaluation_results.csv"

    AskMarkdownReport.generate(report, md_path)
    AskCSVReport.generate(report, csv_path)

    print(f"Markdown report: {md_path}")
    print(f"CSV report:      {csv_path}")
    if artifact_dir:
        print(f"Debug artifacts: {artifact_dir}/")
    print()
    print("Done.")


if __name__ == "__main__":
    main()
