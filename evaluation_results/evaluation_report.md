# KnowledgeVault Evaluation Report

**Run ID:** `e2081ca6-b684-44e7-881f-2ca27226ef4a`

**Created:** 2026-07-26T13:52:02.725691

**Queries:** 152

**K:** 5

## Strategy Comparison

| Strategy | Precision | Recall | Hit Rate | MRR | Intent Acc | Category Acc | Avg Latency (ms) |
|-----------|----------:|-------:|---------:|----:|------------:|-------------:|-----------------:|
| SEMANTIC | 0.307 | 0.208 | 0.743 | 0.553 | - | - | 1.31 |
| INTENT | 0.005 | 0.003 | 0.013 | 0.009 | 0.145 | 0.773 | 28.61 |
| HYBRID | 0.308 | 0.209 | 0.743 | 0.587 | 0.145 | 0.773 | 98.66 |

## Query Results

### SEMANTIC — What are useful Python tips and tricks I've learned?

- **Benchmark ID:** 1
- **Difficulty:** easy
- **Relevant Notes:** [108, 174, 177, 206, 232, 239, 272, 283]
- **Retrieved Notes:** [318, 206, 633, 357, 464]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.125 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| Latency (ms) | 21.90 |

---

### SEMANTIC — Show my Python programming notes

- **Benchmark ID:** 2
- **Difficulty:** easy
- **Relevant Notes:** [108, 174, 177, 206, 232, 239, 272, 283]
- **Retrieved Notes:** [87, 799, 583, 699, 899]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 3.10 |

---

### SEMANTIC — Notes about Python dictionaries and hash maps

- **Benchmark ID:** 3
- **Difficulty:** easy
- **Relevant Notes:** [108, 271, 278, 284, 397, 464, 483, 560, 579, 587]
- **Retrieved Notes:** [284, 587, 397, 464, 745]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.800 |
| Recall@5 | 0.400 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 1.14 |

---

### SEMANTIC — How does Python async programming work?

- **Benchmark ID:** 4
- **Difficulty:** medium
- **Relevant Notes:** [170, 283, 304, 359, 364, 372, 471, 661, 662, 663]
- **Retrieved Notes:** [934, 304, 734, 834, 1034]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.100 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| Latency (ms) | 1.25 |

---

### SEMANTIC — Concurrency and asynchronous patterns in Python

- **Benchmark ID:** 5
- **Difficulty:** medium
- **Relevant Notes:** [170, 283, 304, 359, 364, 372, 471, 661, 662, 663]
- **Retrieved Notes:** [834, 934, 304, 734, 1034]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.100 |
| Hit | True |
| Reciprocal Rank | 0.333 |
| Latency (ms) | 0.80 |

---

### SEMANTIC — Python decorator notes

- **Benchmark ID:** 6
- **Difficulty:** easy
- **Relevant Notes:** [174, 414, 435, 455, 549, 610, 614]
- **Retrieved Notes:** [610, 549, 177, 318, 414]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.600 |
| Recall@5 | 0.429 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 0.85 |

---

### SEMANTIC — What git commands and workflows have I noted?

- **Benchmark ID:** 7
- **Difficulty:** easy
- **Relevant Notes:** [130, 135, 144, 169, 229, 272, 317, 328, 366, 395]
- **Retrieved Notes:** [612, 328, 501, 614, 522]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.100 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| Latency (ms) | 1.98 |

---

### SEMANTIC — Git tips and tricks

- **Benchmark ID:** 8
- **Difficulty:** easy
- **Relevant Notes:** [130, 135, 144, 169, 229, 272, 317, 328, 366, 395]
- **Retrieved Notes:** [646, 719, 819, 497, 919]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 4.54 |

---

### SEMANTIC — JavaScript and TypeScript notes

- **Benchmark ID:** 9
- **Difficulty:** easy
- **Relevant Notes:** [218, 220, 250, 297, 418, 713, 720, 813, 820, 913]
- **Retrieved Notes:** [913, 813, 218, 713, 1013]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.800 |
| Recall@5 | 0.400 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 3.19 |

---

### SEMANTIC — What have I learned about Go programming?

- **Benchmark ID:** 10
- **Difficulty:** medium
- **Relevant Notes:** [114, 138, 206, 208, 266, 297, 320, 339, 488, 512]
- **Retrieved Notes:** [572, 798, 634, 698, 898]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 2.10 |

---

### SEMANTIC — Rust ownership and borrowing notes

- **Benchmark ID:** 11
- **Difficulty:** medium
- **Relevant Notes:** [151, 182, 210, 351, 370, 380, 459, 494, 539, 563]
- **Retrieved Notes:** [789, 889, 689, 370, 989]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.100 |
| Hit | True |
| Reciprocal Rank | 0.250 |
| Latency (ms) | 1.46 |

---

### SEMANTIC — What design patterns have I documented?

- **Benchmark ID:** 12
- **Difficulty:** medium
- **Relevant Notes:** [102, 121, 189, 203, 224, 238, 246, 254, 266, 269]
- **Retrieved Notes:** [102, 121, 787, 687, 887]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.200 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 1.24 |

---

### SEMANTIC — Software design patterns notes

- **Benchmark ID:** 13
- **Difficulty:** easy
- **Relevant Notes:** [102, 121, 189, 203, 224, 238, 246, 254, 266, 269]
- **Retrieved Notes:** [102, 106, 309, 121, 687]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.200 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 1.76 |

---

### SEMANTIC — Performance optimization notes

- **Benchmark ID:** 14
- **Difficulty:** medium
- **Relevant Notes:** [93, 98, 108, 142, 159, 160, 183, 195, 196, 213]
- **Retrieved Notes:** [195, 547, 58, 530, 738]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.100 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 1.90 |

---

### SEMANTIC — SQL tips and advanced query techniques

- **Benchmark ID:** 15
- **Difficulty:** medium
- **Relevant Notes:** [58, 69, 74, 104, 123, 136, 139, 144, 175, 176]
- **Retrieved Notes:** [398, 184, 385, 402, 58]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.100 |
| Hit | True |
| Reciprocal Rank | 0.200 |
| Latency (ms) | 0.97 |

---

### SEMANTIC — Regular expression notes and examples

- **Benchmark ID:** 16
- **Difficulty:** easy
- **Relevant Notes:** [102, 121, 135, 148, 189, 224, 238, 246, 254, 266]
- **Retrieved Notes:** [135, 148, 515, 489, 227]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.200 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 0.92 |

---

### SEMANTIC — Shell and command line tips I've collected

- **Benchmark ID:** 17
- **Difficulty:** easy
- **Relevant Notes:** [147, 153, 243, 314, 355, 374, 379, 455, 597, 688]
- **Retrieved Notes:** [597, 268, 682, 782, 882]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.100 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 2.10 |

---

### SEMANTIC — What do I know about RAG systems?

- **Benchmark ID:** 18
- **Difficulty:** medium
- **Relevant Notes:** [65, 114, 186, 197, 219, 222, 267, 296, 310, 376]
- **Retrieved Notes:** [386, 436, 470, 565, 197]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.100 |
| Hit | True |
| Reciprocal Rank | 0.200 |
| Latency (ms) | 1.14 |

---

### SEMANTIC — Retrieval augmented generation notes

- **Benchmark ID:** 19
- **Difficulty:** easy
- **Relevant Notes:** [65, 114, 186, 197, 219, 222, 267, 296, 310, 376]
- **Retrieved Notes:** [65, 186, 398, 184, 289]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.200 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 1.71 |

---

### SEMANTIC — Notes about embeddings and vector search

- **Benchmark ID:** 20
- **Difficulty:** medium
- **Relevant Notes:** [168, 183, 228, 289, 298, 323, 376, 486, 487, 523]
- **Retrieved Notes:** [196, 333, 726, 298, 826]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.100 |
| Hit | True |
| Reciprocal Rank | 0.250 |
| Latency (ms) | 1.44 |

---

### SEMANTIC — How do text embeddings work?

- **Benchmark ID:** 21
- **Difficulty:** medium
- **Relevant Notes:** [168, 183, 228, 289, 298, 323, 376, 486, 487, 523]
- **Retrieved Notes:** [826, 926, 298, 726, 1026]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.100 |
| Hit | True |
| Reciprocal Rank | 0.333 |
| Latency (ms) | 2.14 |

---

### SEMANTIC — Large language model notes and findings

- **Benchmark ID:** 22
- **Difficulty:** medium
- **Relevant Notes:** [60, 119, 122, 136, 143, 186, 251, 268, 313, 329]
- **Retrieved Notes:** [186, 404, 808, 708, 908]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.100 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 1.28 |

---

### SEMANTIC — What LLMs have I worked with?

- **Benchmark ID:** 23
- **Difficulty:** easy
- **Relevant Notes:** [60, 119, 122, 136, 143, 186, 251, 268, 313, 329]
- **Retrieved Notes:** [143, 543, 427, 509, 268]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.200 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 1.68 |

---

### SEMANTIC — Document chunking strategy notes

- **Benchmark ID:** 24
- **Difficulty:** medium
- **Relevant Notes:** [197, 214, 257, 268, 289, 432, 446, 478, 487, 510]
- **Retrieved Notes:** [558, 821, 533, 721, 921]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 1.14 |

---

### SEMANTIC — Notes about reranking in search systems

- **Benchmark ID:** 25
- **Difficulty:** hard
- **Relevant Notes:** [67, 119, 123, 176, 386, 648, 676, 776, 876, 976]
- **Retrieved Notes:** [67, 176, 119, 305, 58]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.600 |
| Recall@5 | 0.300 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 0.84 |

---

### SEMANTIC — RAG and retrieval evaluation metrics

- **Benchmark ID:** 26
- **Difficulty:** hard
- **Relevant Notes:** [90, 119, 210, 310, 402, 485, 487, 595]
- **Retrieved Notes:** [386, 485, 310, 595, 186]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.600 |
| Recall@5 | 0.375 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| Latency (ms) | 0.82 |

---

### SEMANTIC — How do I measure retrieval quality?

- **Benchmark ID:** 27
- **Difficulty:** hard
- **Relevant Notes:** [90, 119, 210, 310, 402, 485, 487, 595]
- **Retrieved Notes:** [310, 86, 485, 402, 213]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.600 |
| Recall@5 | 0.375 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 1.11 |

---

### SEMANTIC — LLM fine-tuning and alignment notes

- **Benchmark ID:** 28
- **Difficulty:** hard
- **Relevant Notes:** [118, 129, 137, 143, 157, 171, 178, 196, 264, 328]
- **Retrieved Notes:** [592, 143, 613, 268, 682]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.100 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| Latency (ms) | 1.01 |

---

### SEMANTIC — Prompting techniques and tips

- **Benchmark ID:** 29
- **Difficulty:** medium
- **Relevant Notes:** [130, 191, 264, 268, 406, 436, 446, 456, 467, 493]
- **Retrieved Notes:** [406, 264, 507, 459, 199]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.200 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 1.13 |

---

### SEMANTIC — What have I learned about LLM prompting?

- **Benchmark ID:** 30
- **Difficulty:** easy
- **Relevant Notes:** [130, 191, 264, 268, 406, 436, 446, 456, 467, 493]
- **Retrieved Notes:** [882, 268, 682, 782, 982]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.100 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| Latency (ms) | 0.79 |

---

### SEMANTIC — Notes about LLM hallucination and grounding

- **Benchmark ID:** 31
- **Difficulty:** medium
- **Relevant Notes:** [197, 222, 446, 470, 485, 600, 730, 830, 930, 1030]
- **Retrieved Notes:** [197, 478, 600, 651, 716]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.200 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 1.40 |

---

### SEMANTIC — HyDE and query expansion techniques

- **Benchmark ID:** 32
- **Difficulty:** hard
- **Relevant Notes:** [531, 683, 783, 883, 983, 1083]
- **Retrieved Notes:** [184, 531, 783, 683, 883]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.800 |
| Recall@5 | 0.667 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| Latency (ms) | 0.91 |

---

### SEMANTIC — Operating systems study notes

- **Benchmark ID:** 33
- **Difficulty:** medium
- **Relevant Notes:** [59, 132, 141, 146, 174, 179, 203, 205, 233, 255]
- **Retrieved Notes:** [59, 527, 106, 547, 465]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.100 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 0.85 |

---

### SEMANTIC — OS concepts I need to review for exams

- **Benchmark ID:** 34
- **Difficulty:** easy
- **Relevant Notes:** [59, 132, 141, 146, 174, 179, 203, 205, 233, 255]
- **Retrieved Notes:** [360, 59, 309, 169, 527]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.100 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| Latency (ms) | 0.81 |

---

### SEMANTIC — Database management systems notes

- **Benchmark ID:** 35
- **Difficulty:** medium
- **Relevant Notes:** [139, 144, 198, 229, 252, 308, 321, 417, 425, 593]
- **Retrieved Notes:** [425, 231, 439, 608, 144]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.200 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 0.81 |

---

### SEMANTIC — Computer networks study notes

- **Benchmark ID:** 36
- **Difficulty:** medium
- **Relevant Notes:** [75, 118, 159, 162, 168, 180, 237, 276, 280, 298]
- **Retrieved Notes:** [327, 532, 106, 99, 439]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 1.11 |

---

### SEMANTIC — Algorithm and data structures notes

- **Benchmark ID:** 37
- **Difficulty:** medium
- **Relevant Notes:** [59, 60, 116, 156, 182, 204, 215, 244, 247, 261]
- **Retrieved Notes:** [838, 938, 738, 530, 1038]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 0.85 |

---

### SEMANTIC — What algorithms have I studied?

- **Benchmark ID:** 38
- **Difficulty:** easy
- **Relevant Notes:** [59, 60, 116, 156, 182, 204, 215, 244, 247, 261]
- **Retrieved Notes:** [619, 60, 333, 66, 536]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.100 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| Latency (ms) | 1.53 |

---

### SEMANTIC — Compiler design and theory of computation notes

- **Benchmark ID:** 39
- **Difficulty:** hard
- **Relevant Notes:** [148, 227, 228, 241, 311, 578, 633]
- **Retrieved Notes:** [227, 547, 465, 311, 530]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.286 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 1.22 |

---

### SEMANTIC — Capstone project notes

- **Benchmark ID:** 40
- **Difficulty:** medium
- **Relevant Notes:** [175, 190, 199, 225, 233, 236, 263, 277, 285, 382]
- **Retrieved Notes:** [568, 233, 498, 382, 175]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.600 |
| Recall@5 | 0.300 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| Latency (ms) | 1.08 |

---

### SEMANTIC — Parallel programming and concurrency notes

- **Benchmark ID:** 41
- **Difficulty:** hard
- **Relevant Notes:** [151, 229, 283, 287, 296, 304, 421, 462, 474, 504]
- **Retrieved Notes:** [296, 283, 762, 662, 862]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.200 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 0.78 |

---

### SEMANTIC — LeetCode problem patterns and solutions

- **Benchmark ID:** 42
- **Difficulty:** medium
- **Relevant Notes:** [117, 127, 187, 224, 271, 279, 282, 316, 327, 387]
- **Retrieved Notes:** [224, 611, 316, 399, 546]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.200 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 0.85 |

---

### SEMANTIC — Dynamic programming notes and patterns

- **Benchmark ID:** 43
- **Difficulty:** hard
- **Relevant Notes:** [118, 129, 152, 157, 178, 224, 271, 328, 349, 399]
- **Retrieved Notes:** [562, 227, 701, 460, 801]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 0.81 |

---

### SEMANTIC — System design interview prep notes

- **Benchmark ID:** 44
- **Difficulty:** medium
- **Relevant Notes:** [70, 145, 255, 267, 305, 309, 334, 344, 346, 360]
- **Retrieved Notes:** [360, 70, 106, 309, 99]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.600 |
| Recall@5 | 0.300 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 0.98 |

---

### SEMANTIC — What system design topics have I covered?

- **Benchmark ID:** 45
- **Difficulty:** easy
- **Relevant Notes:** [70, 145, 255, 267, 305, 309, 334, 344, 346, 360]
- **Retrieved Notes:** [360, 392, 309, 70, 99]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.600 |
| Recall@5 | 0.300 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 0.86 |

---

### SEMANTIC — Behavioral interview preparation notes

- **Benchmark ID:** 46
- **Difficulty:** medium
- **Relevant Notes:** [169, 197, 263, 294, 309, 344, 468, 478, 504, 605]
- **Retrieved Notes:** [294, 468, 360, 288, 352]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.200 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 1.37 |

---

### SEMANTIC — Mock interview notes and feedback

- **Benchmark ID:** 47
- **Difficulty:** medium
- **Relevant Notes:** [126, 152, 154, 199, 280, 352, 507, 521, 609, 611]
- **Retrieved Notes:** [126, 360, 540, 352, 507]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.600 |
| Recall@5 | 0.300 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 0.78 |

---

### SEMANTIC — Resume writing and improvement tips

- **Benchmark ID:** 48
- **Difficulty:** easy
- **Relevant Notes:** [100, 142, 185, 270, 523, 525]
- **Retrieved Notes:** [100, 142, 185, 525, 472]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.800 |
| Recall@5 | 0.667 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 0.72 |

---

### SEMANTIC — Campus placement preparation notes

- **Benchmark ID:** 49
- **Difficulty:** easy
- **Relevant Notes:** [54, 77, 100, 111, 176, 225, 236, 318, 343, 344]
- **Retrieved Notes:** [415, 620, 100, 236, 343]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.600 |
| Recall@5 | 0.300 |
| Hit | True |
| Reciprocal Rank | 0.333 |
| Latency (ms) | 0.69 |

---

### SEMANTIC — Database sharding and partitioning notes

- **Benchmark ID:** 50
- **Difficulty:** hard
- **Relevant Notes:** [259, 292, 417, 580, 608, 695, 731, 795, 831, 895]
- **Retrieved Notes:** [895, 292, 795, 695, 995]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.800 |
| Recall@5 | 0.400 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 0.75 |

---

### SEMANTIC — Caching strategies and implementations

- **Benchmark ID:** 51
- **Difficulty:** medium
- **Relevant Notes:** [103, 124, 146, 237, 269, 275, 284, 295, 318, 336]
- **Retrieved Notes:** [61, 93, 644, 602, 467]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 1.07 |

---

### SEMANTIC — Message queue and event streaming notes

- **Benchmark ID:** 52
- **Difficulty:** medium
- **Relevant Notes:** [71, 102, 144, 174, 200, 218, 238, 269, 297, 304]
- **Retrieved Notes:** [871, 671, 771, 450, 971]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 0.97 |

---

### SEMANTIC — Microservices architecture notes

- **Benchmark ID:** 53
- **Difficulty:** hard
- **Relevant Notes:** [189, 263, 299, 372, 410, 652, 665, 697, 752, 765]
- **Retrieved Notes:** [372, 392, 106, 102, 410]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.200 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 1.87 |

---

### SEMANTIC — Distributed systems consensus notes

- **Benchmark ID:** 54
- **Difficulty:** hard
- **Relevant Notes:** [99, 140, 264, 299, 308, 346, 354, 390, 439, 450]
- **Retrieved Notes:** [354, 608, 99, 580, 439]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.600 |
| Recall@5 | 0.300 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 0.93 |

---

### SEMANTIC — Observability and monitoring notes

- **Benchmark ID:** 55
- **Difficulty:** medium
- **Relevant Notes:** [299, 477, 570, 665, 765, 865, 965, 1065]
- **Retrieved Notes:** [477, 410, 424, 140, 372]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.125 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 0.93 |

---

### SEMANTIC — Idempotency and distributed system reliability notes

- **Benchmark ID:** 56
- **Difficulty:** hard
- **Relevant Notes:** [140, 299, 392, 431, 665, 765, 865, 965, 1065]
- **Retrieved Notes:** [140, 431, 608, 99, 580]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.222 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 1.33 |

