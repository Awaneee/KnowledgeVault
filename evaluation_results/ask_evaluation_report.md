# KnowledgeVault — Ask Endpoint Evaluation Report

**Run ID:** `b0bc225d-6782-463b-b9f0-f509a2ae6f3f`
**Created:** 2026-07-26T13:45:17.571145+00:00
**Total Queries:** 47
**Estimated Total Cost:** $0.002219 USD

## Overall Averages

| Metric | Score |
|---|---|
| Correctness | 0.000 |
| Groundedness | 0.000 |
| Faithfulness | 0.000 |
| Hallucination (1=none) | 0.000 |
| Completeness | 0.000 |
| **Overall (Weighted)** | **0.000** |

### Latency

| Metric | ms |
|---|---|
| Avg Retrieval | 306.5 |
| Avg LLM | 64432.2 |
| Avg End-to-End | 64738.7 |

## Per-Category Breakdown

| Category | N | Correctness | Groundedness | Faithfulness | Hallucination | Completeness | Overall | Avg ms |
|---|---|---|---|---|---|---|---|---|

## Failure Root Cause Distribution

| Root Cause | Count |
|---|---|
| evaluator_failure | 47 |

## Hardest Queries (Lowest Overall Score)


## Easiest Queries (Highest Overall Score)


## Per-Query Results

### [aq_001] What is the difference between BFS and DFS and when do you use each?

- **Category:** factual_lookup | **Difficulty:** medium
- **Status:** degraded | **Retrieval-Only:** True
- **Expected Notes:** [158, 224, 316, 332, 342, 347, 545, 546, 667, 668, 693, 737, 767, 768, 793, 837, 867, 868, 893, 937, 967, 968, 993, 1037, 1067, 1068, 1093]
- **Retrieved Notes:** [347, 668, 768, 868, 968, 1068, 316, 342]
- **Recall@Expected:** 0.296 | **Context Utilisation:** 0.000
- **Latency:** retrieval=250ms, llm=64687ms, total=64937ms
- **Cost:** $0.00003817 USD

**Root cause:** `evaluator_failure`

**Error:**
```
Judge Gemini failed after 5 retries due to rate limiting (429)
```

**Answer:** AI-generated responses are temporarily unavailable. Here are the most relevant notes we found for your question.

---

### [aq_002] How does the HNSW index work in pgvector?

- **Category:** factual_lookup | **Difficulty:** hard
- **Status:** degraded | **Retrieval-Only:** True
- **Expected Notes:** [58, 66, 104, 113, 139, 168, 183, 187, 188, 215, 217, 228, 249, 252, 280, 298, 300, 323, 333, 337, 367, 372, 376, 396, 404, 417, 430, 446, 500, 523, 531, 567, 590, 623, 628, 648, 672, 681, 683, 686, 696, 704, 708, 726, 730, 731, 732, 742, 754, 772, 781, 783, 786, 796, 804, 808, 826, 830, 831, 832, 842, 854, 872, 881, 883, 886, 896, 904, 908, 926, 930, 931, 932, 942, 954, 972, 981, 983, 986, 996, 1004, 1008, 1026, 1030, 1031, 1032, 1042, 1054, 1072, 1081, 1083, 1086, 1096, 1104, 1108]
- **Retrieved Notes:** [66, 323, 742, 842, 942, 1042, 215, 681]
- **Recall@Expected:** 0.084 | **Context Utilisation:** 0.000
- **Latency:** retrieval=3484ms, llm=64750ms, total=68234ms
- **Cost:** $0.00003600 USD

**Root cause:** `evaluator_failure`

**Error:**
```
Judge Gemini failed after 5 retries due to rate limiting (429)
```

**Answer:** AI-generated responses are temporarily unavailable. Here are the most relevant notes we found for your question.

---

### [aq_003] What is Reciprocal Rank Fusion and how is it used in hybrid search?

- **Category:** factual_lookup | **Difficulty:** hard
- **Status:** degraded | **Retrieval-Only:** True
- **Expected Notes:** [183, 213, 228, 252, 375, 381, 486, 518, 523, 555, 696, 702, 717, 718, 729, 735, 796, 802, 817, 818, 829, 835, 896, 902, 917, 918, 929, 935, 996, 1002, 1017, 1018, 1029, 1035, 1096, 1102]
- **Retrieved Notes:** [518, 718, 818, 918, 1018, 252, 696, 796]
- **Recall@Expected:** 0.222 | **Context Utilisation:** 0.000
- **Latency:** retrieval=62ms, llm=64594ms, total=64656ms
- **Cost:** $0.00003255 USD

**Root cause:** `evaluator_failure`

**Error:**
```
Judge Gemini failed after 5 retries due to rate limiting (429)
```

**Answer:** AI-generated responses are temporarily unavailable. Here are the most relevant notes we found for your question.

---

### [aq_004] What is the CAP theorem?

- **Category:** factual_lookup | **Difficulty:** medium
- **Status:** degraded | **Retrieval-Only:** True
- **Expected Notes:** [229, 259, 292, 417, 580, 608, 621, 631, 690, 695, 731, 790, 795, 831, 890, 895, 931, 990, 995, 1031, 1090, 1095]
- **Retrieved Notes:** [580, 608, 607, 753, 853, 953, 1053, 233]
- **Recall@Expected:** 0.091 | **Context Utilisation:** 0.000
- **Latency:** retrieval=141ms, llm=63656ms, total=63797ms
- **Cost:** $0.00004485 USD

**Root cause:** `evaluator_failure`

**Error:**
```
Judge Gemini failed after 5 retries due to rate limiting (429)
```

**Answer:** AI-generated responses are temporarily unavailable. Here are the most relevant notes we found for your question.

---

### [aq_005] What is HyDE in the context of RAG systems?

- **Category:** factual_lookup | **Difficulty:** hard
- **Status:** degraded | **Retrieval-Only:** True
- **Expected Notes:** [531, 683, 783, 883, 983, 1083]
- **Retrieved Notes:** [531, 683, 783, 883, 983, 1083, 436, 197]
- **Recall@Expected:** 1.000 | **Context Utilisation:** 0.000
- **Latency:** retrieval=94ms, llm=63984ms, total=64078ms
- **Cost:** $0.00003915 USD

**Root cause:** `evaluator_failure`

**Error:**
```
Judge Gemini failed after 5 retries due to rate limiting (429)
```

**Answer:** AI-generated responses are temporarily unavailable. Here are the most relevant notes we found for your question.

---

