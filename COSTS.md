# Token usage and API spend

How much the AI assistance in this project actually cost, in tokens and in
money. This file is generated from the local opencode session database by
`costs.py`; the numbers are read from the tool, not typed by hand.

Last updated: 2026-09-29 21:01

Model: `deepseek-flash (deepseek)`

## Totals

| Metric | Value |
| --- | --- |
| Sessions | 1 |
| Input tokens | 422,659 |
| Output tokens | 69,692 |
| Reasoning tokens | 192,412 |
| Cache-read tokens | 40,639,104 |
| Cache-write tokens | 0 |
| **Total tokens (all kinds)** | **41,323,867** |
| **API spend (USD)** | **$0.2510** |

## Per session

| Session | Started | Input | Output | Reasoning | Cache read | Cache write | Cost (USD) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ses_f17f91a40ffenBLUPW4wByHmy9 | 2026-09-28 14:39 | 422,659 | 69,692 | 192,412 | 40,639,104 | 0 | $0.2510 |

Notes: cache-read tokens are reused context and are charged at a much lower
rate than fresh input, so the token total is larger than the spend might
suggest. The dollar figure is what opencode recorded as the cost of these
sessions.