---

### SEMANTIC — KnowledgeVault project notes

- **Benchmark ID:** 57
- **Difficulty:** easy
- **Relevant Notes:** [57, 88, 89, 90, 91, 94, 95, 96, 97, 107]
- **Retrieved Notes:** [125, 95, 96, 89, 90]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.800 |
| Recall@5 | 0.400 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| Latency (ms) | 0.90 |

---

### SEMANTIC — What decisions have I made for the KnowledgeVault project?

- **Benchmark ID:** 58
- **Difficulty:** medium
- **Relevant Notes:** [57, 88, 89, 90, 91, 94, 95, 96, 97, 107]
- **Retrieved Notes:** [638, 90, 728, 428, 828]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.100 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| Latency (ms) | 0.86 |

---

### SEMANTIC — Notes about hybrid retrieval implementation

- **Benchmark ID:** 59
- **Difficulty:** hard
- **Relevant Notes:** [183, 213, 252, 375, 381, 486, 518, 555, 696, 702]
- **Retrieved Notes:** [902, 802, 486, 702, 1002]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.200 |
| Hit | True |
| Reciprocal Rank | 0.333 |
| Latency (ms) | 0.84 |

---

### SEMANTIC — Docker and containerization notes

- **Benchmark ID:** 60
- **Difficulty:** easy
- **Relevant Notes:** [72, 75, 91, 105, 118, 138, 188, 192, 242, 295]
- **Retrieved Notes:** [72, 105, 192, 75, 491]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.800 |
| Recall@5 | 0.400 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 0.91 |

---

### SEMANTIC — What Docker tips have I collected?

- **Benchmark ID:** 61
- **Difficulty:** easy
- **Relevant Notes:** [72, 75, 91, 105, 118, 138, 188, 192, 242, 295]
- **Retrieved Notes:** [72, 192, 295, 105, 75]

| Metric | Value |
|-------|------:|
| Precision@5 | 1.000 |
| Recall@5 | 0.500 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 0.94 |

---

### SEMANTIC — FastAPI development notes

- **Benchmark ID:** 62
- **Difficulty:** medium
- **Relevant Notes:** [68, 132, 145, 165, 167, 266, 272, 313, 350, 365]
- **Retrieved Notes:** [68, 825, 165, 725, 925]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.200 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 0.97 |

---

### SEMANTIC — PostgreSQL database notes

- **Benchmark ID:** 63
- **Difficulty:** medium
- **Relevant Notes:** [58, 66, 74, 104, 139, 144, 168, 175, 215, 267]
- **Retrieved Notes:** [74, 144, 731, 417, 831]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.200 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 0.84 |

---

### SEMANTIC — What PostgreSQL features and tips do I have?

- **Benchmark ID:** 64
- **Difficulty:** easy
- **Relevant Notes:** [58, 66, 74, 104, 139, 144, 168, 175, 215, 267]
- **Retrieved Notes:** [58, 74, 144, 367, 628]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.600 |
| Recall@5 | 0.300 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 0.76 |

---

### SEMANTIC — Redis usage and patterns

- **Benchmark ID:** 65
- **Difficulty:** easy
- **Relevant Notes:** [61, 73, 92, 103, 124, 146, 157, 174, 237, 246]
- **Retrieved Notes:** [73, 92, 724, 269, 824]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.200 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 0.74 |

---

### SEMANTIC — pgvector and vector search notes

- **Benchmark ID:** 66
- **Difficulty:** hard
- **Relevant Notes:** [66, 168, 183, 215, 217, 228, 252, 298, 323, 333]
- **Retrieved Notes:** [66, 842, 742, 323, 942]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.200 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 0.75 |

---

### SEMANTIC — What meetings have I had?

- **Benchmark ID:** 67
- **Difficulty:** easy
- **Relevant Notes:** [56, 106, 107, 149, 170, 233, 251, 283, 304, 359]
- **Retrieved Notes:** [371, 107, 263, 559, 442]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.100 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| Latency (ms) | 0.71 |

---

### SEMANTIC — Team meeting notes

- **Benchmark ID:** 68
- **Difficulty:** easy
- **Relevant Notes:** [56, 106, 107, 149, 170, 233, 251, 283, 304, 359]
- **Retrieved Notes:** [203, 87, 107, 125, 106]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.200 |
| Hit | True |
| Reciprocal Rank | 0.333 |
| Latency (ms) | 0.77 |

---

### SEMANTIC — Mentor and senior advice I've received

- **Benchmark ID:** 69
- **Difficulty:** easy
- **Relevant Notes:** [68, 126, 185, 199, 236, 260, 272, 274, 330, 372]
- **Retrieved Notes:** [199, 185, 428, 728, 828]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.200 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 0.71 |

---

### SEMANTIC — Hackathon planning notes

- **Benchmark ID:** 70
- **Difficulty:** easy
- **Relevant Notes:** [55, 324, 448, 463, 535, 542]
- **Retrieved Notes:** [448, 324, 463, 55, 542]

| Metric | Value |
|-------|------:|
| Precision@5 | 1.000 |
| Recall@5 | 0.833 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 0.98 |

---

### SEMANTIC — What are my pending tasks and deadlines?

- **Benchmark ID:** 71
- **Difficulty:** easy
- **Relevant Notes:** [155, 179, 184, 207, 233, 266]
- **Retrieved Notes:** [498, 453, 233, 647, 59]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.167 |
| Hit | True |
| Reciprocal Rank | 0.333 |
| Latency (ms) | 1.01 |

---

### SEMANTIC — What health appointments do I have?

- **Benchmark ID:** 72
- **Difficulty:** easy
- **Relevant Notes:** [78, 79, 109, 157, 179, 201, 210, 212, 224, 226]
- **Retrieved Notes:** [79, 601, 559, 575, 198]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.100 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 0.80 |

---

### SEMANTIC — What payments and bills do I need to make?

- **Benchmark ID:** 73
- **Difficulty:** easy
- **Relevant Notes:** [77, 120, 126, 128, 131, 137, 140, 144, 160, 162]
- **Retrieved Notes:** [341, 77, 82, 635, 368]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.100 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| Latency (ms) | 0.92 |

---

### SEMANTIC — What is on my shopping list?

- **Benchmark ID:** 74
- **Difficulty:** easy
- **Relevant Notes:** [76, 322]
- **Retrieved Notes:** [393, 322, 606, 115, 76]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 1.000 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| Latency (ms) | 0.72 |

---

### SEMANTIC — Show all my reminders

- **Benchmark ID:** 75
- **Difficulty:** easy
- **Relevant Notes:** [55, 152, 212, 312, 542, 557]
- **Retrieved Notes:** [382, 56, 312, 290, 442]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.167 |
| Hit | True |
| Reciprocal Rank | 0.333 |
| Latency (ms) | 0.72 |

---

### SEMANTIC — What do I need to remember this week?

- **Benchmark ID:** 76
- **Difficulty:** medium
- **Relevant Notes:** [55, 152, 212, 312, 542, 557]
- **Retrieved Notes:** [77, 212, 475, 442, 755]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.167 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| Latency (ms) | 0.66 |

---

### SEMANTIC — My budget and expense tracking notes

- **Benchmark ID:** 77
- **Difficulty:** easy
- **Relevant Notes:** [82, 153, 202, 210, 216, 254, 281, 291, 331, 345]
- **Retrieved Notes:** [82, 216, 606, 393, 285]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.200 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 0.63 |

---

### SEMANTIC — Monthly expense breakdown

- **Benchmark ID:** 78
- **Difficulty:** medium
- **Relevant Notes:** [82, 153, 202, 210, 216, 254, 281, 291, 331, 345]
- **Retrieved Notes:** [82, 216, 490, 606, 341]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.200 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 0.93 |

---

### SEMANTIC — Investment and savings notes

- **Benchmark ID:** 79
- **Difficulty:** medium
- **Relevant Notes:** [113, 273, 496, 561, 591, 594, 750, 850, 950, 1050]
- **Retrieved Notes:** [162, 285, 113, 594, 539]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.200 |
| Hit | True |
| Reciprocal Rank | 0.333 |
| Latency (ms) | 1.37 |

---

### SEMANTIC — Tech purchase notes and wishlists

- **Benchmark ID:** 80
- **Difficulty:** easy
- **Relevant Notes:** [115, 124, 174, 200, 211, 307, 420, 434, 442, 445]
- **Retrieved Notes:** [444, 605, 87, 262, 285]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 1.00 |

---

### SEMANTIC — My travel plans and notes

- **Benchmark ID:** 81
- **Difficulty:** easy
- **Relevant Notes:** [78, 81, 115, 126, 128, 130, 160, 171, 175, 176]
- **Retrieved Notes:** [290, 81, 212, 393, 444]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.100 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| Latency (ms) | 0.71 |

---

### SEMANTIC — Upcoming trips and travel bookings

- **Benchmark ID:** 82
- **Difficulty:** easy
- **Relevant Notes:** [78, 81, 115, 126, 128, 130, 160, 171, 175, 176]
- **Retrieved Notes:** [538, 627, 81, 128, 190]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.200 |
| Hit | True |
| Reciprocal Rank | 0.333 |
| Latency (ms) | 0.80 |

---

### SEMANTIC — Delhi trip plans

- **Benchmark ID:** 83
- **Difficulty:** easy
- **Relevant Notes:** [55, 115, 256, 324, 448, 463, 524, 535, 542, 577]
- **Retrieved Notes:** [115, 324, 535, 407, 463]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.800 |
| Recall@5 | 0.400 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 1.06 |

---

### SEMANTIC — Hill station and trekking plans

- **Benchmark ID:** 84
- **Difficulty:** medium
- **Relevant Notes:** [81, 128, 351, 407]
- **Retrieved Notes:** [351, 137, 60, 498, 324]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.250 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 0.91 |

---

### SEMANTIC — Train booking tips and notes

- **Benchmark ID:** 85
- **Difficulty:** easy
- **Relevant Notes:** [160, 463, 596]
- **Retrieved Notes:** [596, 160, 393, 203, 290]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.667 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 1.64 |

---

### SEMANTIC — Fitness and workout notes

- **Benchmark ID:** 86
- **Difficulty:** easy
- **Relevant Notes:** [173, 185, 202, 232, 246, 291, 317, 380, 392, 427]
- **Retrieved Notes:** [631, 481, 87, 482, 83]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 1.59 |

---

### SEMANTIC — My exercise routine notes

- **Benchmark ID:** 87
- **Difficulty:** easy
- **Relevant Notes:** [173, 185, 202, 232, 246, 291, 317, 380, 392, 427]
- **Retrieved Notes:** [631, 83, 87, 380, 680]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.100 |
| Hit | True |
| Reciprocal Rank | 0.250 |
| Latency (ms) | 1.00 |

---

### SEMANTIC — Sleep improvement notes

- **Benchmark ID:** 88
- **Difficulty:** medium
- **Relevant Notes:** [133, 136, 202, 288, 348, 380, 434, 538, 548, 574]
- **Retrieved Notes:** [548, 622, 434, 574, 348]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.800 |
| Recall@5 | 0.400 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 0.80 |

---

### SEMANTIC — Nutrition and supplement notes

- **Benchmark ID:** 89
- **Difficulty:** medium
- **Relevant Notes:** [109, 133, 226, 286]
- **Retrieved Notes:** [286, 133, 322, 87, 285]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.500 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 1.65 |

---

### SEMANTIC — Mental health and wellbeing notes

- **Benchmark ID:** 90
- **Difficulty:** medium
- **Relevant Notes:** [152, 288, 291, 317, 472, 575]
- **Retrieved Notes:** [575, 201, 291, 212, 472]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.600 |
| Recall@5 | 0.500 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 0.87 |

---

### SEMANTIC — My startup ideas and business notes

- **Benchmark ID:** 91
- **Difficulty:** easy
- **Relevant Notes:** [85, 86, 117, 120, 125, 128, 131, 134, 143, 157]
- **Retrieved Notes:** [85, 525, 459, 617, 441]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.100 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 0.90 |

---

### SEMANTIC — What business ideas have I documented?

- **Benchmark ID:** 92
- **Difficulty:** easy
- **Relevant Notes:** [85, 86, 117, 120, 125, 128, 131, 134, 143, 157]
- **Retrieved Notes:** [225, 178, 85, 441, 459]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.100 |
| Hit | True |
| Reciprocal Rank | 0.333 |
| Latency (ms) | 0.70 |

---

### SEMANTIC — Y Combinator and startup ecosystem notes

- **Benchmark ID:** 93
- **Difficulty:** medium
- **Relevant Notes:** [72, 133, 137, 205, 248, 307, 342, 347, 438, 536]
- **Retrieved Notes:** [462, 267, 85, 482, 118]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 0.87 |

---

### SEMANTIC — Business model and monetization notes

- **Benchmark ID:** 94
- **Difficulty:** medium
- **Relevant Notes:** [210, 216, 330, 331, 514, 594, 617, 624, 649]
- **Retrieved Notes:** [178, 262, 285, 308, 393]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 0.76 |

---

### SEMANTIC — Startup idea validation notes

- **Benchmark ID:** 95
- **Difficulty:** medium
- **Relevant Notes:** [108, 117, 126, 132, 134, 146, 173, 199, 204, 210]
- **Retrieved Notes:** [459, 525, 134, 617, 441]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.100 |
| Hit | True |
| Reciprocal Rank | 0.333 |
| Latency (ms) | 0.70 |

---

### SEMANTIC — What books have I taken notes on?

- **Benchmark ID:** 96
- **Difficulty:** easy
- **Relevant Notes:** [78, 128, 141, 155, 160, 172, 182, 194, 208, 234]
- **Retrieved Notes:** [309, 290, 240, 444, 87]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 1.00 |

---

### SEMANTIC — My book notes and summaries

- **Benchmark ID:** 97
- **Difficulty:** easy
- **Relevant Notes:** [78, 128, 141, 155, 160, 172, 182, 194, 208, 234]
- **Retrieved Notes:** [87, 699, 583, 799, 899]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 0.81 |

---

### SEMANTIC — Notes from Designing Data-Intensive Applications

- **Benchmark ID:** 98
- **Difficulty:** hard
- **Relevant Notes:** [439, 528]
- **Retrieved Notes:** [528, 439, 267, 106, 402]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 1.000 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 1.21 |

---

### SEMANTIC — Atomic Habits notes and takeaways

- **Benchmark ID:** 99
- **Difficulty:** easy
- **Relevant Notes:** [164, 304, 317, 349, 482, 557, 631, 634, 698, 734]
- **Retrieved Notes:** [482, 229, 690, 790, 890]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.100 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 0.99 |

---

### SEMANTIC — Podcast notes and key insights

- **Benchmark ID:** 100
- **Difficulty:** easy
- **Relevant Notes:** [230, 419, 548]
- **Retrieved Notes:** [230, 87, 419, 442, 755]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.667 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 0.66 |

---

### SEMANTIC — Online courses I'm taking or completed

- **Benchmark ID:** 101
- **Difficulty:** easy
- **Relevant Notes:** [71, 145, 231, 266, 357, 394, 417, 471, 519, 611]
- **Retrieved Notes:** [343, 145, 663, 471, 763]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.200 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| Latency (ms) | 1.50 |

---

### SEMANTIC — Kubernetes learning notes

- **Benchmark ID:** 102
- **Difficulty:** medium
- **Relevant Notes:** [62, 101, 118, 180, 181, 225, 230, 263, 299, 355]
- **Retrieved Notes:** [62, 118, 812, 712, 912]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.200 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 0.98 |

---

### SEMANTIC — Terraform and infrastructure as code notes

- **Benchmark ID:** 103
- **Difficulty:** medium
- **Relevant Notes:** [274]
- **Retrieved Notes:** [274, 62, 181, 106, 316]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 1.000 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 0.81 |

---

### SEMANTIC — Authentication and authorization notes

- **Benchmark ID:** 104
- **Difficulty:** medium
- **Relevant Notes:** [63, 129, 165, 189, 227, 244, 276, 287, 338, 346]
- **Retrieved Notes:** [408, 63, 733, 637, 833]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.100 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| Latency (ms) | 0.92 |

---

### SEMANTIC — Testing and pytest notes

- **Benchmark ID:** 105
- **Difficulty:** medium
- **Relevant Notes:** [108, 124, 126, 152, 153, 163, 165, 172, 245, 277]
- **Retrieved Notes:** [435, 245, 313, 177, 258]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.100 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| Latency (ms) | 0.98 |

---

### SEMANTIC — Debugging sessions and fixes

- **Benchmark ID:** 106
- **Difficulty:** medium
- **Relevant Notes:** [94, 136, 161, 246, 258, 335, 340, 362, 421, 461]
- **Retrieved Notes:** [632, 591, 163, 522, 246]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.100 |
| Hit | True |
| Reciprocal Rank | 0.200 |
| Latency (ms) | 0.74 |

---

### SEMANTIC — What bugs have I debugged recently?

- **Benchmark ID:** 107
- **Difficulty:** easy
- **Relevant Notes:** [94, 136, 161, 246, 258, 335]
- **Retrieved Notes:** [591, 632, 522, 246, 684]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.167 |
| Hit | True |
| Reciprocal Rank | 0.250 |
| Latency (ms) | 0.90 |

---

### SEMANTIC — SQLAlchemy N+1 query problem notes

- **Benchmark ID:** 108
- **Difficulty:** hard
- **Relevant Notes:** [363, 588, 589, 659, 759, 859, 959, 1059]
- **Retrieved Notes:** [759, 859, 589, 659, 959]

| Metric | Value |
|-------|------:|
| Precision@5 | 1.000 |
| Recall@5 | 0.625 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 0.79 |

---

### SEMANTIC — Race condition and concurrency bug notes

- **Benchmark ID:** 109
- **Difficulty:** hard
- **Relevant Notes:** [229, 246, 296, 321, 384, 421, 462, 474, 482, 499]
- **Retrieved Notes:** [462, 827, 727, 384, 927]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.200 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 0.79 |

---

### SEMANTIC — Memory management and leak debugging notes

- **Benchmark ID:** 110
- **Difficulty:** hard
- **Relevant Notes:** [124, 146, 169, 175, 182, 219, 248, 273, 275, 279]
- **Retrieved Notes:** [547, 591, 318, 169, 275]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.200 |
| Hit | True |
| Reciprocal Rank | 0.250 |
| Latency (ms) | 0.73 |

---

### SEMANTIC — My journal entries and personal reflections

- **Benchmark ID:** 111
- **Difficulty:** easy
- **Relevant Notes:** [113, 149, 152, 162, 166, 191, 251, 255]
- **Retrieved Notes:** [472, 290, 550, 700, 800]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 1.12 |

---

### SEMANTIC — Productivity tips and personal notes

- **Benchmark ID:** 112
- **Difficulty:** easy
- **Relevant Notes:** [85, 199, 224, 240, 248, 286, 429, 453, 529, 550]
- **Retrieved Notes:** [87, 699, 799, 583, 899]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 1.16 |

---

### SEMANTIC — Career direction and goal notes

- **Benchmark ID:** 113
- **Difficulty:** medium
- **Relevant Notes:** [56, 61, 91, 96, 101, 106, 166, 175, 177, 180]
- **Retrieved Notes:** [885, 785, 166, 685, 985]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.100 |
| Hit | True |
| Reciprocal Rank | 0.333 |
| Latency (ms) | 0.77 |

---

### SEMANTIC — Open source and building in public notes

- **Benchmark ID:** 114
- **Difficulty:** medium
- **Relevant Notes:** [117, 141, 255, 395, 400, 440, 453, 522, 554, 555]
- **Retrieved Notes:** [255, 285, 106, 87, 141]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.200 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 1.07 |

---

### SEMANTIC — KnowledgeVault RAG pipeline decisions and findings