### [aq_006] What are the ACID properties in databases?

- **Category:** factual_lookup | **Difficulty:** easy
- **Status:** degraded | **Retrieval-Only:** True
- **Expected Notes:** [144, 156, 229, 580, 608, 621, 631, 690, 790, 890, 990, 1090]
- **Retrieved Notes:** [229, 690, 790, 890, 990, 1090, 321, 707]
- **Recall@Expected:** 0.500 | **Context Utilisation:** 0.000
- **Latency:** retrieval=125ms, llm=64391ms, total=64516ms
- **Cost:** $0.00003315 USD

**Root cause:** `evaluator_failure`

**Error:**
```
Judge Gemini failed after 5 retries due to rate limiting (429)
```

**Answer:** AI-generated responses are temporarily unavailable. Here are the most relevant notes we found for your question.

---

### [aq_007] What is the difference between a cross-encoder and a bi-encoder?

- **Category:** factual_lookup | **Difficulty:** hard
- **Status:** degraded | **Retrieval-Only:** True
- **Expected Notes:** [67, 119, 123, 176, 386, 648, 676, 776, 876, 976, 1076]
- **Retrieved Notes:** [123, 676, 776, 876, 976, 1076, 67, 648]
- **Recall@Expected:** 0.727 | **Context Utilisation:** 0.000
- **Latency:** retrieval=78ms, llm=64469ms, total=64547ms
- **Cost:** $0.00003608 USD

**Root cause:** `evaluator_failure`

**Error:**
```
Judge Gemini failed after 5 retries due to rate limiting (429)
```

**Answer:** AI-generated responses are temporarily unavailable. Here are the most relevant notes we found for your question.

---

### [aq_008] How does consistent hashing work?

- **Category:** factual_lookup | **Difficulty:** medium
- **Status:** degraded | **Retrieval-Only:** True
- **Expected Notes:** [104, 114, 135, 136, 145, 148, 152, 155, 166, 177, 204, 210, 213, 219, 220, 242, 243, 251, 269, 272, 278, 280, 284, 292, 300, 319, 333, 334, 350, 352, 353, 356, 387, 390, 419, 424, 431, 442, 451, 461, 470, 473, 475, 484, 489, 504, 516, 517, 519, 559, 561, 565, 587, 603, 615, 633, 641, 677, 685, 695, 711, 724, 729, 739, 754, 755, 777, 785, 795, 811, 824, 829, 839, 854, 855, 877, 885, 895, 911, 924, 929, 939, 954, 955, 977, 985, 995, 1011, 1024, 1029, 1039, 1054, 1055, 1077, 1085, 1095]
- **Retrieved Notes:** [334, 300, 754, 854, 954, 1054, 104, 587]
- **Recall@Expected:** 0.083 | **Context Utilisation:** 0.000
- **Latency:** retrieval=94ms, llm=65109ms, total=65203ms
- **Cost:** $0.00004073 USD

**Root cause:** `evaluator_failure`

**Error:**
```
Judge Gemini failed after 5 retries due to rate limiting (429)
```

**Answer:** AI-generated responses are temporarily unavailable. Here are the most relevant notes we found for your question.

---

### [aq_009] What is the difference between RAG retrieval failure modes?

- **Category:** factual_lookup | **Difficulty:** hard
- **Status:** degraded | **Retrieval-Only:** True
- **Expected Notes:** [119, 148, 197, 222, 239, 268, 365, 369, 386, 432, 436, 446, 449, 454, 470, 478, 485, 487, 488, 564, 569, 600, 615, 623, 625, 655, 682, 692, 694, 730, 782, 792, 794, 830, 882, 892, 894, 930, 982, 992, 994, 1030, 1082, 1092, 1094]
- **Retrieved Notes:** [222, 310, 386, 197, 485, 436, 600, 492]
- **Recall@Expected:** 0.133 | **Context Utilisation:** 0.000
- **Latency:** retrieval=94ms, llm=64250ms, total=64344ms
- **Cost:** $0.00007012 USD

**Root cause:** `evaluator_failure`

**Error:**
```
Judge Gemini failed after 5 retries due to rate limiting (429)
```

**Answer:** AI-generated responses are temporarily unavailable. Here are the most relevant notes we found for your question.

---

### [aq_010] What is token bucket rate limiting?

- **Category:** factual_lookup | **Difficulty:** medium
- **Status:** degraded | **Retrieval-Only:** True
- **Expected Notes:** [136, 150, 165, 189, 244, 251, 279, 346, 373, 697, 703, 725, 797, 803, 825, 897, 903, 925, 997, 1003, 1025, 1097, 1103]
- **Retrieved Notes:** [244, 346, 150, 373, 703, 803, 903, 1003]
- **Recall@Expected:** 0.348 | **Context Utilisation:** 0.000
- **Latency:** retrieval=109ms, llm=64594ms, total=64703ms
- **Cost:** $0.00004537 USD

**Root cause:** `evaluator_failure`

**Error:**
```
Judge Gemini failed after 5 retries due to rate limiting (429)
```

**Answer:** AI-generated responses are temporarily unavailable. Here are the most relevant notes we found for your question.

---

### [aq_011] What is the difference between FIFO, LRU, and Optimal page replacement?

- **Category:** factual_lookup | **Difficulty:** medium
- **Status:** degraded | **Retrieval-Only:** True
- **Expected Notes:** [117, 265, 318, 336, 520, 530, 562, 566, 579, 710, 736, 738, 810, 836, 838, 910, 936, 938, 1010, 1036, 1038]
- **Retrieved Notes:** [530, 738, 838, 938, 1038, 520, 547, 275]
- **Recall@Expected:** 0.286 | **Context Utilisation:** 0.000
- **Latency:** retrieval=94ms, llm=64921ms, total=65015ms
- **Cost:** $0.00004470 USD

**Root cause:** `evaluator_failure`

**Error:**
```
Judge Gemini failed after 5 retries due to rate limiting (429)
```

**Answer:** AI-generated responses are temporarily unavailable. Here are the most relevant notes we found for your question.

---

### [aq_012] What is the two-phase commit protocol?

- **Category:** factual_lookup | **Difficulty:** hard
- **Status:** degraded | **Retrieval-Only:** True
- **Expected Notes:** [308, 479]
- **Retrieved Notes:** [479, 384, 727, 827, 927, 1027, 328, 344]
- **Recall@Expected:** 0.500 | **Context Utilisation:** 0.000
- **Latency:** retrieval=63ms, llm=64156ms, total=64219ms
- **Cost:** $0.00004455 USD

