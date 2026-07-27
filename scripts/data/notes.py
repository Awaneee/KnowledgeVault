"""
~1000 realistic notes written from the perspective of a final-year CS engineering
student (Thapar University, BE 2023 batch) who builds backend projects,
prepares for tech interviews, and keeps a personal knowledge base.

Organized by domain but intentionally interleaved in NOTES list so the
ingestion pipeline sees a realistic mixed-topic stream rather than clean batches.
"""

# fmt: off
_PROGRAMMING = [
    "Python dict comprehension is faster than looping and calling dict.update(). Benchmark: 2.3x speedup for 10k items.",
    "Use `__slots__` in Python classes when creating thousands of instances — reduces memory by ~40% by skipping the per-instance __dict__.",
    "Learned about Python's GIL today. CPU-bound tasks need multiprocessing, not threading. I/O-bound tasks are fine with asyncio or threading.",
    "JavaScript `Promise.all` fails fast — if one promise rejects, the whole thing rejects. Use `Promise.allSettled` when you need all results regardless of failures.",
    "TypeScript `as const` assertion is underused. It narrows the type to the literal value and prevents accidental mutation in arrays and objects.",
    "Git rebase vs merge: rebase rewrites history for a linear log, merge preserves the branch structure. Use rebase for feature branches before PR, never on shared branches.",
    "Learned about Go goroutines today. They're lighter than threads — can spawn millions. The scheduler is M:N (goroutines mapped to OS threads).",
    "Rust ownership rules: each value has exactly one owner, when the owner goes out of scope the value is dropped. Borrowing with & gives a reference without moving.",
    "Factory pattern: create objects through a factory method rather than direct instantiation. Useful when the exact type isn't known until runtime.",
    "Strategy pattern: define a family of algorithms, encapsulate each one, make them interchangeable. Classic example: sorting with different comparators.",
    "Observer pattern is basically pub-sub. Subject notifies all registered observers when state changes. Event systems in React/DOM are built on this.",
    "Python's `contextlib.suppress(Exception)` is cleaner than a try/except that does nothing. Suppress specific exception types silently.",
    "Learned: `git bisect` binary-searches commit history to find which commit introduced a bug. Set good/bad commits, then it auto-checks out midpoints.",
    "SSH config file (~/.ssh/config) can alias hosts. Add `Host myserver\\n  HostName 192.168.1.100\\n  User ubuntu\\n  IdentityFile ~/.ssh/id_rsa` then just `ssh myserver`.",
    "Python walrus operator (:=) assigns inside an expression. `if (n := len(a)) > 10: print(n)` avoids calling len() twice.",
    "Async generators in Python: `async def gen(): yield value` combined with `async for item in gen()`. Great for streaming large datasets.",
    "Decorator order matters in Python: applied bottom-up. `@A @B def f()` is equivalent to `A(B(f))`.",
    "Learned about `functools.cache` (Python 3.9+). Drop-in replacement for `lru_cache(maxsize=None)`. Memoizes with no eviction.",
    "Python dataclasses with `frozen=True` are hashable and can be used as dict keys or in sets. Useful for cache keys.",
    "Type narrowing in TypeScript: `if (typeof x === 'string')` narrows x to string inside the block. Works for typeof, instanceof, and custom type guards.",
    "Go interfaces are satisfied implicitly — no `implements` keyword. If a type has the required methods, it implements the interface.",
    "Learned about `asyncio.gather` with `return_exceptions=True`. Instead of raising on first error, it returns exceptions as values in the results list.",
    "Python `__init_subclass__` hook: called when a class is subclassed. Use it to register subclasses or enforce constraints without a metaclass.",
    "Shell tip: `!!` repeats the last command. `sudo !!` is the classic 'forgot sudo' fix. `!$` is the last argument of the previous command.",
    "CSS Grid vs Flexbox: Grid is for two-dimensional layouts (rows AND columns), Flexbox is one-dimensional. Use Grid for overall page layout.",
    "Learned about HTTP/2 multiplexing: multiple requests over a single TCP connection, no head-of-line blocking. HTTPS required in practice.",
    "SQL window functions: `ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC)` — assigns rank within each group without collapsing rows.",
    "Difference between `==` and `is` in Python: `==` checks value equality, `is` checks object identity. `None` checks should always use `is`.",
    "Python `heapq.nlargest(k, iterable)` vs sorting: nlargest is O(n log k) vs O(n log n) for sort. Much faster when k << n.",
    "Learned: `curl -X POST -H 'Content-Type: application/json' -d @body.json URL` — `-d @file` reads request body from file.",
    "Python `itertools.chain.from_iterable` flattens one level of nesting without building an intermediate list. Memory-efficient for large iterables.",
    "Mutable default arguments in Python are a classic trap: `def f(x=[])` — the list is shared across all calls. Use `None` and create inside the function.",
    "Git `--force-with-lease` is safer than `--force` for push: it only pushes if your local tracking ref matches remote. Prevents overwriting someone else's push.",
    "Learned about connection pooling. SQLAlchemy default pool size is 5. Each API worker maintains its own pool. Under load, pool exhaustion causes 'QueuePool limit exceeded'.",
    "Python `abc.abstractmethod` enforces implementation in subclasses. Combined with `@property` it creates abstract properties. Good for Repository interfaces.",
    "Difference between shallow and deep copy in Python: `copy.copy()` vs `copy.deepcopy()`. Nested mutable objects in shallow copy still share references.",
    "Learned about tail call optimization: Python doesn't do it (stack grows with each recursion). Go doesn't either. Only some functional languages and Kotlin optimize this.",
    "Make targets are just shell commands with dependency tracking. `make test` runs the `test` target, which can depend on `make build` first.",
    "`grep -r 'pattern' . --include='*.py'` recursively searches Python files. `--include` uses glob patterns. `-l` lists filenames only.",
    "Learned: `jq '.[] | select(.status == \"failed\")' logs.json` — jq filters JSON arrays inline. Invaluable for API debugging.",
]

_AI_ML = [
    "RAG pipeline basics: retrieve relevant chunks from a vector store, inject them into the LLM prompt as context, generate grounded answers. Quality bottleneck is usually retrieval, not generation.",
    "Embedding models convert text to dense vectors where semantic similarity is preserved. Cosine similarity is the standard distance metric for text embeddings.",
    "all-MiniLM-L6-v2 produces 384-dimensional vectors. Faster than large models, good quality for English. Sentence-BERT is the model family — fine-tuned on NLI + MS MARCO.",
    "Cross-encoder rerankers read query and document together (not independently), so they capture interaction signals. Higher accuracy than bi-encoders but O(n) per query — only use on top-K candidates.",
    "BM25 is still competitive for exact keyword matching. Hybrid retrieval (BM25 + dense vectors) often beats either alone. The key is score normalization before fusion.",
    "Reciprocal Rank Fusion (RRF): score = Σ 1/(k + rank_i) across multiple retrieval systems. k=60 is the standard default. Doesn't need calibrated scores.",
    "HyDE (Hypothetical Document Embeddings): generate a fake answer to the query, embed it, use that vector for retrieval. Works because hypothetical answers share embedding space with real documents.",
    "Lost in the middle problem: LLMs are better at using context at the beginning and end of the prompt. Important chunks should not be buried in the middle.",
    "Chunking strategy affects retrieval quality significantly. Sentence-level chunks preserve meaning but are small. Paragraph-level is a good default. Hierarchical chunking stores both.",
    "HNSW (Hierarchical Navigable Small World): approximate nearest neighbor graph structure. O(log n) search. pgvector supports it. ef_construction controls build quality vs speed.",
    "Tokenization: BPE (Byte Pair Encoding) is used by most modern LLMs including GPT. Subword tokenization handles rare words by splitting into common subwords.",
    "Attention mechanism: each token attends to all other tokens in the sequence. Self-attention computes Q, K, V matrices. Multi-head attention runs attention in parallel with different projections.",
    "Fine-tuning vs prompting: fine-tuning changes model weights for specific tasks. Prompting uses the base model with crafted inputs. LoRA is a popular parameter-efficient fine-tuning method.",
    "Temperature in LLM generation: 0 = deterministic (most probable token always), 1 = original distribution. For factual tasks use 0, for creative tasks use 0.7-1.0.",
    "Hallucination in RAG: model generates facts not present in the retrieved context. Common causes: context too short, model too confident, conflicting context chunks.",
    "Evaluation metrics for RAG: Faithfulness (claims grounded in context), Answer Relevancy (answers the question), Context Recall (retrieved right docs), Context Precision (retrieved only relevant docs).",
    "LLM-as-judge: use a strong LLM to evaluate outputs from a weaker or different LLM. Problem: same-model bias (model scores its own outputs higher). Use different judge and generator models.",
    "Prompt caching in Gemini API: prefix cache reuses KV cache for repeated system prompts. Useful when you have a long static system prompt and many short queries.",
    "Gemini responseSchema: schema-enforced JSON output using Google's structured output mode. More reliable than instructing the model to output JSON in the prompt.",
    "Groq inference is extremely fast (700+ tokens/s) because they use LPU hardware. Good for low-latency use cases. Limited to supported model list.",
    "Vector database comparison: pgvector (PostgreSQL extension, familiar SQL), Qdrant (purpose-built, high performance), Weaviate (has graph features). For a Postgres-based app, pgvector is simplest.",
    "Embedding drift: if you update the embedding model version, old embeddings become incompatible. Need to re-embed everything on model update. Track model version in the embeddings table.",
    "Context window vs context utilization: Gemini 2.0 Flash has 1M token context but most applications use <2000 tokens. The gap between available and used context is a common optimization opportunity.",
    "Sentence transformers inference is CPU-bound. On a single core, encoding 100 short sentences takes ~50ms. Batch encoding with `model.encode(texts)` is much faster than one-by-one.",
    "ColBERT: late interaction model. Both query and document are encoded to multi-vector representations. MaxSim operator computes score. Better than bi-encoders, cheaper than cross-encoders.",
    "Sparse vectors: SPLADE, BM25 — each dimension corresponds to a vocabulary term. Dense vectors: learned embeddings. Hybrid search combines both.",
    "LLM context poisoning: if retrieved chunks contain conflicting information, the model may hallucinate to reconcile them. Filter chunks by relevance score before injection.",
    "Query expansion: generate multiple reformulations of the query before retrieval. Improves recall by catching different surface forms of the same question.",
    "Embedding models and OOV (out-of-vocabulary) terms: subword tokenization handles most OOV. But very domain-specific jargon (acronyms, product names) may get poor embeddings.",
    "Knowledge graph + RAG: structured knowledge complements unstructured text retrieval. Entity recognition → graph lookup → inject structured facts into context.",
    "Semantic caching: cache LLM responses by embedding the query, use cosine similarity to find cached responses for semantically equivalent queries. Reduces API costs.",
    "Reranking pipeline: (1) recall — fast approximate retrieval (top-100), (2) precision — cross-encoder reranker (top-10), (3) generate — LLM with top-5 context.",
    "Multi-query retrieval: generate 3-5 alternative phrasings of the user question, retrieve for each, merge results. Improves recall for ambiguous queries.",
    "Grounding in RAG: every factual claim in the answer should be traceable to a specific chunk. Hallucination testing checks this systematically.",
    "Sentence window retrieval: index individual sentences for precise retrieval but return the surrounding window (±2 sentences) as context. Good balance of precision and completeness.",
    "Cohere Rerank API: send query + candidate documents, receive relevance scores. Uses a cross-encoder internally. Drop-in for reranking without training your own model.",
    "Eval dataset for RAG should include: (1) easy factual lookups, (2) multi-hop questions requiring combining 2+ docs, (3) unanswerable questions (tests hallucination), (4) paraphrased queries.",
    "Prompt injection in RAG: malicious content in retrieved documents that overrides system instructions. Mitigation: separate context from instructions, validate retrieved content.",
    "LLM output validation: Pydantic models for structured output, regex for format validation, secondary LLM call for content quality check.",
    "MRR (Mean Reciprocal Rank): average of 1/rank of first relevant result. 1.0 = always first. 0.5 = first relevant result is at rank 2 on average. Good for navigational queries.",
]

