#!/usr/bin/env python3
"""Turn essay.md (the master text) into the reader-friendly outputs.

Nothing here is edited by hand. Run this after any change to essay.md or
PROMPTS.md and it rebuilds docs/index.html and docs/print.html.
"""

import html
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "essay.md"
PROMPTS = ROOT / "PROMPTS.md"
DOCS = ROOT / "docs"
REPO_URL = "https://github.com/johannesnorbertwolf/academic-skills-essay-a"

AI_OPEN = re.compile(r"\[\[AI:(\d+)\]\]")
AI_CLOSE = "[[/AI]]"


def parse_prompts(text):
    prompts = {}
    parts = re.split(r"^##\s*Prompt\s+(\d+)\s*$", text, flags=re.M)
    for i in range(1, len(parts) - 1, 2):
        num = int(parts[i])
        body = parts[i + 1]
        snippet = ""
        for line in body.splitlines():
            line = line.strip().lstrip(">").strip()
            if line and not line.startswith("**"):
                snippet = line
                break
        prompts[num] = snippet
    return prompts


def emphasise(text):
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<em>\1</em>", text)
    return text


def plain(text):
    if text == "":
        return ""
    return '<span class="human">' + emphasise(html.escape(text)) + "</span>"


def ai_span(text, num, prompts):
    tip = "Written by the AI \u2014 prompt %d" % num
    snippet = prompts.get(num, "")
    if snippet:
        tip += ': "%s"' % (snippet[:120] + ("\u2026" if len(snippet) > 120 else ""))
    return (
        '<span class="ai" data-prompt="%d" title="%s">%s</span>'
        % (num, html.escape(tip, quote=True), emphasise(html.escape(text)))
    )


def inline(text, prompts):
    out = []
    human_words = ai_words = 0
    pos = 0
    for m in AI_OPEN.finditer(text):
        before = text[pos:m.start()]
        out.append(plain(before))
        human_words += len(before.split())
        close = text.find(AI_CLOSE, m.end())
        num = int(m.group(1))
        if close == -1:
            body = text[m.end():]
            out.append(ai_span(body, num, prompts))
            ai_words += len(body.split())
            pos = len(text)
            break
        body = text[m.end():close]
        out.append(ai_span(body, num, prompts))
        ai_words += len(body.split())
        pos = close + len(AI_CLOSE)
    tail = text[pos:]
    out.append(plain(tail))
    human_words += len(tail.split())
    return "".join(out), human_words, ai_words


def render(md, prompts):
    lines = md.split("\n")
    parts = []
    human_words = ai_words = 0
    i = 0
    n = len(lines)
    while i < n:
        s = lines[i].strip()
        if s == "":
            i += 1
            continue
        if re.match(r"^---+$", s):
            parts.append("<hr>")
            i += 1
            continue
        m = re.match(r"^(#{1,6})\s+(.*)$", s)
        if m:
            inner, h, a = inline(m.group(2), prompts)
            human_words += h
            ai_words += a
            parts.append("<h%d>%s</h%d>" % (len(m.group(1)), inner, len(m.group(1))))
            i += 1
            continue
        if s.startswith(">"):
            block = []
            while i < n and lines[i].strip().startswith(">"):
                block.append(lines[i].strip()[1:].strip())
                i += 1
            inner, h, a = inline(" ".join(block), prompts)
            human_words += h
            ai_words += a
            parts.append("<blockquote><p>%s</p></blockquote>" % inner)
            continue
        if re.match(r"^[-*]\s+", s):
            items = []
            while i < n and re.match(r"^[-*]\s+", lines[i].strip()):
                item = re.sub(r"^[-*]\s+", "", lines[i].strip())
                inner, h, a = inline(item, prompts)
                human_words += h
                ai_words += a
                items.append("<li>%s</li>" % inner)
                i += 1
            parts.append("<ul>%s</ul>" % "".join(items))
            continue
        if re.match(r"^\d+\.\s+", s):
            items = []
            while i < n and re.match(r"^\d+\.\s+", lines[i].strip()):
                item = re.sub(r"^\d+\.\s+", "", lines[i].strip())
                inner, h, a = inline(item, prompts)
                human_words += h
                ai_words += a
                items.append("<li>%s</li>" % inner)
                i += 1
            parts.append("<ol>%s</ol>" % "".join(items))
            continue
        para = []
        while i < n:
            t = lines[i].strip()
            if (
                t == ""
                or t.startswith("#")
                or t.startswith(">")
                or re.match(r"^[-*]\s+", t)
                or re.match(r"^\d+\.\s+", t)
                or re.match(r"^---+$", t)
            ):
                break
            para.append(t)
            i += 1
        inner, h, a = inline(" ".join(para), prompts)
        human_words += h
        ai_words += a
        parts.append("<p>%s</p>" % inner)
    return "\n".join(parts), human_words, ai_words