**Root cause:** `evaluator_failure`

**Error:**
```
Judge Gemini failed after 5 retries due to rate limiting (429)
```

**Answer:** AI-generated responses are temporarily unavailable. Here are the most relevant notes we found for your question.

---

### [aq_013] How can I make Python code run faster?

- **Category:** factual_lookup | **Difficulty:** medium
- **Status:** degraded | **Retrieval-Only:** True
- **Expected Notes:** [98, 108, 142, 159, 160, 174, 177, 183, 195, 196, 206, 213, 221, 232, 235, 239, 249, 253, 255, 272, 283, 284, 295, 304, 310, 318, 327, 333, 335, 336, 349, 358, 359, 366, 367, 374, 375, 381, 388, 396, 402, 404, 406, 414, 420, 445, 447, 451, 464, 474, 483, 530, 547, 549, 552, 563, 572, 579, 587, 588, 595, 598, 610, 617, 618, 628, 633, 640, 645, 651, 655, 656, 657, 662, 708, 716, 717, 729, 732, 734, 735, 736, 738, 745, 756, 757, 762, 808, 816, 817, 829, 832, 834, 835, 836, 838, 845, 856, 857, 862, 908, 916, 917, 929, 932, 934, 935, 936, 938, 945, 956, 957, 962, 1008, 1016, 1017, 1029, 1032, 1034, 1035, 1036, 1038, 1045, 1056, 1057, 1062, 1108]
- **Retrieved Notes:** [464, 745, 845, 945, 1045, 108, 195, 483]
- **Recall@Expected:** 0.063 | **Context Utilisation:** 0.000
- **Latency:** retrieval=187ms, llm=65079ms, total=65266ms
- **Cost:** $0.00004050 USD

**Root cause:** `evaluator_failure`

**Error:**
```
Judge Gemini failed after 5 retries due to rate limiting (429)
```

**Answer:** AI-generated responses are temporarily unavailable. Here are the most relevant notes we found for your question.

---

### [aq_014] When should I use Redis over a traditional database?

- **Category:** factual_lookup | **Difficulty:** medium
- **Status:** degraded | **Retrieval-Only:** True
- **Expected Notes:** [61, 73, 92, 103, 124, 146, 157, 174, 237, 246, 269, 275, 284, 295, 297, 303, 305, 318, 346, 392, 421, 431, 433, 450, 466, 467, 484, 503, 520, 523, 534, 536, 544, 579, 602, 643, 644, 671, 673, 684, 705, 706, 724, 736, 746, 771, 773, 784, 805, 806, 824, 836, 846, 871, 873, 884, 905, 906, 924, 936, 946, 971, 973, 984, 1005, 1006, 1024, 1036, 1046, 1071, 1073, 1084, 1105, 1106]
- **Retrieved Notes:** [73, 61, 269, 724, 824, 924, 1024, 421]
- **Recall@Expected:** 0.108 | **Context Utilisation:** 0.000
- **Latency:** retrieval=47ms, llm=64375ms, total=64422ms
- **Cost:** $0.00003780 USD

**Root cause:** `evaluator_failure`

**Error:**
```
Judge Gemini failed after 5 retries due to rate limiting (429)
```

**Answer:** AI-generated responses are temporarily unavailable. Here are the most relevant notes we found for your question.

---

### [aq_015] What are good strategies for preparing for technical interviews?

- **Category:** factual_lookup | **Difficulty:** easy
- **Status:** degraded | **Retrieval-Only:** True
- **Expected Notes:** [60, 70, 99, 117, 126, 145, 152, 154, 187, 192, 199, 224, 230, 236, 263, 267, 271, 288, 294, 305, 309, 316, 344, 346, 352, 360, 387, 392, 399, 413, 453, 468, 480, 499, 507, 521, 540, 546, 580, 582, 602, 609, 611, 615, 619, 654, 660, 760, 860, 960, 1060]
- **Retrieved Notes:** [352, 236, 507, 100, 609, 360, 199, 357]
- **Recall@Expected:** 0.118 | **Context Utilisation:** 0.000
- **Latency:** retrieval=109ms, llm=64516ms, total=64625ms
- **Cost:** $0.00006585 USD

**Root cause:** `evaluator_failure`

**Error:**
```
Judge Gemini failed after 5 retries due to rate limiting (429)
```

**Answer:** AI-generated responses are temporarily unavailable. Here are the most relevant notes we found for your question.

---

### [aq_016] What makes a good software engineer?

- **Category:** factual_lookup | **Difficulty:** hard
- **Status:** degraded | **Retrieval-Only:** True
- **Expected Notes:** [73, 114, 155, 166, 199, 213, 236, 272, 277, 299, 319, 337, 371, 390, 416, 419, 428, 461, 480, 586, 603, 665, 685, 728, 729, 765, 785, 828, 829, 865, 885, 928, 929, 965, 985, 1028, 1029, 1065, 1085]
- **Retrieved Notes:** [586, 603, 272, 416, 390, 277, 166, 685]
- **Recall@Expected:** 0.205 | **Context Utilisation:** 0.000
- **Latency:** retrieval=78ms, llm=64656ms, total=64734ms
- **Cost:** $0.00006240 USD

**Root cause:** `evaluator_failure`

**Error:**
```
Judge Gemini failed after 5 retries due to rate limiting (429)
```

**Answer:** AI-generated responses are temporarily unavailable. Here are the most relevant notes we found for your question.

---

### [aq_017] What have I decided about KnowledgeVault's retrieval system and why?

- **Category:** multi_hop | **Difficulty:** hard
- **Status:** degraded | **Retrieval-Only:** True
- **Expected Notes:** [57, 65, 86, 88, 89, 90, 91, 94, 95, 96, 97, 107, 119, 125, 183, 184, 185, 186, 201, 213, 222, 228, 247, 251, 252, 262, 289, 298, 310, 311, 329, 337, 375, 381, 386, 398, 402, 413, 426, 428, 430, 444, 446, 452, 453, 486, 487, 492, 518, 523, 531, 533, 555, 558, 603, 607, 623, 625, 628, 638, 641, 644, 666, 683, 696, 702, 717, 718, 721, 726, 728, 729, 730, 732, 735, 753, 766, 783, 796, 802, 817, 818, 821, 826, 828, 829, 830, 832, 835, 853, 866, 883, 896, 902, 917, 918, 921, 926, 928, 929, 930, 932, 935, 953, 966, 983, 996, 1002, 1017, 1018, 1021, 1026, 1028, 1029, 1030, 1032, 1035, 1053, 1066, 1083, 1096, 1102]
- **Retrieved Notes:** [88, 555, 89, 90, 96, 523, 262, 125]
- **Recall@Expected:** 0.066 | **Context Utilisation:** 0.000
- **Latency:** retrieval=94ms, llm=64812ms, total=64906ms
- **Cost:** $0.00005595 USD

