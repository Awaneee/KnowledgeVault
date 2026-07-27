import json, glob, statistics
from pathlib import Path
from collections import defaultdict

debug_dir = Path('evaluation_results/ask_debug')
files = sorted(glob.glob(str(debug_dir / '*_debug.json')))

results = []
for f in files:
    with open(f, encoding='utf-8') as fh:
        results.append(json.load(fh))

def compute_recall(result):
    expected = set(result.get('expected_note_ids', []))
    if not expected:
        return 1.0
    retrieved = set(c['note_id'] for c in result.get('context', {}).get('retrieved_chunks', []))
    return len(expected & retrieved) / len(expected)

def compute_precision(result):
    expected = set(result.get('expected_note_ids', []))
    if not expected:
        return 1.0
    retrieved = [c['note_id'] for c in result.get('context', {}).get('retrieved_chunks', [])]
    if not retrieved:
        return 0.0
    return len(expected & set(retrieved)) / len(retrieved)

def compute_mrr(result):
    expected = set(result.get('expected_note_ids', []))
    if not expected:
        return 1.0
    retrieved = [c['note_id'] for c in result.get('context', {}).get('retrieved_chunks', [])]
    for rank, nid in enumerate(retrieved, 1):
        if nid in expected:
            return 1.0 / rank
    return 0.0

def compute_ndcg(result, k=8):
    expected = set(result.get('expected_note_ids', []))
    if not expected:
        return 1.0
    retrieved = [c['note_id'] for c in result.get('context', {}).get('retrieved_chunks', [])][:k]
    import math
    dcg = sum(1.0 / math.log2(rank + 1) for rank, nid in enumerate(retrieved, 1) if nid in expected)
    ideal = sum(1.0 / math.log2(rank + 1) for rank in range(1, min(len(expected), k) + 1))
    return dcg / ideal if ideal > 0 else 0.0

for r in results:
    r['_recall'] = compute_recall(r)
    r['_precision'] = compute_precision(r)
    r['_mrr'] = compute_mrr(r)
    r['_ndcg'] = compute_ndcg(r)
    r['_top_score'] = max((c['score'] for c in r['context']['retrieved_chunks']), default=0)
    r['_retrieval_ms'] = r.get('pipeline', {}).get('retrieval_ms', 0)
    r['_llm_ms'] = r.get('pipeline', {}).get('llm_ms', 0)
    r['_total_ms'] = r.get('pipeline', {}).get('total_ms', 0)

all_recalls = [r['_recall'] for r in results]
all_precs   = [r['_precision'] for r in results]
all_mrrs    = [r['_mrr'] for r in results]
all_ndcgs   = [r['_ndcg'] for r in results]
all_top     = [r['_top_score'] for r in results]
all_ret_ms  = [r['_retrieval_ms'] for r in results]
all_llm_ms  = [r['_llm_ms'] for r in results if r['_llm_ms'] > 0]
all_tot_ms  = [r['_total_ms'] for r in results]

print('=== COMPREHENSIVE RETRIEVAL METRICS ===')
print(f'Recall@8:      {statistics.mean(all_recalls):.4f} (sd={statistics.stdev(all_recalls):.4f})')
print(f'Precision@8:   {statistics.mean(all_precs):.4f} (sd={statistics.stdev(all_precs):.4f})')
print(f'MRR@8:         {statistics.mean(all_mrrs):.4f} (sd={statistics.stdev(all_mrrs):.4f})')
print(f'nDCG@8:        {statistics.mean(all_ndcgs):.4f} (sd={statistics.stdev(all_ndcgs):.4f})')
print(f'Avg Top Score: {statistics.mean(all_top):.4f}')

print()
cat_data = defaultdict(list)
for r in results:
    cat_data[r['category']].append(r)