_UNIVERSITY = [
    "OS scheduling algorithms: FCFS (simple, convoy effect), SJF (optimal avg wait, starvation), Round Robin (fair, higher turnaround), Priority (can starve, solve with aging).",
    "Page replacement algorithms: FIFO (easy, Belady's anomaly), LRU (good performance, needs hardware support), Optimal (theoretical best, requires future knowledge).",
    "Deadlock conditions (all four must hold): Mutual Exclusion, Hold and Wait, No Preemption, Circular Wait. Breaking any one prevents deadlock.",
    "Banker's algorithm: deadlock avoidance — check if granting a resource request leads to a safe state. O(n²m) complexity. Used in theory, rarely in practice.",
    "Virtual memory: program addresses are virtual, mapped to physical via page table. TLB caches recent translations. Page fault triggers OS to load page from disk.",
    "DBMS normalization: 1NF (atomic values), 2NF (no partial dependency on composite key), 3NF (no transitive dependency), BCNF (every determinant is a candidate key).",
    "ACID properties: Atomicity (all or nothing), Consistency (valid state to valid state), Isolation (concurrent transactions don't see each other's partial results), Durability (committed data survives crashes).",
    "B+ tree: all data in leaves, leaves linked as a doubly linked list. Great for range queries. Height O(log n). PostgreSQL primary indexes use B+ trees by default.",
    "Hashing for DB indexes: O(1) lookup on equality. Can't do range queries. Good for unique key lookups (primary key by hash).",
    "TCP three-way handshake: SYN → SYN-ACK → ACK. Connection teardown: FIN → FIN-ACK → ACK. TIME_WAIT state after close lasts 2×MSL to handle delayed packets.",
    "OSI model layers (1-7): Physical, Data Link, Network, Transport, Session, Presentation, Application. TCP/IP model collapses to 4 layers.",
    "Subnet mask /24 = 255.255.255.0 = 256 addresses (254 usable). /16 = 65536 addresses. CIDR notation makes subnetting readable.",
    "Graph algorithms complexity: DFS/BFS O(V+E), Dijkstra O((V+E) log V) with min-heap, Bellman-Ford O(VE), Floyd-Warshall O(V³), Kruskal O(E log E).",
    "Dynamic programming: overlapping subproblems + optimal substructure. Top-down (memoization) stores results in a map. Bottom-up (tabulation) fills a table iteratively.",
    "Greedy algorithms: locally optimal choices lead to globally optimal solution. Works for: fractional knapsack, activity selection, Huffman coding, Prim's/Kruskal's MST.",
    "NP-complete problems: Traveling Salesman, Knapsack 0/1, Graph Coloring, SAT. No known polynomial-time algorithm. Approximation algorithms exist.",
    "Convex hull algorithms: Graham scan O(n log n), Jarvis march O(nh) where h = hull points. Gift wrapping visualization helped me understand Jarvis march.",
    "Segment trees support range queries in O(log n). Build in O(n). Update in O(log n). Use for range sum, range min/max. Fenwick tree is simpler for prefix sums.",
    "Trie data structure: prefix tree for string storage. Insert/search/delete in O(m) where m = string length. Memory-heavy but very fast for prefix matching.",
    "AVL tree vs Red-Black tree: AVL is more strictly balanced (better lookup), Red-Black has fewer rotations (better insert/delete). Most standard libraries use Red-Black.",
    "Compiler phases: Lexical Analysis → Syntax Analysis (parse tree) → Semantic Analysis → IR Generation → Optimization → Code Generation.",
    "Regular expressions are recognized by DFAs. Context-free grammars by PDAs. Context-sensitive grammars by LBAs. Turing machines recognize recursively enumerable languages.",
    "Capstone project: Building a Timetable Management System for Thapar. Using React frontend, Node.js backend, PostgreSQL. Auto-assigns rooms and professors based on constraints.",
    "Exam tip for DBMS: normalization questions always ask to decompose and check FDs. Write all FDs, find candidate keys, check each normal form definition.",
    "Computer Networks lab assignment: implement a sliding window protocol simulator in Python. Selective Repeat is more complex than Go-Back-N but more efficient.",
    "Distributed systems: CAP theorem — Consistency, Availability, Partition tolerance. Can only guarantee two. CockroachDB and Spanner try to be CP but with high availability.",
    "Cache coherence problem in multiprocessors: MESI protocol states — Modified, Exclusive, Shared, Invalid. Ensures all cores see consistent memory.",
    "Process vs Thread: process has its own memory space, threads share heap and code. Thread creation is faster. Threads within a process can deadlock on shared resources.",
    "Semaphore vs Mutex: mutex has ownership (only locker can unlock), binary semaphore doesn't. Use mutex for mutual exclusion, semaphore for signaling.",
    "Memory hierarchy: registers (fastest), L1 cache, L2 cache, L3 cache, RAM, SSD, HDD (slowest). Each level is larger and slower. Cache hit rate determines effective speed.",
    "Network security: TLS handshake uses asymmetric encryption to exchange a symmetric session key. The actual data transfer uses the faster symmetric key.",
    "Exam week is brutal. DBMS on Monday, CN on Wednesday, OS on Friday. Need to finish the lab practicals before that. Time to stop Netflix.",
    "Discrete math revision: proof by induction — show base case, assume P(k), prove P(k+1). Strong induction assumes all P(i) for i ≤ k.",
    "Set theory: DeMorgan's laws — complement of (A∪B) = complement(A)∩complement(B). Foundation of boolean algebra and database query optimization.",
    "Submitted the OS assignment on process synchronization. Used Peterson's algorithm for the critical section. Professor said the explanation was clear.",
]

_INTERVIEW_PREP = [
    "Two Sum problem: use a hash map. For each element, check if complement (target - element) exists in map. O(n) time, O(n) space. Classic HashMap pattern.",
    "Sliding window for maximum sum subarray of size k: maintain a running sum, add new element, remove leftmost. O(n) — no nested loops.",
    "Binary search template: `lo, hi = 0, len(arr)-1; while lo <= hi: mid = (lo+hi)//2`. If arr[mid] == target return mid. If arr[mid] < target lo = mid+1 else hi = mid-1.",
    "BFS for shortest path in an unweighted graph. Use a deque. Mark visited before enqueuing to avoid cycles. DFS doesn't guarantee shortest path.",
    "Merge intervals: sort by start time. For each interval, if it overlaps the last one in result (start <= last.end), extend last.end = max(last.end, end). Else append.",
    "Linked list reversal: three pointers (prev=None, curr=head, next=None). Loop: next=curr.next, curr.next=prev, prev=curr, curr=next. Return prev.",
    "LRU Cache: OrderedDict in Python. Move to end on access. Pop from front when over capacity. O(1) get and put.",
    "Trie for autocomplete: insert each word character by character. Search by following the prefix path. Collect all words in subtree for suggestions.",
    "Graph cycle detection: DFS with visited set AND recursion stack. A node in the recursion stack that's visited again indicates a cycle. Topological sort also detects cycles.",
    "Tree diameter: DFS returning (height, diameter) from each node. Diameter through node = left_height + right_height + 2. Answer is max across all nodes.",
    "System design: URL shortener. Core components: ID generation (base62 encoding of auto-increment), Redis cache for hot links, PostgreSQL for persistent storage, CDN for redirects.",
    "System design: Twitter feed. Options: fan-out on write (push to follower timelines — great read speed, expensive write for popular users), fan-out on read (pull and merge — fresh but slow).",
    "System design: rate limiter. Token bucket algorithm: each user gets a bucket with max tokens. Tokens replenish at a fixed rate. Request consumes one token. Redis INCR + TTL for distributed.",
    "Consistent hashing: maps both servers and data to a ring. Data goes to the first server clockwise. Adding/removing a server only affects its neighbors on the ring.",
    "CAP theorem in system design: for a distributed database — if partition happens, choose consistency (reject writes) or availability (accept possibly stale reads). Can't have both.",
    "Behavioral question prep: STAR format — Situation, Task, Action, Result. Practice: tell me about a conflict with a teammate, a time you failed, your biggest technical challenge.",
    "For Amazon interviews: Leadership Principles are the frame for behavioral questions. Specifically prepare stories for: Customer Obsession, Bias for Action, Deliver Results, Learn and Be Curious.",
    "DB indexing question came up in mock: covering index, partial index, composite index order (selectivity matters), when indexes hurt (write-heavy tables).",
    "LeetCode mock session result: 2 easy solved in 12 min, 1 medium in 28 min, 1 hard not completed. Need to improve hard DP problems.",
    "HashMap collision handling: open addressing (linear probing, quadratic probing, double hashing) vs chaining (linked list at each bucket). Python uses open addressing with a mix.",
    "Quicksort avg O(n log n) but O(n²) worst case (sorted array with pivot at end). Randomize pivot to avoid worst case. In-place, good cache behavior.",
    "Heap push O(log n), pop O(log n), heapify from array O(n) (not O(n log n)). Python's heapq is a min-heap. For max-heap negate values.",
    "Graph coloring for scheduling: represent conflicts as edges. If two tasks can't run simultaneously, connect them. Minimum colors = chromatic number = minimum parallel resources.",
    "Mock interview feedback: explained the problem clearly, coded correctly but didn't handle edge cases (empty array, single element). Always ask about constraints and edge cases.",
    "Backtracking template: try a choice, recurse, undo the choice. N-Queens, Sudoku solver, permutations/combinations all use this pattern.",
    "Preparing a list of questions to ask interviewers: What does the onboarding process look like? How do teams handle technical debt? What does a successful first 90 days look like?",
    "Resume tip: quantify impact. 'Reduced API latency by 40%' is better than 'improved API performance'. Use numbers wherever possible.",
    "Topological sort (Kahn's algorithm): find nodes with in-degree 0, add to queue, process, decrement neighbors' in-degrees, repeat. Cycle detection: if not all nodes processed, cycle exists.",
    "Floyd-Warshall for all-pairs shortest paths: `dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])` for all k. O(V³). Detects negative cycles if dist[i][i] < 0.",
    "OA preparation: practice under time pressure. 90 minutes for 3 problems means 30 min each max. First 5 min: understand and clarify. Next 20 min: code. Last 5 min: test.",
]

