# Token usage and API spend

How much the AI assistance in this project actually cost, in tokens and in
money. This file is generated from the local opencode session database by
`costs.py`; the numbers are read from the tool, not typed by hand.

Last updated: 2026-09-28 15:34

Model: `deepseek-v4-flash (deepseek)`

## Totals

| Metric | Value |
| --- | --- |
| Sessions | 1 |
| Input tokens | 100,737 |
| Output tokens | 50,772 |
| Reasoning tokens | 124,188 |
| Cache-read tokens | 23,108,992 |
| Cache-write tokens | 0 |
| **Total tokens (all kinds)** | **23,384,689** |
| **API spend (USD)** | **$0.1278** |

## Per session

| Session | Started | Input | Output | Reasoning | Cache read | Cache write | Cost (USD) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ses_f17f91a40ffenBLUPW4wByHmy9 | 2026-09-28 14:39 | 100,737 | 50,772 | 124,188 | 23,108,992 | 0 | $0.1278 |

Notes: cache-read tokens are reused context and are charged at a much lower
rate than fresh input, so the token total is larger than the spend might
suggest. The dollar figure is what opencode recorded as the cost of these
sessions.
