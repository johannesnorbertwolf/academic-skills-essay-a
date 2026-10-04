# Token usage and API spend

How much the AI assistance in this project actually cost, in tokens and in
money. This file is generated from the local opencode session database by
`costs.py`; the numbers are read from the tool, not typed by hand.

Last updated: 2026-10-04 15:33

Model: `deepseek-flash (deepseek)`

## Totals

| Metric | Value |
| --- | --- |
| Sessions | 1 |
| Input tokens | 1,258,511 |
| Output tokens | 149,033 |
| Reasoning tokens | 534,866 |
| Cache-read tokens | 62,164,480 |
| Cache-write tokens | 0 |
| **Total tokens (all kinds)** | **64,106,890** |
| **API spend (USD)** | **$0.6941** |

## Per session

| Session | Started | Input | Output | Reasoning | Cache read | Cache write | Cost (USD) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ses_f17f91a40ffenBLUPW4wByHmy9 | 2026-09-28 14:39 | 1,258,511 | 149,033 | 534,866 | 62,164,480 | 0 | $0.6941 |

Notes: cache-read tokens are reused context and are charged at a much lower
rate than fresh input, so the token total is larger than the spend might
suggest. The dollar figure is what opencode recorded as the cost of these
sessions.