_PROJECT_KVAULT = [
    "KnowledgeVault architecture decision: went with PostgreSQL + pgvector over a dedicated vector DB. Reasoning: single service to manage, familiar SQL, pgvector performance is adequate for personal scale.",
    "Bug fixed: note processing worker was silently swallowing errors because the bare except caught and ignored exception traceback. Changed to logger.exception() so we see full stack traces.",
    "Implementing the hybrid retrieval system. Semantic arm uses note-level embeddings (all-MiniLM-L6-v2). Intent arm classifies query intent and finds matching categories. Fused by additive score boost.",
    "Redis queue implementation uses brpoplpush for reliable delivery: moves job to inflight queue atomically. On worker crash and restart, inflight jobs are recovered and re-queued.",
    "Chunking issue: 500-char chunks with 50-char overlap is too small for PDF uploads. A 10-page research paper creates 60+ tiny chunks with no context. Need to increase chunk size for documents.",
    "Fixed IDOR vulnerability: get_related_notes used to take any note_id without ownership check. An attacker could probe other users' note similarity. Added ownership verification before embedding lookup.",
    "Gemini API rate limiting: free tier is 15 RPM. For evaluation with 54 queries, each needing pipeline + judge = 2 calls, need 16s between queries not 8s. Evaluation was failing silently.",
    "Graceful degradation working correctly: when Gemini returns 429 and Groq also fails, API returns retrieval-only response instead of 500. Users still get relevant notes.",
    "Category naming is deterministic Python rules, no LLM involved. This was the right call — reproducible categories, no hallucinated names, consistent across runs.",
    "Intent classification at query time uses a keyword-only fast classifier. Intent accuracy is 34% on the benchmark. The bottleneck for hybrid retrieval improvement.",
    "Benchmark finding: HYBRID = SEMANTIC exactly on all 50 queries. Intent arm contributes nothing measurable. Root cause: confidence_factor=0 for 50% of queries, is_boosted=False for vector matches.",
    "To-do for KnowledgeVault: add HNSW index on embeddings table. Currently doing sequential scans (O(N)). Fine for <1000 notes but will fail at scale.",
    "Streaming endpoint uses StreamingResponse with text/event-stream media type. But the format is raw tokens, not SSE. Any SSE client library will fail. Need to fix the format to `data: {token}\\n\\n`.",
    "Docker build optimization: three-layer cache strategy. System deps → Python deps → HF model download → App code. Code changes only rebuild the last layer. Build went from 8 min to 45 sec.",
    "CacheService wraps Redis with no error handling. If Redis restarts, every /ask request raises an unhandled exception. Need try/except to bypass cache on failure.",
    "Evaluation framework design: LLM-as-judge uses Gemini to score answers. The judge is the same model as the generator — creates self-serving bias. Should use different model for production eval.",
    "Note: context budget is hardcoded at 3000 chars (~750 tokens). Gemini 2.0 Flash has 1M token window. This is 99.9% waste. Should be configurable, default 8000+.",
    "Password validation missing in UserRegister schema. Empty string or 1-char passwords are accepted. Add `min_length=8` Field constraint.",
    "Upload endpoint reads entire file into memory with `file.file.read()` before writing to disk. A 10GB upload would exhaust memory. Need to stream to disk in chunks.",
    "Scratch folder has analysis notebooks that are committed to the repo. Looks unprofessional. Add to .gitignore.",
    "main.py has imports scattered mid-file after router includes. All imports should be at the top. Quick fix.",
    "Feature idea: add a /health endpoint that pings both DB and Redis. README claims it exists at /health but it returns 404.",
    "Plan: expand the benchmark dataset to 300+ retrieval queries and 150+ ask queries for statistically significant evaluation. Current 50-query benchmark has MDE of 0.10 — too coarse.",
    "Worker handles KeyboardInterrupt for Ctrl-C shutdown, but Docker sends SIGTERM. Python only converts SIGTERM to KeyboardInterrupt if signal.signal is registered. Jobs might be lost on container stop.",
    "The semantic retrieval uses note-level embeddings but chunk embeddings also exist in chunk_embeddings table and are never used in the production retrieval path. Should use chunk embeddings for finer-grained retrieval.",
]

_SYSTEM_DESIGN = [
    "Database sharding: horizontal partitioning across multiple DB instances. Shard key choice is critical — bad key causes hot shards. Options: range-based, hash-based, directory-based.",
    "Read replicas: copy of primary DB for read-heavy workloads. Async replication means replicas may lag. Read-your-own-writes problem: user writes to primary, reads from replica before replication.",
    "Event sourcing: store the sequence of events, not the current state. Current state is derived by replaying events. Easy audit log, but queries require building a read model (CQRS pattern).",
    "Message queues (Kafka vs RabbitMQ): Kafka is a distributed log, persistent, good for high-throughput and replay. RabbitMQ is a traditional message broker, better for complex routing, lower latency.",
    "API gateway pattern: single entry point for all clients. Handles auth, rate limiting, routing, SSL termination, load balancing. Kong, NGINX, AWS API Gateway are common choices.",
    "Circuit breaker pattern: after N consecutive failures, open the circuit and return errors immediately without calling the failing service. After timeout, try one request (half-open state).",
    "CQRS (Command Query Responsibility Segregation): separate models for reads and writes. Write model accepts commands (updates). Read model optimized for queries. Can use different DBs for each.",
    "Load balancing algorithms: round-robin (simple, ignores server load), weighted round-robin (accounts for capacity), least connections (smart for variable request duration), consistent hashing (sticky sessions).",
    "Service mesh (Istio): handles inter-service communication at the infrastructure level. mTLS, retry policies, circuit breaking, distributed tracing without changing application code.",
    "Database connection pooling: creating a new connection is expensive (TCP handshake + auth). Pool maintains N idle connections ready to use. PgBouncer is a PostgreSQL-specific pooler.",
    "Bloom filter: space-efficient probabilistic data structure. Says 'definitely not in set' or 'probably in set'. No false negatives. Used to avoid expensive DB lookups for missing keys.",
    "Two-phase commit (2PC): coordinator asks all participants to prepare (lock resources), then commit. Blocking protocol — if coordinator fails after prepare, participants are stuck. Three-phase commit adds a pre-commit phase.",
    "Sagas for distributed transactions: long-running business processes split into local transactions with compensating transactions for rollback. Choreography (events) vs Orchestration (central coordinator).",
    "CDN (Content Delivery Network): caches static assets close to users. Edge nodes serve content from nearest PoP. Cache invalidation is the hard problem — use versioned URLs.",
    "Observability: logs (what happened), metrics (how much/how often), traces (how long / where time was spent). The three pillars. OpenTelemetry standardizes instrumentation.",
    "WebSockets vs long polling: WebSockets = persistent bidirectional connection, better for real-time. Long polling = client holds connection until server has data, simpler but more overhead.",
    "Multi-tenant architecture: shared database (simple, tenant data mixed), database per tenant (isolated, expensive), schema per tenant (balance). Isolation vs operational complexity trade-off.",
    "Rate limiting strategies: fixed window (simple, burst at window boundary), sliding window log (accurate, memory-heavy), sliding window counter (approximation, memory-efficient).",
    "Health checks for microservices: liveness (is the process alive?), readiness (is it ready to serve traffic?). Kubernetes uses both. Readiness gates traffic. Liveness triggers restart.",
    "Idempotency keys: client sends a unique key with each request. Server stores result by key and returns cached result on retry. Prevents duplicate processing of payments or orders.",
]

_MEETINGS = [
    "Team sync today: three PRs merged this week. Blocked on the database migration — waiting for DevOps to approve the schema change request. Follow up with Ankit by Thursday.",
    "Meeting with Professor Sharma: capstone submission deadline is April 15th. Need to submit a 30-page report plus working demo. Team split: I take backend, Raunak takes frontend, Ayush takes report.",
    "Discussed KnowledgeVault architecture with Sid over video call. He suggested adding a graph-based category relationship. Agreed that the complexity isn't worth it for now.",
    "Internship interview debrief: two-stage process. First round was a coding round (2 DSA problems, 45 min). Second round is system design + behavioral. Prep accordingly.",
    "Mentor session with Arjun: feedback on resume — too many bullet points, not enough impact metrics. Also said to push the KnowledgeVault project more prominently.",
    "Weekly sync with placement cell: 47 companies confirmed for campus placements. Registration opens March 1st. Priority companies: Microsoft, Adobe, Intuit, Atlassian, Flipkart.",
    "Lab session: Professor gave a new assignment — implement a mini file system in C. Uses linked list for FAT (File Allocation Table). Due in 3 weeks.",
    "Hackathon team meeting: topic decided — AI-powered study planner that adapts to exam schedule. Stack: React, FastAPI, SQLite, Gemini API. 36-hour hackathon on February 17th.",
    "Meeting with design team: finalizing UI for the capstone project. Agreed on dark mode by default, card layout for notes, sidebar navigation. Color palette: midnight blue and mint green.",
    "Quick catch-up with Priya: she's doing an internship at a fintech startup. Said the tech stack is outdated (Java Spring Boot, Oracle DB). Helpful context for interview prep.",
    "Department meeting about lab infrastructure: 30 new machines being installed next month. Linux only — professors finally agreed to stop forcing Windows for OS lab.",
    "Project retrospective: sprint 3 went well except the Redis integration took 3 days instead of 1 (underestimated the connection handling complexity). Need better estimates next sprint.",
    "Call with college senior who's at Microsoft: advice — focus on problem-solving clarity, not just getting the right answer. Interviewers evaluate how you think more than just the code.",
    "Brief standup: working on the evaluation framework for KnowledgeVault today. Blocked on Gemini API rate limits during the 54-query evaluation run.",
    "Discussed note batching strategy with Sid: process 100 notes at a time, wait for all to be 'organized' before next batch. Need to poll organization_status.",
    "Meeting notes — backend architecture review: agreed to keep synchronous API calls and async background processing for note indexing. No microservices for now.",
    "Catch-up with Raunak: he finished the React frontend for capstone. Looks clean. Integration with my FastAPI backend due this weekend.",
    "Placement mock interview practice group: 4 people, rotate interviewer role. 2 hours every Saturday morning. Starting next week at the library.",
]

