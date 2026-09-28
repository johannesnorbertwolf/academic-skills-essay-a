# Token usage and API spend

How much the AI assistance in this project actually cost, in tokens and in
money. This file is generated from the local opencode session database by
`costs.py`; the numbers are read from the tool, not typed by hand.

Last updated: 2026-09-28 15:48

Model: `deepseek-v4-flash (deepseek)`

## Totals

| Metric | Value |
| --- | --- |
| Sessions | 1 |
| Input tokens | 110,224 |
| Output tokens | 59,053 |
| Reasoning tokens | 151,488 |
| Cache-read tokens | 33,498,112 |
| Cache-write tokens | 0 |
| **Total tokens (all kinds)** | **33,818,877** |
| **API spend (USD)** | **$0.1682** |

## Per session

| Session | Started | Input | Output | Reasoning | Cache read | Cache write | Cost (USD) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ses_f17f91a40ffenBLUPW4wByHmy9 | 2026-09-28 14:39 | 110,224 | 59,053 | 151,488 | 33,498,112 | 0 | $0.1682 |

Notes: cache-read tokens are reused context and are charged at a much lower
rate than fresh input, so the token total is larger than the spend might
suggest. The dollar figure is what opencode recorded as the cost of these
sessions.