**Root cause:** `evaluator_failure`

**Error:**
```
Judge Gemini failed after 5 retries due to rate limiting (429)
```

**Answer:** AI-generated responses are temporarily unavailable. Here are the most relevant notes we found for your question.

---

### [aq_018] How does the evaluation framework work in KnowledgeVault?

- **Category:** multi_hop | **Difficulty:** hard
- **Status:** degraded | **Retrieval-Only:** True
- **Expected Notes:** [90, 119, 136, 143, 183, 184, 210, 213, 251, 255, 310, 373, 375, 381, 398, 402, 453, 464, 485, 487, 509, 523, 555, 588, 595, 616, 649, 703, 717, 729, 735, 745, 803, 817, 829, 835, 845, 903, 917, 929, 935, 945, 1003, 1017, 1029, 1035, 1045, 1103]
- **Retrieved Notes:** [90, 555, 89, 251, 125, 616, 96, 88]
- **Recall@Expected:** 0.083 | **Context Utilisation:** 0.000
- **Latency:** retrieval=94ms, llm=64641ms, total=64735ms
- **Cost:** $0.00005498 USD

**Root cause:** `evaluator_failure`

**Error:**
```
Judge Gemini failed after 5 retries due to rate limiting (429)
```

**Answer:** AI-generated responses are temporarily unavailable. Here are the most relevant notes we found for your question.

---

### [aq_019] What are the known bugs and issues I've encountered building KnowledgeVault?

- **Category:** multi_hop | **Difficulty:** hard
- **Status:** degraded | **Retrieval-Only:** True
- **Expected Notes:** [57, 88, 89, 90, 91, 94, 95, 96, 97, 107, 125, 129, 136, 147, 163, 168, 170, 173, 185, 188, 244, 246, 247, 249, 251, 255, 258, 262, 270, 279, 310, 328, 335, 337, 340, 346, 357, 362, 413, 421, 426, 428, 430, 432, 444, 447, 452, 453, 461, 473, 488, 494, 502, 519, 522, 523, 534, 551, 555, 558, 574, 589, 591, 603, 604, 607, 628, 632, 637, 638, 652, 659, 678, 684, 692, 709, 728, 732, 733, 739, 746, 749, 752, 753, 759, 778, 784, 792, 809, 828, 832, 833, 839, 846, 849, 852, 853, 859, 878, 884, 892, 909, 928, 932, 933, 939, 946, 949, 952, 953, 959, 978, 984, 992, 1009, 1028, 1032, 1033, 1039, 1046, 1049, 1052, 1053, 1059, 1078, 1084, 1092]
- **Retrieved Notes:** [638, 90, 251, 428, 728, 828, 928, 1028]
- **Recall@Expected:** 0.063 | **Context Utilisation:** 0.000
- **Latency:** retrieval=94ms, llm=64531ms, total=64625ms
- **Cost:** $0.00004155 USD

**Root cause:** `evaluator_failure`

**Error:**
```
Judge Gemini failed after 5 retries due to rate limiting (429)
```

**Answer:** AI-generated responses are temporarily unavailable. Here are the most relevant notes we found for your question.

---

### [aq_020] What is the relationship between embedding quality and RAG answer quality?

- **Category:** multi_hop | **Difficulty:** hard
- **Status:** degraded | **Retrieval-Only:** True
- **Expected Notes:** [64, 65, 86, 88, 112, 119, 148, 158, 168, 184, 186, 196, 197, 199, 205, 213, 215, 222, 228, 239, 252, 268, 273, 289, 298, 300, 310, 313, 323, 329, 332, 365, 369, 375, 376, 378, 381, 386, 398, 402, 404, 430, 432, 436, 446, 454, 470, 478, 485, 486, 487, 488, 492, 502, 518, 523, 531, 533, 540, 555, 558, 564, 569, 590, 600, 604, 615, 616, 623, 625, 637, 640, 644, 655, 666, 681, 682, 683, 692, 693, 694, 696, 702, 708, 717, 718, 721, 726, 729, 730, 733, 735, 737, 742, 749, 750, 754, 766, 781, 782, 783, 792, 793, 794, 796, 802, 808, 817, 818, 821, 826, 829, 830, 833, 835, 837, 842, 849, 850, 854, 866, 881, 882, 883, 892, 893, 894, 896, 902, 908, 917, 918, 921, 926, 929, 930, 933, 935, 937, 942, 949, 950, 954, 966, 981, 982, 983, 992, 993, 994, 996, 1002, 1008, 1017, 1018, 1021, 1026, 1029, 1030, 1033, 1035, 1037, 1042, 1049, 1050, 1054, 1066, 1081, 1082, 1083, 1092, 1093, 1094, 1096, 1102, 1108]
- **Retrieved Notes:** [485, 531, 683, 783, 883, 983, 1083, 310]
- **Recall@Expected:** 0.045 | **Context Utilisation:** 0.000
- **Latency:** retrieval=78ms, llm=64344ms, total=64422ms
- **Cost:** $0.00004087 USD

**Root cause:** `evaluator_failure`

**Error:**
```
Judge Gemini failed after 5 retries due to rate limiting (429)
```

**Answer:** AI-generated responses are temporarily unavailable. Here are the most relevant notes we found for your question.

---

### [aq_021] How do I balance study, projects, and personal life as a student?

- **Category:** multi_hop | **Difficulty:** medium
- **Status:** degraded | **Retrieval-Only:** True
- **Expected Notes:** [58, 62, 66, 79, 85, 109, 156, 157, 169, 179, 201, 210, 212, 224, 240, 248, 301, 303, 343, 348, 355, 380, 410, 429, 434, 438, 448, 453, 540, 575, 601, 612, 617, 623, 634, 664, 680, 688, 698, 764, 780, 788, 798, 864, 880, 888, 898, 964, 980, 988, 998, 1064, 1080, 1088, 1098]
- **Retrieved Notes:** [380, 680, 780, 880, 980, 1080, 272, 603]
- **Recall@Expected:** 0.109 | **Context Utilisation:** 0.000
- **Latency:** retrieval=110ms, llm=64375ms, total=64485ms
- **Cost:** $0.00003908 USD