- **Benchmark ID:** 115
- **Difficulty:** hard
- **Relevant Notes:** [1028, 262, 1030, 1032, 523, 267, 533, 1053]
- **Retrieved Notes:** [310, 90, 446, 730, 830]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 0.82 |

---

### SEMANTIC — All my interview preparation notes — coding and system design

- **Benchmark ID:** 116
- **Difficulty:** hard
- **Relevant Notes:** [769, 129, 387, 642, 516, 255, 392, 267, 271, 399]
- **Retrieved Notes:** [360, 70, 309, 99, 126]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 1.21 |

---

### SEMANTIC — AI system infrastructure notes: vector DB, cache, and retrieval

- **Benchmark ID:** 117
- **Difficulty:** hard
- **Relevant Notes:** [1024, 1030, 1031, 1032, 520, 523, 1036, 1042]
- **Retrieved Notes:** [333, 66, 61, 644, 523]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.125 |
| Hit | True |
| Reciprocal Rank | 0.200 |
| Latency (ms) | 1.39 |

---

### SEMANTIC — All my health and wellness notes

- **Benchmark ID:** 118
- **Difficulty:** medium
- **Relevant Notes:** [643, 764, 773, 646, 133, 392, 905, 522]
- **Retrieved Notes:** [212, 322, 79, 444, 442]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 1.64 |

---

### SEMANTIC — Financial tasks and expense notes

- **Benchmark ID:** 119
- **Difficulty:** medium
- **Relevant Notes:** [1028, 1035, 1043, 1044, 1046, 535, 538, 540]
- **Retrieved Notes:** [82, 87, 393, 216, 285]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 1.61 |

---

### SEMANTIC — My university computer science notes

- **Benchmark ID:** 120
- **Difficulty:** hard
- **Relevant Notes:** [513, 1026, 1027, 515, 516, 510, 1031, 1034, 1038, 526]
- **Retrieved Notes:** [87, 106, 583, 699, 799]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 1.89 |

---

### SEMANTIC — Things I need to do this week

- **Benchmark ID:** 121
- **Difficulty:** medium
- **Relevant Notes:** [155, 179, 184, 207, 233, 266]
- **Retrieved Notes:** [77, 81, 76, 322, 79]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 1.43 |

---

### SEMANTIC — What tasks are pending for me?

- **Benchmark ID:** 122
- **Difficulty:** medium
- **Relevant Notes:** [155, 179, 184, 207, 233, 266]
- **Retrieved Notes:** [453, 647, 77, 498, 174]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 1.02 |

---

### SEMANTIC — Resources for learning backend development

- **Benchmark ID:** 123
- **Difficulty:** medium
- **Relevant Notes:** [1025, 772, 775, 1031, 1032, 266, 523, 267]
- **Retrieved Notes:** [106, 61, 330, 96, 101]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 0.89 |

---

### SEMANTIC — How do I get better at backend engineering?

- **Benchmark ID:** 124
- **Difficulty:** medium
- **Relevant Notes:** [1025, 772, 775, 1031, 1032, 266]
- **Retrieved Notes:** [272, 106, 166, 685, 785]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 0.83 |

---

### SEMANTIC — What are distributed systems trade-offs?

- **Benchmark ID:** 125
- **Difficulty:** hard
- **Relevant Notes:** [897, 771, 259, 390, 1031, 264]
- **Retrieved Notes:** [308, 99, 608, 516, 711]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 1.01 |

---

### SEMANTIC — Notes on scalability and reliability

- **Benchmark ID:** 126
- **Difficulty:** hard
- **Relevant Notes:** [1024, 259, 644, 1031, 520, 906]
- **Retrieved Notes:** [608, 354, 439, 530, 738]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 1.05 |

---

### SEMANTIC — What are my creative ideas?

- **Benchmark ID:** 127
- **Difficulty:** easy
- **Relevant Notes:** [85, 86, 117, 120, 125, 128]
- **Retrieved Notes:** [382, 85, 416, 240, 496]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.167 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| Latency (ms) | 0.92 |

---

### SEMANTIC — Show my brainstorming notes

- **Benchmark ID:** 128
- **Difficulty:** easy
- **Relevant Notes:** [128, 514, 131, 260, 134, 262, 1035, 525]
- **Retrieved Notes:** [87, 85, 290, 416, 583]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 0.75 |

---

### SEMANTIC — Advice and wisdom I've collected

- **Benchmark ID:** 129
- **Difficulty:** medium
- **Relevant Notes:** [260, 1028, 522, 1035, 525, 272]
- **Retrieved Notes:** [928, 828, 428, 728, 1028]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.167 |
| Hit | True |
| Reciprocal Rank | 0.200 |
| Latency (ms) | 0.81 |

---

### SEMANTIC — BM25

- **Benchmark ID:** 130
- **Difficulty:** easy
- **Relevant Notes:** [228, 252, 696, 796, 896, 996, 1096]
- **Retrieved Notes:** [796, 896, 696, 252, 996]

| Metric | Value |
|-------|------:|
| Precision@5 | 1.000 |
| Recall@5 | 0.714 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 1.31 |

---

### SEMANTIC — HNSW index

- **Benchmark ID:** 131
- **Difficulty:** easy
- **Relevant Notes:** [215, 430, 681, 781, 881, 981, 1081]
- **Retrieved Notes:** [430, 781, 215, 681, 881]

| Metric | Value |
|-------|------:|
| Precision@5 | 1.000 |
| Recall@5 | 0.714 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 1.31 |

---

### SEMANTIC — HNSW vector index configuration

- **Benchmark ID:** 132
- **Difficulty:** medium
- **Relevant Notes:** [215, 430, 681, 781, 881, 981, 1081]
- **Retrieved Notes:** [430, 66, 323, 742, 842]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.143 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 0.82 |

---

### SEMANTIC — Reciprocal Rank Fusion

- **Benchmark ID:** 133
- **Difficulty:** medium
- **Relevant Notes:** [518, 718, 818, 918, 1018]
- **Retrieved Notes:** [918, 518, 818, 718, 1018]

| Metric | Value |
|-------|------:|
| Precision@5 | 1.000 |
| Recall@5 | 1.000 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 0.88 |

---

### SEMANTIC — two sum problem

- **Benchmark ID:** 134
- **Difficulty:** easy
- **Relevant Notes:** [278, 677, 777, 877, 977, 1077]
- **Retrieved Notes:** [777, 877, 677, 278, 977]

| Metric | Value |
|-------|------:|
| Precision@5 | 1.000 |
| Recall@5 | 0.833 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 1.29 |

---

### SEMANTIC — LRU cache implementation

- **Benchmark ID:** 135
- **Difficulty:** medium
- **Relevant Notes:** [318, 336, 520, 530, 579, 736, 738, 836, 838, 936]
- **Retrieved Notes:** [520, 318, 579, 736, 836]

| Metric | Value |
|-------|------:|
| Precision@5 | 1.000 |
| Recall@5 | 0.500 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 2.32 |

---

### SEMANTIC — CAP theorem

- **Benchmark ID:** 136
- **Difficulty:** easy
- **Relevant Notes:** [580, 608]
- **Retrieved Notes:** [580, 608, 233, 607, 753]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 1.000 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 1.26 |

---

### SEMANTIC — PageRank or graph algorithms notes

- **Benchmark ID:** 137
- **Difficulty:** medium
- **Relevant Notes:** [60, 158, 224, 316, 342, 347, 545, 546, 619, 667]
- **Retrieved Notes:** [619, 333, 60, 215, 681]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.200 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 1.12 |

---

### SEMANTIC — What have I been working on this month?

- **Benchmark ID:** 138
- **Difficulty:** hard
- **Relevant Notes:** [77, 149, 164, 182, 216, 286]
- **Retrieved Notes:** [453, 77, 82, 647, 375]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.167 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| Latency (ms) | 0.79 |

---

### SEMANTIC — Recent notes and activities

- **Benchmark ID:** 139
- **Difficulty:** hard
- **Relevant Notes:** [77, 149, 164, 182, 216, 286]
- **Retrieved Notes:** [87, 444, 565, 290, 203]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 0.96 |

---

### SEMANTIC — Redis vs Kafka — when to use each

- **Benchmark ID:** 140
- **Difficulty:** hard
- **Relevant Notes:** [1024, 771, 1027, 773, 520, 1034]
- **Retrieved Notes:** [873, 673, 643, 773, 973]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.167 |
| Hit | True |
| Reciprocal Rank | 0.250 |
| Latency (ms) | 1.25 |

---

### SEMANTIC — Python vs Go programming notes

- **Benchmark ID:** 141
- **Difficulty:** hard
- **Relevant Notes:** [512, 320, 898, 266, 138, 586]
- **Retrieved Notes:** [572, 327, 662, 283, 762]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 1.38 |

---

### SEMANTIC — SQL vs NoSQL database comparison

- **Benchmark ID:** 142
- **Difficulty:** hard
- **Relevant Notes:** [772, 775, 904, 1031, 1032, 139]
- **Retrieved Notes:** [954, 854, 300, 754, 1054]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 1.13 |

---

### SEMANTIC — Comparing RAG retrieval strategies: dense, sparse, and reranking

- **Benchmark ID:** 143
- **Difficulty:** hard
- **Relevant Notes:** [386, 1030, 648, 649, 776, 267]
- **Retrieved Notes:** [386, 310, 595, 492, 186]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.167 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 1.25 |

---

### SEMANTIC — REST vs GraphQL API design trade-offs

- **Benchmark ID:** 144
- **Difficulty:** hard
- **Relevant Notes:** [68, 93, 96, 132, 136, 142]
- **Retrieved Notes:** [484, 644, 93, 450, 671]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.167 |
| Hit | True |
| Reciprocal Rank | 0.333 |
| Latency (ms) | 1.15 |

---

### SEMANTIC — Show all my communication notes

- **Benchmark ID:** 145
- **Difficulty:** easy
- **Relevant Notes:** [54, 55, 56, 57, 106, 117]
- **Retrieved Notes:** [141, 699, 799, 583, 899]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 1.26 |

---

### SEMANTIC — All my reminder notes

- **Benchmark ID:** 146
- **Difficulty:** easy
- **Relevant Notes:** [55, 152, 212, 312, 542, 557]
- **Retrieved Notes:** [290, 799, 583, 699, 899]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 1.59 |

---

### SEMANTIC — My study notes on AI and machine learning

- **Benchmark ID:** 147
- **Difficulty:** easy
- **Relevant Notes:** [1026, 774, 1030, 510, 523, 268, 267, 782]
- **Retrieved Notes:** [529, 230, 87, 619, 85]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 2.57 |

---

### SEMANTIC — Notes categorized under system design

- **Benchmark ID:** 148
- **Difficulty:** easy
- **Relevant Notes:** [70, 145, 255, 267, 305, 309]
- **Retrieved Notes:** [106, 392, 87, 602, 309]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.167 |
| Hit | True |
| Reciprocal Rank | 0.200 |
| Latency (ms) | 2.45 |

---

### SEMANTIC — Programming notes I've taken recently

- **Benchmark ID:** 149
- **Difficulty:** medium
- **Relevant Notes:** [512, 1025, 898, 132, 266, 523]
- **Retrieved Notes:** [87, 799, 699, 583, 899]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 3.86 |

---

### SEMANTIC — My financial notes

- **Benchmark ID:** 150
- **Difficulty:** medium
- **Relevant Notes:** [646, 202, 331, 591, 273, 82]
- **Retrieved Notes:** [290, 87, 637, 733, 833]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 2.56 |

---

### SEMANTIC — Projects and ideas I'm excited about

- **Benchmark ID:** 151
- **Difficulty:** hard
- **Relevant Notes:** [514, 260, 1028, 262, 1032, 522]
- **Retrieved Notes:** [85, 528, 442, 755, 855]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 1.09 |

---

### SEMANTIC — Personal notes and self-improvement

- **Benchmark ID:** 152
- **Difficulty:** hard
- **Relevant Notes:** [522, 1035, 785, 529, 277, 283]
- **Retrieved Notes:** [444, 290, 212, 87, 583]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 0.98 |

---

### INTENT — What are useful Python tips and tricks I've learned?

- **Benchmark ID:** 1
- **Difficulty:** easy
- **Relevant Notes:** [108, 174, 177, 206, 232, 239, 272, 283]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 151.67 |
| Predicted Intent | question |
| Expected Intent | study |
| Intent Correct | False |

---

### INTENT — Show my Python programming notes

- **Benchmark ID:** 2
- **Difficulty:** easy
- **Relevant Notes:** [108, 174, 177, 206, 232, 239, 272, 283]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 29.69 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |

---

### INTENT — Notes about Python dictionaries and hash maps

- **Benchmark ID:** 3
- **Difficulty:** easy
- **Relevant Notes:** [108, 271, 278, 284, 397, 464, 483, 560, 579, 587]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 28.52 |
| Predicted Intent | general |
| Expected Intent | reference |
| Intent Correct | False |

---

### INTENT — How does Python async programming work?

- **Benchmark ID:** 4
- **Difficulty:** medium
- **Relevant Notes:** [170, 283, 304, 359, 364, 372, 471, 661, 662, 663]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 26.72 |
| Predicted Intent | question |
| Expected Intent | study |
| Intent Correct | False |

---

### INTENT — Concurrency and asynchronous patterns in Python

- **Benchmark ID:** 5
- **Difficulty:** medium
- **Relevant Notes:** [170, 283, 304, 359, 364, 372, 471, 661, 662, 663]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 28.54 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |

---

### INTENT — Python decorator notes

- **Benchmark ID:** 6
- **Difficulty:** easy
- **Relevant Notes:** [174, 414, 435, 455, 549, 610, 614]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 26.55 |
| Predicted Intent | general |
| Expected Intent | reference |
| Intent Correct | False |

---

### INTENT — What git commands and workflows have I noted?

- **Benchmark ID:** 7
- **Difficulty:** easy
- **Relevant Notes:** [130, 135, 144, 169, 229, 272, 317, 328, 366, 395]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 24.64 |
| Predicted Intent | question |
| Expected Intent | reference |
| Intent Correct | False |

---

### INTENT — Git tips and tricks

- **Benchmark ID:** 8
- **Difficulty:** easy
- **Relevant Notes:** [130, 135, 144, 169, 229, 272, 317, 328, 366, 395]
- **Retrieved Notes:** [646, 614, 582, 558, 533]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 35.73 |
| Predicted Intent | general |
| Expected Intent | reference |
| Intent Correct | False |
| Predicted Category | Ideas - Semantic Retrieval |
| Expected Category | Reference - Git |
| Category Correct | False |

---

### INTENT — JavaScript and TypeScript notes

- **Benchmark ID:** 9
- **Difficulty:** easy
- **Relevant Notes:** [218, 220, 250, 297, 418, 713, 720, 813, 820, 913]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 24.46 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |

---

### INTENT — What have I learned about Go programming?

- **Benchmark ID:** 10
- **Difficulty:** medium
- **Relevant Notes:** [114, 138, 206, 208, 266, 297, 320, 339, 488, 512]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 24.82 |
| Predicted Intent | question |
| Expected Intent | study |
| Intent Correct | False |

---

### INTENT — Rust ownership and borrowing notes

- **Benchmark ID:** 11
- **Difficulty:** medium
- **Relevant Notes:** [151, 182, 210, 351, 370, 380, 459, 494, 539, 563]
- **Retrieved Notes:** [1089, 1069, 989, 969, 889]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 25.75 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |
| Predicted Category | Study - System Design |
| Expected Category | Study - Rust |
| Category Correct | True |

---

### INTENT — What design patterns have I documented?

- **Benchmark ID:** 12
- **Difficulty:** medium
- **Relevant Notes:** [102, 121, 189, 203, 224, 238, 246, 254, 266, 269]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 25.37 |
| Predicted Intent | question |
| Expected Intent | reference |
| Intent Correct | False |

---

### INTENT — Software design patterns notes

- **Benchmark ID:** 13
- **Difficulty:** easy
- **Relevant Notes:** [102, 121, 189, 203, 224, 238, 246, 254, 266, 269]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 25.35 |
| Predicted Intent | general |
| Expected Intent | reference |
| Intent Correct | False |

---

### INTENT — Performance optimization notes

- **Benchmark ID:** 14
- **Difficulty:** medium
- **Relevant Notes:** [93, 98, 108, 142, 159, 160, 183, 195, 196, 213]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 26.50 |
| Predicted Intent | general |
| Expected Intent | reference |
| Intent Correct | False |

---

### INTENT — SQL tips and advanced query techniques

- **Benchmark ID:** 15
- **Difficulty:** medium
- **Relevant Notes:** [58, 69, 74, 104, 123, 136, 139, 144, 175, 176]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 24.77 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |

---

### INTENT — Regular expression notes and examples

- **Benchmark ID:** 16
- **Difficulty:** easy
- **Relevant Notes:** [102, 121, 135, 148, 189, 224, 238, 246, 254, 266]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 24.03 |
| Predicted Intent | general |
| Expected Intent | reference |
| Intent Correct | False |

---

### INTENT — Shell and command line tips I've collected

- **Benchmark ID:** 17
- **Difficulty:** easy
- **Relevant Notes:** [147, 153, 243, 314, 355, 374, 379, 455, 597, 688]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 25.23 |
| Predicted Intent | general |
| Expected Intent | reference |
| Intent Correct | False |

---

### INTENT — What do I know about RAG systems?

- **Benchmark ID:** 18
- **Difficulty:** medium
- **Relevant Notes:** [65, 114, 186, 197, 219, 222, 267, 296, 310, 376]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 24.35 |
| Predicted Intent | question |
| Expected Intent | study |
| Intent Correct | False |

---

### INTENT — Retrieval augmented generation notes

- **Benchmark ID:** 19
- **Difficulty:** easy
- **Relevant Notes:** [65, 114, 186, 197, 219, 222, 267, 296, 310, 376]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 22.93 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |

---

### INTENT — Notes about embeddings and vector search

- **Benchmark ID:** 20
- **Difficulty:** medium
- **Relevant Notes:** [168, 183, 228, 289, 298, 323, 376, 486, 487, 523]
- **Retrieved Notes:** [1083, 1076, 1050, 1049, 1042]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 31.67 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |
| Predicted Category | Study - Cross-encoder Reranking |
| Expected Category | Study - AI |
| Category Correct | True |

---

### INTENT — How do text embeddings work?

- **Benchmark ID:** 21
- **Difficulty:** medium
- **Relevant Notes:** [168, 183, 228, 289, 298, 323, 376, 486, 487, 523]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 26.77 |
| Predicted Intent | question |
| Expected Intent | study |
| Intent Correct | False |

---

### INTENT — Large language model notes and findings

- **Benchmark ID:** 22
- **Difficulty:** medium
- **Relevant Notes:** [60, 119, 122, 136, 143, 186, 251, 268, 313, 329]
- **Retrieved Notes:** [1108, 1102, 1098, 1096, 1092]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 34.71 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |
| Predicted Category | Tasks |
| Expected Category | Study - AI |
| Category Correct | False |

---

### INTENT — What LLMs have I worked with?

- **Benchmark ID:** 23
- **Difficulty:** easy
- **Relevant Notes:** [60, 119, 122, 136, 143, 186, 251, 268, 313, 329]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 29.13 |
| Predicted Intent | question |
| Expected Intent | study |
| Intent Correct | False |

---

### INTENT — Document chunking strategy notes

- **Benchmark ID:** 24
- **Difficulty:** medium
- **Relevant Notes:** [197, 214, 257, 268, 289, 432, 446, 478, 487, 510]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 25.70 |
| Predicted Intent | general |
| Expected Intent | reference |
| Intent Correct | False |

---

### INTENT — Notes about reranking in search systems

