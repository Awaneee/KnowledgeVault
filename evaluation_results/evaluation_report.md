# KnowledgeVault Evaluation Report

**Run ID:** `51bf070a-bf2d-4ce7-9f6f-e1b3ef862fc0`

**Created:** 2026-07-31T19:12:31.231055

**Git Commit:** `8316c96`

**Benchmark Version:** `2.0.0`

**Queries:** 205

**K:** 5

**Corpus Coverage:** 77.3% (fraction of notes touched across all retrieved sets)

## Strategy Comparison

| Strategy | Precision | Recall | Hit Rate | MRR | MRR 95% CI | MAP@K | R-Prec | nDCG | Intent Acc | Category Acc | Avg Latency (ms) |
|-----------|----------:|-------:|---------:|----:|:----------:|------:|-------:|-----:|------------:|-------------:|-----------------:|
| SEMANTIC | 0.282 | 0.297 | 0.746 | 0.580 | [0.519, 0.640] | 0.231 | 0.249 | 0.381 | - | - | 2.18 |
| INTENT | 0.040 | 0.046 | 0.132 | 0.112 | [0.073, 0.157] | 0.038 | 0.039 | 0.064 | 0.376 | 0.343 | 42.40 |
| HYBRID | 0.281 | 0.296 | 0.746 | 0.603 | [0.547, 0.661] | 0.234 | 0.279 | 0.385 | 0.376 | 0.343 | 190.02 |
| RERANK | 0.281 | 0.296 | 0.746 | 0.598 | [0.541, 0.657] | 0.234 | 0.276 | 0.385 | 0.376 | 0.343 | 106.89 |

## Statistical Comparisons (95% Bootstrap CI)

| Comparison | ΔMRR | MRR CI | Significant | ΔHIT | Hit CI | Recommendation |
|-----------|-----:|:------:|:-----------:|-----:|:------:|:--------------|
| HYBRID vs SEMANTIC | +0.0233 | [0.010, 0.038] | ✓ | +0.0000 | [0.000, 0.000] | approve_candidate |
| RERANK vs HYBRID | -0.0051 | [-0.008, -0.003] | ✓ | +0.0000 | [0.000, 0.000] | keep_baseline |

## Per-Difficulty Breakdown

| Strategy | Easy MRR | Hard MRR | Medium MRR |
| --- | ---: | ---: | ---: |
| HYBRID | 0.614 | 0.453 | 0.668 |
| INTENT | 0.209 | 0.026 | 0.042 |
| RERANK | 0.610 | 0.442 | 0.664 |
| SEMANTIC | 0.598 | 0.405 | 0.649 |

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
| Latency (ms) | 38.27 |

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
| Latency (ms) | 2.19 |

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
| Latency (ms) | 2.42 |

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
| Latency (ms) | 1.73 |

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
| Latency (ms) | 1.90 |

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
| Latency (ms) | 1.57 |

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
| Latency (ms) | 2.74 |

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
| Latency (ms) | 1.71 |

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
| Latency (ms) | 1.89 |

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
| Latency (ms) | 2.05 |

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
| Latency (ms) | 1.51 |

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
| Latency (ms) | 1.77 |

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
| Latency (ms) | 1.64 |

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
| Latency (ms) | 1.42 |

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
| Latency (ms) | 1.34 |

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
| Latency (ms) | 1.72 |

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
| Latency (ms) | 1.75 |

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
| Latency (ms) | 1.70 |

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
| Latency (ms) | 2.27 |

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
| Latency (ms) | 2.10 |

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
| Latency (ms) | 2.10 |

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
| Latency (ms) | 2.04 |

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
| Latency (ms) | 2.13 |

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
| Latency (ms) | 1.80 |

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
| Latency (ms) | 3.14 |

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
| Latency (ms) | 2.21 |

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
| Latency (ms) | 2.13 |

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
| Latency (ms) | 2.18 |

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
| Latency (ms) | 1.99 |

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
| Latency (ms) | 1.96 |

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
| Latency (ms) | 2.37 |

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
| Latency (ms) | 1.66 |

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
| Latency (ms) | 1.74 |

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
| Latency (ms) | 1.80 |

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
| Latency (ms) | 2.24 |

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
| Latency (ms) | 2.59 |

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
| Latency (ms) | 3.17 |

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
| Latency (ms) | 2.10 |

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
| Latency (ms) | 1.95 |

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
| Latency (ms) | 1.52 |

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
| Latency (ms) | 1.64 |

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
| Latency (ms) | 2.14 |

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
| Latency (ms) | 2.45 |

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
| Latency (ms) | 1.73 |

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
| Latency (ms) | 2.17 |

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
| Latency (ms) | 1.60 |

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
| Latency (ms) | 1.39 |

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
| Latency (ms) | 1.51 |

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
| Latency (ms) | 1.78 |

---

### SEMANTIC — What are useful Python tips and tricks I've learned?

- **Benchmark ID:** 108_tp_62f888
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [108, 174, 177, 206, 232, 239, 272, 283]
- **Retrieved Notes:** [318, 206, 633, 357, 464]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.125 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| MAP@5 | 0.062 |
| R-Precision | 0.125 |
| Latency (ms) | 2.12 |

---

### SEMANTIC — Show my Python programming notes

- **Benchmark ID:** 108_tp_89ce75
- **Difficulty:** easy
- **Challenge:** lexical
- **Relevant Notes:** [108, 174, 177, 206, 232, 239, 272, 283]
- **Retrieved Notes:** [87, 799, 583, 699, 899]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 1.99 |

---

### SEMANTIC — How does Python async programming work?

- **Benchmark ID:** 170_tp_39fb15
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [170, 283, 304, 359, 364, 372, 471, 661, 662, 663]
- **Retrieved Notes:** [934, 304, 734, 834, 1034]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.100 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| MAP@5 | 0.050 |
| R-Precision | 0.100 |
| Latency (ms) | 1.75 |

---

### SEMANTIC — What git commands and workflows have I noted?

- **Benchmark ID:** 130_tp_e144a1
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [130, 135, 144, 169, 229, 272, 317, 328, 366, 395]
- **Retrieved Notes:** [612, 328, 501, 614, 522]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.100 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| MAP@5 | 0.050 |
| R-Precision | 0.100 |
| Latency (ms) | 2.16 |

---

### SEMANTIC — Git tips and tricks

- **Benchmark ID:** 130_tp_832398
- **Difficulty:** easy
- **Challenge:** lexical
- **Relevant Notes:** [130, 135, 144, 169, 229, 272, 317, 328, 366, 395]
- **Retrieved Notes:** [646, 719, 819, 497, 919]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 1.66 |

---

### SEMANTIC — What do I know about RAG systems?

- **Benchmark ID:** 65_tp_3e802c
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [65, 114, 186, 197, 219, 222, 267, 296, 310, 376]
- **Retrieved Notes:** [386, 436, 470, 565, 197]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.100 |
| Hit | True |
| Reciprocal Rank | 0.200 |
| MAP@5 | 0.020 |
| R-Precision | 0.100 |
| Latency (ms) | 1.49 |

---

### SEMANTIC — Retrieval augmented generation notes

- **Benchmark ID:** 65_tp_034576
- **Difficulty:** easy
- **Challenge:** lexical
- **Relevant Notes:** [65, 114, 186, 197, 219, 222, 267, 296, 310, 376]
- **Retrieved Notes:** [65, 186, 398, 184, 289]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.200 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.200 |
| R-Precision | 0.200 |
| Latency (ms) | 1.73 |

---

### SEMANTIC — Notes about embeddings and vector search

- **Benchmark ID:** 168_tp_f44ea2
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [168, 183, 228, 289, 298, 323, 376, 486, 487, 523]
- **Retrieved Notes:** [196, 333, 726, 298, 826]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.100 |
| Hit | True |
| Reciprocal Rank | 0.250 |
| MAP@5 | 0.025 |
| R-Precision | 0.100 |
| Latency (ms) | 1.71 |

---

### SEMANTIC — Large language model notes and findings

- **Benchmark ID:** 60_tp_438fb0
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [60, 119, 122, 136, 143, 186, 251, 268, 313, 329]
- **Retrieved Notes:** [186, 404, 808, 708, 908]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.100 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.100 |
| R-Precision | 0.100 |
| Latency (ms) | 2.42 |

---

### SEMANTIC — Notes about reranking in search systems

- **Benchmark ID:** 67_tp_248b82
- **Difficulty:** hard
- **Challenge:** semantic
- **Relevant Notes:** [67, 119, 123, 176, 386, 648, 676, 776, 876, 976]
- **Retrieved Notes:** [67, 176, 119, 305, 58]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.600 |
| Recall@5 | 0.300 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.300 |
| R-Precision | 0.300 |
| Latency (ms) | 2.56 |

---

### SEMANTIC — RAG and retrieval evaluation metrics

- **Benchmark ID:** 90_tp_bed875
- **Difficulty:** hard
- **Challenge:** multi_hop
- **Relevant Notes:** [90, 119, 310, 402, 485, 487, 595]
- **Retrieved Notes:** [386, 485, 310, 595, 186]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.600 |
| Recall@5 | 0.429 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| MAP@5 | 0.274 |
| R-Precision | 0.429 |
| Latency (ms) | 1.41 |

---

### SEMANTIC — How do I measure retrieval quality?

- **Benchmark ID:** 90_tp_c1f487
- **Difficulty:** hard
- **Challenge:** semantic
- **Relevant Notes:** [90, 119, 210, 310, 402, 485, 487, 595]
- **Retrieved Notes:** [310, 86, 485, 402, 213]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.600 |
| Recall@5 | 0.375 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.302 |
| R-Precision | 0.375 |
| Latency (ms) | 1.29 |

---

### SEMANTIC — Prompting techniques and tips

- **Benchmark ID:** 130_tp_d166fd
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [130, 191, 264, 268, 406, 436, 446, 456, 467, 493]
- **Retrieved Notes:** [406, 264, 507, 459, 199]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.200 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.200 |
| R-Precision | 0.200 |
| Latency (ms) | 1.34 |

---

### SEMANTIC — Caching strategies and implementations

- **Benchmark ID:** 103_tp_bee00a
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [103, 124, 146, 237, 269, 275, 284, 295, 318, 336]
- **Retrieved Notes:** [61, 93, 644, 602, 467]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 1.28 |

---

### SEMANTIC — Message queue and event streaming notes

- **Benchmark ID:** 71_tp_b1348d
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [71, 102, 144, 174, 200, 218, 238, 269, 297, 304]
- **Retrieved Notes:** [871, 671, 771, 450, 971]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 1.25 |

---

### SEMANTIC — System design interview prep notes

- **Benchmark ID:** 70_tp_c5e045
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [70, 145, 255, 267, 305, 309, 334, 344, 346, 360]
- **Retrieved Notes:** [360, 70, 106, 309, 99]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.600 |
| Recall@5 | 0.300 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.275 |
| R-Precision | 0.300 |
| Latency (ms) | 1.20 |

---

### SEMANTIC — PostgreSQL database notes

- **Benchmark ID:** 58_tp_257a95
- **Difficulty:** medium
- **Challenge:** lexical
- **Relevant Notes:** [58, 66, 74, 104, 139, 144, 168, 175, 215, 267]
- **Retrieved Notes:** [74, 144, 731, 417, 831]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.200 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.200 |
| R-Precision | 0.200 |
| Latency (ms) | 1.52 |

---

### SEMANTIC — Redis usage and patterns

- **Benchmark ID:** 61_tp_89afdd
- **Difficulty:** easy
- **Challenge:** lexical
- **Relevant Notes:** [61, 73, 92, 103, 124, 146, 157, 174, 237, 246]
- **Retrieved Notes:** [73, 92, 724, 269, 824]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.200 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.200 |
| R-Precision | 0.200 |
| Latency (ms) | 1.66 |

---

### SEMANTIC — Docker and containerization notes

- **Benchmark ID:** 72_tp_c8e7e1
- **Difficulty:** easy
- **Challenge:** lexical
- **Relevant Notes:** [72, 75, 91, 105, 118, 138, 188, 192, 242, 295]
- **Retrieved Notes:** [72, 105, 192, 75, 491]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.800 |
| Recall@5 | 0.400 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.400 |
| R-Precision | 0.400 |
| Latency (ms) | 3.89 |

---

### SEMANTIC — What Docker tips have I collected?

- **Benchmark ID:** 72_tp_808bd0
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [72, 75, 91, 105, 118, 138, 188, 192, 242, 295]
- **Retrieved Notes:** [72, 192, 295, 105, 75]

| Metric | Value |
|-------|------:|
| Precision@5 | 1.000 |
| Recall@5 | 0.500 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.500 |
| R-Precision | 0.500 |
| Latency (ms) | 2.97 |

---

### SEMANTIC — FastAPI development notes

- **Benchmark ID:** 68_tp_d59df1
- **Difficulty:** medium
- **Challenge:** lexical
- **Relevant Notes:** [68, 132, 145, 165, 167, 266, 272, 313, 350, 365]
- **Retrieved Notes:** [68, 825, 165, 725, 925]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.200 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.167 |
| R-Precision | 0.200 |
| Latency (ms) | 2.69 |

---

### SEMANTIC — KnowledgeVault project notes

- **Benchmark ID:** 57_tp_c30342
- **Difficulty:** easy
- **Challenge:** lexical
- **Relevant Notes:** [57, 88, 89, 90, 91, 94, 95, 96, 97, 107]
- **Retrieved Notes:** [125, 95, 96, 89, 90]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.800 |
| Recall@5 | 0.400 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| MAP@5 | 0.272 |
| R-Precision | 0.400 |
| Latency (ms) | 2.13 |

---

### SEMANTIC — What decisions have I made for the KnowledgeVault project?

- **Benchmark ID:** 57_tp_5bc303
- **Difficulty:** medium
- **Challenge:** multi_hop
- **Relevant Notes:** [88, 89, 90, 91, 95, 96, 97]
- **Retrieved Notes:** [638, 90, 728, 428, 828]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.143 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| MAP@5 | 0.071 |
| R-Precision | 0.143 |
| Latency (ms) | 1.84 |

---

### SEMANTIC — What meetings have I had?

- **Benchmark ID:** 56_tp_7b886e
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [56, 106, 107, 149, 170, 233, 251, 283, 304, 359]
- **Retrieved Notes:** [371, 107, 263, 559, 442]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.100 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| MAP@5 | 0.050 |
| R-Precision | 0.100 |
| Latency (ms) | 1.84 |

---

### SEMANTIC — What are my pending tasks and deadlines?

- **Benchmark ID:** 233_tp_b305bf
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [233]
- **Retrieved Notes:** [498, 453, 233, 647, 59]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 1.000 |
| Hit | True |
| Reciprocal Rank | 0.333 |
| MAP@5 | 0.333 |
| R-Precision | 0.000 |
| Latency (ms) | 2.11 |

---

### SEMANTIC — What health appointments do I have?

- **Benchmark ID:** 78_tp_db66ee
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [78, 79, 109, 157, 201, 210, 212, 226, 231, 355]
- **Retrieved Notes:** [79, 601, 559, 575, 198]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.100 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.100 |
| R-Precision | 0.100 |
| Latency (ms) | 2.09 |

---

### SEMANTIC — What payments and bills do I need to make?

- **Benchmark ID:** 77_tp_c2ce55
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [77, 120, 126, 128, 131, 137, 140, 144, 160, 162]
- **Retrieved Notes:** [341, 77, 82, 635, 368]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.100 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| MAP@5 | 0.050 |
| R-Precision | 0.100 |
| Latency (ms) | 1.91 |

---

### SEMANTIC — What is on my shopping list?

- **Benchmark ID:** 76_tp_d5a3f9
- **Difficulty:** easy
- **Challenge:** lexical
- **Relevant Notes:** [76, 322]
- **Retrieved Notes:** [393, 322, 606, 115, 76]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 1.000 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| MAP@5 | 0.450 |
| R-Precision | 0.500 |
| Latency (ms) | 1.76 |

---

### SEMANTIC — Show all my reminders

- **Benchmark ID:** 55_tp_1c812c
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [55, 152, 212, 312, 542, 557]
- **Retrieved Notes:** [382, 56, 312, 290, 442]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.167 |
| Hit | True |
| Reciprocal Rank | 0.333 |
| MAP@5 | 0.056 |
| R-Precision | 0.167 |
| Latency (ms) | 1.49 |

---

### SEMANTIC — My budget and expense tracking notes

- **Benchmark ID:** 82_tp_feed7d
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [82, 153, 202, 210, 216, 254, 281, 291, 331, 345]
- **Retrieved Notes:** [82, 216, 606, 393, 285]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.200 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.200 |
| R-Precision | 0.200 |
| Latency (ms) | 1.73 |

---

### SEMANTIC — My travel plans and notes

- **Benchmark ID:** 81_tp_4afce2
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [81, 115, 126, 128, 130, 171, 175, 176, 178, 186]
- **Retrieved Notes:** [290, 81, 212, 393, 444]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.100 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| MAP@5 | 0.050 |
| R-Precision | 0.100 |
| Latency (ms) | 1.24 |

---

### SEMANTIC — Fitness and workout notes

- **Benchmark ID:** 173_tp_d9566a
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [173, 185, 202, 232, 246, 291, 317, 380, 392, 433]
- **Retrieved Notes:** [631, 481, 87, 482, 83]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 2.14 |

---

### SEMANTIC — My startup ideas and business notes

- **Benchmark ID:** 85_tp_6a3292
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [85, 86, 117, 120, 125, 128, 131, 134, 143, 157]
- **Retrieved Notes:** [85, 525, 459, 617, 441]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.100 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.100 |
| R-Precision | 0.100 |
| Latency (ms) | 1.75 |

---

### SEMANTIC — What business ideas have I documented?

- **Benchmark ID:** 85_tp_aeedec
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [85, 86, 117, 120, 125, 128, 131, 134, 143, 157]
- **Retrieved Notes:** [225, 178, 85, 441, 459]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.100 |
| Hit | True |
| Reciprocal Rank | 0.333 |
| MAP@5 | 0.033 |
| R-Precision | 0.100 |
| Latency (ms) | 3.89 |

---

### SEMANTIC — Things I need to tell Sid

- **Benchmark ID:** 54_tp_6e7d12
- **Difficulty:** easy
- **Challenge:** lexical
- **Relevant Notes:** [54, 55, 56, 57, 117, 187, 203, 220, 225, 247]
- **Retrieved Notes:** [54, 56, 57, 55, 423]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.800 |
| Recall@5 | 0.400 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.400 |
| R-Precision | 0.400 |
| Latency (ms) | 2.26 |

---

### SEMANTIC — Things to discuss with Sid at the next meeting

- **Benchmark ID:** 54_tp_68cb9e
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [54, 55, 56, 57, 117, 187, 203, 220, 225, 247]
- **Retrieved Notes:** [57, 54, 56, 423, 247]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.800 |
| Recall@5 | 0.400 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.380 |
| R-Precision | 0.400 |
| Latency (ms) | 2.11 |

---

### SEMANTIC — Message to send to Siddhant about backend

- **Benchmark ID:** 54_tp_a4d45e
- **Difficulty:** medium
- **Challenge:** lexical_gap
- **Relevant Notes:** [54, 55, 56, 57, 117, 187, 203, 220, 225, 247]
- **Retrieved Notes:** [56, 423, 54, 55, 57]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.800 |
| Recall@5 | 0.400 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.322 |
| R-Precision | 0.400 |
| Latency (ms) | 1.90 |

---

### SEMANTIC — Reciprocal Rank Fusion

- **Benchmark ID:** 518_tp_583ff7
- **Difficulty:** medium
- **Challenge:** exact_phrase
- **Relevant Notes:** [518, 718, 818, 918, 1018]
- **Retrieved Notes:** [918, 518, 818, 718, 1018]

| Metric | Value |
|-------|------:|
| Precision@5 | 1.000 |
| Recall@5 | 1.000 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 1.000 |
| R-Precision | 1.000 |
| Latency (ms) | 2.17 |

---

### SEMANTIC — Redis vs Kafka — when to use each

- **Benchmark ID:** 1024_tp_8759f9
- **Difficulty:** hard
- **Challenge:** comparison
- **Relevant Notes:** [1024, 771, 773, 520]
- **Retrieved Notes:** [873, 673, 643, 773, 973]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.250 |
| Hit | True |
| Reciprocal Rank | 0.250 |
| MAP@5 | 0.062 |
| R-Precision | 0.250 |
| Latency (ms) | 2.04 |

---

### SEMANTIC — Resources for learning backend development

- **Benchmark ID:** 108_tp_d16fba
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [132, 68, 165, 108, 206, 174, 177, 145]
- **Retrieved Notes:** [106, 61, 330, 96, 101]

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

### SEMANTIC — Notes about Fortran programming

- **Benchmark ID:** 0_tp_6cd1aa
- **Difficulty:** hard
- **Challenge:** negative
- **Relevant Notes:** []
- **Retrieved Notes:** [465, 547, 619, 471, 663]

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

### SEMANTIC — My notes on ancient Roman history

- **Benchmark ID:** 0_tp_b73b18
- **Difficulty:** hard
- **Challenge:** negative
- **Relevant Notes:** []
- **Retrieved Notes:** [290, 565, 583, 699, 799]

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

### SEMANTIC — Cooking recipes I've saved

- **Benchmark ID:** 0_tp_fe75c4
- **Difficulty:** hard
- **Challenge:** negative
- **Relevant Notes:** []
- **Retrieved Notes:** [322, 475, 71, 281, 286]

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

### SEMANTIC — KnowledgeVault RAG pipeline decisions and findings

- **Benchmark ID:** 1028_tp_65ec5f
- **Difficulty:** hard
- **Challenge:** multi_hop
- **Relevant Notes:** [1030, 1032, 533]
- **Retrieved Notes:** [310, 90, 446, 730, 830]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 2.82 |

---

### SEMANTIC — What benchmark results have I recorded for KnowledgeVault retrieval?

- **Benchmark ID:** 1028_tp_2e0731
- **Difficulty:** hard
- **Challenge:** multi_hop
- **Relevant Notes:** [1032, 523, 402]
- **Retrieved Notes:** [310, 90, 402, 213, 729]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.333 |
| Hit | True |
| Reciprocal Rank | 0.333 |
| MAP@5 | 0.111 |
| R-Precision | 0.333 |
| Latency (ms) | 2.29 |

---

### SEMANTIC — What have I been working on this month?

- **Benchmark ID:** 77_tp_d33a9c
- **Difficulty:** hard
- **Challenge:** temporal
- **Relevant Notes:** [149]
- **Retrieved Notes:** [453, 77, 82, 647, 375]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 2.08 |

---

### SEMANTIC — Recent notes and activities

- **Benchmark ID:** 77_tp_c2c25c
- **Difficulty:** hard
- **Challenge:** temporal
- **Relevant Notes:** [149, 286]
- **Retrieved Notes:** [87, 444, 565, 290, 203]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 2.60 |

---

### SEMANTIC — My study notes on AI and machine learning

- **Benchmark ID:** 1026_tp_74f5bc
- **Difficulty:** easy
- **Challenge:** synthesis
- **Relevant Notes:** [1026, 774, 1030, 510, 523, 268, 267, 782]
- **Retrieved Notes:** [529, 230, 87, 619, 85]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 2.13 |

---

### SEMANTIC — Messages I need to send Siddhant

- **Benchmark ID:** 54_tp_636e21
- **Difficulty:** easy
- **Challenge:** lexical_gap
- **Relevant Notes:** [54, 55, 56, 57, 117, 187, 203, 220]
- **Retrieved Notes:** [56, 423, 55, 54, 57]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.800 |
| Recall@5 | 0.500 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.402 |
| R-Precision | 0.500 |
| Latency (ms) | 1.94 |

---

### SEMANTIC — Pending conversations with Sid

- **Benchmark ID:** 54_tp_d0b55d
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [54, 55, 56, 57, 117, 187, 203, 220]
- **Retrieved Notes:** [56, 423, 57, 54, 55]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.800 |
| Recall@5 | 0.500 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.402 |
| R-Precision | 0.500 |
| Latency (ms) | 1.91 |

---

### SEMANTIC — Notes about Sid and our project discussions

- **Benchmark ID:** 54_tp_e69fe7
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [54, 55, 56, 57, 117, 187, 203, 220]
- **Retrieved Notes:** [57, 56, 423, 247, 54]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.600 |
| Recall@5 | 0.375 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.325 |
| R-Precision | 0.375 |
| Latency (ms) | 1.83 |

---

### SEMANTIC — Business concepts I want to explore

- **Benchmark ID:** 85_tp_712892
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [85, 86, 117, 131, 134, 143, 157, 166]
- **Retrieved Notes:** [309, 178, 225, 85, 166]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.250 |
| Hit | True |
| Reciprocal Rank | 0.250 |
| MAP@5 | 0.081 |
| R-Precision | 0.250 |
| Latency (ms) | 2.14 |

---

### SEMANTIC — Product ideas I have noted down

- **Benchmark ID:** 85_tp_46bae2
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [85, 86, 117, 131, 134, 143, 157, 166]
- **Retrieved Notes:** [85, 322, 202, 475, 117]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.250 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.175 |
| R-Precision | 0.250 |
| Latency (ms) | 1.95 |

---

### SEMANTIC — Entrepreneurship and venture ideas

- **Benchmark ID:** 85_tp_97280d
- **Difficulty:** medium
- **Challenge:** lexical_gap
- **Relevant Notes:** [85, 86, 117, 131, 134, 143, 157, 166]
- **Retrieved Notes:** [85, 785, 685, 166, 885]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.250 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.188 |
| R-Precision | 0.250 |
| Latency (ms) | 2.01 |

---

### SEMANTIC — Outstanding financial obligations

- **Benchmark ID:** 77_tp_c85047
- **Difficulty:** medium
- **Challenge:** lexical_gap
- **Relevant Notes:** [77, 120, 126, 128, 131, 137, 140, 144]
- **Retrieved Notes:** [82, 341, 411, 210, 635]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 1.80 |

---

### SEMANTIC — Payments I still need to make

- **Benchmark ID:** 77_tp_573aa5
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [77, 120, 126, 128, 131, 137, 140, 144]
- **Retrieved Notes:** [341, 635, 160, 312, 331]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 2.32 |

---

### SEMANTIC — Monthly expenses and dues

- **Benchmark ID:** 77_tp_e477f7
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [77, 120, 126, 128, 131, 137, 140, 144]
- **Retrieved Notes:** [82, 341, 216, 635, 490]

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

### SEMANTIC — Medical appointments on my calendar

- **Benchmark ID:** 78_tp_c31b3d
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [78, 79, 109, 157, 201, 210, 212, 226]
- **Retrieved Notes:** [79, 559, 601, 198, 56]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.125 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.125 |
| R-Precision | 0.125 |
| Latency (ms) | 2.60 |

---

### SEMANTIC — Healthcare and wellness reminders

- **Benchmark ID:** 78_tp_d52f8d
- **Difficulty:** easy
- **Challenge:** lexical_gap
- **Relevant Notes:** [78, 79, 109, 157, 201, 210, 212, 226]
- **Retrieved Notes:** [79, 475, 317, 601, 557]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.125 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.125 |
| R-Precision | 0.125 |
| Latency (ms) | 3.36 |

---

### SEMANTIC — In-memory datastore behavior notes

- **Benchmark ID:** 61_tp_0bc3d9
- **Difficulty:** medium
- **Challenge:** lexical_gap
- **Relevant Notes:** [61, 73, 92, 103, 157, 174, 269, 303]
- **Retrieved Notes:** [906, 706, 275, 806, 1006]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 2.49 |

---

### SEMANTIC — Cache eviction policy details

- **Benchmark ID:** 61_tp_d58d06
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [61, 73, 92, 103, 157, 174, 269, 303]
- **Retrieved Notes:** [103, 520, 318, 467, 534]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.125 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.125 |
| R-Precision | 0.125 |
| Latency (ms) | 2.38 |

---

### SEMANTIC — Team meetings I have attended

- **Benchmark ID:** 56_tp_3888f9
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [56, 106, 107, 149, 170, 233, 251, 283]
- **Retrieved Notes:** [107, 263, 371, 448, 294]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.125 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.125 |
| R-Precision | 0.125 |
| Latency (ms) | 2.32 |

---

### SEMANTIC — Sprint retrospective and planning notes

- **Benchmark ID:** 56_tp_b7d172
- **Difficulty:** easy
- **Challenge:** lexical_gap
- **Relevant Notes:** [56, 106, 107, 149, 170, 233, 251, 283]
- **Retrieved Notes:** [107, 203, 466, 372, 82]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.125 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.125 |
| R-Precision | 0.125 |
| Latency (ms) | 2.51 |

---

### SEMANTIC — Sync notes with the team

- **Benchmark ID:** 56_tp_1162c8
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [56, 106, 107, 149, 170, 233, 251, 283]
- **Retrieved Notes:** [372, 203, 87, 149, 444]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.125 |
| Hit | True |
| Reciprocal Rank | 0.250 |
| MAP@5 | 0.031 |
| R-Precision | 0.125 |
| Latency (ms) | 1.70 |

---

### SEMANTIC — Weekly standup summaries

- **Benchmark ID:** 56_tp_59ba00
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [56, 106, 107, 149, 170, 233, 251, 283]
- **Retrieved Notes:** [107, 87, 453, 565, 438]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.125 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.125 |
| R-Precision | 0.125 |
| Latency (ms) | 1.59 |

---

### SEMANTIC — KnowledgeVault project milestones and deliverables

- **Benchmark ID:** 57_tp_d91b61
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [57, 88, 89, 90, 91, 94, 95, 96]
- **Retrieved Notes:** [125, 90, 638, 95, 88]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.600 |
| Recall@5 | 0.375 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| MAP@5 | 0.200 |
| R-Precision | 0.375 |
| Latency (ms) | 1.79 |

---

### SEMANTIC — What is the architecture of my main project?

- **Benchmark ID:** 57_tp_92649a
- **Difficulty:** hard
- **Challenge:** multi_hop
- **Relevant Notes:** [57, 88, 89, 90, 91, 95, 96]
- **Retrieved Notes:** [106, 95, 392, 102, 602]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.143 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| MAP@5 | 0.071 |
| R-Precision | 0.143 |
| Latency (ms) | 2.24 |

---

### SEMANTIC — Current sprint goals for KnowledgeVault

- **Benchmark ID:** 57_tp_74e120
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [57, 88, 89, 90, 91, 94, 95, 96]
- **Retrieved Notes:** [107, 90, 125, 89, 251]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.250 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| MAP@5 | 0.125 |
| R-Precision | 0.250 |
| Latency (ms) | 2.16 |

---

### SEMANTIC — Capstone project tasks and status

- **Benchmark ID:** 175_tp_9c7eb5
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [175, 190, 199, 225, 233, 263, 285, 382]
- **Retrieved Notes:** [233, 498, 175, 568, 607]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.250 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.208 |
| R-Precision | 0.250 |
| Latency (ms) | 2.48 |

---

### SEMANTIC — University project submission deadlines

- **Benchmark ID:** 175_tp_c51da4
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [175, 190, 199, 225, 233, 263, 285, 382]
- **Retrieved Notes:** [233, 498, 506, 411, 620]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.125 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.125 |
| R-Precision | 0.125 |
| Latency (ms) | 2.70 |

---

### SEMANTIC — My personal reflections and journal entries

- **Benchmark ID:** 113_tp_6bba32
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [113, 149, 152, 162, 166, 191]
- **Retrieved Notes:** [472, 290, 550, 700, 800]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 2.49 |

---

### SEMANTIC — What did I realize recently?

- **Benchmark ID:** 113_tp_ff1a3d
- **Difficulty:** hard
- **Challenge:** semantic
- **Relevant Notes:** [113, 149, 152, 162, 166, 191]
- **Retrieved Notes:** [505, 458, 699, 583, 799]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 3.34 |

---

### SEMANTIC — Insights I've been writing down

- **Benchmark ID:** 113_tp_be2de4
- **Difficulty:** medium
- **Challenge:** lexical_gap
- **Relevant Notes:** [113, 149, 152, 162, 166, 191]
- **Retrieved Notes:** [290, 235, 699, 583, 799]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 2.50 |

---

### SEMANTIC — My career goals and direction notes

- **Benchmark ID:** 56_tp_f28e5b
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [56, 61, 91, 96, 101, 106, 114, 155]
- **Retrieved Notes:** [785, 885, 685, 166, 985]

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

### SEMANTIC — Long-term professional planning notes

- **Benchmark ID:** 56_tp_e42aaa
- **Difficulty:** hard
- **Challenge:** lexical_gap
- **Relevant Notes:** [56, 61, 91, 96, 101, 106, 114, 155]
- **Retrieved Notes:** [107, 617, 212, 87, 601]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 1.51 |

---

### SEMANTIC — Time management and focus techniques

- **Benchmark ID:** 85_tp_c33ed2
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [85, 199, 224, 240, 248, 286, 429, 453]
- **Retrieved Notes:** [240, 248, 565, 521, 224]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.600 |
| Recall@5 | 0.375 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.325 |
| R-Precision | 0.375 |
| Latency (ms) | 1.67 |

---

### SEMANTIC — Notes on staying productive while studying

- **Benchmark ID:** 85_tp_a94724
- **Difficulty:** medium
- **Challenge:** lexical_gap
- **Relevant Notes:** [85, 199, 224, 240, 248, 286, 429, 453]
- **Retrieved Notes:** [240, 380, 680, 780, 880]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.125 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.125 |
| R-Precision | 0.125 |
| Latency (ms) | 1.81 |

---

### SEMANTIC — FastAPI route and dependency injection notes

- **Benchmark ID:** 68_tp_025916
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [68, 120, 132, 145, 153, 165, 167, 169]
- **Retrieved Notes:** [68, 825, 165, 725, 925]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.250 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.208 |
| R-Precision | 0.250 |
| Latency (ms) | 2.89 |

---

### SEMANTIC — Python web framework notes for FastAPI

- **Benchmark ID:** 68_tp_f99196
- **Difficulty:** easy
- **Challenge:** lexical_gap
- **Relevant Notes:** [68, 120, 132, 145, 153, 165, 167, 169]
- **Retrieved Notes:** [763, 863, 663, 471, 963]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 2.06 |

---

### SEMANTIC — API endpoint design patterns in FastAPI

- **Benchmark ID:** 68_tp_9b1c89
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [68, 120, 132, 145, 153, 165, 167, 169]
- **Retrieved Notes:** [68, 825, 725, 165, 925]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.250 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.188 |
| R-Precision | 0.250 |
| Latency (ms) | 1.48 |

---

### SEMANTIC — SQLAlchemy ORM usage patterns

- **Benchmark ID:** 55_tp_fbaf81
- **Difficulty:** medium
- **Challenge:** lexical
- **Relevant Notes:** [55, 58, 69, 85, 98, 123, 129, 132]
- **Retrieved Notes:** [69, 206, 363, 365, 694]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.125 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.125 |
| R-Precision | 0.125 |
| Latency (ms) | 1.38 |

---

### SEMANTIC — Database session management in Python

- **Benchmark ID:** 55_tp_e342eb
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [55, 58, 69, 85, 98, 123, 129, 132]
- **Retrieved Notes:** [894, 694, 365, 794, 994]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 1.84 |

---

### SEMANTIC — How do I fix N+1 query problems?

- **Benchmark ID:** 55_tp_d34490
- **Difficulty:** hard
- **Challenge:** semantic
- **Relevant Notes:** [55, 58, 69, 85, 98, 123, 129, 132]
- **Retrieved Notes:** [859, 589, 759, 659, 959]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 2.09 |

---

### SEMANTIC — pgvector setup and index configuration

- **Benchmark ID:** 66_tp_9be255
- **Difficulty:** hard
- **Challenge:** lexical
- **Relevant Notes:** [66, 168, 215, 298, 323, 337, 367, 500]
- **Retrieved Notes:** [66, 323, 842, 742, 942]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.250 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.250 |
| R-Precision | 0.250 |
| Latency (ms) | 1.95 |

---

### SEMANTIC — Vector similarity search configuration

- **Benchmark ID:** 66_tp_72bd4f
- **Difficulty:** hard
- **Challenge:** semantic
- **Relevant Notes:** [66, 168, 215, 298, 323, 337, 367, 500]
- **Retrieved Notes:** [333, 66, 168, 252, 696]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.250 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| MAP@5 | 0.146 |
| R-Precision | 0.250 |
| Latency (ms) | 2.14 |

---

### SEMANTIC — Algorithm and data structure study notes

- **Benchmark ID:** 59_tp_a4350a
- **Difficulty:** medium
- **Challenge:** lexical
- **Relevant Notes:** [59, 60, 182, 204, 215, 224, 244, 247]
- **Retrieved Notes:** [354, 66, 545, 60, 465]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.125 |
| Hit | True |
| Reciprocal Rank | 0.250 |
| MAP@5 | 0.031 |
| R-Precision | 0.125 |
| Latency (ms) | 1.59 |

---

### SEMANTIC — Competitive programming problem patterns

- **Benchmark ID:** 59_tp_a3126e
- **Difficulty:** hard
- **Challenge:** semantic
- **Relevant Notes:** [59, 60, 182, 204, 215, 224, 244, 247]
- **Retrieved Notes:** [302, 701, 801, 460, 901]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 2.51 |

---

### SEMANTIC — How do I solve graph traversal problems?

