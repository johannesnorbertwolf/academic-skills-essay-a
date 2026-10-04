# Token usage and API spend

How much the AI assistance in this project actually cost, in tokens and in
money. This file is generated from the local opencode session database by
`costs.py`; the numbers are read from the tool, not typed by hand.

Last updated: 2026-10-04 16:23

Model: `deepseek-flash (deepseek)`

## Totals

| Metric | Value |
| --- | --- |
| Sessions | 1 |
| Input tokens | 1,436,371 |
| Output tokens | 169,092 |
| Reasoning tokens | 576,635 |
| Cache-read tokens | 66,534,656 |
| Cache-write tokens | 0 |
| **Total tokens (all kinds)** | **68,716,754** |
| **API spend (USD)** | **$0.7710** |

## Per session

| Session | Started | Input | Output | Reasoning | Cache read | Cache write | Cost (USD) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ses_f17f91a40ffenBLUPW4wByHmy9 | 2026-09-28 14:39 | 1,436,371 | 169,092 | 576,635 | 66,534,656 | 0 | $0.7710 |

Notes: cache-read tokens are reused context and are charged at a much lower
rate than fresh input, so the token total is larger than the spend might
suggest. The dollar figure is what opencode recorded as the cost of these
sessions.