- **Benchmark ID:** 25
- **Difficulty:** hard
- **Relevant Notes:** [67, 119, 123, 176, 386, 648, 676, 776, 876, 976]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 27.11 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |

---

### INTENT — RAG and retrieval evaluation metrics

- **Benchmark ID:** 26
- **Difficulty:** hard
- **Relevant Notes:** [90, 119, 210, 310, 402, 485, 487, 595]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 27.33 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |

---

### INTENT — How do I measure retrieval quality?

- **Benchmark ID:** 27
- **Difficulty:** hard
- **Relevant Notes:** [90, 119, 210, 310, 402, 485, 487, 595]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 29.96 |
| Predicted Intent | question |
| Expected Intent | study |
| Intent Correct | False |

---

### INTENT — LLM fine-tuning and alignment notes

- **Benchmark ID:** 28
- **Difficulty:** hard
- **Relevant Notes:** [118, 129, 137, 143, 157, 171, 178, 196, 264, 328]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 29.07 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |

---

### INTENT — Prompting techniques and tips

- **Benchmark ID:** 29
- **Difficulty:** medium
- **Relevant Notes:** [130, 191, 264, 268, 406, 436, 446, 456, 467, 493]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 23.66 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |

---

### INTENT — What have I learned about LLM prompting?

- **Benchmark ID:** 30
- **Difficulty:** easy
- **Relevant Notes:** [130, 191, 264, 268, 406, 436, 446, 456, 467, 493]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 23.24 |
| Predicted Intent | question |
| Expected Intent | study |
| Intent Correct | False |

---

### INTENT — Notes about LLM hallucination and grounding

- **Benchmark ID:** 31
- **Difficulty:** medium
- **Relevant Notes:** [197, 222, 446, 470, 485, 600, 730, 830, 930, 1030]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 30.78 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |

---

### INTENT — HyDE and query expansion techniques

- **Benchmark ID:** 32
- **Difficulty:** hard
- **Relevant Notes:** [531, 683, 783, 883, 983, 1083]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 22.27 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |

---

### INTENT — Operating systems study notes

- **Benchmark ID:** 33
- **Difficulty:** medium
- **Relevant Notes:** [59, 132, 141, 146, 174, 179, 203, 205, 233, 255]
- **Retrieved Notes:** [1106, 1038, 1006, 930, 830]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 25.26 |
| Predicted Intent | study |
| Expected Intent | study |
| Intent Correct | True |
| Predicted Category | Study - Operating Systems |
| Expected Category | Study - Operating Systems |
| Category Correct | True |

---

### INTENT — OS concepts I need to review for exams

- **Benchmark ID:** 34
- **Difficulty:** easy
- **Relevant Notes:** [59, 132, 141, 146, 174, 179, 203, 205, 233, 255]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 27.95 |
| Predicted Intent | idea |
| Expected Intent | study |
| Intent Correct | False |

---

### INTENT — Database management systems notes

- **Benchmark ID:** 35
- **Difficulty:** medium
- **Relevant Notes:** [139, 144, 198, 229, 252, 308, 321, 417, 425, 593]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 29.33 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |

---

### INTENT — Computer networks study notes

- **Benchmark ID:** 36
- **Difficulty:** medium
- **Relevant Notes:** [75, 118, 159, 162, 168, 180, 237, 276, 280, 298]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 24.50 |
| Predicted Intent | study |
| Expected Intent | study |
| Intent Correct | True |

---

### INTENT — Algorithm and data structures notes

- **Benchmark ID:** 37
- **Difficulty:** medium
- **Relevant Notes:** [59, 60, 116, 156, 182, 204, 215, 244, 247, 261]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 24.76 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |

---

### INTENT — What algorithms have I studied?

- **Benchmark ID:** 38
- **Difficulty:** easy
- **Relevant Notes:** [59, 60, 116, 156, 182, 204, 215, 244, 247, 261]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 24.06 |
| Predicted Intent | question |
| Expected Intent | study |
| Intent Correct | False |

---

### INTENT — Compiler design and theory of computation notes

- **Benchmark ID:** 39
- **Difficulty:** hard
- **Relevant Notes:** [148, 227, 228, 241, 311, 578, 633]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 25.02 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |

---

### INTENT — Capstone project notes

- **Benchmark ID:** 40
- **Difficulty:** medium
- **Relevant Notes:** [175, 190, 199, 225, 233, 236, 263, 277, 285, 382]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 24.38 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |

---

### INTENT — Parallel programming and concurrency notes

- **Benchmark ID:** 41
- **Difficulty:** hard
- **Relevant Notes:** [151, 229, 283, 287, 296, 304, 421, 462, 474, 504]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 24.56 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |

---

### INTENT — LeetCode problem patterns and solutions

- **Benchmark ID:** 42
- **Difficulty:** medium
- **Relevant Notes:** [117, 127, 187, 224, 271, 279, 282, 316, 327, 387]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 21.50 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |

---

### INTENT — Dynamic programming notes and patterns

- **Benchmark ID:** 43
- **Difficulty:** hard
- **Relevant Notes:** [118, 129, 152, 157, 178, 224, 271, 328, 349, 399]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 24.90 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |

---

### INTENT — System design interview prep notes

- **Benchmark ID:** 44
- **Difficulty:** medium
- **Relevant Notes:** [70, 145, 255, 267, 305, 309, 334, 344, 346, 360]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 23.55 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |

---

### INTENT — What system design topics have I covered?

- **Benchmark ID:** 45
- **Difficulty:** easy
- **Relevant Notes:** [70, 145, 255, 267, 305, 309, 334, 344, 346, 360]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 30.00 |
| Predicted Intent | question |
| Expected Intent | study |
| Intent Correct | False |

---

### INTENT — Behavioral interview preparation notes

- **Benchmark ID:** 46
- **Difficulty:** medium
- **Relevant Notes:** [169, 197, 263, 294, 309, 344, 468, 478, 504, 605]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 27.77 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |

---

### INTENT — Mock interview notes and feedback

- **Benchmark ID:** 47
- **Difficulty:** medium
- **Relevant Notes:** [126, 152, 154, 199, 280, 352, 507, 521, 609, 611]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 26.21 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |

---

### INTENT — Resume writing and improvement tips

- **Benchmark ID:** 48
- **Difficulty:** easy
- **Relevant Notes:** [100, 142, 185, 270, 523, 525]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 22.11 |
| Predicted Intent | general |
| Expected Intent | reference |
| Intent Correct | False |

---

### INTENT — Campus placement preparation notes

- **Benchmark ID:** 49
- **Difficulty:** easy
- **Relevant Notes:** [54, 77, 100, 111, 176, 225, 236, 318, 343, 344]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 34.49 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |

---

### INTENT — Database sharding and partitioning notes

- **Benchmark ID:** 50
- **Difficulty:** hard
- **Relevant Notes:** [259, 292, 417, 580, 608, 695, 731, 795, 831, 895]
- **Retrieved Notes:** [1095, 1094, 1059, 1056, 1023]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 32.43 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |
| Predicted Category | Study - Sqlalchemy |
| Expected Category | Study - System Design |
| Category Correct | True |

---

### INTENT — Caching strategies and implementations

- **Benchmark ID:** 51
- **Difficulty:** medium
- **Relevant Notes:** [103, 124, 146, 237, 269, 275, 284, 295, 318, 336]
- **Retrieved Notes:** [1106, 1038, 1006, 930, 830]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 29.20 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |
| Predicted Category | Study - Operating Systems |
| Expected Category | Study - System Design |
| Category Correct | True |

---

### INTENT — Message queue and event streaming notes

- **Benchmark ID:** 52
- **Difficulty:** medium
- **Relevant Notes:** [71, 102, 144, 174, 200, 218, 238, 269, 297, 304]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 29.26 |
| Predicted Intent | communication |
| Expected Intent | study |
| Intent Correct | False |

---

### INTENT — Microservices architecture notes

- **Benchmark ID:** 53
- **Difficulty:** hard
- **Relevant Notes:** [189, 263, 299, 372, 410, 652, 665, 697, 752, 765]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 27.44 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |

---

### INTENT — Distributed systems consensus notes

- **Benchmark ID:** 54
- **Difficulty:** hard
- **Relevant Notes:** [99, 140, 264, 299, 308, 346, 354, 390, 439, 450]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 30.94 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |

---

### INTENT — Observability and monitoring notes

- **Benchmark ID:** 55
- **Difficulty:** medium
- **Relevant Notes:** [299, 477, 570, 665, 765, 865, 965, 1065]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 29.09 |
| Predicted Intent | general |
| Expected Intent | reference |
| Intent Correct | False |

---

### INTENT — Idempotency and distributed system reliability notes

- **Benchmark ID:** 56
- **Difficulty:** hard
- **Relevant Notes:** [140, 299, 392, 431, 665, 765, 865, 965, 1065]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 31.19 |
| Predicted Intent | general |
| Expected Intent | reference |
| Intent Correct | False |

---

### INTENT — KnowledgeVault project notes

- **Benchmark ID:** 57
- **Difficulty:** easy
- **Relevant Notes:** [57, 88, 89, 90, 91, 94, 95, 96, 97, 107]
- **Retrieved Notes:** [638, 603, 555, 540, 505]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 32.07 |
| Predicted Intent | general |
| Expected Intent | reference |
| Intent Correct | False |
| Predicted Category | Study - Knowledge Vault |
| Expected Category | Reference - KnowledgeVault |
| Category Correct | False |

---

### INTENT — What decisions have I made for the KnowledgeVault project?

- **Benchmark ID:** 58
- **Difficulty:** medium
- **Relevant Notes:** [57, 88, 89, 90, 91, 94, 95, 96, 97, 107]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 27.59 |
| Predicted Intent | question |
| Expected Intent | reference |
| Intent Correct | False |

---

### INTENT — Notes about hybrid retrieval implementation

- **Benchmark ID:** 59
- **Difficulty:** hard
- **Relevant Notes:** [183, 213, 252, 375, 381, 486, 518, 555, 696, 702]
- **Retrieved Notes:** [1029, 1017, 929, 917, 829]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 30.14 |
| Predicted Intent | general |
| Expected Intent | reference |
| Intent Correct | False |
| Predicted Category | Study - API Performance |
| Expected Category | Reference - KnowledgeVault |
| Category Correct | False |

---

### INTENT — Docker and containerization notes

- **Benchmark ID:** 60
- **Difficulty:** easy
- **Relevant Notes:** [72, 75, 91, 105, 118, 138, 188, 192, 242, 295]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 31.01 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |

---

### INTENT — What Docker tips have I collected?

- **Benchmark ID:** 61
- **Difficulty:** easy
- **Relevant Notes:** [72, 75, 91, 105, 118, 138, 188, 192, 242, 295]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 25.55 |
| Predicted Intent | question |
| Expected Intent | reference |
| Intent Correct | False |

---

### INTENT — FastAPI development notes

- **Benchmark ID:** 62
- **Difficulty:** medium
- **Relevant Notes:** [68, 132, 145, 165, 167, 266, 272, 313, 350, 365]
- **Retrieved Notes:** [1063, 1025, 963, 925, 920]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 39.85 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |
| Predicted Category | Study - FastAPI |
| Expected Category | Study - FastAPI |
| Category Correct | True |

---

### INTENT — PostgreSQL database notes

- **Benchmark ID:** 63
- **Difficulty:** medium
- **Relevant Notes:** [58, 66, 74, 104, 139, 144, 168, 175, 215, 267]
- **Retrieved Notes:** [1104, 1099, 1004, 999, 904]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 41.54 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |
| Predicted Category | Reference - PostgreSQL |
| Expected Category | Study - PostgreSQL |
| Category Correct | False |

---

### INTENT — What PostgreSQL features and tips do I have?

- **Benchmark ID:** 64
- **Difficulty:** easy
- **Relevant Notes:** [58, 66, 74, 104, 139, 144, 168, 175, 215, 267]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 31.95 |
| Predicted Intent | question |
| Expected Intent | study |
| Intent Correct | False |

---

### INTENT — Redis usage and patterns

- **Benchmark ID:** 65
- **Difficulty:** easy
- **Relevant Notes:** [61, 73, 92, 103, 124, 146, 157, 174, 237, 246]
- **Retrieved Notes:** [92, 61, 1105, 1073, 1046]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.200 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 38.77 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |
| Predicted Category | Study - Redis |
| Expected Category | Study - Redis |
| Category Correct | True |

---

### INTENT — pgvector and vector search notes

- **Benchmark ID:** 66
- **Difficulty:** hard
- **Relevant Notes:** [66, 168, 183, 215, 217, 228, 252, 298, 323, 333]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 27.81 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |

---

### INTENT — What meetings have I had?

- **Benchmark ID:** 67
- **Difficulty:** easy
- **Relevant Notes:** [56, 106, 107, 149, 170, 233, 251, 283, 304, 359]
- **Retrieved Notes:** [1044, 944, 844, 744, 601]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 35.23 |
| Predicted Intent | event |
| Expected Intent | event |
| Intent Correct | True |
| Predicted Category | Meetings |
| Expected Category | Meetings |
| Category Correct | True |

---

### INTENT — Team meeting notes

- **Benchmark ID:** 68
- **Difficulty:** easy
- **Relevant Notes:** [56, 106, 107, 149, 170, 233, 251, 283, 304, 359]
- **Retrieved Notes:** [1044, 944, 844, 744, 601]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 32.56 |
| Predicted Intent | event |
| Expected Intent | event |
| Intent Correct | True |
| Predicted Category | Meetings |
| Expected Category | Meetings |
| Category Correct | True |

---

### INTENT — Mentor and senior advice I've received

- **Benchmark ID:** 69
- **Difficulty:** easy
- **Relevant Notes:** [68, 126, 185, 199, 236, 260, 272, 274, 330, 372]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 31.19 |
| Predicted Intent | general |
| Expected Intent | communication |
| Intent Correct | False |

---

### INTENT — Hackathon planning notes

- **Benchmark ID:** 70
- **Difficulty:** easy
- **Relevant Notes:** [55, 324, 448, 463, 535, 542]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 27.03 |
| Predicted Intent | general |
| Expected Intent | event |
| Intent Correct | False |

---

### INTENT — What are my pending tasks and deadlines?

- **Benchmark ID:** 71
- **Difficulty:** easy
- **Relevant Notes:** [155, 179, 184, 207, 233, 266]
- **Retrieved Notes:** [1108, 1102, 1098, 1096, 1092]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 42.25 |
| Predicted Intent | todo |
| Expected Intent | todo |
| Intent Correct | True |
| Predicted Category | Tasks |
| Expected Category | Tasks |
| Category Correct | True |

---

### INTENT — What health appointments do I have?

- **Benchmark ID:** 72
- **Difficulty:** easy
- **Relevant Notes:** [78, 79, 109, 157, 179, 201, 210, 212, 224, 226]
- **Retrieved Notes:** [325, 291, 201, 79]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.200 |
| Hit | True |
| Reciprocal Rank | 0.333 |
| Latency (ms) | 32.20 |
| Predicted Intent | reminder |
| Expected Intent | reminder |
| Intent Correct | True |
| Predicted Category | Appointments |
| Expected Category | Appointments |
| Category Correct | True |

---

### INTENT — What payments and bills do I need to make?

- **Benchmark ID:** 73
- **Difficulty:** easy
- **Relevant Notes:** [77, 120, 126, 128, 131, 137, 140, 144, 160, 162]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 30.44 |
| Predicted Intent | question |
| Expected Intent | todo |
| Intent Correct | False |

---

### INTENT — What is on my shopping list?

- **Benchmark ID:** 74
- **Difficulty:** easy
- **Relevant Notes:** [76, 322]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 29.67 |
| Predicted Intent | question |
| Expected Intent | todo |
| Intent Correct | False |

---

### INTENT — Show all my reminders

- **Benchmark ID:** 75
- **Difficulty:** easy
- **Relevant Notes:** [55, 152, 212, 312, 542, 557]
- **Retrieved Notes:** [1052, 952, 852, 752, 700]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 35.01 |
| Predicted Intent | reminder |
| Expected Intent | reminder |
| Intent Correct | True |
| Predicted Category | Reminders |
| Expected Category | Reminders |
| Category Correct | True |

---

### INTENT — What do I need to remember this week?

- **Benchmark ID:** 76
- **Difficulty:** medium
- **Relevant Notes:** [55, 152, 212, 312, 542, 557]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 25.30 |
| Predicted Intent | question |
| Expected Intent | reminder |
| Intent Correct | False |

---

### INTENT — My budget and expense tracking notes

- **Benchmark ID:** 77
- **Difficulty:** easy
- **Relevant Notes:** [82, 153, 202, 210, 216, 254, 281, 291, 331, 345]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 24.14 |
| Predicted Intent | general |
| Expected Intent | todo |
| Intent Correct | False |

---

### INTENT — Monthly expense breakdown

- **Benchmark ID:** 78
- **Difficulty:** medium
- **Relevant Notes:** [82, 153, 202, 210, 216, 254, 281, 291, 331, 345]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 22.48 |
| Predicted Intent | general |
| Expected Intent | reference |
| Intent Correct | False |

---

### INTENT — Investment and savings notes

- **Benchmark ID:** 79
- **Difficulty:** medium
- **Relevant Notes:** [113, 273, 496, 561, 591, 594, 750, 850, 950, 1050]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 24.05 |
| Predicted Intent | general |
| Expected Intent | reference |
| Intent Correct | False |

---

### INTENT — Tech purchase notes and wishlists

- **Benchmark ID:** 80
- **Difficulty:** easy
- **Relevant Notes:** [115, 124, 174, 200, 211, 307, 420, 434, 442, 445]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 26.91 |
| Predicted Intent | general |
| Expected Intent | todo |
| Intent Correct | False |

---

### INTENT — My travel plans and notes

- **Benchmark ID:** 81
- **Difficulty:** easy
- **Relevant Notes:** [78, 81, 115, 126, 128, 130, 160, 171, 175, 176]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 22.71 |
| Predicted Intent | general |
| Expected Intent | todo |
| Intent Correct | False |

---

### INTENT — Upcoming trips and travel bookings

- **Benchmark ID:** 82
- **Difficulty:** easy
- **Relevant Notes:** [78, 81, 115, 126, 128, 130, 160, 171, 175, 176]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 25.11 |
| Predicted Intent | general |
| Expected Intent | todo |
| Intent Correct | False |

---

### INTENT — Delhi trip plans

- **Benchmark ID:** 83
- **Difficulty:** easy
- **Relevant Notes:** [55, 115, 256, 324, 448, 463, 524, 535, 542, 577]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 22.86 |
| Predicted Intent | general |
| Expected Intent | todo |
| Intent Correct | False |

---

### INTENT — Hill station and trekking plans

- **Benchmark ID:** 84
- **Difficulty:** medium
- **Relevant Notes:** [81, 128, 351, 407]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 25.86 |
| Predicted Intent | general |
| Expected Intent | todo |
| Intent Correct | False |

---

### INTENT — Train booking tips and notes

- **Benchmark ID:** 85
- **Difficulty:** easy
- **Relevant Notes:** [160, 463, 596]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 24.26 |
| Predicted Intent | general |
| Expected Intent | reference |
| Intent Correct | False |

---

### INTENT — Fitness and workout notes

- **Benchmark ID:** 86
- **Difficulty:** easy
- **Relevant Notes:** [173, 185, 202, 232, 246, 291, 317, 380, 392, 427]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 26.17 |
| Predicted Intent | general |
| Expected Intent | todo |
| Intent Correct | False |

---

### INTENT — My exercise routine notes

- **Benchmark ID:** 87
- **Difficulty:** easy
- **Relevant Notes:** [173, 185, 202, 232, 246, 291, 317, 380, 392, 427]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 23.01 |
| Predicted Intent | general |
| Expected Intent | todo |
| Intent Correct | False |

