import json, glob, statistics
from pathlib import Path
from collections import Counter, defaultdict

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

for r in results:
    r['_recall'] = compute_recall(r)
    r['_retrieval_only'] = r.get('pipeline', {}).get('retrieval_only', False)
    r['_answer'] = r.get('pipeline', {}).get('answer', '')
    r['_status'] = r.get('pipeline', {}).get('status', '')
    r['_retrieval_ms'] = r.get('pipeline', {}).get('retrieval_ms', 0)
    r['_llm_ms'] = r.get('pipeline', {}).get('llm_ms', 0)
    r['_total_ms'] = r.get('pipeline', {}).get('total_ms', 0)
    r['_top_score'] = max((c['score'] for c in r['context']['retrieved_chunks']), default=0)
    r['_chunks'] = r['context']['retrieved_chunks']

recalls = [r['_recall'] for r in results]
print('=== RETRIEVAL ANALYSIS (54 queries) ===')
print(f'Perfect recall (1.0): {sum(1 for x in recalls if x == 1.0)} ({sum(1 for x in recalls if x == 1.0)/len(recalls)*100:.1f}%)')
print(f'Partial recall:       {sum(1 for x in recalls if 0 < x < 1.0)} ({sum(1 for x in recalls if 0 < x < 1.0)/len(recalls)*100:.1f}%)')
print(f'Zero recall:          {sum(1 for x in recalls if x == 0.0)} ({sum(1 for x in recalls if x == 0.0)/len(recalls)*100:.1f}%)')
print(f'Mean recall:          {statistics.mean(recalls):.3f}')

ro_count = sum(1 for r in results if r['_retrieval_only'])
print(f'\nRetrieval-only responses (all LLM providers exhausted): {ro_count}/54')

cat_recall = defaultdict(list)
for r in results:
    cat_recall[r['category']].append(r['_recall'])

print('\n=== PER-CATEGORY RECALL ===')
for cat, vals in sorted(cat_recall.items()):
    perfect = sum(1 for v in vals if v==1.0)
    print(f'  {cat:<25} n={len(vals)} recall={statistics.mean(vals):.3f} perfect={perfect}')

top_scores = [r['_top_score'] for r in results]
print(f'\n=== TOP RETRIEVAL SCORE DISTRIBUTION ===')
print(f'Mean top score:  {statistics.mean(top_scores):.3f}')
print(f'Min top score:   {min(top_scores):.3f}')
print(f'Max top score:   {max(top_scores):.3f}')
print(f'Scores >= 0.7:   {sum(1 for s in top_scores if s >= 0.7)} queries')
print(f'Scores 0.4-0.7:  {sum(1 for s in top_scores if 0.4 <= s < 0.7)} queries')
print(f'Scores < 0.4:    {sum(1 for s in top_scores if s < 0.4)} queries')

ret_ms = [r['_retrieval_ms'] for r in results if r['_retrieval_ms']]
llm_ms = [r['_llm_ms'] for r in results if r['_llm_ms']]
total_ms = [r['_total_ms'] for r in results if r['_total_ms']]
print('\n=== LATENCY (ms) ===')
print(f'Retrieval: avg={statistics.mean(ret_ms):.1f}  p50={sorted(ret_ms)[len(ret_ms)//2]:.1f}  max={max(ret_ms):.1f}')
print(f'LLM:       avg={statistics.mean(llm_ms):.1f}  p50={sorted(llm_ms)[len(llm_ms)//2]:.1f}  max={max(llm_ms):.1f}')
print(f'Total:     avg={statistics.mean(total_ms):.1f}  p50={sorted(total_ms)[len(total_ms)//2]:.1f}  max={max(total_ms):.1f}')

# Zero recall
print('\n=== ZERO RECALL QUERIES ===')
zero_recall = [r for r in results if r['_recall'] == 0.0]
for r in zero_recall:
    expected = r.get('expected_note_ids', [])
    retrieved = [c['note_id'] for c in r['_chunks']]
    qid = r['query_id']
    q = r['question'][:60]
    ts = r['_top_score']
    print(f'  [{qid}] {q}')
    print(f'    Expected: {expected}  Retrieved: {retrieved[:5]}  TopScore: {ts:.3f}')

print('\n=== BEST RETRIEVAL (recall=1.0, top>=0.5) ===')
best = sorted([r for r in results if r['_recall'] == 1.0 and r['_top_score'] >= 0.5], key=lambda x: -x['_top_score'])
for r in best[:10]:
    qid = r['query_id']
    ts = r['_top_score']
    cat = r['category']
    q = r['question'][:55]
    print(f'  [{qid}] top={ts:.3f} cat={cat} q={q}')

# Save sorted for scoring selection
best_ids = [r['query_id'] for r in best[:10]]
worst_ids = [r['query_id'] for r in zero_recall[:5]]
score_targets = list(dict.fromkeys(best_ids + worst_ids))  # dedup, preserve order
print('\n=== SCORING TARGETS ===')
print(score_targets)

# Token estimates
total_prompt_tokens = sum(len(r.get('context', {}).get('prompt', '')) // 4 for r in results)
total_compl_tokens = sum(100 for r in results)  # ~100 tokens per answer
print(f'\nEstimated prompt tokens total: {total_prompt_tokens:,}')
print(f'Estimated completion tokens total: {total_compl_tokens:,}')
print(f'Gemini Flash input cost ($0.075/1M): ${total_prompt_tokens * 0.075 / 1_000_000:.6f}')
print(f'Gemini Flash output cost ($0.30/1M): ${total_compl_tokens * 0.30 / 1_000_000:.6f}')
