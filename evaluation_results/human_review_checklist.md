# Benchmark v2.0.0 — Human Review Checklist

Auto-generated from 205-entry verified.json.  
140 entries need NO review.  
65 entries are flagged below.

---

## HIGH PRIORITY — Relevance set review (18 entries)

These challenges are structurally invalid for keyword-union annotation:
- `comparison`: union(A ∪ B) ≠ notes that address A vs B
- `multi_hop`: topic-union may include tangential notes
- `temporal`: keyword match ignores actual dates in notes

**Action per entry:** Open verified.json, inspect each `relevant_note_ids`.
Remove notes that only discuss one side of a comparison, or are
temporally stale. Update `graded_relevance` accordingly.

### H01. [COMPARISON] Docker vs Kubernetes — what is the difference?
- **Difficulty**: hard  |  **n_relevant**: 8
- **Note IDs to verify**: [72, 105, 75, 118, 410, 91, 62, 383]
- **Concern**: keyword-union cannot verify that each of the 8 notes actually addresses this query

### H02. [COMPARISON] Redis vs Kafka — when to use each
- **Difficulty**: hard  |  **n_relevant**: 6
- **Note IDs to verify**: [1024, 771, 1027, 773, 520, 1034]
- **Concern**: keyword-union cannot verify that each of the 6 notes actually addresses this query

### H03. [COMPARISON] Redis vs PostgreSQL — when to use each for persistence?
- **Difficulty**: hard  |  **n_relevant**: 8
- **Note IDs to verify**: [103, 104, 73, 74, 139, 58, 92, 61]
- **Concern**: keyword-union cannot verify that each of the 8 notes actually addresses this query

### H04. [COMPARISON] When should I use GIN vs B-tree indexes?
- **Difficulty**: hard  |  **n_relevant**: 8
- **Note IDs to verify**: [58, 66, 74, 104, 113, 114, 136, 139]
- **Concern**: keyword-union cannot verify that each of the 8 notes actually addresses this query

### H05. [MULTI_HOP] How do I decide between hybrid retrieval and cross-encoder reranking?
- **Difficulty**: hard  |  **n_relevant**: 8
- **Note IDs to verify**: [65, 67, 176, 114, 86, 119, 88, 123]
- **Concern**: keyword-union cannot verify that each of the 8 notes actually addresses this query

### H06. [MULTI_HOP] KnowledgeVault RAG pipeline decisions and findings
- **Difficulty**: hard  |  **n_relevant**: 8
- **Note IDs to verify**: [1028, 262, 1030, 1032, 523, 267, 533, 1053]
- **Concern**: keyword-union cannot verify that each of the 8 notes actually addresses this query

### H07. [MULTI_HOP] RAG and retrieval evaluation metrics
- **Difficulty**: hard  |  **n_relevant**: 8
- **Note IDs to verify**: [90, 119, 210, 310, 402, 485, 487, 595]
- **Concern**: keyword-union cannot verify that each of the 8 notes actually addresses this query

### H08. [MULTI_HOP] What benchmark results have I recorded for KnowledgeVault retrieval?
- **Difficulty**: hard  |  **n_relevant**: 8
- **Note IDs to verify**: [1028, 262, 1032, 523, 402, 413, 1053, 928]
- **Concern**: keyword-union cannot verify that each of the 8 notes actually addresses this query

### H09. [MULTI_HOP] What decisions have I made for the KnowledgeVault project?
- **Difficulty**: medium  |  **n_relevant**: 10
- **Note IDs to verify**: [57, 88, 89, 90, 91, 94, 95, 96, 97, 107]
- **Concern**: keyword-union cannot verify that each of the 10 notes actually addresses this query

### H10. [MULTI_HOP] What have I documented about retrieval quality in KnowledgeVault?
- **Difficulty**: hard  |  **n_relevant**: 8
- **Note IDs to verify**: [89, 485, 487, 402, 595, 88, 57, 90]
- **Concern**: keyword-union cannot verify that each of the 8 notes actually addresses this query

### H11. [MULTI_HOP] What is the architecture of my main project?
- **Difficulty**: hard  |  **n_relevant**: 8
- **Note IDs to verify**: [57, 88, 89, 90, 91, 94, 95, 96]
- **Concern**: keyword-union cannot verify that each of the 8 notes actually addresses this query

### H12. [TEMPORAL] My upcoming travel and trip bookings
- **Difficulty**: easy  |  **n_relevant**: 8
- **Note IDs to verify**: [78, 81, 115, 126, 128, 130, 160, 171]
- **Concern**: keyword-union cannot verify that each of the 8 notes actually addresses this query

### H13. [TEMPORAL] Recent notes and activities
- **Difficulty**: hard  |  **n_relevant**: 6
- **Note IDs to verify**: [77, 149, 164, 182, 286, 341]
- **Concern**: keyword-union cannot verify that each of the 6 notes actually addresses this query

### H14. [TEMPORAL] Tasks I need to complete before month end
- **Difficulty**: hard  |  **n_relevant**: 6
- **Note IDs to verify**: [184, 233, 368, 469, 478, 498]
- **Concern**: keyword-union cannot verify that each of the 6 notes actually addresses this query

### H15. [TEMPORAL] Upcoming deadlines and submission dates
- **Difficulty**: medium  |  **n_relevant**: 6
- **Note IDs to verify**: [184, 233, 368, 469, 478, 498]
- **Concern**: keyword-union cannot verify that each of the 6 notes actually addresses this query

### H16. [TEMPORAL] What appointments have I booked this month?
- **Difficulty**: medium  |  **n_relevant**: 6
- **Note IDs to verify**: [78, 109, 128, 226, 231, 559]
- **Concern**: keyword-union cannot verify that each of the 6 notes actually addresses this query