_REMINDERS_TASKS = [
    "Submit capstone progress report by March 25th. 10 pages minimum. Include architecture diagram and progress against milestones.",
    "Pay hostel fees before March 31st. Late payment incurs a fine of Rs 500 per day. Log into the student portal.",
    "Dentist appointment booked for March 15th at 10 AM at Fortis Dental Clinic. Bring insurance card and ID.",
    "Buy groceries: milk, bread, eggs, bananas, oats, curd, green tea, maggi. Also need a new notebook and pens.",
    "Return library book 'Designing Data-Intensive Applications' by March 20th. Already renewed it once.",
    "Renew vehicle insurance before April 10th. Check HDFC Ergo renewal link. Premium was ~4200 last year.",
    "Call mom on Sunday evening. Send her the capstone project screenshots. She keeps asking about what I'm building.",
    "Remind Raunak to submit the college leave application before the hackathon. Last time he forgot and got a proxy marked.",
    "Recharge Jio monthly plan — it expired yesterday. Use PhonePe for Rs 599 plan (84 days, unlimited data).",
    "Download the semester fee receipt for scholarship application. Portal link: erp.thapar.edu/student.",
    "Fix the broken CI pipeline before the weekend. Failing because the test database isn't configured in GitHub Actions secrets.",
    "Water bill due this week. Pay via Google Pay to the society account. Around Rs 320 this month.",
    "Schedule health checkup before the semester ends. Basic blood panel + eye check. Haven't had a checkup in 18 months.",
    "Update LinkedIn with the KnowledgeVault project. Add a description with tech stack and key features. Add Gemini API and pgvector as skills.",
    "Need to clean my room this weekend. Return borrowed charger to Prashant. Find my missing notebook from the algorithms class.",
    "Backup all code to GitHub. Have local commits that aren't pushed. Do this today before laptop issues cause problems.",
    "Apply for summer research internship at IIT Delhi before February 28th. Need recommendation letter from Professor Sharma.",
    "Electricity bill payment: Rs 1,240 due by March 5th. Set up auto-debit to avoid late fees.",
    "Message Siddhant about his part of the group assignment. Due Friday. He hasn't started yet.",
    "Print ID card for the placement registration — department office needs physical copy.",
    "Start studying for GATE 2025 if I don't get a placement offer by May. Computer Science syllabus is vast — start with DS&A and OS.",
    "Pick up the laptop charger from the repair shop. They said it'll be ready by Tuesday.",
    "Submit the research paper review comments to IEEE by end of month. Professor Gupta asked me to review 2 papers.",
    "Book train ticket to Delhi for the hackathon. March 15th, Shatabdi or Intercity. Book at least a week ahead.",
    "Remind Ayush to pay his part of the mess bill split. Rs 850. He's been forgetting for two weeks.",
    "Check if the scholarship amount has been credited — should have arrived by the 25th of this month.",
    "Set up 2FA on my Google account. Keep getting prompts but keep dismissing. Do it today.",
    "Need to renew my GitHub Student Pack — free tier expired. Student email still works, just need to reapply.",
    "Complete the IEEE membership renewal. Annual fee is $32. Check if the department reimburses it.",
    "Talk to placement officer about the off-campus offer letter documentation requirements. Need original signed copy.",
]

_SHOPPING_FINANCE = [
    "Monthly budget tracking: Feb 2024. Mess: 3200, Transport: 800, Groceries: 1400, Coffee/snacks: 600, Subscriptions: 400, Misc: 500. Total: 6900. Need to reduce misc spending.",
    "Laptop comparison notes: Dell XPS 15 (best build, expensive), MacBook Air M2 (best battery/performance, iOS ecosystem, Rs 100k), Lenovo IdeaPad 5 (good value, Rs 55k). Decision pending.",
    "Bought a new mechanical keyboard — Keychron K8 Pro. Cherry MX Brown switches. Rs 8,500. Should last many years. Already improved typing speed.",
    "Amazon wishlist: external SSD (Samsung T7, 1TB), laptop stand, USB-C hub, blue light glasses, ergonomic chair mat. Total estimate: Rs 12,000.",
    "Savings goal: build Rs 50,000 emergency fund before graduation. Currently at Rs 18,000. Depositing Rs 2,000 per month from stipend.",
    "Mutual fund SIP: started a Rs 1,000/month SIP in NIFTY 50 index fund. Long term goal — don't touch for 5 years. Using Zerodha Coin.",
    "PhonePe rewards: earned Rs 150 cashback this month from grocery payments. Accumulated Rs 650 total in rewards. Redeem against next electricity bill.",
    "Grocery run needed: bring list next time. Forgot oats, forgot coffee, forgot shampoo. Make a checklist on the phone before leaving.",
    "Split expense tracker for hostel room: electricity (split 4 ways), internet (split 4 ways), cleaning supplies (split 4 ways). Use Splitwise to track.",
    "Books to buy: 'Clean Code' by Robert Martin, 'System Design Interview' by Alex Xu (Vol 2). Check Notion for the book list. Amazon or Flipkart.",
    "Course purchase: Udemy 'System Design Masterclass' Rs 399 during sale. Also bought 'FastAPI Full Course' for Rs 299. Discount expires in 3 hours so bought it.",
    "Monthly subscriptions: Netflix (family plan split, pays Rs 150), Spotify (Rs 119), ChatGPT Plus (Rs 1,676). Total: Rs 1,945/month. Cancel ChatGPT if I get Gemini Advanced.",
    "Wanted to buy RAM upgrade for laptop: current 8GB is not enough for running Docker + IDE + multiple browser tabs. 16GB DDR4 SO-DIMM is Rs 3,200.",
    "Food budget breakdown: breakfast Rs 50/day, lunch at mess Rs 90/day, dinner Rs 70/day. Coffee twice a week Rs 120/week. Monthly food cost: ~Rs 6,540.",
    "Investment: considering buying 1 unit of HDFC Nifty Next 50 ETF. Research first — expense ratio 0.2%, tracks Nifty Next 50, good for diversification from Large cap.",
    "Electricity bill split this month: total Rs 1,840, each person pays Rs 460. Prashant, Arjun, Raunak, me. Collect by tomorrow.",
    "Travel expenses for Delhi hackathon: train Rs 620 (Shatabdi return), hostel Rs 500/night × 2, food Rs 500. Total ~Rs 2,240 for the weekend.",
    "Shopping done this week: groceries Rs 1,200, printing notes Rs 80, bus pass recharge Rs 250. Total Rs 1,530.",
    "Recharge DTH for family home visit — prepaid plan for 3 months. Around Rs 700. Do it before going home next month.",
    "Found a good deal on Flipkart: Noise Colorfit Pro 4 smartwatch Rs 2,799. Wanted one for tracking sleep and workouts. Buying on Diwali sale.",
]

_TRAVEL = [
    "Delhi trip plan — hackathon weekend: Train from Chandigarh at 7:10 AM (Shatabdi), reaches Delhi 10:30 AM. Venue is at IIT Delhi. Book return for Sunday evening.",
    "Home visit plan for Holi: leave Friday evening, return Monday. Buy sweets for family. Need to finish the capstone deliverable before going.",
    "Goa trip post-placements plan: 5 people, budget Rs 8,000 per person. Book early on MakeMyTrip — January is off-season, cheaper flights. Flight vs sleeper bus decision pending.",
    "Shimla trek planned for April. Triund trek is 2 days, moderate difficulty. Need trekking shoes (borrow from Ankit) and layered clothing. Best season April-June.",
    "Manali weekend trip: 4 people, rented a cab (Rs 2,000 each). Booked hotel near Mall Road Rs 1,200/night split 2 ways. Activities: rohtang pass (check snow), old manali market.",
    "Train booking lesson: always book in tatkal if you missed the regular window. Tatkal opens 24 hours before departure. 10 AM sharp — be ready to book.",
    "Chandigarh exploration on Sunday: Rose Garden (free), Rock Garden (Rs 30 entry), Sukhna Lake (free). Best by cycle — rent from the rental near sector 17.",
    "Packing list for Delhi trip: laptop + charger, backup power bank, 2 changes of clothes, toiletries, earphones, ID card, cash Rs 2,000, water bottle.",
    "Planning a solo trip to Mcleodganj after exams. Budget: Rs 3,000 for 3 days. Famous for monasteries, Dharamshala cricket ground nearby. May attempt the Triund trek solo.",
    "IRCTC tip: use the official app not third-party. Enable UPI payment for faster checkout. Have multiple payment methods ready for tatkal booking — it's fast.",
    "Hostel stay experience: stayed at Zostel Delhi. Rs 600/night for a dorm bed. Clean, good WiFi, common kitchen. Met a developer from Bangalore — exchanged contacts.",
    "International travel dream: want to visit Singapore and Japan before 30. Start saving. Singapore needs strong finances, Japan needs planning for sakura season (March-April).",
    "Ola vs Rapido: Ola is more expensive but more reliable. Rapido bikes are cheapest for short distances. For the airport, always book Ola or Uber well in advance.",
    "Chandigarh to Delhi road trip notes: NH44 via Ambala. 5 hours without stops. Stop at Murthal for Haldiram's. Toll charges ~Rs 200 one way.",
    "Trip to Amritsar: Golden Temple visit mandatory. Wagah Border ceremony is at 4:30 PM — reach by 3:30. Amritsari kulcha is excellent near the Golden Temple.",
]

_HEALTH = [
    "Started a new workout routine: Monday/Wednesday/Friday push-pull-legs. Sunday is rest. Goal: build consistency before adding weight. Week 1 complete.",
    "Sleep tracking: averaging 6.2 hours this week. Target is 7.5. Coffee after 4 PM is probably the issue. Cut it to one coffee, morning only.",
    "Water intake habit: set a reminder every 2 hours. Aiming for 2.5 liters/day. Currently at ~1.5 liters. Dehydration causes afternoon headaches.",
    "Eye strain from screen time. Following 20-20-20 rule: every 20 minutes, look at something 20 feet away for 20 seconds. Also getting blue light glasses.",
    "Workout progress: bench press 40kg → 50kg in 6 weeks. Pull-ups went from 5 to 9. Consistency matters more than intensity.",
    "Anxiety management: 4-7-8 breathing technique. Inhale 4 counts, hold 7, exhale 8. Works well before interviews or presentations. Also: journaling before sleep.",
    "Nutrition focus this week: more protein. Aim for 100g/day. Eggs (breakfast), dal + paneer (lunch), curd (evening), protein supplement if needed. Cut junk food.",
    "Started meditating: 10 minutes every morning using Headspace app. Two weeks in, noticeably less anxious during exams. Try to continue.",
    "Blood work done: Vitamin D is low (18 ng/mL, normal is >30). Doctor prescribed Vitamin D3 60K IU once a week for 8 weeks. Also take daily multivitamin.",
    "Running goal: 5K in under 30 minutes by May. Currently at 38 minutes. Run 3 times a week, increase pace 5 seconds/km per week.",
    "Posture issues from sitting 8+ hours. Getting lower back pain. Exercise: cat-cow, child's pose, hip flexor stretches. Take standing breaks every 45 minutes.",
    "Mental health note: feeling burnt out from capstone + placement prep simultaneously. Took Saturday completely off. Felt much better. Schedule one complete day off per week.",
    "Wrist pain from typing — probably RSI early signs. Take breaks, wrist circles, compression brace at night. Keyboard raise angle might be wrong. Ergonomics check needed.",
    "Started tracking mood daily in a journal: 1-5 scale. Noticed pattern: mood drops when I skip exercise. Correlation is clear. Exercise = natural antidepressant.",
    "Health checkup results: cholesterol slightly elevated. Doctor says diet change first. Reduce saturated fat, add omega-3. No medication needed yet.",
]

