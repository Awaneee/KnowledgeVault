# KnowledgeVault Evaluation Report

**Run ID:** `f80eebc3-83aa-4039-b894-894334bce6bf`

**Created:** 2026-08-03T21:11:06.151756

**Git Commit:** `21b6bf3`

**Benchmark Version:** `2.0.0`

**Queries:** 50

**K:** 5

**Corpus Coverage:** 42.3% (fraction of notes touched across all retrieved sets)

## Strategy Comparison

| Strategy | Precision | Recall | Hit Rate | MRR | MRR 95% CI | MAP@K | R-Prec | nDCG | Intent Acc | Category Acc | Avg Latency (ms) |
|-----------|----------:|-------:|---------:|----:|:----------:|------:|-------:|-----:|------------:|-------------:|-----------------:|
| SEMANTIC | 0.244 | 0.547 | 0.760 | 0.612 | [0.492, 0.730] | 0.421 | 0.385 | 0.503 | - | - | 2.17 |
| INTENT | 0.068 | 0.129 | 0.280 | 0.221 | [0.117, 0.330] | 0.101 | 0.099 | 0.135 | 0.460 | 0.500 | 28.97 |
| HYBRID | 0.240 | 0.543 | 0.760 | 0.620 | [0.504, 0.736] | 0.418 | 0.383 | 0.500 | 0.460 | 0.500 | 82.46 |
| RERANK | 0.240 | 0.543 | 0.760 | 0.619 | [0.501, 0.735] | 0.418 | 0.383 | 0.500 | 0.460 | 0.500 | 82.13 |
| BM25 | 0.028 | 0.083 | 0.140 | 0.140 | [0.040, 0.240] | 0.083 | 0.083 | 0.096 | - | - | 1.76 |
| HYBRID_BM25 | 0.240 | 0.537 | 0.760 | 0.609 | [0.487, 0.730] | 0.405 | 0.367 | 0.489 | - | - | 25.49 |

## Statistical Comparisons (95% Bootstrap CI)

| Comparison | ΔMRR | MRR CI | Significant | ΔHIT | Hit CI | Recommendation |
|-----------|-----:|:------:|:-----------:|-----:|:------:|:--------------|
| HYBRID vs SEMANTIC | +0.0080 | [0.000, 0.017] | ✗ | +0.0000 | [0.000, 0.000] | insufficient_evidence |
| RERANK vs HYBRID | -0.0012 | [-0.004, 0.000] | ✗ | +0.0000 | [0.000, 0.000] | insufficient_evidence |
| BM25 vs SEMANTIC | -0.4723 | [-0.588, -0.353] | ✓ | -0.6200 | [-0.760, -0.480] | keep_baseline |
| HYBRID_BM25 vs HYBRID | -0.0117 | [-0.027, 0.000] | ✗ | +0.0000 | [0.000, 0.000] | insufficient_evidence |

## Per-Difficulty Breakdown

| Strategy | Easy MRR | Hard MRR | Medium MRR |
| --- | ---: | ---: | ---: |
| BM25 | 0.182 | 0.000 | 0.067 |
| HYBRID | 0.591 | 1.000 | 0.635 |
| HYBRID_BM25 | 0.573 | 1.000 | 0.635 |
| INTENT | 0.268 | 0.500 | 0.080 |
| RERANK | 0.589 | 1.000 | 0.635 |
| SEMANTIC | 0.581 | 1.000 | 0.630 |

## Query Results

### SEMANTIC — What startup ideas do I have?

- **Benchmark ID:** 1
- **Difficulty:** easy
- **Relevant Notes:** [85, 86, 87]
- **Retrieved Notes:** [85, 525, 617, 134, 441]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.333 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.333 |
| R-Precision | 0.333 |
| Latency (ms) | 33.35 |

---

### SEMANTIC — Show my AI research reading goals

- **Benchmark ID:** 2
- **Difficulty:** easy
- **Relevant Notes:** [65, 64, 66, 67]
- **Retrieved Notes:** [529, 617, 416, 85, 230]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 0.99 |

---

### SEMANTIC — How can I improve my health?

- **Benchmark ID:** 3
- **Difficulty:** medium
- **Relevant Notes:** [83, 84]
- **Retrieved Notes:** [84, 109, 83, 79, 286]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 1.000 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.833 |
| R-Precision | 0.500 |
| Latency (ms) | 2.01 |

---

### SEMANTIC — Show my finance reminders

- **Benchmark ID:** 4
- **Difficulty:** easy
- **Relevant Notes:** [77, 82]
- **Retrieved Notes:** [216, 312, 82, 77, 393]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 1.000 |
| Hit | True |
| Reciprocal Rank | 0.333 |
| MAP@5 | 0.417 |
| R-Precision | 0.000 |
| Latency (ms) | 1.33 |

---

### SEMANTIC — Evaluation report work

- **Benchmark ID:** 5
- **Difficulty:** medium
- **Relevant Notes:** [90, 89]
- **Retrieved Notes:** [616, 90, 485, 453, 375]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.500 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| MAP@5 | 0.250 |
| R-Precision | 0.500 |
| Latency (ms) | 2.19 |

---

### SEMANTIC — Markdown support

- **Benchmark ID:** 6
- **Difficulty:** easy
- **Relevant Notes:** [72, 73, 74, 75]
- **Retrieved Notes:** [558, 568, 492, 582, 96]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 2.02 |

---

### SEMANTIC — Improve search latency

- **Benchmark ID:** 7
- **Difficulty:** easy
- **Relevant Notes:** [93, 89]
- **Retrieved Notes:** [93, 402, 195, 333, 86]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.500 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.500 |
| R-Precision | 0.500 |
| Latency (ms) | 1.56 |

---

### SEMANTIC — Attachment upload feature

- **Benchmark ID:** 8
- **Difficulty:** easy
- **Relevant Notes:** [94]
- **Retrieved Notes:** [94, 642, 492, 96, 432]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 1.000 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 1.000 |
| R-Precision | 1.000 |
| Latency (ms) | 1.46 |

---

### SEMANTIC — Flutter improvements

- **Benchmark ID:** 9
- **Difficulty:** easy
- **Relevant Notes:** [97, 98]
- **Retrieved Notes:** [98, 97, 93, 372, 564]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 1.000 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 1.000 |
| R-Precision | 1.000 |
| Latency (ms) | 1.12 |

---

### SEMANTIC — Networking concepts

- **Benchmark ID:** 10
- **Difficulty:** easy
- **Relevant Notes:** [71, 62]
- **Retrieved Notes:** [922, 722, 491, 822, 1022]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 1.00 |

---

### SEMANTIC — Object oriented programming revision

- **Benchmark ID:** 11
- **Difficulty:** easy
- **Relevant Notes:** [59, 60]
- **Retrieved Notes:** [163, 414, 227, 193, 679]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 0.91 |

---

### SEMANTIC — Interview preparation

- **Benchmark ID:** 12
- **Difficulty:** medium
- **Relevant Notes:** [70, 99]
- **Retrieved Notes:** [352, 100, 360, 70, 609]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.500 |
| Hit | True |
| Reciprocal Rank | 0.250 |
| MAP@5 | 0.125 |
| R-Precision | 0.000 |
| Latency (ms) | 0.89 |

---

### SEMANTIC — Portfolio website

- **Benchmark ID:** 13
- **Difficulty:** easy
- **Relevant Notes:** [100, 97]
- **Retrieved Notes:** [951, 266, 751, 851, 1051]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 1.55 |

---

### SEMANTIC — Documentation tasks

- **Benchmark ID:** 14
- **Difficulty:** easy
- **Relevant Notes:** [96, 95]
- **Retrieved Notes:** [110, 96, 485, 87, 583]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.500 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| MAP@5 | 0.250 |
| R-Precision | 0.500 |
| Latency (ms) | 1.11 |

---

### SEMANTIC — Deploy KnowledgeVault

- **Benchmark ID:** 15
- **Difficulty:** easy
- **Relevant Notes:** [91]
- **Retrieved Notes:** [91, 89, 90, 95, 125]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 1.000 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 1.000 |
| R-Precision | 1.000 |
| Latency (ms) | 1.59 |

---

### SEMANTIC — Update GitHub README

- **Benchmark ID:** 16
- **Difficulty:** easy
- **Relevant Notes:** [96]
- **Retrieved Notes:** [440, 501, 395, 522, 400]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 1.14 |

---

### SEMANTIC — Resume preparation

- **Benchmark ID:** 17
- **Difficulty:** easy
- **Relevant Notes:** [100]
- **Retrieved Notes:** [100, 525, 142, 185, 523]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 1.000 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 1.000 |
| R-Precision | 1.000 |
| Latency (ms) | 2.25 |

---

### SEMANTIC — Weekend trip

- **Benchmark ID:** 18
- **Difficulty:** easy
- **Relevant Notes:** [81]
- **Retrieved Notes:** [77, 81, 128, 407, 190]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 1.000 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| MAP@5 | 0.500 |
| R-Precision | 0.000 |
| Latency (ms) | 2.78 |

---

### SEMANTIC — Bills to pay

- **Benchmark ID:** 19
- **Difficulty:** medium
- **Relevant Notes:** [77, 82]
- **Retrieved Notes:** [77, 341, 82, 393, 368]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 1.000 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.833 |
| R-Precision | 0.500 |
| Latency (ms) | 1.56 |

---

### SEMANTIC — Doctor appointment

- **Benchmark ID:** 20
- **Difficulty:** easy
- **Relevant Notes:** [78, 79]
- **Retrieved Notes:** [559, 79, 198, 601, 78]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 1.000 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| MAP@5 | 0.450 |
| R-Precision | 0.500 |
| Latency (ms) | 1.12 |

---

### SEMANTIC — Shopping list

- **Benchmark ID:** 21
- **Difficulty:** medium
- **Relevant Notes:** [76]
- **Retrieved Notes:** [393, 606, 322, 76, 475]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 1.000 |
| Hit | True |
| Reciprocal Rank | 0.250 |
| MAP@5 | 0.250 |
| R-Precision | 0.000 |
| Latency (ms) | 1.10 |

---

### SEMANTIC — Things I need to tell Sid

- **Benchmark ID:** 22
- **Difficulty:** easy
- **Relevant Notes:** [54, 55, 56, 57]
- **Retrieved Notes:** [54, 56, 57, 55, 423]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.800 |
| Recall@5 | 1.000 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 1.000 |
| R-Precision | 1.000 |
| Latency (ms) | 1.60 |

---

### SEMANTIC — Next meeting with the design team

- **Benchmark ID:** 23
- **Difficulty:** medium
- **Relevant Notes:** [106, 107]
- **Retrieved Notes:** [57, 88, 568, 106, 448]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.500 |
| Hit | True |
| Reciprocal Rank | 0.250 |
| MAP@5 | 0.125 |
| R-Precision | 0.000 |
| Latency (ms) | 2.15 |

---

### SEMANTIC — Project deadline for the alpha release

- **Benchmark ID:** 24
- **Difficulty:** easy
- **Relevant Notes:** [89, 91]
- **Retrieved Notes:** [233, 498, 453, 466, 528]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 1.35 |

---

### SEMANTIC — Remind me to call mom

- **Benchmark ID:** 25
- **Difficulty:** easy
- **Relevant Notes:** [78, 79]
- **Retrieved Notes:** [382, 475, 79, 312, 56]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.500 |
| Hit | True |
| Reciprocal Rank | 0.333 |
| MAP@5 | 0.167 |
| R-Precision | 0.000 |
| Latency (ms) | 1.51 |

---

### SEMANTIC — What is the theory of relativity?

- **Benchmark ID:** 26
- **Difficulty:** easy
- **Relevant Notes:** [103, 104, 105]
- **Retrieved Notes:** [489, 290, 565, 225, 116]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 2.41 |

---

### SEMANTIC — Ideas for my new blog post

- **Benchmark ID:** 27
- **Difficulty:** medium
- **Relevant Notes:** [85, 86, 87, 88]
- **Retrieved Notes:** [255, 555, 582, 554, 86]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.250 |
| Hit | True |
| Reciprocal Rank | 0.200 |
| MAP@5 | 0.050 |
| R-Precision | 0.000 |
| Latency (ms) | 2.04 |

---

### SEMANTIC — How to set up a kubernetes cluster

- **Benchmark ID:** 28
- **Difficulty:** hard
- **Relevant Notes:** [62]
- **Retrieved Notes:** [62, 118, 712, 812, 912]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 1.000 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 1.000 |
| R-Precision | 1.000 |
| Latency (ms) | 1.81 |

---

### SEMANTIC — Things to discuss with Sid at the next meeting

- **Benchmark ID:** 29
- **Difficulty:** easy
- **Relevant Notes:** [54, 55, 56, 57]
- **Retrieved Notes:** [57, 54, 56, 423, 247]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.600 |
| Recall@5 | 0.750 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.750 |
| R-Precision | 0.750 |
| Latency (ms) | 1.27 |

---

### SEMANTIC — Study materials for machine learning

- **Benchmark ID:** 30
- **Difficulty:** medium
- **Relevant Notes:** [64, 65, 66, 67]
- **Retrieved Notes:** [309, 528, 439, 619, 357]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 1.02 |

---

### SEMANTIC — Meeting notes from Q3 planning

- **Benchmark ID:** 31
- **Difficulty:** easy
- **Relevant Notes:** [106, 107]
- **Retrieved Notes:** [203, 106, 87, 290, 107]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 1.000 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| MAP@5 | 0.450 |
| R-Precision | 0.500 |
| Latency (ms) | 1.24 |

---

### SEMANTIC — What are the project requirements for KnowledgeVault?

- **Benchmark ID:** 32
- **Difficulty:** medium
- **Relevant Notes:** [89, 90, 91, 92, 93, 94, 95, 96]
- **Retrieved Notes:** [95, 638, 125, 90, 262]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.250 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.188 |
| R-Precision | 0.250 |
| Latency (ms) | 1.31 |

---

### SEMANTIC — Reminders for next week

- **Benchmark ID:** 33
- **Difficulty:** medium
- **Relevant Notes:** [76, 77, 78, 79, 80]
- **Retrieved Notes:** [79, 56, 423, 475, 77]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.400 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.280 |
| R-Precision | 0.400 |
| Latency (ms) | 1.12 |

---

### SEMANTIC — Questions to ask during the interview

- **Benchmark ID:** 34
- **Difficulty:** easy
- **Relevant Notes:** [70, 99]
- **Retrieved Notes:** [352, 70, 154, 99, 360]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 1.000 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| MAP@5 | 0.500 |
| R-Precision | 0.500 |
| Latency (ms) | 1.20 |

---

### SEMANTIC — Brainstorming app names

- **Benchmark ID:** 35
- **Difficulty:** easy
- **Relevant Notes:** [85, 86, 87, 88]
- **Retrieved Notes:** [85, 97, 330, 117, 568]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.250 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.250 |
| R-Precision | 0.250 |
| Latency (ms) | 1.13 |

---

### SEMANTIC — Redis and PostgreSQL reference notes

- **Benchmark ID:** 36
- **Difficulty:** hard
- **Relevant Notes:** [73, 74, 58]
- **Retrieved Notes:** [73, 74, 269, 724, 824]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.667 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.667 |
| R-Precision | 0.667 |
| Latency (ms) | 1.38 |

---

### SEMANTIC — Message to send to Siddhant about backend

