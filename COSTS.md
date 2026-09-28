# Token usage and API spend

How much the AI assistance in this project actually cost, in tokens and in
money. This file is generated from the local opencode session database by
`costs.py`; the numbers are read from the tool, not typed by hand.

Last updated: 2026-09-28 15:49

Model: `deepseek-v4-flash (deepseek)`

## Totals

| Metric | Value |
| --- | --- |
| Sessions | 1 |
| Input tokens | 111,285 |
| Output tokens | 59,917 |
| Reasoning tokens | 152,255 |
| Cache-read tokens | 35,271,936 |
| Cache-write tokens | 0 |
| **Total tokens (all kinds)** | **35,595,393** |
| **API spend (USD)** | **$0.1737** |

## Per session

| Session | Started | Input | Output | Reasoning | Cache read | Cache write | Cost (USD) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ses_f17f91a40ffenBLUPW4wByHmy9 | 2026-09-28 14:39 | 111,285 | 59,917 | 152,255 | 35,271,936 | 0 | $0.1737 |

Notes: cache-read tokens are reused context and are charged at a much lower
rate than fresh input, so the token total is larger than the spend might
suggest. The dollar figure is what opencode recorded as the cost of these
sessions.