_STARTUPS = [
    "Startup idea: AI-powered study planner that integrates with college exam schedules. Detects exam dates, difficulty weights, and optimizes a personalized study plan. Monetize via premium plan.",
    "Business idea: hyperlocal delivery service for college campuses. Students order from outside food vendors. Last-mile delivery by other students who earn commission.",
    "KnowledgeVault as a product: could expand into team knowledge management. Shared knowledge bases, collaborative note taking, team Q&A over docs. Competitive with Confluence but AI-native.",
    "Idea: developer tools SaaS. Code review assistant trained on your codebase. Suggests refactors consistent with your patterns. Charges per seat. Target: mid-size dev teams.",
    "Startup research: EdTech in India. Market is huge but commoditized at the bottom. Premium tier (Rs 500-2000/month) is underserved. Target: serious learners willing to pay.",
    "Read about the YC application process. Apply twice if you don't get in. The most important part is the 'Why now?' and 'What's your unfair advantage?' answers.",
    "Idea validation framework: talk to 10 potential customers before writing code. Ask: what's your current solution? How much do you pay? What frustrates you most about it?",
    "Business model for KnowledgeVault: free tier (500 notes, basic search), pro tier ($8/month, unlimited notes, AI Q&A, advanced categories), team tier ($20/seat, shared workspace).",
    "Competitor analysis for AI note-taking: Notion AI (expensive, not personal knowledge focused), Obsidian (local-first, no AI), Roam Research (expensive, steep learning curve). Gap: simple + AI-native.",
    "Startup idea: AI-powered resume reviewer. Takes your resume + job description, highlights gaps, suggests improvements. Charges Rs 99 per review. High volume, low margin.",
    "Side project idea: automated competitive programming solution explainer. Takes a LeetCode URL, fetches the problem, explains the optimal solution in simple terms. Open source + ads.",
    "Market research: 40% of college students in India use some form of note-taking app. Only 12% use a paid app. Huge conversion opportunity with a compelling free-to-paid funnel.",
    "Idea: API monetization platform for students. Host your ML models, get an API endpoint, track usage, enable monetization. Stripe integration for payments.",
    "Thought about the 1000 true fans concept. For a Rs 1000/year subscription, 1000 customers = Rs 10 lakh/year. Achievable for a niche B2C product in 2-3 years.",
    "Startup lesson: don't build features, solve problems. Every new feature should be justified by customer pain. The MVP should solve one problem extremely well.",
]

_BOOKS_MEDIA = [
    "Designing Data-Intensive Applications (Kleppmann): best technical book I've read. Chapter on replication is outstanding. Makes distributed systems intuitive. Highly recommend to anyone doing backend.",
    "Finished 'The Pragmatic Programmer' by Hunt and Thomas. Key takeaway: DRY (Don't Repeat Yourself), YAGNI (You Aren't Gonna Need It), invest in your knowledge portfolio every day.",
    "Reading 'Clean Code' by Uncle Bob. Controversial but useful. Main point: code is read far more than written. Optimize for readability, not cleverness. Name things what they are.",
    "Currently reading 'System Design Interview' by Alex Xu (Vol 2). Excellent for interview prep. Each chapter is a complete design problem. URL shortener, Uber, YouTube design.",
    "Watched the documentary 'Free Solo' about Alex Honnold free climbing El Capitan. Impressed by the mental preparation — he visualized every move thousands of times before attempting.",
    "Podcast: Lex Fridman interview with Andrej Karpathy. Mind-blowing discussion on AI scaling, AGI timelines, and autonomous vehicles. Karpathy's clarity of thought is exceptional.",
    "Movie: Oppenheimer (2023). 3 hours well spent. The Trinity test scene is the best movie moment in years. Made me curious about the Manhattan Project — started reading Wikipedia.",
    "Book note — Atomic Habits (James Clear): habits are built on cue-routine-reward loops. Environment design is more powerful than willpower. Make good habits obvious and easy.",
    "Just finished 'Zero to One' by Peter Thiel. Best insight: go from 0 to 1 (create something new) vs 1 to n (copy something). Monopolies drive innovation, not competition.",
    "'The Phoenix Project' by Gene Kim is DevOps in novel form. Completely changed how I think about software delivery, bottlenecks, and team dynamics. Required reading for engineering leads.",
    "Watching 'Mr. Robot' — technically accurate hacking scenes. Elliot's use of Linux, social engineering, and Kali Linux tools is realistic. Impressive research by the writers.",
    "Book: 'Deep Work' by Cal Newport. Key idea: the ability to focus without distraction is becoming rare and increasingly valuable. Schedule 4-hour blocks for important work.",
    "Podcast episode: 'Software Engineering Daily' on PostgreSQL internals. MVCC (Multi-Version Concurrency Control) explanation was excellent. Now I understand why VACUUM is needed.",
    "Rewatching 'The Social Network' (2010). Still holds up. The 'you're gonna be left with just your pizza' scene — Aaron Sorkin dialogue at its best.",
    "Currently listening to 'Huberman Lab' podcast on sleep science. Light exposure in the morning, no bright light after 10 PM, cold room for better REM sleep. Implementing gradually.",
    "Reading 'Grokking Algorithms' by Aditya Bhargava. Great visual explanations of sorting, graph algorithms, dynamic programming. Good refresher before interviews.",
    "Finished 'Show Your Work' by Austin Kleon. Key message: share your process publicly. Build in public. People connect with the process, not just the polished final result.",
    "Movie night: Inception (2010). Still confused about the ending but the cinematography and Hans Zimmer soundtrack are timeless. Dream-within-a-dream makes more sense now.",
    "Book summary — 'How to Win Friends and Influence People' (Carnegie): don't criticize, give genuine appreciation, talk about what the other person wants. Basic but effective.",
    "Newsletter recommendation: 'The Pragmatic Engineer' by Gergely Orosz. Best newsletter for senior eng content. Covers system design, big tech insights, career advice.",
]

_JOURNAL = [
    "Today was a good coding day. Finished the hybrid retrieval implementation, ran the benchmark, wrote up the analysis. Feeling productive. Need more days like this.",
    "Feeling a bit lost about career direction. Backend engineering? AI engineering? Research? Startup? All of them appeal to me in different ways. Need to try more things to find out.",
    "Reflection: I procrastinate most when I'm anxious about the outcome. Realized that starting badly is better than not starting. The first 10 minutes are the hardest.",
    "Had a really good conversation with a senior (Karan) who's at Google London. He said his biggest regret was not building personal projects early. Now building KnowledgeVault feels even more worthwhile.",
    "The gap between what I know I should do and what I actually do is frustrating. I know I should exercise daily, sleep 8 hours, study consistently. But doing it is another thing.",
    "Three things I'm grateful for today: (1) my laptop didn't crash during the demo, (2) Sid gave good feedback on the architecture, (3) the capstone presentation went well.",
    "Goal: by May 1st, I want to have a full-time offer in hand, KnowledgeVault deployed and publicly shareable, and the capstone submitted. All three are achievable.",
    "The benchmark analysis was humbling. Built a hybrid retrieval system that sounds impressive but achieves exactly the same results as pure semantic search. Engineering requires honesty.",
    "Late night coding at 2 AM again. The problem is the motivation peaks at night when everyone is asleep. Need to shift this to morning. Consistent schedule is the goal.",
    "Starting to appreciate documentation more. Spent 30 minutes reading a confusing function only to realize there was a comment explaining it in another file. Write the comment.",
    "Imposter syndrome hit hard today during a mock interview. Forgot a standard DP optimization that I've coded before. Reminded myself: interviews test stress, not intelligence.",
    "The KnowledgeVault project is teaching me more than any course. Building something real — with real failures, real bugs, and real design decisions — is irreplaceable.",
    "Read about the 'maker vs manager schedule' concept by Paul Graham. Managers need meetings, makers need uninterrupted blocks. I'm a maker. Protect the blocks.",
    "Thinking about open-sourcing KnowledgeVault after graduation. The evaluation framework and hybrid retrieval implementation are genuinely interesting contributions. Write a blog post about it.",
    "Realized I've been avoiding the hardest problems by working on easier ones. Classic prioritization failure. Start with the most important and hardest thing every day.",
    "February productivity summary: 18 LeetCode problems solved, 3 blog posts drafted, capstone at 70% completion, KnowledgeVault evaluation framework built. Decent month.",
    "Note to future self: the period between 'no offers' and 'first offer' is the most anxious. Trust the process. Keep building, keep practicing. It will work out.",
    "Had a philosophical thought: the notes I'm taking now are evidence of who I am at this point. Future me will read these and see how I was thinking. Write clearly.",
    "A professor said something today that stuck: 'The best engineers are not the smartest — they're the most persistent.' Persistence over brilliance. Write that down.",
    "Today I fixed a bug that had been annoying me for 3 days. The fix was 2 lines. The investigation was the whole work. That's debugging.",
    "Feeling good about the capstone demo. The professors asked hard questions but I knew the answers. All those late nights studying the system design were worth it.",
    "My sleep schedule this semester: average 5.8 hours. That's not sustainable. Committing to 10:30 PM cutoff from next week. Phone on silent, laptop away.",
    "Read a LinkedIn post about someone who built a side project that got them an interview at a top company. My motivation to keep building KnowledgeVault just went up 10x.",
    "Thinking about what 'good engineering' means. Not just working code, but code that others can read, maintain, and extend. KnowledgeVault is teaching me to care about that.",
]

_DEBUGGING = [
    "Bug: Redis connection was timing out under load. Root cause: connection pool size (default 10) was exhausted with 15 concurrent workers. Fix: increased pool size to 50 in redis.StrictRedis.",
    "Debugging session: SQLAlchemy was making N+1 queries for notes with categories. Added `joinedload(Note.category)` to the query. Query count dropped from 51 to 1.",
    "Error: 'CUDA out of memory' when loading the embedding model. Fix: force CPU mode with `SENTENCE_TRANSFORMERS_HOME` and the CPU PyTorch wheel. No CUDA needed for inference at this scale.",
    "TypeError: 'NoneType' is not iterable. Root cause: forgot to check if `note.content` was None before calling `.split()`. Added null guard: `(note.content or '').split()`.",
    "Alembic migration failed: column already exists. Root cause: migration was run twice — the second run tried to add a column that was already created. Fix: add `IF NOT EXISTS` checks.",
    "Debugging a race condition: two workers picked up the same note simultaneously. Root cause: using `brpop` instead of `brpoplpush`. Fix: switched to reliable queue pattern with inflight list.",
    "FastAPI was returning 422 Unprocessable Entity for valid requests. Root cause: Pydantic model had `email: str` but the field was being sent as an EmailStr format that needed validation.",
    "Docker Compose service ordering issue: API started before migrations completed. Fix: added `depends_on: migrate: condition: service_completed_successfully` to the API service.",
    "Memory leak investigation: embedding model was being loaded on every request instead of once at startup. Fix: module-level singleton with `from app.core.embedding_model import embedding_model`.",
    "Infinite loop in the category reuse logic: new category was creating another category due to a recursive embedding similarity match. Added depth guard and unit test.",
    "KeyError in JSON parsing: the LLM occasionally returns `confidence` as a string ('0.85') instead of float. Fix: `float(data.get('confidence', 0.5))` with try/except.",
    "Bug: old embedding wasn't being updated when a note was edited. Root cause: the upsert used `note_id` as the key but checked `if embedding:` without committing first. Race condition on concurrent edits.",
    "Debugging Gemini API 429 errors during eval: the rate limit is 15 RPM. With pipeline + judge = 2 calls per query, max throughput is 7.5 queries/minute. Added 10s sleep between queries.",
    "Strange behavior: category embeddings were drifting toward 'general' topics over time. Root cause: `_refresh_category_embedding` was called on every assignment, averaging the category vector toward all assigned notes.",
    "Segmentation fault in the Docker container: was caused by the PyTorch CPU wheel having a CUDA stub that tried to load libcuda.so. Fixed by using the strict `--extra-index-url` CPU build.",
    "Pytest was importing the wrong `settings` object: production settings loaded from .env instead of test settings. Fix: use `monkeypatch.setenv` or a `conftest.py` that sets test environment variables.",
    "The streaming endpoint was sending malformed SSE. The format should be `data: {content}\\n\\n` but we were sending raw tokens. Fixed format but then client had to be updated too.",
    "JSON repair function was silently dropping valid nested objects. The regex `{.*}` with DOTALL was too greedy and matched across multiple JSON objects in a batch response.",
    "Database performance issue: the `organization_status` column was being queried without an index. Added `Index('ix_notes_org_status', Note.organization_status)` to the model.",
    "pgvector cosine_distance returns None for zero vectors. Fixed by adding a check: if embedding is all zeros, skip similarity search and return empty list.",
]

