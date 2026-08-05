"""
KnowledgeVault Evaluation CLI

Example:

python scripts/evaluate.py \
    --user-id 1 \
    --benchmark app/evaluation/benchmark/benchmark.json \
    --output evaluation_results

Sprint 2-C additions:
  - Emits evaluation_results/{run_id}/manifest.json after every run.
  - Calls generate_dashboard.py to produce dashboard.html.
  - Optionally runs confound detection (--check-confounds flag).
"""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
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
print("DATABASE URL:", engine.url.render_as_string(hide_password=True))
print("=" * 60)


def _get_total_note_count(db, user_id: int) -> int:
    """Return number of organized notes for this user (for corpus coverage)."""
    try:
        import app.database.base_all  # noqa: F401
        from app.models.notes import Note
        return db.query(Note.id).filter(
            Note.user_id == user_id,
            Note.organization_status == "organized",
        ).count()
    except Exception:
        return 0


def _emit_run_manifest(report, output_dir: Path, gates_path: Path) -> dict:
    """Write per-run manifest.json with gate check results. Returns gate_results."""
    gates: dict = {}
    if gates_path.exists():
        try:
            gates = json.loads(gates_path.read_text(encoding="utf-8"))
        except Exception:
            pass

    strategy_gates = gates.get("strategies", {})

    summaries_data: dict[str, dict] = {}
    gate_results: dict[str, dict] = {}

    for summary in report.summaries:
        key = summary.strategy.value.upper()
        ci = summary.mrr_ci
        summaries_data[key] = {
            "mrr": round(summary.mrr, 4),
            "mrr_ci": [round(ci[0], 4), round(ci[1], 4)] if ci else None,
            "hit_rate": round(summary.hit_rate, 4),
            "precision": round(summary.mean_precision_at_k, 4),
            "recall": round(summary.mean_recall_at_k, 4),
            "map_at_k": round(summary.mean_map_at_k, 4),
            "r_precision": round(summary.mean_r_precision, 4),
            "avg_latency_ms": round(summary.avg_latency_ms, 2),
        }

        sg = strategy_gates.get(key, {})
        mrr_floor = sg.get("mrr_floor")
        hit_floor = sg.get("hit_rate_floor")
        lat_ceil = sg.get("avg_latency_ms_ceiling")

        gate_results[key] = {
            "mrr_pass": (mrr_floor is None or summary.mrr >= mrr_floor),
            "hit_rate_pass": (hit_floor is None or summary.hit_rate >= hit_floor),
            "latency_pass": (lat_ceil is None or summary.avg_latency_ms <= lat_ceil),
        }

    comparisons_data = []
    for comp in report.strategy_comparisons:
        comparisons_data.append({
            "baseline": comp.baseline.value,
            "candidate": comp.candidate.value,
            "delta_mrr": comp.delta_mrr,
            "mrr_ci": [comp.mrr_ci_lower, comp.mrr_ci_upper],
            "mrr_significant": comp.mrr_significant,
            "delta_hit_rate": comp.delta_hit_rate,
            "recommendation": comp.recommendation,
        })

    manifest = {
        "run_id": report.run_id,
        "created_at": report.created_at,
        "benchmark_version": report.benchmark_version,
        "git_commit": report.git_commit,
        "corpus_coverage": report.corpus_coverage,
        "k": report.k,
        "total_queries": report.total_queries,
        "strategies": [s.strategy.value for s in report.summaries],
        "summaries": summaries_data,
        "gate_check": gate_results,
        "comparisons": comparisons_data,
    }

    manifest_path = output_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"Run manifest written: {manifest_path}")
    return gate_results


def parse_args():
    parser = argparse.ArgumentParser(
        description="KnowledgeVault Evaluation Framework"
    )
    parser.add_argument("--user-id", type=int, required=True)
    parser.add_argument(
        "--benchmark", type=str,
        default="app/evaluation/benchmark/benchmark.json",
    )
    parser.add_argument("--output", type=str, default="evaluation_results")
    parser.add_argument("--k", type=int, default=5)
    parser.add_argument(
        "--check-confounds", action="store_true",
        help="Run confound detection after the benchmark completes.",
    )
    parser.add_argument(
        "--gates", type=str, default="evaluation_results/gates.json",
        help="Path to gates.json for regression floor checking.",
    )
    parser.add_argument(
        "--no-dashboard", action="store_true",
        help="Skip dashboard generation.",
    )
    parser.add_argument(
        "--strict-gates", action="store_true",
        help="Exit with code 1 if any regression gate fails (for CI use).",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    db = SessionLocal()

    try:
        total_note_count = _get_total_note_count(db, args.user_id)

        runner = EvaluationRunner(
            db=db,
            user_id=args.user_id,
            benchmark_path=args.benchmark,
            k=args.k,
            total_note_count=total_note_count or None,
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

        gate_results = _emit_run_manifest(report, output_dir, Path(args.gates))

        print()
        print("=" * 80)
        print("Evaluation Complete")
        print("=" * 80)
        print()
        print(f"Markdown Report : {output_dir/'evaluation_report.md'}")
        print(f"CSV Report      : {output_dir/'evaluation_results.csv'}")
        print(f"Manifest        : {output_dir/'manifest.json'}")
        print()

    finally:
        db.close()

    # Strict gate enforcement — fail CI if any gate is missed.
    if args.strict_gates:
        failed = [
            f"{strategy}.{metric}"
            for strategy, checks in gate_results.items()
            for metric, passed in checks.items()
            if not passed
        ]
        if failed:
            print(f"\n❌ Gate failures: {', '.join(failed)}")
            sys.exit(1)
        print("\n✅ All regression gates passed.")

    # Dashboard generation (subprocess to avoid import issues)
    if not args.no_dashboard:
        dashboard_script = ROOT / "scripts" / "generate_dashboard.py"
        if dashboard_script.exists():
            try:
                subprocess.run(
                    [sys.executable, str(dashboard_script),
                     "--results-dir", str(output_dir)],
                    check=False,
                )
            except Exception as exc:
                print(f"Dashboard generation failed (non-fatal): {exc}")

    # Confound detection
    if args.check_confounds:
        confound_script = ROOT / "scripts" / "check_benchmark_confounds.py"
        if confound_script.exists():
            print("\nRunning confound detection…")
            result = subprocess.run(
                [sys.executable, str(confound_script),
                 "--results", str(output_dir / "evaluation_results.csv"),
                 "--benchmark", args.benchmark,
                 "--gates", args.gates],
                check=False,
            )
            if result.returncode != 0:
                print("\n⚠  Confounds detected — see details above.")


if __name__ == "__main__":
    main()