- **Benchmark ID:** 37
- **Difficulty:** medium
- **Relevant Notes:** [56, 57, 54]
- **Retrieved Notes:** [56, 423, 54, 55, 57]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.600 |
| Recall@5 | 1.000 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.756 |
| R-Precision | 0.667 |
| Latency (ms) | 1.86 |

---

### SEMANTIC — Study schedule for finals

- **Benchmark ID:** 38
- **Difficulty:** easy
- **Relevant Notes:** [58, 59, 60, 61]
- **Retrieved Notes:** [198, 617, 434, 601, 448]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 1.32 |

---

### SEMANTIC — Sprint planning meeting summary

- **Benchmark ID:** 39
- **Difficulty:** easy
- **Relevant Notes:** [107, 106]
- **Retrieved Notes:** [107, 294, 466, 498, 263]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.500 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.500 |
| R-Precision | 0.500 |
| Latency (ms) | 1.10 |

---

### SEMANTIC — Timeline for the beta launch

- **Benchmark ID:** 40
- **Difficulty:** medium
- **Relevant Notes:** [89, 91]
- **Retrieved Notes:** [498, 466, 620, 233, 553]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 1.67 |

---

### SEMANTIC — Don't forget to buy milk

- **Benchmark ID:** 41
- **Difficulty:** easy
- **Relevant Notes:** [76]
- **Retrieved Notes:** [76, 322, 475, 84, 286]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 1.000 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 1.000 |
| R-Precision | 1.000 |
| Latency (ms) | 1.26 |

---

### SEMANTIC — How does Redis eviction work?

- **Benchmark ID:** 42
- **Difficulty:** easy
- **Relevant Notes:** [103, 73, 61]
- **Retrieved Notes:** [103, 73, 673, 643, 773]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.667 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.667 |
| R-Precision | 0.667 |
| Latency (ms) | 1.71 |

---

### SEMANTIC — Ideas for improving KnowledgeVault

- **Benchmark ID:** 43
- **Difficulty:** medium
- **Relevant Notes:** [86, 87, 88, 89, 90]
- **Retrieved Notes:** [90, 125, 89, 638, 88]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.600 |
| Recall@5 | 0.600 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.453 |
| R-Precision | 0.600 |
| Latency (ms) | 1.56 |

---

### SEMANTIC — Docker commands cheat sheet

- **Benchmark ID:** 44
- **Difficulty:** easy
- **Relevant Notes:** [72, 75]
- **Retrieved Notes:** [72, 75, 688, 355, 788]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 1.000 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 1.000 |
| R-Precision | 1.000 |
| Latency (ms) | 1.68 |

---

### SEMANTIC — Tell Sid about the hackathon

- **Benchmark ID:** 45
- **Difficulty:** easy
- **Relevant Notes:** [55, 54]
- **Retrieved Notes:** [55, 57, 54, 423, 448]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 1.000 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.833 |
| R-Precision | 0.500 |
| Latency (ms) | 2.04 |

---

### SEMANTIC — System design interview study

- **Benchmark ID:** 46
- **Difficulty:** medium
- **Relevant Notes:** [70, 99, 59, 60]
- **Retrieved Notes:** [70, 99, 360, 309, 106]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.500 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.500 |
| R-Precision | 0.500 |
| Latency (ms) | 1.45 |

---

### SEMANTIC — Weekly sync notes

- **Benchmark ID:** 47
- **Difficulty:** easy
- **Relevant Notes:** [106, 107]
- **Retrieved Notes:** [620, 372, 87, 203, 631]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 2.18 |

---

### SEMANTIC — Budget and monthly expenses

- **Benchmark ID:** 48
- **Difficulty:** medium
- **Relevant Notes:** [82, 77]
- **Retrieved Notes:** [82, 216, 535, 281, 606]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.500 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.500 |
| R-Precision | 0.500 |
| Latency (ms) | 2.06 |

---

### SEMANTIC — Health checkup and appointments

- **Benchmark ID:** 49
- **Difficulty:** easy
- **Relevant Notes:** [78, 79, 80]
- **Retrieved Notes:** [79, 601, 559, 109, 475]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.333 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.333 |
| R-Precision | 0.333 |
| Latency (ms) | 1.45 |

---

### SEMANTIC — What are PostgreSQL index types?

- **Benchmark ID:** 50
- **Difficulty:** easy
- **Relevant Notes:** [104, 74, 58]
- **Retrieved Notes:** [104, 417, 831, 731, 931]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.333 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.333 |
| R-Precision | 0.333 |
| Latency (ms) | 1.38 |

---

### INTENT — What startup ideas do I have?

- **Benchmark ID:** 1
- **Difficulty:** easy
- **Relevant Notes:** [85, 86, 87]
- **Retrieved Notes:** [85, 178]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.333 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.333 |
| R-Precision | 0.333 |
| Latency (ms) | 66.65 |
| Predicted Intent | idea |
| Expected Intent | idea |
| Intent Correct | True |
| Predicted Category | Ideas - AI |
| Expected Category | Ideas |
| Category Correct | True |

---

### INTENT — Show my AI research reading goals

- **Benchmark ID:** 2
- **Difficulty:** easy
- **Relevant Notes:** [65, 64, 66, 67]
- **Retrieved Notes:** [65]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.250 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.250 |
| R-Precision | 0.250 |
| Latency (ms) | 29.01 |
| Predicted Intent | study |
| Expected Intent | study |
| Intent Correct | True |
| Predicted Category | Study - AI |
| Expected Category | Study Tasks |
| Category Correct | True |

---

### INTENT — How can I improve my health?

- **Benchmark ID:** 3
- **Difficulty:** medium
- **Relevant Notes:** [83, 84]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 26.23 |
| Predicted Intent | question |
| Expected Intent | todo |
| Intent Correct | False |

---

### INTENT — Show my finance reminders

- **Benchmark ID:** 4
- **Difficulty:** easy
- **Relevant Notes:** [77, 82]
- **Retrieved Notes:** [557, 542, 312, 84, 80]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 28.25 |
| Predicted Intent | reminder |
| Expected Intent | todo |
| Intent Correct | False |
| Predicted Category | Reminders |
| Expected Category | To Do |
| Category Correct | False |

---

### INTENT — Evaluation report work

- **Benchmark ID:** 5
- **Difficulty:** medium
- **Relevant Notes:** [90, 89]
- **Retrieved Notes:** [1093, 1078, 1077, 1067, 1059]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 29.18 |
| Predicted Intent | general |
| Expected Intent | reference |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Reference Notes |
| Category Correct | False |

---

### INTENT — Markdown support

- **Benchmark ID:** 6
- **Difficulty:** easy
- **Relevant Notes:** [72, 73, 74, 75]
- **Retrieved Notes:** [1093, 1078, 1077, 1067, 1059]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 28.91 |
| Predicted Intent | general |
| Expected Intent | reference |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Reference Notes |
| Category Correct | False |

---

### INTENT — Improve search latency

- **Benchmark ID:** 7
- **Difficulty:** easy
- **Relevant Notes:** [93, 89]
- **Retrieved Notes:** [1093, 1078, 1077, 1067, 1059]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 35.43 |
| Predicted Intent | general |
| Expected Intent | reference |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Reference Notes |
| Category Correct | False |

---

### INTENT — Attachment upload feature

- **Benchmark ID:** 8
- **Difficulty:** easy
- **Relevant Notes:** [94]
- **Retrieved Notes:** [1093, 1078, 1077, 1067, 1059]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 26.66 |
| Predicted Intent | general |
| Expected Intent | reference |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Reference Notes |
| Category Correct | False |

---

### INTENT — Flutter improvements

- **Benchmark ID:** 9
- **Difficulty:** easy
- **Relevant Notes:** [97, 98]
- **Retrieved Notes:** [1093, 1078, 1077, 1067, 1059]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 26.56 |
| Predicted Intent | general |
| Expected Intent | reference |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Reference Notes |
| Category Correct | False |

---

### INTENT — Networking concepts

- **Benchmark ID:** 10
- **Difficulty:** easy
- **Relevant Notes:** [71, 62]
- **Retrieved Notes:** [85]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 33.77 |
| Predicted Intent | idea |
| Expected Intent | study |
| Intent Correct | False |
| Predicted Category | Ideas - AI |
| Expected Category | Study Tasks |
| Category Correct | False |

---

### INTENT — Object oriented programming revision

- **Benchmark ID:** 11
- **Difficulty:** easy
- **Relevant Notes:** [59, 60]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 27.38 |
| Predicted Intent | study |
| Expected Intent | study |
| Intent Correct | True |

---

### INTENT — Interview preparation

- **Benchmark ID:** 12
- **Difficulty:** medium
- **Relevant Notes:** [70, 99]
- **Retrieved Notes:** [1093, 1078, 1077, 1067, 1059]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 35.51 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Study Tasks |
| Category Correct | False |

---

### INTENT — Portfolio website

- **Benchmark ID:** 13
- **Difficulty:** easy
- **Relevant Notes:** [100, 97]
- **Retrieved Notes:** [1093, 1078, 1077, 1067, 1059]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 27.42 |
| Predicted Intent | general |
| Expected Intent | todo |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | To Do |
| Category Correct | False |

---

### INTENT — Documentation tasks

- **Benchmark ID:** 14
- **Difficulty:** easy
- **Relevant Notes:** [96, 95]
- **Retrieved Notes:** [96]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.500 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.500 |
| R-Precision | 0.500 |
| Latency (ms) | 26.67 |
| Predicted Intent | reference |
| Expected Intent | todo |
| Intent Correct | False |
| Predicted Category | Reference - Knowledgevault Backend |
| Expected Category | To Do |
| Category Correct | False |

---

### INTENT — Deploy KnowledgeVault

- **Benchmark ID:** 15
- **Difficulty:** easy
- **Relevant Notes:** [91]
- **Retrieved Notes:** [1102, 1098, 1096, 1092, 1086]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 34.52 |
| Predicted Intent | todo |
| Expected Intent | todo |
| Intent Correct | True |
| Predicted Category | Tasks |
| Expected Category | To Do |
| Category Correct | True |

---

### INTENT — Update GitHub README

- **Benchmark ID:** 16
- **Difficulty:** easy
- **Relevant Notes:** [96]
- **Retrieved Notes:** [1102, 1098, 1096, 1092, 1086]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 30.63 |
| Predicted Intent | todo |
| Expected Intent | todo |
| Intent Correct | True |
| Predicted Category | Tasks |
| Expected Category | To Do |
| Category Correct | True |

---

### INTENT — Resume preparation

- **Benchmark ID:** 17
- **Difficulty:** easy
- **Relevant Notes:** [100]
- **Retrieved Notes:** [1093, 1078, 1077, 1067, 1059]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 28.99 |
| Predicted Intent | general |
| Expected Intent | todo |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | To Do |
| Category Correct | False |

---

### INTENT — Weekend trip

- **Benchmark ID:** 18
- **Difficulty:** easy
- **Relevant Notes:** [81]
- **Retrieved Notes:** [1093, 1078, 1077, 1067, 1059]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 26.74 |
| Predicted Intent | general |
| Expected Intent | todo |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | To Do |
| Category Correct | False |

---

### INTENT — Bills to pay

- **Benchmark ID:** 19
- **Difficulty:** medium
- **Relevant Notes:** [77, 82]
- **Retrieved Notes:** [1035, 935, 835, 735, 375]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 25.69 |
| Predicted Intent | todo |
| Expected Intent | todo |
| Intent Correct | True |
| Predicted Category | Bills |
| Expected Category | To Do |
| Category Correct | True |

---

### INTENT — Doctor appointment

- **Benchmark ID:** 20
- **Difficulty:** easy
- **Relevant Notes:** [78, 79]
- **Retrieved Notes:** [79, 557, 542, 312, 84]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.500 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.500 |
| R-Precision | 0.500 |
| Latency (ms) | 27.09 |
| Predicted Intent | reminder |
| Expected Intent | todo |
| Intent Correct | False |
| Predicted Category | Appointments |
| Expected Category | To Do |
| Category Correct | True |

---

### INTENT — Shopping list

- **Benchmark ID:** 21
- **Difficulty:** medium
- **Relevant Notes:** [76]
- **Retrieved Notes:** [1093, 1078, 1077, 1067, 1059]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 25.78 |
| Predicted Intent | general |
| Expected Intent | todo |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | To Do |
| Category Correct | False |

---

### INTENT — Things I need to tell Sid

- **Benchmark ID:** 22
- **Difficulty:** easy
- **Relevant Notes:** [54, 55, 56, 57]
- **Retrieved Notes:** [247, 57, 54]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.500 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| MAP@5 | 0.292 |
| R-Precision | 0.500 |
| Latency (ms) | 33.85 |
| Predicted Intent | communication |
| Expected Intent | communication |
| Intent Correct | True |
| Predicted Category | Communication - Sid |
| Expected Category | Things to Tell Sid |
| Category Correct | True |

---

### INTENT — Next meeting with the design team

- **Benchmark ID:** 23
- **Difficulty:** medium
- **Relevant Notes:** [106, 107]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 25.30 |
| Predicted Intent | event |
| Expected Intent | meeting |
| Intent Correct | False |

---

### INTENT — Project deadline for the alpha release

- **Benchmark ID:** 24
- **Difficulty:** easy
- **Relevant Notes:** [89, 91]
- **Retrieved Notes:** [1102, 1098, 1096, 1092, 1086]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 30.58 |
| Predicted Intent | todo |
| Expected Intent | project |
| Intent Correct | False |
| Predicted Category | Tasks |
| Expected Category | Projects |
| Category Correct | False |

---

### INTENT — Remind me to call mom

- **Benchmark ID:** 25
- **Difficulty:** easy
- **Relevant Notes:** [78, 79]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 24.03 |
| Predicted Intent | communication |
| Expected Intent | todo |
| Intent Correct | False |

---

### INTENT — What is the theory of relativity?

- **Benchmark ID:** 26
- **Difficulty:** easy
- **Relevant Notes:** [103, 104, 105]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 25.54 |
| Predicted Intent | question |
| Expected Intent | question |
| Intent Correct | True |

---

### INTENT — Ideas for my new blog post

- **Benchmark ID:** 27
- **Difficulty:** medium
- **Relevant Notes:** [85, 86, 87, 88]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 23.98 |
| Predicted Intent | idea |
| Expected Intent | idea |
| Intent Correct | True |

---

### INTENT — How to set up a kubernetes cluster

- **Benchmark ID:** 28
- **Difficulty:** hard
- **Relevant Notes:** [62]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 33.86 |
| Predicted Intent | question |
| Expected Intent | study |
| Intent Correct | False |

---

### INTENT — Things to discuss with Sid at the next meeting

- **Benchmark ID:** 29
- **Difficulty:** easy
- **Relevant Notes:** [54, 55, 56, 57]
- **Retrieved Notes:** [247, 57, 54]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.500 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| MAP@5 | 0.292 |
| R-Precision | 0.500 |
| Latency (ms) | 28.88 |
| Predicted Intent | communication |
| Expected Intent | communication |
| Intent Correct | True |
| Predicted Category | Communication - Sid |
| Expected Category | Things to Tell Sid |
| Category Correct | True |

---

### INTENT — Study materials for machine learning

- **Benchmark ID:** 30
- **Difficulty:** medium
- **Relevant Notes:** [64, 65, 66, 67]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 25.51 |
| Predicted Intent | study |
| Expected Intent | study |
| Intent Correct | True |

---

### INTENT — Meeting notes from Q3 planning

