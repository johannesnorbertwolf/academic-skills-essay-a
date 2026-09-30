# Token usage and API spend

How much the AI assistance in this project actually cost, in tokens and in
money. This file is generated from the local opencode session database by
`costs.py`; the numbers are read from the tool, not typed by hand.

Last updated: 2026-09-30 11:39

Model: `deepseek-flash (deepseek)`

## Totals

| Metric | Value |
| --- | --- |
| Sessions | 1 |
| Input tokens | 566,361 |
| Output tokens | 83,232 |
| Reasoning tokens | 287,867 |
| Cache-read tokens | 44,570,112 |
| Cache-write tokens | 0 |
| **Total tokens (all kinds)** | **45,507,572** |
| **API spend (USD)** | **$0.3498** |

## Per session

| Session | Started | Input | Output | Reasoning | Cache read | Cache write | Cost (USD) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ses_f17f91a40ffenBLUPW4wByHmy9 | 2026-09-28 14:39 | 566,361 | 83,232 | 287,867 | 44,570,112 | 0 | $0.3498 |

Notes: cache-read tokens are reused context and are charged at a much lower
rate than fresh input, so the token total is larger than the spend might
suggest. The dollar figure is what opencode recorded as the cost of these
sessions.
