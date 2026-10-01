# Token usage and API spend

How much the AI assistance in this project actually cost, in tokens and in
money. This file is generated from the local opencode session database by
`costs.py`; the numbers are read from the tool, not typed by hand.

Last updated: 2026-10-01 15:13

Model: `deepseek-flash (deepseek)`

## Totals

| Metric | Value |
| --- | --- |
| Sessions | 1 |
| Input tokens | 735,568 |
| Output tokens | 99,061 |
| Reasoning tokens | 359,980 |
| Cache-read tokens | 47,953,024 |
| Cache-write tokens | 0 |
| **Total tokens (all kinds)** | **49,147,633** |
| **API spend (USD)** | **$0.4381** |

## Per session

| Session | Started | Input | Output | Reasoning | Cache read | Cache write | Cost (USD) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ses_f17f91a40ffenBLUPW4wByHmy9 | 2026-09-28 14:39 | 735,568 | 99,061 | 359,980 | 47,953,024 | 0 | $0.4381 |

Notes: cache-read tokens are reused context and are charged at a much lower
rate than fresh input, so the token total is larger than the spend might
suggest. The dollar figure is what opencode recorded as the cost of these
sessions.