**Root cause:** `evaluator_failure`

**Error:**
```
Judge Gemini failed after 5 retries due to rate limiting (429)
```

**Answer:** AI-generated responses are temporarily unavailable. Here are the most relevant notes we found for your question.

---

### [aq_022] What tasks and reminders do I have pending?

- **Category:** temporal | **Difficulty:** medium
- **Status:** degraded | **Retrieval-Only:** True
- **Expected Notes:** [55, 233, 368, 498, 506, 542, 607, 753]
- **Retrieved Notes:** [392, 680, 79, 372, 620, 498, 612, 191]
- **Recall@Expected:** 0.125 | **Context Utilisation:** 0.000
- **Latency:** retrieval=78ms, llm=64688ms, total=64766ms
- **Cost:** $0.00006247 USD

**Root cause:** `evaluator_failure`

**Error:**
```
Judge Gemini failed after 5 retries due to rate limiting (429)
```

**Answer:** AI-generated responses are temporarily unavailable. Here are the most relevant notes we found for your question.

---

### [aq_023] What appointments and scheduled events do I have coming up?

- **Category:** temporal | **Difficulty:** easy
- **Status:** degraded | **Retrieval-Only:** True
- **Expected Notes:** [78, 79, 109, 128, 179, 201, 224, 226, 231, 240, 348, 434, 438, 448, 559, 575, 601, 612, 617, 634, 664, 698, 764, 798, 864, 898, 964, 998, 1064, 1098]
- **Retrieved Notes:** [559, 79, 620, 601, 609, 102, 175, 352]
- **Recall@Expected:** 0.100 | **Context Utilisation:** 0.000
- **Latency:** retrieval=109ms, llm=65031ms, total=65140ms
- **Cost:** $0.00005880 USD

**Root cause:** `evaluator_failure`

**Error:**
```
Judge Gemini failed after 5 retries due to rate limiting (429)
```

**Answer:** AI-generated responses are temporarily unavailable. Here are the most relevant notes we found for your question.

---

### [aq_024] What are my financial obligations this month?

- **Category:** temporal | **Difficulty:** medium
- **Status:** degraded | **Retrieval-Only:** True
- **Expected Notes:** [77, 140, 160, 164, 178, 312, 341, 368, 431, 490, 635]
- **Retrieved Notes:** [82, 77, 341, 635, 216, 79, 601, 162]
- **Recall@Expected:** 0.273 | **Context Utilisation:** 0.000
- **Latency:** retrieval=62ms, llm=64594ms, total=64656ms
- **Cost:** $0.00005310 USD

**Root cause:** `evaluator_failure`

**Error:**
```
Judge Gemini failed after 5 retries due to rate limiting (429)
```

**Answer:** AI-generated responses are temporarily unavailable. Here are the most relevant notes we found for your question.

---

### [aq_025] What trips am I planning in the near future?

- **Category:** temporal | **Difficulty:** medium
- **Status:** degraded | **Retrieval-Only:** True
- **Expected Notes:** [81, 128, 324, 407, 463, 535, 538, 596, 627]
- **Retrieved Notes:** [627, 81, 343, 538, 77, 407, 216, 272]
- **Recall@Expected:** 0.444 | **Context Utilisation:** 0.000
- **Latency:** retrieval=94ms, llm=64734ms, total=64828ms
- **Cost:** $0.00006053 USD

**Root cause:** `evaluator_failure`

**Error:**
```
Judge Gemini failed after 5 retries due to rate limiting (429)
```

**Answer:** AI-generated responses are temporarily unavailable. Here are the most relevant notes we found for your question.

---

### [aq_026] How does Kafka compare to Redis for building a job queue?

- **Category:** comparison | **Difficulty:** hard
- **Status:** degraded | **Retrieval-Only:** True
- **Expected Notes:** [56, 61, 71, 73, 92, 103, 141, 157, 174, 246, 269, 297, 303, 305, 346, 371, 392, 421, 423, 433, 450, 466, 523, 534, 536, 544, 602, 643, 671, 673, 684, 705, 724, 746, 771, 773, 784, 805, 824, 846, 871, 873, 884, 905, 924, 946, 971, 973, 984, 1005, 1024, 1046, 1071, 1073, 1084, 1105]
- **Retrieved Notes:** [643, 673, 773, 873, 973, 1073, 450, 671]
- **Recall@Expected:** 0.143 | **Context Utilisation:** 0.000
- **Latency:** retrieval=172ms, llm=65094ms, total=65266ms
- **Cost:** $0.00003345 USD

**Root cause:** `evaluator_failure`

**Error:**
```
Judge Gemini failed after 5 retries due to rate limiting (429)
```

**Answer:** AI-generated responses are temporarily unavailable. Here are the most relevant notes we found for your question.

---

### [aq_027] What are the trade-offs between Python and Go for backend development?

- **Category:** comparison | **Difficulty:** hard
- **Status:** degraded | **Retrieval-Only:** True
- **Expected Notes:** [59, 60, 108, 113, 114, 138, 152, 162, 170, 174, 177, 182, 190, 191, 200, 202, 204, 206, 208, 232, 239, 244, 247, 258, 261, 262, 265, 266, 272, 283, 284, 295, 297, 300, 304, 318, 320, 326, 327, 328, 332, 334, 335, 336, 339, 341, 346, 348, 354, 358, 359, 364, 366, 370, 372, 374, 375, 376, 378, 388, 391, 396, 404, 409, 413, 414, 420, 427, 428, 437, 442, 443, 445, 447, 450, 451, 458, 460, 464, 471, 475, 481, 482, 483, 486, 488, 496, 499, 503, 507, 512, 516, 530, 533, 536, 538, 540, 541, 542, 545, 549, 552, 558, 561, 563, 566, 572, 573, 577, 579, 581, 586, 587, 588, 589, 595, 597, 598, 599, 603, 605, 607, 610, 618, 619, 623, 624, 629, 631, 632, 633, 634, 640, 645, 649, 651, 657, 659, 660, 661, 662, 663, 664, 671, 689, 693, 698, 701, 702, 708, 709, 710, 711, 716, 721, 728, 734, 735, 736, 738, 743, 745, 751, 753, 754, 755, 757, 759, 760, 761, 762, 763, 764, 771, 789, 793, 798, 801, 802, 808, 809, 810, 811, 816, 821, 828, 834, 835, 836, 838, 843, 845, 851, 853, 854, 855, 857, 859, 860, 861, 862, 863, 864, 871, 889, 893, 898, 901, 902, 908, 909, 910, 911, 916, 921, 928, 934, 935, 936, 938, 943, 945, 951, 953, 954, 955, 957, 959, 960, 961, 962, 963, 964, 971, 989, 993, 998, 1001, 1002, 1008, 1009, 1010, 1011, 1016, 1021, 1028, 1034, 1035, 1036, 1038, 1043, 1045, 1051, 1053, 1054, 1055, 1057, 1059, 1060, 1061, 1062, 1063, 1064, 1071, 1089, 1093, 1098, 1101, 1102, 1108]
- **Retrieved Notes:** [471, 663, 763, 863, 963, 1063, 272, 177]
- **Recall@Expected:** 0.030 | **Context Utilisation:** 0.000
- **Latency:** retrieval=172ms, llm=65031ms, total=65203ms
- **Cost:** $0.00003938 USD

