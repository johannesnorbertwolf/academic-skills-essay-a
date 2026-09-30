# Token usage and API spend

How much the AI assistance in this project actually cost, in tokens and in
money. This file is generated from the local opencode session database by
`costs.py`; the numbers are read from the tool, not typed by hand.

Last updated: 2026-09-30 11:41

Model: `deepseek-flash (deepseek)`

## Totals

| Metric | Value |
| --- | --- |
| Sessions | 1 |
| Input tokens | 576,117 |
| Output tokens | 86,490 |
| Reasoning tokens | 297,858 |
| Cache-read tokens | 45,033,216 |
| Cache-write tokens | 0 |
| **Total tokens (all kinds)** | **45,993,681** |
| **API spend (USD)** | **$0.3606** |

## Per session

| Session | Started | Input | Output | Reasoning | Cache read | Cache write | Cost (USD) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ses_f17f91a40ffenBLUPW4wByHmy9 | 2026-09-28 14:39 | 576,117 | 86,490 | 297,858 | 45,033,216 | 0 | $0.3606 |

Notes: cache-read tokens are reused context and are charged at a much lower
rate than fresh input, so the token total is larger than the spend might
suggest. The dollar figure is what opencode recorded as the cost of these
sessions.