### H17. [TEMPORAL] What have I been working on this month?
- **Difficulty**: hard  |  **n_relevant**: 6
- **Note IDs to verify**: [77, 149, 164, 182, 286, 341]
- **Concern**: keyword-union cannot verify that each of the 6 notes actually addresses this query

### H18. [TEMPORAL] What is due this week?
- **Difficulty**: medium  |  **n_relevant**: 6
- **Note IDs to verify**: [184, 233, 368, 469, 478, 498]
- **Concern**: keyword-union cannot verify that each of the 6 notes actually addresses this query

---

## MEDIUM PRIORITY — Synthesis completeness spot-check (5 entries)

'All my X notes' queries: the keyword match may have missed relevant notes
or included tangential ones.

**Action per entry:** Check that the listed notes are genuinely in the X category.
Add any obviously missing notes. 2–3 minutes total.

### M01. All my brainstorming and ideation notes
- **n_relevant**: 8  |  **Note IDs**: [85, 86, 117, 143, 157, 178, 225, 240]

### M02. All my communication and message drafts
- **n_relevant**: 6  |  **Note IDs**: [54, 56, 57, 106, 132, 141]

### M03. All my university and course study notes
- **n_relevant**: 8  |  **Note IDs**: [58, 61, 62, 66, 69, 122, 130, 131]

### M04. My study notes on AI and machine learning
- **n_relevant**: 8  |  **Note IDs**: [1026, 774, 1030, 510, 523, 268, 267, 782]

### M05. My technical reference cheat sheets
- **n_relevant**: 6  |  **Note IDs**: [72, 73, 74, 75, 122, 135]

---

## LOW PRIORITY — Grade promotion (42 entries)

These are all from the v1.0.0 binary-relevance migration.
All notes are grade-1. At least one should be promoted to grade-2
(the note that most directly answers the query).

**Action per entry:** Identify the primary answer note. Change its
`graded_relevance` score from `1` → `2`. ~10 seconds each.
Total estimated time: 7–10 minutes.

| # | Query | n | Note IDs |
|---|-------|---|----------|
| L01 | Bills to pay | 2 | [77, 82] |
| L02 | Brainstorming app names | 4 | [85, 86, 87, 88] |
| L03 | Budget and monthly expenses | 2 | [82, 77] |
| L04 | Docker commands cheat sheet | 2 | [72, 75] |
| L05 | Doctor appointment | 2 | [78, 79] |
| L06 | Documentation tasks | 2 | [96, 95] |
| L07 | Evaluation report work | 2 | [90, 89] |
| L08 | Flutter improvements | 2 | [97, 98] |
| L09 | Health checkup and appointments | 3 | [78, 79, 80] |
| L10 | How can I improve my health? | 2 | [83, 84] |
| L11 | How does Redis eviction work? | 3 | [103, 73, 61] |
| L12 | Ideas for improving KnowledgeVault | 5 | [86, 87, 88, 89]… |
| L13 | Ideas for my new blog post | 4 | [85, 86, 87, 88] |
| L14 | Improve search latency | 2 | [93, 89] |
| L15 | Interview preparation | 2 | [70, 99] |
| L16 | Markdown support | 4 | [72, 73, 74, 75] |
| L17 | Meeting notes from Q3 planning | 2 | [106, 107] |
| L18 | Message to send to Siddhant about backend | 3 | [56, 57, 54] |
| L19 | Networking concepts | 2 | [71, 62] |
| L20 | Next meeting with the design team | 2 | [106, 107] |
| L21 | Object oriented programming revision | 2 | [59, 60] |
| L22 | Portfolio website | 2 | [100, 97] |
| L23 | Project deadline for the alpha release | 2 | [89, 91] |
| L24 | Questions to ask during the interview | 2 | [70, 99] |
| L25 | Redis and PostgreSQL reference notes | 3 | [73, 74, 58] |
| L26 | Remind me to call mom | 2 | [78, 79] |
| L27 | Reminders for next week | 5 | [76, 77, 78, 79]… |
| L28 | Show my AI research reading goals | 4 | [65, 64, 66, 67] |
| L29 | Show my finance reminders | 2 | [77, 82] |
| L30 | Sprint planning meeting summary | 2 | [107, 106] |
| L31 | Study materials for machine learning | 4 | [64, 65, 66, 67] |
| L32 | Study schedule for finals | 4 | [58, 59, 60, 61] |
| L33 | System design interview study | 4 | [70, 99, 59, 60] |
| L34 | Tell Sid about the hackathon | 2 | [55, 54] |
| L35 | Things I need to tell Sid | 4 | [54, 55, 56, 57] |
| L36 | Things to discuss with Sid at the next meeting | 4 | [54, 55, 56, 57] |
| L37 | Timeline for the beta launch | 2 | [89, 91] |
| L38 | Weekly sync notes | 2 | [106, 107] |
| L39 | What are PostgreSQL index types? | 3 | [104, 74, 58] |
| L40 | What are the project requirements for KnowledgeVault? | 8 | [89, 90, 91, 92]… |
| L41 | What is the theory of relativity? | 3 | [103, 104, 105] |
| L42 | What startup ideas do I have? | 3 | [85, 86, 87] |

---

## Effort Estimate

| Tier | Entries | Time/entry | Total |
|------|---------|------------|-------|
| HIGH | 18 | ~2–3 min | ~45 min |
| MEDIUM | 5 | ~1 min | ~5 min |
| LOW | 42 | ~10 sec | ~7 min |
| **Total** | **65** | | **~57 min** |

After completing this checklist, run:
```bash
python scripts/evaluate.py  # regenerate baseline metrics
python scripts/generate_dashboard.py  # rebuild dashboard
# Then bump version → v2.0.0 and freeze
```