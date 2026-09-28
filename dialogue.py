#!/usr/bin/env python3
"""Write DIALOGUE.md: the conversation that built this project.

For every prompt Johannes typed, this records the prompt verbatim and the AI's
concluding written answer. It deliberately leaves out the AI's internal
reasoning and all tool activity (file edits, commands, searches), so the file
shows only what was actually said to each other.

Everything is read from the local opencode session database; nothing is typed by
hand.
"""

import os
import sqlite3
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO_SLUG = ROOT.name
DB = Path(os.environ.get("OPENCODE_DB", Path.home() / ".local/share/opencode/opencode.db"))


def blockquote(text):
    lines = (text or "").strip().splitlines()
    return "\n".join("> " + line if line.strip() else ">" for line in lines)


def main():
    if not DB.exists():
        print("opencode database not found at %s; nothing to do." % DB)
        return
    con = sqlite3.connect("file:%s?mode=ro" % DB, uri=True)
    con.row_factory = sqlite3.Row
    session_ids = [
        r["id"]
        for r in con.execute(
            """
            SELECT id FROM session
            WHERE directory = :repo
               OR id IN (SELECT DISTINCT session_id FROM part WHERE data LIKE :pat)
            ORDER BY time_created
            """,
            {"repo": str(ROOT), "pat": "%" + REPO_SLUG + "%"},
        )
    ]
    if not session_ids:
        print("No sessions found for this project yet.")
        return

    placeholders = ",".join("?" for _ in session_ids)
    rows = con.execute(
        """
        SELECT p.session_id, p.time_created, p.id,
               json_extract(m.data, '$.role') AS role,
               json_extract(p.data, '$.type') AS type,
               json_extract(p.data, '$.text') AS text
        FROM part p JOIN message m ON p.message_id = m.id
        WHERE p.session_id IN (%s)
        ORDER BY p.time_created, p.id
        """ % placeholders,
        session_ids,
    ).fetchall()

    exchanges = []
    current = None
    for r in rows:
        if r["role"] == "user" and r["type"] == "text":
            if current:
                exchanges.append(current)
            current = {"prompt": r["text"] or "", "time": r["time_created"], "parts": []}
        elif current is not None and r["role"] == "assistant":
            current["parts"].append((r["type"], r["text"] or ""))
    if current:
        exchanges.append(current)

    out = []
    out.append("# Dialogue\n")
    out.append(
        "Every prompt Johannes typed while building this project, and the AI's\n"
        "concluding answer to it. The AI's internal reasoning and all tool activity\n"
        "(edits, commands, searches) are left out, so this is only what was said.\n\n"
        "Generated from the local opencode session database by `dialogue.py`.\n"
    )
    out.append("Last updated: %s\n" % datetime.now().strftime("%Y-%m-%d %H:%M"))

    for i, ex in enumerate(exchanges, 1):
        parts = ex["parts"]
        last_tool = max((j for j, (t, _) in enumerate(parts) if t == "tool"), default=-1)
        answer = "\n\n".join(
            txt for t, txt in parts[last_tool + 1:] if t == "text" and txt.strip()
        )
        if not answer.strip():
            tail = [txt for t, txt in parts if t == "text" and txt.strip()]
            answer = tail[-1] if tail else "_(no written answer recorded)_"
        when = datetime.fromtimestamp((ex["time"] or 0) / 1000).strftime("%Y-%m-%d %H:%M")
        out.append("---\n")
        out.append("## Exchange %d — %s\n" % (i, when))
        out.append("**Johannes:**\n")
        out.append(blockquote(ex["prompt"]) + "\n")
        out.append("**AI:**\n")
        out.append(blockquote(answer) + "\n")

    (ROOT / "DIALOGUE.md").write_text("\n".join(out), encoding="utf-8")
    print("Wrote DIALOGUE.md: %d exchange(s)." % len(exchanges))


if __name__ == "__main__":
    main()
