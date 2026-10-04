# Token usage and API spend

How much the AI assistance in this project actually cost, in tokens and in
money. This file is generated from the local opencode session database by
`costs.py`; the numbers are read from the tool, not typed by hand.

Last updated: 2026-10-04 14:47

Model: `deepseek-flash (deepseek)`

## Totals

| Metric | Value |
| --- | --- |
| Sessions | 1 |
| Input tokens | 1,058,629 |
| Output tokens | 127,570 |
| Reasoning tokens | 460,135 |
| Cache-read tokens | 56,036,608 |
| Cache-write tokens | 0 |
| **Total tokens (all kinds)** | **57,682,942** |
| **API spend (USD)** | **$0.5880** |

## Per session

| Session | Started | Input | Output | Reasoning | Cache read | Cache write | Cost (USD) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ses_f17f91a40ffenBLUPW4wByHmy9 | 2026-09-28 14:39 | 1,058,629 | 127,570 | 460,135 | 56,036,608 | 0 | $0.5880 |

Notes: cache-read tokens are reused context and are charged at a much lower
rate than fresh input, so the token total is larger than the spend might
suggest. The dollar figure is what opencode recorded as the cost of these
sessions.
