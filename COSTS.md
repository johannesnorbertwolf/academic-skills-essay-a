# Token usage and API spend

How much the AI assistance in this project actually cost, in tokens and in
money. This file is generated from the local opencode session database by
`costs.py`; the numbers are read from the tool, not typed by hand.

Last updated: 2026-09-30 12:17

Model: `deepseek-flash (deepseek)`

## Totals

| Metric | Value |
| --- | --- |
| Sessions | 1 |
| Input tokens | 580,294 |
| Output tokens | 92,030 |
| Reasoning tokens | 338,572 |
| Cache-read tokens | 46,915,968 |
| Cache-write tokens | 0 |
| **Total tokens (all kinds)** | **47,926,864** |
| **API spend (USD)** | **$0.3946** |

## Per session

| Session | Started | Input | Output | Reasoning | Cache read | Cache write | Cost (USD) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ses_f17f91a40ffenBLUPW4wByHmy9 | 2026-09-28 14:39 | 580,294 | 92,030 | 338,572 | 46,915,968 | 0 | $0.3946 |

Notes: cache-read tokens are reused context and are charged at a much lower
rate than fresh input, so the token total is larger than the spend might
suggest. The dollar figure is what opencode recorded as the cost of these
sessions.
