
# KnowledgeVault — Category Analysis Report

> Generated after ingesting 1055 notes through the production pipeline.


## 1. Overall Statistics

| Metric | Value |
| --- | --- |
| Total Notes | 1055 |
| Organized | 1055 |
| Failed | 0 |
| Processing Success Rate | 100.0% |
| Total Categories | 50 |
| Category Cap (50) Reached | YES ⚠️ |
| Singleton Categories | 0 |
| Empty Categories | 0 |
| Avg Notes per Category | 21.1 |
| Max Notes in One Category | 242 |
| Fragmentation Rate | 0.0% |
| Category Reuse Rate | 100.0% |

### Fragmentation Rate Interpretation

0.0% fragmentation — **Excellent** — most categories absorb multiple notes. Strong reuse.

## 2. Assignment Method Distribution

| Method | Count | Percentage | Explanation |
| --- | --- | --- | --- |
| cap_fallback | 668 | 63.3% | Category cap (50) reached — forced into nearest category |
| canonical_name | 313 | 29.7% | Exact name match — highest confidence reuse |
| created | 45 | 4.3% | New category created — no suitable existing category found |
| exact_rule | 29 | 2.7% | Rule-based match (intent type + actor) — reliable for communication |

## 3. Intent Type Distribution

| Intent Type | Categories | Category Names |
| --- | --- | --- |
| study | 20 | `Study - NLP Models`, `Study - Graph Algorithms`, `Study - Knowledge Vault`, `Study - Operating Systems`, `Study - Kubernetes`... |
| general | 7 | `Reduce`, `Print`, `Flutter Application Performance.`, `AI`, `Kubernetes`... |
| question | 5 | `Questions - Python`, `Questions - PostgreSQL`, `Questions - Factory`, `Questions - Ego`, `Questions - Philosophy` |
| idea | 4 | `Ideas - AI`, `Ideas - Semantic Retrieval`, `Ideas - AI Summarization`, `Ideas - Leetcode` |
| reference | 4 | `Reference - PostgreSQL`, `Reference - Docker`, `Reference - Redis`, `Reference - Knowledgevault Backend` |
| todo | 4 | `Bills`, `Shopping`, `Tasks`, `Travel` |
| communication | 2 | `Communication - Sid`, `Communication - Siddhant` |
| event | 2 | `Meetings`, `Meetings - Knowledgevault Team` |
| reminder | 2 | `Reminders`, `Appointments` |

## 4. Top 15 Categories by Note Count

| Rank | Category Name | Intent Type | Notes |
| --- | --- | --- | --- |
| 1 | Tasks | todo | 242 |
| 2 | Questions - Python | question | 40 |
| 3 | Flutter Application Performance. | general | 39 |
| 4 | Study - Sqlalchemy | study | 38 |
| 5 | Reference - Redis | reference | 37 |
| 6 | Questions - PostgreSQL | question | 30 |
| 7 | Study - API Performance | study | 28 |
| 8 | Study - Cross-encoder Reranking | study | 27 |
| 9 | Study - Flutter | study | 27 |
| 10 | Study - NLP Models | study | 25 |
| 11 | Study - System Design | study | 25 |
| 12 | Study - Event-driven Architecture | study | 23 |
| 13 | Reference - Knowledgevault Backend | reference | 23 |
| 14 | Study - Graph Algorithms | study | 22 |
| 15 | Study - FastAPI | study | 22 |

## 5. Duplicate Category Detection

**4 duplicate name patterns detected.** These indicate categories that should have been reused but weren't.

| Stem / Key | Duplicate Category Names |
| --- | --- |
| postgresql | `Reference - PostgreSQL` / `Study - PostgreSQL` |
| kubernetes | `Study - Kubernetes` / `Kubernetes` |
| ai | `Study - AI` / `AI` |
| redis | `Study - Redis` / `Reference - Redis` |

**Why this happens:** The category naming system generates a string from intent metadata. If the LLM extracts slightly different topics for two similar notes (e.g., 'PostgreSQL' vs 'Postgres'), the canonical name match fails and a new category is created. This is the system's primary fragmentation mechanism.

## 6. Suspicious Categories

**1 suspiciously generic categories detected:**

- `Tasks`

