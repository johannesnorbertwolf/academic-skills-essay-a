# Token usage and API spend

How much the AI assistance in this project actually cost, in tokens and in
money. This file is generated from the local opencode session database by
`costs.py`; the numbers are read from the tool, not typed by hand.

Last updated: 2026-09-30 11:18

Model: `deepseek-flash (deepseek)`

## Totals

| Metric | Value |
| --- | --- |
| Sessions | 1 |
| Input tokens | 560,447 |
| Output tokens | 81,309 |
| Reasoning tokens | 275,149 |
| Cache-read tokens | 43,996,672 |
| Cache-write tokens | 0 |
| **Total tokens (all kinds)** | **44,913,577** |
| **API spend (USD)** | **$0.3384** |

## Per session

| Session | Started | Input | Output | Reasoning | Cache read | Cache write | Cost (USD) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ses_f17f91a40ffenBLUPW4wByHmy9 | 2026-09-28 14:39 | 560,447 | 81,309 | 275,149 | 43,996,672 | 0 | $0.3384 |

Notes: cache-read tokens are reused context and are charged at a much lower
rate than fresh input, so the token total is larger than the spend might
suggest. The dollar figure is what opencode recorded as the cost of these
sessions.