- **Benchmark ID:** 31
- **Difficulty:** easy
- **Relevant Notes:** [106, 107]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 25.18 |
| Predicted Intent | event |
| Expected Intent | meeting |
| Intent Correct | False |

---

### INTENT — What are the project requirements for KnowledgeVault?

- **Benchmark ID:** 32
- **Difficulty:** medium
- **Relevant Notes:** [89, 90, 91, 92, 93, 94, 95, 96]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 24.94 |
| Predicted Intent | question |
| Expected Intent | reference |
| Intent Correct | False |

---

### INTENT — Reminders for next week

- **Benchmark ID:** 33
- **Difficulty:** medium
- **Relevant Notes:** [76, 77, 78, 79, 80]
- **Retrieved Notes:** [557, 542, 312, 84, 80]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.200 |
| Hit | True |
| Reciprocal Rank | 0.200 |
| MAP@5 | 0.040 |
| R-Precision | 0.200 |
| Latency (ms) | 27.40 |
| Predicted Intent | reminder |
| Expected Intent | todo |
| Intent Correct | False |
| Predicted Category | Reminders |
| Expected Category | To Do |
| Category Correct | False |

---

### INTENT — Questions to ask during the interview

- **Benchmark ID:** 34
- **Difficulty:** easy
- **Relevant Notes:** [70, 99]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 22.94 |
| Predicted Intent | communication |
| Expected Intent | question |
| Intent Correct | False |

---

### INTENT — Brainstorming app names

- **Benchmark ID:** 35
- **Difficulty:** easy
- **Relevant Notes:** [85, 86, 87, 88]
- **Retrieved Notes:** [85]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.250 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.250 |
| R-Precision | 0.250 |
| Latency (ms) | 35.13 |
| Predicted Intent | idea |
| Expected Intent | idea |
| Intent Correct | True |
| Predicted Category | Ideas - AI |
| Expected Category | Ideas |
| Category Correct | True |

---

### INTENT — Redis and PostgreSQL reference notes

- **Benchmark ID:** 36
- **Difficulty:** hard
- **Relevant Notes:** [73, 74, 58]
- **Retrieved Notes:** [74, 1105, 1005, 905, 805]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.333 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.333 |
| R-Precision | 0.333 |
| Latency (ms) | 33.16 |
| Predicted Intent | reference |
| Expected Intent | reference |
| Intent Correct | True |
| Predicted Category | Reference - PostgreSQL |
| Expected Category | Reference Notes |
| Category Correct | True |

---

### INTENT — Message to send to Siddhant about backend

- **Benchmark ID:** 37
- **Difficulty:** medium
- **Relevant Notes:** [56, 57, 54]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 23.53 |
| Predicted Intent | communication |
| Expected Intent | communication |
| Intent Correct | True |

---

### INTENT — Study schedule for finals

- **Benchmark ID:** 38
- **Difficulty:** easy
- **Relevant Notes:** [58, 59, 60, 61]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 23.95 |
| Predicted Intent | study |
| Expected Intent | study |
| Intent Correct | True |

---

### INTENT — Sprint planning meeting summary

- **Benchmark ID:** 39
- **Difficulty:** easy
- **Relevant Notes:** [107, 106]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 25.44 |
| Predicted Intent | event |
| Expected Intent | meeting |
| Intent Correct | False |

---

### INTENT — Timeline for the beta launch

- **Benchmark ID:** 40
- **Difficulty:** medium
- **Relevant Notes:** [89, 91]
- **Retrieved Notes:** [1102, 1098, 1096, 1092, 1086]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 39.79 |
| Predicted Intent | todo |
| Expected Intent | todo |
| Intent Correct | True |
| Predicted Category | Tasks |
| Expected Category | To Do |
| Category Correct | True |

---

### INTENT — Don't forget to buy milk

- **Benchmark ID:** 41
- **Difficulty:** easy
- **Relevant Notes:** [76]
- **Retrieved Notes:** [322, 76, 1102, 1098, 1096]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 1.000 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| MAP@5 | 0.500 |
| R-Precision | 0.000 |
| Latency (ms) | 34.78 |
| Predicted Intent | todo |
| Expected Intent | todo |
| Intent Correct | True |
| Predicted Category | Shopping |
| Expected Category | To Do |
| Category Correct | True |

---

### INTENT — How does Redis eviction work?

- **Benchmark ID:** 42
- **Difficulty:** easy
- **Relevant Notes:** [103, 73, 61]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 24.02 |
| Predicted Intent | question |
| Expected Intent | question |
| Intent Correct | True |

---

### INTENT — Ideas for improving KnowledgeVault

- **Benchmark ID:** 43
- **Difficulty:** medium
- **Relevant Notes:** [86, 87, 88, 89, 90]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 23.36 |
| Predicted Intent | idea |
| Expected Intent | idea |
| Intent Correct | True |

---

### INTENT — Docker commands cheat sheet

- **Benchmark ID:** 44
- **Difficulty:** easy
- **Relevant Notes:** [72, 75]
- **Retrieved Notes:** [75, 72]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 1.000 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 1.000 |
| R-Precision | 1.000 |
| Latency (ms) | 27.08 |
| Predicted Intent | reference |
| Expected Intent | reference |
| Intent Correct | True |
| Predicted Category | Reference - Docker |
| Expected Category | Reference Notes |
| Category Correct | True |

---

### INTENT — Tell Sid about the hackathon

- **Benchmark ID:** 45
- **Difficulty:** easy
- **Relevant Notes:** [55, 54]
- **Retrieved Notes:** [247, 57, 54]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.500 |
| Hit | True |
| Reciprocal Rank | 0.333 |
| MAP@5 | 0.167 |
| R-Precision | 0.000 |
| Latency (ms) | 27.83 |
| Predicted Intent | communication |
| Expected Intent | communication |
| Intent Correct | True |
| Predicted Category | Communication - Sid |
| Expected Category | Things to Tell Sid |
| Category Correct | True |

---

### INTENT — System design interview study

- **Benchmark ID:** 46
- **Difficulty:** medium
- **Relevant Notes:** [70, 99, 59, 60]
- **Retrieved Notes:** [70]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.250 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.250 |
| R-Precision | 0.250 |
| Latency (ms) | 25.92 |
| Predicted Intent | study |
| Expected Intent | study |
| Intent Correct | True |
| Predicted Category | Study - System Design |
| Expected Category | Study Tasks |
| Category Correct | True |

---

### INTENT — Weekly sync notes

- **Benchmark ID:** 47
- **Difficulty:** easy
- **Relevant Notes:** [106, 107]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 24.09 |
| Predicted Intent | reference |
| Expected Intent | meeting |
| Intent Correct | False |

---

### INTENT — Budget and monthly expenses

- **Benchmark ID:** 48
- **Difficulty:** medium
- **Relevant Notes:** [82, 77]
- **Retrieved Notes:** [1093, 1078, 1077, 1067, 1059]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 28.25 |
| Predicted Intent | general |
| Expected Intent | todo |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | To Do |
| Category Correct | False |

---

### INTENT — Health checkup and appointments

- **Benchmark ID:** 49
- **Difficulty:** easy
- **Relevant Notes:** [78, 79, 80]
- **Retrieved Notes:** [79, 557, 542, 312, 84]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.333 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.333 |
| R-Precision | 0.333 |
| Latency (ms) | 29.01 |
| Predicted Intent | reminder |
| Expected Intent | todo |
| Intent Correct | False |
| Predicted Category | Appointments |
| Expected Category | To Do |
| Category Correct | True |

---

### INTENT — What are PostgreSQL index types?

- **Benchmark ID:** 50
- **Difficulty:** easy
- **Relevant Notes:** [104, 74, 58]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 24.26 |
| Predicted Intent | question |
| Expected Intent | question |
| Intent Correct | True |

---

### HYBRID — What startup ideas do I have?

- **Benchmark ID:** 1
- **Difficulty:** easy
- **Relevant Notes:** [85, 86, 87]
- **Retrieved Notes:** [85, 525, 617, 134, 441, 553, 459, 255, 166, 685, 785, 885, 985, 1085, 178, 475, 322, 391, 607, 753]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.333 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.333 |
| R-Precision | 0.333 |
| Latency (ms) | 81.77 |
| Predicted Intent | idea |
| Expected Intent | idea |
| Intent Correct | True |
| Predicted Category | Ideas - AI |
| Expected Category | Ideas |
| Category Correct | True |

---

### HYBRID — Show my AI research reading goals

- **Benchmark ID:** 2
- **Difficulty:** easy
- **Relevant Notes:** [65, 64, 66, 67]
- **Retrieved Notes:** [529, 617, 416, 85, 230, 87, 65, 122, 166, 685, 785, 885, 985, 1085, 240, 525, 523, 290, 413, 235]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.143 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 76.92 |
| Predicted Intent | study |
| Expected Intent | study |
| Intent Correct | True |
| Predicted Category | Study - AI |
| Expected Category | Study Tasks |
| Category Correct | True |

---

### HYBRID — How can I improve my health?

- **Benchmark ID:** 3
- **Difficulty:** medium
- **Relevant Notes:** [83, 84]
- **Retrieved Notes:** [84, 109, 83, 79, 286, 322, 380, 680, 780, 880, 980, 1080, 76, 157, 355, 688, 788, 888, 988, 1088]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 1.000 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.833 |
| R-Precision | 0.500 |
| Latency (ms) | 78.75 |
| Predicted Intent | question |
| Expected Intent | todo |
| Intent Correct | False |

---

### HYBRID — Show my finance reminders

- **Benchmark ID:** 4
- **Difficulty:** easy
- **Relevant Notes:** [77, 82]
- **Retrieved Notes:** [312, 216, 82, 77, 393, 375, 735, 835, 935, 1035, 442, 755, 855, 955, 1055, 583, 699, 799, 899, 999]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 1.000 |
| Hit | True |
| Reciprocal Rank | 0.333 |
| MAP@5 | 0.417 |
| R-Precision | 0.000 |
| Latency (ms) | 142.28 |
| Predicted Intent | reminder |
| Expected Intent | todo |
| Intent Correct | False |
| Predicted Category | Reminders |
| Expected Category | To Do |
| Category Correct | False |

---

### HYBRID — Evaluation report work

- **Benchmark ID:** 5
- **Difficulty:** medium
- **Relevant Notes:** [90, 89]
- **Retrieved Notes:** [616, 90, 485, 453, 375, 735, 835, 935, 1035, 487, 525, 310, 555, 103, 470, 251, 185, 498, 213, 729]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.500 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| MAP@5 | 0.250 |
| R-Precision | 0.500 |
| Latency (ms) | 91.50 |
| Predicted Intent | general |
| Expected Intent | reference |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Reference Notes |
| Category Correct | False |

---

### HYBRID — Markdown support

- **Benchmark ID:** 6
- **Difficulty:** easy
- **Relevant Notes:** [72, 73, 74, 75]
- **Retrieved Notes:** [558, 568, 492, 582, 96, 289, 581, 653, 87, 251, 523, 625, 449, 442, 755, 855, 955, 1055, 386, 338]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 81.08 |
| Predicted Intent | general |
| Expected Intent | reference |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Reference Notes |
| Category Correct | False |

---

### HYBRID — Improve search latency

- **Benchmark ID:** 7
- **Difficulty:** easy
- **Relevant Notes:** [93, 89]
- **Retrieved Notes:** [93, 402, 195, 333, 86, 644, 567, 704, 804, 904, 1004, 1104, 213, 729, 829, 929, 1029, 58, 61, 310]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.500 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.500 |
| R-Precision | 0.500 |
| Latency (ms) | 87.45 |
| Predicted Intent | general |
| Expected Intent | reference |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Reference Notes |
| Category Correct | False |

---

### HYBRID — Attachment upload feature

- **Benchmark ID:** 8
- **Difficulty:** easy
- **Relevant Notes:** [94]
- **Retrieved Notes:** [94, 642, 492, 96, 432, 692, 792, 892, 992, 1092, 386, 506, 523, 465, 486, 702, 802, 902, 1002, 1102]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 1.000 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 1.000 |
| R-Precision | 1.000 |
| Latency (ms) | 97.87 |
| Predicted Intent | general |
| Expected Intent | reference |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Reference Notes |
| Category Correct | False |

---

### HYBRID — Flutter improvements

- **Benchmark ID:** 9
- **Difficulty:** easy
- **Relevant Notes:** [97, 98]
- **Retrieved Notes:** [98, 97, 93, 372, 564, 467, 142, 655, 653, 61, 444, 175, 337, 295, 568, 442, 755, 855, 955, 1055]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 1.000 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 1.000 |
| R-Precision | 1.000 |
| Latency (ms) | 90.05 |
| Predicted Intent | general |
| Expected Intent | reference |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Reference Notes |
| Category Correct | False |

---

### HYBRID — Networking concepts

- **Benchmark ID:** 10
- **Difficulty:** easy
- **Relevant Notes:** [71, 62]
- **Retrieved Notes:** [491, 722, 822, 922, 1022, 532, 99, 633, 439, 327, 106, 516, 711, 811, 911, 1011, 62, 392, 159, 299]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.059 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 76.45 |
| Predicted Intent | idea |
| Expected Intent | study |
| Intent Correct | False |
| Predicted Category | Ideas - AI |
| Expected Category | Study Tasks |
| Category Correct | False |

---

### HYBRID — Object oriented programming revision

- **Benchmark ID:** 11
- **Difficulty:** easy
- **Relevant Notes:** [59, 60]
- **Retrieved Notes:** [163, 414, 227, 193, 679, 779, 879, 979, 1079, 330, 117, 235, 311, 390, 169, 562, 419, 247, 309, 270]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 83.87 |
| Predicted Intent | study |
| Expected Intent | study |
| Intent Correct | True |

---

### HYBRID — Interview preparation

- **Benchmark ID:** 12
- **Difficulty:** medium
- **Relevant Notes:** [70, 99]
- **Retrieved Notes:** [352, 100, 360, 70, 609, 507, 154, 288, 344, 468, 199, 152, 294, 540, 99, 521, 126, 236, 413, 205]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.500 |
| Hit | True |
| Reciprocal Rank | 0.250 |
| MAP@5 | 0.125 |
| R-Precision | 0.000 |
| Latency (ms) | 93.53 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Study Tasks |
| Category Correct | False |

---

### HYBRID — Portfolio website

- **Benchmark ID:** 13
- **Difficulty:** easy
- **Relevant Notes:** [100, 97]
- **Retrieved Notes:** [266, 751, 851, 951, 1051, 131, 117, 528, 413, 555, 178, 360, 65, 66, 525, 619, 60, 175, 607, 753]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 92.15 |
| Predicted Intent | general |
| Expected Intent | todo |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | To Do |
| Category Correct | False |

---

### HYBRID — Documentation tasks

- **Benchmark ID:** 14
- **Difficulty:** easy
- **Relevant Notes:** [96, 95]
- **Retrieved Notes:** [110, 96, 485, 87, 583, 699, 799, 899, 999, 1099, 453, 186, 565, 360, 558, 330, 487, 625, 523, 510]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.500 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| MAP@5 | 0.250 |
| R-Precision | 0.500 |
| Latency (ms) | 82.08 |
| Predicted Intent | reference |
| Expected Intent | todo |
| Intent Correct | False |
| Predicted Category | Reference - Knowledgevault Backend |
| Expected Category | To Do |
| Category Correct | False |

---