**Root cause:** `evaluator_failure`

**Error:**
```
Judge Gemini failed after 5 retries due to rate limiting (429)
```

**Answer:** AI-generated responses are temporarily unavailable. Here are the most relevant notes we found for your question.

---

### [aq_028] Compare LRU and LFU cache eviction policies.

- **Category:** comparison | **Difficulty:** medium
- **Status:** degraded | **Retrieval-Only:** True
- **Expected Notes:** [57, 62, 65, 67, 89, 95, 99, 102, 103, 106, 124, 131, 146, 156, 166, 168, 207, 213, 215, 219, 224, 228, 237, 247, 261, 262, 269, 275, 282, 284, 285, 295, 303, 318, 319, 328, 333, 336, 354, 368, 372, 374, 386, 404, 405, 429, 431, 432, 442, 463, 467, 484, 487, 498, 503, 506, 510, 520, 524, 528, 529, 530, 533, 534, 554, 559, 561, 565, 579, 592, 595, 602, 620, 627, 628, 635, 644, 669, 670, 681, 685, 692, 706, 708, 721, 724, 729, 732, 736, 738, 755, 769, 770, 781, 785, 792, 806, 808, 821, 824, 829, 832, 836, 838, 855, 869, 870, 881, 885, 892, 906, 908, 921, 924, 929, 932, 936, 938, 955, 969, 970, 981, 985, 992, 1006, 1008, 1021, 1024, 1029, 1032, 1036, 1038, 1055, 1069, 1070, 1081, 1085, 1092, 1106, 1108]
- **Retrieved Notes:** [520, 318, 103, 579, 736, 836, 936, 1036]
- **Recall@Expected:** 0.057 | **Context Utilisation:** 0.000
- **Latency:** retrieval=156ms, llm=64641ms, total=64797ms
- **Cost:** $0.00003817 USD

**Root cause:** `evaluator_failure`

**Error:**
```
Judge Gemini failed after 5 retries due to rate limiting (429)
```

**Answer:** AI-generated responses are temporarily unavailable. Here are the most relevant notes we found for your question.

---

### [aq_029] Reranking vs hybrid fusion: which approach is better for RAG?

- **Category:** comparison | **Difficulty:** hard
- **Status:** degraded | **Retrieval-Only:** True
- **Expected Notes:** [67, 119, 123, 176, 183, 213, 228, 252, 375, 381, 386, 486, 518, 523, 555, 648, 676, 696, 702, 717, 718, 729, 735, 776, 796, 802, 817, 818, 829, 835, 876, 896, 902, 917, 918, 929, 935, 976, 996, 1002, 1017, 1018, 1029, 1035, 1076, 1096, 1102]
- **Retrieved Notes:** [386, 252, 696, 796, 896, 996, 1096, 595]
- **Recall@Expected:** 0.149 | **Context Utilisation:** 0.000
- **Latency:** retrieval=579ms, llm=64671ms, total=65250ms
- **Cost:** $0.00003870 USD

**Root cause:** `evaluator_failure`

**Error:**
```
Judge Gemini failed after 5 retries due to rate limiting (429)
```

**Answer:** AI-generated responses are temporarily unavailable. Here are the most relevant notes we found for your question.

---

### [aq_030] What are the trade-offs between monolith and microservices architectures?

- **Category:** comparison | **Difficulty:** hard
- **Status:** degraded | **Retrieval-Only:** True
- **Expected Notes:** [62, 101, 118, 180, 181, 225, 263, 299, 355, 372, 383, 392, 408, 410, 519, 534, 628, 652, 665, 688, 712, 732, 739, 752, 765, 788, 812, 832, 839, 852, 865, 888, 912, 932, 939, 952, 965, 988, 1012, 1032, 1039, 1052, 1065, 1088]
- **Retrieved Notes:** [105, 263, 156, 178, 372, 189, 697, 797]
- **Recall@Expected:** 0.045 | **Context Utilisation:** 0.000
- **Latency:** retrieval=110ms, llm=64609ms, total=64719ms
- **Cost:** $0.00005377 USD

**Root cause:** `evaluator_failure`

**Error:**
```
Judge Gemini failed after 5 retries due to rate limiting (429)
```

**Answer:** AI-generated responses are temporarily unavailable. Here are the most relevant notes we found for your question.

---

### [aq_031] Summarize all my AI and machine learning study notes.

- **Category:** synthesis | **Difficulty:** hard
- **Status:** degraded | **Retrieval-Only:** True
- **Expected Notes:** [60, 64, 72, 85, 87, 101, 110, 112, 114, 117]
- **Retrieved Notes:** [87, 529, 85, 230, 525, 416, 619, 617]
- **Recall@Expected:** 0.200 | **Context Utilisation:** 0.000
- **Latency:** retrieval=79ms, llm=64359ms, total=64438ms
- **Cost:** $0.00006292 USD

**Root cause:** `evaluator_failure`

**Error:**
```
Judge Gemini failed after 5 retries due to rate limiting (429)
```

**Answer:** AI-generated responses are temporarily unavailable. Here are the most relevant notes we found for your question.

---

### [aq_032] What are all the KnowledgeVault architectural decisions I've documented?