---

### INTENT — Sleep improvement notes

- **Benchmark ID:** 88
- **Difficulty:** medium
- **Relevant Notes:** [133, 136, 202, 288, 348, 380, 434, 538, 548, 574]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 24.08 |
| Predicted Intent | general |
| Expected Intent | reference |
| Intent Correct | False |

---

### INTENT — Nutrition and supplement notes

- **Benchmark ID:** 89
- **Difficulty:** medium
- **Relevant Notes:** [109, 133, 226, 286]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 24.77 |
| Predicted Intent | general |
| Expected Intent | reference |
| Intent Correct | False |

---

### INTENT — Mental health and wellbeing notes

- **Benchmark ID:** 90
- **Difficulty:** medium
- **Relevant Notes:** [152, 288, 291, 317, 472, 575]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 28.75 |
| Predicted Intent | general |
| Expected Intent | reference |
| Intent Correct | False |

---

### INTENT — My startup ideas and business notes

- **Benchmark ID:** 91
- **Difficulty:** easy
- **Relevant Notes:** [85, 86, 117, 120, 125, 128, 131, 134, 143, 157]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 28.37 |
| Predicted Intent | idea |
| Expected Intent | idea |
| Intent Correct | True |

---

### INTENT — What business ideas have I documented?

- **Benchmark ID:** 92
- **Difficulty:** easy
- **Relevant Notes:** [85, 86, 117, 120, 125, 128, 131, 134, 143, 157]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 25.39 |
| Predicted Intent | idea |
| Expected Intent | idea |
| Intent Correct | True |

---

### INTENT — Y Combinator and startup ecosystem notes

- **Benchmark ID:** 93
- **Difficulty:** medium
- **Relevant Notes:** [72, 133, 137, 205, 248, 307, 342, 347, 438, 536]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 31.58 |
| Predicted Intent | idea |
| Expected Intent | reference |
| Intent Correct | False |

---

### INTENT — Business model and monetization notes

- **Benchmark ID:** 94
- **Difficulty:** medium
- **Relevant Notes:** [210, 216, 330, 331, 514, 594, 617, 624, 649]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 36.59 |
| Predicted Intent | general |
| Expected Intent | reference |
| Intent Correct | False |

---

### INTENT — Startup idea validation notes

- **Benchmark ID:** 95
- **Difficulty:** medium
- **Relevant Notes:** [108, 117, 126, 132, 134, 146, 173, 199, 204, 210]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 32.41 |
| Predicted Intent | idea |
| Expected Intent | reference |
| Intent Correct | False |

---

### INTENT — What books have I taken notes on?

- **Benchmark ID:** 96
- **Difficulty:** easy
- **Relevant Notes:** [78, 128, 141, 155, 160, 172, 182, 194, 208, 234]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 29.22 |
| Predicted Intent | question |
| Expected Intent | reference |
| Intent Correct | False |

---

### INTENT — My book notes and summaries

- **Benchmark ID:** 97
- **Difficulty:** easy
- **Relevant Notes:** [78, 128, 141, 155, 160, 172, 182, 194, 208, 234]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 25.89 |
| Predicted Intent | general |
| Expected Intent | reference |
| Intent Correct | False |

---

### INTENT — Notes from Designing Data-Intensive Applications

- **Benchmark ID:** 98
- **Difficulty:** hard
- **Relevant Notes:** [439, 528]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 28.21 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |

---

### INTENT — Atomic Habits notes and takeaways

- **Benchmark ID:** 99
- **Difficulty:** easy
- **Relevant Notes:** [164, 304, 317, 349, 482, 557, 631, 634, 698, 734]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 29.40 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |

---

### INTENT — Podcast notes and key insights

- **Benchmark ID:** 100
- **Difficulty:** easy
- **Relevant Notes:** [230, 419, 548]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 21.73 |
| Predicted Intent | general |
| Expected Intent | reference |
| Intent Correct | False |

---

### INTENT — Online courses I'm taking or completed

- **Benchmark ID:** 101
- **Difficulty:** easy
- **Relevant Notes:** [71, 145, 231, 266, 357, 394, 417, 471, 519, 611]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 25.96 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |

---

### INTENT — Kubernetes learning notes

- **Benchmark ID:** 102
- **Difficulty:** medium
- **Relevant Notes:** [62, 101, 118, 180, 181, 225, 230, 263, 299, 355]
- **Retrieved Notes:** [1071, 971, 871, 865, 797]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 31.72 |
| Predicted Intent | study |
| Expected Intent | study |
| Intent Correct | True |
| Predicted Category | Study - Kubernetes |
| Expected Category | Study - Kubernetes |
| Category Correct | True |

---

### INTENT — Terraform and infrastructure as code notes

- **Benchmark ID:** 103
- **Difficulty:** medium
- **Relevant Notes:** [274]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 22.13 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |

---

### INTENT — Authentication and authorization notes

- **Benchmark ID:** 104
- **Difficulty:** medium
- **Relevant Notes:** [63, 129, 165, 189, 227, 244, 276, 287, 338, 346]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 23.19 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |

---

### INTENT — Testing and pytest notes

- **Benchmark ID:** 105
- **Difficulty:** medium
- **Relevant Notes:** [108, 124, 126, 152, 153, 163, 165, 172, 245, 277]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 26.24 |
| Predicted Intent | general |
| Expected Intent | reference |
| Intent Correct | False |

---

### INTENT — Debugging sessions and fixes

- **Benchmark ID:** 106
- **Difficulty:** medium
- **Relevant Notes:** [94, 136, 161, 246, 258, 335, 340, 362, 421, 461]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 24.91 |
| Predicted Intent | general |
| Expected Intent | reference |
| Intent Correct | False |

---

### INTENT — What bugs have I debugged recently?

- **Benchmark ID:** 107
- **Difficulty:** easy
- **Relevant Notes:** [94, 136, 161, 246, 258, 335]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 27.76 |
| Predicted Intent | question |
| Expected Intent | reference |
| Intent Correct | False |

---

### INTENT — SQLAlchemy N+1 query problem notes

- **Benchmark ID:** 108
- **Difficulty:** hard
- **Relevant Notes:** [363, 588, 589, 659, 759, 859, 959, 1059]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 28.30 |
| Predicted Intent | general |
| Expected Intent | reference |
| Intent Correct | False |

---

### INTENT — Race condition and concurrency bug notes

- **Benchmark ID:** 109
- **Difficulty:** hard
- **Relevant Notes:** [229, 246, 296, 321, 384, 421, 462, 474, 482, 499]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 25.08 |
| Predicted Intent | general |
| Expected Intent | reference |
| Intent Correct | False |

---

### INTENT — Memory management and leak debugging notes

- **Benchmark ID:** 110
- **Difficulty:** hard
- **Relevant Notes:** [124, 146, 169, 175, 182, 219, 248, 273, 275, 279]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 23.51 |
| Predicted Intent | general |
| Expected Intent | reference |
| Intent Correct | False |

---

### INTENT — My journal entries and personal reflections

- **Benchmark ID:** 111
- **Difficulty:** easy
- **Relevant Notes:** [113, 149, 152, 162, 166, 191, 251, 255]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 32.89 |
| Predicted Intent | general |
| Expected Intent | general |
| Intent Correct | True |

---

### INTENT — Productivity tips and personal notes

- **Benchmark ID:** 112
- **Difficulty:** easy
- **Relevant Notes:** [85, 199, 224, 240, 248, 286, 429, 453, 529, 550]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 28.90 |
| Predicted Intent | general |
| Expected Intent | reference |
| Intent Correct | False |

---

### INTENT — Career direction and goal notes

- **Benchmark ID:** 113
- **Difficulty:** medium
- **Relevant Notes:** [56, 61, 91, 96, 101, 106, 166, 175, 177, 180]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 29.29 |
| Predicted Intent | general |
| Expected Intent | general |
| Intent Correct | True |

---

### INTENT — Open source and building in public notes

- **Benchmark ID:** 114
- **Difficulty:** medium
- **Relevant Notes:** [117, 141, 255, 395, 400, 440, 453, 522, 554, 555]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 26.27 |
| Predicted Intent | general |
| Expected Intent | idea |
| Intent Correct | False |

---

### INTENT — KnowledgeVault RAG pipeline decisions and findings

- **Benchmark ID:** 115
- **Difficulty:** hard
- **Relevant Notes:** [1028, 262, 1030, 1032, 523, 267, 533, 1053]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 29.03 |
| Predicted Intent | general |
| Expected Intent | reference |
| Intent Correct | False |

---

### INTENT — All my interview preparation notes — coding and system design

- **Benchmark ID:** 116
- **Difficulty:** hard
- **Relevant Notes:** [769, 129, 387, 642, 516, 255, 392, 267, 271, 399]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 29.34 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |

---

### INTENT — AI system infrastructure notes: vector DB, cache, and retrieval

- **Benchmark ID:** 117
- **Difficulty:** hard
- **Relevant Notes:** [1024, 1030, 1031, 1032, 520, 523, 1036, 1042]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 27.32 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |

---

### INTENT — All my health and wellness notes

- **Benchmark ID:** 118
- **Difficulty:** medium
- **Relevant Notes:** [643, 764, 773, 646, 133, 392, 905, 522]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 38.27 |
| Predicted Intent | general |
| Expected Intent | reference |
| Intent Correct | False |

---

### INTENT — Financial tasks and expense notes

- **Benchmark ID:** 119
- **Difficulty:** medium
- **Relevant Notes:** [1028, 1035, 1043, 1044, 1046, 535, 538, 540]
- **Retrieved Notes:** [1108, 1102, 1098, 1096, 1092]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 31.97 |
| Predicted Intent | todo |
| Expected Intent | todo |
| Intent Correct | True |
| Predicted Category | Tasks |
| Expected Category | Finance |
| Category Correct | True |

---

### INTENT — My university computer science notes

- **Benchmark ID:** 120
- **Difficulty:** hard
- **Relevant Notes:** [513, 1026, 1027, 515, 516, 510, 1031, 1034, 1038, 526]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 25.27 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |

---

### INTENT — Things I need to do this week

- **Benchmark ID:** 121
- **Difficulty:** medium
- **Relevant Notes:** [155, 179, 184, 207, 233, 266]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 21.09 |
| Predicted Intent | general |
| Expected Intent | todo |
| Intent Correct | False |

---

### INTENT — What tasks are pending for me?

- **Benchmark ID:** 122
- **Difficulty:** medium
- **Relevant Notes:** [155, 179, 184, 207, 233, 266]
- **Retrieved Notes:** [1108, 1102, 1098, 1096, 1092]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 32.84 |
| Predicted Intent | todo |
| Expected Intent | todo |
| Intent Correct | True |
| Predicted Category | Tasks |
| Expected Category | Tasks |
| Category Correct | True |

---

### INTENT — Resources for learning backend development

- **Benchmark ID:** 123
- **Difficulty:** medium
- **Relevant Notes:** [1025, 772, 775, 1031, 1032, 266, 523, 267]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 25.89 |
| Predicted Intent | study |
| Expected Intent | study |
| Intent Correct | True |

---

### INTENT — How do I get better at backend engineering?

- **Benchmark ID:** 124
- **Difficulty:** medium
- **Relevant Notes:** [1025, 772, 775, 1031, 1032, 266]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 29.16 |
| Predicted Intent | question |
| Expected Intent | study |
| Intent Correct | False |

---

### INTENT — What are distributed systems trade-offs?

- **Benchmark ID:** 125
- **Difficulty:** hard
- **Relevant Notes:** [897, 771, 259, 390, 1031, 264]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 28.83 |
| Predicted Intent | question |
| Expected Intent | study |
| Intent Correct | False |

---

### INTENT — Notes on scalability and reliability

- **Benchmark ID:** 126
- **Difficulty:** hard
- **Relevant Notes:** [1024, 259, 644, 1031, 520, 906]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 23.37 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |

---

### INTENT — What are my creative ideas?

- **Benchmark ID:** 127
- **Difficulty:** easy
- **Relevant Notes:** [85, 86, 117, 120, 125, 128]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 27.63 |
| Predicted Intent | idea |
| Expected Intent | idea |
| Intent Correct | True |

---

### INTENT — Show my brainstorming notes

- **Benchmark ID:** 128
- **Difficulty:** easy
- **Relevant Notes:** [128, 514, 131, 260, 134, 262, 1035, 525]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 24.21 |
| Predicted Intent | general |
| Expected Intent | idea |
| Intent Correct | False |

---

### INTENT — Advice and wisdom I've collected

- **Benchmark ID:** 129
- **Difficulty:** medium
- **Relevant Notes:** [260, 1028, 522, 1035, 525, 272]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 25.27 |
| Predicted Intent | general |
| Expected Intent | general |
| Intent Correct | True |

---

### INTENT — BM25

- **Benchmark ID:** 130
- **Difficulty:** easy
- **Relevant Notes:** [228, 252, 696, 796, 896, 996, 1096]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 23.27 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |

---

### INTENT — HNSW index

- **Benchmark ID:** 131
- **Difficulty:** easy
- **Relevant Notes:** [215, 430, 681, 781, 881, 981, 1081]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 23.45 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |

---

### INTENT — HNSW vector index configuration

- **Benchmark ID:** 132
- **Difficulty:** medium
- **Relevant Notes:** [215, 430, 681, 781, 881, 981, 1081]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 34.83 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |

---

### INTENT — Reciprocal Rank Fusion

- **Benchmark ID:** 133
- **Difficulty:** medium
- **Relevant Notes:** [518, 718, 818, 918, 1018]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 22.23 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |

---

### INTENT — two sum problem

- **Benchmark ID:** 134
- **Difficulty:** easy
- **Relevant Notes:** [278, 677, 777, 877, 977, 1077]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 29.21 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |

---

### INTENT — LRU cache implementation

- **Benchmark ID:** 135
- **Difficulty:** medium
- **Relevant Notes:** [318, 336, 520, 530, 579, 736, 738, 836, 838, 936]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 23.61 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |

---

### INTENT — CAP theorem

- **Benchmark ID:** 136
- **Difficulty:** easy
- **Relevant Notes:** [580, 608]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 25.51 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |

---

### INTENT — PageRank or graph algorithms notes

- **Benchmark ID:** 137
- **Difficulty:** medium
- **Relevant Notes:** [60, 158, 224, 316, 342, 347, 545, 546, 619, 667]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 23.32 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |

---

### INTENT — What have I been working on this month?

- **Benchmark ID:** 138
- **Difficulty:** hard
- **Relevant Notes:** [77, 149, 164, 182, 216, 286]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 28.67 |
| Predicted Intent | question |
| Expected Intent | general |
| Intent Correct | False |

---

### INTENT — Recent notes and activities

- **Benchmark ID:** 139
- **Difficulty:** hard
- **Relevant Notes:** [77, 149, 164, 182, 216, 286]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 24.05 |
| Predicted Intent | general |
| Expected Intent | general |
| Intent Correct | True |

---

### INTENT — Redis vs Kafka — when to use each

- **Benchmark ID:** 140
- **Difficulty:** hard
- **Relevant Notes:** [1024, 771, 1027, 773, 520, 1034]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 26.12 |
| Predicted Intent | question |
| Expected Intent | study |
| Intent Correct | False |

---

### INTENT — Python vs Go programming notes

- **Benchmark ID:** 141
- **Difficulty:** hard
- **Relevant Notes:** [512, 320, 898, 266, 138, 586]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 24.75 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |

---

### INTENT — SQL vs NoSQL database comparison

- **Benchmark ID:** 142
- **Difficulty:** hard
- **Relevant Notes:** [772, 775, 904, 1031, 1032, 139]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 28.07 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |

---

### INTENT — Comparing RAG retrieval strategies: dense, sparse, and reranking

- **Benchmark ID:** 143
- **Difficulty:** hard
- **Relevant Notes:** [386, 1030, 648, 649, 776, 267]
- **Retrieved Notes:** [1029, 1017, 929, 917, 829]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 31.71 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |
| Predicted Category | Study - API Performance |
| Expected Category | Study - AI |
| Category Correct | True |

---

### INTENT — REST vs GraphQL API design trade-offs

- **Benchmark ID:** 144
- **Difficulty:** hard
- **Relevant Notes:** [68, 93, 96, 132, 136, 142]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 28.50 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |

---

### INTENT — Show all my communication notes

- **Benchmark ID:** 145
- **Difficulty:** easy
- **Relevant Notes:** [54, 55, 56, 57, 106, 117]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 27.56 |
| Predicted Intent | general |
| Expected Intent | communication |
| Intent Correct | False |

---

### INTENT — All my reminder notes

- **Benchmark ID:** 146
- **Difficulty:** easy
- **Relevant Notes:** [55, 152, 212, 312, 542, 557]
- **Retrieved Notes:** [1052, 952, 852, 752, 700]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 27.25 |
| Predicted Intent | reminder |
| Expected Intent | reminder |
| Intent Correct | True |
| Predicted Category | Reminders |
| Expected Category | Reminders |
| Category Correct | True |

---

### INTENT — My study notes on AI and machine learning

- **Benchmark ID:** 147
- **Difficulty:** easy
- **Relevant Notes:** [1026, 774, 1030, 510, 523, 268, 267, 782]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 28.06 |
| Predicted Intent | study |
| Expected Intent | study |
| Intent Correct | True |

---

### INTENT — Notes categorized under system design

- **Benchmark ID:** 148
- **Difficulty:** easy
- **Relevant Notes:** [70, 145, 255, 267, 305, 309]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 34.25 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |

---

### INTENT — Programming notes I've taken recently

- **Benchmark ID:** 149
- **Difficulty:** medium
- **Relevant Notes:** [512, 1025, 898, 132, 266, 523]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 35.29 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |

---

### INTENT — My financial notes

- **Benchmark ID:** 150
- **Difficulty:** medium
- **Relevant Notes:** [646, 202, 331, 591, 273, 82]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 35.14 |
| Predicted Intent | general |
| Expected Intent | todo |
| Intent Correct | False |

---

### INTENT — Projects and ideas I'm excited about

- **Benchmark ID:** 151
- **Difficulty:** hard
- **Relevant Notes:** [514, 260, 1028, 262, 1032, 522]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 26.29 |
| Predicted Intent | idea |
| Expected Intent | idea |
| Intent Correct | True |

---

### INTENT — Personal notes and self-improvement

- **Benchmark ID:** 152
- **Difficulty:** hard
- **Relevant Notes:** [522, 1035, 785, 529, 277, 283]
- **Retrieved Notes:** []

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 23.41 |
| Predicted Intent | general |
| Expected Intent | general |
| Intent Correct | True |

---

### HYBRID — What are useful Python tips and tricks I've learned?

- **Benchmark ID:** 1
- **Difficulty:** easy
- **Relevant Notes:** [108, 174, 177, 206, 232, 239, 272, 283]
- **Retrieved Notes:** [318, 206, 633, 357, 464]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.125 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| Latency (ms) | 87.58 |
| Predicted Intent | question |
| Expected Intent | study |
| Intent Correct | False |

---

### HYBRID — Show my Python programming notes

- **Benchmark ID:** 2
- **Difficulty:** easy
- **Relevant Notes:** [108, 174, 177, 206, 232, 239, 272, 283]
- **Retrieved Notes:** [87, 583, 699, 799, 899]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 75.99 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |

---

### HYBRID — Notes about Python dictionaries and hash maps

- **Benchmark ID:** 3
- **Difficulty:** easy
- **Relevant Notes:** [108, 271, 278, 284, 397, 464, 483, 560, 579, 587]
- **Retrieved Notes:** [284, 587, 397, 464, 745]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.800 |
| Recall@5 | 0.400 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 73.70 |
| Predicted Intent | general |
| Expected Intent | reference |
| Intent Correct | False |

---

### HYBRID — How does Python async programming work?