### HYBRID — Deploy KnowledgeVault

- **Benchmark ID:** 15
- **Difficulty:** easy
- **Relevant Notes:** [91]
- **Retrieved Notes:** [91, 89, 95, 90, 125, 96, 94, 88, 638, 97, 57, 337, 251, 262, 607, 753, 853, 953, 1053, 555]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 1.000 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 1.000 |
| R-Precision | 1.000 |
| Latency (ms) | 107.13 |
| Predicted Intent | todo |
| Expected Intent | todo |
| Intent Correct | True |
| Predicted Category | Tasks |
| Expected Category | To Do |
| Category Correct | True |

---

### HYBRID — Update GitHub README

- **Benchmark ID:** 16
- **Difficulty:** easy
- **Relevant Notes:** [96]
- **Retrieved Notes:** [440, 501, 522, 395, 400, 328, 612, 646, 366, 235, 497, 719, 819, 919, 1019, 614, 141, 193, 679, 779]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 96.04 |
| Predicted Intent | todo |
| Expected Intent | todo |
| Intent Correct | True |
| Predicted Category | Tasks |
| Expected Category | To Do |
| Category Correct | True |

---

### HYBRID — Resume preparation

- **Benchmark ID:** 17
- **Difficulty:** easy
- **Relevant Notes:** [100]
- **Retrieved Notes:** [100, 525, 142, 185, 523, 107, 288, 352, 601, 521, 184, 360, 415, 485, 199, 617, 268, 682, 782, 882]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 1.000 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 1.000 |
| R-Precision | 1.000 |
| Latency (ms) | 86.78 |
| Predicted Intent | general |
| Expected Intent | todo |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | To Do |
| Category Correct | False |

---

### HYBRID — Weekend trip

- **Benchmark ID:** 18
- **Difficulty:** easy
- **Relevant Notes:** [81]
- **Retrieved Notes:** [77, 81, 128, 407, 190, 198, 351, 324, 393, 575, 538, 400, 375, 735, 835, 935, 1035, 631, 627, 639]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 1.000 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| MAP@5 | 0.500 |
| R-Precision | 0.000 |
| Latency (ms) | 80.42 |
| Predicted Intent | general |
| Expected Intent | todo |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | To Do |
| Category Correct | False |

---

### HYBRID — Bills to pay

- **Benchmark ID:** 19
- **Difficulty:** medium
- **Relevant Notes:** [77, 82]
- **Retrieved Notes:** [77, 341, 82, 393, 368, 312, 490, 178, 331, 411, 216, 76, 140, 399, 371, 403, 635, 322, 285, 573]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 1.000 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.833 |
| R-Precision | 0.500 |
| Latency (ms) | 97.53 |
| Predicted Intent | todo |
| Expected Intent | todo |
| Intent Correct | True |
| Predicted Category | Bills |
| Expected Category | To Do |
| Category Correct | True |

---

### HYBRID — Doctor appointment

- **Benchmark ID:** 20
- **Difficulty:** easy
- **Relevant Notes:** [78, 79]
- **Retrieved Notes:** [559, 79, 198, 601, 78, 609, 70, 56, 231, 54, 575, 448, 288, 475, 111, 356, 423, 59, 57, 81]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 1.000 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| MAP@5 | 0.450 |
| R-Precision | 0.500 |
| Latency (ms) | 80.75 |
| Predicted Intent | reminder |
| Expected Intent | todo |
| Intent Correct | False |
| Predicted Category | Appointments |
| Expected Category | To Do |
| Category Correct | True |

---

### HYBRID — Shopping list

- **Benchmark ID:** 21
- **Difficulty:** medium
- **Relevant Notes:** [76]
- **Retrieved Notes:** [170, 393, 606, 322, 76, 475, 216, 115, 202, 605, 358, 145, 204, 182, 82, 265, 303, 331, 178, 309]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 1.000 |
| Hit | True |
| Reciprocal Rank | 0.200 |
| MAP@5 | 0.200 |
| R-Precision | 0.000 |
| Latency (ms) | 80.37 |
| Predicted Intent | general |
| Expected Intent | todo |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | To Do |
| Category Correct | False |

---

### HYBRID — Things I need to tell Sid

- **Benchmark ID:** 22
- **Difficulty:** easy
- **Relevant Notes:** [54, 55, 56, 57]
- **Retrieved Notes:** [54, 57, 56, 55, 423, 247, 442, 755, 855, 955, 1055, 203, 230, 382, 268, 682, 782, 882, 982, 1082]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.800 |
| Recall@5 | 1.000 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 1.000 |
| R-Precision | 1.000 |
| Latency (ms) | 75.82 |
| Predicted Intent | communication |
| Expected Intent | communication |
| Intent Correct | True |
| Predicted Category | Communication - Sid |
| Expected Category | Things to Tell Sid |
| Category Correct | True |

---

### HYBRID — Next meeting with the design team

- **Benchmark ID:** 23
- **Difficulty:** medium
- **Relevant Notes:** [106, 107]
- **Retrieved Notes:** [57, 88, 568, 106, 448, 360, 56, 107, 382, 626, 95, 528, 141, 175, 70, 330, 442, 755, 855, 955]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.500 |
| Hit | True |
| Reciprocal Rank | 0.250 |
| MAP@5 | 0.125 |
| R-Precision | 0.000 |
| Latency (ms) | 73.20 |
| Predicted Intent | event |
| Expected Intent | meeting |
| Intent Correct | False |

---

### HYBRID — Project deadline for the alpha release

- **Benchmark ID:** 24
- **Difficulty:** easy
- **Relevant Notes:** [89, 91]
- **Retrieved Notes:** [233, 498, 190, 252, 257, 264, 270, 289, 309, 317, 480, 497, 591, 616, 644, 696, 715, 719, 796, 815]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 96.37 |
| Predicted Intent | todo |
| Expected Intent | project |
| Intent Correct | False |
| Predicted Category | Tasks |
| Expected Category | Projects |
| Category Correct | False |

---

### HYBRID — Remind me to call mom

- **Benchmark ID:** 25
- **Difficulty:** easy
- **Relevant Notes:** [78, 79]
- **Retrieved Notes:** [382, 475, 79, 312, 56, 78, 77, 54, 290, 212, 182, 550, 700, 800, 900, 1000, 1100, 322, 55, 317]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.500 |
| Hit | True |
| Reciprocal Rank | 0.333 |
| MAP@5 | 0.167 |
| R-Precision | 0.000 |
| Latency (ms) | 76.73 |
| Predicted Intent | communication |
| Expected Intent | todo |
| Intent Correct | False |

---

### HYBRID — What is the theory of relativity?

- **Benchmark ID:** 26
- **Difficulty:** easy
- **Relevant Notes:** [103, 104, 105]
- **Retrieved Notes:** [489, 290, 565, 225, 116, 424, 306, 102, 287, 613, 298, 726, 826, 926, 1026, 130, 608, 175, 179, 260]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 68.69 |
| Predicted Intent | question |
| Expected Intent | question |
| Intent Correct | True |

---

### HYBRID — Ideas for my new blog post

- **Benchmark ID:** 27
- **Difficulty:** medium
- **Relevant Notes:** [85, 86, 87, 88]
- **Retrieved Notes:** [255, 555, 582, 554, 86, 413, 85, 525, 375, 735, 835, 935, 1035, 453, 337, 208, 442, 755, 855, 955]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.250 |
| Hit | True |
| Reciprocal Rank | 0.200 |
| MAP@5 | 0.050 |
| R-Precision | 0.000 |
| Latency (ms) | 71.66 |
| Predicted Intent | idea |
| Expected Intent | idea |
| Intent Correct | True |

---

### HYBRID — How to set up a kubernetes cluster

- **Benchmark ID:** 28
- **Difficulty:** hard
- **Relevant Notes:** [62]
- **Retrieved Notes:** [62, 118, 712, 812, 912, 1012, 410, 383, 91, 352, 192, 439, 95, 609, 392, 566, 710, 810, 910, 1010]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 1.000 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 1.000 |
| R-Precision | 1.000 |
| Latency (ms) | 78.13 |
| Predicted Intent | question |
| Expected Intent | study |
| Intent Correct | False |

---

### HYBRID — Things to discuss with Sid at the next meeting

- **Benchmark ID:** 29
- **Difficulty:** easy
- **Relevant Notes:** [54, 55, 56, 57]
- **Retrieved Notes:** [57, 54, 56, 423, 247, 55, 203, 442, 755, 855, 955, 1055, 230, 448, 263, 185, 175, 107, 81, 382]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.600 |
| Recall@5 | 0.750 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.750 |
| R-Precision | 0.750 |
| Latency (ms) | 79.79 |
| Predicted Intent | communication |
| Expected Intent | communication |
| Intent Correct | True |
| Predicted Category | Communication - Sid |
| Expected Category | Things to Tell Sid |
| Category Correct | True |

---

### HYBRID — Study materials for machine learning

- **Benchmark ID:** 30
- **Difficulty:** medium
- **Relevant Notes:** [64, 65, 66, 67]
- **Retrieved Notes:** [309, 528, 439, 619, 357, 60, 360, 66, 343, 592, 178, 74, 547, 266, 751, 851, 951, 1051, 196, 529]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.125 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 72.80 |
| Predicted Intent | study |
| Expected Intent | study |
| Intent Correct | True |

---

### HYBRID — Meeting notes from Q3 planning

- **Benchmark ID:** 31
- **Difficulty:** easy
- **Relevant Notes:** [106, 107]
- **Retrieved Notes:** [203, 106, 87, 290, 107, 372, 448, 175, 438, 56, 371, 423, 212, 479, 444, 539, 141, 60, 617, 216]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 1.000 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| MAP@5 | 0.450 |
| R-Precision | 0.500 |
| Latency (ms) | 76.95 |
| Predicted Intent | event |
| Expected Intent | meeting |
| Intent Correct | False |

---

### HYBRID — What are the project requirements for KnowledgeVault?

- **Benchmark ID:** 32
- **Difficulty:** medium
- **Relevant Notes:** [89, 90, 91, 92, 93, 94, 95, 96]
- **Retrieved Notes:** [95, 638, 125, 90, 262, 89, 57, 247, 555, 96, 97, 88, 413, 428, 728, 828, 928, 1028, 337, 107]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.250 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.188 |
| R-Precision | 0.375 |
| Latency (ms) | 73.48 |
| Predicted Intent | question |
| Expected Intent | reference |
| Intent Correct | False |

---

### HYBRID — Reminders for next week

- **Benchmark ID:** 33
- **Difficulty:** medium
- **Relevant Notes:** [76, 77, 78, 79, 80]
- **Retrieved Notes:** [79, 56, 423, 312, 475, 77, 198, 382, 631, 107, 392, 216, 442, 755, 855, 955, 1055, 57, 528, 557]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.200 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.200 |
| R-Precision | 0.200 |
| Latency (ms) | 75.71 |
| Predicted Intent | reminder |
| Expected Intent | todo |
| Intent Correct | False |
| Predicted Category | Reminders |
| Expected Category | To Do |
| Category Correct | False |

---

### HYBRID — Questions to ask during the interview

- **Benchmark ID:** 34
- **Difficulty:** easy
- **Relevant Notes:** [70, 99]
- **Retrieved Notes:** [352, 70, 154, 99, 360, 468, 294, 199, 540, 459, 593, 344, 609, 507, 413, 205, 54, 126, 398, 470]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 1.000 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| MAP@5 | 0.500 |
| R-Precision | 0.500 |
| Latency (ms) | 68.79 |
| Predicted Intent | communication |
| Expected Intent | question |
| Intent Correct | False |

---

### HYBRID — Brainstorming app names

- **Benchmark ID:** 35
- **Difficulty:** easy
- **Relevant Notes:** [85, 86, 87, 88]
- **Retrieved Notes:** [85, 97, 330, 117, 568, 617, 448, 155, 525, 87, 266, 751, 851, 951, 1051, 459, 382, 175, 166, 685]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.250 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.250 |
| R-Precision | 0.250 |
| Latency (ms) | 72.38 |
| Predicted Intent | idea |
| Expected Intent | idea |
| Intent Correct | True |
| Predicted Category | Ideas - AI |
| Expected Category | Ideas |
| Category Correct | True |

---

### HYBRID — Redis and PostgreSQL reference notes

- **Benchmark ID:** 36
- **Difficulty:** hard
- **Relevant Notes:** [73, 74, 58]
- **Retrieved Notes:** [73, 74, 269, 724, 824, 924, 1024, 421, 746, 846, 946, 1046, 92, 643, 673, 773, 873, 973, 1073, 61]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.667 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.667 |
| R-Precision | 0.667 |
| Latency (ms) | 85.36 |
| Predicted Intent | reference |
| Expected Intent | reference |
| Intent Correct | True |
| Predicted Category | Reference - PostgreSQL |
| Expected Category | Reference Notes |
| Category Correct | True |

---

### HYBRID — Message to send to Siddhant about backend

- **Benchmark ID:** 37
- **Difficulty:** medium
- **Relevant Notes:** [56, 57, 54]
- **Retrieved Notes:** [56, 423, 54, 55, 57, 106, 392, 372, 129, 91, 132, 658, 758, 858, 958, 1058, 247, 61, 337, 96]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.600 |
| Recall@5 | 1.000 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.756 |
| R-Precision | 0.667 |
| Latency (ms) | 76.01 |
| Predicted Intent | communication |
| Expected Intent | communication |
| Intent Correct | True |

---

### HYBRID — Study schedule for finals

- **Benchmark ID:** 38
- **Difficulty:** easy
- **Relevant Notes:** [58, 59, 60, 61]
- **Retrieved Notes:** [198, 617, 434, 601, 448, 521, 107, 343, 224, 524, 380, 680, 780, 880, 980, 1080, 317, 344, 495, 620]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 82.23 |
| Predicted Intent | study |
| Expected Intent | study |
| Intent Correct | True |

---

### HYBRID — Sprint planning meeting summary

- **Benchmark ID:** 39
- **Difficulty:** easy
- **Relevant Notes:** [107, 106]
- **Retrieved Notes:** [107, 294, 466, 498, 263, 203, 216, 448, 567, 704, 804, 904, 1004, 1104, 423, 56, 438, 352, 468, 538]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.500 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.500 |
| R-Precision | 0.500 |
| Latency (ms) | 73.28 |
| Predicted Intent | event |
| Expected Intent | meeting |
| Intent Correct | False |

---

### HYBRID — Timeline for the beta launch

- **Benchmark ID:** 40
- **Difficulty:** medium
- **Relevant Notes:** [89, 91]
- **Retrieved Notes:** [155, 190, 252, 257, 264, 270, 289, 309, 480, 497, 591, 616, 644, 696, 715, 719, 796, 815, 819, 896]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 100.09 |
| Predicted Intent | todo |
| Expected Intent | todo |
| Intent Correct | True |
| Predicted Category | Tasks |
| Expected Category | To Do |
| Category Correct | True |

---

### HYBRID — Don't forget to buy milk

- **Benchmark ID:** 41
- **Difficulty:** easy
- **Relevant Notes:** [76]
- **Retrieved Notes:** [76, 322, 475, 84, 286, 78, 83, 79, 134, 202, 309, 343, 496, 584, 586, 77, 281, 82, 190, 109]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 1.000 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 1.000 |
| R-Precision | 1.000 |
| Latency (ms) | 94.33 |
| Predicted Intent | todo |
| Expected Intent | todo |
| Intent Correct | True |
| Predicted Category | Shopping |
| Expected Category | To Do |
| Category Correct | True |