- **Category:** synthesis | **Difficulty:** hard
- **Status:** degraded | **Retrieval-Only:** True
- **Expected Notes:** [57, 62, 65, 70, 87, 88, 89, 90, 91, 94, 95, 96, 97, 102, 106, 107, 125, 145, 156, 185, 227, 231, 236, 247, 251, 255, 262, 267, 305, 309, 310, 337, 344, 346, 360, 372, 386, 392, 405, 413, 420, 426, 428, 430, 439, 442, 444, 452, 453, 480, 482, 498, 523, 528, 538, 540, 555, 568, 580, 582, 602, 603, 607, 616, 626, 628, 638, 728, 732, 753, 755, 828, 832, 853, 855, 928, 932, 953, 955, 1028, 1032, 1053, 1055]
- **Retrieved Notes:** [95, 90, 57, 628, 732, 832, 932, 1032]
- **Recall@Expected:** 0.096 | **Context Utilisation:** 0.000
- **Latency:** retrieval=109ms, llm=64954ms, total=65063ms
- **Cost:** $0.00003495 USD

**Root cause:** `evaluator_failure`

**Error:**
```
Judge Gemini failed after 5 retries due to rate limiting (429)
```

**Answer:** AI-generated responses are temporarily unavailable. Here are the most relevant notes we found for your question.

---

### [aq_033] What programming languages and technologies have I been studying?

- **Category:** synthesis | **Difficulty:** medium
- **Status:** degraded | **Retrieval-Only:** True
- **Expected Notes:** [59, 60, 108, 113, 114, 138, 152, 162, 174, 177]
- **Retrieved Notes:** [563, 266, 751, 851, 951, 1051, 357, 416]
- **Recall@Expected:** 0.000 | **Context Utilisation:** 0.000
- **Latency:** retrieval=937ms, llm=64079ms, total=65016ms
- **Cost:** $0.00004500 USD

**Root cause:** `evaluator_failure`

**Error:**
```
Judge Gemini failed after 5 retries due to rate limiting (429)
```

**Answer:** AI-generated responses are temporarily unavailable. Here are the most relevant notes we found for your question.

---

### [aq_034] Summarize my health and wellness notes.

- **Category:** synthesis | **Difficulty:** medium
- **Status:** degraded | **Retrieval-Only:** True
- **Expected Notes:** [79, 109, 133, 136, 157, 201, 202, 210, 212, 286, 288, 317, 348, 355, 380, 410, 434, 472, 538, 548, 574, 575, 601, 621, 622, 631, 664, 680, 688, 764, 780, 788, 864, 880, 888, 964, 980, 988, 1064, 1080, 1088]
- **Retrieved Notes:** [87, 212, 444, 575, 583, 699, 799, 899]
- **Recall@Expected:** 0.049 | **Context Utilisation:** 0.000
- **Latency:** retrieval=500ms, llm=63250ms, total=63750ms
- **Cost:** $0.00004755 USD

**Root cause:** `evaluator_failure`

**Error:**
```
Judge Gemini failed after 5 retries due to rate limiting (429)
```

**Answer:** AI-generated responses are temporarily unavailable. Here are the most relevant notes we found for your question.

---

### [aq_035] What are all my startup ideas and business notes?

- **Category:** synthesis | **Difficulty:** medium
- **Status:** degraded | **Retrieval-Only:** True
- **Expected Notes:** [85, 86, 117, 120, 125, 128, 131, 134]
- **Retrieved Notes:** [85, 525, 459, 134, 617, 441, 178, 87]
- **Recall@Expected:** 0.250 | **Context Utilisation:** 0.000
- **Latency:** retrieval=3531ms, llm=64156ms, total=67687ms
- **Cost:** $0.00006157 USD

**Root cause:** `evaluator_failure`

**Error:**
```
Judge Gemini failed after 5 retries due to rate limiting (429)
```

**Answer:** AI-generated responses are temporarily unavailable. Here are the most relevant notes we found for your question.

---

### [aq_036] What have I been learning lately?

- **Category:** ambiguous | **Difficulty:** medium
- **Status:** degraded | **Retrieval-Only:** True
- **Expected Notes:** [140, 144, 145, 149, 152, 163, 170, 171]
- **Retrieved Notes:** [357, 505, 119, 613, 69, 272, 540, 603]
- **Recall@Expected:** 0.000 | **Context Utilisation:** 0.000
- **Latency:** retrieval=437ms, llm=64344ms, total=64781ms
- **Cost:** $0.00006517 USD

**Root cause:** `evaluator_failure`

**Error:**
```
Judge Gemini failed after 5 retries due to rate limiting (429)
```

**Answer:** AI-generated responses are temporarily unavailable. Here are the most relevant notes we found for your question.

---

### [aq_037] What technical problems have I been solving?

- **Category:** ambiguous | **Difficulty:** medium
- **Status:** degraded | **Retrieval-Only:** True
- **Expected Notes:** [94, 136, 163, 246, 270, 335, 340, 357]
- **Retrieved Notes:** [647, 357, 199, 522, 591, 632, 453, 99]
- **Recall@Expected:** 0.125 | **Context Utilisation:** 0.000
- **Latency:** retrieval=109ms, llm=64188ms, total=64297ms
- **Cost:** $0.00006368 USD

**Root cause:** `evaluator_failure`

**Error:**
```
Judge Gemini failed after 5 retries due to rate limiting (429)
```

**Answer:** AI-generated responses are temporarily unavailable. Here are the most relevant notes we found for your question.

---

### [aq_038] What are the most important things I've realized this month?

- **Category:** ambiguous | **Difficulty:** hard
- **Status:** degraded | **Retrieval-Only:** True
- **Expected Notes:** [63, 102, 140, 154, 163, 170]
- **Retrieved Notes:** [647, 442, 755, 855, 955, 1055, 77, 212]
- **Recall@Expected:** 0.000 | **Context Utilisation:** 0.000
- **Latency:** retrieval=484ms, llm=64360ms, total=64844ms
- **Cost:** $0.00004140 USD

**Root cause:** `evaluator_failure`

**Error:**
```
Judge Gemini failed after 5 retries due to rate limiting (429)
```

**Answer:** AI-generated responses are temporarily unavailable. Here are the most relevant notes we found for your question.

---

### [aq_039] Notes related to my project

- **Category:** ambiguous | **Difficulty:** medium
- **Status:** degraded | **Retrieval-Only:** True
- **Expected Notes:** [62, 89, 91, 92, 97, 117, 118, 134]
- **Retrieved Notes:** [87, 106, 444, 290, 583, 699, 799, 899]
- **Recall@Expected:** 0.000 | **Context Utilisation:** 0.000
- **Latency:** retrieval=125ms, llm=64031ms, total=64156ms
- **Cost:** $0.00004350 USD

**Root cause:** `evaluator_failure`

