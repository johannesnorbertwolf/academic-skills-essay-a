#!/usr/bin/env python3
"""Write COSTS.md from the local opencode session database.

Finds the sessions that belong to this project and reports the token counts and
API spend opencode recorded for them. Nothing here is typed by hand.
"""

import json
import os
import sqlite3
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO_SLUG = ROOT.name
DB = Path(os.environ.get("OPENCODE_DB", Path.home() / ".local/share/opencode/opencode.db"))


def fmt(n):
    return "{:,}".format(int(n or 0))


def model_label(raw):
    try:
        data = json.loads(raw) if raw else {}
    except (ValueError, TypeError):
        return raw or "unknown"
    ident = data.get("id", "unknown")
    provider = data.get("providerID", "")
    return ("%s (%s)" % (ident, provider)) if provider else ident


def main():
    if not DB.exists():
        print("opencode database not found at %s; nothing to do." % DB)
        return
    con = sqlite3.connect("file:%s?mode=ro" % DB, uri=True)
    con.row_factory = sqlite3.Row
    rows = con.execute(
        """
        SELECT id, title, directory, model, cost, tokens_input, tokens_output,
               tokens_reasoning, tokens_cache_read, tokens_cache_write,
               time_created, time_updated
        FROM session
        WHERE directory = :repo
           OR id IN (SELECT DISTINCT session_id FROM part WHERE data LIKE :pat)
        ORDER BY time_created
        """,
        {"repo": str(ROOT), "pat": "%" + REPO_SLUG + "%"},
    ).fetchall()

    totals = {
        "cost": 0.0,
        "tokens_input": 0,
        "tokens_output": 0,
        "tokens_reasoning": 0,
        "tokens_cache_read": 0,
        "tokens_cache_write": 0,
    }
    for r in rows:
        for key in totals:
            totals[key] += r[key] or 0

    lines = []
    lines.append("# Token usage and API spend\n")
    lines.append(
        "How much the AI assistance in this project actually cost, in tokens and in\n"
        "money. This file is generated from the local opencode session database by\n"
        "`costs.py`; the numbers are read from the tool, not typed by hand.\n"
    )
    lines.append("Last updated: %s\n" % datetime.now().strftime("%Y-%m-%d %H:%M"))
    lines.append("Model: `%s`\n" % (model_label(rows[-1]["model"]) if rows else "unknown"))
    lines.append("## Totals\n")
    lines.append("| Metric | Value |")
    lines.append("| --- | --- |")
    lines.append("| Sessions | %d |" % len(rows))
    lines.append("| Input tokens | %s |" % fmt(totals["tokens_input"]))
    lines.append("| Output tokens | %s |" % fmt(totals["tokens_output"]))
    lines.append("| Reasoning tokens | %s |" % fmt(totals["tokens_reasoning"]))
    lines.append("| Cache-read tokens | %s |" % fmt(totals["tokens_cache_read"]))
    lines.append("| Cache-write tokens | %s |" % fmt(totals["tokens_cache_write"]))
    lines.append("| **Total tokens (all kinds)** | **%s** |" % fmt(sum(totals.values()) - totals["cost"]))
    lines.append("| **API spend (USD)** | **$%.4f** |" % totals["cost"])
    lines.append("")
    lines.append("## Per session\n")
    lines.append(
        "| Session | Started | Input | Output | Reasoning | Cache read | Cache write | Cost (USD) |"
    )
    lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for r in rows:
        started = datetime.fromtimestamp((r["time_created"] or 0) / 1000).strftime("%Y-%m-%d %H:%M")
        lines.append(
            "| %s | %s | %s | %s | %s | %s | %s | $%.4f |"
            % (
                r["id"],
                started,
                fmt(r["tokens_input"]),
                fmt(r["tokens_output"]),
                fmt(r["tokens_reasoning"]),
                fmt(r["tokens_cache_read"]),
                fmt(r["tokens_cache_write"]),
                r["cost"] or 0,
            )
        )
    lines.append("")
    lines.append(
        "Notes: cache-read tokens are reused context and are charged at a much lower\n"
        "rate than fresh input, so the token total is larger than the spend might\n"
        "suggest. The dollar figure is what opencode recorded as the cost of these\n"
        "sessions.\n"
    )
    (ROOT / "COSTS.md").write_text("\n".join(lines), encoding="utf-8")
    print("Wrote COSTS.md: %d session(s), $%.4f." % (len(rows), totals["cost"]))


if __name__ == "__main__":
    main()