STYLE = """
:root{--human-bg:#e6f6e6;--human-bg-hover:#d3efd3;--ai-bg:#e3f0ff;--ai-bg-hover:#cfe4ff;
--ai-line:#2f6fd0;--ink:#1a1a1a;}
*{box-sizing:border-box;}
body{margin:0;font-family:Georgia,'Times New Roman',serif;color:var(--ink);line-height:1.6;background:#fafafa;}
header{background:#fff;border-bottom:1px solid #ddd;padding:1.5rem 1.5rem 1rem;}
header h1{font-size:1.3rem;margin:0 0 .3rem;font-family:system-ui,sans-serif;}
.lede{margin:0 0 .8rem;color:#444;max-width:60rem;font-family:system-ui,sans-serif;font-size:.92rem;}
.legend{display:flex;flex-wrap:wrap;gap:1.2rem;margin:.6rem 0;font-family:system-ui,sans-serif;font-size:.9rem;}
.legend .item{display:inline-flex;align-items:center;gap:.45rem;}
.swatch{width:1.1rem;height:1.1rem;display:inline-block;border-radius:3px;}
.swatch.human{background:var(--human-bg);border:1px solid #bcd9bc;}
.swatch.ai{background:var(--ai-bg);border:1px solid var(--ai-line);border-bottom:2px dashed var(--ai-line);}
.summary{font-family:system-ui,sans-serif;font-size:.9rem;color:#333;background:#f2f4f7;
border:1px solid #e0e4ea;border-radius:6px;padding:.6rem .8rem;display:inline-block;margin-top:.4rem;}
main{max-width:46rem;margin:2rem auto;background:#fff;padding:2rem 2.2rem 3rem;border:1px solid #e6e6e6;border-radius:8px;}
main h1,main h2,main h3{font-family:system-ui,sans-serif;line-height:1.25;}
main h1{font-size:1.7rem;margin-top:0;}
main h2{font-size:1.25rem;margin-top:2rem;border-bottom:1px solid #eee;padding-bottom:.2rem;}
main p{margin:0 0 1rem;}
.human{background:var(--human-bg);border-radius:2px;}
.ai{background:var(--ai-bg);border-radius:2px;border-bottom:2px dashed var(--ai-line);cursor:help;}
.ai:hover{background:var(--ai-bg-hover);}
footer{max-width:46rem;margin:0 auto 3rem;padding:0 2.2rem;font-family:system-ui,sans-serif;
font-size:.8rem;color:#666;}
footer a{color:#2f6fd0;}
@media print{
 body{background:#fff;}
 header{border-bottom:1px solid #000;}
 main{border:none;margin:0;padding:0;max-width:none;}
 footer{max-width:none;padding:0;}
 .human,.ai{-webkit-print-color-adjust:exact;print-color-adjust:exact;}
}
"""


def page(title, mode, body, human_words, ai_words, prompts):
    total = human_words + ai_words
    if total:
        hp = round(100 * human_words / total)
        ap = 100 - hp
        summary = (
            "%d words in total &middot; <strong>%d (%d%%) written by Johannes Wolf</strong> "
            "&middot; %d (%d%%) written by the AI" % (total, human_words, hp, ai_words, ap)
        )
    else:
        summary = "No text yet."
    note = (
        "<p class=\"lede\"><strong>Printable version.</strong> Print this page and enable "
        "&ldquo;background graphics&rdquo; so the colours are kept. Light green is the human "
        "author; light blue with a dashed underline is the AI.</p>"
        if mode == "print"
        else ""
    )
    hover = (
        ""
        if mode == "print"
        else " Hover any blue passage to see which prompt produced it."
    )
    return """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%s</title>
<style>%s</style>
</head>
<body>
<header>
<h1>Academic Skills Essay A &mdash; who wrote what</h1>
<p class="lede">Every word is labelled. This page is generated from the master text
(<code>essay.md</code>) and cannot disagree with it.%s</p>
%s
<div class="legend">
<span class="item"><span class="swatch human"></span> Written by Johannes Wolf</span>
<span class="item"><span class="swatch ai"></span> Written by the AI</span>
</div>
<p class="summary">%s</p>
</header>
<main>
%s
</main>
<footer>
<p>Generated from the master text on %s. Source, full prompt log and history:
<a href="%s">%s</a></p>
</footer>
</body>
</html>
""" % (
        html.escape(title),
        STYLE,
        hover,
        note,
        summary,
        body,
        date.today().isoformat(),
        REPO_URL,
        REPO_URL,
    )


def main():
    md = SRC.read_text(encoding="utf-8")
    md = re.sub(r"<!--.*?-->", "", md, flags=re.S)
    prompts = parse_prompts(PROMPTS.read_text(encoding="utf-8")) if PROMPTS.exists() else {}
    body, human_words, ai_words = render(md, prompts)
    DOCS.mkdir(exist_ok=True)
    (DOCS / "index.html").write_text(
        page("Academic Skills Essay A", "screen", body, human_words, ai_words, prompts),
        encoding="utf-8",
    )
    (DOCS / "print.html").write_text(
        page("Academic Skills Essay A (print)", "print", body, human_words, ai_words, prompts),
        encoding="utf-8",
    )
    print("Built docs/index.html and docs/print.html: %d human words, %d AI words."
          % (human_words, ai_words))


if __name__ == "__main__":
    main()