**Error:**
```
Judge Gemini failed after 5 retries due to rate limiting (429)
```

**Answer:** AI-generated responses are temporarily unavailable. Here are the most relevant notes we found for your question.

---

### [aq_040] Show all my communication and meeting notes.

- **Category:** category | **Difficulty:** easy
- **Status:** degraded | **Retrieval-Only:** True
- **Expected Notes:** [54, 55, 56, 57, 106, 107, 117, 141]
- **Retrieved Notes:** [372, 568, 371, 56, 382, 141, 290, 583]
- **Recall@Expected:** 0.250 | **Context Utilisation:** 0.000
- **Latency:** retrieval=125ms, llm=63641ms, total=63766ms
- **Cost:** $0.00006397 USD

**Root cause:** `evaluator_failure`

**Error:**
```
Judge Gemini failed after 5 retries due to rate limiting (429)
```

**Answer:** AI-generated responses are temporarily unavailable. Here are the most relevant notes we found for your question.

---

### [aq_041] What reminders and shopping lists do I have?

- **Category:** category | **Difficulty:** easy
- **Status:** degraded | **Retrieval-Only:** True
- **Expected Notes:** [76, 115, 122, 139, 164, 168]
- **Retrieved Notes:** [475, 393, 216, 322, 680, 76, 606, 620]
- **Recall@Expected:** 0.167 | **Context Utilisation:** 0.000
- **Latency:** retrieval=110ms, llm=64500ms, total=64610ms
- **Cost:** $0.00006180 USD

**Root cause:** `evaluator_failure`

**Error:**
```
Judge Gemini failed after 5 retries due to rate limiting (429)
```

**Answer:** AI-generated responses are temporarily unavailable. Here are the most relevant notes we found for your question.

---

### [aq_042] What ideas am I excited about?

- **Category:** category | **Difficulty:** easy
- **Status:** degraded | **Retrieval-Only:** True
- **Expected Notes:** [85, 86, 95, 97, 117, 121]
- **Retrieved Notes:** [85, 166, 685, 785, 885, 985, 1085, 416]
- **Recall@Expected:** 0.167 | **Context Utilisation:** 0.000
- **Latency:** retrieval=109ms, llm=64375ms, total=64484ms
- **Cost:** $0.00003495 USD

**Root cause:** `evaluator_failure`

**Error:**
```
Judge Gemini failed after 5 retries due to rate limiting (429)
```

**Answer:** AI-generated responses are temporarily unavailable. Here are the most relevant notes we found for your question.

---

### [aq_043] Show all my university study notes.

- **Category:** category | **Difficulty:** medium
- **Status:** degraded | **Retrieval-Only:** True
- **Expected Notes:** [138, 175, 198, 227, 231, 233, 236, 270]
- **Retrieved Notes:** [290, 540, 583, 699, 799, 899, 999, 1099]
- **Recall@Expected:** 0.000 | **Context Utilisation:** 0.000
- **Latency:** retrieval=94ms, llm=63688ms, total=63782ms
- **Cost:** $0.00003825 USD

**Root cause:** `evaluator_failure`

**Error:**
```
Judge Gemini failed after 5 retries due to rate limiting (429)
```

**Answer:** AI-generated responses are temporarily unavailable. Here are the most relevant notes we found for your question.

---

### [aq_044] What is BRPOPLPUSH?

- **Category:** factual_lookup | **Difficulty:** hard
- **Status:** degraded | **Retrieval-Only:** True
- **Expected Notes:** [246, 433, 643, 673, 684, 705, 773, 784, 805, 873, 884, 905, 973, 984, 1005, 1073, 1084, 1105]
- **Retrieved Notes:** [643, 673, 773, 873, 973, 1073, 246, 684]
- **Recall@Expected:** 0.444 | **Context Utilisation:** 0.000
- **Latency:** retrieval=125ms, llm=64562ms, total=64687ms
- **Cost:** $0.00003263 USD

**Root cause:** `evaluator_failure`

**Error:**
```
Judge Gemini failed after 5 retries due to rate limiting (429)
```

**Answer:** AI-generated responses are temporarily unavailable. Here are the most relevant notes we found for your question.

---

### [aq_045] What is Atomic Habits about?

- **Category:** factual_lookup | **Difficulty:** easy
- **Status:** degraded | **Retrieval-Only:** True
- **Expected Notes:** [482, 557]
- **Retrieved Notes:** [482, 229, 690, 790, 890, 990, 1090, 73]
- **Recall@Expected:** 0.500 | **Context Utilisation:** 0.000
- **Latency:** retrieval=141ms, llm=63859ms, total=64000ms
- **Cost:** $0.00003518 USD

**Root cause:** `evaluator_failure`

**Error:**
```
Judge Gemini failed after 5 retries due to rate limiting (429)
```

**Answer:** AI-generated responses are temporarily unavailable. Here are the most relevant notes we found for your question.

---

### [aq_046] What is the walrus operator in Python?

- **Category:** factual_lookup | **Difficulty:** easy
- **Status:** degraded | **Retrieval-Only:** True
- **Expected Notes:** [336]
- **Retrieved Notes:** [336, 588, 388, 396, 232, 610, 640, 587]
- **Recall@Expected:** 1.000 | **Context Utilisation:** 0.000
- **Latency:** retrieval=109ms, llm=64313ms, total=64422ms
- **Cost:** $0.00006510 USD

**Root cause:** `evaluator_failure`

**Error:**
```
Judge Gemini failed after 5 retries due to rate limiting (429)
```

**Answer:** AI-generated responses are temporarily unavailable. Here are the most relevant notes we found for your question.

---

### [aq_047] What is CQRS?

- **Category:** factual_lookup | **Difficulty:** medium
- **Status:** degraded | **Retrieval-Only:** True
- **Expected Notes:** [238, 253, 656, 744, 756, 844, 856, 944, 956, 1044, 1056]
- **Retrieved Notes:** [253, 656, 756, 856, 956, 1056, 217, 238]
- **Recall@Expected:** 0.636 | **Context Utilisation:** 0.000
- **Latency:** retrieval=172ms, llm=63671ms, total=63843ms
- **Cost:** $0.00003900 USD

**Root cause:** `evaluator_failure`

**Error:**
```
Judge Gemini failed after 5 retries due to rate limiting (429)
```

**Answer:** AI-generated responses are temporarily unavailable. Here are the most relevant notes we found for your question.

---


---
_Generated automatically by the KnowledgeVault Ask Evaluation Framework._