_LEARNING = [
    "Started the 'FastAPI Full Course' on Udemy. Excellent content. Key difference from Flask: async support, automatic OpenAPI docs, Pydantic for validation. Will use for all future projects.",
    "PostgreSQL tutorial resource: 'Use the Index, Luke' (use-the-index-luke.com). Best free resource for understanding how DB indexes actually work. Covers B-tree, range scans, partitioning.",
    "Completed 'CS50 Web Programming' by Harvard. Django section was useful for understanding MTV pattern. FastAPI is better for APIs but Django Admin is genuinely impressive.",
    "Reading the Gemini API documentation. Key APIs: generateContent, streamGenerateContent, responseSchema for structured output. The schema enforcement is more reliable than prompt-based JSON extraction.",
    "Redis documentation note: LPUSH adds to left, RPUSH to right. LPOP/RPOP remove from respective ends. LRANGE fetches a range. BRPOPLPUSH is deprecated in Redis 6.2, use BLMOVE.",
    "Learning about Docker networking: bridge network (default, containers can communicate by name), host network (container shares host network, fast but less isolated), overlay (for Docker Swarm).",
    "pgvector extension guide: after installing, `CREATE EXTENSION vector`. Create a column: `embedding vector(384)`. Index: `CREATE INDEX ON table USING ivfflat (embedding vector_cosine_ops)`. Query: `embedding <=> query_vector`.",
    "Learned Python's asyncio model: single-threaded event loop, coroutines yield control with `await`. Perfect for I/O-bound tasks. For CPU-bound, need ProcessPoolExecutor.",
    "SQLAlchemy 2.0 tutorial: moved from Query API to `select()` statement. `db.execute(select(User)).scalars().all()`. Cleaner syntax, better typing support.",
    "Kubernetes basics: Pod (smallest deployable unit, 1+ containers), Deployment (manages Pod replicas), Service (stable network endpoint for Pods), ConfigMap (environment configuration).",
    "GitHub Actions: workflows defined in `.github/workflows/*.yml`. Triggers: push, pull_request, schedule. Jobs run in parallel by default. Steps run sequentially within a job.",
    "Terraform basics: infrastructure as code for cloud providers. Define resources in `.tf` files. `terraform plan` previews changes. `terraform apply` executes. State stored in `.tfstate`.",
    "Learning about database transactions and isolation levels: Read Uncommitted, Read Committed (PostgreSQL default), Repeatable Read, Serializable. Each prevents different anomalies.",
    "Prometheus + Grafana setup: Prometheus scrapes metrics from application endpoints. Grafana visualizes. FastAPI can expose metrics via `prometheus-fastapi-instrumentator`.",
    "GraphQL vs REST: GraphQL lets clients request exactly the data they need, avoids over-fetching. But harder to cache, more complex server implementation. REST is simpler for CRUD APIs.",
    "OAuth 2.0 flow: Authorization Code (web apps, most secure), Implicit (browser apps, deprecated), Client Credentials (service-to-service), Device Code (IoT/CLIs).",
    "WebAssembly (WASM): runs near-native code in the browser. Rust, C, C++ can compile to WASM. Use cases: games, video editing, compute-intensive tasks. Python now runs in browser via Pyodide.",
    "Learned about idempotency: a request that can be applied multiple times without changing the result beyond the first application. Crucial for payment systems and distributed systems.",
    "Nginx as reverse proxy: routes requests to backend services, handles SSL termination, load balancing. Config: `proxy_pass http://backend:8000` in a location block.",
    "Celery for Python task queues: broker (Redis/RabbitMQ), workers, tasks. `@app.task def process(): ...`. Call with `.delay()`. Monitor with Flower. Alternative to the custom Redis worker.",
    "Read about Blue-Green deployments: two identical environments, switch traffic from Blue to Green after deployment. Instant rollback by switching back. Requires double infrastructure.",
    "Learned about the Twelve-Factor App methodology: config in environment, stateless processes, port binding, dev/prod parity, disposability. KnowledgeVault follows most of these.",
    "Type-safe Python with mypy: strict mode catches many bugs at compile time. Add `--strict` to mypy config. Common issues: Optional[T] not handled, Any leaking through.",
    "Docker multi-stage builds: separate build environment from runtime image. Example: compile Go binary in `golang` image, copy only the binary to `scratch` or `alpine`. Dramatically smaller images.",
    "Learned about CORS (Cross-Origin Resource Sharing): browsers block requests to different origins without proper headers. FastAPI CORS middleware: `from fastapi.middleware.cors import CORSMiddleware`.",
    "Rate limiting algorithms: fixed window is simplest (count per time bucket), token bucket is smooth (tokens replenish continuously), leaky bucket is strict (constant drain rate).",
    "Serverless vs containers: serverless scales to zero (cheaper for sporadic traffic), containers are always warm (better for steady traffic), serverless has cold starts, containers have idle costs.",
    "OWASP Top 10 for web security: Injection, Broken Auth, Sensitive Data Exposure, XXE, Broken Access Control, Security Misconfiguration, XSS, Insecure Deserialization, Using Vulnerable Components, Insufficient Logging.",
    "Regular expressions cheat sheet: `.` any char, `*` zero or more, `+` one or more, `?` optional, `^` start, `$` end, `\\d` digit, `\\w` word char, `[abc]` char class, `(?:)` non-capturing group.",
    "Learning about service discovery: in Docker Compose, services discover each other by name. In Kubernetes, services get DNS entries. In bare-metal, use Consul or etcd.",
]

_RESEARCH = [
    "Research note: RAFT consensus algorithm. Leader election, log replication, safety guarantees. More understandable than Paxos. Used in etcd, CockroachDB, TiKV.",
    "Reading about cache replacement policies: LRU evicts least recently used, LFU evicts least frequently used, ARC adapts between LRU and LFU based on hit rates.",
    "Research on Transformer architecture: encoder-only (BERT — understanding tasks), decoder-only (GPT — generation), encoder-decoder (T5 — seq2seq). BERT uses bidirectional attention.",
    "Reading about FAISS (Facebook AI Similarity Search): efficient similarity search and clustering of dense vectors. IVF index (Inverted File Index) for approximate search. GPU-optimized.",
    "Survey on RAG architectures: Naive RAG, Advanced RAG, Modular RAG. Advanced RAG adds pre-retrieval (query expansion, routing) and post-retrieval (reranking, context compression).",
    "Research on knowledge graph integration with RAG: entities extracted from text, linked to a KG, structured facts retrieved alongside text chunks. Improves factual accuracy.",
    "Reading: 'Attention Is All You Need' (Vaswani et al. 2017). Self-attention mechanism replaced recurrence. Positional encoding preserves sequence order. Still the foundational paper for LLMs.",
    "Research note on evaluation metrics: BLEU (n-gram overlap, for translation), ROUGE (recall-oriented, for summarization), BERTScore (contextual embedding similarity, more semantic).",
    "Reading about Mixture of Experts (MoE): sparse model where different parts activate for different inputs. Mistral 8x7B uses MoE. More efficient than dense models at same parameter count.",
    "Research on instruction tuning: fine-tune base LLM on (instruction, response) pairs. RLHF adds human preference signal. Makes models follow instructions vs just predicting next token.",
    "Paper notes: 'REALM' (Retrieval Enhanced Language Models). First end-to-end RAG with the retriever trained jointly with the reader. Showed retrieval quality drives answer quality.",
    "Research interest: temporal reasoning in RAG systems. Current systems don't understand 'notes from this month' or 'what happened last week'. Need metadata-based filtering.",
    "Note on DPO (Direct Preference Optimization): an alternative to RLHF. Directly optimizes the language model using preference data without a separate reward model. Simpler training.",
    "Survey finding: RAG systems degrade significantly when the relevant document is not retrieved (precision miss). Retrieval accuracy gates answer quality — confirms the KnowledgeVault benchmark findings.",
    "Reading about multi-modal RAG: retrieve from text, images, and audio simultaneously. CLIP embeddings allow text-image retrieval. Useful for rich knowledge bases.",
]

_TECHNICAL_DOCS = [
    "FastAPI dependency injection: use `Depends()` for shared logic. Database sessions, auth verification, rate limiting all implemented as dependencies. Composable and testable.",
    "PostgreSQL EXPLAIN ANALYZE: prepend to any query to see the execution plan with actual timings. Look for Sequential Scans on large tables — those need an index.",
    "Alembic migration workflow: `alembic revision --autogenerate -m 'description'` (generates migration from model changes), `alembic upgrade head` (applies all pending), `alembic downgrade -1` (rolls back one).",
    "SQLAlchemy session management: always use context managers or explicit close(). Unclosed sessions leak connections. In FastAPI: `yield db` with `finally: db.close()` in the dependency.",
    "pgvector installation on local PostgreSQL: `CREATE EXTENSION IF NOT EXISTS vector;`. Requires pgvector shared library. In Docker use `pgvector/pgvector:pg16` image.",
    "Pydantic v2 migration: `.dict()` is now `.model_dump()`, `.from_orm()` is now `model_validate()`, `Config` class is now `model_config = ConfigDict(...)`. Breaking changes from v1.",
    "JWT token structure: header.payload.signature. Header: algorithm type. Payload: claims (sub, exp, iat). Signature: HMAC(base64(header) + '.' + base64(payload), secret).",
    "Docker health check in Compose: `test: ['CMD-SHELL', 'pg_isready -U user']`, `interval: 5s`, `timeout: 3s`, `retries: 10`. `depends_on: condition: service_healthy` waits for this.",
    "Uvicorn workers: `uvicorn main:app --workers 4` runs 4 separate processes. Each has its own event loop and connection pool. State is NOT shared between workers.",
    "Redis data types: String (counter, cache), Hash (user session), List (queue), Set (unique tags), Sorted Set (leaderboard), Stream (event log). Choose based on access pattern.",
    "Bcrypt password hashing: intentionally slow to resist brute force. Work factor (cost) determines rounds. Default 12 means 2^12 rounds. Higher = slower to crack, slower to verify.",
    "Environment variable management: never commit .env to Git. Use .env.example as a template. `python-dotenv` loads .env automatically. Pydantic Settings handles validation and defaults.",
    "GitHub Actions secret management: add secrets in repo Settings → Secrets. Access in workflow as `${{ secrets.SECRET_NAME }}`. Never echo secrets in workflow output.",
    "pytest fixtures: `@pytest.fixture` creates reusable setup/teardown. `scope='session'` runs once per test session. Use `yield` for teardown code after the fixture.",
    "curl cheat sheet: `-X POST` sets method, `-H 'Content-Type: application/json'` sets header, `-d '{}'` sends body, `-b cookie.txt -c cookie.txt` handles cookies, `-v` verbose output.",
    "Logging configuration: use `logging.basicConfig(level=logging.INFO)` at entry point. Use `logger = logging.getLogger(__name__)` in each module. Use structured logging (JSON) in production.",
    "SQLAlchemy relationship loading strategies: lazy (default, N+1 problem), eager with `joinedload` (single JOIN query), `selectinload` (separate IN query). Choose based on access patterns.",
    "Dockerfile best practices: multi-stage builds, minimize layers, copy requirements before code, use .dockerignore, pin versions, run as non-root user, use COPY not ADD.",
    "Nginx rate limiting: `limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;` then `limit_req zone=api burst=20 nodelay;` in location block. Returns 429 when exceeded.",
    "SSL certificate with Certbot: `certbot --nginx -d domain.com`. Auto-renews with systemd timer. Make sure port 80 and 443 are open in firewall. Let's Encrypt certificates expire every 90 days.",
]