- **Benchmark ID:** 59_tp_fe7b32
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [59, 60, 182, 204, 215, 224, 244, 247]
- **Retrieved Notes:** [60, 545, 204, 342, 667]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.250 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.208 |
| R-Precision | 0.250 |
| Latency (ms) | 1.71 |

---

### SEMANTIC — Operating systems exam preparation notes

- **Benchmark ID:** 59_tp_652a70
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [59, 132, 141, 146, 174, 179, 203, 205]
- **Retrieved Notes:** [59, 360, 70, 309, 527]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.125 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.125 |
| R-Precision | 0.125 |
| Latency (ms) | 1.53 |

---

### SEMANTIC — CPU scheduling algorithms I need to know

- **Benchmark ID:** 59_tp_566c28
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [59, 132, 141, 146, 174, 179, 203, 205]
- **Retrieved Notes:** [179, 810, 710, 566, 910]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.125 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.125 |
| R-Precision | 0.125 |
| Latency (ms) | 1.55 |

---

### SEMANTIC — Computer networking concepts for university

- **Benchmark ID:** 75_tp_eae57f
- **Difficulty:** medium
- **Challenge:** lexical
- **Relevant Notes:** [75, 118, 159, 162, 168, 180, 237, 276]
- **Retrieved Notes:** [327, 532, 491, 722, 822]

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

### SEMANTIC — TCP/IP and HTTP protocol notes

- **Benchmark ID:** 75_tp_ac0c4f
- **Difficulty:** easy
- **Challenge:** lexical
- **Relevant Notes:** [75, 118, 159, 162, 168, 180, 237, 276]
- **Retrieved Notes:** [633, 654, 532, 159, 350]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.125 |
| Hit | True |
| Reciprocal Rank | 0.250 |
| MAP@5 | 0.031 |
| R-Precision | 0.125 |
| Latency (ms) | 1.74 |

---

### SEMANTIC — Kubernetes cluster management notes

- **Benchmark ID:** 62_tp_d2020d
- **Difficulty:** medium
- **Challenge:** lexical
- **Relevant Notes:** [62, 118, 181, 230, 383, 410, 419, 548]
- **Retrieved Notes:** [62, 712, 118, 812, 912]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.250 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.208 |
| R-Precision | 0.250 |
| Latency (ms) | 1.52 |

---

### SEMANTIC — Container orchestration with K8s

- **Benchmark ID:** 62_tp_9d6d2c
- **Difficulty:** hard
- **Challenge:** lexical_gap
- **Relevant Notes:** [62, 118, 181, 230, 383, 410, 419, 548]
- **Retrieved Notes:** [62, 383, 75, 118, 712]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.600 |
| Recall@5 | 0.375 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.344 |
| R-Precision | 0.375 |
| Latency (ms) | 1.47 |

---

### SEMANTIC — Authentication and JWT token notes

- **Benchmark ID:** 63_tp_d8d22b
- **Difficulty:** medium
- **Challenge:** lexical
- **Relevant Notes:** [63, 129, 165, 189, 227, 244, 276, 287]
- **Retrieved Notes:** [63, 843, 541, 743, 943]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.125 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.125 |
| R-Precision | 0.125 |
| Latency (ms) | 2.13 |

---

### SEMANTIC — How does OAuth 2.0 work?

- **Benchmark ID:** 63_tp_6690cb
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [63, 129, 165, 189, 227, 244, 276, 287]
- **Retrieved Notes:** [408, 63, 189, 697, 797]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.250 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| MAP@5 | 0.146 |
| R-Precision | 0.250 |
| Latency (ms) | 2.03 |

---

### SEMANTIC — What eviction policies does Redis support?

- **Benchmark ID:** 61_tp_217848
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [61, 73, 92, 103, 124, 146, 157, 169]
- **Retrieved Notes:** [103, 73, 643, 673, 773]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.250 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.250 |
| R-Precision | 0.250 |
| Latency (ms) | 1.95 |

---

### SEMANTIC — What types of indexes does PostgreSQL support?

- **Benchmark ID:** 58_tp_3d1edd
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [58, 66, 74, 104, 113, 114, 136, 139]
- **Retrieved Notes:** [104, 731, 831, 417, 931]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.125 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.125 |
| R-Precision | 0.125 |
| Latency (ms) | 2.07 |

---

### SEMANTIC — When should I use GIN vs B-tree indexes?

- **Benchmark ID:** 58_tp_7b89c1
- **Difficulty:** hard
- **Challenge:** comparison
- **Relevant Notes:** [58, 66, 74, 104, 139]
- **Retrieved Notes:** [886, 139, 786, 686, 986]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.200 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| MAP@5 | 0.100 |
| R-Precision | 0.200 |
| Latency (ms) | 1.93 |

---

### SEMANTIC — How does retrieval augmented generation work?

- **Benchmark ID:** 65_tp_d64f03
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [65, 114, 186, 197, 219, 222, 267, 296]
- **Retrieved Notes:** [65, 184, 186, 398, 119]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.250 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.208 |
| R-Precision | 0.250 |
| Latency (ms) | 3.18 |

---

### SEMANTIC — What are the steps in a RAG pipeline?

- **Benchmark ID:** 65_tp_0a59fb
- **Difficulty:** hard
- **Challenge:** semantic
- **Relevant Notes:** [65, 114, 186, 197, 219, 222, 267, 296]
- **Retrieved Notes:** [930, 830, 730, 446, 1030]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 2.01 |

---

### SEMANTIC — How are text embeddings generated?

- **Benchmark ID:** 168_tp_cc9fa1
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [168, 183, 228, 289, 298, 323, 376, 486]
- **Retrieved Notes:** [926, 298, 726, 826, 1026]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.125 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| MAP@5 | 0.062 |
| R-Precision | 0.125 |
| Latency (ms) | 2.86 |

---

### SEMANTIC — What is the difference between semantic and keyword search?

- **Benchmark ID:** 168_tp_df38ac
- **Difficulty:** hard
- **Challenge:** semantic
- **Relevant Notes:** [168, 183, 228, 289, 298, 323, 376, 486]
- **Retrieved Notes:** [86, 89, 696, 252, 796]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 2.32 |

---

### SEMANTIC — What is due this week?

- **Benchmark ID:** 184_tp_c5a4df
- **Difficulty:** medium
- **Challenge:** temporal
- **Relevant Notes:** [233, 368, 498]
- **Retrieved Notes:** [77, 341, 423, 453, 393]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 3.08 |

---

### SEMANTIC — Upcoming deadlines and submission dates

- **Benchmark ID:** 184_tp_cf679c
- **Difficulty:** medium
- **Challenge:** temporal
- **Relevant Notes:** [233, 368, 498]
- **Retrieved Notes:** [233, 498, 506, 411, 607]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.667 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.667 |
| R-Precision | 0.667 |
| Latency (ms) | 1.68 |

---

### SEMANTIC — Tasks I need to complete before month end

- **Benchmark ID:** 184_tp_96ea32
- **Difficulty:** hard
- **Challenge:** temporal
- **Relevant Notes:** [233, 368, 498]
- **Retrieved Notes:** [79, 82, 601, 453, 498]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.333 |
| Hit | True |
| Reciprocal Rank | 0.200 |
| MAP@5 | 0.067 |
| R-Precision | 0.000 |
| Latency (ms) | 1.46 |

---

### SEMANTIC — What appointments have I booked this month?

- **Benchmark ID:** 78_tp_63adc1
- **Difficulty:** medium
- **Challenge:** temporal
- **Relevant Notes:** [78, 559]
- **Retrieved Notes:** [559, 79, 620, 601, 198]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.500 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.500 |
| R-Precision | 0.500 |
| Latency (ms) | 1.35 |

---

### SEMANTIC — My upcoming travel and trip bookings

- **Benchmark ID:** 78_tp_a0f1d8
- **Difficulty:** easy
- **Challenge:** temporal
- **Relevant Notes:** [78, 81, 115]
- **Retrieved Notes:** [538, 627, 81, 539, 407]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.333 |
| Hit | True |
| Reciprocal Rank | 0.333 |
| MAP@5 | 0.111 |
| R-Precision | 0.333 |
| Latency (ms) | 2.04 |

---

### SEMANTIC — Transport and accommodation I need to arrange

- **Benchmark ID:** 78_tp_219ffa
- **Difficulty:** medium
- **Challenge:** lexical_gap
- **Relevant Notes:** [78, 81, 115, 126, 128, 130, 160, 171]
- **Retrieved Notes:** [577, 538, 115, 128, 407]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.250 |
| Hit | True |
| Reciprocal Rank | 0.333 |
| MAP@5 | 0.104 |
| R-Precision | 0.250 |
| Latency (ms) | 2.08 |

---

### SEMANTIC — Redis vs PostgreSQL — when to use each for persistence?

- **Benchmark ID:** 103_tp_7520ad
- **Difficulty:** hard
- **Challenge:** comparison
- **Relevant Notes:** [103, 104, 73, 74, 58, 92, 61]
- **Retrieved Notes:** [73, 61, 269, 724, 824]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.286 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.286 |
| R-Precision | 0.286 |
| Latency (ms) | 2.30 |

---

### SEMANTIC — Docker vs Kubernetes — what is the difference?

- **Benchmark ID:** 72_tp_807260
- **Difficulty:** hard
- **Challenge:** comparison
- **Relevant Notes:** [118, 62, 383]
- **Retrieved Notes:** [912, 712, 118, 812, 1012]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.333 |
| Hit | True |
| Reciprocal Rank | 0.333 |
| MAP@5 | 0.111 |
| R-Precision | 0.333 |
| Latency (ms) | 2.64 |

---

### SEMANTIC — How do I decide between hybrid retrieval and cross-encoder reranking?

- **Benchmark ID:** 65_tp_205f1c
- **Difficulty:** hard
- **Challenge:** multi_hop
- **Relevant Notes:** [67, 176, 119, 88, 123]
- **Retrieved Notes:** [67, 776, 123, 676, 876]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.400 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.333 |
| R-Precision | 0.400 |
| Latency (ms) | 1.60 |

---

### SEMANTIC — What have I documented about retrieval quality in KnowledgeVault?

- **Benchmark ID:** 89_tp_0f29db
- **Difficulty:** hard
- **Challenge:** multi_hop
- **Relevant Notes:** [89, 485, 487, 402, 595, 88, 90]
- **Retrieved Notes:** [90, 310, 88, 555, 86]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.286 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.238 |
| R-Precision | 0.286 |
| Latency (ms) | 2.09 |

---

### SEMANTIC — All my university and course study notes

- **Benchmark ID:** 58_tp_32b5cf
- **Difficulty:** easy
- **Challenge:** synthesis
- **Relevant Notes:** [58, 61, 62, 66, 69, 122, 130, 131]
- **Retrieved Notes:** [444, 290, 699, 583, 799]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 1.28 |

---

### SEMANTIC — All my brainstorming and ideation notes

- **Benchmark ID:** 85_tp_f46697
- **Difficulty:** easy
- **Challenge:** synthesis
- **Relevant Notes:** [85, 86, 117, 143, 157, 178, 225, 240]
- **Retrieved Notes:** [85, 459, 87, 416, 617]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.125 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.125 |
| R-Precision | 0.125 |
| Latency (ms) | 1.12 |

---

### SEMANTIC — My technical reference cheat sheets

- **Benchmark ID:** 72_tp_32bacd
- **Difficulty:** easy
- **Challenge:** synthesis
- **Relevant Notes:** [72, 73, 74, 75, 122, 135]
- **Retrieved Notes:** [309, 74, 485, 110, 235]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.167 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| MAP@5 | 0.083 |
| R-Precision | 0.167 |
| Latency (ms) | 1.46 |

---

### SEMANTIC — All my communication and message drafts

- **Benchmark ID:** 54_tp_b42b02
- **Difficulty:** easy
- **Challenge:** synthesis
- **Relevant Notes:** [54, 56, 57, 106, 132, 141]
- **Retrieved Notes:** [371, 141, 56, 582, 290]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.333 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| MAP@5 | 0.194 |
| R-Precision | 0.333 |
| Latency (ms) | 1.32 |

---

### SEMANTIC — Errands I need to run today

- **Benchmark ID:** 76_tp_c52e4b
- **Difficulty:** medium
- **Challenge:** lexical_gap
- **Relevant Notes:** [76, 164, 190, 202, 286, 309, 322, 475]
- **Retrieved Notes:** [475, 79, 735, 375, 835]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.125 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.125 |
| R-Precision | 0.125 |
| Latency (ms) | 1.98 |

---

### SEMANTIC — Things I need to pick up from the store

- **Benchmark ID:** 76_tp_c74a5f
- **Difficulty:** easy
- **Challenge:** lexical_gap
- **Relevant Notes:** [76, 164, 190, 202, 286, 309, 322, 475]
- **Retrieved Notes:** [76, 322, 475, 393, 182]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.600 |
| Recall@5 | 0.375 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.375 |
| R-Precision | 0.375 |
| Latency (ms) | 1.96 |

---

### SEMANTIC — Physical training and exercise plan

- **Benchmark ID:** 173_tp_f41c30
- **Difficulty:** easy
- **Challenge:** lexical_gap
- **Relevant Notes:** [173, 202, 291, 317, 380, 621, 631, 680]
- **Retrieved Notes:** [83, 631, 481, 437, 621]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.250 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| MAP@5 | 0.113 |
| R-Precision | 0.250 |
| Latency (ms) | 1.52 |

---

### SEMANTIC — How am I planning to stay healthy?

- **Benchmark ID:** 173_tp_7bafaa
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [173, 202, 291, 317, 380, 621, 631, 680]
- **Retrieved Notes:** [83, 212, 79, 84, 286]

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

### SEMANTIC — How much am I spending per month?

- **Benchmark ID:** 82_tp_86df0e
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [82, 210, 216, 281, 331, 345, 407, 535]
- **Retrieved Notes:** [216, 82, 331, 281, 490]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.800 |
| Recall@5 | 0.500 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.500 |
| R-Precision | 0.500 |
| Latency (ms) | 1.40 |

---

### SEMANTIC — Personal finance tracking notes

- **Benchmark ID:** 82_tp_3665b0
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [82, 210, 216, 281, 331, 345, 407, 535]
- **Retrieved Notes:** [87, 82, 216, 285, 393]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.250 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| MAP@5 | 0.146 |
| R-Precision | 0.250 |
| Latency (ms) | 1.75 |

---

### SEMANTIC — BRPOPLPUSH reliable queue implementation

- **Benchmark ID:** 246_tp_6ef122
- **Difficulty:** hard
- **Challenge:** exact_phrase
- **Relevant Notes:** [246, 433, 643, 673, 684, 705, 773, 784]
- **Retrieved Notes:** [773, 873, 673, 643, 973]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.600 |
| Recall@5 | 0.375 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.302 |
| R-Precision | 0.375 |
| Latency (ms) | 1.96 |

---

### SEMANTIC — ACID properties of databases

- **Benchmark ID:** 229_tp_454ff2
- **Difficulty:** easy
- **Challenge:** exact_phrase
- **Relevant Notes:** [229, 690, 790, 890, 990, 1090]
- **Retrieved Notes:** [790, 890, 229, 690, 990]

| Metric | Value |
|-------|------:|
| Precision@5 | 1.000 |
| Recall@5 | 0.833 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.833 |
| R-Precision | 0.833 |
| Latency (ms) | 1.73 |

---

### SEMANTIC — RRF score combination for hybrid search

- **Benchmark ID:** 518_tp_930ea0
- **Difficulty:** hard
- **Challenge:** exact_phrase
- **Relevant Notes:** [518, 718, 818, 918, 1018]
- **Retrieved Notes:** [918, 718, 818, 518, 1018]

| Metric | Value |
|-------|------:|
| Precision@5 | 1.000 |
| Recall@5 | 1.000 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 1.000 |
| R-Precision | 1.000 |
| Latency (ms) | 1.93 |

---

### SEMANTIC — HNSW approximate nearest neighbor algorithm

- **Benchmark ID:** 215_tp_55df73
- **Difficulty:** hard
- **Challenge:** exact_phrase
- **Relevant Notes:** [215, 430, 681, 781, 881, 981, 1081]
- **Retrieved Notes:** [781, 881, 681, 215, 981]

| Metric | Value |
|-------|------:|
| Precision@5 | 1.000 |
| Recall@5 | 0.714 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.714 |
| R-Precision | 0.714 |
| Latency (ms) | 2.86 |

---

### SEMANTIC — What do I need to buy this weekend?

- **Benchmark ID:** 76_tp_5c724a
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [76, 164, 190, 202, 309, 322, 393, 475]
- **Retrieved Notes:** [77, 76, 322, 393, 286]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.600 |
| Recall@5 | 0.375 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| MAP@5 | 0.240 |
| R-Precision | 0.375 |
| Latency (ms) | 2.54 |

---

### SEMANTIC — All my pending reminders and follow-ups

- **Benchmark ID:** 55_tp_3ff20c
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [55, 152, 212, 312, 542, 557]
- **Retrieved Notes:** [79, 191, 392, 372, 312]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.167 |
| Hit | True |
| Reciprocal Rank | 0.200 |
| MAP@5 | 0.033 |
| R-Precision | 0.167 |
| Latency (ms) | 1.41 |

---

### SEMANTIC — What have I told myself not to forget?

- **Benchmark ID:** 55_tp_05e927
- **Difficulty:** medium
- **Challenge:** lexical_gap
- **Relevant Notes:** [55, 152, 212, 312, 542, 557]
- **Retrieved Notes:** [212, 647, 475, 290, 505]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.167 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.167 |
| R-Precision | 0.167 |
| Latency (ms) | 1.37 |

---

### SEMANTIC — LeetCode patterns and problem-solving techniques

- **Benchmark ID:** 117_tp_44e6df
- **Difficulty:** medium
- **Challenge:** lexical
- **Relevant Notes:** [117, 127, 187, 224, 271, 279, 282, 316]
- **Retrieved Notes:** [224, 611, 316, 187, 546]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.600 |
| Recall@5 | 0.375 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.302 |
| R-Precision | 0.375 |
| Latency (ms) | 1.32 |

---

### SEMANTIC — How do I approach dynamic programming questions?

- **Benchmark ID:** 117_tp_7bf7d7
- **Difficulty:** hard
- **Challenge:** semantic
- **Relevant Notes:** [117, 127, 187, 224, 271, 279, 282, 316]
- **Retrieved Notes:** [562, 459, 117, 352, 302]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.125 |
| Hit | True |
| Reciprocal Rank | 0.333 |
| MAP@5 | 0.042 |
| R-Precision | 0.125 |
| Latency (ms) | 1.23 |

---

### SEMANTIC — System design concepts I need to review

- **Benchmark ID:** 70_tp_39b780
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [70, 145, 267, 305, 309, 334, 344, 346]
- **Retrieved Notes:** [392, 70, 360, 309, 99]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.250 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| MAP@5 | 0.125 |
| R-Precision | 0.250 |
| Latency (ms) | 1.84 |

---

### SEMANTIC — How do I design a scalable URL shortener?

- **Benchmark ID:** 70_tp_c6f60d
- **Difficulty:** hard
- **Challenge:** semantic
- **Relevant Notes:** [70, 145, 267, 305, 309, 334, 344, 346]
- **Retrieved Notes:** [602, 93, 346, 386, 644]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.125 |
| Hit | True |
| Reciprocal Rank | 0.333 |
| MAP@5 | 0.042 |
| R-Precision | 0.125 |
| Latency (ms) | 1.59 |

---

### SEMANTIC — Behavioral interview story preparation

- **Benchmark ID:** 83_tp_a140c7
- **Difficulty:** medium
- **Challenge:** lexical
- **Relevant Notes:** [83, 85, 113, 114, 116, 131, 134, 135]
- **Retrieved Notes:** [468, 294, 360, 344, 263]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 2.28 |

---

### SEMANTIC — Resume writing tips and improvement notes

- **Benchmark ID:** 100_tp_b51d58
- **Difficulty:** easy
- **Challenge:** lexical
- **Relevant Notes:** [100, 142, 185, 270, 523, 525]
- **Retrieved Notes:** [142, 100, 185, 415, 87]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.600 |
| Recall@5 | 0.500 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.500 |
| R-Precision | 0.500 |
| Latency (ms) | 1.94 |

---

### SEMANTIC — How should I write my software engineer resume?

- **Benchmark ID:** 100_tp_fcae97
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [100, 142, 185, 270, 523, 525]
- **Retrieved Notes:** [100, 142, 525, 185, 330]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.800 |
| Recall@5 | 0.667 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.667 |
| R-Precision | 0.667 |
| Latency (ms) | 2.33 |

---

### SEMANTIC — Books I am reading or have read recently

- **Benchmark ID:** 78_tp_c601ae
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [78, 128, 155, 160, 172, 182, 194, 234]
- **Retrieved Notes:** [240, 528, 290, 309, 565]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 2.30 |

---

### SEMANTIC — Reading list and book notes

- **Benchmark ID:** 78_tp_0f3259
- **Difficulty:** easy
- **Challenge:** lexical
- **Relevant Notes:** [78, 128, 155, 160, 172, 182, 194, 234]
- **Retrieved Notes:** [87, 444, 235, 290, 203]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 3.00 |

---

### SEMANTIC — Habit formation notes from Atomic Habits

- **Benchmark ID:** 304_tp_4994bc
- **Difficulty:** easy
- **Challenge:** lexical
- **Relevant Notes:** [304, 317, 482, 557, 631, 634, 698, 734]
- **Retrieved Notes:** [482, 73, 557, 318, 116]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.250 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.208 |
| R-Precision | 0.250 |
| Latency (ms) | 1.86 |

---

### SEMANTIC — Summary of James Clear's key ideas on habits

- **Benchmark ID:** 304_tp_37657b
- **Difficulty:** medium
- **Challenge:** lexical_gap
- **Relevant Notes:** [304, 317, 482, 557, 631, 634, 698, 734]
- **Retrieved Notes:** [482, 240, 496, 309, 235]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.125 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.125 |
| R-Precision | 0.125 |
| Latency (ms) | 1.69 |

---

### SEMANTIC — Online courses and tutorials I am taking

- **Benchmark ID:** 71_tp_43e20b
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [71, 145, 231, 266, 357, 394, 417, 471]
- **Retrieved Notes:** [863, 763, 471, 663, 963]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.125 |
| Hit | True |
| Reciprocal Rank | 0.333 |
| MAP@5 | 0.042 |
| R-Precision | 0.125 |
| Latency (ms) | 1.57 |

---

### SEMANTIC — Sleep improvement techniques and tips

- **Benchmark ID:** 133_tp_12eb56
- **Difficulty:** medium
- **Challenge:** lexical
- **Relevant Notes:** [133, 136, 202, 288, 348, 380, 434, 538]
- **Retrieved Notes:** [622, 434, 574, 317, 548]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.125 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| MAP@5 | 0.062 |
| R-Precision | 0.125 |
| Latency (ms) | 2.02 |

---

### SEMANTIC — How can I improve my sleep quality?

- **Benchmark ID:** 133_tp_2c6b3e
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [133, 136, 202, 288, 348, 380, 434, 538]
- **Retrieved Notes:** [434, 622, 574, 548, 317]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.125 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.125 |
| R-Precision | 0.125 |
| Latency (ms) | 2.36 |

---

### SEMANTIC — Nutrition and supplement tracking notes

- **Benchmark ID:** 109_tp_f852f9
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [109, 133, 226, 286]
- **Retrieved Notes:** [286, 133, 322, 285, 216]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.500 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.500 |
| R-Precision | 0.500 |
| Latency (ms) | 1.90 |

---

### SEMANTIC — What supplements should I be taking?

- **Benchmark ID:** 109_tp_f444c2
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [109, 133, 226, 286]
- **Retrieved Notes:** [133, 286, 226, 109, 84]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.800 |
| Recall@5 | 1.000 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 1.000 |
| R-Precision | 1.000 |
| Latency (ms) | 1.53 |

---

### SEMANTIC — Mental health practices and coping strategies

- **Benchmark ID:** 152_tp_3685ae
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [152, 288, 317, 472, 575]
- **Retrieved Notes:** [288, 575, 212, 472, 201]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.600 |
| Recall@5 | 0.600 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.550 |
| R-Precision | 0.600 |
| Latency (ms) | 1.92 |

---

### SEMANTIC — My notes on managing stress and anxiety

- **Benchmark ID:** 152_tp_5aba2a
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [152, 288, 317, 472, 575]
- **Retrieved Notes:** [288, 472, 212, 356, 539]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.400 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.400 |
| R-Precision | 0.400 |
| Latency (ms) | 3.51 |

---

### SEMANTIC — Plans for open source and public building

- **Benchmark ID:** 117_tp_eab7a3
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [117, 141, 395, 400, 440, 453, 522, 554]
- **Retrieved Notes:** [255, 141, 554, 117, 106]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.600 |
| Recall@5 | 0.375 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| MAP@5 | 0.240 |
| R-Precision | 0.375 |
| Latency (ms) | 2.03 |

---

### SEMANTIC — Notes on growing my developer presence online

- **Benchmark ID:** 117_tp_594cbf
- **Difficulty:** medium
- **Challenge:** lexical_gap
- **Relevant Notes:** [117, 141, 395, 400, 440, 453, 522, 554]
- **Retrieved Notes:** [255, 330, 141, 155, 555]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.125 |
| Hit | True |
| Reciprocal Rank | 0.333 |
| MAP@5 | 0.042 |
| R-Precision | 0.125 |
| Latency (ms) | 2.41 |

---

### SEMANTIC — Fortran programming and legacy code notes

- **Benchmark ID:** 0_tp_07253f
- **Difficulty:** hard
- **Challenge:** negative
- **Relevant Notes:** []
- **Retrieved Notes:** [465, 547, 227, 169, 389]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 2.27 |

---

### SEMANTIC — Ancient history and archaeology notes

- **Benchmark ID:** 0_tp_13e990
- **Difficulty:** hard
- **Challenge:** negative
- **Relevant Notes:** []
- **Retrieved Notes:** [565, 290, 372, 386, 619]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 2.36 |

---

### SEMANTIC — Wine and cheese pairing recommendations

- **Benchmark ID:** 0_tp_f9589c
- **Difficulty:** hard
- **Challenge:** negative
- **Relevant Notes:** []
- **Retrieved Notes:** [81, 363, 69, 639, 139]

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

### SEMANTIC — Piano lessons and music theory notes

- **Benchmark ID:** 0_tp_5abfd7
- **Difficulty:** hard
- **Challenge:** negative
- **Relevant Notes:** []
- **Retrieved Notes:** [444, 290, 87, 637, 733]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 2.33 |

---

### SEMANTIC — Gardening and plant care notes

- **Benchmark ID:** 0_tp_4fb99e
- **Difficulty:** hard
- **Challenge:** negative
- **Relevant Notes:** []
- **Retrieved Notes:** [899, 583, 799, 699, 999]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 2.19 |

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
| Latency (ms) | 404.16 |
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
| Latency (ms) | 73.37 |
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
| Latency (ms) | 37.12 |
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
| Latency (ms) | 36.72 |
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
| Latency (ms) | 38.79 |
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
| Latency (ms) | 32.05 |
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
| Latency (ms) | 37.40 |
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
| Latency (ms) | 34.71 |
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
| Latency (ms) | 38.99 |
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
| Latency (ms) | 37.70 |
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
| Latency (ms) | 38.99 |
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
| Latency (ms) | 39.01 |
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
| Latency (ms) | 40.10 |
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
| Latency (ms) | 37.24 |
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
| Latency (ms) | 49.20 |
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
| Latency (ms) | 56.04 |
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
| Latency (ms) | 44.17 |
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
| Latency (ms) | 44.36 |
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
| Latency (ms) | 44.94 |
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
| Latency (ms) | 42.95 |
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
| Latency (ms) | 36.73 |
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
| Latency (ms) | 50.12 |
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
| Latency (ms) | 32.72 |
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
| Latency (ms) | 39.82 |
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
| Latency (ms) | 30.69 |
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
| Latency (ms) | 29.77 |
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
| Latency (ms) | 33.92 |
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
| Latency (ms) | 42.25 |
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
| Latency (ms) | 35.35 |
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
| Latency (ms) | 27.52 |
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
| Latency (ms) | 28.80 |
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
| Latency (ms) | 36.02 |
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
| Latency (ms) | 36.84 |
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
| Latency (ms) | 40.68 |
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
| Latency (ms) | 44.60 |
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
| Latency (ms) | 54.15 |
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
| Latency (ms) | 47.78 |
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
| Latency (ms) | 35.37 |
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
| Latency (ms) | 36.73 |
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
| Latency (ms) | 45.57 |
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
| Latency (ms) | 56.43 |
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
| Latency (ms) | 45.23 |
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
| Latency (ms) | 49.17 |
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
| Latency (ms) | 42.00 |
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
| Latency (ms) | 43.52 |
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
| Latency (ms) | 38.57 |
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
| Latency (ms) | 30.62 |
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
| Latency (ms) | 40.10 |
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
| Latency (ms) | 41.81 |
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
| Latency (ms) | 33.43 |
| Predicted Intent | question |
| Expected Intent | question |
| Intent Correct | True |

---

### INTENT — What are useful Python tips and tricks I've learned?

- **Benchmark ID:** 108_tp_62f888
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [108, 174, 177, 206, 232, 239, 272, 283]
- **Retrieved Notes:** [1045, 1036, 945, 936, 845]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 38.62 |
| Predicted Intent | question |
| Expected Intent | study |
| Intent Correct | False |
| Predicted Category | Questions - Python |
| Expected Category | Study - Python |
| Category Correct | False |

---

### INTENT — Show my Python programming notes

- **Benchmark ID:** 108_tp_89ce75
- **Difficulty:** easy
- **Challenge:** lexical
- **Relevant Notes:** [108, 174, 177, 206, 232, 239, 272, 283]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 23.85 |
| Predicted Intent | reference |
| Expected Intent | study |
| Intent Correct | False |

---

### INTENT — How does Python async programming work?

- **Benchmark ID:** 170_tp_39fb15
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [170, 283, 304, 359, 364, 372, 471, 661, 662, 663]
- **Retrieved Notes:** [1045, 1036, 945, 936, 845]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 35.99 |
| Predicted Intent | question |
| Expected Intent | study |
| Intent Correct | False |
| Predicted Category | Questions - Python |
| Expected Category | Study - Python |
| Category Correct | False |

---

### INTENT — What git commands and workflows have I noted?

- **Benchmark ID:** 130_tp_e144a1
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [130, 135, 144, 169, 229, 272, 317, 328, 366, 395]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 35.24 |
| Predicted Intent | question |
| Expected Intent | reference |
| Intent Correct | False |

---

### INTENT — Git tips and tricks

- **Benchmark ID:** 130_tp_832398
- **Difficulty:** easy
- **Challenge:** lexical
- **Relevant Notes:** [130, 135, 144, 169, 229, 272, 317, 328, 366, 395]
- **Retrieved Notes:** [1093, 1078, 1077, 1067, 1059]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 39.37 |
| Predicted Intent | general |
| Expected Intent | reference |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Reference - Git |
| Category Correct | False |

---

### INTENT — What do I know about RAG systems?

- **Benchmark ID:** 65_tp_3e802c
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [65, 114, 186, 197, 219, 222, 267, 296, 310, 376]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 41.94 |
| Predicted Intent | question |
| Expected Intent | study |
| Intent Correct | False |

---

### INTENT — Retrieval augmented generation notes

- **Benchmark ID:** 65_tp_034576
- **Difficulty:** easy
- **Challenge:** lexical
- **Relevant Notes:** [65, 114, 186, 197, 219, 222, 267, 296, 310, 376]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 66.68 |
| Predicted Intent | reference |
| Expected Intent | study |
| Intent Correct | False |

---

### INTENT — Notes about embeddings and vector search

- **Benchmark ID:** 168_tp_f44ea2
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [168, 183, 228, 289, 298, 323, 376, 486, 487, 523]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 50.27 |
| Predicted Intent | reference |
| Expected Intent | study |
| Intent Correct | False |

---

### INTENT — Large language model notes and findings

- **Benchmark ID:** 60_tp_438fb0
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [60, 119, 122, 136, 143, 186, 251, 268, 313, 329]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 65.91 |
| Predicted Intent | reference |
| Expected Intent | study |
| Intent Correct | False |

---

### INTENT — Notes about reranking in search systems

- **Benchmark ID:** 67_tp_248b82
- **Difficulty:** hard
- **Challenge:** semantic
- **Relevant Notes:** [67, 119, 123, 176, 386, 648, 676, 776, 876, 976]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 54.33 |
| Predicted Intent | reference |
| Expected Intent | study |
| Intent Correct | False |

---

### INTENT — RAG and retrieval evaluation metrics

- **Benchmark ID:** 90_tp_bed875
- **Difficulty:** hard
- **Challenge:** multi_hop
- **Relevant Notes:** [90, 119, 310, 402, 485, 487, 595]
- **Retrieved Notes:** [1093, 1078, 1077, 1067, 1059]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 70.77 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Study - AI |
| Category Correct | False |

---

### INTENT — How do I measure retrieval quality?

- **Benchmark ID:** 90_tp_c1f487
- **Difficulty:** hard
- **Challenge:** semantic
- **Relevant Notes:** [90, 119, 210, 310, 402, 485, 487, 595]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 52.08 |
| Predicted Intent | question |
| Expected Intent | study |
| Intent Correct | False |

---

### INTENT — Prompting techniques and tips

- **Benchmark ID:** 130_tp_d166fd
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [130, 191, 264, 268, 406, 436, 446, 456, 467, 493]
- **Retrieved Notes:** [1093, 1078, 1077, 1067, 1059]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 51.92 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Study - AI |
| Category Correct | False |

---

### INTENT — Caching strategies and implementations

- **Benchmark ID:** 103_tp_bee00a
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [103, 124, 146, 237, 269, 275, 284, 295, 318, 336]
- **Retrieved Notes:** [1093, 1078, 1077, 1067, 1059]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 40.77 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Study - System Design |
| Category Correct | False |

---

### INTENT — Message queue and event streaming notes

- **Benchmark ID:** 71_tp_b1348d
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [71, 102, 144, 174, 200, 218, 238, 269, 297, 304]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 41.36 |
| Predicted Intent | communication |
| Expected Intent | study |
| Intent Correct | False |

---

### INTENT — System design interview prep notes

- **Benchmark ID:** 70_tp_c5e045
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [70, 145, 255, 267, 305, 309, 334, 344, 346, 360]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 36.75 |
| Predicted Intent | reference |
| Expected Intent | study |
| Intent Correct | False |

---

### INTENT — PostgreSQL database notes

- **Benchmark ID:** 58_tp_257a95
- **Difficulty:** medium
- **Challenge:** lexical
- **Relevant Notes:** [58, 66, 74, 104, 139, 144, 168, 175, 215, 267]
- **Retrieved Notes:** [74]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.100 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.100 |
| R-Precision | 0.100 |
| Latency (ms) | 40.92 |
| Predicted Intent | reference |
| Expected Intent | study |
| Intent Correct | False |
| Predicted Category | Reference - PostgreSQL |
| Expected Category | Study - PostgreSQL |
| Category Correct | False |

---

### INTENT — Redis usage and patterns

- **Benchmark ID:** 61_tp_89afdd
- **Difficulty:** easy
- **Challenge:** lexical
- **Relevant Notes:** [61, 73, 92, 103, 124, 146, 157, 174, 237, 246]
- **Retrieved Notes:** [1093, 1078, 1077, 1067, 1059]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 47.10 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Study - Redis |
| Category Correct | False |

---

### INTENT — Docker and containerization notes

- **Benchmark ID:** 72_tp_c8e7e1
- **Difficulty:** easy
- **Challenge:** lexical
- **Relevant Notes:** [72, 75, 91, 105, 118, 138, 188, 192, 242, 295]
- **Retrieved Notes:** [75, 72]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.200 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.200 |
| R-Precision | 0.200 |
| Latency (ms) | 36.51 |
| Predicted Intent | reference |
| Expected Intent | study |
| Intent Correct | False |
| Predicted Category | Reference - Docker |
| Expected Category | Study - Docker |
| Category Correct | False |

---

### INTENT — What Docker tips have I collected?

- **Benchmark ID:** 72_tp_808bd0
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [72, 75, 91, 105, 118, 138, 188, 192, 242, 295]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 30.03 |
| Predicted Intent | question |
| Expected Intent | reference |
| Intent Correct | False |

---

### INTENT — FastAPI development notes

- **Benchmark ID:** 68_tp_d59df1
- **Difficulty:** medium
- **Challenge:** lexical
- **Relevant Notes:** [68, 132, 145, 165, 167, 266, 272, 313, 350, 365]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 36.73 |
| Predicted Intent | reference |
| Expected Intent | study |
| Intent Correct | False |

---

### INTENT — KnowledgeVault project notes

- **Benchmark ID:** 57_tp_c30342
- **Difficulty:** easy
- **Challenge:** lexical
- **Relevant Notes:** [57, 88, 89, 90, 91, 94, 95, 96, 97, 107]
- **Retrieved Notes:** [125, 96]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.100 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| MAP@5 | 0.050 |
| R-Precision | 0.100 |
| Latency (ms) | 42.04 |
| Predicted Intent | reference |
| Expected Intent | reference |
| Intent Correct | True |
| Predicted Category | Reference - Shared |
| Expected Category | Reference - KnowledgeVault |
| Category Correct | True |

---

### INTENT — What decisions have I made for the KnowledgeVault project?

