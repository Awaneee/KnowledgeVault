
# KnowledgeVault — Category Analysis Report

> Generated after ingesting 1055 notes through the production pipeline.


## 1. Overall Statistics

| Metric | Value |
| --- | --- |
| Total Notes | 1055 |
| Organized | 1055 |
| Failed | 0 |
| Processing Success Rate | 100.0% |
| Total Categories | 105 |
| Category Cap (50) Reached | YES ⚠️ |
| Singleton Categories | 69 |
| Empty Categories | 0 |
| Avg Notes per Category | 5.05 |
| Max Notes in One Category | 229 |
| Fragmentation Rate | 65.7% |
| Category Reuse Rate | 34.3% |

### Fragmentation Rate Interpretation

65.7% fragmentation — **Poor** — over half of categories hold only one note. Category naming is too specific.

## 2. Assignment Method Distribution

| Method | Count | Percentage | Explanation |
| --- | --- | --- | --- |
| canonical_name | 420 | 79.2% | Exact name match — highest confidence reuse |
| created | 104 | 19.6% | New category created — no suitable existing category found |
| general_catchall | 6 | 1.1% | Other |

## 3. Intent Type Distribution

| Intent Type | Categories | Category Names |
| --- | --- | --- |
| general | 37 | `General`, `Flutter UI Knowledgevault`, `Backend Service Layer`, `Flutter Application Performance`, `Distributed Systems Interview`... |
| study | 20 | `Study - Knowledgeretrievalsystems`, `Study - Operating Systems`, `Study - Graph Algorithms`, `Study - Kubernetes`, `Study - JWT Authentication`... |
| question | 18 | `Questions - Nginx`, `Questions - Diameter`, `Questions - Python`, `Questions - Ego`, `Questions - Philosophy`... |
| communication | 8 | `Communication - Siddhant`, `Communication - Sid`, `Communication - Python`, `Communication - Mock`, `Communication - Show`... |
| idea | 8 | `Ideas - AI`, `Ideas - Semantic Retrieval`, `Ideas - AI Summarization`, `Ideas - Leetcode`, `Ideas - India`... |
| todo | 6 | `Tasks`, `Travel`, `Shopping`, `Bills`, `Health`... |
| reference | 5 | `Reference - Docker`, `Reference - PostgreSQL`, `Reference - Redis`, `Reference - Knowledgevault Backend`, `Reference - Shared` |
| reminder | 2 | `Appointments`, `Reminders` |
| event | 1 | `Meetings - Social` |

## 4. Top 15 Categories by Note Count

| Rank | Category Name | Intent Type | Notes |
| --- | --- | --- | --- |
| 1 | Tasks | todo | 229 |
| 2 | General | general | 38 |
| 3 | Questions - Python | question | 23 |
| 4 | FastAPI | general | 15 |
| 5 | Questions | question | 10 |
| 6 | Docker | general | 8 |
| 7 | Communication - Python | communication | 8 |
| 8 | Questions - Nginx | question | 8 |
| 9 | Reference - Redis | reference | 7 |
| 10 | Reminders | reminder | 7 |
| 11 | Errands | todo | 7 |
| 12 | Bills | todo | 6 |
| 13 | API | general | 6 |
| 14 | Cross | general | 6 |
| 15 | Questions - Factory | question | 6 |

## 5. Duplicate Category Detection

**6 duplicate name patterns detected.** These indicate categories that should have been reused but weren't.

| Stem / Key | Duplicate Category Names |
| --- | --- |
| docker | `Reference - Docker` / `Docker` |
| kubernetes | `Study - Kubernetes` / `Kubernetes` |
| ai | `Study - AI` / `AI` |
| fastapi | `Study - FastAPI` / `FastAPI` |
| postgresql | `Reference - PostgreSQL` / `Study - PostgreSQL` |
| redis | `Reference - Redis` / `Study - Redis` |

