# Token usage and API spend

How much the AI assistance in this project actually cost, in tokens and in
money. This file is generated from the local opencode session database by
`costs.py`; the numbers are read from the tool, not typed by hand.

Last updated: 2026-10-04 15:46

Model: `deepseek-flash (deepseek)`

## Totals

| Metric | Value |
| --- | --- |
| Sessions | 1 |
| Input tokens | 1,259,375 |
| Output tokens | 150,178 |
| Reasoning tokens | 539,050 |
| Cache-read tokens | 63,002,112 |
| Cache-write tokens | 0 |
| **Total tokens (all kinds)** | **64,950,715** |
| **API spend (USD)** | **$0.6999** |

## Per session

| Session | Started | Input | Output | Reasoning | Cache read | Cache write | Cost (USD) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ses_f17f91a40ffenBLUPW4wByHmy9 | 2026-09-28 14:39 | 1,259,375 | 150,178 | 539,050 | 63,002,112 | 0 | $0.6999 |

Notes: cache-read tokens are reused context and are charged at a much lower
rate than fresh input, so the token total is larger than the spend might
suggest. The dollar figure is what opencode recorded as the cost of these
sessions.
