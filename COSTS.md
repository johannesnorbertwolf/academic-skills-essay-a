# Token usage and API spend

How much the AI assistance in this project actually cost, in tokens and in
money. This file is generated from the local opencode session database by
`costs.py`; the numbers are read from the tool, not typed by hand.

Last updated: 2026-09-28 14:53

Model: `deepseek-v4-flash (deepseek)`

## Totals

| Metric | Value |
| --- | --- |
| Sessions | 1 |
| Input tokens | 18,989 |
| Output tokens | 17,928 |
| Reasoning tokens | 40,237 |
| Cache-read tokens | 1,517,568 |
| Cache-write tokens | 0 |
| **Total tokens (all kinds)** | **1,594,722** |
| **API spend (USD)** | **$0.0232** |

## Per session

| Session | Started | Input | Output | Reasoning | Cache read | Cache write | Cost (USD) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ses_f17f91a40ffenBLUPW4wByHmy9 | 2026-09-28 14:39 | 18,989 | 17,928 | 40,237 | 1,517,568 | 0 | $0.0232 |

Notes: cache-read tokens are reused context and are charged at a much lower
rate than fresh input, so the token total is larger than the spend might
suggest. The dollar figure is what opencode recorded as the cost of these
sessions.