- **Benchmark ID:** 57_tp_5bc303
- **Difficulty:** medium
- **Challenge:** multi_hop
- **Relevant Notes:** [88, 89, 90, 91, 95, 96, 97]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 29.07 |
| Predicted Intent | question |
| Expected Intent | reference |
| Intent Correct | False |

---

### INTENT — What meetings have I had?

- **Benchmark ID:** 56_tp_7b886e
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [56, 106, 107, 149, 170, 233, 251, 283, 304, 359]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 33.43 |
| Predicted Intent | event |
| Expected Intent | event |
| Intent Correct | True |

---

### INTENT — What are my pending tasks and deadlines?

- **Benchmark ID:** 233_tp_b305bf
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [233]
- **Retrieved Notes:** [1102, 1098, 1096, 1092, 1086]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 100.91 |
| Predicted Intent | todo |
| Expected Intent | todo |
| Intent Correct | True |
| Predicted Category | Tasks |
| Expected Category | Tasks |
| Category Correct | True |

---

### INTENT — What health appointments do I have?

- **Benchmark ID:** 78_tp_db66ee
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [78, 79, 109, 157, 201, 210, 212, 226, 231, 355]
- **Retrieved Notes:** [79, 557, 542, 312, 84]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.100 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.100 |
| R-Precision | 0.100 |
| Latency (ms) | 40.59 |
| Predicted Intent | reminder |
| Expected Intent | reminder |
| Intent Correct | True |
| Predicted Category | Appointments |
| Expected Category | Appointments |
| Category Correct | True |

---

### INTENT — What payments and bills do I need to make?

- **Benchmark ID:** 77_tp_c2ce55
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [77, 120, 126, 128, 131, 137, 140, 144, 160, 162]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 33.96 |
| Predicted Intent | question |
| Expected Intent | todo |
| Intent Correct | False |

---

### INTENT — What is on my shopping list?

- **Benchmark ID:** 76_tp_d5a3f9
- **Difficulty:** easy
- **Challenge:** lexical
- **Relevant Notes:** [76, 322]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 25.90 |
| Predicted Intent | question |
| Expected Intent | todo |
| Intent Correct | False |

---

### INTENT — Show all my reminders

- **Benchmark ID:** 55_tp_1c812c
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [55, 152, 212, 312, 542, 557]
- **Retrieved Notes:** [557, 542, 312, 84, 80]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.600 |
| Recall@5 | 0.500 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.500 |
| R-Precision | 0.500 |
| Latency (ms) | 42.78 |
| Predicted Intent | reminder |
| Expected Intent | reminder |
| Intent Correct | True |
| Predicted Category | Reminders |
| Expected Category | Reminders |
| Category Correct | True |

---

### INTENT — My budget and expense tracking notes

- **Benchmark ID:** 82_tp_feed7d
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [82, 153, 202, 210, 216, 254, 281, 291, 331, 345]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 35.59 |
| Predicted Intent | reference |
| Expected Intent | todo |
| Intent Correct | False |

---

### INTENT — My travel plans and notes

- **Benchmark ID:** 81_tp_4afce2
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [81, 115, 126, 128, 130, 171, 175, 176, 178, 186]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 28.94 |
| Predicted Intent | reference |
| Expected Intent | todo |
| Intent Correct | False |

---

### INTENT — Fitness and workout notes

- **Benchmark ID:** 173_tp_d9566a
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [173, 185, 202, 232, 246, 291, 317, 380, 392, 433]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 36.15 |
| Predicted Intent | reference |
| Expected Intent | todo |
| Intent Correct | False |

---

### INTENT — My startup ideas and business notes

- **Benchmark ID:** 85_tp_6a3292
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [85, 86, 117, 120, 125, 128, 131, 134, 143, 157]
- **Retrieved Notes:** [85, 87, 178]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.100 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.100 |
| R-Precision | 0.100 |
| Latency (ms) | 48.43 |
| Predicted Intent | idea |
| Expected Intent | idea |
| Intent Correct | True |
| Predicted Category | Ideas - AI |
| Expected Category | Ideas - Startups |
| Category Correct | True |

---

### INTENT — What business ideas have I documented?

- **Benchmark ID:** 85_tp_aeedec
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [85, 86, 117, 120, 125, 128, 131, 134, 143, 157]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 33.71 |
| Predicted Intent | idea |
| Expected Intent | idea |
| Intent Correct | True |

---

### INTENT — Things I need to tell Sid

- **Benchmark ID:** 54_tp_6e7d12
- **Difficulty:** easy
- **Challenge:** lexical
- **Relevant Notes:** [54, 55, 56, 57, 117, 187, 203, 220, 225, 247]
- **Retrieved Notes:** [247, 57, 54]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.600 |
| Recall@5 | 0.300 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.300 |
| R-Precision | 0.300 |
| Latency (ms) | 35.28 |
| Predicted Intent | communication |
| Expected Intent | communication |
| Intent Correct | True |
| Predicted Category | Communication - Sid |
| Expected Category | Things to Tell Sid |
| Category Correct | True |

---

### INTENT — Things to discuss with Sid at the next meeting

- **Benchmark ID:** 54_tp_68cb9e
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [54, 55, 56, 57, 117, 187, 203, 220, 225, 247]
- **Retrieved Notes:** [247, 57, 54]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.600 |
| Recall@5 | 0.300 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.300 |
| R-Precision | 0.300 |
| Latency (ms) | 36.41 |
| Predicted Intent | communication |
| Expected Intent | communication |
| Intent Correct | True |
| Predicted Category | Communication - Sid |
| Expected Category | Things to Tell Sid |
| Category Correct | True |

---

### INTENT — Message to send to Siddhant about backend

- **Benchmark ID:** 54_tp_a4d45e
- **Difficulty:** medium
- **Challenge:** lexical_gap
- **Relevant Notes:** [54, 55, 56, 57, 117, 187, 203, 220, 225, 247]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 33.81 |
| Predicted Intent | communication |
| Expected Intent | communication |
| Intent Correct | True |

---

### INTENT — Reciprocal Rank Fusion

- **Benchmark ID:** 518_tp_583ff7
- **Difficulty:** medium
- **Challenge:** exact_phrase
- **Relevant Notes:** [518, 718, 818, 918, 1018]
- **Retrieved Notes:** [1093, 1078, 1077, 1067, 1059]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 40.47 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Study - AI |
| Category Correct | False |

---

### INTENT — Redis vs Kafka — when to use each

- **Benchmark ID:** 1024_tp_8759f9
- **Difficulty:** hard
- **Challenge:** comparison
- **Relevant Notes:** [1024, 771, 773, 520]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 38.94 |
| Predicted Intent | question |
| Expected Intent | study |
| Intent Correct | False |

---

### INTENT — Resources for learning backend development

- **Benchmark ID:** 108_tp_d16fba
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [132, 68, 165, 108, 206, 174, 177, 145]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 37.20 |
| Predicted Intent | study |
| Expected Intent | study |
| Intent Correct | True |

---

### INTENT — Notes about Fortran programming

- **Benchmark ID:** 0_tp_6cd1aa
- **Difficulty:** hard
- **Challenge:** negative
- **Relevant Notes:** []
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 33.68 |
| Predicted Intent | reference |
| Expected Intent | general |
| Intent Correct | False |

---

### INTENT — My notes on ancient Roman history

- **Benchmark ID:** 0_tp_b73b18
- **Difficulty:** hard
- **Challenge:** negative
- **Relevant Notes:** []
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 29.19 |
| Predicted Intent | reference |
| Expected Intent | general |
| Intent Correct | False |

---

### INTENT — Cooking recipes I've saved

- **Benchmark ID:** 0_tp_fe75c4
- **Difficulty:** hard
- **Challenge:** negative
- **Relevant Notes:** []
- **Retrieved Notes:** [1093, 1078, 1077, 1067, 1059]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 35.57 |
| Predicted Intent | general |
| Expected Intent | general |
| Intent Correct | True |
| Predicted Category | General |
| Expected Category | General |
| Category Correct | True |

---

### INTENT — KnowledgeVault RAG pipeline decisions and findings

- **Benchmark ID:** 1028_tp_65ec5f
- **Difficulty:** hard
- **Challenge:** multi_hop
- **Relevant Notes:** [1030, 1032, 533]
- **Retrieved Notes:** [1093, 1078, 1077, 1067, 1059]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 38.69 |
| Predicted Intent | general |
| Expected Intent | reference |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Reference - KnowledgeVault |
| Category Correct | False |

---

### INTENT — What benchmark results have I recorded for KnowledgeVault retrieval?

- **Benchmark ID:** 1028_tp_2e0731
- **Difficulty:** hard
- **Challenge:** multi_hop
- **Relevant Notes:** [1032, 523, 402]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 32.76 |
| Predicted Intent | question |
| Expected Intent | reference |
| Intent Correct | False |

---

### INTENT — What have I been working on this month?

- **Benchmark ID:** 77_tp_d33a9c
- **Difficulty:** hard
- **Challenge:** temporal
- **Relevant Notes:** [149]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 31.89 |
| Predicted Intent | question |
| Expected Intent | general |
| Intent Correct | False |

---

### INTENT — Recent notes and activities

- **Benchmark ID:** 77_tp_c2c25c
- **Difficulty:** hard
- **Challenge:** temporal
- **Relevant Notes:** [149, 286]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 29.17 |
| Predicted Intent | reference |
| Expected Intent | general |
| Intent Correct | False |

---

### INTENT — My study notes on AI and machine learning

- **Benchmark ID:** 1026_tp_74f5bc
- **Difficulty:** easy
- **Challenge:** synthesis
- **Relevant Notes:** [1026, 774, 1030, 510, 523, 268, 267, 782]
- **Retrieved Notes:** [65]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 29.46 |
| Predicted Intent | study |
| Expected Intent | study |
| Intent Correct | True |
| Predicted Category | Study - AI |
| Expected Category | Study - AI |
| Category Correct | True |

---

### INTENT — Messages I need to send Siddhant

- **Benchmark ID:** 54_tp_636e21
- **Difficulty:** easy
- **Challenge:** lexical_gap
- **Relevant Notes:** [54, 55, 56, 57, 117, 187, 203, 220]
- **Retrieved Notes:** [1093, 1078, 1077, 1067, 1059]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 36.04 |
| Predicted Intent | general |
| Expected Intent | communication |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Things to Tell Sid |
| Category Correct | False |

---

### INTENT — Pending conversations with Sid

- **Benchmark ID:** 54_tp_d0b55d
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [54, 55, 56, 57, 117, 187, 203, 220]
- **Retrieved Notes:** [1102, 1098, 1096, 1092, 1086]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 47.40 |
| Predicted Intent | todo |
| Expected Intent | communication |
| Intent Correct | False |
| Predicted Category | Tasks |
| Expected Category | Things to Tell Sid |
| Category Correct | False |

---

### INTENT — Notes about Sid and our project discussions

- **Benchmark ID:** 54_tp_e69fe7
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [54, 55, 56, 57, 117, 187, 203, 220]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 26.59 |
| Predicted Intent | reference |
| Expected Intent | communication |
| Intent Correct | False |

---

### INTENT — Business concepts I want to explore

- **Benchmark ID:** 85_tp_712892
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [85, 86, 117, 131, 134, 143, 157, 166]
- **Retrieved Notes:** [85, 117]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.250 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.250 |
| R-Precision | 0.250 |
| Latency (ms) | 46.10 |
| Predicted Intent | idea |
| Expected Intent | idea |
| Intent Correct | True |
| Predicted Category | Ideas - AI |
| Expected Category | Ideas |
| Category Correct | True |

---

### INTENT — Product ideas I have noted down

- **Benchmark ID:** 85_tp_46bae2
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [85, 86, 117, 131, 134, 143, 157, 166]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 35.81 |
| Predicted Intent | idea |
| Expected Intent | idea |
| Intent Correct | True |

---

### INTENT — Entrepreneurship and venture ideas

- **Benchmark ID:** 85_tp_97280d
- **Difficulty:** medium
- **Challenge:** lexical_gap
- **Relevant Notes:** [85, 86, 117, 131, 134, 143, 157, 166]
- **Retrieved Notes:** [85]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.125 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.125 |
| R-Precision | 0.125 |
| Latency (ms) | 44.49 |
| Predicted Intent | idea |
| Expected Intent | idea |
| Intent Correct | True |
| Predicted Category | Ideas - AI |
| Expected Category | Ideas |
| Category Correct | True |

---

### INTENT — Outstanding financial obligations

- **Benchmark ID:** 77_tp_c85047
- **Difficulty:** medium
- **Challenge:** lexical_gap
- **Relevant Notes:** [77, 120, 126, 128, 131, 137, 140, 144]
- **Retrieved Notes:** [1093, 1078, 1077, 1067, 1059]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 39.56 |
| Predicted Intent | general |
| Expected Intent | todo |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Bills |
| Category Correct | False |

---

### INTENT — Payments I still need to make

- **Benchmark ID:** 77_tp_573aa5
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [77, 120, 126, 128, 131, 137, 140, 144]
- **Retrieved Notes:** [1093, 1078, 1077, 1067, 1059]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 40.19 |
| Predicted Intent | general |
| Expected Intent | todo |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Bills |
| Category Correct | False |

---

### INTENT — Monthly expenses and dues

- **Benchmark ID:** 77_tp_e477f7
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [77, 120, 126, 128, 131, 137, 140, 144]
- **Retrieved Notes:** [1093, 1078, 1077, 1067, 1059]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 40.58 |
| Predicted Intent | general |
| Expected Intent | todo |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Bills |
| Category Correct | False |

---

### INTENT — Medical appointments on my calendar

- **Benchmark ID:** 78_tp_c31b3d
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [78, 79, 109, 157, 201, 210, 212, 226]
- **Retrieved Notes:** [557, 542, 312, 84, 80]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 40.44 |
| Predicted Intent | reminder |
| Expected Intent | todo |
| Intent Correct | False |
| Predicted Category | Reminders |
| Expected Category | To Do |
| Category Correct | False |

---

### INTENT — Healthcare and wellness reminders

- **Benchmark ID:** 78_tp_d52f8d
- **Difficulty:** easy
- **Challenge:** lexical_gap
- **Relevant Notes:** [78, 79, 109, 157, 201, 210, 212, 226]
- **Retrieved Notes:** [79, 557, 542, 312, 84]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.125 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.125 |
| R-Precision | 0.125 |
| Latency (ms) | 41.74 |
| Predicted Intent | reminder |
| Expected Intent | reminder |
| Intent Correct | True |
| Predicted Category | Appointments |
| Expected Category | Appointments |
| Category Correct | True |

---

### INTENT — In-memory datastore behavior notes

- **Benchmark ID:** 61_tp_0bc3d9
- **Difficulty:** medium
- **Challenge:** lexical_gap
- **Relevant Notes:** [61, 73, 92, 103, 157, 174, 269, 303]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 36.61 |
| Predicted Intent | reference |
| Expected Intent | study |
| Intent Correct | False |

---

### INTENT — Cache eviction policy details

- **Benchmark ID:** 61_tp_d58d06
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [61, 73, 92, 103, 157, 174, 269, 303]
- **Retrieved Notes:** [1093, 1078, 1077, 1067, 1059]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 42.01 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Study - Redis |
| Category Correct | False |

---

### INTENT — Team meetings I have attended

- **Benchmark ID:** 56_tp_3888f9
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [56, 106, 107, 149, 170, 233, 251, 283]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 36.38 |
| Predicted Intent | event |
| Expected Intent | event |
| Intent Correct | True |

---

### INTENT — Sprint retrospective and planning notes

- **Benchmark ID:** 56_tp_b7d172
- **Difficulty:** easy
- **Challenge:** lexical_gap
- **Relevant Notes:** [56, 106, 107, 149, 170, 233, 251, 283]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 33.30 |
| Predicted Intent | reference |
| Expected Intent | event |
| Intent Correct | False |

---

### INTENT — Sync notes with the team

- **Benchmark ID:** 56_tp_1162c8
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [56, 106, 107, 149, 170, 233, 251, 283]
- **Retrieved Notes:** [125]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 35.13 |
| Predicted Intent | reference |
| Expected Intent | meeting |
| Intent Correct | False |
| Predicted Category | Reference - Shared |
| Expected Category | Meetings |
| Category Correct | False |

---

### INTENT — Weekly standup summaries

- **Benchmark ID:** 56_tp_59ba00
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [56, 106, 107, 149, 170, 233, 251, 283]
- **Retrieved Notes:** [1093, 1078, 1077, 1067, 1059]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 44.02 |
| Predicted Intent | general |
| Expected Intent | meeting |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Meetings |
| Category Correct | False |

---

### INTENT — KnowledgeVault project milestones and deliverables

- **Benchmark ID:** 57_tp_d91b61
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [57, 88, 89, 90, 91, 94, 95, 96]
- **Retrieved Notes:** [1093, 1078, 1077, 1067, 1059]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 54.29 |
| Predicted Intent | general |
| Expected Intent | project |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Projects |
| Category Correct | False |

---

### INTENT — What is the architecture of my main project?

- **Benchmark ID:** 57_tp_92649a
- **Difficulty:** hard
- **Challenge:** multi_hop
- **Relevant Notes:** [57, 88, 89, 90, 91, 95, 96]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 41.90 |
| Predicted Intent | question |
| Expected Intent | project |
| Intent Correct | False |

---

### INTENT — Current sprint goals for KnowledgeVault

- **Benchmark ID:** 57_tp_74e120
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [57, 88, 89, 90, 91, 94, 95, 96]
- **Retrieved Notes:** [1093, 1078, 1077, 1067, 1059]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 46.16 |
| Predicted Intent | general |
| Expected Intent | project |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Projects |
| Category Correct | False |

---

### INTENT — Capstone project tasks and status

- **Benchmark ID:** 175_tp_9c7eb5
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [175, 190, 199, 225, 233, 263, 285, 382]
- **Retrieved Notes:** [1102, 1098, 1096, 1092, 1086]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 49.26 |
| Predicted Intent | todo |
| Expected Intent | project |
| Intent Correct | False |
| Predicted Category | Tasks |
| Expected Category | Projects |
| Category Correct | False |

---

### INTENT — University project submission deadlines

- **Benchmark ID:** 175_tp_c51da4
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [175, 190, 199, 225, 233, 263, 285, 382]
- **Retrieved Notes:** [1093, 1078, 1077, 1067, 1059]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 40.70 |
| Predicted Intent | general |
| Expected Intent | project |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Projects |
| Category Correct | False |

---

### INTENT — My personal reflections and journal entries

- **Benchmark ID:** 113_tp_6bba32
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [113, 149, 152, 162, 166, 191]
- **Retrieved Notes:** [1093, 1078, 1077, 1067, 1059]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 39.69 |
| Predicted Intent | general |
| Expected Intent | general |
| Intent Correct | True |
| Predicted Category | General |
| Expected Category | General |
| Category Correct | True |

---

### INTENT — What did I realize recently?

- **Benchmark ID:** 113_tp_ff1a3d
- **Difficulty:** hard
- **Challenge:** semantic
- **Relevant Notes:** [113, 149, 152, 162, 166, 191]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 36.70 |
| Predicted Intent | question |
| Expected Intent | general |
| Intent Correct | False |

---

### INTENT — Insights I've been writing down

- **Benchmark ID:** 113_tp_be2de4
- **Difficulty:** medium
- **Challenge:** lexical_gap
- **Relevant Notes:** [113, 149, 152, 162, 166, 191]
- **Retrieved Notes:** [1093, 1078, 1077, 1067, 1059]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 41.42 |
| Predicted Intent | general |
| Expected Intent | general |
| Intent Correct | True |
| Predicted Category | General |
| Expected Category | General |
| Category Correct | True |

---

### INTENT — My career goals and direction notes

- **Benchmark ID:** 56_tp_f28e5b
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [56, 61, 91, 96, 101, 106, 114, 155]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 30.96 |
| Predicted Intent | reference |
| Expected Intent | general |
| Intent Correct | False |

---

### INTENT — Long-term professional planning notes

- **Benchmark ID:** 56_tp_e42aaa
- **Difficulty:** hard
- **Challenge:** lexical_gap
- **Relevant Notes:** [56, 61, 91, 96, 101, 106, 114, 155]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 34.68 |
| Predicted Intent | reference |
| Expected Intent | general |
| Intent Correct | False |

---

### INTENT — Time management and focus techniques

- **Benchmark ID:** 85_tp_c33ed2
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [85, 199, 224, 240, 248, 286, 429, 453]
- **Retrieved Notes:** [1093, 1078, 1077, 1067, 1059]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 40.52 |
| Predicted Intent | general |
| Expected Intent | reference |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Reference - Productivity |
| Category Correct | False |

---

### INTENT — Notes on staying productive while studying

- **Benchmark ID:** 85_tp_a94724
- **Difficulty:** medium
- **Challenge:** lexical_gap
- **Relevant Notes:** [85, 199, 224, 240, 248, 286, 429, 453]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 39.69 |
| Predicted Intent | reference |
| Expected Intent | reference |
| Intent Correct | True |

---

### INTENT — FastAPI route and dependency injection notes

- **Benchmark ID:** 68_tp_025916
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [68, 120, 132, 145, 153, 165, 167, 169]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 36.57 |
| Predicted Intent | reference |
| Expected Intent | reference |
| Intent Correct | True |

---

### INTENT — Python web framework notes for FastAPI

- **Benchmark ID:** 68_tp_f99196
- **Difficulty:** easy
- **Challenge:** lexical_gap
- **Relevant Notes:** [68, 120, 132, 145, 153, 165, 167, 169]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 35.29 |
| Predicted Intent | reference |
| Expected Intent | study |
| Intent Correct | False |

---

### INTENT — API endpoint design patterns in FastAPI

- **Benchmark ID:** 68_tp_9b1c89
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [68, 120, 132, 145, 153, 165, 167, 169]
- **Retrieved Notes:** [1093, 1078, 1077, 1067, 1059]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 47.38 |
| Predicted Intent | general |
| Expected Intent | reference |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Reference - KnowledgeVault Backend |
| Category Correct | False |

---

### INTENT — SQLAlchemy ORM usage patterns

- **Benchmark ID:** 55_tp_fbaf81
- **Difficulty:** medium
- **Challenge:** lexical
- **Relevant Notes:** [55, 58, 69, 85, 98, 123, 129, 132]
- **Retrieved Notes:** [1093, 1078, 1077, 1067, 1059]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 55.70 |
| Predicted Intent | general |
| Expected Intent | reference |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Reference - KnowledgeVault Backend |
| Category Correct | False |

---

### INTENT — Database session management in Python

- **Benchmark ID:** 55_tp_e342eb
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [55, 58, 69, 85, 98, 123, 129, 132]
- **Retrieved Notes:** [1093, 1078, 1077, 1067, 1059]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 40.81 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Study - FastAPI |
| Category Correct | False |

---

### INTENT — How do I fix N+1 query problems?

- **Benchmark ID:** 55_tp_d34490
- **Difficulty:** hard
- **Challenge:** semantic
- **Relevant Notes:** [55, 58, 69, 85, 98, 123, 129, 132]
- **Retrieved Notes:** [1102, 1098, 1096, 1092, 1086]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 52.02 |
| Predicted Intent | todo |
| Expected Intent | question |
| Intent Correct | False |
| Predicted Category | Tasks |
| Expected Category | Questions |
| Category Correct | False |

---

### INTENT — pgvector setup and index configuration

- **Benchmark ID:** 66_tp_9be255
- **Difficulty:** hard
- **Challenge:** lexical
- **Relevant Notes:** [66, 168, 215, 298, 323, 337, 367, 500]
- **Retrieved Notes:** [1093, 1078, 1077, 1067, 1059]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 42.62 |
| Predicted Intent | general |
| Expected Intent | reference |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Reference - PostgreSQL |
| Category Correct | False |

---

### INTENT — Vector similarity search configuration

- **Benchmark ID:** 66_tp_72bd4f
- **Difficulty:** hard
- **Challenge:** semantic
- **Relevant Notes:** [66, 168, 215, 298, 323, 337, 367, 500]
- **Retrieved Notes:** [1093, 1078, 1077, 1067, 1059]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 45.75 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Study - AI |
| Category Correct | False |

---

### INTENT — Algorithm and data structure study notes

- **Benchmark ID:** 59_tp_a4350a
- **Difficulty:** medium
- **Challenge:** lexical
- **Relevant Notes:** [59, 60, 182, 204, 215, 224, 244, 247]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 36.30 |
| Predicted Intent | study |
| Expected Intent | study |
| Intent Correct | True |

---

### INTENT — Competitive programming problem patterns

- **Benchmark ID:** 59_tp_a3126e
- **Difficulty:** hard
- **Challenge:** semantic
- **Relevant Notes:** [59, 60, 182, 204, 215, 224, 244, 247]
- **Retrieved Notes:** [1093, 1078, 1077, 1067, 1059]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 40.67 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Study - Algorithms |
| Category Correct | False |

---

### INTENT — How do I solve graph traversal problems?

- **Benchmark ID:** 59_tp_fe7b32
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [59, 60, 182, 204, 215, 224, 244, 247]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 39.96 |
| Predicted Intent | question |
| Expected Intent | question |
| Intent Correct | True |

---

### INTENT — Operating systems exam preparation notes

- **Benchmark ID:** 59_tp_652a70
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [59, 132, 141, 146, 174, 179, 203, 205]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 41.04 |
| Predicted Intent | reference |
| Expected Intent | study |
| Intent Correct | False |

---

### INTENT — CPU scheduling algorithms I need to know

- **Benchmark ID:** 59_tp_566c28
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [59, 132, 141, 146, 174, 179, 203, 205]
- **Retrieved Notes:** [1093, 1078, 1077, 1067, 1059]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 45.98 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Study - Operating Systems |
| Category Correct | False |

---

### INTENT — Computer networking concepts for university

- **Benchmark ID:** 75_tp_eae57f
- **Difficulty:** medium
- **Challenge:** lexical
- **Relevant Notes:** [75, 118, 159, 162, 168, 180, 237, 276]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 41.77 |
| Predicted Intent | idea |
| Expected Intent | study |
| Intent Correct | False |

---

### INTENT — TCP/IP and HTTP protocol notes

- **Benchmark ID:** 75_tp_ac0c4f
- **Difficulty:** easy
- **Challenge:** lexical
- **Relevant Notes:** [75, 118, 159, 162, 168, 180, 237, 276]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 42.48 |
| Predicted Intent | reference |
| Expected Intent | study |
| Intent Correct | False |

---

### INTENT — Kubernetes cluster management notes

- **Benchmark ID:** 62_tp_d2020d
- **Difficulty:** medium
- **Challenge:** lexical
- **Relevant Notes:** [62, 118, 181, 230, 383, 410, 419, 548]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 31.93 |
| Predicted Intent | reference |
| Expected Intent | study |
| Intent Correct | False |

---

### INTENT — Container orchestration with K8s

- **Benchmark ID:** 62_tp_9d6d2c
- **Difficulty:** hard
- **Challenge:** lexical_gap
- **Relevant Notes:** [62, 118, 181, 230, 383, 410, 419, 548]
- **Retrieved Notes:** [1093, 1078, 1077, 1067, 1059]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 41.81 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Study - Kubernetes |
| Category Correct | False |

---

### INTENT — Authentication and JWT token notes

- **Benchmark ID:** 63_tp_d8d22b
- **Difficulty:** medium
- **Challenge:** lexical
- **Relevant Notes:** [63, 129, 165, 189, 227, 244, 276, 287]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 45.68 |
| Predicted Intent | reference |
| Expected Intent | study |
| Intent Correct | False |

---

### INTENT — How does OAuth 2.0 work?

- **Benchmark ID:** 63_tp_6690cb
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [63, 129, 165, 189, 227, 244, 276, 287]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 39.79 |
| Predicted Intent | question |
| Expected Intent | question |
| Intent Correct | True |

---

### INTENT — What eviction policies does Redis support?

- **Benchmark ID:** 61_tp_217848
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [61, 73, 92, 103, 124, 146, 157, 169]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 31.89 |
| Predicted Intent | question |
| Expected Intent | question |
| Intent Correct | True |

---

### INTENT — What types of indexes does PostgreSQL support?

- **Benchmark ID:** 58_tp_3d1edd
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [58, 66, 74, 104, 113, 114, 136, 139]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 27.62 |
| Predicted Intent | question |
| Expected Intent | question |
| Intent Correct | True |

---

### INTENT — When should I use GIN vs B-tree indexes?

- **Benchmark ID:** 58_tp_7b89c1
- **Difficulty:** hard
- **Challenge:** comparison
- **Relevant Notes:** [58, 66, 74, 104, 139]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 30.03 |
| Predicted Intent | question |
| Expected Intent | question |
| Intent Correct | True |

---

### INTENT — How does retrieval augmented generation work?

- **Benchmark ID:** 65_tp_d64f03
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [65, 114, 186, 197, 219, 222, 267, 296]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 26.69 |
| Predicted Intent | question |
| Expected Intent | question |
| Intent Correct | True |

---

### INTENT — What are the steps in a RAG pipeline?

- **Benchmark ID:** 65_tp_0a59fb
- **Difficulty:** hard
- **Challenge:** semantic
- **Relevant Notes:** [65, 114, 186, 197, 219, 222, 267, 296]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 31.73 |
| Predicted Intent | question |
| Expected Intent | question |
| Intent Correct | True |

---

### INTENT — How are text embeddings generated?

- **Benchmark ID:** 168_tp_cc9fa1
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [168, 183, 228, 289, 298, 323, 376, 486]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 36.47 |
| Predicted Intent | question |
| Expected Intent | question |
| Intent Correct | True |

---

### INTENT — What is the difference between semantic and keyword search?

- **Benchmark ID:** 168_tp_df38ac
- **Difficulty:** hard
- **Challenge:** semantic
- **Relevant Notes:** [168, 183, 228, 289, 298, 323, 376, 486]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 37.53 |
| Predicted Intent | question |
| Expected Intent | question |
| Intent Correct | True |

---

### INTENT — What is due this week?

- **Benchmark ID:** 184_tp_c5a4df
- **Difficulty:** medium
- **Challenge:** temporal
- **Relevant Notes:** [233, 368, 498]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 32.42 |
| Predicted Intent | question |
| Expected Intent | todo |
| Intent Correct | False |

---

### INTENT — Upcoming deadlines and submission dates

- **Benchmark ID:** 184_tp_cf679c
- **Difficulty:** medium
- **Challenge:** temporal
- **Relevant Notes:** [233, 368, 498]
- **Retrieved Notes:** [1093, 1078, 1077, 1067, 1059]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 35.85 |
| Predicted Intent | general |
| Expected Intent | todo |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Tasks |
| Category Correct | False |

---

### INTENT — Tasks I need to complete before month end

- **Benchmark ID:** 184_tp_96ea32
- **Difficulty:** hard
- **Challenge:** temporal
- **Relevant Notes:** [233, 368, 498]
- **Retrieved Notes:** [1102, 1098, 1096, 1092, 1086]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 41.73 |
| Predicted Intent | todo |
| Expected Intent | todo |
| Intent Correct | True |
| Predicted Category | Tasks |
| Expected Category | Tasks |
| Category Correct | True |

---

### INTENT — What appointments have I booked this month?

- **Benchmark ID:** 78_tp_63adc1
- **Difficulty:** medium
- **Challenge:** temporal
- **Relevant Notes:** [78, 559]
- **Retrieved Notes:** [557, 542, 312, 84, 80]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 37.89 |
| Predicted Intent | reminder |
| Expected Intent | reminder |
| Intent Correct | True |
| Predicted Category | Reminders |
| Expected Category | Appointments |
| Category Correct | False |

---

### INTENT — My upcoming travel and trip bookings

- **Benchmark ID:** 78_tp_a0f1d8
- **Difficulty:** easy
- **Challenge:** temporal
- **Relevant Notes:** [78, 81, 115]
- **Retrieved Notes:** [1093, 1078, 1077, 1067, 1059]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 32.91 |
| Predicted Intent | general |
| Expected Intent | todo |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Travel |
| Category Correct | False |

---

### INTENT — Transport and accommodation I need to arrange

- **Benchmark ID:** 78_tp_219ffa
- **Difficulty:** medium
- **Challenge:** lexical_gap
- **Relevant Notes:** [78, 81, 115, 126, 128, 130, 160, 171]
- **Retrieved Notes:** [1093, 1078, 1077, 1067, 1059]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 41.15 |
| Predicted Intent | general |
| Expected Intent | todo |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Travel |
| Category Correct | False |

---

### INTENT — Redis vs PostgreSQL — when to use each for persistence?

- **Benchmark ID:** 103_tp_7520ad
- **Difficulty:** hard
- **Challenge:** comparison
- **Relevant Notes:** [103, 104, 73, 74, 58, 92, 61]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 40.52 |
| Predicted Intent | question |
| Expected Intent | study |
| Intent Correct | False |

---

### INTENT — Docker vs Kubernetes — what is the difference?

- **Benchmark ID:** 72_tp_807260
- **Difficulty:** hard
- **Challenge:** comparison
- **Relevant Notes:** [118, 62, 383]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 54.92 |
| Predicted Intent | question |
| Expected Intent | study |
| Intent Correct | False |

---

### INTENT — How do I decide between hybrid retrieval and cross-encoder reranking?

- **Benchmark ID:** 65_tp_205f1c
- **Difficulty:** hard
- **Challenge:** multi_hop
- **Relevant Notes:** [67, 176, 119, 88, 123]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 112.12 |
| Predicted Intent | question |
| Expected Intent | study |
| Intent Correct | False |

---

### INTENT — What have I documented about retrieval quality in KnowledgeVault?

- **Benchmark ID:** 89_tp_0f29db
- **Difficulty:** hard
- **Challenge:** multi_hop
- **Relevant Notes:** [89, 485, 487, 402, 595, 88, 90]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 65.11 |
| Predicted Intent | question |
| Expected Intent | reference |
| Intent Correct | False |

---

### INTENT — All my university and course study notes

- **Benchmark ID:** 58_tp_32b5cf
- **Difficulty:** easy
- **Challenge:** synthesis
- **Relevant Notes:** [58, 61, 62, 66, 69, 122, 130, 131]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 39.32 |
| Predicted Intent | study |
| Expected Intent | study |
| Intent Correct | True |

---

### INTENT — All my brainstorming and ideation notes

- **Benchmark ID:** 85_tp_f46697
- **Difficulty:** easy
- **Challenge:** synthesis
- **Relevant Notes:** [85, 86, 117, 143, 157, 178, 225, 240]
- **Retrieved Notes:** [87, 85, 117]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.250 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| MAP@5 | 0.146 |
| R-Precision | 0.250 |
| Latency (ms) | 60.93 |
| Predicted Intent | idea |
| Expected Intent | idea |
| Intent Correct | True |
| Predicted Category | Ideas - AI Summarization |
| Expected Category | Ideas |
| Category Correct | True |

---

### INTENT — My technical reference cheat sheets

- **Benchmark ID:** 72_tp_32bacd
- **Difficulty:** easy
- **Challenge:** synthesis
- **Relevant Notes:** [72, 73, 74, 75, 122, 135]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 43.83 |
| Predicted Intent | reference |
| Expected Intent | reference |
| Intent Correct | True |

---

### INTENT — All my communication and message drafts

- **Benchmark ID:** 54_tp_b42b02
- **Difficulty:** easy
- **Challenge:** synthesis
- **Relevant Notes:** [54, 56, 57, 106, 132, 141]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 36.09 |
| Predicted Intent | communication |
| Expected Intent | communication |
| Intent Correct | True |

---

### INTENT — Errands I need to run today

- **Benchmark ID:** 76_tp_c52e4b
- **Difficulty:** medium
- **Challenge:** lexical_gap
- **Relevant Notes:** [76, 164, 190, 202, 286, 309, 322, 475]
- **Retrieved Notes:** [1093, 1078, 1077, 1067, 1059]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 43.00 |
| Predicted Intent | general |
| Expected Intent | todo |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | To Do |
| Category Correct | False |

---

### INTENT — Things I need to pick up from the store

- **Benchmark ID:** 76_tp_c74a5f
- **Difficulty:** easy
- **Challenge:** lexical_gap
- **Relevant Notes:** [76, 164, 190, 202, 286, 309, 322, 475]
- **Retrieved Notes:** [1093, 1078, 1077, 1067, 1059]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 41.44 |
| Predicted Intent | general |
| Expected Intent | todo |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Shopping |
| Category Correct | False |

---

### INTENT — Physical training and exercise plan

- **Benchmark ID:** 173_tp_f41c30
- **Difficulty:** easy
- **Challenge:** lexical_gap
- **Relevant Notes:** [173, 202, 291, 317, 380, 621, 631, 680]
- **Retrieved Notes:** [1093, 1078, 1077, 1067, 1059]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 44.27 |
| Predicted Intent | general |
| Expected Intent | todo |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Health |
| Category Correct | False |

---

### INTENT — How am I planning to stay healthy?

- **Benchmark ID:** 173_tp_7bafaa
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [173, 202, 291, 317, 380, 621, 631, 680]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 36.98 |
| Predicted Intent | question |
| Expected Intent | question |
| Intent Correct | True |

---

### INTENT — How much am I spending per month?

- **Benchmark ID:** 82_tp_86df0e
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [82, 210, 216, 281, 331, 345, 407, 535]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 46.85 |
| Predicted Intent | question |
| Expected Intent | question |
| Intent Correct | True |