- **Benchmark ID:** 4
- **Difficulty:** medium
- **Relevant Notes:** [170, 283, 304, 359, 364, 372, 471, 661, 662, 663]
- **Retrieved Notes:** [304, 734, 834, 934, 1034]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.100 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 76.88 |
| Predicted Intent | question |
| Expected Intent | study |
| Intent Correct | False |

---

### HYBRID — Concurrency and asynchronous patterns in Python

- **Benchmark ID:** 5
- **Difficulty:** medium
- **Relevant Notes:** [170, 283, 304, 359, 364, 372, 471, 661, 662, 663]
- **Retrieved Notes:** [304, 734, 834, 934, 1034]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.100 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 75.78 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |

---

### HYBRID — Python decorator notes

- **Benchmark ID:** 6
- **Difficulty:** easy
- **Relevant Notes:** [174, 414, 435, 455, 549, 610, 614]
- **Retrieved Notes:** [610, 549, 177, 318, 414]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.600 |
| Recall@5 | 0.429 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 79.54 |
| Predicted Intent | general |
| Expected Intent | reference |
| Intent Correct | False |

---

### HYBRID — What git commands and workflows have I noted?

- **Benchmark ID:** 7
- **Difficulty:** easy
- **Relevant Notes:** [130, 135, 144, 169, 229, 272, 317, 328, 366, 395]
- **Retrieved Notes:** [612, 328, 501, 614, 522]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.100 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| Latency (ms) | 80.44 |
| Predicted Intent | question |
| Expected Intent | reference |
| Intent Correct | False |

---

### HYBRID — Git tips and tricks

- **Benchmark ID:** 8
- **Difficulty:** easy
- **Relevant Notes:** [130, 135, 144, 169, 229, 272, 317, 328, 366, 395]
- **Retrieved Notes:** [646, 497, 719, 819, 919]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 76.33 |
| Predicted Intent | general |
| Expected Intent | reference |
| Intent Correct | False |
| Predicted Category | Ideas - Semantic Retrieval |
| Expected Category | Reference - Git |
| Category Correct | False |

---

### HYBRID — JavaScript and TypeScript notes

- **Benchmark ID:** 9
- **Difficulty:** easy
- **Relevant Notes:** [218, 220, 250, 297, 418, 713, 720, 813, 820, 913]
- **Retrieved Notes:** [218, 713, 813, 913, 1013]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.800 |
| Recall@5 | 0.400 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 74.75 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |

---

### HYBRID — What have I learned about Go programming?

- **Benchmark ID:** 10
- **Difficulty:** medium
- **Relevant Notes:** [114, 138, 206, 208, 266, 297, 320, 339, 488, 512]
- **Retrieved Notes:** [572, 634, 698, 798, 898]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 73.33 |
| Predicted Intent | question |
| Expected Intent | study |
| Intent Correct | False |

---

### HYBRID — Rust ownership and borrowing notes

- **Benchmark ID:** 11
- **Difficulty:** medium
- **Relevant Notes:** [151, 182, 210, 351, 370, 380, 459, 494, 539, 563]
- **Retrieved Notes:** [370, 689, 789, 889, 989]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.100 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 79.37 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |
| Predicted Category | Study - System Design |
| Expected Category | Study - Rust |
| Category Correct | True |

---

### HYBRID — What design patterns have I documented?

- **Benchmark ID:** 12
- **Difficulty:** medium
- **Relevant Notes:** [102, 121, 189, 203, 224, 238, 246, 254, 266, 269]
- **Retrieved Notes:** [102, 121, 687, 787, 887]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.200 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 75.29 |
| Predicted Intent | question |
| Expected Intent | reference |
| Intent Correct | False |

---

### HYBRID — Software design patterns notes

- **Benchmark ID:** 13
- **Difficulty:** easy
- **Relevant Notes:** [102, 121, 189, 203, 224, 238, 246, 254, 266, 269]
- **Retrieved Notes:** [102, 106, 309, 121, 687]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.200 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 66.59 |
| Predicted Intent | general |
| Expected Intent | reference |
| Intent Correct | False |

---

### HYBRID — Performance optimization notes

- **Benchmark ID:** 14
- **Difficulty:** medium
- **Relevant Notes:** [93, 98, 108, 142, 159, 160, 183, 195, 196, 213]
- **Retrieved Notes:** [195, 547, 58, 530, 738]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.100 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 72.93 |
| Predicted Intent | general |
| Expected Intent | reference |
| Intent Correct | False |

---

### HYBRID — SQL tips and advanced query techniques

- **Benchmark ID:** 15
- **Difficulty:** medium
- **Relevant Notes:** [58, 69, 74, 104, 123, 136, 139, 144, 175, 176]
- **Retrieved Notes:** [398, 184, 385, 402, 58]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.100 |
| Hit | True |
| Reciprocal Rank | 0.200 |
| Latency (ms) | 74.39 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |

---

### HYBRID — Regular expression notes and examples

- **Benchmark ID:** 16
- **Difficulty:** easy
- **Relevant Notes:** [102, 121, 135, 148, 189, 224, 238, 246, 254, 266]
- **Retrieved Notes:** [135, 148, 515, 489, 227]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.200 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 72.21 |
| Predicted Intent | general |
| Expected Intent | reference |
| Intent Correct | False |

---

### HYBRID — Shell and command line tips I've collected

- **Benchmark ID:** 17
- **Difficulty:** easy
- **Relevant Notes:** [147, 153, 243, 314, 355, 374, 379, 455, 597, 688]
- **Retrieved Notes:** [597, 268, 682, 782, 882]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.100 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 80.60 |
| Predicted Intent | general |
| Expected Intent | reference |
| Intent Correct | False |

---

### HYBRID — What do I know about RAG systems?

- **Benchmark ID:** 18
- **Difficulty:** medium
- **Relevant Notes:** [65, 114, 186, 197, 219, 222, 267, 296, 310, 376]
- **Retrieved Notes:** [386, 436, 470, 565, 197]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.100 |
| Hit | True |
| Reciprocal Rank | 0.200 |
| Latency (ms) | 69.72 |
| Predicted Intent | question |
| Expected Intent | study |
| Intent Correct | False |

---

### HYBRID — Retrieval augmented generation notes

- **Benchmark ID:** 19
- **Difficulty:** easy
- **Relevant Notes:** [65, 114, 186, 197, 219, 222, 267, 296, 310, 376]
- **Retrieved Notes:** [65, 186, 398, 184, 289]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.200 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 75.97 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |

---

### HYBRID — Notes about embeddings and vector search

- **Benchmark ID:** 20
- **Difficulty:** medium
- **Relevant Notes:** [168, 183, 228, 289, 298, 323, 376, 486, 487, 523]
- **Retrieved Notes:** [196, 333, 298, 726, 826]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.100 |
| Hit | True |
| Reciprocal Rank | 0.333 |
| Latency (ms) | 91.00 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |
| Predicted Category | Study - Cross-encoder Reranking |
| Expected Category | Study - AI |
| Category Correct | True |

---

### HYBRID — How do text embeddings work?

- **Benchmark ID:** 21
- **Difficulty:** medium
- **Relevant Notes:** [168, 183, 228, 289, 298, 323, 376, 486, 487, 523]
- **Retrieved Notes:** [298, 726, 826, 926, 1026]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.100 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 76.44 |
| Predicted Intent | question |
| Expected Intent | study |
| Intent Correct | False |

---

### HYBRID — Large language model notes and findings

- **Benchmark ID:** 22
- **Difficulty:** medium
- **Relevant Notes:** [60, 119, 122, 136, 143, 186, 251, 268, 313, 329]
- **Retrieved Notes:** [186, 404, 708, 808, 908]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.100 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 107.42 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |
| Predicted Category | Tasks |
| Expected Category | Study - AI |
| Category Correct | False |

---

### HYBRID — What LLMs have I worked with?

- **Benchmark ID:** 23
- **Difficulty:** easy
- **Relevant Notes:** [60, 119, 122, 136, 143, 186, 251, 268, 313, 329]
- **Retrieved Notes:** [143, 543, 427, 509, 268]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.200 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 75.92 |
| Predicted Intent | question |
| Expected Intent | study |
| Intent Correct | False |

---

### HYBRID — Document chunking strategy notes

- **Benchmark ID:** 24
- **Difficulty:** medium
- **Relevant Notes:** [197, 214, 257, 268, 289, 432, 446, 478, 487, 510]
- **Retrieved Notes:** [558, 533, 721, 821, 921]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 67.52 |
| Predicted Intent | general |
| Expected Intent | reference |
| Intent Correct | False |

---

### HYBRID — Notes about reranking in search systems

- **Benchmark ID:** 25
- **Difficulty:** hard
- **Relevant Notes:** [67, 119, 123, 176, 386, 648, 676, 776, 876, 976]
- **Retrieved Notes:** [67, 176, 119, 305, 58]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.600 |
| Recall@5 | 0.300 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 78.16 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |

---

### HYBRID — RAG and retrieval evaluation metrics

- **Benchmark ID:** 26
- **Difficulty:** hard
- **Relevant Notes:** [90, 119, 210, 310, 402, 485, 487, 595]
- **Retrieved Notes:** [386, 485, 310, 595, 186]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.600 |
| Recall@5 | 0.375 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| Latency (ms) | 84.79 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |

---

### HYBRID — How do I measure retrieval quality?

- **Benchmark ID:** 27
- **Difficulty:** hard
- **Relevant Notes:** [90, 119, 210, 310, 402, 485, 487, 595]
- **Retrieved Notes:** [310, 86, 485, 402, 213]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.600 |
| Recall@5 | 0.375 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 76.52 |
| Predicted Intent | question |
| Expected Intent | study |
| Intent Correct | False |

---

### HYBRID — LLM fine-tuning and alignment notes

- **Benchmark ID:** 28
- **Difficulty:** hard
- **Relevant Notes:** [118, 129, 137, 143, 157, 171, 178, 196, 264, 328]
- **Retrieved Notes:** [592, 143, 613, 268, 682]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.100 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| Latency (ms) | 89.09 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |

---

### HYBRID — Prompting techniques and tips

- **Benchmark ID:** 29
- **Difficulty:** medium
- **Relevant Notes:** [130, 191, 264, 268, 406, 436, 446, 456, 467, 493]
- **Retrieved Notes:** [406, 264, 507, 459, 199]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.200 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 100.49 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |

---

### HYBRID — What have I learned about LLM prompting?

- **Benchmark ID:** 30
- **Difficulty:** easy
- **Relevant Notes:** [130, 191, 264, 268, 406, 436, 446, 456, 467, 493]
- **Retrieved Notes:** [268, 682, 782, 882, 982]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.100 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 87.16 |
| Predicted Intent | question |
| Expected Intent | study |
| Intent Correct | False |

---

### HYBRID — Notes about LLM hallucination and grounding

- **Benchmark ID:** 31
- **Difficulty:** medium
- **Relevant Notes:** [197, 222, 446, 470, 485, 600, 730, 830, 930, 1030]
- **Retrieved Notes:** [197, 478, 600, 651, 716]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.200 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 84.73 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |

---

### HYBRID — HyDE and query expansion techniques

- **Benchmark ID:** 32
- **Difficulty:** hard
- **Relevant Notes:** [531, 683, 783, 883, 983, 1083]
- **Retrieved Notes:** [184, 531, 683, 783, 883]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.800 |
| Recall@5 | 0.667 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| Latency (ms) | 97.75 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |

---

### HYBRID — Operating systems study notes

- **Benchmark ID:** 33
- **Difficulty:** medium
- **Relevant Notes:** [59, 132, 141, 146, 174, 179, 203, 205, 233, 255]
- **Retrieved Notes:** [59, 527, 106, 547, 465]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.100 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 84.68 |
| Predicted Intent | study |
| Expected Intent | study |
| Intent Correct | True |
| Predicted Category | Study - Operating Systems |
| Expected Category | Study - Operating Systems |
| Category Correct | True |

---

### HYBRID — OS concepts I need to review for exams

- **Benchmark ID:** 34
- **Difficulty:** easy
- **Relevant Notes:** [59, 132, 141, 146, 174, 179, 203, 205, 233, 255]
- **Retrieved Notes:** [360, 59, 309, 169, 527]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.100 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| Latency (ms) | 75.21 |
| Predicted Intent | idea |
| Expected Intent | study |
| Intent Correct | False |

---

### HYBRID — Database management systems notes

- **Benchmark ID:** 35
- **Difficulty:** medium
- **Relevant Notes:** [139, 144, 198, 229, 252, 308, 321, 417, 425, 593]
- **Retrieved Notes:** [425, 231, 439, 608, 144]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.200 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 77.83 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |

---

### HYBRID — Computer networks study notes

- **Benchmark ID:** 36
- **Difficulty:** medium
- **Relevant Notes:** [75, 118, 159, 162, 168, 180, 237, 276, 280, 298]
- **Retrieved Notes:** [327, 532, 106, 99, 439]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 74.18 |
| Predicted Intent | study |
| Expected Intent | study |
| Intent Correct | True |

---

### HYBRID — Algorithm and data structures notes

- **Benchmark ID:** 37
- **Difficulty:** medium
- **Relevant Notes:** [59, 60, 116, 156, 182, 204, 215, 244, 247, 261]
- **Retrieved Notes:** [530, 738, 838, 938, 1038]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 72.12 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |

---

### HYBRID — What algorithms have I studied?

- **Benchmark ID:** 38
- **Difficulty:** easy
- **Relevant Notes:** [59, 60, 116, 156, 182, 204, 215, 244, 247, 261]
- **Retrieved Notes:** [619, 60, 333, 66, 536]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.100 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| Latency (ms) | 69.32 |
| Predicted Intent | question |
| Expected Intent | study |
| Intent Correct | False |

---

### HYBRID — Compiler design and theory of computation notes

- **Benchmark ID:** 39
- **Difficulty:** hard
- **Relevant Notes:** [148, 227, 228, 241, 311, 578, 633]
- **Retrieved Notes:** [227, 547, 465, 311, 530]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.286 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 75.80 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |

---

### HYBRID — Capstone project notes

- **Benchmark ID:** 40
- **Difficulty:** medium
- **Relevant Notes:** [175, 190, 199, 225, 233, 236, 263, 277, 285, 382]
- **Retrieved Notes:** [568, 233, 498, 382, 175]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.600 |
| Recall@5 | 0.300 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| Latency (ms) | 73.33 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |

---

### HYBRID — Parallel programming and concurrency notes

- **Benchmark ID:** 41
- **Difficulty:** hard
- **Relevant Notes:** [151, 229, 283, 287, 296, 304, 421, 462, 474, 504]
- **Retrieved Notes:** [296, 283, 662, 762, 862]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.200 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 70.73 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |

---

### HYBRID — LeetCode problem patterns and solutions

- **Benchmark ID:** 42
- **Difficulty:** medium
- **Relevant Notes:** [117, 127, 187, 224, 271, 279, 282, 316, 327, 387]
- **Retrieved Notes:** [224, 611, 316, 399, 546]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.200 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 71.22 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |

---

### HYBRID — Dynamic programming notes and patterns

- **Benchmark ID:** 43
- **Difficulty:** hard
- **Relevant Notes:** [118, 129, 152, 157, 178, 224, 271, 328, 349, 399]
- **Retrieved Notes:** [562, 227, 460, 701, 801]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 77.44 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |

---

### HYBRID — System design interview prep notes

- **Benchmark ID:** 44
- **Difficulty:** medium
- **Relevant Notes:** [70, 145, 255, 267, 305, 309, 334, 344, 346, 360]
- **Retrieved Notes:** [360, 70, 106, 309, 99]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.600 |
| Recall@5 | 0.300 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 78.06 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |

---

### HYBRID — What system design topics have I covered?

- **Benchmark ID:** 45
- **Difficulty:** easy
- **Relevant Notes:** [70, 145, 255, 267, 305, 309, 334, 344, 346, 360]
- **Retrieved Notes:** [360, 392, 309, 70, 99]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.600 |
| Recall@5 | 0.300 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 79.26 |
| Predicted Intent | question |
| Expected Intent | study |
| Intent Correct | False |

---

### HYBRID — Behavioral interview preparation notes

- **Benchmark ID:** 46
- **Difficulty:** medium
- **Relevant Notes:** [169, 197, 263, 294, 309, 344, 468, 478, 504, 605]
- **Retrieved Notes:** [294, 468, 360, 288, 352]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.200 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 75.02 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |

---

### HYBRID — Mock interview notes and feedback

- **Benchmark ID:** 47
- **Difficulty:** medium
- **Relevant Notes:** [126, 152, 154, 199, 280, 352, 507, 521, 609, 611]
- **Retrieved Notes:** [126, 360, 540, 352, 507]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.600 |
| Recall@5 | 0.300 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 77.50 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |

---

### HYBRID — Resume writing and improvement tips

- **Benchmark ID:** 48
- **Difficulty:** easy
- **Relevant Notes:** [100, 142, 185, 270, 523, 525]
- **Retrieved Notes:** [100, 142, 185, 525, 472]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.800 |
| Recall@5 | 0.667 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 87.53 |
| Predicted Intent | general |
| Expected Intent | reference |
| Intent Correct | False |

---

### HYBRID — Campus placement preparation notes

- **Benchmark ID:** 49
- **Difficulty:** easy
- **Relevant Notes:** [54, 77, 100, 111, 176, 225, 236, 318, 343, 344]
- **Retrieved Notes:** [415, 620, 100, 236, 343]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.600 |
| Recall@5 | 0.300 |
| Hit | True |
| Reciprocal Rank | 0.333 |
| Latency (ms) | 79.99 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |

---

### HYBRID — Database sharding and partitioning notes

- **Benchmark ID:** 50
- **Difficulty:** hard
- **Relevant Notes:** [259, 292, 417, 580, 608, 695, 731, 795, 831, 895]
- **Retrieved Notes:** [292, 695, 795, 895, 995]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.800 |
| Recall@5 | 0.400 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 104.43 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |
| Predicted Category | Study - Sqlalchemy |
| Expected Category | Study - System Design |
| Category Correct | True |

---

### HYBRID — Caching strategies and implementations

- **Benchmark ID:** 51
- **Difficulty:** medium
- **Relevant Notes:** [103, 124, 146, 237, 269, 275, 284, 295, 318, 336]
- **Retrieved Notes:** [61, 93, 644, 602, 467]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 89.07 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |
| Predicted Category | Study - Operating Systems |
| Expected Category | Study - System Design |
| Category Correct | True |

---

### HYBRID — Message queue and event streaming notes

- **Benchmark ID:** 52
- **Difficulty:** medium
- **Relevant Notes:** [71, 102, 144, 174, 200, 218, 238, 269, 297, 304]
- **Retrieved Notes:** [450, 671, 771, 871, 971]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 80.44 |
| Predicted Intent | communication |
| Expected Intent | study |
| Intent Correct | False |

---

### HYBRID — Microservices architecture notes

- **Benchmark ID:** 53
- **Difficulty:** hard
- **Relevant Notes:** [189, 263, 299, 372, 410, 652, 665, 697, 752, 765]
- **Retrieved Notes:** [372, 392, 106, 102, 410]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.200 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 83.37 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |

---

### HYBRID — Distributed systems consensus notes

- **Benchmark ID:** 54
- **Difficulty:** hard
- **Relevant Notes:** [99, 140, 264, 299, 308, 346, 354, 390, 439, 450]
- **Retrieved Notes:** [354, 608, 99, 580, 439]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.600 |
| Recall@5 | 0.300 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 79.55 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |

---

### HYBRID — Observability and monitoring notes

- **Benchmark ID:** 55
- **Difficulty:** medium
- **Relevant Notes:** [299, 477, 570, 665, 765, 865, 965, 1065]
- **Retrieved Notes:** [477, 410, 424, 140, 372]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.125 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 79.27 |
| Predicted Intent | general |
| Expected Intent | reference |
| Intent Correct | False |

