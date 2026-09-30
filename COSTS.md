# Token usage and API spend

How much the AI assistance in this project actually cost, in tokens and in
money. This file is generated from the local opencode session database by
`costs.py`; the numbers are read from the tool, not typed by hand.

Last updated: 2026-09-30 11:49

Model: `deepseek-flash (deepseek)`

## Totals

| Metric | Value |
| --- | --- |
| Sessions | 1 |
| Input tokens | 577,848 |
| Output tokens | 89,413 |
| Reasoning tokens | 321,283 |
| Cache-read tokens | 45,937,408 |
| Cache-write tokens | 0 |
| **Total tokens (all kinds)** | **46,925,952** |
| **API spend (USD)** | **$0.3794** |

## Per session

| Session | Started | Input | Output | Reasoning | Cache read | Cache write | Cost (USD) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ses_f17f91a40ffenBLUPW4wByHmy9 | 2026-09-28 14:39 | 577,848 | 89,413 | 321,283 | 45,937,408 | 0 | $0.3794 |

Notes: cache-read tokens are reused context and are charged at a much lower
rate than fresh input, so the token total is larger than the spend might
suggest. The dollar figure is what opencode recorded as the cost of these
sessions.