---

### INTENT — Personal finance tracking notes

- **Benchmark ID:** 82_tp_3665b0
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [82, 210, 216, 281, 331, 345, 407, 535]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 36.60 |
| Predicted Intent | reference |
| Expected Intent | reference |
| Intent Correct | True |

---

### INTENT — BRPOPLPUSH reliable queue implementation

- **Benchmark ID:** 246_tp_6ef122
- **Difficulty:** hard
- **Challenge:** exact_phrase
- **Relevant Notes:** [246, 433, 643, 673, 684, 705, 773, 784]
- **Retrieved Notes:** [1093, 1078, 1077, 1067, 1059]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 48.78 |
| Predicted Intent | general |
| Expected Intent | reference |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Reference - Redis |
| Category Correct | False |

---

### INTENT — ACID properties of databases

- **Benchmark ID:** 229_tp_454ff2
- **Difficulty:** easy
- **Challenge:** exact_phrase
- **Relevant Notes:** [229, 690, 790, 890, 990, 1090]
- **Retrieved Notes:** [1093, 1078, 1077, 1067, 1059]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 41.18 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Study - DBMS |
| Category Correct | False |

---

### INTENT — RRF score combination for hybrid search

- **Benchmark ID:** 518_tp_930ea0
- **Difficulty:** hard
- **Challenge:** exact_phrase
- **Relevant Notes:** [518, 718, 818, 918, 1018]
- **Retrieved Notes:** [1093, 1078, 1077, 1067, 1059]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 37.66 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Study - AI |
| Category Correct | False |

---

### INTENT — HNSW approximate nearest neighbor algorithm

- **Benchmark ID:** 215_tp_55df73
- **Difficulty:** hard
- **Challenge:** exact_phrase
- **Relevant Notes:** [215, 430, 681, 781, 881, 981, 1081]
- **Retrieved Notes:** [1093, 1078, 1077, 1067, 1059]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 42.69 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Study - AI |
| Category Correct | False |

---

### INTENT — What do I need to buy this weekend?

- **Benchmark ID:** 76_tp_5c724a
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [76, 164, 190, 202, 309, 322, 393, 475]
- **Retrieved Notes:** [1102, 1098, 1096, 1092, 1086]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 42.99 |
| Predicted Intent | todo |
| Expected Intent | todo |
| Intent Correct | True |
| Predicted Category | Tasks |
| Expected Category | Shopping |
| Category Correct | True |

---

### INTENT — All my pending reminders and follow-ups

- **Benchmark ID:** 55_tp_3ff20c
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [55, 152, 212, 312, 542, 557]
- **Retrieved Notes:** [557, 542, 312, 84, 80]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.600 |
| Recall@5 | 0.500 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.500 |
| R-Precision | 0.500 |
| Latency (ms) | 39.81 |
| Predicted Intent | reminder |
| Expected Intent | reminder |
| Intent Correct | True |
| Predicted Category | Reminders |
| Expected Category | Reminders |
| Category Correct | True |

---

### INTENT — What have I told myself not to forget?

- **Benchmark ID:** 55_tp_05e927
- **Difficulty:** medium
- **Challenge:** lexical_gap
- **Relevant Notes:** [55, 152, 212, 312, 542, 557]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 33.38 |
| Predicted Intent | question |
| Expected Intent | reminder |
| Intent Correct | False |

---

### INTENT — LeetCode patterns and problem-solving techniques

- **Benchmark ID:** 117_tp_44e6df
- **Difficulty:** medium
- **Challenge:** lexical
- **Relevant Notes:** [117, 127, 187, 224, 271, 279, 282, 316]
- **Retrieved Notes:** [1093, 1078, 1077, 1067, 1059]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 41.60 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Study - Interview Prep |
| Category Correct | False |

---

### INTENT — How do I approach dynamic programming questions?

- **Benchmark ID:** 117_tp_7bf7d7
- **Difficulty:** hard
- **Challenge:** semantic
- **Relevant Notes:** [117, 127, 187, 224, 271, 279, 282, 316]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 34.59 |
| Predicted Intent | question |
| Expected Intent | question |
| Intent Correct | True |

---

### INTENT — System design concepts I need to review

- **Benchmark ID:** 70_tp_39b780
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [70, 145, 267, 305, 309, 334, 344, 346]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 36.03 |
| Predicted Intent | idea |
| Expected Intent | study |
| Intent Correct | False |

---

### INTENT — How do I design a scalable URL shortener?

- **Benchmark ID:** 70_tp_c6f60d
- **Difficulty:** hard
- **Challenge:** semantic
- **Relevant Notes:** [70, 145, 267, 305, 309, 334, 344, 346]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 42.66 |
| Predicted Intent | question |
| Expected Intent | question |
| Intent Correct | True |

---

### INTENT — Behavioral interview story preparation

- **Benchmark ID:** 83_tp_a140c7
- **Difficulty:** medium
- **Challenge:** lexical
- **Relevant Notes:** [83, 85, 113, 114, 116, 131, 134, 135]
- **Retrieved Notes:** [1093, 1078, 1077, 1067, 1059]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 38.09 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Study - Interview Prep |
| Category Correct | False |

---

### INTENT — Resume writing tips and improvement notes

- **Benchmark ID:** 100_tp_b51d58
- **Difficulty:** easy
- **Challenge:** lexical
- **Relevant Notes:** [100, 142, 185, 270, 523, 525]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 34.82 |
| Predicted Intent | reference |
| Expected Intent | reference |
| Intent Correct | True |

---

### INTENT — How should I write my software engineer resume?

- **Benchmark ID:** 100_tp_fcae97
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [100, 142, 185, 270, 523, 525]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 32.03 |
| Predicted Intent | question |
| Expected Intent | question |
| Intent Correct | True |

---

### INTENT — Books I am reading or have read recently

- **Benchmark ID:** 78_tp_c601ae
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [78, 128, 155, 160, 172, 182, 194, 234]
- **Retrieved Notes:** [1093, 1078, 1077, 1067, 1059]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 42.15 |
| Predicted Intent | general |
| Expected Intent | reference |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Reference - Books |
| Category Correct | False |

---

### INTENT — Reading list and book notes

- **Benchmark ID:** 78_tp_0f3259
- **Difficulty:** easy
- **Challenge:** lexical
- **Relevant Notes:** [78, 128, 155, 160, 172, 182, 194, 234]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 35.95 |
| Predicted Intent | reference |
| Expected Intent | reference |
| Intent Correct | True |

---

### INTENT — Habit formation notes from Atomic Habits

- **Benchmark ID:** 304_tp_4994bc
- **Difficulty:** easy
- **Challenge:** lexical
- **Relevant Notes:** [304, 317, 482, 557, 631, 634, 698, 734]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 40.68 |
| Predicted Intent | reference |
| Expected Intent | study |
| Intent Correct | False |

---

### INTENT — Summary of James Clear's key ideas on habits

- **Benchmark ID:** 304_tp_37657b
- **Difficulty:** medium
- **Challenge:** lexical_gap
- **Relevant Notes:** [304, 317, 482, 557, 631, 634, 698, 734]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 38.75 |
| Predicted Intent | idea |
| Expected Intent | study |
| Intent Correct | False |

---

### INTENT — Online courses and tutorials I am taking

- **Benchmark ID:** 71_tp_43e20b
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [71, 145, 231, 266, 357, 394, 417, 471]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 31.98 |
| Predicted Intent | study |
| Expected Intent | study |
| Intent Correct | True |

---

### INTENT — Sleep improvement techniques and tips

- **Benchmark ID:** 133_tp_12eb56
- **Difficulty:** medium
- **Challenge:** lexical
- **Relevant Notes:** [133, 136, 202, 288, 348, 380, 434, 538]
- **Retrieved Notes:** [1093, 1078, 1077, 1067, 1059]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 41.71 |
| Predicted Intent | general |
| Expected Intent | reference |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Reference - Health |
| Category Correct | False |

---

### INTENT — How can I improve my sleep quality?

- **Benchmark ID:** 133_tp_2c6b3e
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [133, 136, 202, 288, 348, 380, 434, 538]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 34.81 |
| Predicted Intent | question |
| Expected Intent | question |
| Intent Correct | True |

---

### INTENT — Nutrition and supplement tracking notes

- **Benchmark ID:** 109_tp_f852f9
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [109, 133, 226, 286]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 35.23 |
| Predicted Intent | reference |
| Expected Intent | reference |
| Intent Correct | True |

---

### INTENT — What supplements should I be taking?

- **Benchmark ID:** 109_tp_f444c2
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [109, 133, 226, 286]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 34.04 |
| Predicted Intent | question |
| Expected Intent | question |
| Intent Correct | True |

---

### INTENT — Mental health practices and coping strategies

- **Benchmark ID:** 152_tp_3685ae
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [152, 288, 317, 472, 575]
- **Retrieved Notes:** [1093, 1078, 1077, 1067, 1059]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 40.78 |
| Predicted Intent | general |
| Expected Intent | reference |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Reference - Health |
| Category Correct | False |

---

### INTENT — My notes on managing stress and anxiety

- **Benchmark ID:** 152_tp_5aba2a
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [152, 288, 317, 472, 575]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 38.42 |
| Predicted Intent | reference |
| Expected Intent | reference |
| Intent Correct | True |

---

### INTENT — Plans for open source and public building

- **Benchmark ID:** 117_tp_eab7a3
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [117, 141, 395, 400, 440, 453, 522, 554]
- **Retrieved Notes:** [1093, 1078, 1077, 1067, 1059]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 41.14 |
| Predicted Intent | general |
| Expected Intent | idea |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Ideas |
| Category Correct | False |

---

### INTENT — Notes on growing my developer presence online

- **Benchmark ID:** 117_tp_594cbf
- **Difficulty:** medium
- **Challenge:** lexical_gap
- **Relevant Notes:** [117, 141, 395, 400, 440, 453, 522, 554]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 45.48 |
| Predicted Intent | reference |
| Expected Intent | idea |
| Intent Correct | False |

---

### INTENT — Fortran programming and legacy code notes

- **Benchmark ID:** 0_tp_07253f
- **Difficulty:** hard
- **Challenge:** negative
- **Relevant Notes:** []
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 37.79 |
| Predicted Intent | reference |
| Expected Intent | general |
| Intent Correct | False |

---

### INTENT — Ancient history and archaeology notes

- **Benchmark ID:** 0_tp_13e990
- **Difficulty:** hard
- **Challenge:** negative
- **Relevant Notes:** []
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 35.86 |
| Predicted Intent | reference |
| Expected Intent | general |
| Intent Correct | False |

---

### INTENT — Wine and cheese pairing recommendations

- **Benchmark ID:** 0_tp_f9589c
- **Difficulty:** hard
- **Challenge:** negative
- **Relevant Notes:** []
- **Retrieved Notes:** [1093, 1078, 1077, 1067, 1059]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 44.00 |
| Predicted Intent | general |
| Expected Intent | general |
| Intent Correct | True |
| Predicted Category | General |
| Expected Category | General |
| Category Correct | True |

---

### INTENT — Piano lessons and music theory notes

- **Benchmark ID:** 0_tp_5abfd7
- **Difficulty:** hard
- **Challenge:** negative
- **Relevant Notes:** []
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 36.41 |
| Predicted Intent | reference |
| Expected Intent | general |
| Intent Correct | False |

---

### INTENT — Gardening and plant care notes

- **Benchmark ID:** 0_tp_4fb99e
- **Difficulty:** hard
- **Challenge:** negative
- **Relevant Notes:** []
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 32.59 |
| Predicted Intent | reference |
| Expected Intent | general |
| Intent Correct | False |

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
| Latency (ms) | 176.99 |
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
| Latency (ms) | 104.12 |
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
| Latency (ms) | 102.04 |
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
| Latency (ms) | 111.59 |
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
| Latency (ms) | 126.72 |
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
| Latency (ms) | 123.87 |
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
| Latency (ms) | 115.76 |
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
| Latency (ms) | 118.19 |
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
| Latency (ms) | 120.78 |
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
| Latency (ms) | 101.12 |
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
| Latency (ms) | 91.74 |
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
| Latency (ms) | 109.05 |
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
| Latency (ms) | 113.72 |
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
| Latency (ms) | 108.75 |
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
| Latency (ms) | 131.32 |
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
| Latency (ms) | 132.11 |
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
| Latency (ms) | 110.08 |
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
| Latency (ms) | 116.22 |
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
| Latency (ms) | 117.42 |
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
| Latency (ms) | 97.36 |
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
| Latency (ms) | 109.98 |
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
| Latency (ms) | 102.13 |
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
| Latency (ms) | 107.86 |
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
| Latency (ms) | 136.80 |
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
| Latency (ms) | 102.75 |
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
| Latency (ms) | 111.92 |
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
| Latency (ms) | 143.71 |
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
| Latency (ms) | 147.52 |
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
| Latency (ms) | 120.35 |
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
| Latency (ms) | 111.63 |
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
| Latency (ms) | 197.12 |
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
| Latency (ms) | 110.58 |
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
| Latency (ms) | 109.80 |
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
| Latency (ms) | 112.11 |
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
| Latency (ms) | 108.10 |
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
| Latency (ms) | 101.61 |
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
| Latency (ms) | 113.52 |
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
| Latency (ms) | 105.72 |
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
| Latency (ms) | 112.83 |
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
| Latency (ms) | 147.03 |
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
| Latency (ms) | 135.68 |
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
| Latency (ms) | 105.72 |
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
| Latency (ms) | 100.78 |
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
| Latency (ms) | 104.52 |
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
| Latency (ms) | 99.63 |
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
| Latency (ms) | 100.60 |
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
| Latency (ms) | 103.26 |
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
| Latency (ms) | 114.88 |
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
| Latency (ms) | 123.33 |
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
| Latency (ms) | 120.35 |
| Predicted Intent | question |
| Expected Intent | question |
| Intent Correct | True |

---

### HYBRID — What are useful Python tips and tricks I've learned?

- **Benchmark ID:** 108_tp_62f888
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [108, 174, 177, 206, 232, 239, 272, 283]
- **Retrieved Notes:** [318, 206, 633, 357, 464, 745, 845, 945, 1045, 451, 266, 751, 851, 951, 1051, 69, 272, 327, 388, 163]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.125 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| MAP@5 | 0.062 |
| R-Precision | 0.125 |
| Latency (ms) | 122.02 |
| Predicted Intent | question |
| Expected Intent | study |
| Intent Correct | False |
| Predicted Category | Questions - Python |
| Expected Category | Study - Python |
| Category Correct | False |

---

### HYBRID — Show my Python programming notes

- **Benchmark ID:** 108_tp_89ce75
- **Difficulty:** easy
- **Challenge:** lexical
- **Relevant Notes:** [108, 174, 177, 206, 232, 239, 272, 283]
- **Retrieved Notes:** [87, 583, 699, 799, 899, 999, 1099, 258, 709, 809, 909, 1009, 283, 662, 762, 862, 962, 1062, 110, 633]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.077 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 112.88 |
| Predicted Intent | reference |
| Expected Intent | study |
| Intent Correct | False |

---

### HYBRID — How does Python async programming work?

- **Benchmark ID:** 170_tp_39fb15
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [170, 283, 304, 359, 364, 372, 471, 661, 662, 663]
- **Retrieved Notes:** [304, 734, 834, 934, 1034, 359, 283, 662, 762, 862, 962, 1062, 633, 170, 471, 663, 763, 863, 963, 1063]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.100 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.100 |
| R-Precision | 0.400 |
| Latency (ms) | 110.92 |
| Predicted Intent | question |
| Expected Intent | study |
| Intent Correct | False |
| Predicted Category | Questions - Python |
| Expected Category | Study - Python |
| Category Correct | False |

---

### HYBRID — What git commands and workflows have I noted?

- **Benchmark ID:** 130_tp_e144a1
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [130, 135, 144, 169, 229, 272, 317, 328, 366, 395]
- **Retrieved Notes:** [612, 328, 501, 614, 522, 193, 679, 779, 879, 979, 1079, 497, 719, 819, 919, 1019, 169, 646, 366, 395]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.100 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| MAP@5 | 0.050 |
| R-Precision | 0.100 |
| Latency (ms) | 122.24 |
| Predicted Intent | question |
| Expected Intent | reference |
| Intent Correct | False |

---

### HYBRID — Git tips and tricks

- **Benchmark ID:** 130_tp_832398
- **Difficulty:** easy
- **Challenge:** lexical
- **Relevant Notes:** [130, 135, 144, 169, 229, 272, 317, 328, 366, 395]
- **Retrieved Notes:** [646, 497, 719, 819, 919, 1019, 328, 522, 192, 614, 501, 366, 612, 330, 270, 395, 272, 400, 104, 140]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.143 |
| MAP@5 | 0.000 |
| R-Precision | 0.100 |
| Latency (ms) | 135.39 |
| Predicted Intent | general |
| Expected Intent | reference |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Reference - Git |
| Category Correct | False |

---

### HYBRID — What do I know about RAG systems?

- **Benchmark ID:** 65_tp_3e802c
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [65, 114, 186, 197, 219, 222, 267, 296, 310, 376]
- **Retrieved Notes:** [386, 436, 470, 565, 197, 446, 730, 830, 930, 1030, 595, 485, 600, 310, 625, 510, 492, 222, 70, 74]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.100 |
| Hit | True |
| Reciprocal Rank | 0.200 |
| MAP@5 | 0.020 |
| R-Precision | 0.100 |
| Latency (ms) | 124.60 |
| Predicted Intent | question |
| Expected Intent | study |
| Intent Correct | False |

---

### HYBRID — Retrieval augmented generation notes

- **Benchmark ID:** 65_tp_034576
- **Difficulty:** easy
- **Challenge:** lexical
- **Relevant Notes:** [65, 114, 186, 197, 219, 222, 267, 296, 310, 376]
- **Retrieved Notes:** [65, 186, 398, 184, 289, 86, 487, 523, 486, 702, 802, 902, 1002, 1102, 87, 492, 623, 386, 531, 683]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.200 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.200 |
| R-Precision | 0.200 |
| Latency (ms) | 112.44 |
| Predicted Intent | reference |
| Expected Intent | study |
| Intent Correct | False |

---

### HYBRID — Notes about embeddings and vector search

- **Benchmark ID:** 168_tp_f44ea2
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [168, 183, 228, 289, 298, 323, 376, 486, 487, 523]
- **Retrieved Notes:** [196, 333, 298, 726, 826, 926, 1026, 228, 531, 683, 783, 883, 983, 1083, 66, 648, 64, 492, 289, 323]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.100 |
| Hit | True |
| Reciprocal Rank | 0.333 |
| MAP@5 | 0.033 |
| R-Precision | 0.200 |
| Latency (ms) | 120.15 |
| Predicted Intent | reference |
| Expected Intent | study |
| Intent Correct | False |

---

### HYBRID — Large language model notes and findings

- **Benchmark ID:** 60_tp_438fb0
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [60, 119, 122, 136, 143, 186, 251, 268, 313, 329]
- **Retrieved Notes:** [186, 404, 708, 808, 908, 1008, 1108, 487, 221, 349, 87, 405, 533, 721, 821, 921, 1021, 289, 558, 613]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.100 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.100 |
| R-Precision | 0.100 |
| Latency (ms) | 110.47 |
| Predicted Intent | reference |
| Expected Intent | study |
| Intent Correct | False |

---

### HYBRID — Notes about reranking in search systems

- **Benchmark ID:** 67_tp_248b82
- **Difficulty:** hard
- **Challenge:** semantic
- **Relevant Notes:** [67, 119, 123, 176, 386, 648, 676, 776, 876, 976]
- **Retrieved Notes:** [67, 176, 119, 305, 58, 333, 213, 729, 829, 929, 1029, 252, 696, 796, 896, 996, 1096, 619, 649, 265]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.600 |
| Recall@5 | 0.300 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.300 |
| R-Precision | 0.300 |
| Latency (ms) | 90.44 |
| Predicted Intent | reference |
| Expected Intent | study |
| Intent Correct | False |

---

### HYBRID — RAG and retrieval evaluation metrics

- **Benchmark ID:** 90_tp_bed875
- **Difficulty:** hard
- **Challenge:** multi_hop
- **Relevant Notes:** [90, 119, 310, 402, 485, 487, 595]
- **Retrieved Notes:** [386, 485, 310, 595, 186, 470, 492, 213, 729, 829, 929, 1029, 487, 523, 402, 625, 446, 730, 830, 930]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.600 |
| Recall@5 | 0.429 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| MAP@5 | 0.274 |
| R-Precision | 0.429 |
| Latency (ms) | 620.13 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Study - AI |
| Category Correct | False |

---

### HYBRID — How do I measure retrieval quality?

- **Benchmark ID:** 90_tp_c1f487
- **Difficulty:** hard
- **Challenge:** semantic
- **Relevant Notes:** [90, 119, 210, 310, 402, 485, 487, 595]
- **Retrieved Notes:** [310, 86, 485, 402, 213, 729, 829, 929, 1029, 186, 533, 721, 821, 921, 1021, 184, 623, 142, 65, 595]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.600 |
| Recall@5 | 0.375 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.302 |
| R-Precision | 0.375 |
| Latency (ms) | 92.37 |
| Predicted Intent | question |
| Expected Intent | study |
| Intent Correct | False |

---

### HYBRID — Prompting techniques and tips

- **Benchmark ID:** 130_tp_d166fd
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [130, 191, 264, 268, 406, 436, 446, 456, 467, 493]
- **Retrieved Notes:** [406, 264, 507, 459, 199, 468, 632, 294, 236, 352, 330, 154, 270, 263, 382, 540, 184, 163, 288, 70]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.200 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.200 |
| R-Precision | 0.200 |
| Latency (ms) | 182.54 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Study - AI |
| Category Correct | False |

---

### HYBRID — Caching strategies and implementations

- **Benchmark ID:** 103_tp_bee00a
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [103, 124, 146, 237, 269, 275, 284, 295, 318, 336]
- **Retrieved Notes:** [61, 93, 644, 602, 467, 318, 520, 146, 237, 530, 738, 838, 938, 1038, 124, 579, 736, 836, 936, 1036]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.167 |
| MAP@5 | 0.000 |
| R-Precision | 0.300 |
| Latency (ms) | 181.20 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Study - System Design |
| Category Correct | False |

---

### HYBRID — Message queue and event streaming notes

- **Benchmark ID:** 71_tp_b1348d
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [71, 102, 144, 174, 200, 218, 238, 269, 297, 304]
- **Retrieved Notes:** [450, 671, 771, 871, 971, 1071, 372, 392, 203, 371, 246, 684, 784, 884, 984, 1084, 87, 238, 744, 844]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.056 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 96.08 |
| Predicted Intent | communication |
| Expected Intent | study |
| Intent Correct | False |

---

### HYBRID — System design interview prep notes

- **Benchmark ID:** 70_tp_c5e045
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [70, 145, 255, 267, 305, 309, 334, 344, 346, 360]
- **Retrieved Notes:** [360, 70, 106, 309, 99, 392, 352, 540, 442, 755, 855, 955, 1055, 294, 459, 419, 372, 199, 102, 344]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.600 |
| Recall@5 | 0.300 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.275 |
| R-Precision | 0.300 |
| Latency (ms) | 176.40 |
| Predicted Intent | reference |
| Expected Intent | study |
| Intent Correct | False |

---

### HYBRID — PostgreSQL database notes

- **Benchmark ID:** 58_tp_257a95
- **Difficulty:** medium
- **Challenge:** lexical
- **Relevant Notes:** [58, 66, 74, 104, 139, 144, 168, 175, 215, 267]
- **Retrieved Notes:** [74, 144, 417, 731, 831, 931, 1031, 58, 425, 567, 704, 804, 904, 1004, 1104, 367, 628, 732, 832, 932]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.200 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.200 |
| R-Precision | 0.300 |
| Latency (ms) | 172.52 |
| Predicted Intent | reference |
| Expected Intent | study |
| Intent Correct | False |
| Predicted Category | Reference - PostgreSQL |
| Expected Category | Study - PostgreSQL |
| Category Correct | False |

---

### HYBRID — Redis usage and patterns

- **Benchmark ID:** 61_tp_89afdd
- **Difficulty:** easy
- **Challenge:** lexical
- **Relevant Notes:** [61, 73, 92, 103, 124, 146, 157, 174, 237, 246]
- **Retrieved Notes:** [73, 92, 269, 724, 824, 924, 1024, 61, 643, 673, 773, 873, 973, 1073, 421, 746, 846, 946, 1046, 346]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.200 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.200 |
| R-Precision | 0.300 |
| Latency (ms) | 115.23 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Study - Redis |
| Category Correct | False |

---

### HYBRID — Docker and containerization notes

- **Benchmark ID:** 72_tp_c8e7e1
- **Difficulty:** easy
- **Challenge:** lexical
- **Relevant Notes:** [72, 75, 91, 105, 118, 138, 188, 192, 242, 295]
- **Retrieved Notes:** [72, 105, 192, 75, 491, 722, 822, 922, 1022, 295, 138, 118, 712, 812, 912, 1012, 383, 188, 242, 62]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.800 |
| Recall@5 | 0.400 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.400 |
| R-Precision | 0.500 |
| Latency (ms) | 274.17 |
| Predicted Intent | reference |
| Expected Intent | study |
| Intent Correct | False |
| Predicted Category | Reference - Docker |
| Expected Category | Study - Docker |
| Category Correct | False |

---

### HYBRID — What Docker tips have I collected?

- **Benchmark ID:** 72_tp_808bd0
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [72, 75, 91, 105, 118, 138, 188, 192, 242, 295]
- **Retrieved Notes:** [72, 192, 295, 105, 75, 188, 355, 688, 788, 888, 988, 1088, 491, 722, 822, 922, 1022, 383, 138, 442]

| Metric | Value |
|-------|------:|
| Precision@5 | 1.000 |
| Recall@5 | 0.500 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.500 |
| R-Precision | 0.600 |
| Latency (ms) | 280.09 |
| Predicted Intent | question |
| Expected Intent | reference |
| Intent Correct | False |

---

### HYBRID — FastAPI development notes

- **Benchmark ID:** 68_tp_d59df1
- **Difficulty:** medium
- **Challenge:** lexical
- **Relevant Notes:** [68, 132, 145, 165, 167, 266, 272, 313, 350, 365]
- **Retrieved Notes:** [68, 165, 725, 825, 925, 1025, 471, 663, 763, 863, 963, 1063, 266, 751, 851, 951, 1051, 570, 106, 132]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.200 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.200 |
| R-Precision | 0.200 |
| Latency (ms) | 146.02 |
| Predicted Intent | reference |
| Expected Intent | study |
| Intent Correct | False |

---

### HYBRID — KnowledgeVault project notes

- **Benchmark ID:** 57_tp_c30342
- **Difficulty:** easy
- **Challenge:** lexical
- **Relevant Notes:** [57, 88, 89, 90, 91, 94, 95, 96, 97, 107]
- **Retrieved Notes:** [125, 95, 96, 89, 90, 262, 444, 57, 88, 555, 638, 247, 97, 251, 107, 337, 428, 728, 828, 928]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.800 |
| Recall@5 | 0.400 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| MAP@5 | 0.272 |
| R-Precision | 0.600 |
| Latency (ms) | 196.95 |
| Predicted Intent | reference |
| Expected Intent | reference |
| Intent Correct | True |
| Predicted Category | Reference - Shared |
| Expected Category | Reference - KnowledgeVault |
| Category Correct | True |

---

### HYBRID — What decisions have I made for the KnowledgeVault project?

- **Benchmark ID:** 57_tp_5bc303
- **Difficulty:** medium
- **Challenge:** multi_hop
- **Relevant Notes:** [88, 89, 90, 91, 95, 96, 97]
- **Retrieved Notes:** [638, 90, 428, 728, 828, 928, 1028, 95, 57, 88, 555, 125, 413, 89, 262, 247, 251, 97, 628, 732]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.143 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| MAP@5 | 0.071 |
| R-Precision | 0.143 |
| Latency (ms) | 103.25 |
| Predicted Intent | question |
| Expected Intent | reference |
| Intent Correct | False |

---

### HYBRID — What meetings have I had?

- **Benchmark ID:** 56_tp_7b886e
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [56, 106, 107, 149, 170, 233, 251, 283, 304, 359]
- **Retrieved Notes:** [371, 107, 263, 559, 442, 755, 855, 955, 1055, 438, 448, 203, 288, 233, 609, 57, 175, 185, 382, 540]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.100 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| MAP@5 | 0.050 |
| R-Precision | 0.100 |
| Latency (ms) | 377.10 |
| Predicted Intent | event |
| Expected Intent | event |
| Intent Correct | True |

---

### HYBRID — What are my pending tasks and deadlines?

- **Benchmark ID:** 233_tp_b305bf
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [233]
- **Retrieved Notes:** [498, 453, 233, 647, 235, 268, 289, 554, 586, 682, 782, 882, 982, 1082, 59, 620, 198, 400, 79, 174]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 1.000 |
| Hit | True |
| Reciprocal Rank | 0.333 |
| MAP@5 | 0.333 |
| R-Precision | 0.000 |
| Latency (ms) | 303.04 |
| Predicted Intent | todo |
| Expected Intent | todo |
| Intent Correct | True |
| Predicted Category | Tasks |
| Expected Category | Tasks |
| Category Correct | True |

---

### HYBRID — What health appointments do I have?

- **Benchmark ID:** 78_tp_db66ee
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [78, 79, 109, 157, 201, 210, 212, 226, 231, 355]
- **Retrieved Notes:** [79, 601, 559, 575, 198, 475, 78, 173, 609, 288, 231, 76, 224, 109, 200, 620, 82, 317, 322, 157]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.100 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.100 |
| R-Precision | 0.200 |
| Latency (ms) | 236.92 |
| Predicted Intent | reminder |
| Expected Intent | reminder |
| Intent Correct | True |
| Predicted Category | Appointments |
| Expected Category | Appointments |
| Category Correct | True |

---

### HYBRID — What payments and bills do I need to make?

- **Benchmark ID:** 77_tp_c2ce55
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [77, 120, 126, 128, 131, 137, 140, 144, 160, 162]
- **Retrieved Notes:** [341, 77, 82, 635, 368, 331, 76, 573, 178, 393, 162, 601, 490, 606, 216, 111, 322, 160, 415, 459]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.100 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| MAP@5 | 0.050 |
| R-Precision | 0.100 |
| Latency (ms) | 104.68 |
| Predicted Intent | question |
| Expected Intent | todo |
| Intent Correct | False |

---

### HYBRID — What is on my shopping list?

- **Benchmark ID:** 76_tp_d5a3f9
- **Difficulty:** easy
- **Challenge:** lexical
- **Relevant Notes:** [76, 322]
- **Retrieved Notes:** [393, 322, 606, 115, 76, 475, 605, 216, 202, 82, 358, 602, 267, 229, 690, 790, 890, 990, 1090, 331]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 1.000 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| MAP@5 | 0.450 |
| R-Precision | 0.500 |
| Latency (ms) | 1073.09 |
| Predicted Intent | question |
| Expected Intent | todo |
| Intent Correct | False |

---

### HYBRID — Show all my reminders

- **Benchmark ID:** 55_tp_1c812c
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [55, 152, 212, 312, 542, 557]
- **Retrieved Notes:** [382, 56, 312, 290, 442, 755, 855, 955, 1055, 475, 423, 557, 216, 583, 699, 799, 899, 999, 1099, 348]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.167 |
| Hit | True |
| Reciprocal Rank | 0.333 |
| MAP@5 | 0.056 |
| R-Precision | 0.167 |
| Latency (ms) | 1485.23 |
| Predicted Intent | reminder |
| Expected Intent | reminder |
| Intent Correct | True |
| Predicted Category | Reminders |
| Expected Category | Reminders |
| Category Correct | True |

---

### HYBRID — My budget and expense tracking notes

- **Benchmark ID:** 82_tp_feed7d
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [82, 153, 202, 210, 216, 254, 281, 291, 331, 345]
- **Retrieved Notes:** [82, 216, 606, 393, 285, 341, 87, 459, 403, 115, 77, 202, 178, 535, 444, 331, 312, 583, 699, 799]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.200 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.200 |
| R-Precision | 0.200 |
| Latency (ms) | 90.20 |
| Predicted Intent | reference |
| Expected Intent | todo |
| Intent Correct | False |

---

### HYBRID — My travel plans and notes

- **Benchmark ID:** 81_tp_4afce2
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [81, 115, 126, 128, 130, 171, 175, 176, 178, 186]
- **Retrieved Notes:** [290, 81, 212, 393, 444, 77, 190, 627, 115, 87, 82, 216, 225, 322, 106, 203, 583, 699, 799, 899]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.100 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| MAP@5 | 0.050 |
| R-Precision | 0.200 |
| Latency (ms) | 84.76 |
| Predicted Intent | reference |
| Expected Intent | todo |
| Intent Correct | False |

---

### HYBRID — Fitness and workout notes

- **Benchmark ID:** 173_tp_d9566a
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [173, 185, 202, 232, 246, 291, 317, 380, 392, 433]
- **Retrieved Notes:** [631, 481, 87, 482, 83, 212, 107, 621, 444, 286, 203, 583, 699, 799, 899, 999, 1099, 110, 240, 380]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.050 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 95.28 |
| Predicted Intent | reference |
| Expected Intent | todo |
| Intent Correct | False |

---

### HYBRID — My startup ideas and business notes

- **Benchmark ID:** 85_tp_6a3292
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [85, 86, 117, 120, 125, 128, 131, 134, 143, 157]
- **Retrieved Notes:** [85, 525, 459, 617, 441, 134, 87, 178, 444, 255, 203, 413, 212, 285, 166, 685, 785, 885, 985, 1085]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.100 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.100 |
| R-Precision | 0.200 |
| Latency (ms) | 96.14 |
| Predicted Intent | idea |
| Expected Intent | idea |
| Intent Correct | True |
| Predicted Category | Ideas - AI |
| Expected Category | Ideas - Startups |
| Category Correct | True |

---

### HYBRID — What business ideas have I documented?

- **Benchmark ID:** 85_tp_aeedec
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [85, 86, 117, 120, 125, 128, 131, 134, 143, 157]
- **Retrieved Notes:** [225, 178, 85, 441, 459, 260, 413, 240, 330, 117, 309, 371, 308, 525, 255, 624, 617, 391, 238, 744]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.100 |
| Hit | True |
| Reciprocal Rank | 0.333 |
| MAP@5 | 0.033 |
| R-Precision | 0.200 |
| Latency (ms) | 86.02 |
| Predicted Intent | idea |
| Expected Intent | idea |
| Intent Correct | True |

---

### HYBRID — Things I need to tell Sid

- **Benchmark ID:** 54_tp_6e7d12
- **Difficulty:** easy
- **Challenge:** lexical
- **Relevant Notes:** [54, 55, 56, 57, 117, 187, 203, 220, 225, 247]
- **Retrieved Notes:** [54, 57, 56, 55, 423, 247, 442, 755, 855, 955, 1055, 203, 230, 382, 268, 682, 782, 882, 982, 1082]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.800 |
| Recall@5 | 0.400 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.400 |
| R-Precision | 0.500 |
| Latency (ms) | 618.37 |
| Predicted Intent | communication |
| Expected Intent | communication |
| Intent Correct | True |
| Predicted Category | Communication - Sid |
| Expected Category | Things to Tell Sid |
| Category Correct | True |

---

### HYBRID — Things to discuss with Sid at the next meeting

- **Benchmark ID:** 54_tp_68cb9e
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [54, 55, 56, 57, 117, 187, 203, 220, 225, 247]
- **Retrieved Notes:** [57, 54, 56, 423, 247, 55, 203, 442, 755, 855, 955, 1055, 230, 448, 263, 185, 175, 107, 81, 382]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.800 |
| Recall@5 | 0.400 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.380 |
| R-Precision | 0.600 |
| Latency (ms) | 107.50 |
| Predicted Intent | communication |
| Expected Intent | communication |
| Intent Correct | True |
| Predicted Category | Communication - Sid |
| Expected Category | Things to Tell Sid |
| Category Correct | True |

---

### HYBRID — Message to send to Siddhant about backend

- **Benchmark ID:** 54_tp_a4d45e
- **Difficulty:** medium
- **Challenge:** lexical_gap
- **Relevant Notes:** [54, 55, 56, 57, 117, 187, 203, 220, 225, 247]
- **Retrieved Notes:** [56, 423, 54, 55, 57, 106, 392, 372, 129, 91, 132, 658, 758, 858, 958, 1058, 247, 61, 337, 96]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.800 |
| Recall@5 | 0.400 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.322 |
| R-Precision | 0.400 |
| Latency (ms) | 104.18 |
| Predicted Intent | communication |
| Expected Intent | communication |
| Intent Correct | True |

---

### HYBRID — Reciprocal Rank Fusion

- **Benchmark ID:** 518_tp_583ff7
- **Difficulty:** medium
- **Challenge:** exact_phrase
- **Relevant Notes:** [518, 718, 818, 918, 1018]
- **Retrieved Notes:** [518, 718, 818, 918, 1018, 649, 67, 176, 259, 119, 252, 696, 796, 896, 996, 1096, 590, 305, 321, 707]

| Metric | Value |
|-------|------:|
| Precision@5 | 1.000 |
| Recall@5 | 1.000 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 1.000 |
| R-Precision | 1.000 |
| Latency (ms) | 740.74 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Study - AI |
| Category Correct | False |