---

### HYBRID — How does Redis eviction work?

- **Benchmark ID:** 42
- **Difficulty:** easy
- **Relevant Notes:** [103, 73, 61]
- **Retrieved Notes:** [103, 73, 643, 673, 773, 873, 973, 1073, 433, 705, 805, 905, 1005, 1105, 92, 269, 724, 824, 924, 1024]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.667 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.667 |
| R-Precision | 0.667 |
| Latency (ms) | 72.79 |
| Predicted Intent | question |
| Expected Intent | question |
| Intent Correct | True |

---

### HYBRID — Ideas for improving KnowledgeVault

- **Benchmark ID:** 43
- **Difficulty:** medium
- **Relevant Notes:** [86, 87, 88, 89, 90]
- **Retrieved Notes:** [90, 125, 89, 638, 88, 428, 728, 828, 928, 1028, 555, 95, 57, 97, 96, 262, 247, 337, 444, 107]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.600 |
| Recall@5 | 0.600 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.453 |
| R-Precision | 0.600 |
| Latency (ms) | 72.79 |
| Predicted Intent | idea |
| Expected Intent | idea |
| Intent Correct | True |

---

### HYBRID — Docker commands cheat sheet

- **Benchmark ID:** 44
- **Difficulty:** easy
- **Relevant Notes:** [72, 75]
- **Retrieved Notes:** [72, 75, 355, 688, 788, 888, 988, 1088, 192, 105, 295, 138, 491, 722, 822, 922, 1022, 383, 91, 445]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 1.000 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 1.000 |
| R-Precision | 1.000 |
| Latency (ms) | 76.18 |
| Predicted Intent | reference |
| Expected Intent | reference |
| Intent Correct | True |
| Predicted Category | Reference - Docker |
| Expected Category | Reference Notes |
| Category Correct | True |

---

### HYBRID — Tell Sid about the hackathon

- **Benchmark ID:** 45
- **Difficulty:** easy
- **Relevant Notes:** [55, 54]
- **Retrieved Notes:** [55, 57, 54, 423, 448, 56, 542, 324, 463, 319, 247, 535, 442, 755, 855, 955, 1055, 449, 553, 436]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 1.000 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.833 |
| R-Precision | 0.500 |
| Latency (ms) | 72.39 |
| Predicted Intent | communication |
| Expected Intent | communication |
| Intent Correct | True |
| Predicted Category | Communication - Sid |
| Expected Category | Things to Tell Sid |
| Category Correct | True |

---

### HYBRID — System design interview study

- **Benchmark ID:** 46
- **Difficulty:** medium
- **Relevant Notes:** [70, 99, 59, 60]
- **Retrieved Notes:** [70, 99, 360, 309, 106, 392, 540, 352, 102, 88, 199, 344, 59, 442, 755, 855, 955, 1055, 169, 126]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.500 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.500 |
| R-Precision | 0.500 |
| Latency (ms) | 77.00 |
| Predicted Intent | study |
| Expected Intent | study |
| Intent Correct | True |
| Predicted Category | Study - System Design |
| Expected Category | Study Tasks |
| Category Correct | True |

---

### HYBRID — Weekly sync notes

- **Benchmark ID:** 47
- **Difficulty:** easy
- **Relevant Notes:** [106, 107]
- **Retrieved Notes:** [620, 372, 87, 203, 631, 393, 444, 107, 216, 198, 565, 82, 202, 495, 582, 604, 331, 224, 375, 735]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.125 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 70.08 |
| Predicted Intent | reference |
| Expected Intent | meeting |
| Intent Correct | False |

---

### HYBRID — Budget and monthly expenses

- **Benchmark ID:** 48
- **Difficulty:** medium
- **Relevant Notes:** [82, 77]
- **Retrieved Notes:** [82, 216, 535, 281, 606, 490, 393, 341, 635, 538, 601, 331, 77, 403, 162, 115, 573, 564, 407, 210]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.500 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.500 |
| R-Precision | 0.500 |
| Latency (ms) | 76.83 |
| Predicted Intent | general |
| Expected Intent | todo |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | To Do |
| Category Correct | False |

---

### HYBRID — Health checkup and appointments

- **Benchmark ID:** 49
- **Difficulty:** easy
- **Relevant Notes:** [78, 79, 80]
- **Retrieved Notes:** [79, 601, 559, 109, 475, 575, 198, 231, 82, 111, 355, 688, 788, 888, 988, 1088, 609, 620, 542, 78]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.333 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.333 |
| R-Precision | 0.333 |
| Latency (ms) | 74.08 |
| Predicted Intent | reminder |
| Expected Intent | todo |
| Intent Correct | False |
| Predicted Category | Appointments |
| Expected Category | To Do |
| Category Correct | True |

---

### HYBRID — What are PostgreSQL index types?

- **Benchmark ID:** 50
- **Difficulty:** easy
- **Relevant Notes:** [104, 74, 58]
- **Retrieved Notes:** [104, 417, 731, 831, 931, 1031, 58, 74, 280, 66, 567, 704, 804, 904, 1004, 1104, 139, 686, 786, 886]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.333 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.333 |
| R-Precision | 0.333 |
| Latency (ms) | 74.44 |
| Predicted Intent | question |
| Expected Intent | question |
| Intent Correct | True |

---

### RERANK — What startup ideas do I have?

- **Benchmark ID:** 1
- **Difficulty:** easy
- **Relevant Notes:** [85, 86, 87]
- **Retrieved Notes:** [85, 525, 617, 134, 441, 553, 459, 255]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.333 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.333 |
| R-Precision | 0.333 |
| Latency (ms) | 84.55 |
| Predicted Intent | idea |
| Expected Intent | idea |
| Intent Correct | True |
| Predicted Category | Ideas - AI |
| Expected Category | Ideas |
| Category Correct | True |

---

### RERANK — Show my AI research reading goals

- **Benchmark ID:** 2
- **Difficulty:** easy
- **Relevant Notes:** [65, 64, 66, 67]
- **Retrieved Notes:** [529, 617, 416, 85, 230, 87, 65, 122]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.143 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 77.47 |
| Predicted Intent | study |
| Expected Intent | study |
| Intent Correct | True |
| Predicted Category | Study - AI |
| Expected Category | Study Tasks |
| Category Correct | True |

---

### RERANK — How can I improve my health?

- **Benchmark ID:** 3
- **Difficulty:** medium
- **Relevant Notes:** [83, 84]
- **Retrieved Notes:** [84, 109, 83, 79, 286, 322, 380, 680]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 1.000 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.833 |
| R-Precision | 0.500 |
| Latency (ms) | 70.83 |
| Predicted Intent | question |
| Expected Intent | todo |
| Intent Correct | False |

---

### RERANK — Show my finance reminders

- **Benchmark ID:** 4
- **Difficulty:** easy
- **Relevant Notes:** [77, 82]
- **Retrieved Notes:** [312, 216, 82, 77, 393, 375, 735, 835]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 1.000 |
| Hit | True |
| Reciprocal Rank | 0.333 |
| MAP@5 | 0.417 |
| R-Precision | 0.000 |
| Latency (ms) | 76.93 |
| Predicted Intent | reminder |
| Expected Intent | todo |
| Intent Correct | False |
| Predicted Category | Reminders |
| Expected Category | To Do |
| Category Correct | False |

---

### RERANK — Evaluation report work

- **Benchmark ID:** 5
- **Difficulty:** medium
- **Relevant Notes:** [90, 89]
- **Retrieved Notes:** [616, 90, 485, 453, 375, 735, 835, 935]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.500 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| MAP@5 | 0.250 |
| R-Precision | 0.500 |
| Latency (ms) | 81.11 |
| Predicted Intent | general |
| Expected Intent | reference |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Reference Notes |
| Category Correct | False |

---

### RERANK — Markdown support

- **Benchmark ID:** 6
- **Difficulty:** easy
- **Relevant Notes:** [72, 73, 74, 75]
- **Retrieved Notes:** [558, 568, 492, 582, 96, 289, 581, 653]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 81.61 |
| Predicted Intent | general |
| Expected Intent | reference |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Reference Notes |
| Category Correct | False |

---

### RERANK — Improve search latency

- **Benchmark ID:** 7
- **Difficulty:** easy
- **Relevant Notes:** [93, 89]
- **Retrieved Notes:** [93, 402, 195, 333, 86, 644, 567, 704]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.500 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.500 |
| R-Precision | 0.500 |
| Latency (ms) | 218.82 |
| Predicted Intent | general |
| Expected Intent | reference |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Reference Notes |
| Category Correct | False |

---

### RERANK — Attachment upload feature

- **Benchmark ID:** 8
- **Difficulty:** easy
- **Relevant Notes:** [94]
- **Retrieved Notes:** [94, 642, 492, 96, 432, 692, 792, 892]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 1.000 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 1.000 |
| R-Precision | 1.000 |
| Latency (ms) | 80.77 |
| Predicted Intent | general |
| Expected Intent | reference |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Reference Notes |
| Category Correct | False |

---

### RERANK — Flutter improvements

- **Benchmark ID:** 9
- **Difficulty:** easy
- **Relevant Notes:** [97, 98]
- **Retrieved Notes:** [98, 97, 93, 372, 564, 467, 142, 655]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 1.000 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 1.000 |
| R-Precision | 1.000 |
| Latency (ms) | 83.50 |
| Predicted Intent | general |
| Expected Intent | reference |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Reference Notes |
| Category Correct | False |

---

### RERANK — Networking concepts

- **Benchmark ID:** 10
- **Difficulty:** easy
- **Relevant Notes:** [71, 62]
- **Retrieved Notes:** [491, 722, 822, 922, 1022, 532, 99, 633]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 74.11 |
| Predicted Intent | idea |
| Expected Intent | study |
| Intent Correct | False |
| Predicted Category | Ideas - AI |
| Expected Category | Study Tasks |
| Category Correct | False |

---

### RERANK — Object oriented programming revision

- **Benchmark ID:** 11
- **Difficulty:** easy
- **Relevant Notes:** [59, 60]
- **Retrieved Notes:** [163, 414, 227, 193, 679, 779, 879, 979]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 71.53 |
| Predicted Intent | study |
| Expected Intent | study |
| Intent Correct | True |

---

### RERANK — Interview preparation

- **Benchmark ID:** 12
- **Difficulty:** medium
- **Relevant Notes:** [70, 99]
- **Retrieved Notes:** [352, 100, 360, 70, 609, 507, 154, 288]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.500 |
| Hit | True |
| Reciprocal Rank | 0.250 |
| MAP@5 | 0.125 |
| R-Precision | 0.000 |
| Latency (ms) | 82.74 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Study Tasks |
| Category Correct | False |

---

### RERANK — Portfolio website

- **Benchmark ID:** 13
- **Difficulty:** easy
- **Relevant Notes:** [100, 97]
- **Retrieved Notes:** [266, 751, 851, 951, 1051, 131, 117, 528]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 80.21 |
| Predicted Intent | general |
| Expected Intent | todo |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | To Do |
| Category Correct | False |

---

### RERANK — Documentation tasks

- **Benchmark ID:** 14
- **Difficulty:** easy
- **Relevant Notes:** [96, 95]
- **Retrieved Notes:** [110, 96, 485, 87, 583, 699, 799, 899]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.500 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| MAP@5 | 0.250 |
| R-Precision | 0.500 |
| Latency (ms) | 71.51 |
| Predicted Intent | reference |
| Expected Intent | todo |
| Intent Correct | False |
| Predicted Category | Reference - Knowledgevault Backend |
| Expected Category | To Do |
| Category Correct | False |

---

### RERANK — Deploy KnowledgeVault

- **Benchmark ID:** 15
- **Difficulty:** easy
- **Relevant Notes:** [91]
- **Retrieved Notes:** [91, 89, 95, 90, 125, 96, 94, 88]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 1.000 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 1.000 |
| R-Precision | 1.000 |
| Latency (ms) | 94.18 |
| Predicted Intent | todo |
| Expected Intent | todo |
| Intent Correct | True |
| Predicted Category | Tasks |
| Expected Category | To Do |
| Category Correct | True |

---

### RERANK — Update GitHub README

- **Benchmark ID:** 16
- **Difficulty:** easy
- **Relevant Notes:** [96]
- **Retrieved Notes:** [440, 501, 522, 395, 400, 328, 612, 646]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 87.59 |
| Predicted Intent | todo |
| Expected Intent | todo |
| Intent Correct | True |
| Predicted Category | Tasks |
| Expected Category | To Do |
| Category Correct | True |

---

### RERANK — Resume preparation

- **Benchmark ID:** 17
- **Difficulty:** easy
- **Relevant Notes:** [100]
- **Retrieved Notes:** [100, 525, 142, 185, 523, 107, 288, 352]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 1.000 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 1.000 |
| R-Precision | 1.000 |
| Latency (ms) | 80.83 |
| Predicted Intent | general |
| Expected Intent | todo |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | To Do |
| Category Correct | False |

---

### RERANK — Weekend trip

- **Benchmark ID:** 18
- **Difficulty:** easy
- **Relevant Notes:** [81]
- **Retrieved Notes:** [77, 81, 128, 407, 190, 198, 351, 324]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 1.000 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| MAP@5 | 0.500 |
| R-Precision | 0.000 |
| Latency (ms) | 79.95 |
| Predicted Intent | general |
| Expected Intent | todo |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | To Do |
| Category Correct | False |

---

### RERANK — Bills to pay

- **Benchmark ID:** 19
- **Difficulty:** medium
- **Relevant Notes:** [77, 82]
- **Retrieved Notes:** [77, 341, 82, 393, 368, 312, 490, 178]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 1.000 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.833 |
| R-Precision | 0.500 |
| Latency (ms) | 99.64 |
| Predicted Intent | todo |
| Expected Intent | todo |
| Intent Correct | True |
| Predicted Category | Bills |
| Expected Category | To Do |
| Category Correct | True |

---

### RERANK — Doctor appointment

- **Benchmark ID:** 20
- **Difficulty:** easy
- **Relevant Notes:** [78, 79]
- **Retrieved Notes:** [559, 79, 198, 601, 78, 609, 70, 56]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 1.000 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| MAP@5 | 0.450 |
| R-Precision | 0.500 |
| Latency (ms) | 76.71 |
| Predicted Intent | reminder |
| Expected Intent | todo |
| Intent Correct | False |
| Predicted Category | Appointments |
| Expected Category | To Do |
| Category Correct | True |

---

### RERANK — Shopping list

- **Benchmark ID:** 21
- **Difficulty:** medium
- **Relevant Notes:** [76]
- **Retrieved Notes:** [170, 393, 606, 322, 76, 475, 216, 115]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 1.000 |
| Hit | True |
| Reciprocal Rank | 0.200 |
| MAP@5 | 0.200 |
| R-Precision | 0.000 |
| Latency (ms) | 79.09 |
| Predicted Intent | general |
| Expected Intent | todo |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | To Do |
| Category Correct | False |

---

### RERANK — Things I need to tell Sid

- **Benchmark ID:** 22
- **Difficulty:** easy
- **Relevant Notes:** [54, 55, 56, 57]
- **Retrieved Notes:** [54, 57, 56, 55, 423, 247, 442, 755]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.800 |
| Recall@5 | 1.000 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 1.000 |
| R-Precision | 1.000 |
| Latency (ms) | 74.92 |
| Predicted Intent | communication |
| Expected Intent | communication |
| Intent Correct | True |
| Predicted Category | Communication - Sid |
| Expected Category | Things to Tell Sid |
| Category Correct | True |