**Why they exist:** When the intent classifier cannot extract a meaningful topic, the category name falls back to a broad intent-type label (e.g., 'Study', 'General', 'Tasks'). These categories absorb notes that couldn't be more specifically classified.

## 7. Category Cap Analysis

⚠️ **The 50-category cap has been reached.** All subsequent notes are assigned to the nearest existing category using `cap_fallback` method, regardless of semantic compatibility.

**Impact:** Notes that would have created new specific categories are now lumped into the closest existing one. This **inflates** category reuse metrics while **reducing** categorization precision. The effective reuse rate after cap is not genuine reuse — it is forced assignment.

**Recommendation:** If the dataset has grown significantly beyond 50 natural topic clusters, raise `MAX_CATEGORIES_PER_USER` in `IntentCategoryService`. The current limit was set for personal use (50 notes), not for 1000+ notes.

## 8. Complete Category Listing

| ID | Category Name | Intent Type | Notes | Has Actor |
| --- | --- | --- | --- | --- |
| 114 | AI | general | 18 | Yes |
| 88 | Appointments | reminder | 4 | No |
| 87 | Bills | todo | 20 | No |
| 66 | Communication - Sid | communication | 17 | Yes |
| 68 | Communication - Siddhant | communication | 6 | Yes |
| 104 | Flutter Application Performance. | general | 39 | No |
| 110 | Id | general | 10 | Yes |
| 91 | Ideas - AI | idea | 11 | No |
| 93 | Ideas - AI Summarization | idea | 13 | No |
| 112 | Ideas - Leetcode | idea | 10 | Yes |
| 92 | Ideas - Semantic Retrieval | idea | 20 | No |
| 113 | Kubernetes | general | 22 | Yes |
| 102 | Meetings | event | 13 | No |
| 103 | Meetings - Knowledgevault Team | event | 18 | Yes |
| 107 | Print | general | 7 | Yes |
| 109 | Questions - Ego | question | 3 | No |
| 115 | Questions - Factory | question | 17 | Yes |
| 111 | Questions - Philosophy | question | 9 | Yes |
| 101 | Questions - PostgreSQL | question | 30 | No |
| 105 | Questions - Python | question | 40 | Yes |
| 106 | Reduce | general | 6 | Yes |
| 83 | Reference - Docker | reference | 15 | No |
| 98 | Reference - Knowledgevault Backend | reference | 23 | No |
| 85 | Reference - PostgreSQL | reference | 16 | No |
| 84 | Reference - Redis | reference | 37 | No |
| 67 | Reminders | reminder | 17 | Yes |
| 108 | Rs | general | 12 | Yes |
| 86 | Shopping | todo | 2 | No |
| 76 | Study - AI | study | 7 | No |
| 97 | Study - API Performance | study | 28 | No |
| 78 | Study - Cross-encoder Reranking | study | 27 | No |
| 100 | Study - Event-driven Architecture | study | 23 | No |
| 79 | Study - FastAPI | study | 22 | No |
| 99 | Study - Flutter | study | 27 | No |
| 71 | Study - Graph Algorithms | study | 22 | No |
| 74 | Study - JWT Authentication | study | 16 | No |
| 82 | Study - Kafka | study | 8 | No |
| 96 | Study - Knowledge Vault | study | 13 | No |
| 94 | Study - Knowledgeretrievalsystems | study | 19 | No |
| 73 | Study - Kubernetes | study | 19 | No |
| 75 | Study - NLP Models | study | 25 | No |
| 70 | Study - Operating Systems | study | 10 | No |
| 69 | Study - PostgreSQL | study | 9 | No |
| 72 | Study - Redis | study | 2 | No |
| 95 | Study - Semantic Search | study | 9 | No |
| 80 | Study - Sqlalchemy | study | 38 | No |
| 81 | Study - System Design | study | 25 | No |
| 77 | Study - Vector Databases | study | 5 | No |
| 90 | Tasks | todo | 242 | No |
| 89 | Travel | todo | 4 | No |

## 9. Recommendations

1. **Category cap hit**: Raise `MAX_CATEGORIES_PER_USER` to 100 for large datasets. Current cap forces misclassification via `cap_fallback`.
2. **4 duplicate stems**: Review topic synonym mappings in `IntentCategoryService.TOPIC_SYNONYMS`. Common culprit: 'postgres' vs 'postgresql', 'redis cache' vs 'redis'.