---

### HYBRID — Redis vs Kafka — when to use each

- **Benchmark ID:** 1024_tp_8759f9
- **Difficulty:** hard
- **Challenge:** comparison
- **Relevant Notes:** [1024, 771, 773, 520]
- **Retrieved Notes:** [643, 673, 773, 873, 973, 1073, 450, 671, 771, 871, 971, 1071, 73, 269, 724, 824, 924, 1024, 92, 301]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.250 |
| Hit | True |
| Reciprocal Rank | 0.333 |
| MAP@5 | 0.083 |
| R-Precision | 0.250 |
| Latency (ms) | 115.69 |
| Predicted Intent | question |
| Expected Intent | study |
| Intent Correct | False |

---

### HYBRID — Resources for learning backend development

- **Benchmark ID:** 108_tp_d16fba
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [132, 68, 165, 108, 206, 174, 177, 145]
- **Retrieved Notes:** [106, 61, 330, 96, 101, 439, 272, 357, 110, 309, 471, 663, 763, 863, 963, 1063, 452, 155, 360, 95]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 184.09 |
| Predicted Intent | study |
| Expected Intent | study |
| Intent Correct | True |

---

### HYBRID — Notes about Fortran programming

- **Benchmark ID:** 0_tp_6cd1aa
- **Difficulty:** hard
- **Challenge:** negative
- **Relevant Notes:** []
- **Retrieved Notes:** [465, 547, 619, 471, 663, 763, 863, 963, 1063, 566, 710, 810, 910, 1010, 327, 562, 296, 439, 283, 662]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 208.96 |
| Predicted Intent | reference |
| Expected Intent | general |
| Intent Correct | False |

---

### HYBRID — My notes on ancient Roman history

- **Benchmark ID:** 0_tp_b73b18
- **Difficulty:** hard
- **Challenge:** negative
- **Relevant Notes:** []
- **Retrieved Notes:** [290, 565, 583, 699, 799, 899, 999, 1099, 360, 87, 442, 755, 855, 955, 1055, 230, 235, 444, 529, 309]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 136.79 |
| Predicted Intent | reference |
| Expected Intent | general |
| Intent Correct | False |

---

### HYBRID — Cooking recipes I've saved

- **Benchmark ID:** 0_tp_fe75c4
- **Difficulty:** hard
- **Challenge:** negative
- **Relevant Notes:** []
- **Retrieved Notes:** [322, 475, 71, 281, 286, 76, 438, 212, 416, 444, 458, 582, 270, 105, 382, 290, 472, 496, 75, 240]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 166.57 |
| Predicted Intent | general |
| Expected Intent | general |
| Intent Correct | True |
| Predicted Category | General |
| Expected Category | General |
| Category Correct | True |

---

### HYBRID — KnowledgeVault RAG pipeline decisions and findings

- **Benchmark ID:** 1028_tp_65ec5f
- **Difficulty:** hard
- **Challenge:** multi_hop
- **Relevant Notes:** [1030, 1032, 533]
- **Retrieved Notes:** [310, 90, 446, 730, 830, 930, 1030, 638, 96, 428, 728, 828, 928, 1028, 88, 125, 510, 89, 555, 523]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.143 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 103.80 |
| Predicted Intent | general |
| Expected Intent | reference |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Reference - KnowledgeVault |
| Category Correct | False |

---

### HYBRID — What benchmark results have I recorded for KnowledgeVault retrieval?

- **Benchmark ID:** 1028_tp_2e0731
- **Difficulty:** hard
- **Challenge:** multi_hop
- **Relevant Notes:** [1032, 523, 402]
- **Retrieved Notes:** [310, 90, 402, 213, 729, 829, 929, 1029, 88, 96, 251, 89, 523, 595, 555, 430, 262, 485, 186, 86]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.333 |
| Hit | True |
| Reciprocal Rank | 0.333 |
| MAP@5 | 0.111 |
| R-Precision | 0.333 |
| Latency (ms) | 393.43 |
| Predicted Intent | question |
| Expected Intent | reference |
| Intent Correct | False |

---

### HYBRID — What have I been working on this month?

- **Benchmark ID:** 77_tp_d33a9c
- **Difficulty:** hard
- **Challenge:** temporal
- **Relevant Notes:** [149]
- **Retrieved Notes:** [453, 77, 82, 647, 375, 735, 835, 935, 1035, 248, 79, 631, 601, 498, 442, 755, 855, 955, 1055, 175]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 356.55 |
| Predicted Intent | question |
| Expected Intent | general |
| Intent Correct | False |

---

### HYBRID — Recent notes and activities

- **Benchmark ID:** 77_tp_c2c25c
- **Difficulty:** hard
- **Challenge:** temporal
- **Relevant Notes:** [149, 286]
- **Retrieved Notes:** [87, 444, 565, 290, 203, 372, 453, 442, 755, 855, 955, 1055, 583, 699, 799, 899, 999, 1099, 249, 393]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 124.02 |
| Predicted Intent | reference |
| Expected Intent | general |
| Intent Correct | False |

---

### HYBRID — My study notes on AI and machine learning

- **Benchmark ID:** 1026_tp_74f5bc
- **Difficulty:** easy
- **Challenge:** synthesis
- **Relevant Notes:** [1026, 774, 1030, 510, 523, 268, 267, 782]
- **Retrieved Notes:** [529, 230, 87, 619, 85, 416, 122, 444, 617, 333, 528, 235, 309, 439, 357, 360, 60, 565, 166, 685]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 702.66 |
| Predicted Intent | study |
| Expected Intent | study |
| Intent Correct | True |
| Predicted Category | Study - AI |
| Expected Category | Study - AI |
| Category Correct | True |

---

### HYBRID — Messages I need to send Siddhant

- **Benchmark ID:** 54_tp_636e21
- **Difficulty:** easy
- **Challenge:** lexical_gap
- **Relevant Notes:** [54, 55, 56, 57, 117, 187, 203, 220]
- **Retrieved Notes:** [56, 423, 55, 54, 57, 392, 382, 129, 256, 524, 450, 671, 771, 871, 971, 1071, 203, 132, 658, 758]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.800 |
| Recall@5 | 0.500 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.402 |
| R-Precision | 0.500 |
| Latency (ms) | 4686.31 |
| Predicted Intent | general |
| Expected Intent | communication |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Things to Tell Sid |
| Category Correct | False |

---

### HYBRID — Pending conversations with Sid

- **Benchmark ID:** 54_tp_d0b55d
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [54, 55, 56, 57, 117, 187, 203, 220]
- **Retrieved Notes:** [56, 423, 57, 54, 55, 247, 203, 264, 283, 343, 406, 431, 432, 507, 642, 647, 662, 692, 762, 792]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.800 |
| Recall@5 | 0.500 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.402 |
| R-Precision | 0.625 |
| Latency (ms) | 1418.27 |
| Predicted Intent | todo |
| Expected Intent | communication |
| Intent Correct | False |
| Predicted Category | Tasks |
| Expected Category | Things to Tell Sid |
| Category Correct | False |

---

### HYBRID — Notes about Sid and our project discussions

- **Benchmark ID:** 54_tp_e69fe7
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [54, 55, 56, 57, 117, 187, 203, 220]
- **Retrieved Notes:** [57, 56, 423, 247, 54, 55, 442, 755, 855, 955, 1055, 203, 230, 106, 439, 565, 99, 413, 624, 185]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.600 |
| Recall@5 | 0.375 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.325 |
| R-Precision | 0.500 |
| Latency (ms) | 122.39 |
| Predicted Intent | reference |
| Expected Intent | communication |
| Intent Correct | False |

---

### HYBRID — Business concepts I want to explore

- **Benchmark ID:** 85_tp_712892
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [85, 86, 117, 131, 134, 143, 157, 166]
- **Retrieved Notes:** [309, 178, 225, 85, 166, 685, 785, 885, 985, 1085, 617, 102, 117, 360, 555, 459, 71, 308, 468, 262]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.250 |
| Hit | True |
| Reciprocal Rank | 0.250 |
| MAP@5 | 0.081 |
| R-Precision | 0.250 |
| Latency (ms) | 102.87 |
| Predicted Intent | idea |
| Expected Intent | idea |
| Intent Correct | True |
| Predicted Category | Ideas - AI |
| Expected Category | Ideas |
| Category Correct | True |

---

### HYBRID — Product ideas I have noted down

- **Benchmark ID:** 85_tp_46bae2
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [85, 86, 117, 131, 134, 143, 157, 166]
- **Retrieved Notes:** [85, 322, 202, 475, 117, 178, 325, 459, 133, 439, 605, 442, 755, 855, 955, 1055, 175, 225, 382, 97]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.250 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.175 |
| R-Precision | 0.250 |
| Latency (ms) | 130.32 |
| Predicted Intent | idea |
| Expected Intent | idea |
| Intent Correct | True |

---

### HYBRID — Entrepreneurship and venture ideas

- **Benchmark ID:** 85_tp_97280d
- **Difficulty:** medium
- **Challenge:** lexical_gap
- **Relevant Notes:** [85, 86, 117, 131, 134, 143, 157, 166]
- **Retrieved Notes:** [85, 166, 685, 785, 885, 985, 1085, 617, 594, 155, 525, 391, 413, 441, 117, 426, 131, 459, 178, 529]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.250 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.250 |
| R-Precision | 0.250 |
| Latency (ms) | 102.93 |
| Predicted Intent | idea |
| Expected Intent | idea |
| Intent Correct | True |
| Predicted Category | Ideas - AI |
| Expected Category | Ideas |
| Category Correct | True |

---

### HYBRID — Outstanding financial obligations

- **Benchmark ID:** 77_tp_c85047
- **Difficulty:** medium
- **Challenge:** lexical_gap
- **Relevant Notes:** [77, 120, 126, 128, 131, 137, 140, 144]
- **Retrieved Notes:** [82, 341, 411, 210, 635, 77, 162, 393, 637, 733, 833, 933, 1033, 403, 312, 371, 370, 689, 789, 889]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.167 |
| MAP@5 | 0.000 |
| R-Precision | 0.125 |
| Latency (ms) | 108.19 |
| Predicted Intent | general |
| Expected Intent | todo |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Bills |
| Category Correct | False |

---

### HYBRID — Payments I still need to make

- **Benchmark ID:** 77_tp_573aa5
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [77, 120, 126, 128, 131, 137, 140, 144]
- **Retrieved Notes:** [341, 635, 160, 312, 331, 77, 369, 626, 368, 411, 573, 162, 539, 393, 103, 490, 80, 76, 178, 399]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.167 |
| MAP@5 | 0.000 |
| R-Precision | 0.125 |
| Latency (ms) | 280.77 |
| Predicted Intent | general |
| Expected Intent | todo |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Bills |
| Category Correct | False |

---

### HYBRID — Monthly expenses and dues

- **Benchmark ID:** 77_tp_e477f7
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [77, 120, 126, 128, 131, 137, 140, 144]
- **Retrieved Notes:** [82, 341, 216, 635, 490, 601, 368, 535, 393, 77, 281, 403, 606, 411, 79, 331, 573, 210, 312, 115]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.100 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 97.51 |
| Predicted Intent | general |
| Expected Intent | todo |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Bills |
| Category Correct | False |

---

### HYBRID — Medical appointments on my calendar

- **Benchmark ID:** 78_tp_c31b3d
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [78, 79, 109, 157, 201, 210, 212, 226]
- **Retrieved Notes:** [79, 559, 601, 198, 78, 56, 231, 620, 575, 448, 609, 54, 175, 70, 351, 111, 224, 216, 59, 617]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.250 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.175 |
| R-Precision | 0.250 |
| Latency (ms) | 91.01 |
| Predicted Intent | reminder |
| Expected Intent | todo |
| Intent Correct | False |
| Predicted Category | Reminders |
| Expected Category | To Do |
| Category Correct | False |

---

### HYBRID — Healthcare and wellness reminders

- **Benchmark ID:** 78_tp_d52f8d
- **Difficulty:** easy
- **Challenge:** lexical_gap
- **Relevant Notes:** [78, 79, 109, 157, 201, 210, 212, 226]
- **Retrieved Notes:** [79, 475, 317, 601, 557, 575, 322, 392, 56, 201, 442, 755, 855, 955, 1055, 355, 688, 788, 888, 988]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.125 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.125 |
| R-Precision | 0.125 |
| Latency (ms) | 90.20 |
| Predicted Intent | reminder |
| Expected Intent | reminder |
| Intent Correct | True |
| Predicted Category | Appointments |
| Expected Category | Appointments |
| Category Correct | True |

---

### HYBRID — In-memory datastore behavior notes

- **Benchmark ID:** 61_tp_0bc3d9
- **Difficulty:** medium
- **Challenge:** lexical_gap
- **Relevant Notes:** [61, 73, 92, 103, 157, 174, 269, 303]
- **Retrieved Notes:** [275, 706, 806, 906, 1006, 1106, 219, 146, 644, 537, 364, 661, 761, 861, 961, 1061, 303, 579, 736, 836]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.059 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 736.68 |
| Predicted Intent | reference |
| Expected Intent | study |
| Intent Correct | False |

---

### HYBRID — Cache eviction policy details

- **Benchmark ID:** 61_tp_d58d06
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [61, 73, 92, 103, 157, 174, 269, 303]
- **Retrieved Notes:** [103, 520, 318, 467, 534, 61, 644, 579, 736, 836, 936, 1036, 93, 275, 706, 806, 906, 1006, 1106, 146]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.125 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.125 |
| R-Precision | 0.250 |
| Latency (ms) | 579.01 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Study - Redis |
| Category Correct | False |

---

### HYBRID — Team meetings I have attended

- **Benchmark ID:** 56_tp_3888f9
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [56, 106, 107, 149, 170, 233, 251, 283]
- **Retrieved Notes:** [107, 263, 371, 448, 294, 438, 141, 81, 352, 125, 609, 382, 54, 423, 149, 185, 56, 233, 106, 540]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.125 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.125 |
| R-Precision | 0.125 |
| Latency (ms) | 256.10 |
| Predicted Intent | event |
| Expected Intent | event |
| Intent Correct | True |

---

### HYBRID — Sprint retrospective and planning notes

- **Benchmark ID:** 56_tp_b7d172
- **Difficulty:** easy
- **Challenge:** lexical_gap
- **Relevant Notes:** [56, 106, 107, 149, 170, 233, 251, 283]
- **Retrieved Notes:** [107, 203, 466, 372, 82, 106, 294, 212, 498, 142, 617, 290, 100, 620, 539, 565, 263, 87, 344, 352]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.125 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.125 |
| R-Precision | 0.250 |
| Latency (ms) | 94.89 |
| Predicted Intent | reference |
| Expected Intent | event |
| Intent Correct | False |

---

### HYBRID — Sync notes with the team

- **Benchmark ID:** 56_tp_1162c8
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [56, 106, 107, 149, 170, 233, 251, 283]
- **Retrieved Notes:** [372, 203, 87, 149, 444, 125, 604, 637, 733, 833, 933, 1033, 106, 620, 141, 249, 364, 661, 761, 861]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.125 |
| Hit | True |
| Reciprocal Rank | 0.250 |
| MAP@5 | 0.031 |
| R-Precision | 0.125 |
| Latency (ms) | 91.85 |
| Predicted Intent | reference |
| Expected Intent | meeting |
| Intent Correct | False |
| Predicted Category | Reference - Shared |
| Expected Category | Meetings |
| Category Correct | False |

---

### HYBRID — Weekly standup summaries

- **Benchmark ID:** 56_tp_59ba00
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [56, 106, 107, 149, 170, 233, 251, 283]
- **Retrieved Notes:** [107, 87, 453, 565, 438, 230, 240, 631, 375, 735, 835, 935, 1035, 419, 360, 619, 525, 439, 398, 469]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.125 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.125 |
| R-Precision | 0.125 |
| Latency (ms) | 89.72 |
| Predicted Intent | general |
| Expected Intent | meeting |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Meetings |
| Category Correct | False |

---

### HYBRID — KnowledgeVault project milestones and deliverables

- **Benchmark ID:** 57_tp_d91b61
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [57, 88, 89, 90, 91, 94, 95, 96]
- **Retrieved Notes:** [125, 90, 638, 95, 88, 57, 96, 428, 728, 828, 928, 1028, 89, 555, 107, 262, 251, 337, 97, 413]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.600 |
| Recall@5 | 0.375 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| MAP@5 | 0.200 |
| R-Precision | 0.625 |
| Latency (ms) | 112.99 |
| Predicted Intent | general |
| Expected Intent | project |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Projects |
| Category Correct | False |

---

### HYBRID — What is the architecture of my main project?

- **Benchmark ID:** 57_tp_92649a
- **Difficulty:** hard
- **Challenge:** multi_hop
- **Relevant Notes:** [57, 88, 89, 90, 91, 95, 96]
- **Retrieved Notes:** [106, 95, 392, 102, 602, 175, 62, 178, 117, 57, 439, 141, 169, 413, 156, 360, 532, 255, 231, 116]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.143 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| MAP@5 | 0.071 |
| R-Precision | 0.143 |
| Latency (ms) | 85.26 |
| Predicted Intent | question |
| Expected Intent | project |
| Intent Correct | False |

---

### HYBRID — Current sprint goals for KnowledgeVault

- **Benchmark ID:** 57_tp_74e120
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [57, 88, 89, 90, 91, 94, 95, 96]
- **Retrieved Notes:** [107, 90, 125, 89, 251, 428, 728, 828, 928, 1028, 555, 262, 638, 628, 732, 832, 932, 1032, 57, 337]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.250 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| MAP@5 | 0.125 |
| R-Precision | 0.250 |
| Latency (ms) | 113.05 |
| Predicted Intent | general |
| Expected Intent | project |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Projects |
| Category Correct | False |

---

### HYBRID — Capstone project tasks and status

- **Benchmark ID:** 175_tp_9c7eb5
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [175, 190, 199, 225, 233, 263, 285, 382]
- **Retrieved Notes:** [498, 233, 175, 568, 607, 753, 853, 953, 1053, 453, 653, 263, 382, 190, 575, 540, 203, 580, 442, 755]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.250 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| MAP@5 | 0.146 |
| R-Precision | 0.250 |
| Latency (ms) | 132.68 |
| Predicted Intent | todo |
| Expected Intent | project |
| Intent Correct | False |
| Predicted Category | Tasks |
| Expected Category | Projects |
| Category Correct | False |

---

### HYBRID — University project submission deadlines

- **Benchmark ID:** 175_tp_c51da4
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [175, 190, 199, 225, 233, 263, 285, 382]
- **Retrieved Notes:** [233, 498, 506, 411, 620, 453, 607, 753, 853, 953, 1053, 524, 521, 344, 635, 466, 528, 611, 403, 626]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.125 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.125 |
| R-Precision | 0.125 |
| Latency (ms) | 337.35 |
| Predicted Intent | general |
| Expected Intent | project |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Projects |
| Category Correct | False |

---

### HYBRID — My personal reflections and journal entries

- **Benchmark ID:** 113_tp_6bba32
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [113, 149, 152, 162, 166, 191]
- **Retrieved Notes:** [472, 290, 550, 700, 800, 900, 1000, 1100, 565, 234, 485, 413, 230, 442, 755, 855, 955, 1055, 506, 267]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 197.65 |
| Predicted Intent | general |
| Expected Intent | general |
| Intent Correct | True |
| Predicted Category | General |
| Expected Category | General |
| Category Correct | True |

---

### HYBRID — What did I realize recently?

- **Benchmark ID:** 113_tp_ff1a3d
- **Difficulty:** hard
- **Challenge:** semantic
- **Relevant Notes:** [113, 149, 152, 162, 166, 191]
- **Retrieved Notes:** [505, 458, 583, 699, 799, 899, 999, 1099, 647, 428, 728, 828, 928, 1028, 376, 290, 591, 77, 615, 291]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 173.21 |
| Predicted Intent | question |
| Expected Intent | general |
| Intent Correct | False |

---

### HYBRID — Insights I've been writing down

- **Benchmark ID:** 113_tp_be2de4
- **Difficulty:** medium
- **Challenge:** lexical_gap
- **Relevant Notes:** [113, 149, 152, 162, 166, 191]
- **Retrieved Notes:** [290, 235, 583, 699, 799, 899, 999, 1099, 550, 700, 800, 900, 1000, 1100, 212, 586, 416, 472, 428, 728]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 174.09 |
| Predicted Intent | general |
| Expected Intent | general |
| Intent Correct | True |
| Predicted Category | General |
| Expected Category | General |
| Category Correct | True |

---

### HYBRID — My career goals and direction notes

- **Benchmark ID:** 56_tp_f28e5b
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [56, 61, 91, 96, 101, 106, 114, 155]
- **Retrieved Notes:** [166, 685, 785, 885, 985, 1085, 272, 290, 428, 728, 828, 928, 1028, 413, 107, 212, 539, 416, 277, 550]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 126.14 |
| Predicted Intent | reference |
| Expected Intent | general |
| Intent Correct | False |

---

### HYBRID — Long-term professional planning notes

- **Benchmark ID:** 56_tp_e42aaa
- **Difficulty:** hard
- **Challenge:** lexical_gap
- **Relevant Notes:** [56, 61, 91, 96, 101, 106, 114, 155]
- **Retrieved Notes:** [107, 617, 212, 87, 601, 203, 82, 528, 290, 539, 415, 416, 438, 565, 106, 100, 240, 352, 459, 498]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.067 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 120.76 |
| Predicted Intent | reference |
| Expected Intent | general |
| Intent Correct | False |

---

### HYBRID — Time management and focus techniques

- **Benchmark ID:** 85_tp_c33ed2
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [85, 199, 224, 240, 248, 286, 429, 453]
- **Retrieved Notes:** [240, 248, 565, 521, 224, 438, 348, 664, 764, 864, 964, 1064, 223, 175, 279, 550, 700, 800, 900, 1000]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.600 |
| Recall@5 | 0.375 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.325 |
| R-Precision | 0.375 |
| Latency (ms) | 139.38 |
| Predicted Intent | general |
| Expected Intent | reference |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Reference - Productivity |
| Category Correct | False |

---

### HYBRID — Notes on staying productive while studying

- **Benchmark ID:** 85_tp_a94724
- **Difficulty:** medium
- **Challenge:** lexical_gap
- **Relevant Notes:** [85, 199, 224, 240, 248, 286, 429, 453]
- **Retrieved Notes:** [240, 380, 680, 780, 880, 980, 1080, 496, 356, 434, 617, 482, 583, 699, 799, 899, 999, 1099, 277, 235]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.125 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.125 |
| R-Precision | 0.125 |
| Latency (ms) | 106.74 |
| Predicted Intent | reference |
| Expected Intent | reference |
| Intent Correct | True |

---

### HYBRID — FastAPI route and dependency injection notes

- **Benchmark ID:** 68_tp_025916
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [68, 120, 132, 145, 153, 165, 167, 169]
- **Retrieved Notes:** [68, 165, 725, 825, 925, 1025, 132, 658, 758, 858, 958, 1058, 471, 663, 763, 863, 963, 1063, 189, 697]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.250 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.250 |
| R-Precision | 0.375 |
| Latency (ms) | 89.27 |
| Predicted Intent | reference |
| Expected Intent | reference |
| Intent Correct | True |

---

### HYBRID — Python web framework notes for FastAPI

- **Benchmark ID:** 68_tp_f99196
- **Difficulty:** easy
- **Challenge:** lexical_gap
- **Relevant Notes:** [68, 120, 132, 145, 153, 165, 167, 169]
- **Retrieved Notes:** [471, 663, 763, 863, 963, 1063, 266, 751, 851, 951, 1051, 68, 633, 563, 165, 725, 825, 925, 1025, 304]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.083 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 89.16 |
| Predicted Intent | reference |
| Expected Intent | study |
| Intent Correct | False |

---

### HYBRID — API endpoint design patterns in FastAPI

- **Benchmark ID:** 68_tp_9b1c89
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [68, 120, 132, 145, 153, 165, 167, 169]
- **Retrieved Notes:** [68, 165, 725, 825, 925, 1025, 189, 697, 797, 897, 997, 1097, 132, 658, 758, 858, 958, 1058, 570, 93]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.250 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.250 |
| R-Precision | 0.250 |
| Latency (ms) | 101.19 |
| Predicted Intent | general |
| Expected Intent | reference |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Reference - KnowledgeVault Backend |
| Category Correct | False |

---

### HYBRID — SQLAlchemy ORM usage patterns

- **Benchmark ID:** 55_tp_fbaf81
- **Difficulty:** medium
- **Challenge:** lexical
- **Relevant Notes:** [55, 58, 69, 85, 98, 123, 129, 132]
- **Retrieved Notes:** [69, 206, 363, 365, 694, 794, 894, 994, 1094, 394, 723, 823, 923, 1023, 589, 659, 759, 859, 959, 1059]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.125 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.125 |
| R-Precision | 0.125 |
| Latency (ms) | 105.60 |
| Predicted Intent | general |
| Expected Intent | reference |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Reference - KnowledgeVault Backend |
| Category Correct | False |

---

### HYBRID — Database session management in Python

- **Benchmark ID:** 55_tp_e342eb
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [55, 58, 69, 85, 98, 123, 129, 132]
- **Retrieved Notes:** [365, 694, 794, 894, 994, 1094, 483, 657, 757, 857, 957, 1057, 206, 633, 69, 435, 508, 544, 284, 589]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.067 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 109.76 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Study - FastAPI |
| Category Correct | False |

---

### HYBRID — How do I fix N+1 query problems?

- **Benchmark ID:** 55_tp_d34490
- **Difficulty:** hard
- **Challenge:** semantic
- **Relevant Notes:** [55, 58, 69, 85, 98, 123, 129, 132]
- **Retrieved Notes:** [589, 659, 759, 859, 959, 1059, 259, 385, 300, 754, 854, 954, 1054, 184, 58, 398, 430, 363, 94, 134]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.067 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 132.16 |
| Predicted Intent | todo |
| Expected Intent | question |
| Intent Correct | False |
| Predicted Category | Tasks |
| Expected Category | Questions |
| Category Correct | False |

---

### HYBRID — pgvector setup and index configuration

- **Benchmark ID:** 66_tp_9be255
- **Difficulty:** hard
- **Challenge:** lexical
- **Relevant Notes:** [66, 168, 215, 298, 323, 337, 367, 500]
- **Retrieved Notes:** [66, 323, 742, 842, 942, 1042, 500, 672, 772, 872, 972, 1072, 58, 417, 731, 831, 931, 1031, 280, 168]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.250 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.250 |
| R-Precision | 0.375 |
| Latency (ms) | 114.42 |
| Predicted Intent | general |
| Expected Intent | reference |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Reference - PostgreSQL |
| Category Correct | False |

---

### HYBRID — Vector similarity search configuration

- **Benchmark ID:** 66_tp_72bd4f
- **Difficulty:** hard
- **Challenge:** semantic
- **Relevant Notes:** [66, 168, 215, 298, 323, 337, 367, 500]
- **Retrieved Notes:** [333, 66, 168, 252, 696, 796, 896, 996, 1096, 67, 298, 726, 826, 926, 1026, 215, 681, 781, 881, 981]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.250 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| MAP@5 | 0.146 |
| R-Precision | 0.250 |
| Latency (ms) | 118.67 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Study - AI |
| Category Correct | False |

---

### HYBRID — Algorithm and data structure study notes

- **Benchmark ID:** 59_tp_a4350a
- **Difficulty:** medium
- **Challenge:** lexical
- **Relevant Notes:** [59, 60, 182, 204, 215, 224, 244, 247]
- **Retrieved Notes:** [354, 66, 545, 60, 465, 530, 738, 838, 938, 1038, 619, 215, 681, 781, 881, 981, 1081, 204, 219, 261]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.125 |
| Hit | True |
| Reciprocal Rank | 0.250 |
| MAP@5 | 0.031 |
| R-Precision | 0.125 |
| Latency (ms) | 160.45 |
| Predicted Intent | study |
| Expected Intent | study |
| Intent Correct | True |

---

### HYBRID — Competitive programming problem patterns

- **Benchmark ID:** 59_tp_a3126e
- **Difficulty:** hard
- **Challenge:** semantic
- **Relevant Notes:** [59, 60, 182, 204, 215, 224, 244, 247]
- **Retrieved Notes:** [302, 460, 701, 801, 901, 1001, 1101, 117, 562, 204, 265, 327, 566, 710, 810, 910, 1010, 60, 529, 504]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.100 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 159.79 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Study - Algorithms |
| Category Correct | False |

---

### HYBRID — How do I solve graph traversal problems?

- **Benchmark ID:** 59_tp_fe7b32
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [59, 60, 182, 204, 215, 224, 244, 247]
- **Retrieved Notes:** [60, 545, 204, 342, 667, 767, 867, 967, 1067, 536, 639, 215, 681, 781, 881, 981, 1081, 347, 668, 768]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.250 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.208 |
| R-Precision | 0.250 |
| Latency (ms) | 91.42 |
| Predicted Intent | question |
| Expected Intent | question |
| Intent Correct | True |

---

### HYBRID — Operating systems exam preparation notes

- **Benchmark ID:** 59_tp_652a70
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [59, 132, 141, 146, 174, 179, 203, 205]
- **Retrieved Notes:** [59, 360, 70, 309, 527, 343, 593, 465, 629, 547, 419, 442, 755, 855, 955, 1055, 352, 99, 106, 540]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.125 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.125 |
| R-Precision | 0.125 |
| Latency (ms) | 95.06 |
| Predicted Intent | reference |
| Expected Intent | study |
| Intent Correct | False |

---

### HYBRID — CPU scheduling algorithms I need to know

- **Benchmark ID:** 59_tp_566c28
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [59, 132, 141, 146, 174, 179, 203, 205]
- **Retrieved Notes:** [179, 566, 710, 810, 910, 1010, 59, 634, 698, 798, 898, 998, 1098, 629, 516, 711, 811, 911, 1011, 283]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.125 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.125 |
| R-Precision | 0.250 |
| Latency (ms) | 175.91 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Study - Operating Systems |
| Category Correct | False |

---

### HYBRID — Computer networking concepts for university

- **Benchmark ID:** 75_tp_eae57f
- **Difficulty:** medium
- **Challenge:** lexical
- **Relevant Notes:** [75, 118, 159, 162, 168, 180, 237, 276]
- **Retrieved Notes:** [327, 532, 491, 722, 822, 922, 1022, 633, 343, 99, 178, 439, 106, 62, 516, 711, 811, 911, 1011, 527]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 93.15 |
| Predicted Intent | idea |
| Expected Intent | study |
| Intent Correct | False |

---

### HYBRID — TCP/IP and HTTP protocol notes

- **Benchmark ID:** 75_tp_ac0c4f
- **Difficulty:** easy
- **Challenge:** lexical
- **Relevant Notes:** [75, 118, 159, 162, 168, 180, 237, 276]
- **Retrieved Notes:** [633, 654, 532, 159, 350, 75, 327, 189, 697, 797, 897, 997, 1097, 449, 408, 526, 714, 814, 914, 1014]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.125 |
| Hit | True |
| Reciprocal Rank | 0.250 |
| MAP@5 | 0.031 |
| R-Precision | 0.250 |
| Latency (ms) | 95.07 |
| Predicted Intent | reference |
| Expected Intent | study |
| Intent Correct | False |

---

### HYBRID — Kubernetes cluster management notes

- **Benchmark ID:** 62_tp_d2020d
- **Difficulty:** medium
- **Challenge:** lexical
- **Relevant Notes:** [62, 118, 181, 230, 383, 410, 419, 548]
- **Retrieved Notes:** [62, 118, 712, 812, 912, 1012, 410, 383, 439, 566, 710, 810, 910, 1010, 392, 346, 608, 107, 106, 203]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.250 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.250 |
| R-Precision | 0.500 |
| Latency (ms) | 100.04 |
| Predicted Intent | reference |
| Expected Intent | study |
| Intent Correct | False |

---

### HYBRID — Container orchestration with K8s

- **Benchmark ID:** 62_tp_9d6d2c
- **Difficulty:** hard
- **Challenge:** lexical_gap
- **Relevant Notes:** [62, 118, 181, 230, 383, 410, 419, 548]
- **Retrieved Notes:** [62, 383, 75, 118, 712, 812, 912, 1012, 105, 91, 72, 192, 138, 519, 739, 839, 939, 1039, 295, 410]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.600 |
| Recall@5 | 0.375 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.344 |
| R-Precision | 0.375 |
| Latency (ms) | 106.51 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Study - Kubernetes |
| Category Correct | False |

---

### HYBRID — Authentication and JWT token notes

- **Benchmark ID:** 63_tp_d8d22b
- **Difficulty:** medium
- **Challenge:** lexical
- **Relevant Notes:** [63, 129, 165, 189, 227, 244, 276, 287]
- **Retrieved Notes:** [63, 541, 743, 843, 943, 1043, 408, 637, 733, 833, 933, 1033, 454, 604, 110, 372, 431, 569, 285, 493]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.125 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.125 |
| R-Precision | 0.125 |
| Latency (ms) | 73.42 |
| Predicted Intent | reference |
| Expected Intent | study |
| Intent Correct | False |

---

### HYBRID — How does OAuth 2.0 work?

- **Benchmark ID:** 63_tp_6690cb
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [63, 129, 165, 189, 227, 244, 276, 287]
- **Retrieved Notes:** [408, 63, 189, 697, 797, 897, 997, 1097, 541, 743, 843, 943, 1043, 191, 350, 569, 449, 178, 244, 431]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.250 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| MAP@5 | 0.146 |
| R-Precision | 0.250 |
| Latency (ms) | 91.01 |
| Predicted Intent | question |
| Expected Intent | question |
| Intent Correct | True |

---

### HYBRID — What eviction policies does Redis support?

- **Benchmark ID:** 61_tp_217848
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [61, 73, 92, 103, 124, 146, 157, 169]
- **Retrieved Notes:** [103, 73, 643, 673, 773, 873, 973, 1073, 92, 433, 705, 805, 905, 1005, 1105, 61, 346, 534, 421, 746]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.250 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.250 |
| R-Precision | 0.250 |
| Latency (ms) | 93.04 |
| Predicted Intent | question |
| Expected Intent | question |
| Intent Correct | True |

---

### HYBRID — What types of indexes does PostgreSQL support?

- **Benchmark ID:** 58_tp_3d1edd
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [58, 66, 74, 104, 113, 114, 136, 139]
- **Retrieved Notes:** [104, 417, 731, 831, 931, 1031, 58, 66, 74, 280, 139, 686, 786, 886, 986, 1086, 567, 704, 804, 904]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.125 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.125 |
| R-Precision | 0.375 |
| Latency (ms) | 170.29 |
| Predicted Intent | question |
| Expected Intent | question |
| Intent Correct | True |

---

### HYBRID — When should I use GIN vs B-tree indexes?

- **Benchmark ID:** 58_tp_7b89c1
- **Difficulty:** hard
- **Challenge:** comparison
- **Relevant Notes:** [58, 66, 74, 104, 139]
- **Retrieved Notes:** [139, 686, 786, 886, 986, 1086, 301, 417, 731, 831, 931, 1031, 58, 650, 104, 300, 754, 854, 954, 1054]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.200 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.200 |
| R-Precision | 0.200 |
| Latency (ms) | 97.43 |
| Predicted Intent | question |
| Expected Intent | question |
| Intent Correct | True |

---

### HYBRID — How does retrieval augmented generation work?

- **Benchmark ID:** 65_tp_d64f03
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [65, 114, 186, 197, 219, 222, 267, 296]
- **Retrieved Notes:** [65, 184, 186, 398, 119, 310, 140, 623, 523, 613, 176, 644, 486, 702, 802, 902, 1002, 1102, 86, 533]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.250 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.208 |
| R-Precision | 0.250 |
| Latency (ms) | 96.87 |
| Predicted Intent | question |
| Expected Intent | question |
| Intent Correct | True |

---

### HYBRID — What are the steps in a RAG pipeline?

- **Benchmark ID:** 65_tp_0a59fb
- **Difficulty:** hard
- **Challenge:** semantic
- **Relevant Notes:** [65, 114, 186, 197, 219, 222, 267, 296]
- **Retrieved Notes:** [446, 730, 830, 930, 1030, 169, 612, 386, 600, 470, 602, 147, 197, 222, 436, 485, 74, 595, 119, 334]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.077 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 222.24 |
| Predicted Intent | question |
| Expected Intent | question |
| Intent Correct | True |

---

### HYBRID — How are text embeddings generated?

- **Benchmark ID:** 168_tp_cc9fa1
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [168, 183, 228, 289, 298, 323, 376, 486]
- **Retrieved Notes:** [298, 726, 826, 926, 1026, 196, 531, 683, 783, 883, 983, 1083, 492, 289, 376, 648, 378, 221, 446, 730]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.125 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.125 |
| R-Precision | 0.125 |
| Latency (ms) | 91.59 |
| Predicted Intent | question |
| Expected Intent | question |
| Intent Correct | True |

---

### HYBRID — What is the difference between semantic and keyword search?

- **Benchmark ID:** 168_tp_df38ac
- **Difficulty:** hard
- **Challenge:** semantic
- **Relevant Notes:** [168, 183, 228, 289, 298, 323, 376, 486]
- **Retrieved Notes:** [86, 89, 252, 696, 796, 896, 996, 1096, 486, 702, 802, 902, 1002, 1102, 289, 625, 213, 729, 829, 929]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.111 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 82.51 |
| Predicted Intent | question |
| Expected Intent | question |
| Intent Correct | True |