**Why this happens:** The category naming system generates a string from intent metadata. If the LLM extracts slightly different topics for two similar notes (e.g., 'PostgreSQL' vs 'Postgres'), the canonical name match fails and a new category is created. This is the system's primary fragmentation mechanism.

## 6. Suspicious Categories

**2 suspiciously generic categories detected:**

- `Tasks`
- `General`

**Why they exist:** When the intent classifier cannot extract a meaningful topic, the category name falls back to a broad intent-type label (e.g., 'Study', 'General', 'Tasks'). These categories absorb notes that couldn't be more specifically classified.

## 7. Category Cap Analysis

⚠️ **The 50-category cap has been reached.** All subsequent notes are assigned to the nearest existing category using `cap_fallback` method, regardless of semantic compatibility.

**Impact:** Notes that would have created new specific categories are now lumped into the closest existing one. This **inflates** category reuse metrics while **reducing** categorization precision. The effective reuse rate after cap is not genuine reuse — it is forced assignment.

**Recommendation:** If the dataset has grown significantly beyond 50 natural topic clusters, raise `MAX_CATEGORIES_PER_USER` in `IntentCategoryService`. The current limit was set for personal use (50 notes), not for 1000+ notes.

## 8. Complete Category Listing

| ID | Category Name | Intent Type | Notes | Has Actor |
| --- | --- | --- | --- | --- |
| 213 | AI | general | 4 | Yes |
| 247 | API | general | 6 | Yes |
| 238 | Alembic | general | 5 | Yes |
| 252 | Also | general | 1 | Yes |
| 231 | Always | general | 1 | Yes |
| 189 | Appointments | reminder | 1 | No |
| 203 | Backend Service Layer | general | 1 | No |
| 188 | Bills | todo | 6 | No |
| 220 | Booked | general | 1 | Yes |
| 259 | Common | general | 1 | Yes |
| 234 | Communication - Ask | communication | 2 | Yes |
| 260 | Communication - Microsoft | communication | 1 | Yes |
| 218 | Communication - Mock | communication | 1 | Yes |
| 245 | Communication - Python | communication | 8 | Yes |
| 228 | Communication - Show | communication | 1 | Yes |
| 167 | Communication - Sid | communication | 3 | Yes |
| 169 | Communication - Siddhant | communication | 2 | Yes |
| 223 | Communication - Unprocessable | communication | 6 | Yes |
| 215 | Cross | general | 6 | Yes |
| 227 | Crucial | general | 1 | Yes |
| 239 | Danger | general | 1 | Yes |
| 221 | Distillation | general | 1 | Yes |
| 202 | Distributed Systems Interview | general | 1 | No |
| 226 | Docker | general | 8 | Yes |
| 258 | Embeddings | general | 1 | Yes |
| 250 | Errands | todo | 7 | Yes |
| 204 | Event-driven Architecture Patterns | general | 1 | No |
| 224 | Expressions Cheat `.` | general | 1 | Yes |
| 230 | FastAPI | general | 15 | Yes |
| 201 | Flutter Application Performance | general | 1 | No |
| 200 | Flutter UI Knowledgevault | general | 1 | No |
| 206 | From Backend Architecture | general | 1 | No |
| 205 | General | general | 38 | No |
| 244 | Health | todo | 1 | Yes |
| 192 | Ideas - AI | idea | 1 | No |
| 194 | Ideas - AI Summarization | idea | 1 | No |
| 229 | Ideas - AI Writing | idea | 1 | Yes |
| 248 | Ideas - API Monetization | idea | 1 | Yes |
| 222 | Ideas - India | idea | 1 | Yes |
| 211 | Ideas - Leetcode | idea | 1 | Yes |
| 236 | Ideas - Redis | idea | 1 | Yes |
| 193 | Ideas - Semantic Retrieval | idea | 1 | No |
| 241 | Instead | general | 1 | Yes |
| 235 | Isolation | general | 1 | Yes |
| 212 | Kubernetes | general | 5 | Yes |
| 254 | Leetcode | general | 4 | Yes |
| 262 | Meetings - Social | event | 1 | Yes |
| 255 | Migration `alembic Revision | general | 6 | Yes |
| 267 | Navigable | general | 6 | Yes |
| 249 | Nginx | general | 1 | Yes |
| 264 | None | general | 5 | No |
| 242 | Parameter | general | 1 | Yes |
| 271 | Questions | question | 10 | Yes |
| 225 | Questions - API | question | 2 | Yes |
| 263 | Questions - Apply | question | 1 | Yes |
| 237 | Questions - Diameter | question | 5 | Yes |
| 257 | Questions - Don T | question | 1 | Yes |
| 209 | Questions - Ego | question | 1 | No |
| 214 | Questions - Factory | question | 6 | Yes |
| 269 | Questions - Memory | question | 1 | Yes |
| 265 | Questions - Monthly | question | 1 | Yes |
| 243 | Questions - Movie | question | 1 | Yes |
| 232 | Questions - Nginx | question | 8 | Yes |
| 256 | Questions - Ola | question | 1 | Yes |
| 210 | Questions - Philosophy | question | 1 | Yes |
| 261 | Questions - Preventing | question | 1 | Yes |
| 208 | Questions - Python | question | 23 | Yes |
| 216 | Questions - Ssd | question | 1 | Yes |
| 233 | Questions - Targets Are | question | 1 | Yes |
| 268 | Questions - Typescript | question | 5 | Yes |
| 246 | React | general | 2 | Yes |
| 253 | Realm | general | 1 | Yes |
| 184 | Reference - Docker | reference | 2 | No |
| 199 | Reference - Knowledgevault Backend | reference | 1 | No |
| 186 | Reference - PostgreSQL | reference | 1 | No |
| 185 | Reference - Redis | reference | 7 | No |
| 217 | Reference - Shared | reference | 1 | Yes |
| 168 | Reminders | reminder | 7 | Yes |
| 251 | Semantic | general | 1 | Yes |
| 187 | Shopping | todo | 2 | No |
| 177 | Study - AI | study | 1 | No |
| 198 | Study - API Performance | study | 1 | No |
| 179 | Study - Cross-encoder Reranking | study | 1 | No |
| 180 | Study - FastAPI | study | 1 | No |
| 172 | Study - Graph Algorithms | study | 1 | No |
| 175 | Study - JWT Authentication | study | 1 | No |
| 183 | Study - Kafka | study | 1 | No |
| 197 | Study - Knowledge Vault | study | 1 | No |
| 195 | Study - Knowledgeretrievalsystems | study | 1 | No |
| 174 | Study - Kubernetes | study | 1 | No |
| 176 | Study - NLP Models | study | 1 | No |
| 171 | Study - Operating Systems | study | 1 | No |
| 240 | Study - Pipelining | study | 1 | Yes |
| 170 | Study - PostgreSQL | study | 2 | No |
| 173 | Study - Redis | study | 2 | No |
| 196 | Study - Semantic Search | study | 1 | No |
| 181 | Study - Sqlalchemy | study | 1 | No |
| 182 | Study - System Design | study | 1 | No |
| 178 | Study - Vector Databases | study | 1 | No |
| 266 | Study - Writing | study | 1 | Yes |
| 207 | Summary Weekly Knowledgevault | general | 1 | No |
| 191 | Tasks | todo | 229 | No |
| 190 | Travel | todo | 1 | No |
| 270 | Typescript | general | 2 | Yes |
| 219 | Window Maximum Sum | general | 5 | Yes |

## 9. Recommendations

1. **High fragmentation**: Lower `CATEGORY_INGEST_THRESHOLD` from 0.40 to 0.35 to encourage more category reuse. Run backfill after changing.
2. **Category cap hit**: Raise `MAX_CATEGORIES_PER_USER` to 100 for large datasets. Current cap forces misclassification via `cap_fallback`.
3. **6 duplicate stems**: Review topic synonym mappings in `IntentCategoryService.TOPIC_SYNONYMS`. Common culprit: 'postgres' vs 'postgresql', 'redis cache' vs 'redis'.