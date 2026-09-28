# Token usage and API spend

How much the AI assistance in this project actually cost, in tokens and in
money. This file is generated from the local opencode session database by
`costs.py`; the numbers are read from the tool, not typed by hand.

Last updated: 2026-09-28 15:14

Model: `deepseek-v4-flash (deepseek)`

## Totals

| Metric | Value |
| --- | --- |
| Sessions | 1 |
| Input tokens | 89,002 |
| Output tokens | 42,562 |
| Reasoning tokens | 98,697 |
| Cache-read tokens | 16,975,232 |
| Cache-write tokens | 0 |
| **Total tokens (all kinds)** | **17,205,493** |
| **API spend (USD)** | **$0.0995** |

## Per session

| Session | Started | Input | Output | Reasoning | Cache read | Cache write | Cost (USD) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ses_f17f91a40ffenBLUPW4wByHmy9 | 2026-09-28 14:39 | 89,002 | 42,562 | 98,697 | 16,975,232 | 0 | $0.0995 |

Notes: cache-read tokens are reused context and are charged at a much lower
rate than fresh input, so the token total is larger than the spend might
suggest. The dollar figure is what opencode recorded as the cost of these
sessions.
