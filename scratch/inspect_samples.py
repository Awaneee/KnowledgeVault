import json, glob
from pathlib import Path

debug_dir = Path('evaluation_results/ask_debug')

for qid in ['mns_04', 'summ_01', 'fq_01', 'cmp_01', 'rem_05', 'comm_01', 'appt_02', 'summ_02', 'summ_03', 'summ_04']:
    f = list(debug_dir.glob(f'*{qid}*'))
    if not f:
        print(f'Not found: {qid}')
        continue
    with open(f[0]) as fh:
        r = json.load(fh)
    question = r['question']
    category = r['category']
    difficulty = r['difficulty']
    expected = r.get('expected_note_ids', [])
    chunks = r.get('context', {}).get('retrieved_chunks', [])
    retrieved_ids = [c['note_id'] for c in chunks]
    answer = r.get('pipeline', {}).get('answer', '')
    retrieval_only = r.get('pipeline', {}).get('retrieval_only', False)
    top_score = max((c['score'] for c in chunks), default=0)
    ref = r.get('reference_answer', '')
    
    print(f'=== {qid} ===')
    print(f'Q: {question}')
    print(f'Category: {category}  Difficulty: {difficulty}')
    print(f'Expected note IDs: {expected}')
    print(f'Retrieved note IDs: {retrieved_ids}')
    print(f'Top score: {top_score:.3f}  Retrieval-only: {retrieval_only}')
    print(f'Answer[:300]: {answer[:300]}')
    print(f'Reference[:200]: {ref[:200]}')
    print()
