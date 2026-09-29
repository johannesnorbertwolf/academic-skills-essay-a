# Token usage and API spend

How much the AI assistance in this project actually cost, in tokens and in
money. This file is generated from the local opencode session database by
`costs.py`; the numbers are read from the tool, not typed by hand.

Last updated: 2026-09-29 20:57

Model: `deepseek-flash (deepseek)`

## Totals

| Metric | Value |
| --- | --- |
| Sessions | 1 |
| Input tokens | 420,444 |
| Output tokens | 68,109 |
| Reasoning tokens | 189,535 |
| Cache-read tokens | 40,348,160 |
| Cache-write tokens | 0 |
| **Total tokens (all kinds)** | **41,026,248** |
| **API spend (USD)** | **$0.2472** |

## Per session

| Session | Started | Input | Output | Reasoning | Cache read | Cache write | Cost (USD) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ses_f17f91a40ffenBLUPW4wByHmy9 | 2026-09-28 14:39 | 420,444 | 68,109 | 189,535 | 40,348,160 | 0 | $0.2472 |

Notes: cache-read tokens are reused context and are charged at a much lower
rate than fresh input, so the token total is larger than the spend might
suggest. The dollar figure is what opencode recorded as the cost of these
sessions.