---

### HYBRID — Idempotency and distributed system reliability notes

- **Benchmark ID:** 56
- **Difficulty:** hard
- **Relevant Notes:** [140, 299, 392, 431, 665, 765, 865, 965, 1065]
- **Retrieved Notes:** [140, 431, 608, 99, 580]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.222 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 73.92 |
| Predicted Intent | general |
| Expected Intent | reference |
| Intent Correct | False |

---

### HYBRID — KnowledgeVault project notes

- **Benchmark ID:** 57
- **Difficulty:** easy
- **Relevant Notes:** [57, 88, 89, 90, 91, 94, 95, 96, 97, 107]
- **Retrieved Notes:** [125, 95, 96, 89, 90]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.800 |
| Recall@5 | 0.400 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| Latency (ms) | 87.01 |
| Predicted Intent | general |
| Expected Intent | reference |
| Intent Correct | False |
| Predicted Category | Study - Knowledge Vault |
| Expected Category | Reference - KnowledgeVault |
| Category Correct | False |

---

### HYBRID — What decisions have I made for the KnowledgeVault project?

- **Benchmark ID:** 58
- **Difficulty:** medium
- **Relevant Notes:** [57, 88, 89, 90, 91, 94, 95, 96, 97, 107]
- **Retrieved Notes:** [638, 90, 428, 728, 828]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.100 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| Latency (ms) | 97.10 |
| Predicted Intent | question |
| Expected Intent | reference |
| Intent Correct | False |

---

### HYBRID — Notes about hybrid retrieval implementation

- **Benchmark ID:** 59
- **Difficulty:** hard
- **Relevant Notes:** [183, 213, 252, 375, 381, 486, 518, 555, 696, 702]
- **Retrieved Notes:** [486, 702, 802, 902, 1002]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.200 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 74.96 |
| Predicted Intent | general |
| Expected Intent | reference |
| Intent Correct | False |
| Predicted Category | Study - API Performance |
| Expected Category | Reference - KnowledgeVault |
| Category Correct | False |

---

### HYBRID — Docker and containerization notes

- **Benchmark ID:** 60
- **Difficulty:** easy
- **Relevant Notes:** [72, 75, 91, 105, 118, 138, 188, 192, 242, 295]
- **Retrieved Notes:** [72, 105, 192, 75, 491]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.800 |
| Recall@5 | 0.400 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 85.23 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |

---

### HYBRID — What Docker tips have I collected?

- **Benchmark ID:** 61
- **Difficulty:** easy
- **Relevant Notes:** [72, 75, 91, 105, 118, 138, 188, 192, 242, 295]
- **Retrieved Notes:** [72, 192, 295, 105, 75]

| Metric | Value |
|-------|------:|
| Precision@5 | 1.000 |
| Recall@5 | 0.500 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 186.11 |
| Predicted Intent | question |
| Expected Intent | reference |
| Intent Correct | False |

---

### HYBRID — FastAPI development notes

- **Benchmark ID:** 62
- **Difficulty:** medium
- **Relevant Notes:** [68, 132, 145, 165, 167, 266, 272, 313, 350, 365]
- **Retrieved Notes:** [68, 165, 725, 825, 925]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.200 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 156.84 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |
| Predicted Category | Study - FastAPI |
| Expected Category | Study - FastAPI |
| Category Correct | True |

---

### HYBRID — PostgreSQL database notes

- **Benchmark ID:** 63
- **Difficulty:** medium
- **Relevant Notes:** [58, 66, 74, 104, 139, 144, 168, 175, 215, 267]
- **Retrieved Notes:** [74, 144, 417, 731, 831]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.200 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 102.58 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |
| Predicted Category | Reference - PostgreSQL |
| Expected Category | Study - PostgreSQL |
| Category Correct | False |

---

### HYBRID — What PostgreSQL features and tips do I have?

- **Benchmark ID:** 64
- **Difficulty:** easy
- **Relevant Notes:** [58, 66, 74, 104, 139, 144, 168, 175, 215, 267]
- **Retrieved Notes:** [58, 74, 144, 367, 628]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.600 |
| Recall@5 | 0.300 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 122.30 |
| Predicted Intent | question |
| Expected Intent | study |
| Intent Correct | False |

---

### HYBRID — Redis usage and patterns

- **Benchmark ID:** 65
- **Difficulty:** easy
- **Relevant Notes:** [61, 73, 92, 103, 124, 146, 157, 174, 237, 246]
- **Retrieved Notes:** [73, 92, 269, 724, 824]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.200 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 105.22 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |
| Predicted Category | Study - Redis |
| Expected Category | Study - Redis |
| Category Correct | True |

---

### HYBRID — pgvector and vector search notes

- **Benchmark ID:** 66
- **Difficulty:** hard
- **Relevant Notes:** [66, 168, 183, 215, 217, 228, 252, 298, 323, 333]
- **Retrieved Notes:** [66, 323, 742, 842, 942]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.200 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 110.86 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |

---

### HYBRID — What meetings have I had?

- **Benchmark ID:** 67
- **Difficulty:** easy
- **Relevant Notes:** [56, 106, 107, 149, 170, 233, 251, 283, 304, 359]
- **Retrieved Notes:** [371, 107, 263, 559, 233]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.200 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| Latency (ms) | 143.60 |
| Predicted Intent | event |
| Expected Intent | event |
| Intent Correct | True |
| Predicted Category | Meetings |
| Expected Category | Meetings |
| Category Correct | True |

---

### HYBRID — Team meeting notes

- **Benchmark ID:** 68
- **Difficulty:** easy
- **Relevant Notes:** [56, 106, 107, 149, 170, 233, 251, 283, 304, 359]
- **Retrieved Notes:** [233, 203, 87, 107, 125]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.200 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 110.72 |
| Predicted Intent | event |
| Expected Intent | event |
| Intent Correct | True |
| Predicted Category | Meetings |
| Expected Category | Meetings |
| Category Correct | True |

---

### HYBRID — Mentor and senior advice I've received

- **Benchmark ID:** 69
- **Difficulty:** easy
- **Relevant Notes:** [68, 126, 185, 199, 236, 260, 272, 274, 330, 372]
- **Retrieved Notes:** [199, 185, 428, 728, 828]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.200 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 102.89 |
| Predicted Intent | general |
| Expected Intent | communication |
| Intent Correct | False |

---

### HYBRID — Hackathon planning notes

- **Benchmark ID:** 70
- **Difficulty:** easy
- **Relevant Notes:** [55, 324, 448, 463, 535, 542]
- **Retrieved Notes:** [448, 324, 463, 55, 542]

| Metric | Value |
|-------|------:|
| Precision@5 | 1.000 |
| Recall@5 | 0.833 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 94.16 |
| Predicted Intent | general |
| Expected Intent | event |
| Intent Correct | False |

---

### HYBRID — What are my pending tasks and deadlines?

- **Benchmark ID:** 71
- **Difficulty:** easy
- **Relevant Notes:** [155, 179, 184, 207, 233, 266]
- **Retrieved Notes:** [498, 453, 233, 647, 235]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.167 |
| Hit | True |
| Reciprocal Rank | 0.333 |
| Latency (ms) | 124.73 |
| Predicted Intent | todo |
| Expected Intent | todo |
| Intent Correct | True |
| Predicted Category | Tasks |
| Expected Category | Tasks |
| Category Correct | True |

---

### HYBRID — What health appointments do I have?

- **Benchmark ID:** 72
- **Difficulty:** easy
- **Relevant Notes:** [78, 79, 109, 157, 179, 201, 210, 212, 224, 226]
- **Retrieved Notes:** [79, 601, 559, 575, 198]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.100 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 96.17 |
| Predicted Intent | reminder |
| Expected Intent | reminder |
| Intent Correct | True |
| Predicted Category | Appointments |
| Expected Category | Appointments |
| Category Correct | True |

---

### HYBRID — What payments and bills do I need to make?

- **Benchmark ID:** 73
- **Difficulty:** easy
- **Relevant Notes:** [77, 120, 126, 128, 131, 137, 140, 144, 160, 162]
- **Retrieved Notes:** [341, 77, 82, 635, 368]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.100 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| Latency (ms) | 91.91 |
| Predicted Intent | question |
| Expected Intent | todo |
| Intent Correct | False |

---

### HYBRID — What is on my shopping list?

- **Benchmark ID:** 74
- **Difficulty:** easy
- **Relevant Notes:** [76, 322]
- **Retrieved Notes:** [393, 322, 606, 115, 76]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 1.000 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| Latency (ms) | 92.60 |
| Predicted Intent | question |
| Expected Intent | todo |
| Intent Correct | False |

---

### HYBRID — Show all my reminders

- **Benchmark ID:** 75
- **Difficulty:** easy
- **Relevant Notes:** [55, 152, 212, 312, 542, 557]
- **Retrieved Notes:** [382, 56, 312, 290, 442]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.167 |
| Hit | True |
| Reciprocal Rank | 0.333 |
| Latency (ms) | 135.66 |
| Predicted Intent | reminder |
| Expected Intent | reminder |
| Intent Correct | True |
| Predicted Category | Reminders |
| Expected Category | Reminders |
| Category Correct | True |

---

### HYBRID — What do I need to remember this week?

- **Benchmark ID:** 76
- **Difficulty:** medium
- **Relevant Notes:** [55, 152, 212, 312, 542, 557]
- **Retrieved Notes:** [77, 212, 475, 442, 755]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.167 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| Latency (ms) | 91.11 |
| Predicted Intent | question |
| Expected Intent | reminder |
| Intent Correct | False |

---

### HYBRID — My budget and expense tracking notes

- **Benchmark ID:** 77
- **Difficulty:** easy
- **Relevant Notes:** [82, 153, 202, 210, 216, 254, 281, 291, 331, 345]
- **Retrieved Notes:** [82, 216, 606, 393, 285]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.200 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 96.25 |
| Predicted Intent | general |
| Expected Intent | todo |
| Intent Correct | False |

---

### HYBRID — Monthly expense breakdown

- **Benchmark ID:** 78
- **Difficulty:** medium
- **Relevant Notes:** [82, 153, 202, 210, 216, 254, 281, 291, 331, 345]
- **Retrieved Notes:** [82, 216, 490, 606, 341]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.200 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 91.81 |
| Predicted Intent | general |
| Expected Intent | reference |
| Intent Correct | False |

---

### HYBRID — Investment and savings notes

- **Benchmark ID:** 79
- **Difficulty:** medium
- **Relevant Notes:** [113, 273, 496, 561, 591, 594, 750, 850, 950, 1050]
- **Retrieved Notes:** [162, 285, 113, 594, 539]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.200 |
| Hit | True |
| Reciprocal Rank | 0.333 |
| Latency (ms) | 95.86 |
| Predicted Intent | general |
| Expected Intent | reference |
| Intent Correct | False |

---

### HYBRID — Tech purchase notes and wishlists

- **Benchmark ID:** 80
- **Difficulty:** easy
- **Relevant Notes:** [115, 124, 174, 200, 211, 307, 420, 434, 442, 445]
- **Retrieved Notes:** [444, 605, 87, 262, 285]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 95.53 |
| Predicted Intent | general |
| Expected Intent | todo |
| Intent Correct | False |

---

### HYBRID — My travel plans and notes

- **Benchmark ID:** 81
- **Difficulty:** easy
- **Relevant Notes:** [78, 81, 115, 126, 128, 130, 160, 171, 175, 176]
- **Retrieved Notes:** [290, 81, 212, 393, 444]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.100 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| Latency (ms) | 94.91 |
| Predicted Intent | general |
| Expected Intent | todo |
| Intent Correct | False |

---

### HYBRID — Upcoming trips and travel bookings

- **Benchmark ID:** 82
- **Difficulty:** easy
- **Relevant Notes:** [78, 81, 115, 126, 128, 130, 160, 171, 175, 176]
- **Retrieved Notes:** [538, 627, 81, 128, 190]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.200 |
| Hit | True |
| Reciprocal Rank | 0.333 |
| Latency (ms) | 97.53 |
| Predicted Intent | general |
| Expected Intent | todo |
| Intent Correct | False |

---

### HYBRID — Delhi trip plans

- **Benchmark ID:** 83
- **Difficulty:** easy
- **Relevant Notes:** [55, 115, 256, 324, 448, 463, 524, 535, 542, 577]
- **Retrieved Notes:** [115, 324, 535, 407, 463]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.800 |
| Recall@5 | 0.400 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 97.56 |
| Predicted Intent | general |
| Expected Intent | todo |
| Intent Correct | False |

---

### HYBRID — Hill station and trekking plans

- **Benchmark ID:** 84
- **Difficulty:** medium
- **Relevant Notes:** [81, 128, 351, 407]
- **Retrieved Notes:** [351, 137, 60, 498, 324]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.250 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 101.81 |
| Predicted Intent | general |
| Expected Intent | todo |
| Intent Correct | False |

---

### HYBRID — Train booking tips and notes

- **Benchmark ID:** 85
- **Difficulty:** easy
- **Relevant Notes:** [160, 463, 596]
- **Retrieved Notes:** [596, 160, 393, 203, 290]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.667 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 96.78 |
| Predicted Intent | general |
| Expected Intent | reference |
| Intent Correct | False |

---

### HYBRID — Fitness and workout notes

- **Benchmark ID:** 86
- **Difficulty:** easy
- **Relevant Notes:** [173, 185, 202, 232, 246, 291, 317, 380, 392, 427]
- **Retrieved Notes:** [631, 481, 87, 482, 83]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 93.76 |
| Predicted Intent | general |
| Expected Intent | todo |
| Intent Correct | False |

---

### HYBRID — My exercise routine notes

- **Benchmark ID:** 87
- **Difficulty:** easy
- **Relevant Notes:** [173, 185, 202, 232, 246, 291, 317, 380, 392, 427]
- **Retrieved Notes:** [631, 83, 87, 380, 680]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.100 |
| Hit | True |
| Reciprocal Rank | 0.250 |
| Latency (ms) | 98.28 |
| Predicted Intent | general |
| Expected Intent | todo |
| Intent Correct | False |

---

### HYBRID — Sleep improvement notes

- **Benchmark ID:** 88
- **Difficulty:** medium
- **Relevant Notes:** [133, 136, 202, 288, 348, 380, 434, 538, 548, 574]
- **Retrieved Notes:** [548, 622, 434, 574, 348]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.800 |
| Recall@5 | 0.400 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 92.45 |
| Predicted Intent | general |
| Expected Intent | reference |
| Intent Correct | False |

---

### HYBRID — Nutrition and supplement notes

- **Benchmark ID:** 89
- **Difficulty:** medium
- **Relevant Notes:** [109, 133, 226, 286]
- **Retrieved Notes:** [286, 133, 322, 87, 285]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.500 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 100.37 |
| Predicted Intent | general |
| Expected Intent | reference |
| Intent Correct | False |

---

### HYBRID — Mental health and wellbeing notes

- **Benchmark ID:** 90
- **Difficulty:** medium
- **Relevant Notes:** [152, 288, 291, 317, 472, 575]
- **Retrieved Notes:** [575, 201, 291, 212, 472]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.600 |
| Recall@5 | 0.500 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 101.65 |
| Predicted Intent | general |
| Expected Intent | reference |
| Intent Correct | False |

---

### HYBRID — My startup ideas and business notes

- **Benchmark ID:** 91
- **Difficulty:** easy
- **Relevant Notes:** [85, 86, 117, 120, 125, 128, 131, 134, 143, 157]
- **Retrieved Notes:** [85, 525, 459, 617, 441]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.100 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 97.05 |
| Predicted Intent | idea |
| Expected Intent | idea |
| Intent Correct | True |

---

### HYBRID — What business ideas have I documented?

- **Benchmark ID:** 92
- **Difficulty:** easy
- **Relevant Notes:** [85, 86, 117, 120, 125, 128, 131, 134, 143, 157]
- **Retrieved Notes:** [225, 178, 85, 441, 459]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.100 |
| Hit | True |
| Reciprocal Rank | 0.333 |
| Latency (ms) | 107.38 |
| Predicted Intent | idea |
| Expected Intent | idea |
| Intent Correct | True |

---

### HYBRID — Y Combinator and startup ecosystem notes

- **Benchmark ID:** 93
- **Difficulty:** medium
- **Relevant Notes:** [72, 133, 137, 205, 248, 307, 342, 347, 438, 536]
- **Retrieved Notes:** [462, 267, 85, 482, 118]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 114.97 |
| Predicted Intent | idea |
| Expected Intent | reference |
| Intent Correct | False |

---

### HYBRID — Business model and monetization notes

- **Benchmark ID:** 94
- **Difficulty:** medium
- **Relevant Notes:** [210, 216, 330, 331, 514, 594, 617, 624, 649]
- **Retrieved Notes:** [178, 262, 285, 308, 393]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 151.26 |
| Predicted Intent | general |
| Expected Intent | reference |
| Intent Correct | False |

---

### HYBRID — Startup idea validation notes

- **Benchmark ID:** 95
- **Difficulty:** medium
- **Relevant Notes:** [108, 117, 126, 132, 134, 146, 173, 199, 204, 210]
- **Retrieved Notes:** [459, 525, 134, 617, 441]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.100 |
| Hit | True |
| Reciprocal Rank | 0.333 |
| Latency (ms) | 123.14 |
| Predicted Intent | idea |
| Expected Intent | reference |
| Intent Correct | False |

---

### HYBRID — What books have I taken notes on?

- **Benchmark ID:** 96
- **Difficulty:** easy
- **Relevant Notes:** [78, 128, 141, 155, 160, 172, 182, 194, 208, 234]
- **Retrieved Notes:** [309, 290, 240, 444, 87]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 107.23 |
| Predicted Intent | question |
| Expected Intent | reference |
| Intent Correct | False |

---

### HYBRID — My book notes and summaries

- **Benchmark ID:** 97
- **Difficulty:** easy
- **Relevant Notes:** [78, 128, 141, 155, 160, 172, 182, 194, 208, 234]
- **Retrieved Notes:** [87, 583, 699, 799, 899]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 117.18 |
| Predicted Intent | general |
| Expected Intent | reference |
| Intent Correct | False |

---

### HYBRID — Notes from Designing Data-Intensive Applications

- **Benchmark ID:** 98
- **Difficulty:** hard
- **Relevant Notes:** [439, 528]
- **Retrieved Notes:** [528, 439, 267, 106, 402]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 1.000 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 138.53 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |

---

### HYBRID — Atomic Habits notes and takeaways

- **Benchmark ID:** 99
- **Difficulty:** easy
- **Relevant Notes:** [164, 304, 317, 349, 482, 557, 631, 634, 698, 734]
- **Retrieved Notes:** [482, 229, 690, 790, 890]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.100 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 110.25 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |

---

### HYBRID — Podcast notes and key insights

- **Benchmark ID:** 100
- **Difficulty:** easy
- **Relevant Notes:** [230, 419, 548]
- **Retrieved Notes:** [230, 87, 419, 442, 755]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.667 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 108.09 |
| Predicted Intent | general |
| Expected Intent | reference |
| Intent Correct | False |

---

### HYBRID — Online courses I'm taking or completed

- **Benchmark ID:** 101
- **Difficulty:** easy
- **Relevant Notes:** [71, 145, 231, 266, 357, 394, 417, 471, 519, 611]
- **Retrieved Notes:** [343, 145, 471, 663, 763]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.200 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| Latency (ms) | 101.78 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |

---

### HYBRID — Kubernetes learning notes