---

### RERANK — Next meeting with the design team

- **Benchmark ID:** 23
- **Difficulty:** medium
- **Relevant Notes:** [106, 107]
- **Retrieved Notes:** [57, 88, 568, 106, 448, 360, 56, 107]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.500 |
| Hit | True |
| Reciprocal Rank | 0.250 |
| MAP@5 | 0.125 |
| R-Precision | 0.000 |
| Latency (ms) | 69.92 |
| Predicted Intent | event |
| Expected Intent | meeting |
| Intent Correct | False |

---

### RERANK — Project deadline for the alpha release

- **Benchmark ID:** 24
- **Difficulty:** easy
- **Relevant Notes:** [89, 91]
- **Retrieved Notes:** [233, 498, 190, 252, 257, 264, 270, 289]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 96.16 |
| Predicted Intent | todo |
| Expected Intent | project |
| Intent Correct | False |
| Predicted Category | Tasks |
| Expected Category | Projects |
| Category Correct | False |

---

### RERANK — Remind me to call mom

- **Benchmark ID:** 25
- **Difficulty:** easy
- **Relevant Notes:** [78, 79]
- **Retrieved Notes:** [382, 475, 79, 312, 56, 78, 77, 54]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.500 |
| Hit | True |
| Reciprocal Rank | 0.333 |
| MAP@5 | 0.167 |
| R-Precision | 0.000 |
| Latency (ms) | 69.90 |
| Predicted Intent | communication |
| Expected Intent | todo |
| Intent Correct | False |

---

### RERANK — What is the theory of relativity?

- **Benchmark ID:** 26
- **Difficulty:** easy
- **Relevant Notes:** [103, 104, 105]
- **Retrieved Notes:** [489, 290, 565, 225, 116, 424, 306, 102]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 72.99 |
| Predicted Intent | question |
| Expected Intent | question |
| Intent Correct | True |

---

### RERANK — Ideas for my new blog post

- **Benchmark ID:** 27
- **Difficulty:** medium
- **Relevant Notes:** [85, 86, 87, 88]
- **Retrieved Notes:** [255, 555, 582, 554, 86, 413, 85, 525]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.250 |
| Hit | True |
| Reciprocal Rank | 0.200 |
| MAP@5 | 0.050 |
| R-Precision | 0.000 |
| Latency (ms) | 75.25 |
| Predicted Intent | idea |
| Expected Intent | idea |
| Intent Correct | True |

---

### RERANK — How to set up a kubernetes cluster

- **Benchmark ID:** 28
- **Difficulty:** hard
- **Relevant Notes:** [62]
- **Retrieved Notes:** [62, 118, 712, 812, 912, 1012, 410, 383]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 1.000 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 1.000 |
| R-Precision | 1.000 |
| Latency (ms) | 74.82 |
| Predicted Intent | question |
| Expected Intent | study |
| Intent Correct | False |

---

### RERANK — Things to discuss with Sid at the next meeting

- **Benchmark ID:** 29
- **Difficulty:** easy
- **Relevant Notes:** [54, 55, 56, 57]
- **Retrieved Notes:** [57, 54, 56, 423, 247, 55, 203, 442]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.600 |
| Recall@5 | 0.750 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.750 |
| R-Precision | 0.750 |
| Latency (ms) | 73.71 |
| Predicted Intent | communication |
| Expected Intent | communication |
| Intent Correct | True |
| Predicted Category | Communication - Sid |
| Expected Category | Things to Tell Sid |
| Category Correct | True |

---

### RERANK — Study materials for machine learning

- **Benchmark ID:** 30
- **Difficulty:** medium
- **Relevant Notes:** [64, 65, 66, 67]
- **Retrieved Notes:** [309, 528, 439, 619, 357, 60, 360, 66]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.125 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 71.55 |
| Predicted Intent | study |
| Expected Intent | study |
| Intent Correct | True |

---

### RERANK — Meeting notes from Q3 planning

- **Benchmark ID:** 31
- **Difficulty:** easy
- **Relevant Notes:** [106, 107]
- **Retrieved Notes:** [203, 106, 87, 290, 107, 372, 448, 175]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 1.000 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| MAP@5 | 0.450 |
| R-Precision | 0.500 |
| Latency (ms) | 69.99 |
| Predicted Intent | event |
| Expected Intent | meeting |
| Intent Correct | False |

---

### RERANK — What are the project requirements for KnowledgeVault?

- **Benchmark ID:** 32
- **Difficulty:** medium
- **Relevant Notes:** [89, 90, 91, 92, 93, 94, 95, 96]
- **Retrieved Notes:** [95, 638, 125, 90, 262, 89, 57, 247]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.250 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.188 |
| R-Precision | 0.375 |
| Latency (ms) | 76.23 |
| Predicted Intent | question |
| Expected Intent | reference |
| Intent Correct | False |

---

### RERANK — Reminders for next week

- **Benchmark ID:** 33
- **Difficulty:** medium
- **Relevant Notes:** [76, 77, 78, 79, 80]
- **Retrieved Notes:** [79, 56, 423, 312, 475, 77, 198, 382]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.200 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.200 |
| R-Precision | 0.200 |
| Latency (ms) | 76.05 |
| Predicted Intent | reminder |
| Expected Intent | todo |
| Intent Correct | False |
| Predicted Category | Reminders |
| Expected Category | To Do |
| Category Correct | False |

---

### RERANK — Questions to ask during the interview

- **Benchmark ID:** 34
- **Difficulty:** easy
- **Relevant Notes:** [70, 99]
- **Retrieved Notes:** [352, 70, 154, 99, 360, 468, 294, 199]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 1.000 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| MAP@5 | 0.500 |
| R-Precision | 0.500 |
| Latency (ms) | 74.57 |
| Predicted Intent | communication |
| Expected Intent | question |
| Intent Correct | False |

---

### RERANK — Brainstorming app names

- **Benchmark ID:** 35
- **Difficulty:** easy
- **Relevant Notes:** [85, 86, 87, 88]
- **Retrieved Notes:** [85, 97, 330, 117, 568, 617, 448, 155]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.250 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.250 |
| R-Precision | 0.250 |
| Latency (ms) | 77.29 |
| Predicted Intent | idea |
| Expected Intent | idea |
| Intent Correct | True |
| Predicted Category | Ideas - AI |
| Expected Category | Ideas |
| Category Correct | True |

---

### RERANK — Redis and PostgreSQL reference notes

- **Benchmark ID:** 36
- **Difficulty:** hard
- **Relevant Notes:** [73, 74, 58]
- **Retrieved Notes:** [73, 74, 269, 724, 824, 924, 1024, 421]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.667 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.667 |
| R-Precision | 0.667 |
| Latency (ms) | 80.87 |
| Predicted Intent | reference |
| Expected Intent | reference |
| Intent Correct | True |
| Predicted Category | Reference - PostgreSQL |
| Expected Category | Reference Notes |
| Category Correct | True |

---

### RERANK — Message to send to Siddhant about backend

- **Benchmark ID:** 37
- **Difficulty:** medium
- **Relevant Notes:** [56, 57, 54]
- **Retrieved Notes:** [56, 423, 54, 55, 57, 106, 392, 372]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.600 |
| Recall@5 | 1.000 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.756 |
| R-Precision | 0.667 |
| Latency (ms) | 74.23 |
| Predicted Intent | communication |
| Expected Intent | communication |
| Intent Correct | True |

---

### RERANK — Study schedule for finals

- **Benchmark ID:** 38
- **Difficulty:** easy
- **Relevant Notes:** [58, 59, 60, 61]
- **Retrieved Notes:** [198, 617, 434, 601, 448, 521, 107, 343]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 69.03 |
| Predicted Intent | study |
| Expected Intent | study |
| Intent Correct | True |

---

### RERANK — Sprint planning meeting summary

- **Benchmark ID:** 39
- **Difficulty:** easy
- **Relevant Notes:** [107, 106]
- **Retrieved Notes:** [107, 294, 466, 498, 263, 203, 216, 448]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.500 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.500 |
| R-Precision | 0.500 |
| Latency (ms) | 66.19 |
| Predicted Intent | event |
| Expected Intent | meeting |
| Intent Correct | False |

---

### RERANK — Timeline for the beta launch

- **Benchmark ID:** 40
- **Difficulty:** medium
- **Relevant Notes:** [89, 91]
- **Retrieved Notes:** [155, 190, 252, 257, 264, 270, 289, 309]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 100.09 |
| Predicted Intent | todo |
| Expected Intent | todo |
| Intent Correct | True |
| Predicted Category | Tasks |
| Expected Category | To Do |
| Category Correct | True |

---

### RERANK — Don't forget to buy milk

- **Benchmark ID:** 41
- **Difficulty:** easy
- **Relevant Notes:** [76]
- **Retrieved Notes:** [76, 322, 475, 84, 286, 78, 83, 79]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 1.000 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 1.000 |
| R-Precision | 1.000 |
| Latency (ms) | 105.23 |
| Predicted Intent | todo |
| Expected Intent | todo |
| Intent Correct | True |
| Predicted Category | Shopping |
| Expected Category | To Do |
| Category Correct | True |

---

### RERANK — How does Redis eviction work?

- **Benchmark ID:** 42
- **Difficulty:** easy
- **Relevant Notes:** [103, 73, 61]
- **Retrieved Notes:** [103, 73, 643, 673, 773, 873, 973, 1073]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.667 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.667 |
| R-Precision | 0.667 |
| Latency (ms) | 79.46 |
| Predicted Intent | question |
| Expected Intent | question |
| Intent Correct | True |

---

### RERANK — Ideas for improving KnowledgeVault

- **Benchmark ID:** 43
- **Difficulty:** medium
- **Relevant Notes:** [86, 87, 88, 89, 90]
- **Retrieved Notes:** [90, 125, 89, 638, 88, 428, 728, 828]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.600 |
| Recall@5 | 0.600 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.453 |
| R-Precision | 0.600 |
| Latency (ms) | 75.57 |
| Predicted Intent | idea |
| Expected Intent | idea |
| Intent Correct | True |

---

### RERANK — Docker commands cheat sheet

- **Benchmark ID:** 44
- **Difficulty:** easy
- **Relevant Notes:** [72, 75]
- **Retrieved Notes:** [72, 75, 355, 688, 788, 888, 988, 1088]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 1.000 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 1.000 |
| R-Precision | 1.000 |
| Latency (ms) | 84.51 |
| Predicted Intent | reference |
| Expected Intent | reference |
| Intent Correct | True |
| Predicted Category | Reference - Docker |
| Expected Category | Reference Notes |
| Category Correct | True |

---

### RERANK — Tell Sid about the hackathon

- **Benchmark ID:** 45
- **Difficulty:** easy
- **Relevant Notes:** [55, 54]
- **Retrieved Notes:** [55, 57, 54, 423, 448, 56, 542, 324]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 1.000 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.833 |
| R-Precision | 0.500 |
| Latency (ms) | 78.61 |
| Predicted Intent | communication |
| Expected Intent | communication |
| Intent Correct | True |
| Predicted Category | Communication - Sid |
| Expected Category | Things to Tell Sid |
| Category Correct | True |

---

### RERANK — System design interview study

- **Benchmark ID:** 46
- **Difficulty:** medium
- **Relevant Notes:** [70, 99, 59, 60]
- **Retrieved Notes:** [70, 99, 360, 309, 106, 392, 540, 352]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.500 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.500 |
| R-Precision | 0.500 |
| Latency (ms) | 76.21 |
| Predicted Intent | study |
| Expected Intent | study |
| Intent Correct | True |
| Predicted Category | Study - System Design |
| Expected Category | Study Tasks |
| Category Correct | True |

---

### RERANK — Weekly sync notes

- **Benchmark ID:** 47
- **Difficulty:** easy
- **Relevant Notes:** [106, 107]
- **Retrieved Notes:** [620, 372, 87, 203, 631, 393, 444, 107]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.125 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 74.71 |
| Predicted Intent | reference |
| Expected Intent | meeting |
| Intent Correct | False |

---

### RERANK — Budget and monthly expenses

- **Benchmark ID:** 48
- **Difficulty:** medium
- **Relevant Notes:** [82, 77]
- **Retrieved Notes:** [82, 216, 535, 281, 606, 490, 393, 341]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.500 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.500 |
| R-Precision | 0.500 |
| Latency (ms) | 80.53 |
| Predicted Intent | general |
| Expected Intent | todo |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | To Do |
| Category Correct | False |

---

### RERANK — Health checkup and appointments

- **Benchmark ID:** 49
- **Difficulty:** easy
- **Relevant Notes:** [78, 79, 80]
- **Retrieved Notes:** [79, 601, 559, 109, 475, 575, 198, 231]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.333 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.333 |
| R-Precision | 0.333 |
| Latency (ms) | 88.04 |
| Predicted Intent | reminder |
| Expected Intent | todo |
| Intent Correct | False |
| Predicted Category | Appointments |
| Expected Category | To Do |
| Category Correct | True |

---

### RERANK — What are PostgreSQL index types?

- **Benchmark ID:** 50
- **Difficulty:** easy
- **Relevant Notes:** [104, 74, 58]
- **Retrieved Notes:** [104, 417, 731, 831, 931, 1031, 58, 74]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.333 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.333 |
| R-Precision | 0.333 |
| Latency (ms) | 86.41 |
| Predicted Intent | question |
| Expected Intent | question |
| Intent Correct | True |

---

### BM25 — What startup ideas do I have?

- **Benchmark ID:** 1
- **Difficulty:** easy
- **Relevant Notes:** [85, 86, 87]
- **Retrieved Notes:** [85, 525, 617]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.333 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.333 |
| R-Precision | 0.333 |
| Latency (ms) | 4.11 |

---

### BM25 — Show my AI research reading goals

- **Benchmark ID:** 2
- **Difficulty:** easy
- **Relevant Notes:** [65, 64, 66, 67]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 1.56 |

---

### BM25 — How can I improve my health?

- **Benchmark ID:** 3
- **Difficulty:** medium
- **Relevant Notes:** [83, 84]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 1.50 |

---

### BM25 — Show my finance reminders

- **Benchmark ID:** 4
- **Difficulty:** easy
- **Relevant Notes:** [77, 82]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 1.53 |

---

### BM25 — Evaluation report work

- **Benchmark ID:** 5
- **Difficulty:** medium
- **Relevant Notes:** [90, 89]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 1.56 |

---

### BM25 — Markdown support

- **Benchmark ID:** 6
- **Difficulty:** easy
- **Relevant Notes:** [72, 73, 74, 75]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 2.20 |

---

### BM25 — Improve search latency

- **Benchmark ID:** 7
- **Difficulty:** easy
- **Relevant Notes:** [93, 89]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 1.72 |

---

### BM25 — Attachment upload feature

- **Benchmark ID:** 8
- **Difficulty:** easy
- **Relevant Notes:** [94]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 1.50 |

---

### BM25 — Flutter improvements

- **Benchmark ID:** 9
- **Difficulty:** easy
- **Relevant Notes:** [97, 98]
- **Retrieved Notes:** [98]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.500 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.500 |
| R-Precision | 0.500 |
| Latency (ms) | 1.50 |

---