_PROGRAMMING_2 = [
    "Python `property` decorator creates managed attributes. Getter, setter, and deleter. Useful for validation or computed values without changing the public API.",
    "Learned about monkey patching: replacing or extending code at runtime. Useful in tests to replace external calls. Dangerous in production — hard to debug.",
    "List vs tuple in Python: lists are mutable, tuples are immutable. Tuples are slightly faster to create and iterate. Use tuples for heterogeneous data (like struct), lists for homogeneous sequences.",
    "f-strings are faster than `.format()` and `%` formatting in Python 3.6+. For complex formatting, f-strings are also more readable. `f'{value:.2f}'` for two decimal places.",
    "Python packaging: `pyproject.toml` is the modern standard. `setuptools`, `poetry`, `hatch` are build backends. `pip install -e .` for editable installs during development.",
    "Learned about Python descriptors: implement `__get__`, `__set__`, `__delete__`. Django ORM model fields are descriptors. SQLAlchemy `Column` is a descriptor.",
    "Regex lookahead `(?=pattern)` matches position before pattern without consuming. Lookbehind `(?<=pattern)` matches position after pattern. Zero-width assertions.",
    "The `__enter__` and `__exit__` methods make a class a context manager. `__exit__` receives exception info — return True to suppress the exception.",
    "`collections.defaultdict(list)` creates a dict that auto-initializes missing keys to an empty list. `defaultdict(int)` for counting. Cleaner than `dict.setdefault`.",
    "Python `enumerate(iterable, start=0)` adds an index. Better than `for i in range(len(lst))`. `for i, val in enumerate(lst): ...`.",
    "Learned about `__repr__` vs `__str__`: `__repr__` is for developers (unambiguous, eval-able if possible), `__str__` is for end users. `repr()` calls `__repr__`, `str()` calls `__str__`.",
    "Python generator expressions save memory: `(x**2 for x in range(1000000))` doesn't build the list. Chain with `sum()`, `max()`, etc. for lazy evaluation.",
    "JavaScript event loop: call stack, callback queue, microtask queue. Promises go to microtask queue (processed before next macro-task). `setTimeout` goes to macro-task queue.",
    "TypeScript discriminated unions: add a `kind` or `type` field to distinguish union members. TypeScript can narrow the type based on checking that field.",
    "SQL `COALESCE(a, b, c)` returns the first non-null value. Useful for default values in queries. `NULLIF(a, b)` returns null if a == b.",
    "Learned about SQL CTEs (Common Table Expressions): `WITH cte AS (SELECT ...) SELECT ... FROM cte`. Readable, reusable within the query, enables recursion.",
    "Go `defer` runs after the surrounding function returns. LIFO order. Use for cleanup (file close, mutex unlock). Deferred functions execute even if there's a panic.",
    "Go error handling pattern: `if err != nil { return fmt.Errorf('operation failed: %w', err) }`. Wrap errors with context. Unwrap with `errors.Is` and `errors.As`.",
    "Rust `Result<T, E>`: `Ok(value)` or `Err(error)`. `?` operator propagates errors. `match result { Ok(v) => ..., Err(e) => ... }` for handling.",
    "Shell scripting: `set -e` exits on first error. `set -u` treats unset variables as errors. `set -o pipefail` catches errors in pipes. Always use these three together.",
    "AWK for log processing: `awk '{print $2}' log.txt` prints second field. `awk -F',' '{sum+=$3} END {print sum}' data.csv` sums the third CSV column.",
    "vim productivity: `:w` save, `:q!` quit without save, `dd` delete line, `yy` yank (copy) line, `p` paste, `/pattern` search, `n` next match, `:%s/old/new/g` replace all.",
    "Make a minimal reproducible example before asking for help. Reduces the problem to its essence, often reveals the bug in the process. MCVE is the standard.",
    "Learned: `git stash` saves uncommitted changes, `git stash pop` restores them. `git stash list` shows all stashes. `git stash drop stash@{0}` removes a specific stash.",
    "Python `pathlib.Path` is better than `os.path`. `Path(__file__).parent` is cleaner than `os.dirname(__file__)`. Works on Windows and Linux without path separator issues.",
]

_AI_ML_2 = [
    "Learned about PEFT (Parameter-Efficient Fine-Tuning): LoRA (Low-Rank Adaptation) adds trainable low-rank matrices to frozen model weights. Trains <1% of parameters.",
    "Vector quantization: compresses high-dimensional vectors to discrete codes. Used in image generation (VQ-VAE), audio (EnCodec), and database compression (PQ — Product Quantization).",
    "Sparse attention mechanisms: instead of attending to all tokens (O(n²)), attend to a subset. Longformer uses sliding window + global attention. BigBird uses random + sliding + global.",
    "Tool use / function calling in LLMs: the model selects a tool and arguments from a schema. Works via special tokens or structured generation. Powers AI agents.",
    "Chain-of-thought prompting: `Let's think step by step`. Significantly improves performance on reasoning tasks. Few-shot CoT (with examples) is stronger than zero-shot.",
    "Constitutional AI (Anthropic): fine-tune LLM using self-critique and revision guided by a list of principles. More scalable than human preference labeling at scale.",
    "Embeddings for classification: embed text, train a small classifier on top of the frozen embeddings. Much faster than fine-tuning the full model.",
    "Document chunking strategies comparison: fixed-size (simple), sentence-based (semantic), paragraph-based (good default), semantic chunking (split at topic boundaries using embedding similarity).",
    "RAG failure modes: (1) retrieval miss — relevant doc not in top-K, (2) context window overflow — too much context confuses model, (3) hallucination — model ignores context entirely.",
    "Gemini 2.0 Flash: 1M token context, multimodal (text+image+audio), function calling, structured output via responseSchema. Free tier: 15 RPM. Significantly faster than GPT-4.",
    "Ollama for local LLM inference: `ollama run llama3` pulls and serves the model locally. REST API compatible with OpenAI format. Good for dev/privacy-sensitive use cases.",
    "Benchmark datasets for RAG evaluation: HotpotQA (multi-hop), TriviaQA (factual), Natural Questions (Google search queries), MS MARCO (passage ranking).",
    "Calibration in ML: a well-calibrated model's confidence scores match actual accuracy. If model says 80% confidence, it should be correct 80% of the time. ECE (Expected Calibration Error) measures this.",
    "Distillation: train a smaller student model to mimic a larger teacher model. Student learns from soft probability distributions (temperature-scaled logits) rather than hard labels.",
    "Vector dimension reduction: PCA reduces dimensions while preserving maximum variance. UMAP preserves local neighborhood structure better. Useful for visualizing embeddings.",
    "Chunking overlap rationale: if a sentence spans a chunk boundary, it gets split. The overlap carries the tail of the previous chunk into the next so queries about boundary-spanning content succeed.",
    "Neural network training tip: use learning rate warmup (gradually increase LR from small value) followed by cosine decay. Prevents early instability and ensures good convergence.",
    "Few-shot learning vs zero-shot: few-shot includes examples in the prompt. Zero-shot relies entirely on instruction. Few-shot is more reliable but uses more tokens.",
    "Token counting: GPT tokenizer averages ~4 characters per token for English. `tiktoken` library counts exactly. Important for staying within context limits.",
    "Attention head interpretation: different heads learn different patterns. Some heads attend to syntactic structure, others to coreference, others to positional proximity.",
]

_UNIVERSITY_2 = [
    "Completed the database design assignment: ER diagram for a hospital management system. Entities: Patient, Doctor, Appointment, Ward, Medication. Junction table for many-to-many relationships.",
    "Lecture notes — Memory Management: static allocation (compile-time), stack allocation (automatic, LIFO), heap allocation (manual or GC). Stack is faster but limited in size.",
    "Study note — CPU Pipelining: fetch, decode, execute, memory, write-back. Pipeline hazards: structural (resource conflict), data (dependency), control (branch).",
    "Networking assignment: implement a basic HTTP server in Python using raw sockets. Parse the HTTP request line, headers, and body. Send a valid HTTP response.",
    "Professor's advice for placements: communication skills matter as much as technical skills. Practice explaining technical decisions clearly. Write clean, commented code in interviews.",
    "OS lab: implemented producer-consumer problem using semaphores in C. `sem_wait` and `sem_post` for signaling. Tricky to avoid deadlock when both semaphores are held.",
    "Studied file systems today: FAT (File Allocation Table), ext4 (Linux), NTFS (Windows). Inodes in Linux: metadata about a file (permissions, timestamps, data block pointers).",
    "Compiler design assignment: implement a lexer for a subset of C using a DFA. Tokenize keywords, identifiers, numbers, operators. Output: (token_type, value) pairs.",
    "Data structures revision: skip list is a probabilistic alternative to balanced BST. O(log n) expected for search, insert, delete. Used in Redis for sorted sets.",
    "Learned about NUMA (Non-Uniform Memory Access) in multiprocessors. Memory access time depends on which processor's memory is being accessed. NUMA-aware code keeps data local to the CPU using it.",
    "Studied the Linux kernel scheduler: CFS (Completely Fair Scheduler). Uses a red-black tree sorted by virtual runtime. Fair to all processes. Replaces the earlier O(1) scheduler.",
    "Assignment on parallel programming with OpenMP: `#pragma omp parallel for` distributes loop iterations across threads. Race conditions on shared variables. Use `reduction` clause.",
    "Discrete Math revision: permutations `P(n,r) = n!/(n-r)!`, combinations `C(n,r) = n!/(r!(n-r)!)`. Probability: conditional probability, Bayes theorem, independence.",
    "DBMS lab: wrote stored procedures and triggers in PostgreSQL. Trigger to auto-update `updated_at` timestamp on row modification. Useful for audit trails.",
    "Theory of Computation: pumping lemma for regular languages. If L is regular, every string of length ≥ p can be pumped. Use to prove languages are not regular.",
]