---

### HYBRID — What is due this week?

- **Benchmark ID:** 184_tp_c5a4df
- **Difficulty:** medium
- **Challenge:** temporal
- **Relevant Notes:** [233, 368, 498]
- **Retrieved Notes:** [77, 341, 423, 453, 393, 198, 216, 375, 735, 835, 935, 1035, 442, 755, 855, 955, 1055, 411, 448, 79]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 89.78 |
| Predicted Intent | question |
| Expected Intent | todo |
| Intent Correct | False |

---

### HYBRID — Upcoming deadlines and submission dates

- **Benchmark ID:** 184_tp_cf679c
- **Difficulty:** medium
- **Challenge:** temporal
- **Relevant Notes:** [233, 368, 498]
- **Retrieved Notes:** [233, 498, 506, 411, 607, 753, 853, 953, 1053, 453, 539, 620, 524, 559, 198, 79, 528, 343, 351, 56]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.667 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.667 |
| R-Precision | 0.667 |
| Latency (ms) | 187.33 |
| Predicted Intent | general |
| Expected Intent | todo |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Tasks |
| Category Correct | False |

---

### HYBRID — Tasks I need to complete before month end

- **Benchmark ID:** 184_tp_96ea32
- **Difficulty:** hard
- **Challenge:** temporal
- **Relevant Notes:** [233, 368, 498]
- **Retrieved Notes:** [79, 82, 601, 498, 100, 453, 506, 524, 647, 175, 343, 162, 283, 573, 631, 642, 662, 762, 862, 962]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.333 |
| Hit | True |
| Reciprocal Rank | 0.250 |
| MAP@5 | 0.083 |
| R-Precision | 0.000 |
| Latency (ms) | 191.40 |
| Predicted Intent | todo |
| Expected Intent | todo |
| Intent Correct | True |
| Predicted Category | Tasks |
| Expected Category | Tasks |
| Category Correct | True |

---

### HYBRID — What appointments have I booked this month?

- **Benchmark ID:** 78_tp_63adc1
- **Difficulty:** medium
- **Challenge:** temporal
- **Relevant Notes:** [78, 559]
- **Retrieved Notes:** [559, 79, 620, 601, 198, 216, 78, 609, 393, 82, 538, 448, 351, 57, 175, 224, 331, 107, 77, 341]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.500 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.500 |
| R-Precision | 0.500 |
| Latency (ms) | 104.24 |
| Predicted Intent | reminder |
| Expected Intent | reminder |
| Intent Correct | True |
| Predicted Category | Reminders |
| Expected Category | Appointments |
| Category Correct | False |

---

### HYBRID — My upcoming travel and trip bookings

- **Benchmark ID:** 78_tp_a0f1d8
- **Difficulty:** easy
- **Challenge:** temporal
- **Relevant Notes:** [78, 81, 115]
- **Retrieved Notes:** [538, 627, 81, 539, 407, 128, 190, 115, 216, 393, 82, 343, 635, 607, 753, 853, 953, 1053, 160, 331]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.333 |
| Hit | True |
| Reciprocal Rank | 0.333 |
| MAP@5 | 0.111 |
| R-Precision | 0.333 |
| Latency (ms) | 167.61 |
| Predicted Intent | general |
| Expected Intent | todo |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Travel |
| Category Correct | False |

---

### HYBRID — Transport and accommodation I need to arrange

- **Benchmark ID:** 78_tp_219ffa
- **Difficulty:** medium
- **Challenge:** lexical_gap
- **Relevant Notes:** [78, 81, 115, 126, 128, 130, 160, 171]
- **Retrieved Notes:** [577, 538, 115, 128, 407, 606, 535, 190, 635, 393, 137, 627, 81, 524, 573, 200, 216, 225, 281, 175]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.250 |
| Hit | True |
| Reciprocal Rank | 0.333 |
| MAP@5 | 0.104 |
| R-Precision | 0.250 |
| Latency (ms) | 397.49 |
| Predicted Intent | general |
| Expected Intent | todo |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Travel |
| Category Correct | False |

---

### HYBRID — Redis vs PostgreSQL — when to use each for persistence?

- **Benchmark ID:** 103_tp_7520ad
- **Difficulty:** hard
- **Challenge:** comparison
- **Relevant Notes:** [103, 104, 73, 74, 58, 92, 61]
- **Retrieved Notes:** [73, 61, 269, 724, 824, 924, 1024, 643, 673, 773, 873, 973, 1073, 144, 602, 628, 732, 832, 932, 1032]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.286 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.286 |
| R-Precision | 0.286 |
| Latency (ms) | 595.86 |
| Predicted Intent | question |
| Expected Intent | study |
| Intent Correct | False |

---

### HYBRID — Docker vs Kubernetes — what is the difference?

- **Benchmark ID:** 72_tp_807260
- **Difficulty:** hard
- **Challenge:** comparison
- **Relevant Notes:** [118, 62, 383]
- **Retrieved Notes:** [118, 712, 812, 912, 1012, 105, 62, 383, 491, 722, 822, 922, 1022, 72, 242, 192, 75, 138, 295, 445]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.333 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.333 |
| R-Precision | 0.333 |
| Latency (ms) | 227.31 |
| Predicted Intent | question |
| Expected Intent | study |
| Intent Correct | False |

---

### HYBRID — How do I decide between hybrid retrieval and cross-encoder reranking?

- **Benchmark ID:** 65_tp_205f1c
- **Difficulty:** hard
- **Challenge:** multi_hop
- **Relevant Notes:** [67, 176, 119, 88, 123]
- **Retrieved Notes:** [67, 123, 676, 776, 876, 976, 1076, 119, 176, 252, 696, 796, 896, 996, 1096, 486, 702, 802, 902, 1002]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.400 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.400 |
| R-Precision | 0.400 |
| Latency (ms) | 86.66 |
| Predicted Intent | question |
| Expected Intent | study |
| Intent Correct | False |

---

### HYBRID — What have I documented about retrieval quality in KnowledgeVault?

- **Benchmark ID:** 89_tp_0f29db
- **Difficulty:** hard
- **Challenge:** multi_hop
- **Relevant Notes:** [89, 485, 487, 402, 595, 88, 90]
- **Retrieved Notes:** [90, 310, 88, 555, 86, 89, 96, 251, 523, 186, 213, 729, 829, 929, 1029, 428, 728, 828, 928, 1028]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.286 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.238 |
| R-Precision | 0.429 |
| Latency (ms) | 98.98 |
| Predicted Intent | question |
| Expected Intent | reference |
| Intent Correct | False |

---

### HYBRID — All my university and course study notes

- **Benchmark ID:** 58_tp_32b5cf
- **Difficulty:** easy
- **Challenge:** synthesis
- **Relevant Notes:** [58, 61, 62, 66, 69, 122, 130, 131]
- **Retrieved Notes:** [444, 290, 583, 699, 799, 899, 999, 1099, 285, 203, 343, 403, 212, 87, 442, 755, 855, 955, 1055, 415]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 201.58 |
| Predicted Intent | study |
| Expected Intent | study |
| Intent Correct | True |

---

### HYBRID — All my brainstorming and ideation notes

- **Benchmark ID:** 85_tp_f46697
- **Difficulty:** easy
- **Challenge:** synthesis
- **Relevant Notes:** [85, 86, 117, 143, 157, 178, 225, 240]
- **Retrieved Notes:** [85, 459, 87, 416, 617, 525, 444, 568, 330, 134, 117, 235, 212, 178, 290, 106, 453, 442, 755, 855]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.125 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.125 |
| R-Precision | 0.125 |
| Latency (ms) | 137.28 |
| Predicted Intent | idea |
| Expected Intent | idea |
| Intent Correct | True |
| Predicted Category | Ideas - AI Summarization |
| Expected Category | Ideas |
| Category Correct | True |

---

### HYBRID — My technical reference cheat sheets

- **Benchmark ID:** 72_tp_32bacd
- **Difficulty:** easy
- **Challenge:** synthesis
- **Relevant Notes:** [72, 73, 74, 75, 122, 135]
- **Retrieved Notes:** [309, 74, 485, 110, 235, 547, 360, 69, 530, 738, 838, 938, 1038, 163, 236, 357, 439, 528, 619, 602]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.167 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| MAP@5 | 0.083 |
| R-Precision | 0.167 |
| Latency (ms) | 114.66 |
| Predicted Intent | reference |
| Expected Intent | reference |
| Intent Correct | True |

---

### HYBRID — All my communication and message drafts

- **Benchmark ID:** 54_tp_b42b02
- **Difficulty:** easy
- **Challenge:** synthesis
- **Relevant Notes:** [54, 56, 57, 106, 132, 141]
- **Retrieved Notes:** [371, 141, 56, 582, 290, 382, 423, 415, 263, 472, 106, 87, 255, 453, 212, 613, 268, 682, 782, 882]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.333 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| MAP@5 | 0.194 |
| R-Precision | 0.333 |
| Latency (ms) | 111.48 |
| Predicted Intent | communication |
| Expected Intent | communication |
| Intent Correct | True |

---

### HYBRID — Errands I need to run today

- **Benchmark ID:** 76_tp_c52e4b
- **Difficulty:** medium
- **Challenge:** lexical_gap
- **Relevant Notes:** [76, 164, 190, 202, 286, 309, 322, 475]
- **Retrieved Notes:** [475, 79, 375, 735, 835, 935, 1035, 77, 393, 553, 248, 182, 92, 437, 601, 442, 755, 855, 955, 1055]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.125 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.125 |
| R-Precision | 0.125 |
| Latency (ms) | 109.46 |
| Predicted Intent | general |
| Expected Intent | todo |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | To Do |
| Category Correct | False |

---

### HYBRID — Things I need to pick up from the store

- **Benchmark ID:** 76_tp_c74a5f
- **Difficulty:** easy
- **Challenge:** lexical_gap
- **Relevant Notes:** [76, 164, 190, 202, 286, 309, 322, 475]
- **Retrieved Notes:** [76, 322, 475, 393, 589, 659, 759, 859, 959, 1059, 182, 115, 309, 606, 225, 216, 605, 71, 111, 82]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.600 |
| Recall@5 | 0.375 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.375 |
| R-Precision | 0.375 |
| Latency (ms) | 120.96 |
| Predicted Intent | general |
| Expected Intent | todo |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Shopping |
| Category Correct | False |

---

### HYBRID — Physical training and exercise plan

- **Benchmark ID:** 173_tp_f41c30
- **Difficulty:** easy
- **Challenge:** lexical_gap
- **Relevant Notes:** [173, 202, 291, 317, 380, 621, 631, 680]
- **Retrieved Notes:** [83, 631, 481, 437, 621, 107, 317, 380, 680, 780, 880, 980, 1080, 286, 79, 601, 82, 617, 212, 575]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.250 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| MAP@5 | 0.113 |
| R-Precision | 0.500 |
| Latency (ms) | 135.45 |
| Predicted Intent | general |
| Expected Intent | todo |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Health |
| Category Correct | False |

---

### HYBRID — How am I planning to stay healthy?

- **Benchmark ID:** 173_tp_7bafaa
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [173, 202, 291, 317, 380, 621, 631, 680]
- **Retrieved Notes:** [83, 212, 79, 84, 286, 380, 680, 780, 880, 980, 1080, 317, 437, 601, 76, 631, 495, 109, 557, 322]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.167 |
| MAP@5 | 0.000 |
| R-Precision | 0.250 |
| Latency (ms) | 117.36 |
| Predicted Intent | question |
| Expected Intent | question |
| Intent Correct | True |

---

### HYBRID — How much am I spending per month?

- **Benchmark ID:** 82_tp_86df0e
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [82, 210, 216, 281, 331, 345, 407, 535]
- **Retrieved Notes:** [216, 82, 331, 281, 490, 434, 341, 77, 535, 564, 393, 538, 606, 573, 577, 514, 571, 407, 557, 162]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.800 |
| Recall@5 | 0.500 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.500 |
| R-Precision | 0.500 |
| Latency (ms) | 113.56 |
| Predicted Intent | question |
| Expected Intent | question |
| Intent Correct | True |

---

### HYBRID — Personal finance tracking notes

- **Benchmark ID:** 82_tp_3665b0
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [82, 210, 216, 281, 331, 345, 407, 535]
- **Retrieved Notes:** [87, 82, 216, 285, 393, 637, 733, 833, 933, 1033, 341, 444, 411, 178, 290, 624, 403, 331, 371, 606]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.250 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| MAP@5 | 0.146 |
| R-Precision | 0.250 |
| Latency (ms) | 118.65 |
| Predicted Intent | reference |
| Expected Intent | reference |
| Intent Correct | True |

---

### HYBRID — BRPOPLPUSH reliable queue implementation

- **Benchmark ID:** 246_tp_6ef122
- **Difficulty:** hard
- **Challenge:** exact_phrase
- **Relevant Notes:** [246, 433, 643, 673, 684, 705, 773, 784]
- **Retrieved Notes:** [643, 673, 773, 873, 973, 1073, 246, 684, 784, 884, 984, 1084, 450, 671, 771, 871, 971, 1071, 462, 354]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.600 |
| Recall@5 | 0.375 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.375 |
| R-Precision | 0.625 |
| Latency (ms) | 121.85 |
| Predicted Intent | general |
| Expected Intent | reference |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Reference - Redis |
| Category Correct | False |

---

### HYBRID — ACID properties of databases

- **Benchmark ID:** 229_tp_454ff2
- **Difficulty:** easy
- **Challenge:** exact_phrase
- **Relevant Notes:** [229, 690, 790, 890, 990, 1090]
- **Retrieved Notes:** [229, 690, 790, 890, 990, 1090, 321, 707, 807, 907, 1007, 1107, 537, 156, 144, 292, 695, 795, 895, 995]

| Metric | Value |
|-------|------:|
| Precision@5 | 1.000 |
| Recall@5 | 0.833 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.833 |
| R-Precision | 1.000 |
| Latency (ms) | 136.83 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Study - DBMS |
| Category Correct | False |

---

### HYBRID — RRF score combination for hybrid search

- **Benchmark ID:** 518_tp_930ea0
- **Difficulty:** hard
- **Challenge:** exact_phrase
- **Relevant Notes:** [518, 718, 818, 918, 1018]
- **Retrieved Notes:** [518, 718, 818, 918, 1018, 252, 696, 796, 896, 996, 1096, 213, 729, 829, 929, 1029, 349, 402, 67, 183]

| Metric | Value |
|-------|------:|
| Precision@5 | 1.000 |
| Recall@5 | 1.000 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 1.000 |
| R-Precision | 1.000 |
| Latency (ms) | 122.89 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Study - AI |
| Category Correct | False |

---

### HYBRID — HNSW approximate nearest neighbor algorithm

- **Benchmark ID:** 215_tp_55df73
- **Difficulty:** hard
- **Challenge:** exact_phrase
- **Relevant Notes:** [215, 430, 681, 781, 881, 981, 1081]
- **Retrieved Notes:** [215, 681, 781, 881, 981, 1081, 430, 536, 67, 261, 639, 333, 650, 278, 677, 777, 877, 977, 1077, 545]

| Metric | Value |
|-------|------:|
| Precision@5 | 1.000 |
| Recall@5 | 0.714 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.714 |
| R-Precision | 1.000 |
| Latency (ms) | 137.50 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Study - AI |
| Category Correct | False |

---

### HYBRID — What do I need to buy this weekend?

- **Benchmark ID:** 76_tp_5c724a
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [76, 164, 190, 202, 309, 322, 393, 475]
- **Retrieved Notes:** [77, 110, 554, 76, 322, 393, 286, 115, 475, 216, 605, 631, 202, 112, 149, 164, 166, 198, 203, 235]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.250 |
| Hit | True |
| Reciprocal Rank | 0.250 |
| MAP@5 | 0.081 |
| R-Precision | 0.375 |
| Latency (ms) | 143.70 |
| Predicted Intent | todo |
| Expected Intent | todo |
| Intent Correct | True |
| Predicted Category | Tasks |
| Expected Category | Shopping |
| Category Correct | True |

---

### HYBRID — All my pending reminders and follow-ups

- **Benchmark ID:** 55_tp_3ff20c
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [55, 152, 212, 312, 542, 557]
- **Retrieved Notes:** [79, 191, 312, 392, 372, 620, 382, 475, 539, 56, 216, 582, 498, 203, 631, 77, 423, 290, 612, 442]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.167 |
| Hit | True |
| Reciprocal Rank | 0.333 |
| MAP@5 | 0.056 |
| R-Precision | 0.167 |
| Latency (ms) | 136.50 |
| Predicted Intent | reminder |
| Expected Intent | reminder |
| Intent Correct | True |
| Predicted Category | Reminders |
| Expected Category | Reminders |
| Category Correct | True |

---

### HYBRID — What have I told myself not to forget?

- **Benchmark ID:** 55_tp_05e927
- **Difficulty:** medium
- **Challenge:** lexical_gap
- **Relevant Notes:** [55, 152, 212, 312, 542, 557]
- **Retrieved Notes:** [212, 647, 475, 290, 505, 380, 680, 780, 880, 980, 1080, 318, 496, 240, 539, 458, 428, 728, 828, 928]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.167 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.167 |
| R-Precision | 0.167 |
| Latency (ms) | 116.04 |
| Predicted Intent | question |
| Expected Intent | reminder |
| Intent Correct | False |

---

### HYBRID — LeetCode patterns and problem-solving techniques

- **Benchmark ID:** 117_tp_44e6df
- **Difficulty:** medium
- **Challenge:** lexical
- **Relevant Notes:** [117, 127, 187, 224, 271, 279, 282, 316]
- **Retrieved Notes:** [224, 611, 316, 187, 546, 117, 399, 387, 453, 647, 460, 701, 801, 901, 1001, 1101, 302, 60, 536, 505]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.600 |
| Recall@5 | 0.375 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.302 |
| R-Precision | 0.500 |
| Latency (ms) | 140.06 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Study - Interview Prep |
| Category Correct | False |

---

### HYBRID — How do I approach dynamic programming questions?

- **Benchmark ID:** 117_tp_7bf7d7
- **Difficulty:** hard
- **Challenge:** semantic
- **Relevant Notes:** [117, 127, 187, 224, 271, 279, 282, 316]
- **Retrieved Notes:** [562, 459, 117, 352, 302, 398, 70, 227, 99, 416, 507, 593, 311, 154, 617, 199, 327, 309, 470, 294]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.125 |
| Hit | True |
| Reciprocal Rank | 0.333 |
| MAP@5 | 0.042 |
| R-Precision | 0.125 |
| Latency (ms) | 131.61 |
| Predicted Intent | question |
| Expected Intent | question |
| Intent Correct | True |

---

### HYBRID — System design concepts I need to review

- **Benchmark ID:** 70_tp_39b780
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [70, 145, 267, 305, 309, 334, 344, 346]
- **Retrieved Notes:** [392, 70, 360, 309, 99, 106, 439, 102, 602, 231, 267, 101, 608, 65, 95, 459, 178, 116, 565, 59]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.250 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| MAP@5 | 0.125 |
| R-Precision | 0.250 |
| Latency (ms) | 132.86 |
| Predicted Intent | idea |
| Expected Intent | study |
| Intent Correct | False |

---

### HYBRID — How do I design a scalable URL shortener?

- **Benchmark ID:** 70_tp_c6f60d
- **Difficulty:** hard
- **Challenge:** semantic
- **Relevant Notes:** [70, 145, 267, 305, 309, 334, 344, 346]
- **Retrieved Notes:** [602, 93, 346, 386, 644, 61, 219, 215, 681, 781, 881, 981, 1081, 119, 533, 721, 821, 921, 1021, 244]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.125 |
| Hit | True |
| Reciprocal Rank | 0.333 |
| MAP@5 | 0.042 |
| R-Precision | 0.125 |
| Latency (ms) | 111.95 |
| Predicted Intent | question |
| Expected Intent | question |
| Intent Correct | True |

---

### HYBRID — Behavioral interview story preparation

- **Benchmark ID:** 83_tp_a140c7
- **Difficulty:** medium
- **Challenge:** lexical
- **Relevant Notes:** [83, 85, 113, 114, 116, 131, 134, 135]
- **Retrieved Notes:** [468, 294, 360, 344, 263, 288, 70, 100, 609, 472, 540, 413, 154, 107, 152, 352, 507, 496, 54, 199]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 125.37 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Study - Interview Prep |
| Category Correct | False |

---

### HYBRID — Resume writing tips and improvement notes

- **Benchmark ID:** 100_tp_b51d58
- **Difficulty:** easy
- **Challenge:** lexical
- **Relevant Notes:** [100, 142, 185, 270, 523, 525]
- **Retrieved Notes:** [142, 100, 185, 415, 87, 203, 525, 583, 699, 799, 899, 999, 1099, 485, 330, 372, 110, 212, 106, 236]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.600 |
| Recall@5 | 0.500 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.500 |
| R-Precision | 0.500 |
| Latency (ms) | 116.35 |
| Predicted Intent | reference |
| Expected Intent | reference |
| Intent Correct | True |

---

### HYBRID — How should I write my software engineer resume?

- **Benchmark ID:** 100_tp_fcae97
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [100, 142, 185, 270, 523, 525]
- **Retrieved Notes:** [100, 142, 525, 185, 330, 496, 352, 272, 485, 360, 415, 70, 523, 199, 236, 107, 459, 134, 528, 166]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.800 |
| Recall@5 | 0.667 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.667 |
| R-Precision | 0.667 |
| Latency (ms) | 108.29 |
| Predicted Intent | question |
| Expected Intent | question |
| Intent Correct | True |

---

### HYBRID — Books I am reading or have read recently

- **Benchmark ID:** 78_tp_c601ae
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [78, 128, 155, 160, 172, 182, 194, 234]
- **Retrieved Notes:** [240, 528, 290, 309, 565, 439, 235, 360, 619, 496, 322, 472, 208, 458, 234, 69, 613, 492, 444, 582]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.067 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 184.34 |
| Predicted Intent | general |
| Expected Intent | reference |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Reference - Books |
| Category Correct | False |

---

### HYBRID — Reading list and book notes

- **Benchmark ID:** 78_tp_0f3259
- **Difficulty:** easy
- **Challenge:** lexical
- **Relevant Notes:** [78, 128, 155, 160, 172, 182, 194, 234]
- **Retrieved Notes:** [87, 444, 235, 290, 203, 240, 583, 699, 799, 899, 999, 1099, 393, 309, 258, 709, 809, 909, 1009, 430]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 114.85 |
| Predicted Intent | reference |
| Expected Intent | reference |
| Intent Correct | True |

---

### HYBRID — Habit formation notes from Atomic Habits

- **Benchmark ID:** 304_tp_4994bc
- **Difficulty:** easy
- **Challenge:** lexical
- **Relevant Notes:** [304, 317, 482, 557, 631, 634, 698, 734]
- **Retrieved Notes:** [482, 73, 557, 318, 116, 467, 224, 342, 667, 767, 867, 967, 1067, 550, 700, 800, 900, 1000, 1100, 328]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.250 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.208 |
| R-Precision | 0.250 |
| Latency (ms) | 104.61 |
| Predicted Intent | reference |
| Expected Intent | study |
| Intent Correct | False |

---

### HYBRID — Summary of James Clear's key ideas on habits

- **Benchmark ID:** 304_tp_37657b
- **Difficulty:** medium
- **Challenge:** lexical_gap
- **Relevant Notes:** [304, 317, 482, 557, 631, 634, 698, 734]
- **Retrieved Notes:** [482, 240, 496, 309, 235, 234, 469, 438, 439, 360, 444, 71, 134, 290, 472, 557, 85, 540, 550, 700]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.125 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.125 |
| R-Precision | 0.125 |
| Latency (ms) | 113.20 |
| Predicted Intent | idea |
| Expected Intent | study |
| Intent Correct | False |

---

### HYBRID — Online courses and tutorials I am taking

- **Benchmark ID:** 71_tp_43e20b
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [71, 145, 231, 266, 357, 394, 417, 471]
- **Retrieved Notes:** [471, 663, 763, 863, 963, 1063, 357, 343, 619, 145, 266, 751, 851, 951, 1051, 236, 309, 439, 60, 417]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.125 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.125 |
| R-Precision | 0.250 |
| Latency (ms) | 126.07 |
| Predicted Intent | study |
| Expected Intent | study |
| Intent Correct | True |

---

### HYBRID — Sleep improvement techniques and tips

- **Benchmark ID:** 133_tp_12eb56
- **Difficulty:** medium
- **Challenge:** lexical
- **Relevant Notes:** [133, 136, 202, 288, 348, 380, 434, 538]
- **Retrieved Notes:** [622, 434, 574, 317, 548, 348, 664, 764, 864, 964, 1064, 133, 288, 356, 472, 380, 680, 780, 880, 980]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.125 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| MAP@5 | 0.062 |
| R-Precision | 0.250 |
| Latency (ms) | 161.53 |
| Predicted Intent | general |
| Expected Intent | reference |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Reference - Health |
| Category Correct | False |

---

### HYBRID — How can I improve my sleep quality?

- **Benchmark ID:** 133_tp_2c6b3e
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [133, 136, 202, 288, 348, 380, 434, 538]
- **Retrieved Notes:** [434, 622, 574, 548, 317, 133, 348, 664, 764, 864, 964, 1064, 356, 84, 380, 680, 780, 880, 980, 1080]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.125 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.125 |
| R-Precision | 0.375 |
| Latency (ms) | 123.71 |
| Predicted Intent | question |
| Expected Intent | question |
| Intent Correct | True |

---

### HYBRID — Nutrition and supplement tracking notes

- **Benchmark ID:** 109_tp_f852f9
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [109, 133, 226, 286]
- **Retrieved Notes:** [286, 133, 322, 285, 216, 393, 87, 444, 495, 109, 475, 637, 733, 833, 933, 1033, 281, 289, 565, 76]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.500 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.500 |
| R-Precision | 0.500 |
| Latency (ms) | 104.59 |
| Predicted Intent | reference |
| Expected Intent | reference |
| Intent Correct | True |

---

### HYBRID — What supplements should I be taking?

- **Benchmark ID:** 109_tp_f444c2
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [109, 133, 226, 286]
- **Retrieved Notes:** [133, 286, 226, 109, 84, 322, 83, 631, 293, 601, 120, 331, 470, 291, 79, 76, 557, 495, 173, 475]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.800 |
| Recall@5 | 1.000 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 1.000 |
| R-Precision | 1.000 |
| Latency (ms) | 107.30 |
| Predicted Intent | question |
| Expected Intent | question |
| Intent Correct | True |

---

### HYBRID — Mental health practices and coping strategies

- **Benchmark ID:** 152_tp_3685ae
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [152, 288, 317, 472, 575]
- **Retrieved Notes:** [288, 575, 212, 472, 201, 380, 680, 780, 880, 980, 1080, 539, 550, 700, 800, 900, 1000, 1100, 291, 81]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.600 |
| Recall@5 | 0.600 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.550 |
| R-Precision | 0.600 |
| Latency (ms) | 119.29 |
| Predicted Intent | general |
| Expected Intent | reference |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Reference - Health |
| Category Correct | False |

---

### HYBRID — My notes on managing stress and anxiety

- **Benchmark ID:** 152_tp_5aba2a
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [152, 288, 317, 472, 575]
- **Retrieved Notes:** [288, 472, 212, 356, 539, 290, 360, 482, 550, 700, 800, 900, 1000, 1100, 575, 647, 203, 240, 380, 680]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.400 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.400 |
| R-Precision | 0.400 |
| Latency (ms) | 105.85 |
| Predicted Intent | reference |
| Expected Intent | reference |
| Intent Correct | True |

---

### HYBRID — Plans for open source and public building

- **Benchmark ID:** 117_tp_eab7a3
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [117, 141, 395, 400, 440, 453, 522, 554]
- **Retrieved Notes:** [255, 141, 554, 117, 106, 555, 175, 178, 140, 559, 528, 498, 95, 105, 413, 155, 607, 753, 853, 953]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.600 |
| Recall@5 | 0.375 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| MAP@5 | 0.240 |
| R-Precision | 0.375 |
| Latency (ms) | 106.40 |
| Predicted Intent | general |
| Expected Intent | idea |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Ideas |
| Category Correct | False |

---

### HYBRID — Notes on growing my developer presence online

- **Benchmark ID:** 117_tp_594cbf
- **Difficulty:** medium
- **Challenge:** lexical_gap
- **Relevant Notes:** [117, 141, 395, 400, 440, 453, 522, 554]
- **Retrieved Notes:** [255, 330, 141, 155, 555, 85, 106, 439, 272, 459, 99, 178, 413, 142, 528, 453, 583, 699, 799, 899]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.125 |
| Hit | True |
| Reciprocal Rank | 0.333 |
| MAP@5 | 0.042 |
| R-Precision | 0.125 |
| Latency (ms) | 97.44 |
| Predicted Intent | reference |
| Expected Intent | idea |
| Intent Correct | False |

---

### HYBRID — Fortran programming and legacy code notes

- **Benchmark ID:** 0_tp_07253f
- **Difficulty:** hard
- **Challenge:** negative
- **Relevant Notes:** []
- **Retrieved Notes:** [465, 547, 227, 169, 389, 110, 471, 663, 763, 863, 963, 1063, 163, 235, 283, 662, 762, 862, 962, 1062]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 117.17 |
| Predicted Intent | reference |
| Expected Intent | general |
| Intent Correct | False |

---

### HYBRID — Ancient history and archaeology notes

- **Benchmark ID:** 0_tp_13e990
- **Difficulty:** hard
- **Challenge:** negative
- **Relevant Notes:** []
- **Retrieved Notes:** [565, 290, 372, 386, 619, 444, 637, 733, 833, 933, 1033, 442, 755, 855, 955, 1055, 570, 625, 529, 289]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 124.55 |
| Predicted Intent | reference |
| Expected Intent | general |
| Intent Correct | False |

---

### HYBRID — Wine and cheese pairing recommendations

- **Benchmark ID:** 0_tp_f9589c
- **Difficulty:** hard
- **Challenge:** negative
- **Relevant Notes:** []
- **Retrieved Notes:** [81, 363, 104, 140, 217, 332, 342, 362, 369, 378, 559, 636, 667, 678, 693, 767, 778, 793, 867, 878]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 121.44 |
| Predicted Intent | general |
| Expected Intent | general |
| Intent Correct | True |
| Predicted Category | General |
| Expected Category | General |
| Category Correct | True |

---

### HYBRID — Piano lessons and music theory notes

- **Benchmark ID:** 0_tp_5abfd7
- **Difficulty:** hard
- **Challenge:** negative
- **Relevant Notes:** []
- **Retrieved Notes:** [444, 290, 87, 637, 733, 833, 933, 1033, 240, 235, 430, 565, 289, 583, 699, 799, 899, 999, 1099, 234]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 107.74 |
| Predicted Intent | reference |
| Expected Intent | general |
| Intent Correct | False |

---

### HYBRID — Gardening and plant care notes

- **Benchmark ID:** 0_tp_4fb99e
- **Difficulty:** hard
- **Challenge:** negative
- **Relevant Notes:** []
- **Retrieved Notes:** [583, 699, 799, 899, 999, 1099, 475, 110, 322, 212, 372, 74, 203, 87, 565, 485, 487, 419, 274, 415]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 104.84 |
| Predicted Intent | reference |
| Expected Intent | general |
| Intent Correct | False |

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
| Latency (ms) | 111.55 |
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
| Latency (ms) | 122.96 |
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
| Latency (ms) | 99.05 |
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
| Latency (ms) | 98.87 |
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
| Latency (ms) | 104.55 |
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
| Latency (ms) | 104.80 |
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
| Latency (ms) | 122.97 |
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
| Latency (ms) | 113.37 |
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
| Latency (ms) | 118.41 |
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
| Latency (ms) | 107.41 |
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
| Latency (ms) | 102.55 |
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
| Latency (ms) | 113.38 |
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
| Latency (ms) | 102.44 |
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
| Latency (ms) | 94.03 |
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
| Latency (ms) | 145.60 |
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
| Latency (ms) | 150.77 |
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
| Latency (ms) | 122.30 |
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
| Latency (ms) | 109.78 |
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
| Latency (ms) | 133.58 |
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
| Latency (ms) | 98.15 |
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
| Latency (ms) | 114.58 |
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
| Latency (ms) | 86.61 |
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
| Latency (ms) | 86.05 |
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
| Latency (ms) | 122.86 |
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
| Latency (ms) | 97.62 |
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
| Latency (ms) | 95.84 |
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
| Latency (ms) | 98.87 |
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
| Latency (ms) | 105.80 |
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
| Latency (ms) | 117.51 |
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
| Latency (ms) | 92.66 |
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
| Latency (ms) | 152.83 |
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
| Latency (ms) | 106.62 |
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
| Latency (ms) | 106.62 |
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
| Latency (ms) | 96.65 |
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
| Latency (ms) | 109.20 |
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
| Latency (ms) | 126.68 |
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
| Latency (ms) | 116.29 |
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
| Latency (ms) | 130.70 |
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
| Latency (ms) | 87.39 |
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
| Latency (ms) | 106.55 |
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
| Latency (ms) | 119.20 |
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
| Latency (ms) | 97.27 |
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
| Latency (ms) | 103.33 |
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
| Latency (ms) | 93.47 |
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
| Latency (ms) | 113.96 |
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
| Latency (ms) | 102.31 |
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
| Latency (ms) | 77.76 |
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
| Latency (ms) | 101.38 |
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
| Latency (ms) | 87.52 |
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
| Latency (ms) | 89.37 |
| Predicted Intent | question |
| Expected Intent | question |
| Intent Correct | True |

---

### RERANK — What are useful Python tips and tricks I've learned?

- **Benchmark ID:** 108_tp_62f888
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [108, 174, 177, 206, 232, 239, 272, 283]
- **Retrieved Notes:** [318, 206, 633, 357, 464, 745, 845, 945]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.125 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| MAP@5 | 0.062 |
| R-Precision | 0.125 |
| Latency (ms) | 108.03 |
| Predicted Intent | question |
| Expected Intent | study |
| Intent Correct | False |
| Predicted Category | Questions - Python |
| Expected Category | Study - Python |
| Category Correct | False |

---

### RERANK — Show my Python programming notes

- **Benchmark ID:** 108_tp_89ce75
- **Difficulty:** easy
- **Challenge:** lexical
- **Relevant Notes:** [108, 174, 177, 206, 232, 239, 272, 283]
- **Retrieved Notes:** [87, 583, 699, 799, 899, 999, 1099, 258]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 118.13 |
| Predicted Intent | reference |
| Expected Intent | study |
| Intent Correct | False |

---

### RERANK — How does Python async programming work?

- **Benchmark ID:** 170_tp_39fb15
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [170, 283, 304, 359, 364, 372, 471, 661, 662, 663]
- **Retrieved Notes:** [304, 734, 834, 934, 1034, 359, 283, 662]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.100 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.100 |
| R-Precision | 0.400 |
| Latency (ms) | 117.57 |
| Predicted Intent | question |
| Expected Intent | study |
| Intent Correct | False |
| Predicted Category | Questions - Python |
| Expected Category | Study - Python |
| Category Correct | False |

---

### RERANK — What git commands and workflows have I noted?

- **Benchmark ID:** 130_tp_e144a1
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [130, 135, 144, 169, 229, 272, 317, 328, 366, 395]
- **Retrieved Notes:** [612, 328, 501, 614, 522, 193, 679, 779]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.100 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| MAP@5 | 0.050 |
| R-Precision | 0.100 |
| Latency (ms) | 116.06 |
| Predicted Intent | question |
| Expected Intent | reference |
| Intent Correct | False |

---

### RERANK — Git tips and tricks

- **Benchmark ID:** 130_tp_832398
- **Difficulty:** easy
- **Challenge:** lexical
- **Relevant Notes:** [130, 135, 144, 169, 229, 272, 317, 328, 366, 395]
- **Retrieved Notes:** [646, 497, 719, 819, 919, 1019, 328, 522]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.143 |
| MAP@5 | 0.000 |
| R-Precision | 0.100 |
| Latency (ms) | 118.94 |
| Predicted Intent | general |
| Expected Intent | reference |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Reference - Git |
| Category Correct | False |

---

### RERANK — What do I know about RAG systems?

- **Benchmark ID:** 65_tp_3e802c
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [65, 114, 186, 197, 219, 222, 267, 296, 310, 376]
- **Retrieved Notes:** [386, 436, 470, 565, 197, 446, 730, 830]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.100 |
| Hit | True |
| Reciprocal Rank | 0.200 |
| MAP@5 | 0.020 |
| R-Precision | 0.100 |
| Latency (ms) | 94.92 |
| Predicted Intent | question |
| Expected Intent | study |
| Intent Correct | False |

---

### RERANK — Retrieval augmented generation notes

- **Benchmark ID:** 65_tp_034576
- **Difficulty:** easy
- **Challenge:** lexical
- **Relevant Notes:** [65, 114, 186, 197, 219, 222, 267, 296, 310, 376]
- **Retrieved Notes:** [65, 186, 398, 184, 289, 86, 487, 523]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.200 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.200 |
| R-Precision | 0.200 |
| Latency (ms) | 99.41 |
| Predicted Intent | reference |
| Expected Intent | study |
| Intent Correct | False |

---

