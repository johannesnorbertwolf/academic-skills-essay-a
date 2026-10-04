# Token usage and API spend

How much the AI assistance in this project actually cost, in tokens and in
money. This file is generated from the local opencode session database by
`costs.py`; the numbers are read from the tool, not typed by hand.

Last updated: 2026-10-04 16:01

Model: `deepseek-flash (deepseek)`

## Totals

| Metric | Value |
| --- | --- |
| Sessions | 1 |
| Input tokens | 1,435,004 |
| Output tokens | 167,018 |
| Reasoning tokens | 573,721 |
| Cache-read tokens | 66,009,856 |
| Cache-write tokens | 0 |
| **Total tokens (all kinds)** | **68,185,599** |
| **API spend (USD)** | **$0.7662** |

## Per session

| Session | Started | Input | Output | Reasoning | Cache read | Cache write | Cost (USD) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ses_f17f91a40ffenBLUPW4wByHmy9 | 2026-09-28 14:39 | 1,435,004 | 167,018 | 573,721 | 66,009,856 | 0 | $0.7662 |

Notes: cache-read tokens are reused context and are charged at a much lower
rate than fresh input, so the token total is larger than the spend might
suggest. The dollar figure is what opencode recorded as the cost of these
sessions.