- **Benchmark ID:** 102
- **Difficulty:** medium
- **Relevant Notes:** [62, 101, 118, 180, 181, 225, 230, 263, 299, 355]
- **Retrieved Notes:** [62, 118, 712, 812, 912]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.200 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 121.51 |
| Predicted Intent | study |
| Expected Intent | study |
| Intent Correct | True |
| Predicted Category | Study - Kubernetes |
| Expected Category | Study - Kubernetes |
| Category Correct | True |

---

### HYBRID — Terraform and infrastructure as code notes

- **Benchmark ID:** 103
- **Difficulty:** medium
- **Relevant Notes:** [274]
- **Retrieved Notes:** [274, 62, 181, 106, 316]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 1.000 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 112.69 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |

---

### HYBRID — Authentication and authorization notes

- **Benchmark ID:** 104
- **Difficulty:** medium
- **Relevant Notes:** [63, 129, 165, 189, 227, 244, 276, 287, 338, 346]
- **Retrieved Notes:** [408, 63, 637, 733, 833]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.100 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| Latency (ms) | 107.02 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |

---

### HYBRID — Testing and pytest notes

- **Benchmark ID:** 105
- **Difficulty:** medium
- **Relevant Notes:** [108, 124, 126, 152, 153, 163, 165, 172, 245, 277]
- **Retrieved Notes:** [435, 245, 313, 177, 258]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.100 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| Latency (ms) | 107.23 |
| Predicted Intent | general |
| Expected Intent | reference |
| Intent Correct | False |

---

### HYBRID — Debugging sessions and fixes

- **Benchmark ID:** 106
- **Difficulty:** medium
- **Relevant Notes:** [94, 136, 161, 246, 258, 335, 340, 362, 421, 461]
- **Retrieved Notes:** [632, 591, 163, 522, 246]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.100 |
| Hit | True |
| Reciprocal Rank | 0.200 |
| Latency (ms) | 115.21 |
| Predicted Intent | general |
| Expected Intent | reference |
| Intent Correct | False |

---

### HYBRID — What bugs have I debugged recently?

- **Benchmark ID:** 107
- **Difficulty:** easy
- **Relevant Notes:** [94, 136, 161, 246, 258, 335]
- **Retrieved Notes:** [591, 632, 522, 246, 684]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.167 |
| Hit | True |
| Reciprocal Rank | 0.250 |
| Latency (ms) | 121.40 |
| Predicted Intent | question |
| Expected Intent | reference |
| Intent Correct | False |

---

### HYBRID — SQLAlchemy N+1 query problem notes

- **Benchmark ID:** 108
- **Difficulty:** hard
- **Relevant Notes:** [363, 588, 589, 659, 759, 859, 959, 1059]
- **Retrieved Notes:** [589, 659, 759, 859, 959]

| Metric | Value |
|-------|------:|
| Precision@5 | 1.000 |
| Recall@5 | 0.625 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 122.09 |
| Predicted Intent | general |
| Expected Intent | reference |
| Intent Correct | False |

---

### HYBRID — Race condition and concurrency bug notes

- **Benchmark ID:** 109
- **Difficulty:** hard
- **Relevant Notes:** [229, 246, 296, 321, 384, 421, 462, 474, 482, 499]
- **Retrieved Notes:** [462, 384, 727, 827, 927]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.200 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 100.34 |
| Predicted Intent | general |
| Expected Intent | reference |
| Intent Correct | False |

---

### HYBRID — Memory management and leak debugging notes

- **Benchmark ID:** 110
- **Difficulty:** hard
- **Relevant Notes:** [124, 146, 169, 175, 182, 219, 248, 273, 275, 279]
- **Retrieved Notes:** [547, 591, 318, 169, 275]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.200 |
| Hit | True |
| Reciprocal Rank | 0.250 |
| Latency (ms) | 105.52 |
| Predicted Intent | general |
| Expected Intent | reference |
| Intent Correct | False |

---

### HYBRID — My journal entries and personal reflections

- **Benchmark ID:** 111
- **Difficulty:** easy
- **Relevant Notes:** [113, 149, 152, 162, 166, 191, 251, 255]
- **Retrieved Notes:** [472, 290, 550, 700, 800]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 95.66 |
| Predicted Intent | general |
| Expected Intent | general |
| Intent Correct | True |

---

### HYBRID — Productivity tips and personal notes

- **Benchmark ID:** 112
- **Difficulty:** easy
- **Relevant Notes:** [85, 199, 224, 240, 248, 286, 429, 453, 529, 550]
- **Retrieved Notes:** [87, 583, 699, 799, 899]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 97.06 |
| Predicted Intent | general |
| Expected Intent | reference |
| Intent Correct | False |

---

### HYBRID — Career direction and goal notes

- **Benchmark ID:** 113
- **Difficulty:** medium
- **Relevant Notes:** [56, 61, 91, 96, 101, 106, 166, 175, 177, 180]
- **Retrieved Notes:** [166, 685, 785, 885, 985]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.100 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 106.84 |
| Predicted Intent | general |
| Expected Intent | general |
| Intent Correct | True |

---

### HYBRID — Open source and building in public notes

- **Benchmark ID:** 114
- **Difficulty:** medium
- **Relevant Notes:** [117, 141, 255, 395, 400, 440, 453, 522, 554, 555]
- **Retrieved Notes:** [255, 285, 106, 87, 141]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.200 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 94.83 |
| Predicted Intent | general |
| Expected Intent | idea |
| Intent Correct | False |

---

### HYBRID — KnowledgeVault RAG pipeline decisions and findings

- **Benchmark ID:** 115
- **Difficulty:** hard
- **Relevant Notes:** [1028, 262, 1030, 1032, 523, 267, 533, 1053]
- **Retrieved Notes:** [310, 90, 446, 730, 830]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 136.92 |
| Predicted Intent | general |
| Expected Intent | reference |
| Intent Correct | False |

---

### HYBRID — All my interview preparation notes — coding and system design

- **Benchmark ID:** 116
- **Difficulty:** hard
- **Relevant Notes:** [769, 129, 387, 642, 516, 255, 392, 267, 271, 399]
- **Retrieved Notes:** [360, 70, 309, 99, 126]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 115.95 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |

---

### HYBRID — AI system infrastructure notes: vector DB, cache, and retrieval

- **Benchmark ID:** 117
- **Difficulty:** hard
- **Relevant Notes:** [1024, 1030, 1031, 1032, 520, 523, 1036, 1042]
- **Retrieved Notes:** [333, 66, 61, 644, 523]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.125 |
| Hit | True |
| Reciprocal Rank | 0.200 |
| Latency (ms) | 130.24 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |

---

### HYBRID — All my health and wellness notes

- **Benchmark ID:** 118
- **Difficulty:** medium
- **Relevant Notes:** [643, 764, 773, 646, 133, 392, 905, 522]
- **Retrieved Notes:** [212, 322, 79, 444, 442]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 104.85 |
| Predicted Intent | general |
| Expected Intent | reference |
| Intent Correct | False |

---

### HYBRID — Financial tasks and expense notes

- **Benchmark ID:** 119
- **Difficulty:** medium
- **Relevant Notes:** [1028, 1035, 1043, 1044, 1046, 535, 538, 540]
- **Retrieved Notes:** [82, 87, 393, 216, 285]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 154.96 |
| Predicted Intent | todo |
| Expected Intent | todo |
| Intent Correct | True |
| Predicted Category | Tasks |
| Expected Category | Finance |
| Category Correct | True |

---

### HYBRID — My university computer science notes

- **Benchmark ID:** 120
- **Difficulty:** hard
- **Relevant Notes:** [513, 1026, 1027, 515, 516, 510, 1031, 1034, 1038, 526]
- **Retrieved Notes:** [87, 106, 583, 699, 799]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 99.10 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |

---

### HYBRID — Things I need to do this week

- **Benchmark ID:** 121
- **Difficulty:** medium
- **Relevant Notes:** [155, 179, 184, 207, 233, 266]
- **Retrieved Notes:** [77, 81, 76, 322, 79]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 99.95 |
| Predicted Intent | general |
| Expected Intent | todo |
| Intent Correct | False |

---

### HYBRID — What tasks are pending for me?

- **Benchmark ID:** 122
- **Difficulty:** medium
- **Relevant Notes:** [155, 179, 184, 207, 233, 266]
- **Retrieved Notes:** [235, 264, 283, 289, 504]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 129.84 |
| Predicted Intent | todo |
| Expected Intent | todo |
| Intent Correct | True |
| Predicted Category | Tasks |
| Expected Category | Tasks |
| Category Correct | True |

---

### HYBRID — Resources for learning backend development

- **Benchmark ID:** 123
- **Difficulty:** medium
- **Relevant Notes:** [1025, 772, 775, 1031, 1032, 266, 523, 267]
- **Retrieved Notes:** [106, 61, 330, 96, 101]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 126.12 |
| Predicted Intent | study |
| Expected Intent | study |
| Intent Correct | True |

---

### HYBRID — How do I get better at backend engineering?

- **Benchmark ID:** 124
- **Difficulty:** medium
- **Relevant Notes:** [1025, 772, 775, 1031, 1032, 266]
- **Retrieved Notes:** [272, 106, 166, 685, 785]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 120.28 |
| Predicted Intent | question |
| Expected Intent | study |
| Intent Correct | False |

---

### HYBRID — What are distributed systems trade-offs?

- **Benchmark ID:** 125
- **Difficulty:** hard
- **Relevant Notes:** [897, 771, 259, 390, 1031, 264]
- **Retrieved Notes:** [308, 99, 608, 516, 711]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 147.69 |
| Predicted Intent | question |
| Expected Intent | study |
| Intent Correct | False |

---

### HYBRID — Notes on scalability and reliability

- **Benchmark ID:** 126
- **Difficulty:** hard
- **Relevant Notes:** [1024, 259, 644, 1031, 520, 906]
- **Retrieved Notes:** [608, 354, 439, 530, 738]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 108.58 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |

---

### HYBRID — What are my creative ideas?

- **Benchmark ID:** 127
- **Difficulty:** easy
- **Relevant Notes:** [85, 86, 117, 120, 125, 128]
- **Retrieved Notes:** [382, 85, 416, 240, 496]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.167 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| Latency (ms) | 126.14 |
| Predicted Intent | idea |
| Expected Intent | idea |
| Intent Correct | True |

---

### HYBRID — Show my brainstorming notes

- **Benchmark ID:** 128
- **Difficulty:** easy
- **Relevant Notes:** [128, 514, 131, 260, 134, 262, 1035, 525]
- **Retrieved Notes:** [87, 85, 290, 416, 583]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 110.16 |
| Predicted Intent | general |
| Expected Intent | idea |
| Intent Correct | False |

---

### HYBRID — Advice and wisdom I've collected

- **Benchmark ID:** 129
- **Difficulty:** medium
- **Relevant Notes:** [260, 1028, 522, 1035, 525, 272]
- **Retrieved Notes:** [428, 728, 828, 928, 1028]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.167 |
| Hit | True |
| Reciprocal Rank | 0.200 |
| Latency (ms) | 106.99 |
| Predicted Intent | general |
| Expected Intent | general |
| Intent Correct | True |

---

### HYBRID — BM25

- **Benchmark ID:** 130
- **Difficulty:** easy
- **Relevant Notes:** [228, 252, 696, 796, 896, 996, 1096]
- **Retrieved Notes:** [252, 696, 796, 896, 996]

| Metric | Value |
|-------|------:|
| Precision@5 | 1.000 |
| Recall@5 | 0.714 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 98.94 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |

---

### HYBRID — HNSW index

- **Benchmark ID:** 131
- **Difficulty:** easy
- **Relevant Notes:** [215, 430, 681, 781, 881, 981, 1081]
- **Retrieved Notes:** [430, 215, 681, 781, 881]

| Metric | Value |
|-------|------:|
| Precision@5 | 1.000 |
| Recall@5 | 0.714 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 99.25 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |

---

### HYBRID — HNSW vector index configuration

- **Benchmark ID:** 132
- **Difficulty:** medium
- **Relevant Notes:** [215, 430, 681, 781, 881, 981, 1081]
- **Retrieved Notes:** [430, 66, 323, 742, 842]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.143 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 98.68 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |

---

### HYBRID — Reciprocal Rank Fusion

- **Benchmark ID:** 133
- **Difficulty:** medium
- **Relevant Notes:** [518, 718, 818, 918, 1018]
- **Retrieved Notes:** [518, 718, 818, 918, 1018]

| Metric | Value |
|-------|------:|
| Precision@5 | 1.000 |
| Recall@5 | 1.000 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 92.28 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |

---

### HYBRID — two sum problem

- **Benchmark ID:** 134
- **Difficulty:** easy
- **Relevant Notes:** [278, 677, 777, 877, 977, 1077]
- **Retrieved Notes:** [278, 677, 777, 877, 977]

| Metric | Value |
|-------|------:|
| Precision@5 | 1.000 |
| Recall@5 | 0.833 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 105.34 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |

---

### HYBRID — LRU cache implementation

- **Benchmark ID:** 135
- **Difficulty:** medium
- **Relevant Notes:** [318, 336, 520, 530, 579, 736, 738, 836, 838, 936]
- **Retrieved Notes:** [520, 318, 579, 736, 836]

| Metric | Value |
|-------|------:|
| Precision@5 | 1.000 |
| Recall@5 | 0.500 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 126.22 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |

---

### HYBRID — CAP theorem

- **Benchmark ID:** 136
- **Difficulty:** easy
- **Relevant Notes:** [580, 608]
- **Retrieved Notes:** [580, 608, 233, 607, 753]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 1.000 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 115.15 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |

---

### HYBRID — PageRank or graph algorithms notes

- **Benchmark ID:** 137
- **Difficulty:** medium
- **Relevant Notes:** [60, 158, 224, 316, 342, 347, 545, 546, 619, 667]
- **Retrieved Notes:** [619, 333, 60, 215, 681]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.400 |
| Recall@5 | 0.200 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 144.80 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |

---

### HYBRID — What have I been working on this month?

- **Benchmark ID:** 138
- **Difficulty:** hard
- **Relevant Notes:** [77, 149, 164, 182, 216, 286]
- **Retrieved Notes:** [453, 77, 82, 647, 375]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.167 |
| Hit | True |
| Reciprocal Rank | 0.500 |
| Latency (ms) | 100.00 |
| Predicted Intent | question |
| Expected Intent | general |
| Intent Correct | False |

---

### HYBRID — Recent notes and activities

- **Benchmark ID:** 139
- **Difficulty:** hard
- **Relevant Notes:** [77, 149, 164, 182, 216, 286]
- **Retrieved Notes:** [87, 444, 565, 290, 203]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 110.28 |
| Predicted Intent | general |
| Expected Intent | general |
| Intent Correct | True |

---

### HYBRID — Redis vs Kafka — when to use each

- **Benchmark ID:** 140
- **Difficulty:** hard
- **Relevant Notes:** [1024, 771, 1027, 773, 520, 1034]
- **Retrieved Notes:** [643, 673, 773, 873, 973]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.167 |
| Hit | True |
| Reciprocal Rank | 0.333 |
| Latency (ms) | 108.69 |
| Predicted Intent | question |
| Expected Intent | study |
| Intent Correct | False |

---

### HYBRID — Python vs Go programming notes

- **Benchmark ID:** 141
- **Difficulty:** hard
- **Relevant Notes:** [512, 320, 898, 266, 138, 586]
- **Retrieved Notes:** [572, 327, 283, 662, 762]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 106.46 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |

---

### HYBRID — SQL vs NoSQL database comparison

- **Benchmark ID:** 142
- **Difficulty:** hard
- **Relevant Notes:** [772, 775, 904, 1031, 1032, 139]
- **Retrieved Notes:** [300, 754, 854, 954, 1054]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 102.38 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |

---

### HYBRID — Comparing RAG retrieval strategies: dense, sparse, and reranking

- **Benchmark ID:** 143
- **Difficulty:** hard
- **Relevant Notes:** [386, 1030, 648, 649, 776, 267]
- **Retrieved Notes:** [386, 310, 595, 492, 186]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.167 |
| Hit | True |
| Reciprocal Rank | 1.000 |
| Latency (ms) | 118.01 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |
| Predicted Category | Study - API Performance |
| Expected Category | Study - AI |
| Category Correct | True |

---

### HYBRID — REST vs GraphQL API design trade-offs

- **Benchmark ID:** 144
- **Difficulty:** hard
- **Relevant Notes:** [68, 93, 96, 132, 136, 142]
- **Retrieved Notes:** [484, 644, 93, 450, 671]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.167 |
| Hit | True |
| Reciprocal Rank | 0.333 |
| Latency (ms) | 107.05 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |

---

### HYBRID — Show all my communication notes

- **Benchmark ID:** 145
- **Difficulty:** easy
- **Relevant Notes:** [54, 55, 56, 57, 106, 117]
- **Retrieved Notes:** [141, 583, 699, 799, 899]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 98.77 |
| Predicted Intent | general |
| Expected Intent | communication |
| Intent Correct | False |

---

### HYBRID — All my reminder notes

- **Benchmark ID:** 146
- **Difficulty:** easy
- **Relevant Notes:** [55, 152, 212, 312, 542, 557]
- **Retrieved Notes:** [290, 583, 699, 799, 899]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 117.27 |
| Predicted Intent | reminder |
| Expected Intent | reminder |
| Intent Correct | True |
| Predicted Category | Reminders |
| Expected Category | Reminders |
| Category Correct | True |

---

### HYBRID — My study notes on AI and machine learning

- **Benchmark ID:** 147
- **Difficulty:** easy
- **Relevant Notes:** [1026, 774, 1030, 510, 523, 268, 267, 782]
- **Retrieved Notes:** [529, 230, 87, 619, 85]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 102.81 |
| Predicted Intent | study |
| Expected Intent | study |
| Intent Correct | True |

---

### HYBRID — Notes categorized under system design

- **Benchmark ID:** 148
- **Difficulty:** easy
- **Relevant Notes:** [70, 145, 255, 267, 305, 309]
- **Retrieved Notes:** [106, 392, 87, 602, 309]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.200 |
| Recall@5 | 0.167 |
| Hit | True |
| Reciprocal Rank | 0.200 |
| Latency (ms) | 97.94 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |

---

### HYBRID — Programming notes I've taken recently

- **Benchmark ID:** 149
- **Difficulty:** medium
- **Relevant Notes:** [512, 1025, 898, 132, 266, 523]
- **Retrieved Notes:** [87, 583, 699, 799, 899]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 97.79 |
| Predicted Intent | general |
| Expected Intent | study |
| Intent Correct | False |

---

### HYBRID — My financial notes

- **Benchmark ID:** 150
- **Difficulty:** medium
- **Relevant Notes:** [646, 202, 331, 591, 273, 82]
- **Retrieved Notes:** [290, 87, 637, 733, 833]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 95.74 |
| Predicted Intent | general |
| Expected Intent | todo |
| Intent Correct | False |

---

### HYBRID — Projects and ideas I'm excited about

- **Benchmark ID:** 151
- **Difficulty:** hard
- **Relevant Notes:** [514, 260, 1028, 262, 1032, 522]
- **Retrieved Notes:** [85, 528, 442, 755, 855]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 111.48 |
| Predicted Intent | idea |
| Expected Intent | idea |
| Intent Correct | True |

---

### HYBRID — Personal notes and self-improvement

- **Benchmark ID:** 152
- **Difficulty:** hard
- **Relevant Notes:** [522, 1035, 785, 529, 277, 283]
- **Retrieved Notes:** [444, 290, 212, 87, 583]

| Metric | Value |
|-------|------:|
| Precision@5 | 0.000 |
| Recall@5 | 0.000 |
| Hit | False |
| Reciprocal Rank | 0.000 |
| Latency (ms) | 124.36 |
| Predicted Intent | general |
| Expected Intent | general |
| Intent Correct | True |

---


---

_Generated automatically by the KnowledgeVault Evaluation Framework._