### BM25 — Networking concepts

- **Benchmark ID:** 10
- **Difficulty:** easy
- **Relevant Notes:** [71, 62]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 1.37 |

---

### BM25 — Object oriented programming revision

- **Benchmark ID:** 11
- **Difficulty:** easy
- **Relevant Notes:** [59, 60]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 1.38 |

---

### BM25 — Interview preparation

- **Benchmark ID:** 12
- **Difficulty:** medium
- **Relevant Notes:** [70, 99]
- **Retrieved Notes:** [352, 468]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 1.55 |

---

### BM25 — Portfolio website

- **Benchmark ID:** 13
- **Difficulty:** easy
- **Relevant Notes:** [100, 97]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 1.38 |

---

### BM25 — Documentation tasks

- **Benchmark ID:** 14
- **Difficulty:** easy
- **Relevant Notes:** [96, 95]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 4.23 |

---

### BM25 — Deploy KnowledgeVault

- **Benchmark ID:** 15
- **Difficulty:** easy
- **Relevant Notes:** [91]
- **Retrieved Notes:** [91, 607, 753, 853, 953, 1053]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 1.000 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 1.000 |
| R-Precision | 1.000 |
| Latency (ms) | 2.30 |

---

### BM25 — Update GitHub README

- **Benchmark ID:** 16
- **Difficulty:** easy
- **Relevant Notes:** [96]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 1.70 |

---

### BM25 — Resume preparation

- **Benchmark ID:** 17
- **Difficulty:** easy
- **Relevant Notes:** [100]
- **Retrieved Notes:** [100]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 1.000 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 1.000 |
| R-Precision | 1.000 |
| Latency (ms) | 1.43 |

---

### BM25 — Weekend trip

- **Benchmark ID:** 18
- **Difficulty:** easy
- **Relevant Notes:** [81]
- **Retrieved Notes:** [128, 324]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 1.52 |

---

### BM25 — Bills to pay

- **Benchmark ID:** 19
- **Difficulty:** medium
- **Relevant Notes:** [77, 82]
- **Retrieved Notes:** [77, 341, 312, 490]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.500 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.500 |
| R-Precision | 0.500 |
| Latency (ms) | 1.60 |

---

### BM25 — Doctor appointment

- **Benchmark ID:** 20
- **Difficulty:** easy
- **Relevant Notes:** [78, 79]
- **Retrieved Notes:** [231]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 1.56 |

---

### BM25 — Shopping list

- **Benchmark ID:** 21
- **Difficulty:** medium
- **Relevant Notes:** [76]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 1.33 |

---

### BM25 — Things I need to tell Sid

- **Benchmark ID:** 22
- **Difficulty:** easy
- **Relevant Notes:** [54, 55, 56, 57]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 1.50 |

---

### BM25 — Next meeting with the design team

- **Benchmark ID:** 23
- **Difficulty:** medium
- **Relevant Notes:** [106, 107]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 1.55 |

---

### BM25 — Project deadline for the alpha release

- **Benchmark ID:** 24
- **Difficulty:** easy
- **Relevant Notes:** [89, 91]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 1.44 |

---

### BM25 — Remind me to call mom

- **Benchmark ID:** 25
- **Difficulty:** easy
- **Relevant Notes:** [78, 79]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 1.36 |

---

### BM25 — What is the theory of relativity?

- **Benchmark ID:** 26
- **Difficulty:** easy
- **Relevant Notes:** [103, 104, 105]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 1.46 |

---

### BM25 — Ideas for my new blog post

- **Benchmark ID:** 27
- **Difficulty:** medium
- **Relevant Notes:** [85, 86, 87, 88]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 1.44 |

---

### BM25 — How to set up a kubernetes cluster

- **Benchmark ID:** 28
- **Difficulty:** hard
- **Relevant Notes:** [62]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 1.47 |

---

### BM25 — Things to discuss with Sid at the next meeting

- **Benchmark ID:** 29
- **Difficulty:** easy
- **Relevant Notes:** [54, 55, 56, 57]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 1.49 |

---

### BM25 — Study materials for machine learning

- **Benchmark ID:** 30
- **Difficulty:** medium
- **Relevant Notes:** [64, 65, 66, 67]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 1.48 |

---

### BM25 — Meeting notes from Q3 planning

- **Benchmark ID:** 31
- **Difficulty:** easy
- **Relevant Notes:** [106, 107]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 4.41 |

---

### BM25 — What are the project requirements for KnowledgeVault?

- **Benchmark ID:** 32
- **Difficulty:** medium
- **Relevant Notes:** [89, 90, 91, 92, 93, 94, 95, 96]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 1.79 |

---

### BM25 — Reminders for next week

- **Benchmark ID:** 33
- **Difficulty:** medium
- **Relevant Notes:** [76, 77, 78, 79, 80]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 1.45 |

---

### BM25 — Questions to ask during the interview

- **Benchmark ID:** 34
- **Difficulty:** easy
- **Relevant Notes:** [70, 99]
- **Retrieved Notes:** [352, 154]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 1.65 |

---

### BM25 — Brainstorming app names

- **Benchmark ID:** 35
- **Difficulty:** easy
- **Relevant Notes:** [85, 86, 87, 88]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 1.44 |

---

### BM25 — Redis and PostgreSQL reference notes

- **Benchmark ID:** 36
- **Difficulty:** hard
- **Relevant Notes:** [73, 74, 58]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 1.56 |

---

### BM25 — Message to send to Siddhant about backend

- **Benchmark ID:** 37
- **Difficulty:** medium
- **Relevant Notes:** [56, 57, 54]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 1.57 |

---

### BM25 — Study schedule for finals

- **Benchmark ID:** 38
- **Difficulty:** easy
- **Relevant Notes:** [58, 59, 60, 61]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 1.62 |

---

### BM25 — Sprint planning meeting summary

- **Benchmark ID:** 39
- **Difficulty:** easy
- **Relevant Notes:** [107, 106]
- **Retrieved Notes:** [107]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.500 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.500 |
| R-Precision | 0.500 |
| Latency (ms) | 1.78 |

---

### BM25 — Timeline for the beta launch

- **Benchmark ID:** 40
- **Difficulty:** medium
- **Relevant Notes:** [89, 91]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 2.11 |

---

### BM25 — Don't forget to buy milk

- **Benchmark ID:** 41
- **Difficulty:** easy
- **Relevant Notes:** [76]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 1.49 |

---

### BM25 — How does Redis eviction work?

- **Benchmark ID:** 42
- **Difficulty:** easy
- **Relevant Notes:** [103, 73, 61]
- **Retrieved Notes:** [103]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.333 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.333 |
| R-Precision | 0.333 |
| Latency (ms) | 1.69 |

---

### BM25 — Ideas for improving KnowledgeVault

- **Benchmark ID:** 43
- **Difficulty:** medium
- **Relevant Notes:** [86, 87, 88, 89, 90]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 1.52 |

---

### BM25 — Docker commands cheat sheet

- **Benchmark ID:** 44
- **Difficulty:** easy
- **Relevant Notes:** [72, 75]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 1.55 |

---

### BM25 — Tell Sid about the hackathon

- **Benchmark ID:** 45
- **Difficulty:** easy
- **Relevant Notes:** [55, 54]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 1.92 |

---

### BM25 — System design interview study

- **Benchmark ID:** 46
- **Difficulty:** medium
- **Relevant Notes:** [70, 99, 59, 60]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 1.47 |

---

### BM25 — Weekly sync notes

- **Benchmark ID:** 47
- **Difficulty:** easy
- **Relevant Notes:** [106, 107]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 1.79 |

---

### BM25 — Budget and monthly expenses

- **Benchmark ID:** 48
- **Difficulty:** medium
- **Relevant Notes:** [82, 77]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 1.85 |

---

### BM25 — Health checkup and appointments

- **Benchmark ID:** 49
- **Difficulty:** easy
- **Relevant Notes:** [78, 79, 80]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 1.86 |

---

### BM25 — What are PostgreSQL index types?

- **Benchmark ID:** 50
- **Difficulty:** easy
- **Relevant Notes:** [104, 74, 58]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 1.64 |

---

### HYBRID_BM25 — What startup ideas do I have?

- **Benchmark ID:** 1
- **Difficulty:** easy
- **Relevant Notes:** [85, 86, 87]
- **Retrieved Notes:** [85, 525, 617, 134, 441, 553, 459, 255, 166, 685, 785, 885, 985, 1085, 178, 475, 322, 391, 607, 753]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.333 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.333 |
| R-Precision | 0.333 |
| Latency (ms) | 26.04 |

---

### HYBRID_BM25 — Show my AI research reading goals

- **Benchmark ID:** 2
- **Difficulty:** easy
- **Relevant Notes:** [65, 64, 66, 67]
- **Retrieved Notes:** [529, 617, 416, 85, 230, 87, 65, 122, 166, 685, 785, 885, 985, 1085, 240, 525, 523, 290, 413, 235]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.143 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 30.58 |

---

### HYBRID_BM25 — How can I improve my health?

- **Benchmark ID:** 3
- **Difficulty:** medium
- **Relevant Notes:** [83, 84]
- **Retrieved Notes:** [84, 109, 83, 79, 286, 322, 380, 680, 780, 880, 980, 1080, 76, 157, 355, 688, 788, 888, 988, 1088]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 1.000 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.833 |
| R-Precision | 0.500 |
| Latency (ms) | 25.19 |

---

### HYBRID_BM25 — Show my finance reminders

- **Benchmark ID:** 4
- **Difficulty:** easy
- **Relevant Notes:** [77, 82]
- **Retrieved Notes:** [216, 312, 82, 77, 393, 375, 735, 835, 935, 1035, 442, 755, 855, 955, 1055, 583, 699, 799, 899, 999]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 1.000 |
| Hit | True |
| Reciprocal Rank | 0.333 |
| MAP@5 | 0.417 |
| R-Precision | 0.000 |
| Latency (ms) | 28.14 |

---

### HYBRID_BM25 — Evaluation report work

- **Benchmark ID:** 5
- **Difficulty:** medium
- **Relevant Notes:** [90, 89]
- **Retrieved Notes:** [616, 90, 485, 453, 375, 735, 835, 935, 1035, 487, 525, 310, 555, 470, 251, 185, 498, 213, 729, 829]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.500 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| MAP@5 | 0.250 |
| R-Precision | 0.500 |
| Latency (ms) | 27.57 |

---

### HYBRID_BM25 — Markdown support

- **Benchmark ID:** 6
- **Difficulty:** easy
- **Relevant Notes:** [72, 73, 74, 75]
- **Retrieved Notes:** [558, 568, 492, 582, 96, 289, 581, 653, 87, 251, 523, 625, 449, 442, 755, 855, 955, 1055, 386, 338]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 25.13 |

---

### HYBRID_BM25 — Improve search latency

- **Benchmark ID:** 7
- **Difficulty:** easy
- **Relevant Notes:** [93, 89]
- **Retrieved Notes:** [93, 402, 195, 333, 86, 644, 567, 704, 804, 904, 1004, 1104, 213, 729, 829, 929, 1029, 58, 61, 310]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.500 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.500 |
| R-Precision | 0.500 |
| Latency (ms) | 26.25 |

---

### HYBRID_BM25 — Attachment upload feature

- **Benchmark ID:** 8
- **Difficulty:** easy
- **Relevant Notes:** [94]
- **Retrieved Notes:** [94, 642, 492, 96, 432, 692, 792, 892, 992, 1092, 386, 506, 523, 465, 486, 702, 802, 902, 1002, 1102]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 1.000 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 1.000 |
| R-Precision | 1.000 |
| Latency (ms) | 25.40 |

---

### HYBRID_BM25 — Flutter improvements

- **Benchmark ID:** 9
- **Difficulty:** easy
- **Relevant Notes:** [97, 98]
- **Retrieved Notes:** [98, 97, 93, 372, 564, 467, 142, 655, 653, 61, 444, 175, 337, 295, 568, 442, 755, 855, 955, 1055]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 1.000 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 1.000 |
| R-Precision | 1.000 |
| Latency (ms) | 21.51 |

---

### HYBRID_BM25 — Networking concepts

- **Benchmark ID:** 10
- **Difficulty:** easy
- **Relevant Notes:** [71, 62]
- **Retrieved Notes:** [491, 722, 822, 922, 1022, 532, 99, 633, 439, 327, 106, 516, 711, 811, 911, 1011, 62, 392, 159, 299]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.059 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 24.98 |

---

### HYBRID_BM25 — Object oriented programming revision

- **Benchmark ID:** 11
- **Difficulty:** easy
- **Relevant Notes:** [59, 60]
- **Retrieved Notes:** [163, 414, 227, 193, 679, 779, 879, 979, 1079, 330, 117, 235, 311, 390, 169, 562, 419, 247, 309, 270]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 25.26 |

---

### HYBRID_BM25 — Interview preparation

- **Benchmark ID:** 12
- **Difficulty:** medium
- **Relevant Notes:** [70, 99]
- **Retrieved Notes:** [352, 468, 100, 360, 70, 609, 507, 154, 288, 344, 199, 152, 294, 540, 99, 521, 126, 236, 413, 205]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.500 |
| Hit | True |
| Reciprocal Rank | 0.200 |
| MAP@5 | 0.100 |
| R-Precision | 0.000 |
| Latency (ms) | 26.97 |

---

### HYBRID_BM25 — Portfolio website

- **Benchmark ID:** 13
- **Difficulty:** easy
- **Relevant Notes:** [100, 97]
- **Retrieved Notes:** [266, 751, 851, 951, 1051, 131, 117, 528, 413, 555, 178, 360, 65, 66, 525, 619, 60, 175, 607, 753]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 26.27 |

---

### HYBRID_BM25 — Documentation tasks

- **Benchmark ID:** 14
- **Difficulty:** easy
- **Relevant Notes:** [96, 95]
- **Retrieved Notes:** [110, 96, 485, 87, 583, 699, 799, 899, 999, 1099, 453, 186, 565, 360, 558, 330, 487, 625, 523, 510]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.500 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| MAP@5 | 0.250 |
| R-Precision | 0.500 |
| Latency (ms) | 24.20 |

---

### HYBRID_BM25 — Deploy KnowledgeVault

- **Benchmark ID:** 15
- **Difficulty:** easy
- **Relevant Notes:** [91]
- **Retrieved Notes:** [91, 607, 753, 853, 953, 1053, 89, 90, 95, 125, 96, 88, 94, 638, 97, 57, 337, 262, 555, 251]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 1.000 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 1.000 |
| R-Precision | 1.000 |
| Latency (ms) | 25.67 |

---

### HYBRID_BM25 — Update GitHub README

- **Benchmark ID:** 16
- **Difficulty:** easy
- **Relevant Notes:** [96]
- **Retrieved Notes:** [440, 501, 395, 522, 400, 328, 612, 646, 366, 614, 235, 141, 497, 719, 819, 919, 1019, 193, 679, 779]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 24.84 |

---

### HYBRID_BM25 — Resume preparation

- **Benchmark ID:** 17
- **Difficulty:** easy
- **Relevant Notes:** [100]
- **Retrieved Notes:** [100, 525, 142, 185, 523, 107, 288, 352, 601, 521, 184, 360, 415, 485, 199, 617, 268, 682, 782, 882]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 1.000 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 1.000 |
| R-Precision | 1.000 |
| Latency (ms) | 25.01 |

---

### HYBRID_BM25 — Weekend trip

