# Token usage and API spend

How much the AI assistance in this project actually cost, in tokens and in
money. This file is generated from the local opencode session database by
`costs.py`; the numbers are read from the tool, not typed by hand.

Last updated: 2026-10-04 15:53

Model: `deepseek-flash (deepseek)`

## Totals

| Metric | Value |
| --- | --- |
| Sessions | 1 |
| Input tokens | 1,409,399 |
| Output tokens | 156,218 |
| Reasoning tokens | 548,448 |
| Cache-read tokens | 64,955,008 |
| Cache-write tokens | 0 |
| **Total tokens (all kinds)** | **67,069,073** |
| **API spend (USD)** | **$0.7375** |

## Per session

| Session | Started | Input | Output | Reasoning | Cache read | Cache write | Cost (USD) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ses_f17f91a40ffenBLUPW4wByHmy9 | 2026-09-28 14:39 | 1,409,399 | 156,218 | 548,448 | 64,955,008 | 0 | $0.7375 |

Notes: cache-read tokens are reused context and are charged at a much lower
rate than fresh input, so the token total is larger than the spend might
suggest. The dollar figure is what opencode recorded as the cost of these
sessions.
