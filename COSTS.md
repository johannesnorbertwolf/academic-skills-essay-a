# Token usage and API spend

How much the AI assistance in this project actually cost, in tokens and in
money. This file is generated from the local opencode session database by
`costs.py`; the numbers are read from the tool, not typed by hand.

Last updated: 2026-10-01 15:03

Model: `deepseek-flash (deepseek)`

## Totals

| Metric | Value |
| --- | --- |
| Sessions | 1 |
| Input tokens | 725,444 |
| Output tokens | 95,742 |
| Reasoning tokens | 349,662 |
| Cache-read tokens | 47,451,904 |
| Cache-write tokens | 0 |
| **Total tokens (all kinds)** | **48,622,752** |
| **API spend (USD)** | **$0.4269** |

## Per session

| Session | Started | Input | Output | Reasoning | Cache read | Cache write | Cost (USD) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ses_f17f91a40ffenBLUPW4wByHmy9 | 2026-09-28 14:39 | 725,444 | 95,742 | 349,662 | 47,451,904 | 0 | $0.4269 |

Notes: cache-read tokens are reused context and are charged at a much lower
rate than fresh input, so the token total is larger than the spend might
suggest. The dollar figure is what opencode recorded as the cost of these
sessions.