### RERANK — Notes about embeddings and vector search

- **Benchmark ID:** 168_tp_f44ea2
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [168, 183, 228, 289, 298, 323, 376, 486, 487, 523]
- **Retrieved Notes:** [196, 333, 298, 726, 826, 926, 1026, 228]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.100 |
| Hit | True |
| Reciprocal Rank | 0.333 |
| MAP@5 | 0.033 |
| R-Precision | 0.200 |
| Latency (ms) | 113.34 |
| Predicted Intent | reference |
| Expected Intent | study |
| Intent Correct | False |

---

### RERANK — Large language model notes and findings

- **Benchmark ID:** 60_tp_438fb0
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [60, 119, 122, 136, 143, 186, 251, 268, 313, 329]
- **Retrieved Notes:** [186, 404, 708, 808, 908, 1008, 1108, 487]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.100 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.100 |
| R-Precision | 0.100 |
| Latency (ms) | 102.39 |
| Predicted Intent | reference |
| Expected Intent | study |
| Intent Correct | False |

---

### RERANK — Notes about reranking in search systems

- **Benchmark ID:** 67_tp_248b82
- **Difficulty:** hard
- **Challenge:** semantic
- **Relevant Notes:** [67, 119, 123, 176, 386, 648, 676, 776, 876, 976]
- **Retrieved Notes:** [67, 176, 119, 305, 58, 333, 213, 729]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.600 |
| Recall@5 | 0.300 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.300 |
| R-Precision | 0.300 |
| Latency (ms) | 94.09 |
| Predicted Intent | reference |
| Expected Intent | study |
| Intent Correct | False |

---

### RERANK — RAG and retrieval evaluation metrics

- **Benchmark ID:** 90_tp_bed875
- **Difficulty:** hard
- **Challenge:** multi_hop
- **Relevant Notes:** [90, 119, 310, 402, 485, 487, 595]
- **Retrieved Notes:** [386, 485, 310, 595, 186, 470, 492, 213]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.600 |
| Recall@5 | 0.429 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| MAP@5 | 0.274 |
| R-Precision | 0.429 |
| Latency (ms) | 107.72 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Study - AI |
| Category Correct | False |

---

### RERANK — How do I measure retrieval quality?

- **Benchmark ID:** 90_tp_c1f487
- **Difficulty:** hard
- **Challenge:** semantic
- **Relevant Notes:** [90, 119, 210, 310, 402, 485, 487, 595]
- **Retrieved Notes:** [310, 86, 485, 402, 213, 729, 829, 929]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.600 |
| Recall@5 | 0.375 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.302 |
| R-Precision | 0.375 |
| Latency (ms) | 110.72 |
| Predicted Intent | question |
| Expected Intent | study |
| Intent Correct | False |

---

### RERANK — Prompting techniques and tips

- **Benchmark ID:** 130_tp_d166fd
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [130, 191, 264, 268, 406, 436, 446, 456, 467, 493]
- **Retrieved Notes:** [406, 264, 507, 459, 199, 468, 632, 294]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.200 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.200 |
| R-Precision | 0.200 |
| Latency (ms) | 98.05 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Study - AI |
| Category Correct | False |

---

### RERANK — Caching strategies and implementations

- **Benchmark ID:** 103_tp_bee00a
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [103, 124, 146, 237, 269, 275, 284, 295, 318, 336]
- **Retrieved Notes:** [61, 93, 644, 602, 467, 318, 520, 146]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.167 |
| MAP@5 | 0.000 |
| R-Precision | 0.200 |
| Latency (ms) | 114.63 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Study - System Design |
| Category Correct | False |

---

### RERANK — Message queue and event streaming notes

- **Benchmark ID:** 71_tp_b1348d
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [71, 102, 144, 174, 200, 218, 238, 269, 297, 304]
- **Retrieved Notes:** [450, 671, 771, 871, 971, 1071, 372, 392]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 81.85 |
| Predicted Intent | communication |
| Expected Intent | study |
| Intent Correct | False |

---

### RERANK — System design interview prep notes

- **Benchmark ID:** 70_tp_c5e045
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [70, 145, 255, 267, 305, 309, 334, 344, 346, 360]
- **Retrieved Notes:** [360, 70, 106, 309, 99, 392, 352, 540]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.600 |
| Recall@5 | 0.300 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.275 |
| R-Precision | 0.300 |
| Latency (ms) | 84.14 |
| Predicted Intent | reference |
| Expected Intent | study |
| Intent Correct | False |

---

### RERANK — PostgreSQL database notes

- **Benchmark ID:** 58_tp_257a95
- **Difficulty:** medium
- **Challenge:** lexical
- **Relevant Notes:** [58, 66, 74, 104, 139, 144, 168, 175, 215, 267]
- **Retrieved Notes:** [74, 144, 417, 731, 831, 931, 1031, 58]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.200 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.200 |
| R-Precision | 0.300 |
| Latency (ms) | 95.30 |
| Predicted Intent | reference |
| Expected Intent | study |
| Intent Correct | False |
| Predicted Category | Reference - PostgreSQL |
| Expected Category | Study - PostgreSQL |
| Category Correct | False |

---

### RERANK — Redis usage and patterns

- **Benchmark ID:** 61_tp_89afdd
- **Difficulty:** easy
- **Challenge:** lexical
- **Relevant Notes:** [61, 73, 92, 103, 124, 146, 157, 174, 237, 246]
- **Retrieved Notes:** [73, 92, 269, 724, 824, 924, 1024, 61]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.200 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.200 |
| R-Precision | 0.300 |
| Latency (ms) | 91.92 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Study - Redis |
| Category Correct | False |

---

### RERANK — Docker and containerization notes

- **Benchmark ID:** 72_tp_c8e7e1
- **Difficulty:** easy
- **Challenge:** lexical
- **Relevant Notes:** [72, 75, 91, 105, 118, 138, 188, 192, 242, 295]
- **Retrieved Notes:** [72, 105, 192, 75, 491, 722, 822, 922]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.800 |
| Recall@5 | 0.400 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.400 |
| R-Precision | 0.400 |
| Latency (ms) | 89.77 |
| Predicted Intent | reference |
| Expected Intent | study |
| Intent Correct | False |
| Predicted Category | Reference - Docker |
| Expected Category | Study - Docker |
| Category Correct | False |

---

### RERANK — What Docker tips have I collected?

- **Benchmark ID:** 72_tp_808bd0
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [72, 75, 91, 105, 118, 138, 188, 192, 242, 295]
- **Retrieved Notes:** [72, 192, 295, 105, 75, 188, 355, 688]

| Metric | Value |
|-------|------:|
| Precision@5 | 1.000 |
| Recall@5 | 0.500 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.500 |
| R-Precision | 0.600 |
| Latency (ms) | 92.46 |
| Predicted Intent | question |
| Expected Intent | reference |
| Intent Correct | False |

---

### RERANK — FastAPI development notes

- **Benchmark ID:** 68_tp_d59df1
- **Difficulty:** medium
- **Challenge:** lexical
- **Relevant Notes:** [68, 132, 145, 165, 167, 266, 272, 313, 350, 365]
- **Retrieved Notes:** [68, 165, 725, 825, 925, 1025, 471, 663]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.200 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.200 |
| R-Precision | 0.200 |
| Latency (ms) | 97.57 |
| Predicted Intent | reference |
| Expected Intent | study |
| Intent Correct | False |

---

### RERANK — KnowledgeVault project notes

- **Benchmark ID:** 57_tp_c30342
- **Difficulty:** easy
- **Challenge:** lexical
- **Relevant Notes:** [57, 88, 89, 90, 91, 94, 95, 96, 97, 107]
- **Retrieved Notes:** [125, 95, 96, 89, 90, 262, 444, 57]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.800 |
| Recall@5 | 0.400 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| MAP@5 | 0.272 |
| R-Precision | 0.500 |
| Latency (ms) | 137.07 |
| Predicted Intent | reference |
| Expected Intent | reference |
| Intent Correct | True |
| Predicted Category | Reference - Shared |
| Expected Category | Reference - KnowledgeVault |
| Category Correct | True |

---

### RERANK — What decisions have I made for the KnowledgeVault project?

- **Benchmark ID:** 57_tp_5bc303
- **Difficulty:** medium
- **Challenge:** multi_hop
- **Relevant Notes:** [88, 89, 90, 91, 95, 96, 97]
- **Retrieved Notes:** [638, 90, 428, 728, 828, 928, 1028, 95]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.143 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| MAP@5 | 0.071 |
| R-Precision | 0.143 |
| Latency (ms) | 118.04 |
| Predicted Intent | question |
| Expected Intent | reference |
| Intent Correct | False |

---

### RERANK — What meetings have I had?

- **Benchmark ID:** 56_tp_7b886e
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [56, 106, 107, 149, 170, 233, 251, 283, 304, 359]
- **Retrieved Notes:** [371, 107, 263, 559, 442, 755, 855, 955]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.100 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| MAP@5 | 0.050 |
| R-Precision | 0.100 |
| Latency (ms) | 100.53 |
| Predicted Intent | event |
| Expected Intent | event |
| Intent Correct | True |

---

### RERANK — What are my pending tasks and deadlines?

- **Benchmark ID:** 233_tp_b305bf
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [233]
- **Retrieved Notes:** [498, 453, 233, 647, 235, 268, 289, 554]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 1.000 |
| Hit | True |
| Reciprocal Rank | 0.333 |
| MAP@5 | 0.333 |
| R-Precision | 0.000 |
| Latency (ms) | 133.80 |
| Predicted Intent | todo |
| Expected Intent | todo |
| Intent Correct | True |
| Predicted Category | Tasks |
| Expected Category | Tasks |
| Category Correct | True |

---

### RERANK — What health appointments do I have?

- **Benchmark ID:** 78_tp_db66ee
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [78, 79, 109, 157, 201, 210, 212, 226, 231, 355]
- **Retrieved Notes:** [79, 601, 559, 575, 198, 475, 78, 173]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.100 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.100 |
| R-Precision | 0.200 |
| Latency (ms) | 99.29 |
| Predicted Intent | reminder |
| Expected Intent | reminder |
| Intent Correct | True |
| Predicted Category | Appointments |
| Expected Category | Appointments |
| Category Correct | True |

---

### RERANK — What payments and bills do I need to make?

- **Benchmark ID:** 77_tp_c2ce55
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [77, 120, 126, 128, 131, 137, 140, 144, 160, 162]
- **Retrieved Notes:** [341, 77, 82, 635, 368, 331, 76, 573]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.100 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| MAP@5 | 0.050 |
| R-Precision | 0.100 |
| Latency (ms) | 86.23 |
| Predicted Intent | question |
| Expected Intent | todo |
| Intent Correct | False |

---

### RERANK — What is on my shopping list?

- **Benchmark ID:** 76_tp_d5a3f9
- **Difficulty:** easy
- **Challenge:** lexical
- **Relevant Notes:** [76, 322]
- **Retrieved Notes:** [393, 322, 606, 115, 76, 475, 605, 216]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 1.000 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| MAP@5 | 0.450 |
| R-Precision | 0.500 |
| Latency (ms) | 93.80 |
| Predicted Intent | question |
| Expected Intent | todo |
| Intent Correct | False |

---

### RERANK — Show all my reminders

- **Benchmark ID:** 55_tp_1c812c
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [55, 152, 212, 312, 542, 557]
- **Retrieved Notes:** [382, 56, 312, 290, 442, 755, 855, 955]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.167 |
| Hit | True |
| Reciprocal Rank | 0.333 |
| MAP@5 | 0.056 |
| R-Precision | 0.167 |
| Latency (ms) | 100.40 |
| Predicted Intent | reminder |
| Expected Intent | reminder |
| Intent Correct | True |
| Predicted Category | Reminders |
| Expected Category | Reminders |
| Category Correct | True |

---

### RERANK — My budget and expense tracking notes

- **Benchmark ID:** 82_tp_feed7d
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [82, 153, 202, 210, 216, 254, 281, 291, 331, 345]
- **Retrieved Notes:** [82, 216, 606, 393, 285, 341, 87, 459]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.200 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.200 |
| R-Precision | 0.200 |
| Latency (ms) | 91.30 |
| Predicted Intent | reference |
| Expected Intent | todo |
| Intent Correct | False |

---

### RERANK — My travel plans and notes

- **Benchmark ID:** 81_tp_4afce2
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [81, 115, 126, 128, 130, 171, 175, 176, 178, 186]
- **Retrieved Notes:** [290, 81, 212, 393, 444, 77, 190, 627]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.100 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| MAP@5 | 0.050 |
| R-Precision | 0.100 |
| Latency (ms) | 92.86 |
| Predicted Intent | reference |
| Expected Intent | todo |
| Intent Correct | False |

---

### RERANK — Fitness and workout notes

- **Benchmark ID:** 173_tp_d9566a
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [173, 185, 202, 232, 246, 291, 317, 380, 392, 433]
- **Retrieved Notes:** [631, 481, 87, 482, 83, 212, 107, 621]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 96.55 |
| Predicted Intent | reference |
| Expected Intent | todo |
| Intent Correct | False |

---

### RERANK — My startup ideas and business notes

- **Benchmark ID:** 85_tp_6a3292
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [85, 86, 117, 120, 125, 128, 131, 134, 143, 157]
- **Retrieved Notes:** [85, 525, 459, 617, 441, 134, 87, 178]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.100 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.100 |
| R-Precision | 0.200 |
| Latency (ms) | 106.83 |
| Predicted Intent | idea |
| Expected Intent | idea |
| Intent Correct | True |
| Predicted Category | Ideas - AI |
| Expected Category | Ideas - Startups |
| Category Correct | True |

---

### RERANK — What business ideas have I documented?

- **Benchmark ID:** 85_tp_aeedec
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [85, 86, 117, 120, 125, 128, 131, 134, 143, 157]
- **Retrieved Notes:** [225, 178, 85, 441, 459, 260, 413, 240]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.100 |
| Hit | True |
| Reciprocal Rank | 0.333 |
| MAP@5 | 0.033 |
| R-Precision | 0.100 |
| Latency (ms) | 96.67 |
| Predicted Intent | idea |
| Expected Intent | idea |
| Intent Correct | True |

---

### RERANK — Things I need to tell Sid

- **Benchmark ID:** 54_tp_6e7d12
- **Difficulty:** easy
- **Challenge:** lexical
- **Relevant Notes:** [54, 55, 56, 57, 117, 187, 203, 220, 225, 247]
- **Retrieved Notes:** [54, 57, 56, 55, 423, 247, 442, 755]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.800 |
| Recall@5 | 0.400 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.400 |
| R-Precision | 0.500 |
| Latency (ms) | 91.48 |
| Predicted Intent | communication |
| Expected Intent | communication |
| Intent Correct | True |
| Predicted Category | Communication - Sid |
| Expected Category | Things to Tell Sid |
| Category Correct | True |

---

### RERANK — Things to discuss with Sid at the next meeting

- **Benchmark ID:** 54_tp_68cb9e
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [54, 55, 56, 57, 117, 187, 203, 220, 225, 247]
- **Retrieved Notes:** [57, 54, 56, 423, 247, 55, 203, 442]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.800 |
| Recall@5 | 0.400 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.380 |
| R-Precision | 0.600 |
| Latency (ms) | 100.70 |
| Predicted Intent | communication |
| Expected Intent | communication |
| Intent Correct | True |
| Predicted Category | Communication - Sid |
| Expected Category | Things to Tell Sid |
| Category Correct | True |

---

### RERANK — Message to send to Siddhant about backend

- **Benchmark ID:** 54_tp_a4d45e
- **Difficulty:** medium
- **Challenge:** lexical_gap
- **Relevant Notes:** [54, 55, 56, 57, 117, 187, 203, 220, 225, 247]
- **Retrieved Notes:** [56, 423, 54, 55, 57, 106, 392, 372]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.800 |
| Recall@5 | 0.400 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.322 |
| R-Precision | 0.400 |
| Latency (ms) | 93.90 |
| Predicted Intent | communication |
| Expected Intent | communication |
| Intent Correct | True |

---

### RERANK — Reciprocal Rank Fusion

- **Benchmark ID:** 518_tp_583ff7
- **Difficulty:** medium
- **Challenge:** exact_phrase
- **Relevant Notes:** [518, 718, 818, 918, 1018]
- **Retrieved Notes:** [518, 718, 818, 918, 1018, 649, 67, 176]

| Metric | Value |
|-------|------:|
| Precision@5 | 1.000 |
| Recall@5 | 1.000 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 1.000 |
| R-Precision | 1.000 |
| Latency (ms) | 108.06 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Study - AI |
| Category Correct | False |

---

### RERANK — Redis vs Kafka — when to use each

- **Benchmark ID:** 1024_tp_8759f9
- **Difficulty:** hard
- **Challenge:** comparison
- **Relevant Notes:** [1024, 771, 773, 520]
- **Retrieved Notes:** [643, 673, 773, 873, 973, 1073, 450, 671]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.250 |
| Hit | True |
| Reciprocal Rank | 0.333 |
| MAP@5 | 0.083 |
| R-Precision | 0.250 |
| Latency (ms) | 175.30 |
| Predicted Intent | question |
| Expected Intent | study |
| Intent Correct | False |

---

### RERANK — Resources for learning backend development

- **Benchmark ID:** 108_tp_d16fba
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [132, 68, 165, 108, 206, 174, 177, 145]
- **Retrieved Notes:** [106, 61, 330, 96, 101, 439, 272, 357]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 97.53 |
| Predicted Intent | study |
| Expected Intent | study |
| Intent Correct | True |

---

### RERANK — Notes about Fortran programming

- **Benchmark ID:** 0_tp_6cd1aa
- **Difficulty:** hard
- **Challenge:** negative
- **Relevant Notes:** []
- **Retrieved Notes:** [465, 547, 619, 471, 663, 763, 863, 963]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 98.46 |
| Predicted Intent | reference |
| Expected Intent | general |
| Intent Correct | False |

---

### RERANK — My notes on ancient Roman history

- **Benchmark ID:** 0_tp_b73b18
- **Difficulty:** hard
- **Challenge:** negative
- **Relevant Notes:** []
- **Retrieved Notes:** [290, 565, 583, 699, 799, 899, 999, 1099]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 98.24 |
| Predicted Intent | reference |
| Expected Intent | general |
| Intent Correct | False |

---

### RERANK — Cooking recipes I've saved

- **Benchmark ID:** 0_tp_fe75c4
- **Difficulty:** hard
- **Challenge:** negative
- **Relevant Notes:** []
- **Retrieved Notes:** [322, 475, 71, 281, 286, 76, 438, 212]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 104.36 |
| Predicted Intent | general |
| Expected Intent | general |
| Intent Correct | True |
| Predicted Category | General |
| Expected Category | General |
| Category Correct | True |

---

### RERANK — KnowledgeVault RAG pipeline decisions and findings

- **Benchmark ID:** 1028_tp_65ec5f
- **Difficulty:** hard
- **Challenge:** multi_hop
- **Relevant Notes:** [1030, 1032, 533]
- **Retrieved Notes:** [310, 90, 446, 730, 830, 930, 1030, 638]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.143 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 96.06 |
| Predicted Intent | general |
| Expected Intent | reference |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Reference - KnowledgeVault |
| Category Correct | False |

---

### RERANK — What benchmark results have I recorded for KnowledgeVault retrieval?

- **Benchmark ID:** 1028_tp_2e0731
- **Difficulty:** hard
- **Challenge:** multi_hop
- **Relevant Notes:** [1032, 523, 402]
- **Retrieved Notes:** [310, 90, 402, 213, 729, 829, 929, 1029]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.333 |
| Hit | True |
| Reciprocal Rank | 0.333 |
| MAP@5 | 0.111 |
| R-Precision | 0.333 |
| Latency (ms) | 92.82 |
| Predicted Intent | question |
| Expected Intent | reference |
| Intent Correct | False |

---

### RERANK — What have I been working on this month?

- **Benchmark ID:** 77_tp_d33a9c
- **Difficulty:** hard
- **Challenge:** temporal
- **Relevant Notes:** [149]
- **Retrieved Notes:** [453, 77, 82, 647, 375, 735, 835, 935]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 89.30 |
| Predicted Intent | question |
| Expected Intent | general |
| Intent Correct | False |

---

### RERANK — Recent notes and activities

- **Benchmark ID:** 77_tp_c2c25c
- **Difficulty:** hard
- **Challenge:** temporal
- **Relevant Notes:** [149, 286]
- **Retrieved Notes:** [87, 444, 565, 290, 203, 372, 453, 442]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 90.01 |
| Predicted Intent | reference |
| Expected Intent | general |
| Intent Correct | False |

---

### RERANK — My study notes on AI and machine learning

- **Benchmark ID:** 1026_tp_74f5bc
- **Difficulty:** easy
- **Challenge:** synthesis
- **Relevant Notes:** [1026, 774, 1030, 510, 523, 268, 267, 782]
- **Retrieved Notes:** [529, 230, 87, 619, 85, 416, 122, 444]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 100.40 |
| Predicted Intent | study |
| Expected Intent | study |
| Intent Correct | True |
| Predicted Category | Study - AI |
| Expected Category | Study - AI |
| Category Correct | True |

---

### RERANK — Messages I need to send Siddhant

- **Benchmark ID:** 54_tp_636e21
- **Difficulty:** easy
- **Challenge:** lexical_gap
- **Relevant Notes:** [54, 55, 56, 57, 117, 187, 203, 220]
- **Retrieved Notes:** [56, 423, 55, 54, 57, 392, 382, 129]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.800 |
| Recall@5 | 0.500 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.402 |
| R-Precision | 0.500 |
| Latency (ms) | 105.71 |
| Predicted Intent | general |
| Expected Intent | communication |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Things to Tell Sid |
| Category Correct | False |

---

### RERANK — Pending conversations with Sid

- **Benchmark ID:** 54_tp_d0b55d
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [54, 55, 56, 57, 117, 187, 203, 220]
- **Retrieved Notes:** [56, 423, 57, 54, 55, 247, 203, 264]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.800 |
| Recall@5 | 0.500 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.402 |
| R-Precision | 0.625 |
| Latency (ms) | 123.78 |
| Predicted Intent | todo |
| Expected Intent | communication |
| Intent Correct | False |
| Predicted Category | Tasks |
| Expected Category | Things to Tell Sid |
| Category Correct | False |

---

### RERANK — Notes about Sid and our project discussions

- **Benchmark ID:** 54_tp_e69fe7
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [54, 55, 56, 57, 117, 187, 203, 220]
- **Retrieved Notes:** [57, 56, 423, 247, 54, 55, 442, 755]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.600 |
| Recall@5 | 0.375 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.325 |
| R-Precision | 0.500 |
| Latency (ms) | 98.03 |
| Predicted Intent | reference |
| Expected Intent | communication |
| Intent Correct | False |

---

### RERANK — Business concepts I want to explore

- **Benchmark ID:** 85_tp_712892
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [85, 86, 117, 131, 134, 143, 157, 166]
- **Retrieved Notes:** [309, 178, 225, 85, 166, 685, 785, 885]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.250 |
| Hit | True |
| Reciprocal Rank | 0.250 |
| MAP@5 | 0.081 |
| R-Precision | 0.250 |
| Latency (ms) | 99.40 |
| Predicted Intent | idea |
| Expected Intent | idea |
| Intent Correct | True |
| Predicted Category | Ideas - AI |
| Expected Category | Ideas |
| Category Correct | True |

---

### RERANK — Product ideas I have noted down

- **Benchmark ID:** 85_tp_46bae2
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [85, 86, 117, 131, 134, 143, 157, 166]
- **Retrieved Notes:** [85, 322, 202, 475, 117, 178, 325, 459]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.250 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.175 |
| R-Precision | 0.250 |
| Latency (ms) | 91.83 |
| Predicted Intent | idea |
| Expected Intent | idea |
| Intent Correct | True |

---

### RERANK — Entrepreneurship and venture ideas

- **Benchmark ID:** 85_tp_97280d
- **Difficulty:** medium
- **Challenge:** lexical_gap
- **Relevant Notes:** [85, 86, 117, 131, 134, 143, 157, 166]
- **Retrieved Notes:** [85, 166, 685, 785, 885, 985, 1085, 617]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.250 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.250 |
| R-Precision | 0.250 |
| Latency (ms) | 93.46 |
| Predicted Intent | idea |
| Expected Intent | idea |
| Intent Correct | True |
| Predicted Category | Ideas - AI |
| Expected Category | Ideas |
| Category Correct | True |

---

### RERANK — Outstanding financial obligations

- **Benchmark ID:** 77_tp_c85047
- **Difficulty:** medium
- **Challenge:** lexical_gap
- **Relevant Notes:** [77, 120, 126, 128, 131, 137, 140, 144]
- **Retrieved Notes:** [82, 341, 411, 210, 635, 77, 162, 393]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.167 |
| MAP@5 | 0.000 |
| R-Precision | 0.125 |
| Latency (ms) | 95.77 |
| Predicted Intent | general |
| Expected Intent | todo |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Bills |
| Category Correct | False |

---

### RERANK — Payments I still need to make

- **Benchmark ID:** 77_tp_573aa5
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [77, 120, 126, 128, 131, 137, 140, 144]
- **Retrieved Notes:** [341, 635, 160, 312, 331, 77, 369, 626]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.167 |
| MAP@5 | 0.000 |
| R-Precision | 0.125 |
| Latency (ms) | 94.57 |
| Predicted Intent | general |
| Expected Intent | todo |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Bills |
| Category Correct | False |

---

### RERANK — Monthly expenses and dues

- **Benchmark ID:** 77_tp_e477f7
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [77, 120, 126, 128, 131, 137, 140, 144]
- **Retrieved Notes:** [82, 341, 216, 635, 490, 601, 368, 535]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 109.12 |
| Predicted Intent | general |
| Expected Intent | todo |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Bills |
| Category Correct | False |

---

### RERANK — Medical appointments on my calendar

- **Benchmark ID:** 78_tp_c31b3d
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [78, 79, 109, 157, 201, 210, 212, 226]
- **Retrieved Notes:** [79, 559, 601, 198, 78, 56, 231, 620]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.250 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.175 |
| R-Precision | 0.250 |
| Latency (ms) | 108.96 |
| Predicted Intent | reminder |
| Expected Intent | todo |
| Intent Correct | False |
| Predicted Category | Reminders |
| Expected Category | To Do |
| Category Correct | False |

---

### RERANK — Healthcare and wellness reminders

- **Benchmark ID:** 78_tp_d52f8d
- **Difficulty:** easy
- **Challenge:** lexical_gap
- **Relevant Notes:** [78, 79, 109, 157, 201, 210, 212, 226]
- **Retrieved Notes:** [79, 475, 317, 601, 557, 575, 322, 392]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.125 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.125 |
| R-Precision | 0.125 |
| Latency (ms) | 102.35 |
| Predicted Intent | reminder |
| Expected Intent | reminder |
| Intent Correct | True |
| Predicted Category | Appointments |
| Expected Category | Appointments |
| Category Correct | True |

---

### RERANK — In-memory datastore behavior notes

- **Benchmark ID:** 61_tp_0bc3d9
- **Difficulty:** medium
- **Challenge:** lexical_gap
- **Relevant Notes:** [61, 73, 92, 103, 157, 174, 269, 303]
- **Retrieved Notes:** [275, 706, 806, 906, 1006, 1106, 219, 146]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 93.10 |
| Predicted Intent | reference |
| Expected Intent | study |
| Intent Correct | False |

---

### RERANK — Cache eviction policy details

- **Benchmark ID:** 61_tp_d58d06
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [61, 73, 92, 103, 157, 174, 269, 303]
- **Retrieved Notes:** [103, 520, 318, 467, 534, 61, 644, 579]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.125 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.125 |
| R-Precision | 0.250 |
| Latency (ms) | 110.14 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Study - Redis |
| Category Correct | False |

---

### RERANK — Team meetings I have attended

- **Benchmark ID:** 56_tp_3888f9
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [56, 106, 107, 149, 170, 233, 251, 283]
- **Retrieved Notes:** [107, 263, 371, 448, 294, 438, 141, 81]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.125 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.125 |
| R-Precision | 0.125 |
| Latency (ms) | 88.70 |
| Predicted Intent | event |
| Expected Intent | event |
| Intent Correct | True |

---

### RERANK — Sprint retrospective and planning notes

- **Benchmark ID:** 56_tp_b7d172
- **Difficulty:** easy
- **Challenge:** lexical_gap
- **Relevant Notes:** [56, 106, 107, 149, 170, 233, 251, 283]
- **Retrieved Notes:** [107, 203, 466, 372, 82, 106, 294, 212]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.125 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.125 |
| R-Precision | 0.250 |
| Latency (ms) | 86.45 |
| Predicted Intent | reference |
| Expected Intent | event |
| Intent Correct | False |

---

### RERANK — Sync notes with the team

- **Benchmark ID:** 56_tp_1162c8
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [56, 106, 107, 149, 170, 233, 251, 283]
- **Retrieved Notes:** [372, 203, 87, 149, 444, 125, 604, 637]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.125 |
| Hit | True |
| Reciprocal Rank | 0.250 |
| MAP@5 | 0.031 |
| R-Precision | 0.125 |
| Latency (ms) | 91.70 |
| Predicted Intent | reference |
| Expected Intent | meeting |
| Intent Correct | False |
| Predicted Category | Reference - Shared |
| Expected Category | Meetings |
| Category Correct | False |

---

### RERANK — Weekly standup summaries

- **Benchmark ID:** 56_tp_59ba00
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [56, 106, 107, 149, 170, 233, 251, 283]
- **Retrieved Notes:** [107, 87, 453, 565, 438, 230, 240, 631]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.125 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.125 |
| R-Precision | 0.125 |
| Latency (ms) | 93.60 |
| Predicted Intent | general |
| Expected Intent | meeting |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Meetings |
| Category Correct | False |

---

### RERANK — KnowledgeVault project milestones and deliverables

- **Benchmark ID:** 57_tp_d91b61
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [57, 88, 89, 90, 91, 94, 95, 96]
- **Retrieved Notes:** [125, 90, 638, 95, 88, 57, 96, 428]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.600 |
| Recall@5 | 0.375 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| MAP@5 | 0.200 |
| R-Precision | 0.625 |
| Latency (ms) | 112.18 |
| Predicted Intent | general |
| Expected Intent | project |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Projects |
| Category Correct | False |

---

### RERANK — What is the architecture of my main project?

- **Benchmark ID:** 57_tp_92649a
- **Difficulty:** hard
- **Challenge:** multi_hop
- **Relevant Notes:** [57, 88, 89, 90, 91, 95, 96]
- **Retrieved Notes:** [106, 95, 392, 102, 602, 175, 62, 178]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.143 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| MAP@5 | 0.071 |
| R-Precision | 0.143 |
| Latency (ms) | 95.33 |
| Predicted Intent | question |
| Expected Intent | project |
| Intent Correct | False |

---

### RERANK — Current sprint goals for KnowledgeVault

- **Benchmark ID:** 57_tp_74e120
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [57, 88, 89, 90, 91, 94, 95, 96]
- **Retrieved Notes:** [107, 90, 125, 89, 251, 428, 728, 828]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.250 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| MAP@5 | 0.125 |
| R-Precision | 0.250 |
| Latency (ms) | 109.80 |
| Predicted Intent | general |
| Expected Intent | project |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Projects |
| Category Correct | False |

---

### RERANK — Capstone project tasks and status

- **Benchmark ID:** 175_tp_9c7eb5
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [175, 190, 199, 225, 233, 263, 285, 382]
- **Retrieved Notes:** [498, 233, 175, 568, 607, 753, 853, 953]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.250 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| MAP@5 | 0.146 |
| R-Precision | 0.250 |
| Latency (ms) | 121.13 |
| Predicted Intent | todo |
| Expected Intent | project |
| Intent Correct | False |
| Predicted Category | Tasks |
| Expected Category | Projects |
| Category Correct | False |

---

### RERANK — University project submission deadlines

- **Benchmark ID:** 175_tp_c51da4
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [175, 190, 199, 225, 233, 263, 285, 382]
- **Retrieved Notes:** [233, 498, 506, 411, 620, 453, 607, 753]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.125 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.125 |
| R-Precision | 0.125 |
| Latency (ms) | 106.66 |
| Predicted Intent | general |
| Expected Intent | project |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Projects |
| Category Correct | False |

---

### RERANK — My personal reflections and journal entries

- **Benchmark ID:** 113_tp_6bba32
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [113, 149, 152, 162, 166, 191]
- **Retrieved Notes:** [472, 290, 550, 700, 800, 900, 1000, 1100]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 109.76 |
| Predicted Intent | general |
| Expected Intent | general |
| Intent Correct | True |
| Predicted Category | General |
| Expected Category | General |
| Category Correct | True |

---

### RERANK — What did I realize recently?

- **Benchmark ID:** 113_tp_ff1a3d
- **Difficulty:** hard
- **Challenge:** semantic
- **Relevant Notes:** [113, 149, 152, 162, 166, 191]
- **Retrieved Notes:** [505, 458, 583, 699, 799, 899, 999, 1099]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 89.71 |
| Predicted Intent | question |
| Expected Intent | general |
| Intent Correct | False |

---

### RERANK — Insights I've been writing down

- **Benchmark ID:** 113_tp_be2de4
- **Difficulty:** medium
- **Challenge:** lexical_gap
- **Relevant Notes:** [113, 149, 152, 162, 166, 191]
- **Retrieved Notes:** [290, 235, 583, 699, 799, 899, 999, 1099]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 103.83 |
| Predicted Intent | general |
| Expected Intent | general |
| Intent Correct | True |
| Predicted Category | General |
| Expected Category | General |
| Category Correct | True |

---

### RERANK — My career goals and direction notes

- **Benchmark ID:** 56_tp_f28e5b
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [56, 61, 91, 96, 101, 106, 114, 155]
- **Retrieved Notes:** [166, 685, 785, 885, 985, 1085, 272, 290]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 94.86 |
| Predicted Intent | reference |
| Expected Intent | general |
| Intent Correct | False |

---

### RERANK — Long-term professional planning notes

- **Benchmark ID:** 56_tp_e42aaa
- **Difficulty:** hard
- **Challenge:** lexical_gap
- **Relevant Notes:** [56, 61, 91, 96, 101, 106, 114, 155]
- **Retrieved Notes:** [107, 617, 212, 87, 601, 203, 82, 528]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 104.02 |
| Predicted Intent | reference |
| Expected Intent | general |
| Intent Correct | False |

---

### RERANK — Time management and focus techniques

- **Benchmark ID:** 85_tp_c33ed2
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [85, 199, 224, 240, 248, 286, 429, 453]
- **Retrieved Notes:** [240, 248, 565, 521, 224, 438, 348, 664]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.600 |
| Recall@5 | 0.375 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.325 |
| R-Precision | 0.375 |
| Latency (ms) | 150.98 |
| Predicted Intent | general |
| Expected Intent | reference |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Reference - Productivity |
| Category Correct | False |

---

### RERANK — Notes on staying productive while studying

- **Benchmark ID:** 85_tp_a94724
- **Difficulty:** medium
- **Challenge:** lexical_gap
- **Relevant Notes:** [85, 199, 224, 240, 248, 286, 429, 453]
- **Retrieved Notes:** [240, 380, 680, 780, 880, 980, 1080, 496]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.125 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.125 |
| R-Precision | 0.125 |
| Latency (ms) | 101.78 |
| Predicted Intent | reference |
| Expected Intent | reference |
| Intent Correct | True |

---

### RERANK — FastAPI route and dependency injection notes

- **Benchmark ID:** 68_tp_025916
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [68, 120, 132, 145, 153, 165, 167, 169]
- **Retrieved Notes:** [68, 165, 725, 825, 925, 1025, 132, 658]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.250 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.250 |
| R-Precision | 0.375 |
| Latency (ms) | 87.61 |
| Predicted Intent | reference |
| Expected Intent | reference |
| Intent Correct | True |

---

### RERANK — Python web framework notes for FastAPI

- **Benchmark ID:** 68_tp_f99196
- **Difficulty:** easy
- **Challenge:** lexical_gap
- **Relevant Notes:** [68, 120, 132, 145, 153, 165, 167, 169]
- **Retrieved Notes:** [471, 663, 763, 863, 963, 1063, 266, 751]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 97.72 |
| Predicted Intent | reference |
| Expected Intent | study |
| Intent Correct | False |

---

### RERANK — API endpoint design patterns in FastAPI

- **Benchmark ID:** 68_tp_9b1c89
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [68, 120, 132, 145, 153, 165, 167, 169]
- **Retrieved Notes:** [68, 165, 725, 825, 925, 1025, 189, 697]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.250 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.250 |
| R-Precision | 0.250 |
| Latency (ms) | 115.43 |
| Predicted Intent | general |
| Expected Intent | reference |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Reference - KnowledgeVault Backend |
| Category Correct | False |

---

### RERANK — SQLAlchemy ORM usage patterns

- **Benchmark ID:** 55_tp_fbaf81
- **Difficulty:** medium
- **Challenge:** lexical
- **Relevant Notes:** [55, 58, 69, 85, 98, 123, 129, 132]
- **Retrieved Notes:** [69, 206, 363, 365, 694, 794, 894, 994]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.125 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.125 |
| R-Precision | 0.125 |
| Latency (ms) | 110.98 |
| Predicted Intent | general |
| Expected Intent | reference |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Reference - KnowledgeVault Backend |
| Category Correct | False |

