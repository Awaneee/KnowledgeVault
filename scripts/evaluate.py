"""
KnowledgeVault Evaluation CLI

Example:

python scripts/evaluate.py \
    --user-id 1 \
    --benchmark app/evaluation/benchmark/benchmark.json \
    --output evaluation_results
"""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


import argparse

from app.database.session import SessionLocal

from app.evaluation.runner import EvaluationRunner

from app.evaluation.reports.console import ConsoleReport
from app.evaluation.reports.markdown import MarkdownReport
from app.evaluation.reports.csv import CSVReport
from app.database.session import engine

print("=" * 60)
print("DATABASE URL:", engine.url)
print("=" * 60)


def parse_args():

    parser = argparse.ArgumentParser(
        description="KnowledgeVault Evaluation Framework"
    )

    parser.add_argument(
        "--user-id",
        type=int,
        required=True,
        help="User whose notes will be evaluated."
    )

    parser.add_argument(
        "--benchmark",
        type=str,
        default="app/evaluation/benchmark/benchmark.json",
        help="Benchmark dataset."
    )

    parser.add_argument(
        "--output",
        type=str,
        default="evaluation_results",
        help="Directory for generated reports."
    )

    parser.add_argument(
        "--k",
        type=int,
        default=5,
        help="K used for Recall@K / Precision@K."
    )

    return parser.parse_args()


def main():

    args = parse_args()

    output_dir = Path(args.output)
    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    db = SessionLocal()

    try:

        runner = EvaluationRunner(
            db=db,
            user_id=args.user_id,
            benchmark_path=args.benchmark,
            k=args.k,
        )

        report = runner.run()

        ConsoleReport.render(report)

        MarkdownReport.generate(
            report,
            output_dir / "evaluation_report.md",
        )

        CSVReport.generate(
            report,
            output_dir / "evaluation_results.csv",
        )

        print()

        print("=" * 80)
        print("Evaluation Complete")
        print("=" * 80)

        print()

        print(
            f"Markdown Report : {output_dir/'evaluation_report.md'}"
        )

        print(
            f"CSV Report      : {output_dir/'evaluation_results.csv'}"
        )

        print()

    finally:
        db.close()


if __name__ == "__main__":
    main()