print('=== PER-CATEGORY METRICS ===')
for cat in sorted(cat_data.keys()):
    items = cat_data[cat]
    recalls = [r['_recall'] for r in items]
    mrrs = [r['_mrr'] for r in items]
    ndcgs = [r['_ndcg'] for r in items]
    precs = [r['_precision'] for r in items]
    n = len(items)
    best_q = max(items, key=lambda x: x['_ndcg'])
    worst_q = min(items, key=lambda x: x['_ndcg'])
    bq = best_q['question'][:50]
    wq = worst_q['question'][:50]
    print(f'{cat}:')
    print(f'  n={n} recall={statistics.mean(recalls):.3f} prec={statistics.mean(precs):.3f} MRR={statistics.mean(mrrs):.3f} nDCG={statistics.mean(ndcgs):.3f}')
    print(f'  best: [{best_q["query_id"]}] nDCG={best_q["_ndcg"]:.3f} "{bq}"')
    print(f'  worst:[{worst_q["query_id"]}] nDCG={worst_q["_ndcg"]:.3f} "{wq}"')

sorted_by_ndcg = sorted(results, key=lambda x: x['_ndcg'])
print()
print('=== 10 LOWEST nDCG QUERIES ===')
for r in sorted_by_ndcg[:10]:
    q = r['question'][:60]
    expected = r.get('expected_note_ids', [])
    retrieved = [c['note_id'] for c in r['context']['retrieved_chunks']]
    print(f'  [{r["query_id"]}] nDCG={r["_ndcg"]:.3f} MRR={r["_mrr"]:.3f} recall={r["_recall"]:.3f}')
    print(f'    Q: {q}')
    print(f'    Expected: {expected}')
    print(f'    Retrieved: {retrieved}')

print()
print('=== 10 HIGHEST nDCG QUERIES ===')
for r in sorted_by_ndcg[-10:]:
    q = r['question'][:60]
    print(f'  [{r["query_id"]}] nDCG={r["_ndcg"]:.3f} MRR={r["_mrr"]:.3f} recall={r["_recall"]:.3f} top={r["_top_score"]:.3f}')
    print(f'    Q: {q}')

print()
ret_ms_sorted = sorted(all_ret_ms)
tot_ms_sorted = sorted(all_tot_ms)
print('=== LATENCY STATISTICS ===')
print(f'Retrieval: avg={statistics.mean(all_ret_ms):.1f}ms p50={ret_ms_sorted[len(ret_ms_sorted)//2]:.1f}ms p95={ret_ms_sorted[int(len(ret_ms_sorted)*0.95)]:.1f}ms max={max(all_ret_ms):.1f}ms')
print(f'Total:     avg={statistics.mean(all_tot_ms):.1f}ms p50={tot_ms_sorted[len(tot_ms_sorted)//2]:.1f}ms p95={tot_ms_sorted[int(len(tot_ms_sorted)*0.95)]:.1f}ms max={max(all_tot_ms):.1f}ms')

print()
print('=== ROOT CAUSE ANALYSIS ===')
zero_recall = [r for r in results if r['_recall'] == 0.0]
partial_recall = [r for r in results if 0 < r['_recall'] < 1.0]
perfect_recall = [r for r in results if r['_recall'] == 1.0]

print(f'retrieval_failure (zero recall):         {len(zero_recall)} ({len(zero_recall)/len(results)*100:.1f}%)')
print(f'  Examples: {[r["query_id"] for r in zero_recall]}')
print(f'partial_retrieval (partial recall):      {len(partial_recall)} ({len(partial_recall)/len(results)*100:.1f}%)')
print(f'perfect_retrieval:                       {len(perfect_recall)} ({len(perfect_recall)/len(results)*100:.1f}%)')
print(f'evaluator_failure (all 54 LLM calls):    54 (100.0%)')
print(f'  Cause: Gemini free-tier 15 RPM quota exhausted')

# difficulty breakdown
print()
diff_data = defaultdict(list)
for r in results:
    diff_data[r['difficulty']].append(r)
print('=== BY DIFFICULTY ===')
for diff in ['easy','medium','hard']:
    items = diff_data.get(diff, [])
    if not items: continue
    recalls = [r['_recall'] for r in items]
    ndcgs = [r['_ndcg'] for r in items]
    print(f'  {diff}: n={len(items)} recall={statistics.mean(recalls):.3f} nDCG={statistics.mean(ndcgs):.3f}')
