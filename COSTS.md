# Token usage and API spend

How much the AI assistance in this project actually cost, in tokens and in
money. This file is generated from the local opencode session database by
`costs.py`; the numbers are read from the tool, not typed by hand.

Last updated: 2026-09-29 21:22

Model: `deepseek-flash (deepseek)`

## Totals

| Metric | Value |
| --- | --- |
| Sessions | 1 |
| Input tokens | 439,695 |
| Output tokens | 74,065 |
| Reasoning tokens | 243,064 |
| Cache-read tokens | 42,500,480 |
| Cache-write tokens | 0 |
| **Total tokens (all kinds)** | **43,257,304** |
| **API spend (USD)** | **$0.2922** |

## Per session

| Session | Started | Input | Output | Reasoning | Cache read | Cache write | Cost (USD) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ses_f17f91a40ffenBLUPW4wByHmy9 | 2026-09-28 14:39 | 439,695 | 74,065 | 243,064 | 42,500,480 | 0 | $0.2922 |

Notes: cache-read tokens are reused context and are charged at a much lower
rate than fresh input, so the token total is larger than the spend might
suggest. The dollar figure is what opencode recorded as the cost of these
sessions.
