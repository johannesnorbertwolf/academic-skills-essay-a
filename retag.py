#!/usr/bin/env python3
"""Re-tag essay.md after Johannes edits it by hand.

The rule: when in doubt, assign the words to Johannes.

It aligns the working copy against the last committed version paragraph by
paragraph, then word by word inside a paragraph. Only a run of at least
MIN_RUN consecutive unchanged words is kept as AI (with its original prompt
number). Everything else — short coincidental matches, edits and additions —
becomes Johannes's (untagged).

Run with no argument to print the result; run with --write to apply it.
"""

import re
import subprocess
import sys
from difflib import SequenceMatcher
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "essay.md"
MIN_RUN = 5

TAG = re.compile(r"\[\[AI:(\d+)\]\]|\[\[/AI\]\]")
TOKEN = re.compile(r"\[\[AI:(\d+)\]\]|\[\[/AI\]\]|(\S+)")


def split_prefix(text):
    idx = text.find("-->")
    if idx == -1:
        return "", text
    idx += len("-->")
    return text[:idx], text[idx:]


def words_with_prompt(line):
    words = []
    prompt = None
    for m in TOKEN.finditer(line):
        if m.group(1):
            prompt = int(m.group(1))
        elif m.group(0) == "[[/AI]]":
            prompt = None
        else:
            words.append((m.group(2), prompt))
    return words


def tokens(text):
    return [(m.group(0), m.start(), m.end()) for m in re.finditer(r"\S+", text)]


def retag_line(base_line, cur_line):
    base = words_with_prompt(base_line)
    base_tokens = [w for w, _ in base]
    base_prompts = [p for _, p in base]
    plain = TAG.sub("", cur_line)
    toks = tokens(plain)
    cur_words = [w for w, _, _ in toks]

    attr = [None] * len(cur_words)
    matcher = SequenceMatcher(None, base_tokens, cur_words, autojunk=False)
    opcodes = matcher.get_opcodes()
    for op, i1, i2, j1, j2 in opcodes:
        if op == "equal" and (j2 - j1) >= MIN_RUN:
            for k in range(j2 - j1):
                attr[j1 + k] = base_prompts[i1 + k]
    # When in doubt, assign to Johannes: trim one word where an unchanged run
    # meets an edit, so coincidental boundary matches are not claimed as AI.
    for op, i1, i2, j1, j2 in opcodes:
        if op == "equal" and (j2 - j1) >= MIN_RUN:
            if j1 > 0 and attr[j1 - 1] is None:
                attr[j1] = None
            if j2 < len(attr) and attr[j2] is None:
                attr[j2 - 1] = None

    out = []
    prev_attr = None
    prev_end = 0
    for idx, (word, start, end) in enumerate(toks):
        out.append(plain[prev_end:start])
        here = attr[idx]
        if here != prev_attr:
            if prev_attr is not None:
                out.append("[[/AI]]")
            if here is not None:
                out.append("[[AI:%d]]" % here)
        out.append(word)
        prev_attr = here
        prev_end = end
    if prev_attr is not None:
        out.append("[[/AI]]")
    out.append(plain[prev_end:])
    return "".join(out)


def main():
    current = SRC.read_text(encoding="utf-8")
    prefix, body_cur = split_prefix(current)
    base = subprocess.run(
        ["git", "show", "HEAD:essay.md"], cwd=ROOT, capture_output=True, text=True
    ).stdout
    _, body_base = split_prefix(base)

    base_lines = body_base.split("\n")
    cur_lines = body_cur.split("\n")

    matcher = SequenceMatcher(None, base_lines, cur_lines, autojunk=False)
    out_lines = []
    for op, i1, i2, j1, j2 in matcher.get_opcodes():
        if op == "equal":
            out_lines.extend(cur_lines[j1:j2])
        elif op == "replace":
            block = base_lines[i1:i2]
            for k, cl in enumerate(cur_lines[j1:j2]):
                bl = block[k] if k < len(block) else ""
                out_lines.append(retag_line(bl, cl))
        elif op == "insert":
            out_lines.extend(TAG.sub("", cl) for cl in cur_lines[j1:j2])

    result = prefix + "\n".join(out_lines)
    if "--write" in sys.argv:
        SRC.write_text(result, encoding="utf-8")
        print("Re-tagged essay.md.")
    else:
        sys.stdout.write(result)


if __name__ == "__main__":
    main()