_INTERVIEW_PREP_2 = [
    "LeetCode problem: Maximum Depth of Binary Tree. Simple DFS: `return max(depth(root.left), depth(root.right)) + 1 if root else 0`. O(n) time.",
    "LeetCode: Longest Palindromic Substring. Expand around center approach — for each character (and pair), expand outward while characters match. O(n²) time, O(1) space.",
    "LeetCode: Word Break. DP: `dp[i] = True if dp[j] and s[j:i] in wordDict for any j`. Build from left. O(n² × max_word_len) time.",
    "LeetCode: Coin Change. Classic DP: `dp[amount] = min(dp[amount], dp[amount - coin] + 1)`. Initialize dp[0]=0, rest to infinity. O(amount × len(coins)).",
    "LeetCode: Number of Islands. BFS/DFS to mark connected land cells as visited. Count how many times we start a new BFS/DFS. O(m×n) time and space.",
    "System design: design a notification service. Components: API to create notifications, priority queue (SQS/Kafka), worker pool, delivery adapters (email/SMS/push), retry logic, dead letter queue.",
    "System design: design a real-time leaderboard. Redis Sorted Set: `ZADD leaderboard score user_id`, `ZREVRANK leaderboard user_id` for rank. O(log n) operations.",
    "FAANG interview insight: interviewers care about how you handle ambiguity. Ask clarifying questions before coding. State your assumptions explicitly.",
    "LeetCode practice schedule: 2 easy + 1 medium per day. Focus on patterns: sliding window, two pointers, binary search, DFS/BFS, DP. Don't grind randomly — master patterns.",
    "System design: design Instagram. Storage: metadata in PostgreSQL, images in S3 with CDN, user feed via pre-computed timeline (fan-out on write for small following, fan-out on read for large).",
    "Behavioral prep: 'Tell me about a time you disagreed with your team.' Story: disagreed on using microservices for capstone — advocated for monolith first. Team agreed after discussion.",
    "Mock interview tip: say `I'm going to start with a brute force approach` before diving into optimization. Shows structured thinking. Never jump to optimization without explaining the naive solution.",
    "LeetCode: Trapping Rain Water. Two-pointer approach: left and right pointers, maintain max height from each side. Water at index = min(leftMax, rightMax) - height[i]. O(n) time.",
    "Competitive programming contest strategy: read all problems first, sort by estimated difficulty, solve easy problems first to accumulate points, then try harder ones.",
    "Resume bullet point: 'Built KnowledgeVault — an AI-powered RAG system using FastAPI, pgvector, Redis, and Gemini API. Implemented hybrid semantic-intent retrieval with LLM-as-judge evaluation.' Solid.",
]

_STARTUPS_2 = [
    "SaaS metrics to know: MRR (Monthly Recurring Revenue), ARR (Annual), Churn Rate, CAC (Customer Acquisition Cost), LTV (Lifetime Value). LTV/CAC > 3 is healthy.",
    "Idea: subscription-based API for Indian government data (DPIIT company data, MCA filings, court orders). Developers would pay Rs 999/month for clean, structured access.",
    "Product-market fit signals: users who would be 'very disappointed' if the product disappeared > 40%. Metric from Sean Ellis. Survey your users.",
    "Startup legal checklist: incorporate (LLP or Pvt Ltd), file for GST, open a current account, register on DPIIT startup India for tax exemptions.",
    "Read about zero-to-one companies: creating something entirely new. Peter Thiel's criteria: 10x better than competition (or different enough to be its own category), proprietary technology, network effects.",
    "Build in public strategy: tweet daily about what you built, what broke, and what you learned. Builds audience before launch. DHH, Pieter Levels, Marc Lou do this.",
    "Idea: AI writing assistant for Indian legal documents. LLMs are bad at Indian legal language. Fine-tuning on Indian judgements + legislative text could produce a niche, high-value product.",
    "Fundraising note: Angel investors in India invest Rs 25L–2Cr typically. VCs start at Rs 5Cr+ (seed). First get revenue or product traction before seeking VC.",
    "Competitive moat thinking: for KnowledgeVault, the moat is personal data (notes are private and valuable), network effects are weak (personal tool), switching cost is moderate (export is possible).",
    "Startup mistake: building in secret for 6 months before showing anyone. Talk to users as early as possible. Build for 1 user who loves it before scaling to 100.",
]

_HEALTH_2 = [
    "Supplement stack: Vitamin D3 (4000 IU, once deficient), Magnesium Glycinate (400mg before bed — better sleep), Omega-3 Fish Oil (1000mg), Zinc (15mg). All evidence-based.",
    "Cold shower benefits: improved mood (norepinephrine spike), alertness, resilience training. Start with 30 seconds at the end of a warm shower. Build to 2-3 minutes.",
    "Ideal morning routine: wake at 6:30, no phone for first 30 minutes, glass of water, 10 minutes meditation, 20 minutes workout or walk. Grounding before the digital world hits.",
    "Caffeine tolerance break: take 2 weeks off coffee every 2-3 months. Resets sensitivity so normal doses work again. Week 1 is hard. Week 2 energy stabilizes.",
    "Learned about sleep cycles: 90-minute cycles. Wake up at a cycle boundary (7.5 hours = 5 cycles) to feel more rested than 8 hours (interrupts mid-cycle).",
    "Running form tips: land midfoot not heel, slight forward lean, arms relaxed at 90 degrees, cadence ~170-180 steps/minute. Good form prevents injuries.",
    "Intermittent fasting experiment: 16:8 (eat noon to 8 PM). Week 1 rough. Week 2 easier. Energy is surprisingly stable. Blood work: blood sugar improved slightly.",
    "Ergonomic setup: monitor at eye level (add a stand), keyboard at a height where elbows are at 90°, lumbar support, feet flat on floor. Preventing RSI is easier than treating it.",
    "Social health matters: schedule time for friends intentionally, not just when it happens. Loneliness is correlated with worse health outcomes than smoking. Prioritize relationships.",
    "Journaling for anxiety: 'morning pages' technique — write 3 pages of anything, stream of consciousness, every morning. Clears the mental buffer, surfaces hidden worries.",
]

_MISC = [
    "Random thought: the best way to learn a technology is to build something real with it, break it, debug it, and build it again. Tutorials only get you so far.",
    "Productivity hack: use the Pomodoro technique — 25 minutes focused work, 5 minute break. After 4 cycles take a longer break. Keeps me from doomscrolling mid-task.",
    "Realized I should start building in public on Twitter. Share the process — bugs, design decisions, benchmark results. Builds credibility and attracts collaborators.",
    "Note: don't optimize prematurely. Get it working first, then measure, then optimize only the bottleneck. 'Premature optimization is the root of all evil' — Knuth.",
    "Interesting comparison: being a software engineer is like being a writer. The first draft (prototype) is always ugly. Refactoring is editing. Ship the revised draft.",
    "Good engineering takes courage: the courage to say 'this doesn't work', 'I was wrong', 'let's delete this and start over'. Ego is the enemy of good technical judgment.",
    "Overheard in the lab: 'If it works in development, ship to production. If it breaks, that's why we have backups.' Terrible advice but also kind of relatable.",
    "The best documentation is code that doesn't need documentation. But when you do write comments, explain WHY, not WHAT. The code already says what.",
    "Caffeine dependence is real. Skipped coffee yesterday and had a headache by 3 PM. The dependency makes me less productive in aggregate even though it helps in the short term.",
    "Random thought: 10 years from now, AI will write most boilerplate code. The valuable skill will be knowing what to build and why, not how to write a for loop.",
    "Interesting problem: the more you know, the more you realize how much you don't know. Early in CS, I thought I was almost done learning. Now the map of unknown territory keeps expanding.",
    "Good debugging session: rubber duck debugging actually works. Explaining the problem out loud to an inanimate object forces you to articulate assumptions and often reveals the bug.",
    "Career advice I keep getting: specialize deeply in one area, then branch out. T-shaped skills. My T: backend Python/FastAPI with a branch toward AI/ML engineering.",
    "The three-day rule for tech decisions: if a design decision still seems right after three days, proceed. Immediate enthusiasm can mislead.",
    "Observation: the best engineers I've met are characterized by intellectual humility — they're confident in their skills but quick to say 'I don't know' and go find out.",
    "Writing this note because I need to remember: it's okay to not have everything figured out at 21. Keep building, keep learning, take care of your health. The rest will follow.",
    "The feeling when a complex bug is finally fixed: immediate relief, then the realization that you spent 4 hours on 2 lines of code. Engineering.",
    "Thinking about digital minimalism: I have 7 different note-taking apps and still can't find my notes. KnowledgeVault is meant to solve this. 'Eating your own dog food' is real.",
    "Random observation: meetings that could have been emails, emails that could have been messages, messages that could have been a comment in the code. Communication debt is real.",
    "Philosophy note: 'A complex system that works is invariably found to have evolved from a simple system that works.' Start simple. Add complexity only when necessary.",
]

# Mix all domain lists into one flat list
_PROGRAMMING = _PROGRAMMING + _PROGRAMMING_2
_AI_ML = _AI_ML + _AI_ML_2
_UNIVERSITY = _UNIVERSITY + _UNIVERSITY_2
_INTERVIEW_PREP = _INTERVIEW_PREP + _INTERVIEW_PREP_2
_STARTUPS = _STARTUPS + _STARTUPS_2
_HEALTH = _HEALTH + _HEALTH_2


import random

_ALL_GROUPS = (
    _PROGRAMMING * 1 +
    _AI_ML * 1 +
    _UNIVERSITY * 1 +
    _INTERVIEW_PREP * 1 +
    _PROJECT_KVAULT * 1 +
    _SYSTEM_DESIGN * 1 +
    _MEETINGS * 1 +
    _REMINDERS_TASKS * 1 +
    _SHOPPING_FINANCE * 1 +
    _TRAVEL * 1 +
    _HEALTH * 1 +
    _STARTUPS * 1 +
    _BOOKS_MEDIA * 1 +
    _JOURNAL * 1 +
    _DEBUGGING * 1 +
    _LEARNING * 1 +
    _RESEARCH * 1 +
    _TECHNICAL_DOCS * 1 +
    _MISC * 1
)

# Shuffle with a fixed seed so the order is reproducible
_rng = random.Random(42)
NOTES = list(_ALL_GROUPS)
_rng.shuffle(NOTES)

# Pad to exactly 1000 with a second pass from the longest lists
_EXTRA = (
    _PROGRAMMING[:10] +
    _AI_ML[:10] +
    _LEARNING[:10] +
    _TECHNICAL_DOCS[:10] +
    _UNIVERSITY[:10] +
    _INTERVIEW_PREP[:10] +
    _PROJECT_KVAULT[:10] +
    _DEBUGGING[:10] +
    _JOURNAL[:10] +
    _SYSTEM_DESIGN[:10]
)
_rng.shuffle(_EXTRA)

_extra_idx = 0
_EXTRA_CYCLE = _EXTRA * 5  # enough headroom
while len(NOTES) < 1000 and _extra_idx < len(_EXTRA_CYCLE):
    NOTES.append(_EXTRA_CYCLE[_extra_idx])
    _extra_idx += 1

NOTES = NOTES[:1000]

if __name__ == "__main__":
    # Domain statistics
    domain_sizes = {
        "programming": len(_PROGRAMMING),
        "ai_ml": len(_AI_ML),
        "university": len(_UNIVERSITY),
        "interview_prep": len(_INTERVIEW_PREP),
        "project_kvault": len(_PROJECT_KVAULT),
        "system_design": len(_SYSTEM_DESIGN),
        "meetings": len(_MEETINGS),
        "reminders_tasks": len(_REMINDERS_TASKS),
        "shopping_finance": len(_SHOPPING_FINANCE),
        "travel": len(_TRAVEL),
        "health": len(_HEALTH),
        "startups": len(_STARTUPS),
        "books_media": len(_BOOKS_MEDIA),
        "journal": len(_JOURNAL),
        "debugging": len(_DEBUGGING),
        "learning": len(_LEARNING),
        "research": len(_RESEARCH),
        "technical_docs": len(_TECHNICAL_DOCS),
        "misc": len(_MISC),
    }
    total = sum(domain_sizes.values())
    print(f"Total notes in dataset: {len(NOTES)}")
    print(f"Base domain total:      {total}")
    for domain, count in sorted(domain_sizes.items(), key=lambda x: -x[1]):
        print(f"  {domain:<20}: {count}")