- **Benchmark ID:** 18
- **Difficulty:** easy
- **Relevant Notes:** [81]
- **Retrieved Notes:** [128, 324, 77, 81, 407, 190, 198, 351, 393, 575, 538, 400, 375, 735, 835, 935, 1035, 631, 627, 639]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 1.000 |
| Hit | True |
| Reciprocal Rank | 0.250 |
| MAP@5 | 0.250 |
| R-Precision | 0.000 |
| Latency (ms) | 25.18 |

---

### HYBRID_BM25 — Bills to pay

- **Benchmark ID:** 19
- **Difficulty:** medium
- **Relevant Notes:** [77, 82]
- **Retrieved Notes:** [77, 341, 312, 490, 82, 393, 368, 178, 331, 411, 216, 76, 140, 399, 371, 403, 635, 322, 285, 573]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 1.000 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.700 |
| R-Precision | 0.500 |
| Latency (ms) | 25.82 |

---

### HYBRID_BM25 — Doctor appointment

- **Benchmark ID:** 20
- **Difficulty:** easy
- **Relevant Notes:** [78, 79]
- **Retrieved Notes:** [231, 559, 79, 198, 601, 78, 609, 70, 56, 54, 575, 448, 288, 475, 111, 356, 423, 59, 57, 81]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.500 |
| Hit | True |
| Reciprocal Rank | 0.333 |
| MAP@5 | 0.167 |
| R-Precision | 0.000 |
| Latency (ms) | 21.47 |

---

### HYBRID_BM25 — Shopping list

- **Benchmark ID:** 21
- **Difficulty:** medium
- **Relevant Notes:** [76]
- **Retrieved Notes:** [393, 606, 322, 76, 475, 216, 115, 202, 605, 358, 145, 204, 182, 82, 265, 303, 331, 178, 309, 175]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 1.000 |
| Hit | True |
| Reciprocal Rank | 0.250 |
| MAP@5 | 0.250 |
| R-Precision | 0.000 |
| Latency (ms) | 24.50 |

---

### HYBRID_BM25 — Things I need to tell Sid

- **Benchmark ID:** 22
- **Difficulty:** easy
- **Relevant Notes:** [54, 55, 56, 57]
- **Retrieved Notes:** [54, 56, 57, 55, 423, 247, 442, 755, 855, 955, 1055, 203, 230, 382, 268, 682, 782, 882, 982, 1082]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.800 |
| Recall@5 | 1.000 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 1.000 |
| R-Precision | 1.000 |
| Latency (ms) | 27.25 |

---

### HYBRID_BM25 — Next meeting with the design team

- **Benchmark ID:** 23
- **Difficulty:** medium
- **Relevant Notes:** [106, 107]
- **Retrieved Notes:** [57, 88, 568, 106, 448, 360, 56, 107, 382, 626, 95, 528, 141, 175, 70, 330, 442, 755, 855, 955]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.500 |
| Hit | True |
| Reciprocal Rank | 0.250 |
| MAP@5 | 0.125 |
| R-Precision | 0.000 |
| Latency (ms) | 25.60 |

---

### HYBRID_BM25 — Project deadline for the alpha release

- **Benchmark ID:** 24
- **Difficulty:** easy
- **Relevant Notes:** [89, 91]
- **Retrieved Notes:** [233, 498, 453, 466, 528, 149, 553, 448, 620, 351, 607, 753, 853, 953, 1053, 155, 521, 653, 626, 527]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 25.04 |

---

### HYBRID_BM25 — Remind me to call mom

- **Benchmark ID:** 25
- **Difficulty:** easy
- **Relevant Notes:** [78, 79]
- **Retrieved Notes:** [382, 475, 79, 312, 56, 78, 77, 54, 290, 212, 182, 550, 700, 800, 900, 1000, 1100, 322, 55, 317]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.500 |
| Hit | True |
| Reciprocal Rank | 0.333 |
| MAP@5 | 0.167 |
| R-Precision | 0.000 |
| Latency (ms) | 24.43 |

---

### HYBRID_BM25 — What is the theory of relativity?

- **Benchmark ID:** 26
- **Difficulty:** easy
- **Relevant Notes:** [103, 104, 105]
- **Retrieved Notes:** [489, 290, 565, 225, 116, 424, 306, 102, 287, 613, 298, 726, 826, 926, 1026, 130, 608, 175, 179, 260]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 26.16 |

---

### HYBRID_BM25 — Ideas for my new blog post

- **Benchmark ID:** 27
- **Difficulty:** medium
- **Relevant Notes:** [85, 86, 87, 88]
- **Retrieved Notes:** [255, 555, 582, 554, 86, 413, 85, 525, 375, 735, 835, 935, 1035, 453, 337, 208, 442, 755, 855, 955]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.250 |
| Hit | True |
| Reciprocal Rank | 0.200 |
| MAP@5 | 0.050 |
| R-Precision | 0.000 |
| Latency (ms) | 21.67 |

---

### HYBRID_BM25 — How to set up a kubernetes cluster

- **Benchmark ID:** 28
- **Difficulty:** hard
- **Relevant Notes:** [62]
- **Retrieved Notes:** [62, 118, 712, 812, 912, 1012, 410, 383, 91, 352, 192, 439, 95, 609, 392, 566, 710, 810, 910, 1010]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 1.000 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 1.000 |
| R-Precision | 1.000 |
| Latency (ms) | 32.02 |

---

### HYBRID_BM25 — Things to discuss with Sid at the next meeting

- **Benchmark ID:** 29
- **Difficulty:** easy
- **Relevant Notes:** [54, 55, 56, 57]
- **Retrieved Notes:** [57, 54, 56, 423, 247, 55, 203, 442, 755, 855, 955, 1055, 230, 448, 263, 185, 175, 107, 81, 382]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.600 |
| Recall@5 | 0.750 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.750 |
| R-Precision | 0.750 |
| Latency (ms) | 25.63 |

---

### HYBRID_BM25 — Study materials for machine learning

- **Benchmark ID:** 30
- **Difficulty:** medium
- **Relevant Notes:** [64, 65, 66, 67]
- **Retrieved Notes:** [309, 528, 439, 619, 357, 60, 360, 66, 343, 592, 178, 74, 547, 266, 751, 851, 951, 1051, 196, 529]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.125 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 24.88 |

---

### HYBRID_BM25 — Meeting notes from Q3 planning

- **Benchmark ID:** 31
- **Difficulty:** easy
- **Relevant Notes:** [106, 107]
- **Retrieved Notes:** [203, 106, 87, 290, 107, 372, 448, 175, 438, 56, 371, 423, 212, 479, 444, 539, 141, 60, 617, 216]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 1.000 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| MAP@5 | 0.450 |
| R-Precision | 0.500 |
| Latency (ms) | 25.10 |

---

### HYBRID_BM25 — What are the project requirements for KnowledgeVault?

- **Benchmark ID:** 32
- **Difficulty:** medium
- **Relevant Notes:** [89, 90, 91, 92, 93, 94, 95, 96]
- **Retrieved Notes:** [95, 638, 125, 90, 262, 89, 57, 247, 555, 96, 97, 88, 413, 428, 728, 828, 928, 1028, 337, 107]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.250 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.188 |
| R-Precision | 0.375 |
| Latency (ms) | 24.75 |

---

### HYBRID_BM25 — Reminders for next week

- **Benchmark ID:** 33
- **Difficulty:** medium
- **Relevant Notes:** [76, 77, 78, 79, 80]
- **Retrieved Notes:** [79, 56, 423, 475, 77, 198, 382, 312, 631, 107, 392, 216, 442, 755, 855, 955, 1055, 57, 528, 620]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.400 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.280 |
| R-Precision | 0.400 |
| Latency (ms) | 23.94 |

---

### HYBRID_BM25 — Questions to ask during the interview

- **Benchmark ID:** 34
- **Difficulty:** easy
- **Relevant Notes:** [70, 99]
- **Retrieved Notes:** [352, 154, 70, 99, 360, 468, 294, 199, 540, 459, 593, 344, 609, 507, 413, 205, 54, 126, 398, 470]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 1.000 |
| Hit | True |
| Reciprocal Rank | 0.333 |
| MAP@5 | 0.417 |
| R-Precision | 0.000 |
| Latency (ms) | 24.34 |

---

### HYBRID_BM25 — Brainstorming app names

- **Benchmark ID:** 35
- **Difficulty:** easy
- **Relevant Notes:** [85, 86, 87, 88]
- **Retrieved Notes:** [85, 97, 330, 117, 568, 617, 448, 155, 525, 87, 266, 751, 851, 951, 1051, 459, 382, 175, 166, 685]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.250 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.250 |
| R-Precision | 0.250 |
| Latency (ms) | 24.40 |

---

### HYBRID_BM25 — Redis and PostgreSQL reference notes

- **Benchmark ID:** 36
- **Difficulty:** hard
- **Relevant Notes:** [73, 74, 58]
- **Retrieved Notes:** [73, 74, 269, 724, 824, 924, 1024, 421, 746, 846, 946, 1046, 92, 643, 673, 773, 873, 973, 1073, 61]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.667 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.667 |
| R-Precision | 0.667 |
| Latency (ms) | 26.28 |

---

### HYBRID_BM25 — Message to send to Siddhant about backend

- **Benchmark ID:** 37
- **Difficulty:** medium
- **Relevant Notes:** [56, 57, 54]
- **Retrieved Notes:** [56, 423, 54, 55, 57, 106, 392, 372, 129, 91, 132, 658, 758, 858, 958, 1058, 247, 61, 337, 96]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.600 |
| Recall@5 | 1.000 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.756 |
| R-Precision | 0.667 |
| Latency (ms) | 26.59 |

---

### HYBRID_BM25 — Study schedule for finals

- **Benchmark ID:** 38
- **Difficulty:** easy
- **Relevant Notes:** [58, 59, 60, 61]
- **Retrieved Notes:** [198, 617, 434, 601, 448, 521, 107, 343, 224, 524, 380, 680, 780, 880, 980, 1080, 317, 344, 495, 620]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 25.24 |

---

### HYBRID_BM25 — Sprint planning meeting summary

- **Benchmark ID:** 39
- **Difficulty:** easy
- **Relevant Notes:** [107, 106]
- **Retrieved Notes:** [107, 294, 466, 498, 263, 203, 216, 448, 567, 704, 804, 904, 1004, 1104, 423, 56, 438, 352, 468, 538]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.500 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.500 |
| R-Precision | 0.500 |
| Latency (ms) | 27.17 |

---

### HYBRID_BM25 — Timeline for the beta launch

- **Benchmark ID:** 40
- **Difficulty:** medium
- **Relevant Notes:** [89, 91]
- **Retrieved Notes:** [498, 466, 620, 233, 553, 107, 343, 255, 216, 528, 423, 448, 453, 324, 198, 631, 607, 753, 853, 953]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 24.53 |

---

### HYBRID_BM25 — Don't forget to buy milk

- **Benchmark ID:** 41
- **Difficulty:** easy
- **Relevant Notes:** [76]
- **Retrieved Notes:** [76, 322, 475, 84, 286, 78, 83, 79, 77, 281, 82, 190, 109, 212, 81, 437, 557, 312, 409, 175]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 1.000 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 1.000 |
| R-Precision | 1.000 |
| Latency (ms) | 24.89 |

---

### HYBRID_BM25 — How does Redis eviction work?

- **Benchmark ID:** 42
- **Difficulty:** easy
- **Relevant Notes:** [103, 73, 61]
- **Retrieved Notes:** [103, 73, 643, 673, 773, 873, 973, 1073, 433, 705, 805, 905, 1005, 1105, 92, 269, 724, 824, 924, 1024]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.667 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.667 |
| R-Precision | 0.667 |
| Latency (ms) | 25.41 |

---

### HYBRID_BM25 — Ideas for improving KnowledgeVault

- **Benchmark ID:** 43
- **Difficulty:** medium
- **Relevant Notes:** [86, 87, 88, 89, 90]
- **Retrieved Notes:** [90, 125, 89, 638, 88, 428, 728, 828, 928, 1028, 555, 95, 57, 97, 96, 262, 247, 337, 444, 107]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.600 |
| Recall@5 | 0.600 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.453 |
| R-Precision | 0.600 |
| Latency (ms) | 25.48 |

---

### HYBRID_BM25 — Docker commands cheat sheet

- **Benchmark ID:** 44
- **Difficulty:** easy
- **Relevant Notes:** [72, 75]
- **Retrieved Notes:** [72, 75, 355, 688, 788, 888, 988, 1088, 192, 105, 295, 138, 491, 722, 822, 922, 1022, 383, 91, 445]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 1.000 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 1.000 |
| R-Precision | 1.000 |
| Latency (ms) | 24.89 |

---

### HYBRID_BM25 — Tell Sid about the hackathon

- **Benchmark ID:** 45
- **Difficulty:** easy
- **Relevant Notes:** [55, 54]
- **Retrieved Notes:** [55, 57, 54, 423, 448, 56, 542, 324, 463, 319, 247, 535, 442, 755, 855, 955, 1055, 449, 553, 436]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 1.000 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.833 |
| R-Precision | 0.500 |
| Latency (ms) | 24.52 |

---

### HYBRID_BM25 — System design interview study

- **Benchmark ID:** 46
- **Difficulty:** medium
- **Relevant Notes:** [70, 99, 59, 60]
- **Retrieved Notes:** [70, 99, 360, 309, 106, 392, 540, 352, 102, 88, 199, 344, 59, 442, 755, 855, 955, 1055, 169, 126]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.500 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.500 |
| R-Precision | 0.500 |
| Latency (ms) | 24.89 |

---

### HYBRID_BM25 — Weekly sync notes

- **Benchmark ID:** 47
- **Difficulty:** easy
- **Relevant Notes:** [106, 107]
- **Retrieved Notes:** [620, 372, 87, 203, 631, 393, 444, 107, 216, 198, 565, 82, 202, 495, 582, 604, 331, 224, 375, 735]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.125 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 25.30 |

---

### HYBRID_BM25 — Budget and monthly expenses

- **Benchmark ID:** 48
- **Difficulty:** medium
- **Relevant Notes:** [82, 77]
- **Retrieved Notes:** [82, 216, 535, 281, 606, 490, 393, 341, 635, 538, 601, 331, 77, 403, 162, 115, 573, 564, 407, 210]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.500 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.500 |
| R-Precision | 0.500 |
| Latency (ms) | 27.43 |

---

### HYBRID_BM25 — Health checkup and appointments

- **Benchmark ID:** 49
- **Difficulty:** easy
- **Relevant Notes:** [78, 79, 80]
- **Retrieved Notes:** [79, 601, 559, 109, 475, 575, 198, 231, 82, 111, 355, 688, 788, 888, 988, 1088, 609, 620, 78, 157]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.333 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.333 |
| R-Precision | 0.333 |
| Latency (ms) | 25.66 |

---

### HYBRID_BM25 — What are PostgreSQL index types?

- **Benchmark ID:** 50
- **Difficulty:** easy
- **Relevant Notes:** [104, 74, 58]
- **Retrieved Notes:** [104, 417, 731, 831, 931, 1031, 58, 74, 280, 66, 567, 704, 804, 904, 1004, 1104, 139, 686, 786, 886]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.333 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.333 |
| R-Precision | 0.333 |
| Latency (ms) | 25.06 |

---


---

_Generated automatically by the KnowledgeVault Evaluation Framework._