# KnowledgeVault Retrieval Benchmark Gate Protocol

This document defines the protocol for using benchmark results to make
production retrieval decisions.  It encodes the lessons from Sprint 2-B
where a false-positive result caused `RERANKING_ENABLED=True` to be
temporarily set before the error was caught by post-hoc latency analysis.

---

## What is a gate?

A **benchmark gate** is a minimum quality floor that a retrieval strategy
must clear before its feature flag is enabled in production.  Gates are
stored in `evaluation_results/gates.json`.

---

## Current gates

Established from **Benchmark v2.0.0** run `2c80e257` (205 queries, graded
relevance, k=5, 2026-07-31).

| Strategy | MRR floor | HR floor | nDCG@5 floor | Avg latency ceiling | Observed MRR | Observed HR |
|---|---:|---:|---:|---:|---:|---:|
| SEMANTIC | 0.5625 | 0.7239 | 0.3697 | 100ms | 0.5799 | 0.7463 |
| HYBRID | 0.5851 | 0.7239 | 0.3737 | 300ms | 0.6032 | 0.7463 |
| RERANK | not established | not established | not established | 500ms | 0.5981 | 0.7463 |

Floors are set at 97% of the observed value for that strategy
(`floor = observed × 0.97`).  The RERANK gate is not established because
`RERANKING_ENABLED=False` — observed RERANK metrics reflect the HYBRID
candidate pool without cross-encoder scoring and are not meaningful as a
performance floor (see ADR-003 addendum).

**Sprint 2-B gates (v1.0.0, 50-query benchmark, run `c1df0566`) are
superseded.** They are preserved in git history only.

---

## How to run a gate check

```bash
# Step 1: Run the benchmark
python scripts/evaluate.py \
    --user-id 1 \
    --benchmark app/evaluation/benchmark/verified.json \
    --output evaluation_results/my_run \
    --check-confounds

# Step 2: Verify corpus is consistent with the benchmark
python scripts/verify_corpus_version.py --user-id 1

# Step 3: Check confounds manually (if --check-confounds showed warnings)
python scripts/check_benchmark_confounds.py \
    --results evaluation_results/my_run/evaluation_results.csv \
    --benchmark app/evaluation/benchmark/benchmark.json
```

The `--check-confounds` flag in `evaluate.py` calls confound detection
automatically after every run and prints a summary.

---

## Rules for approving a retrieval change

A retrieval change (new strategy, new model, parameter change) is approved
for production when **all** of the following are true:

1. **Benchmark version ≥ 2.0.0** — graded relevance must be enabled.
   Benchmark v2.0.0 is now the active benchmark (`verified.json`, 205 queries).
   Version 1.0.0 results (`benchmark.json`, 50 queries) are archived and must
   not be used for gate decisions.

2. **Query count ≥ 100** — too few queries produce unreliable bootstrap CIs.
   The v2.0.0 benchmark satisfies this with 205 queries.

3. **Proposed strategy MRR > baseline HYBRID MRR** with bootstrap 95% CI
   excluding zero.  The CI is reported automatically in the Markdown report
   and in `manifest.json` under `comparisons`.

4. **Hit Rate ≥ baseline HYBRID Hit Rate** — no regression on hit rate.

5. **Avg latency within the approved ceiling** for the strategy (from gates.json).

6. **No confounds detected** by `check_benchmark_confounds.py`.  Specifically:
   - C1: RERANK latency must be ≥ 50ms above HYBRID to confirm the
     cross-encoder actually ran (prevents Sprint 2-B false positive).
   - C2: All relevant_note_ids must exist in the database.
   - C3: RERANK and HYBRID results must not be identical across all queries.

7. **Corpus version matches** the benchmark's `note_count_at_labeling`
   (verified by `verify_corpus_version.py`).

---

## Updating gate floors

When a new strategy improvement clears all gates and is shipped to production,
update `evaluation_results/gates.json` to reflect the new baseline:

1. Run the full benchmark against the new production code.
2. Record the new MRR and Hit Rate in `gates.json` as:
   ```
   new_floor = observed_value * 0.97
   ```
3. Commit `gates.json` in the same PR as the feature flag change.
4. Update the `established_from_run` field to the current run ID.

Do not raise gates without a corresponding PR — this ensures there is always
an explicit decision record.

---

## Sprint 2-B post-mortem (lessons encoded here)

On 2026-07-28, cross-encoder reranking appeared to improve Hit Rate from
0.740 to 0.760 in a benchmark run.  The change was approved and
`RERANKING_ENABLED=True` was briefly set.

The final smoke benchmark showed RERANK degraded to Hit Rate=0.640 and
MRR=0.483, worse than HYBRID.  Investigation revealed:

1. The intermediate run used a WSL2 shell env-var `RERANKING_ENABLED=true`
   that was not inherited by the Windows Python binary.
2. The cross-encoder never executed — `rerank_model` was `None`.
3. The improvement was from the expanded candidate pool (limit=20 vs limit=5
   for the HYBRID adapter baseline), not from the cross-encoder.
4. Latency delta was only 9ms (pool expansion overhead), not the expected
   250–400ms (inference overhead).

**Confound C1** in `check_benchmark_confounds.py` directly encodes the
latency check that would have caught this immediately.

---

## Benchmark file roles

| File | Role | Gate decisions |
|---|---|---|
| `benchmark/verified.json` | **Active** 205-query graded-relevance benchmark (v2.0.0) | ✓ required for all Sprint 3+ decisions |
| `benchmark/manifest.json` | Dataset version metadata | metadata only |
| `benchmark/benchmark.json` | Archived 50-query binary-relevance benchmark (v1.0.0) | ✗ superseded; do not use for gates |
| `benchmark/candidates.json` | Auto-generated pool (not human-reviewed) | ✗ never |
| `benchmark/uncertain.json` | Skipped entries awaiting resolution | ✗ never |
| `evaluation_results/gates.json` | Regression floor values | gate reference |