---

### RERANK — Database session management in Python

- **Benchmark ID:** 55_tp_e342eb
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [55, 58, 69, 85, 98, 123, 129, 132]
- **Retrieved Notes:** [365, 694, 794, 894, 994, 1094, 483, 657]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 98.07 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Study - FastAPI |
| Category Correct | False |

---

### RERANK — How do I fix N+1 query problems?

- **Benchmark ID:** 55_tp_d34490
- **Difficulty:** hard
- **Challenge:** semantic
- **Relevant Notes:** [55, 58, 69, 85, 98, 123, 129, 132]
- **Retrieved Notes:** [589, 659, 759, 859, 959, 1059, 259, 385]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 145.15 |
| Predicted Intent | todo |
| Expected Intent | question |
| Intent Correct | False |
| Predicted Category | Tasks |
| Expected Category | Questions |
| Category Correct | False |

---

### RERANK — pgvector setup and index configuration

- **Benchmark ID:** 66_tp_9be255
- **Difficulty:** hard
- **Challenge:** lexical
- **Relevant Notes:** [66, 168, 215, 298, 323, 337, 367, 500]
- **Retrieved Notes:** [66, 323, 742, 842, 942, 1042, 500, 672]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.250 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.250 |
| R-Precision | 0.375 |
| Latency (ms) | 172.39 |
| Predicted Intent | general |
| Expected Intent | reference |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Reference - PostgreSQL |
| Category Correct | False |

---

### RERANK — Vector similarity search configuration

- **Benchmark ID:** 66_tp_72bd4f
- **Difficulty:** hard
- **Challenge:** semantic
- **Relevant Notes:** [66, 168, 215, 298, 323, 337, 367, 500]
- **Retrieved Notes:** [333, 66, 168, 252, 696, 796, 896, 996]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.250 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| MAP@5 | 0.146 |
| R-Precision | 0.250 |
| Latency (ms) | 205.17 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Study - AI |
| Category Correct | False |

---

### RERANK — Algorithm and data structure study notes

- **Benchmark ID:** 59_tp_a4350a
- **Difficulty:** medium
- **Challenge:** lexical
- **Relevant Notes:** [59, 60, 182, 204, 215, 224, 244, 247]
- **Retrieved Notes:** [354, 66, 545, 60, 465, 530, 738, 838]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.125 |
| Hit | True |
| Reciprocal Rank | 0.250 |
| MAP@5 | 0.031 |
| R-Precision | 0.125 |
| Latency (ms) | 117.61 |
| Predicted Intent | study |
| Expected Intent | study |
| Intent Correct | True |

---

### RERANK — Competitive programming problem patterns

- **Benchmark ID:** 59_tp_a3126e
- **Difficulty:** hard
- **Challenge:** semantic
- **Relevant Notes:** [59, 60, 182, 204, 215, 224, 244, 247]
- **Retrieved Notes:** [302, 460, 701, 801, 901, 1001, 1101, 117]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 132.11 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Study - Algorithms |
| Category Correct | False |

---

### RERANK — How do I solve graph traversal problems?

- **Benchmark ID:** 59_tp_fe7b32
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [59, 60, 182, 204, 215, 224, 244, 247]
- **Retrieved Notes:** [60, 545, 204, 342, 667, 767, 867, 967]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.250 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.208 |
| R-Precision | 0.250 |
| Latency (ms) | 124.63 |
| Predicted Intent | question |
| Expected Intent | question |
| Intent Correct | True |

---

### RERANK — Operating systems exam preparation notes

- **Benchmark ID:** 59_tp_652a70
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [59, 132, 141, 146, 174, 179, 203, 205]
- **Retrieved Notes:** [59, 360, 70, 309, 527, 343, 593, 465]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.125 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.125 |
| R-Precision | 0.125 |
| Latency (ms) | 112.98 |
| Predicted Intent | reference |
| Expected Intent | study |
| Intent Correct | False |

---

### RERANK — CPU scheduling algorithms I need to know

- **Benchmark ID:** 59_tp_566c28
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [59, 132, 141, 146, 174, 179, 203, 205]
- **Retrieved Notes:** [179, 566, 710, 810, 910, 1010, 59, 634]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.125 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.125 |
| R-Precision | 0.250 |
| Latency (ms) | 132.02 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Study - Operating Systems |
| Category Correct | False |

---

### RERANK — Computer networking concepts for university

- **Benchmark ID:** 75_tp_eae57f
- **Difficulty:** medium
- **Challenge:** lexical
- **Relevant Notes:** [75, 118, 159, 162, 168, 180, 237, 276]
- **Retrieved Notes:** [327, 532, 491, 722, 822, 922, 1022, 633]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 99.48 |
| Predicted Intent | idea |
| Expected Intent | study |
| Intent Correct | False |

---

### RERANK — TCP/IP and HTTP protocol notes

- **Benchmark ID:** 75_tp_ac0c4f
- **Difficulty:** easy
- **Challenge:** lexical
- **Relevant Notes:** [75, 118, 159, 162, 168, 180, 237, 276]
- **Retrieved Notes:** [633, 654, 532, 159, 350, 75, 327, 189]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.125 |
| Hit | True |
| Reciprocal Rank | 0.250 |
| MAP@5 | 0.031 |
| R-Precision | 0.250 |
| Latency (ms) | 106.13 |
| Predicted Intent | reference |
| Expected Intent | study |
| Intent Correct | False |

---

### RERANK — Kubernetes cluster management notes

- **Benchmark ID:** 62_tp_d2020d
- **Difficulty:** medium
- **Challenge:** lexical
- **Relevant Notes:** [62, 118, 181, 230, 383, 410, 419, 548]
- **Retrieved Notes:** [62, 118, 712, 812, 912, 1012, 410, 383]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.250 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.250 |
| R-Precision | 0.500 |
| Latency (ms) | 117.20 |
| Predicted Intent | reference |
| Expected Intent | study |
| Intent Correct | False |

---

### RERANK — Container orchestration with K8s

- **Benchmark ID:** 62_tp_9d6d2c
- **Difficulty:** hard
- **Challenge:** lexical_gap
- **Relevant Notes:** [62, 118, 181, 230, 383, 410, 419, 548]
- **Retrieved Notes:** [62, 383, 75, 118, 712, 812, 912, 1012]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.600 |
| Recall@5 | 0.375 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.344 |
| R-Precision | 0.375 |
| Latency (ms) | 110.12 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Study - Kubernetes |
| Category Correct | False |

---

### RERANK — Authentication and JWT token notes

- **Benchmark ID:** 63_tp_d8d22b
- **Difficulty:** medium
- **Challenge:** lexical
- **Relevant Notes:** [63, 129, 165, 189, 227, 244, 276, 287]
- **Retrieved Notes:** [63, 541, 743, 843, 943, 1043, 408, 637]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.125 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.125 |
| R-Precision | 0.125 |
| Latency (ms) | 92.19 |
| Predicted Intent | reference |
| Expected Intent | study |
| Intent Correct | False |

---

### RERANK — How does OAuth 2.0 work?

- **Benchmark ID:** 63_tp_6690cb
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [63, 129, 165, 189, 227, 244, 276, 287]
- **Retrieved Notes:** [408, 63, 189, 697, 797, 897, 997, 1097]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.250 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| MAP@5 | 0.146 |
| R-Precision | 0.250 |
| Latency (ms) | 95.26 |
| Predicted Intent | question |
| Expected Intent | question |
| Intent Correct | True |

---

### RERANK — What eviction policies does Redis support?

- **Benchmark ID:** 61_tp_217848
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [61, 73, 92, 103, 124, 146, 157, 169]
- **Retrieved Notes:** [103, 73, 643, 673, 773, 873, 973, 1073]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.250 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.250 |
| R-Precision | 0.250 |
| Latency (ms) | 105.40 |
| Predicted Intent | question |
| Expected Intent | question |
| Intent Correct | True |

---

### RERANK — What types of indexes does PostgreSQL support?

- **Benchmark ID:** 58_tp_3d1edd
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [58, 66, 74, 104, 113, 114, 136, 139]
- **Retrieved Notes:** [104, 417, 731, 831, 931, 1031, 58, 66]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.125 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.125 |
| R-Precision | 0.375 |
| Latency (ms) | 109.92 |
| Predicted Intent | question |
| Expected Intent | question |
| Intent Correct | True |

---

### RERANK — When should I use GIN vs B-tree indexes?

- **Benchmark ID:** 58_tp_7b89c1
- **Difficulty:** hard
- **Challenge:** comparison
- **Relevant Notes:** [58, 66, 74, 104, 139]
- **Retrieved Notes:** [139, 686, 786, 886, 986, 1086, 301, 417]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.200 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.200 |
| R-Precision | 0.200 |
| Latency (ms) | 91.97 |
| Predicted Intent | question |
| Expected Intent | question |
| Intent Correct | True |

---

### RERANK — How does retrieval augmented generation work?

- **Benchmark ID:** 65_tp_d64f03
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [65, 114, 186, 197, 219, 222, 267, 296]
- **Retrieved Notes:** [65, 184, 186, 398, 119, 310, 140, 623]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.250 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.208 |
| R-Precision | 0.250 |
| Latency (ms) | 102.90 |
| Predicted Intent | question |
| Expected Intent | question |
| Intent Correct | True |

---

### RERANK — What are the steps in a RAG pipeline?

- **Benchmark ID:** 65_tp_0a59fb
- **Difficulty:** hard
- **Challenge:** semantic
- **Relevant Notes:** [65, 114, 186, 197, 219, 222, 267, 296]
- **Retrieved Notes:** [446, 730, 830, 930, 1030, 169, 612, 386]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 104.34 |
| Predicted Intent | question |
| Expected Intent | question |
| Intent Correct | True |

---

### RERANK — How are text embeddings generated?

- **Benchmark ID:** 168_tp_cc9fa1
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [168, 183, 228, 289, 298, 323, 376, 486]
- **Retrieved Notes:** [298, 726, 826, 926, 1026, 196, 531, 683]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.125 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.125 |
| R-Precision | 0.125 |
| Latency (ms) | 107.55 |
| Predicted Intent | question |
| Expected Intent | question |
| Intent Correct | True |

---

### RERANK — What is the difference between semantic and keyword search?

- **Benchmark ID:** 168_tp_df38ac
- **Difficulty:** hard
- **Challenge:** semantic
- **Relevant Notes:** [168, 183, 228, 289, 298, 323, 376, 486]
- **Retrieved Notes:** [86, 89, 252, 696, 796, 896, 996, 1096]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 99.76 |
| Predicted Intent | question |
| Expected Intent | question |
| Intent Correct | True |

---

### RERANK — What is due this week?

- **Benchmark ID:** 184_tp_c5a4df
- **Difficulty:** medium
- **Challenge:** temporal
- **Relevant Notes:** [233, 368, 498]
- **Retrieved Notes:** [77, 341, 423, 453, 393, 198, 216, 375]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 89.21 |
| Predicted Intent | question |
| Expected Intent | todo |
| Intent Correct | False |

---

### RERANK — Upcoming deadlines and submission dates

- **Benchmark ID:** 184_tp_cf679c
- **Difficulty:** medium
- **Challenge:** temporal
- **Relevant Notes:** [233, 368, 498]
- **Retrieved Notes:** [233, 498, 506, 411, 607, 753, 853, 953]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.667 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.667 |
| R-Precision | 0.667 |
| Latency (ms) | 104.31 |
| Predicted Intent | general |
| Expected Intent | todo |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Tasks |
| Category Correct | False |

---

### RERANK — Tasks I need to complete before month end

- **Benchmark ID:** 184_tp_96ea32
- **Difficulty:** hard
- **Challenge:** temporal
- **Relevant Notes:** [233, 368, 498]
- **Retrieved Notes:** [79, 82, 601, 498, 100, 453, 506, 524]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.333 |
| Hit | True |
| Reciprocal Rank | 0.250 |
| MAP@5 | 0.083 |
| R-Precision | 0.000 |
| Latency (ms) | 117.67 |
| Predicted Intent | todo |
| Expected Intent | todo |
| Intent Correct | True |
| Predicted Category | Tasks |
| Expected Category | Tasks |
| Category Correct | True |

---

### RERANK — What appointments have I booked this month?

- **Benchmark ID:** 78_tp_63adc1
- **Difficulty:** medium
- **Challenge:** temporal
- **Relevant Notes:** [78, 559]
- **Retrieved Notes:** [559, 79, 620, 601, 198, 216, 78, 609]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.500 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.500 |
| R-Precision | 0.500 |
| Latency (ms) | 96.46 |
| Predicted Intent | reminder |
| Expected Intent | reminder |
| Intent Correct | True |
| Predicted Category | Reminders |
| Expected Category | Appointments |
| Category Correct | False |

---

### RERANK — My upcoming travel and trip bookings

- **Benchmark ID:** 78_tp_a0f1d8
- **Difficulty:** easy
- **Challenge:** temporal
- **Relevant Notes:** [78, 81, 115]
- **Retrieved Notes:** [538, 627, 81, 539, 407, 128, 190, 115]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.333 |
| Hit | True |
| Reciprocal Rank | 0.333 |
| MAP@5 | 0.111 |
| R-Precision | 0.333 |
| Latency (ms) | 99.72 |
| Predicted Intent | general |
| Expected Intent | todo |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Travel |
| Category Correct | False |

---

### RERANK — Transport and accommodation I need to arrange

- **Benchmark ID:** 78_tp_219ffa
- **Difficulty:** medium
- **Challenge:** lexical_gap
- **Relevant Notes:** [78, 81, 115, 126, 128, 130, 160, 171]
- **Retrieved Notes:** [577, 538, 115, 128, 407, 606, 535, 190]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.250 |
| Hit | True |
| Reciprocal Rank | 0.333 |
| MAP@5 | 0.104 |
| R-Precision | 0.250 |
| Latency (ms) | 97.89 |
| Predicted Intent | general |
| Expected Intent | todo |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Travel |
| Category Correct | False |

---

### RERANK — Redis vs PostgreSQL — when to use each for persistence?

- **Benchmark ID:** 103_tp_7520ad
- **Difficulty:** hard
- **Challenge:** comparison
- **Relevant Notes:** [103, 104, 73, 74, 58, 92, 61]
- **Retrieved Notes:** [73, 61, 269, 724, 824, 924, 1024, 643]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.286 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.286 |
| R-Precision | 0.286 |
| Latency (ms) | 105.81 |
| Predicted Intent | question |
| Expected Intent | study |
| Intent Correct | False |

---

### RERANK — Docker vs Kubernetes — what is the difference?

- **Benchmark ID:** 72_tp_807260
- **Difficulty:** hard
- **Challenge:** comparison
- **Relevant Notes:** [118, 62, 383]
- **Retrieved Notes:** [118, 712, 812, 912, 1012, 105, 62, 383]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.333 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.333 |
| R-Precision | 0.333 |
| Latency (ms) | 110.99 |
| Predicted Intent | question |
| Expected Intent | study |
| Intent Correct | False |

---

### RERANK — How do I decide between hybrid retrieval and cross-encoder reranking?

- **Benchmark ID:** 65_tp_205f1c
- **Difficulty:** hard
- **Challenge:** multi_hop
- **Relevant Notes:** [67, 176, 119, 88, 123]
- **Retrieved Notes:** [67, 123, 676, 776, 876, 976, 1076, 119]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.400 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.400 |
| R-Precision | 0.400 |
| Latency (ms) | 107.72 |
| Predicted Intent | question |
| Expected Intent | study |
| Intent Correct | False |

---

### RERANK — What have I documented about retrieval quality in KnowledgeVault?

- **Benchmark ID:** 89_tp_0f29db
- **Difficulty:** hard
- **Challenge:** multi_hop
- **Relevant Notes:** [89, 485, 487, 402, 595, 88, 90]
- **Retrieved Notes:** [90, 310, 88, 555, 86, 89, 96, 251]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.286 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.238 |
| R-Precision | 0.429 |
| Latency (ms) | 95.15 |
| Predicted Intent | question |
| Expected Intent | reference |
| Intent Correct | False |

---

### RERANK — All my university and course study notes

- **Benchmark ID:** 58_tp_32b5cf
- **Difficulty:** easy
- **Challenge:** synthesis
- **Relevant Notes:** [58, 61, 62, 66, 69, 122, 130, 131]
- **Retrieved Notes:** [444, 290, 583, 699, 799, 899, 999, 1099]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 101.56 |
| Predicted Intent | study |
| Expected Intent | study |
| Intent Correct | True |

---

### RERANK — All my brainstorming and ideation notes

- **Benchmark ID:** 85_tp_f46697
- **Difficulty:** easy
- **Challenge:** synthesis
- **Relevant Notes:** [85, 86, 117, 143, 157, 178, 225, 240]
- **Retrieved Notes:** [85, 459, 87, 416, 617, 525, 444, 568]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.125 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.125 |
| R-Precision | 0.125 |
| Latency (ms) | 118.21 |
| Predicted Intent | idea |
| Expected Intent | idea |
| Intent Correct | True |
| Predicted Category | Ideas - AI Summarization |
| Expected Category | Ideas |
| Category Correct | True |

---

### RERANK — My technical reference cheat sheets

- **Benchmark ID:** 72_tp_32bacd
- **Difficulty:** easy
- **Challenge:** synthesis
- **Relevant Notes:** [72, 73, 74, 75, 122, 135]
- **Retrieved Notes:** [309, 74, 485, 110, 235, 547, 360, 69]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.167 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| MAP@5 | 0.083 |
| R-Precision | 0.167 |
| Latency (ms) | 123.79 |
| Predicted Intent | reference |
| Expected Intent | reference |
| Intent Correct | True |

---

### RERANK — All my communication and message drafts

- **Benchmark ID:** 54_tp_b42b02
- **Difficulty:** easy
- **Challenge:** synthesis
- **Relevant Notes:** [54, 56, 57, 106, 132, 141]
- **Retrieved Notes:** [371, 141, 56, 582, 290, 382, 423, 415]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.333 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| MAP@5 | 0.194 |
| R-Precision | 0.333 |
| Latency (ms) | 86.25 |
| Predicted Intent | communication |
| Expected Intent | communication |
| Intent Correct | True |

---

### RERANK — Errands I need to run today

- **Benchmark ID:** 76_tp_c52e4b
- **Difficulty:** medium
- **Challenge:** lexical_gap
- **Relevant Notes:** [76, 164, 190, 202, 286, 309, 322, 475]
- **Retrieved Notes:** [475, 79, 375, 735, 835, 935, 1035, 77]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.125 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.125 |
| R-Precision | 0.125 |
| Latency (ms) | 97.54 |
| Predicted Intent | general |
| Expected Intent | todo |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | To Do |
| Category Correct | False |

---

### RERANK — Things I need to pick up from the store

- **Benchmark ID:** 76_tp_c74a5f
- **Difficulty:** easy
- **Challenge:** lexical_gap
- **Relevant Notes:** [76, 164, 190, 202, 286, 309, 322, 475]
- **Retrieved Notes:** [76, 322, 475, 393, 589, 659, 759, 859]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.600 |
| Recall@5 | 0.375 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.375 |
| R-Precision | 0.375 |
| Latency (ms) | 185.68 |
| Predicted Intent | general |
| Expected Intent | todo |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Shopping |
| Category Correct | False |

---

### RERANK — Physical training and exercise plan

- **Benchmark ID:** 173_tp_f41c30
- **Difficulty:** easy
- **Challenge:** lexical_gap
- **Relevant Notes:** [173, 202, 291, 317, 380, 621, 631, 680]
- **Retrieved Notes:** [83, 631, 481, 437, 621, 107, 317, 380]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.250 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| MAP@5 | 0.113 |
| R-Precision | 0.500 |
| Latency (ms) | 110.24 |
| Predicted Intent | general |
| Expected Intent | todo |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Health |
| Category Correct | False |

---

### RERANK — How am I planning to stay healthy?

- **Benchmark ID:** 173_tp_7bafaa
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [173, 202, 291, 317, 380, 621, 631, 680]
- **Retrieved Notes:** [83, 212, 79, 84, 286, 380, 680, 780]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.167 |
| MAP@5 | 0.000 |
| R-Precision | 0.250 |
| Latency (ms) | 93.18 |
| Predicted Intent | question |
| Expected Intent | question |
| Intent Correct | True |

---

### RERANK — How much am I spending per month?

- **Benchmark ID:** 82_tp_86df0e
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [82, 210, 216, 281, 331, 345, 407, 535]
- **Retrieved Notes:** [216, 82, 331, 281, 490, 434, 341, 77]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.800 |
| Recall@5 | 0.500 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.500 |
| R-Precision | 0.500 |
| Latency (ms) | 92.98 |
| Predicted Intent | question |
| Expected Intent | question |
| Intent Correct | True |

---

### RERANK — Personal finance tracking notes

- **Benchmark ID:** 82_tp_3665b0
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [82, 210, 216, 281, 331, 345, 407, 535]
- **Retrieved Notes:** [87, 82, 216, 285, 393, 637, 733, 833]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.250 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| MAP@5 | 0.146 |
| R-Precision | 0.250 |
| Latency (ms) | 96.84 |
| Predicted Intent | reference |
| Expected Intent | reference |
| Intent Correct | True |

---

### RERANK — BRPOPLPUSH reliable queue implementation

- **Benchmark ID:** 246_tp_6ef122
- **Difficulty:** hard
- **Challenge:** exact_phrase
- **Relevant Notes:** [246, 433, 643, 673, 684, 705, 773, 784]
- **Retrieved Notes:** [643, 673, 773, 873, 973, 1073, 246, 684]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.600 |
| Recall@5 | 0.375 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.375 |
| R-Precision | 0.625 |
| Latency (ms) | 99.54 |
| Predicted Intent | general |
| Expected Intent | reference |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Reference - Redis |
| Category Correct | False |

---

### RERANK — ACID properties of databases

- **Benchmark ID:** 229_tp_454ff2
- **Difficulty:** easy
- **Challenge:** exact_phrase
- **Relevant Notes:** [229, 690, 790, 890, 990, 1090]
- **Retrieved Notes:** [229, 690, 790, 890, 990, 1090, 321, 707]

| Metric | Value |
|-------|------:|
| Precision@5 | 1.000 |
| Recall@5 | 0.833 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.833 |
| R-Precision | 1.000 |
| Latency (ms) | 104.65 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Study - DBMS |
| Category Correct | False |

---

### RERANK — RRF score combination for hybrid search

- **Benchmark ID:** 518_tp_930ea0
- **Difficulty:** hard
- **Challenge:** exact_phrase
- **Relevant Notes:** [518, 718, 818, 918, 1018]
- **Retrieved Notes:** [518, 718, 818, 918, 1018, 252, 696, 796]

| Metric | Value |
|-------|------:|
| Precision@5 | 1.000 |
| Recall@5 | 1.000 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 1.000 |
| R-Precision | 1.000 |
| Latency (ms) | 103.64 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Study - AI |
| Category Correct | False |

---

### RERANK — HNSW approximate nearest neighbor algorithm

- **Benchmark ID:** 215_tp_55df73
- **Difficulty:** hard
- **Challenge:** exact_phrase
- **Relevant Notes:** [215, 430, 681, 781, 881, 981, 1081]
- **Retrieved Notes:** [215, 681, 781, 881, 981, 1081, 430, 536]

| Metric | Value |
|-------|------:|
| Precision@5 | 1.000 |
| Recall@5 | 0.714 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.714 |
| R-Precision | 1.000 |
| Latency (ms) | 96.26 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Study - AI |
| Category Correct | False |

---

### RERANK — What do I need to buy this weekend?

- **Benchmark ID:** 76_tp_5c724a
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [76, 164, 190, 202, 309, 322, 393, 475]
- **Retrieved Notes:** [77, 110, 554, 76, 322, 393, 286, 115]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.250 |
| Hit | True |
| Reciprocal Rank | 0.250 |
| MAP@5 | 0.081 |
| R-Precision | 0.375 |
| Latency (ms) | 119.41 |
| Predicted Intent | todo |
| Expected Intent | todo |
| Intent Correct | True |
| Predicted Category | Tasks |
| Expected Category | Shopping |
| Category Correct | True |

---

### RERANK — All my pending reminders and follow-ups

- **Benchmark ID:** 55_tp_3ff20c
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [55, 152, 212, 312, 542, 557]
- **Retrieved Notes:** [79, 191, 312, 392, 372, 620, 382, 475]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.167 |
| Hit | True |
| Reciprocal Rank | 0.333 |
| MAP@5 | 0.056 |
| R-Precision | 0.167 |
| Latency (ms) | 103.09 |
| Predicted Intent | reminder |
| Expected Intent | reminder |
| Intent Correct | True |
| Predicted Category | Reminders |
| Expected Category | Reminders |
| Category Correct | True |

---

### RERANK — What have I told myself not to forget?

- **Benchmark ID:** 55_tp_05e927
- **Difficulty:** medium
- **Challenge:** lexical_gap
- **Relevant Notes:** [55, 152, 212, 312, 542, 557]
- **Retrieved Notes:** [212, 647, 475, 290, 505, 380, 680, 780]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.167 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.167 |
| R-Precision | 0.167 |
| Latency (ms) | 97.96 |
| Predicted Intent | question |
| Expected Intent | reminder |
| Intent Correct | False |

---

### RERANK — LeetCode patterns and problem-solving techniques

- **Benchmark ID:** 117_tp_44e6df
- **Difficulty:** medium
- **Challenge:** lexical
- **Relevant Notes:** [117, 127, 187, 224, 271, 279, 282, 316]
- **Retrieved Notes:** [224, 611, 316, 187, 546, 117, 399, 387]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.600 |
| Recall@5 | 0.375 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.302 |
| R-Precision | 0.500 |
| Latency (ms) | 111.57 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Study - Interview Prep |
| Category Correct | False |

---

### RERANK — How do I approach dynamic programming questions?

- **Benchmark ID:** 117_tp_7bf7d7
- **Difficulty:** hard
- **Challenge:** semantic
- **Relevant Notes:** [117, 127, 187, 224, 271, 279, 282, 316]
- **Retrieved Notes:** [562, 459, 117, 352, 302, 398, 70, 227]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.125 |
| Hit | True |
| Reciprocal Rank | 0.333 |
| MAP@5 | 0.042 |
| R-Precision | 0.125 |
| Latency (ms) | 137.94 |
| Predicted Intent | question |
| Expected Intent | question |
| Intent Correct | True |

---

### RERANK — System design concepts I need to review

- **Benchmark ID:** 70_tp_39b780
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [70, 145, 267, 305, 309, 334, 344, 346]
- **Retrieved Notes:** [392, 70, 360, 309, 99, 106, 439, 102]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.250 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| MAP@5 | 0.125 |
| R-Precision | 0.250 |
| Latency (ms) | 129.33 |
| Predicted Intent | idea |
| Expected Intent | study |
| Intent Correct | False |

---

### RERANK — How do I design a scalable URL shortener?

- **Benchmark ID:** 70_tp_c6f60d
- **Difficulty:** hard
- **Challenge:** semantic
- **Relevant Notes:** [70, 145, 267, 305, 309, 334, 344, 346]
- **Retrieved Notes:** [602, 93, 346, 386, 644, 61, 219, 215]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.125 |
| Hit | True |
| Reciprocal Rank | 0.333 |
| MAP@5 | 0.042 |
| R-Precision | 0.125 |
| Latency (ms) | 133.31 |
| Predicted Intent | question |
| Expected Intent | question |
| Intent Correct | True |

---

### RERANK — Behavioral interview story preparation

- **Benchmark ID:** 83_tp_a140c7
- **Difficulty:** medium
- **Challenge:** lexical
- **Relevant Notes:** [83, 85, 113, 114, 116, 131, 134, 135]
- **Retrieved Notes:** [468, 294, 360, 344, 263, 288, 70, 100]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 105.76 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Study - Interview Prep |
| Category Correct | False |

---

### RERANK — Resume writing tips and improvement notes

- **Benchmark ID:** 100_tp_b51d58
- **Difficulty:** easy
- **Challenge:** lexical
- **Relevant Notes:** [100, 142, 185, 270, 523, 525]
- **Retrieved Notes:** [142, 100, 185, 415, 87, 203, 525, 583]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.600 |
| Recall@5 | 0.500 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.500 |
| R-Precision | 0.500 |
| Latency (ms) | 102.36 |
| Predicted Intent | reference |
| Expected Intent | reference |
| Intent Correct | True |

---

### RERANK — How should I write my software engineer resume?

- **Benchmark ID:** 100_tp_fcae97
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [100, 142, 185, 270, 523, 525]
- **Retrieved Notes:** [100, 142, 525, 185, 330, 496, 352, 272]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.800 |
| Recall@5 | 0.667 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.667 |
| R-Precision | 0.667 |
| Latency (ms) | 101.49 |
| Predicted Intent | question |
| Expected Intent | question |
| Intent Correct | True |

---

### RERANK — Books I am reading or have read recently

- **Benchmark ID:** 78_tp_c601ae
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [78, 128, 155, 160, 172, 182, 194, 234]
- **Retrieved Notes:** [240, 528, 290, 309, 565, 439, 235, 360]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 108.90 |
| Predicted Intent | general |
| Expected Intent | reference |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Reference - Books |
| Category Correct | False |

---

### RERANK — Reading list and book notes

- **Benchmark ID:** 78_tp_0f3259
- **Difficulty:** easy
- **Challenge:** lexical
- **Relevant Notes:** [78, 128, 155, 160, 172, 182, 194, 234]
- **Retrieved Notes:** [87, 444, 235, 290, 203, 240, 583, 699]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 101.00 |
| Predicted Intent | reference |
| Expected Intent | reference |
| Intent Correct | True |

---

### RERANK — Habit formation notes from Atomic Habits

- **Benchmark ID:** 304_tp_4994bc
- **Difficulty:** easy
- **Challenge:** lexical
- **Relevant Notes:** [304, 317, 482, 557, 631, 634, 698, 734]
- **Retrieved Notes:** [482, 73, 557, 318, 116, 467, 224, 342]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.250 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.208 |
| R-Precision | 0.250 |
| Latency (ms) | 100.34 |
| Predicted Intent | reference |
| Expected Intent | study |
| Intent Correct | False |

---

### RERANK — Summary of James Clear's key ideas on habits

- **Benchmark ID:** 304_tp_37657b
- **Difficulty:** medium
- **Challenge:** lexical_gap
- **Relevant Notes:** [304, 317, 482, 557, 631, 634, 698, 734]
- **Retrieved Notes:** [482, 240, 496, 309, 235, 234, 469, 438]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.125 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.125 |
| R-Precision | 0.125 |
| Latency (ms) | 100.51 |
| Predicted Intent | idea |
| Expected Intent | study |
| Intent Correct | False |

---

### RERANK — Online courses and tutorials I am taking

- **Benchmark ID:** 71_tp_43e20b
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [71, 145, 231, 266, 357, 394, 417, 471]
- **Retrieved Notes:** [471, 663, 763, 863, 963, 1063, 357, 343]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.125 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.125 |
| R-Precision | 0.250 |
| Latency (ms) | 90.38 |
| Predicted Intent | study |
| Expected Intent | study |
| Intent Correct | True |

---

### RERANK — Sleep improvement techniques and tips

- **Benchmark ID:** 133_tp_12eb56
- **Difficulty:** medium
- **Challenge:** lexical
- **Relevant Notes:** [133, 136, 202, 288, 348, 380, 434, 538]
- **Retrieved Notes:** [622, 434, 574, 317, 548, 348, 664, 764]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.125 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| MAP@5 | 0.062 |
| R-Precision | 0.250 |
| Latency (ms) | 102.50 |
| Predicted Intent | general |
| Expected Intent | reference |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Reference - Health |
| Category Correct | False |

---

### RERANK — How can I improve my sleep quality?

- **Benchmark ID:** 133_tp_2c6b3e
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [133, 136, 202, 288, 348, 380, 434, 538]
- **Retrieved Notes:** [434, 622, 574, 548, 317, 133, 348, 664]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.125 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.125 |
| R-Precision | 0.375 |
| Latency (ms) | 83.32 |
| Predicted Intent | question |
| Expected Intent | question |
| Intent Correct | True |

---

### RERANK — Nutrition and supplement tracking notes

- **Benchmark ID:** 109_tp_f852f9
- **Difficulty:** easy
- **Challenge:** semantic
- **Relevant Notes:** [109, 133, 226, 286]
- **Retrieved Notes:** [286, 133, 322, 285, 216, 393, 87, 444]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.500 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.500 |
| R-Precision | 0.500 |
| Latency (ms) | 85.92 |
| Predicted Intent | reference |
| Expected Intent | reference |
| Intent Correct | True |

---

### RERANK — What supplements should I be taking?

- **Benchmark ID:** 109_tp_f444c2
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [109, 133, 226, 286]
- **Retrieved Notes:** [133, 286, 226, 109, 84, 322, 83, 631]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.800 |
| Recall@5 | 1.000 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 1.000 |
| R-Precision | 1.000 |
| Latency (ms) | 92.52 |
| Predicted Intent | question |
| Expected Intent | question |
| Intent Correct | True |

---

### RERANK — Mental health practices and coping strategies

- **Benchmark ID:** 152_tp_3685ae
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [152, 288, 317, 472, 575]
- **Retrieved Notes:** [288, 575, 212, 472, 201, 380, 680, 780]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.600 |
| Recall@5 | 0.600 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.550 |
| R-Precision | 0.600 |
| Latency (ms) | 111.22 |
| Predicted Intent | general |
| Expected Intent | reference |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Reference - Health |
| Category Correct | False |

---

### RERANK — My notes on managing stress and anxiety

- **Benchmark ID:** 152_tp_5aba2a
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [152, 288, 317, 472, 575]
- **Retrieved Notes:** [288, 472, 212, 356, 539, 290, 360, 482]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.400 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| MAP@5 | 0.400 |
| R-Precision | 0.400 |
| Latency (ms) | 99.02 |
| Predicted Intent | reference |
| Expected Intent | reference |
| Intent Correct | True |

---

### RERANK — Plans for open source and public building

- **Benchmark ID:** 117_tp_eab7a3
- **Difficulty:** medium
- **Challenge:** semantic
- **Relevant Notes:** [117, 141, 395, 400, 440, 453, 522, 554]
- **Retrieved Notes:** [255, 141, 554, 117, 106, 555, 175, 178]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.600 |
| Recall@5 | 0.375 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| MAP@5 | 0.240 |
| R-Precision | 0.375 |
| Latency (ms) | 105.98 |
| Predicted Intent | general |
| Expected Intent | idea |
| Intent Correct | False |
| Predicted Category | General |
| Expected Category | Ideas |
| Category Correct | False |

---

### RERANK — Notes on growing my developer presence online

- **Benchmark ID:** 117_tp_594cbf
- **Difficulty:** medium
- **Challenge:** lexical_gap
- **Relevant Notes:** [117, 141, 395, 400, 440, 453, 522, 554]
- **Retrieved Notes:** [255, 330, 141, 155, 555, 85, 106, 439]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.125 |
| Hit | True |
| Reciprocal Rank | 0.333 |
| MAP@5 | 0.042 |
| R-Precision | 0.125 |
| Latency (ms) | 91.32 |
| Predicted Intent | reference |
| Expected Intent | idea |
| Intent Correct | False |

---

### RERANK — Fortran programming and legacy code notes

- **Benchmark ID:** 0_tp_07253f
- **Difficulty:** hard
- **Challenge:** negative
- **Relevant Notes:** []
- **Retrieved Notes:** [465, 547, 227, 169, 389, 110, 471, 663]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 103.37 |
| Predicted Intent | reference |
| Expected Intent | general |
| Intent Correct | False |

---

### RERANK — Ancient history and archaeology notes

- **Benchmark ID:** 0_tp_13e990
- **Difficulty:** hard
- **Challenge:** negative
- **Relevant Notes:** []
- **Retrieved Notes:** [565, 290, 372, 386, 619, 444, 637, 733]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 81.73 |
| Predicted Intent | reference |
| Expected Intent | general |
| Intent Correct | False |

---

### RERANK — Wine and cheese pairing recommendations

- **Benchmark ID:** 0_tp_f9589c
- **Difficulty:** hard
- **Challenge:** negative
- **Relevant Notes:** []
- **Retrieved Notes:** [81, 363, 104, 140, 217, 332, 342, 362]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 100.30 |
| Predicted Intent | general |
| Expected Intent | general |
| Intent Correct | True |
| Predicted Category | General |
| Expected Category | General |
| Category Correct | True |

---

### RERANK — Piano lessons and music theory notes

- **Benchmark ID:** 0_tp_5abfd7
- **Difficulty:** hard
- **Challenge:** negative
- **Relevant Notes:** []
- **Retrieved Notes:** [444, 290, 87, 637, 733, 833, 933, 1033]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 86.87 |
| Predicted Intent | reference |
| Expected Intent | general |
| Intent Correct | False |

---

### RERANK — Gardening and plant care notes

- **Benchmark ID:** 0_tp_4fb99e
- **Difficulty:** hard
- **Challenge:** negative
- **Relevant Notes:** []
- **Retrieved Notes:** [583, 699, 799, 899, 999, 1099, 475, 110]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| MAP@5 | 0.000 |
| R-Precision | 0.000 |
| Latency (ms) | 252.87 |
| Predicted Intent | reference |
| Expected Intent | general |
| Intent Correct | False |

---


---

_Generated automatically by the KnowledgeVault Evaluation Framework._