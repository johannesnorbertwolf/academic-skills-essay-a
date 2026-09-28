#!/usr/bin/env python3
"""Build every reader-facing output from the master text (essay.md).

Produces:
  docs/index.html   colour-coded, word-level attribution (web)
  docs/print.html   same, for printing
  docs/essay.pdf    clean APA 7 PDF for submission

Run this after any change to essay.md, PROMPTS.md or refs.bib.
"""

import html
import re
import shutil
import subprocess
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "essay.md"
PROMPTS = ROOT / "PROMPTS.md"
REFS = ROOT / "refs.bib"
DOCS = ROOT / "docs"
BUILD = ROOT / ".build"
DEFAULT_REPO = "https://github.com/johannesnorbertwolf/academic-skills-essay-a"

AI_OPEN = re.compile(r"\[\[AI:(\d+)\]\]")
AI_CLOSE = "[[/AI]]"


def split_front_matter(text):
    m = re.match(r"\s*---\s*\n(.*?)\n---\s*\n?", text, re.S)
    if not m:
        return {}, text
    meta = {}
    for line in m.group(1).splitlines():
        line = line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        meta[key.strip().lower()] = value.strip().strip('"').strip("'")
    return meta, text[m.end():]


def parse_prompts(text):
    prompts = {}
    parts = re.split(r"^##\s*Prompt\s+(\d+)\s*$", text, flags=re.M)
    for i in range(1, len(parts) - 1, 2):
        num = int(parts[i])
        snippet = ""
        for line in parts[i + 1].splitlines():
            line = line.strip()
            if line.startswith(">"):
                snippet = line.lstrip(">").strip()
                break
        prompts[num] = snippet
    return prompts


# --------------------------------------------------------------------- HTML

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


def inline_html(text, prompts):
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


def render_html(md, prompts):
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
            inner, h, a = inline_html(m.group(2), prompts)
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
            inner, h, a = inline_html(" ".join(block), prompts)
            human_words += h
            ai_words += a
            parts.append("<blockquote><p>%s</p></blockquote>" % inner)
            continue
        if re.match(r"^[-*]\s+", s):
            items = []
            while i < n and re.match(r"^[-*]\s+", lines[i].strip()):
                item = re.sub(r"^[-*]\s+", "", lines[i].strip())
                inner, h, a = inline_html(item, prompts)
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
                inner, h, a = inline_html(item, prompts)
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
        inner, h, a = inline_html(" ".join(para), prompts)
        human_words += h
        ai_words += a
        parts.append("<p>%s</p>" % inner)
    return "\n".join(parts), human_words, ai_words


def strip_ai_tags(text):
    return re.sub(r"\s+", " ", AI_OPEN.sub(" ", text).replace(AI_CLOSE, " "))


APPENDIX_RE = re.compile(r"\b(appendix|reflection)\b|ai (usage|use)|use of ai", re.I)


def count_essay_words(md):
    """Count the words that count toward the limit.

    Headings are not counted, and neither is anything from the first
    appendix/reflection/AI-statement heading onward. Everything before that is
    the essay body.
    """
    lines = md.split("\n")
    count = 0
    in_appendix = False
    i = 0
    n = len(lines)
    while i < n:
        s = lines[i].strip()
        if s == "" or re.match(r"^---+$", s):
            i += 1
            continue
        m = re.match(r"^(#{1,6})\s+(.*)$", s)
        if m:
            if APPENDIX_RE.search(m.group(2)):
                in_appendix = True
            i += 1
            continue
        if s.startswith(">"):
            block = []
            while i < n and lines[i].strip().startswith(">"):
                block.append(lines[i].strip()[1:].strip())
                i += 1
            if not in_appendix:
                count += len(strip_ai_tags(" ".join(block)).split())
            continue
        if re.match(r"^[-*]\s+", s) or re.match(r"^\d+\.\s+", s):
            while i < n and (
                re.match(r"^[-*]\s+", lines[i].strip())
                or re.match(r"^\d+\.\s+", lines[i].strip())
            ):
                item = re.sub(r"^[-*]\s+", "", lines[i].strip())
                item = re.sub(r"^\d+\.\s+", "", item)
                if not in_appendix:
                    count += len(strip_ai_tags(item).split())
                i += 1
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
        if not in_appendix:
            count += len(strip_ai_tags(" ".join(para)).split())
    return count


def word_limits(meta):
    def as_int(key, default):
        try:
            return int(meta.get(key, default))
        except (ValueError, TypeError):
            return default

    return as_int("word_min", 700), as_int("word_max", 1000), as_int("word_target", 800)


def word_state(count, lo, hi):
    if count < lo:
        return "UNDER the minimum"
    if count > hi:
        return "OVER the maximum"
    return "within the required range"


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


def html_page(meta, mode, body, human_words, ai_words, essay_words):
    title = meta.get("title", "Essay")
    repo = meta.get("repo", DEFAULT_REPO)
    total = human_words + ai_words
    if total:
        hp = round(100 * human_words / total)
        summary = (
            "Whole document: %d words &middot; <strong>%d (%d%%) written by Johannes Wolf</strong> "
            "&middot; %d (%d%%) written by the AI" % (total, human_words, hp, ai_words, 100 - hp)
        )
    else:
        summary = "No text yet."
    lo, hi, target = word_limits(meta)
    state = word_state(essay_words, lo, hi)
    essay_line = (
        "Essay body (counted toward the word limit): <strong>%d words</strong> "
        "&middot; target %d, required %d&ndash;%d &middot; <strong>%s</strong>"
        % (essay_words, target, lo, hi, state)
    )
    note = (
        '<p class="lede"><strong>Printable version.</strong> Print this page and enable '
        "&ldquo;background graphics&rdquo; so the colours are kept. Light green is the human "
        "author; light blue with a dashed underline is the AI.</p>"
        if mode == "print"
        else ""
    )
    hover = "" if mode == "print" else " Hover any blue passage to see which prompt produced it."
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
<h1>%s &mdash; who wrote what</h1>
<p class="lede">Every word is labelled. This page is generated from the master text
(<code>essay.md</code>) and cannot disagree with it.%s</p>
%s
<div class="legend">
<span class="item"><span class="swatch human"></span> Written by Johannes Wolf</span>
<span class="item"><span class="swatch ai"></span> Written by the AI</span>
</div>
<p class="summary">%s</p>
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
        html.escape(title),
        hover,
        note,
        summary,
        essay_line,
        body,
        date.today().isoformat(),
        html.escape(repo, quote=True),
        html.escape(repo),
    )


# -------------------------------------------------------------------- Typst

TYPST_SPECIAL = set("\\#$~*_`<>@[]")


def tesc(text):
    return "".join(("\\" + c) if c in TYPST_SPECIAL else c for c in text)


def fmt_chunk(text):
    pattern = re.compile(r"\*\*(.+?)\*\*|\*(.+?)\*|\[@([^\]]+)\]", re.S)
    pieces = []
    pos = 0
    for m in pattern.finditer(text):
        pieces.append(("text", text[pos:m.start()]))
        if m.group(1) is not None:
            pieces.append(("bold", m.group(1)))
        elif m.group(2) is not None:
            pieces.append(("italic", m.group(2)))
        else:
            pieces.append(("cite", m.group(3)))
        pos = m.end()
    pieces.append(("text", text[pos:]))
    out = []
    for kind, value in pieces:
        if kind == "text":
            out.append(tesc(value))
        elif kind == "bold":
            out.append("*" + tesc(value) + "*")
        elif kind == "italic":
            out.append("_" + tesc(value) + "_")
        else:
            keys = [k for k in re.findall(r"[\w:.\-]+", value) if k]
            out.append(" ".join("#cite(<%s>)" % k for k in keys))
    return "".join(out)


def inline_typst(text):
    text = AI_OPEN.sub(" ", text).replace(AI_CLOSE, " ")
    text = re.sub(r"[ \t]+", " ", text)
    return fmt_chunk(text)


def render_typst_body(md):
    lines = md.split("\n")
    out = []
    i = 0
    n = len(lines)
    while i < n:
        s = lines[i].strip()
        if s == "":
            i += 1
            continue
        if re.match(r"^---+$", s):
            out.append("#line(length: 100%)")
            i += 1
            continue
        m = re.match(r"^(#{1,6})\s+(.*)$", s)
        if m:
            out.append("=" * len(m.group(1)) + " " + inline_typst(m.group(2)))
            i += 1
            continue
        if s.startswith(">"):
            block = []
            while i < n and lines[i].strip().startswith(">"):
                block.append(lines[i].strip()[1:].strip())
                i += 1
            out.append("#block(inset: (left: 0.5in))[%s]" % inline_typst(" ".join(block)))
            continue
        if re.match(r"^[-*]\s+", s):
            items = []
            while i < n and re.match(r"^[-*]\s+", lines[i].strip()):
                item = re.sub(r"^[-*]\s+", "", lines[i].strip())
                items.append("- " + inline_typst(item))
                i += 1
            out.append("\n".join(items))
            continue
        if re.match(r"^\d+\.\s+", s):
            items = []
            while i < n and re.match(r"^\d+\.\s+", lines[i].strip()):
                item = re.sub(r"^\d+\.\s+", "", lines[i].strip())
                items.append("+ " + inline_typst(item))
                i += 1
            out.append("\n".join(items))
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
        text = inline_typst(" ".join(para))
        if text[:1] in ("-", "+", "/", "="):
            text = "\\" + text
        out.append(text)
    return "\n\n".join(out)


TYPST_TEMPLATE = r'''#set page(
  paper: "@@PAPERSIZE@@",
  margin: 1in,
  numbering: none,
  header: context {
    set text(font: "@@FONT@@", size: 12pt)
    align(right, counter(page).display("1"))
  },
)
#set text(font: "@@FONT@@", size: 12pt, lang: "en")
#set par(leading: 1em, first-line-indent: (amount: 0.5in, all: true), justify: false)

#show heading.where(level: 1): it => block(above: 1.2em, below: 0.6em, align(center, text(weight: "bold", it.body)))
#show heading.where(level: 2): it => block(above: 1.2em, below: 0.6em, text(weight: "bold", it.body))
#show heading.where(level: 3): it => block(above: 1.2em, below: 0.6em, text(weight: "bold", style: "italic", it.body))

#show bibliography: set par(first-line-indent: (amount: 0.5in, all: true), hanging-indent: 0.5in)

// ------------------------------------------------- title page
#v(2.5in)
#align(center)[#text(weight: "bold")[@@TITLE@@]]
#v(1.5em)
#align(center)[
  @@STACK@@
]
#v(1fr)
#align(center)[#text(size: 10pt)[Transparency record: every word is attributed and every prompt is logged at @@REPO@@]]

#pagebreak()

// ------------------------------------------------- body
#align(center)[#text(weight: "bold")[@@TITLE@@]]

@@BODY@@

@@REFERENCES@@
'''

PAPER_SIZES = {"a4": "a4", "letter": "us-letter", "us-letter": "us-letter", "usletter": "us-letter"}


def typst_document(meta, body, has_cites):
    stack_lines = [
        meta.get("author", ""),
        meta.get("affiliation", ""),
        meta.get("course", ""),
        meta.get("instructor", ""),
        meta.get("date", ""),
    ]
    stack = " \\\n  ".join(tesc(x) for x in stack_lines if x)
    references = ""
    if has_cites:
        references = (
            "#pagebreak()\n"
            "#align(center)[#text(weight: \"bold\")[References]]\n\n"
            '#bibliography("../refs.bib", style: "apa")'
        )
    doc = TYPST_TEMPLATE
    replacements = {
        "@@PAPERSIZE@@": PAPER_SIZES.get(meta.get("papersize", "a4").lower(), "a4"),
        "@@FONT@@": meta.get("font", "Times New Roman"),
        "@@TITLE@@": tesc(meta.get("title", "Essay")),
        "@@STACK@@": stack,
        "@@REPO@@": tesc(meta.get("repo", DEFAULT_REPO)),
        "@@BODY@@": body,
        "@@REFERENCES@@": references,
    }
    for key, value in replacements.items():
        doc = doc.replace(key, value)
    return doc


def build_pdf(meta, md):
    if shutil.which("typst") is None:
        print("Typst not found; skipping the APA PDF.")
        return
    body = render_typst_body(md)
    has_cites = "#cite(" in body and REFS.exists() and bool(REFS.read_text(encoding="utf-8").strip())
    BUILD.mkdir(exist_ok=True)
    DOCS.mkdir(exist_ok=True)
    typ_path = BUILD / "paper.typ"
    typ_path.write_text(typst_document(meta, body, has_cites), encoding="utf-8")
    out = DOCS / "essay.pdf"
    result = subprocess.run(
        ["typst", "compile", "--root", str(ROOT), str(typ_path), str(out)],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print("Typst could not build the PDF:")
        print(result.stderr.strip())
    else:
        if result.stderr.strip():
            print(result.stderr.strip())
        print("Built docs/essay.pdf")


def write_wordcount(meta, count):
    lo, hi, target = word_limits(meta)
    state = word_state(count, lo, hi)
    lines = [
        "# Word count",
        "",
        "The essay body only: the main text. Headings are not counted, and neither",
        "is anything from the appendix onward (the reflection and the statement on AI",
        "use). The reference list is generated separately and is not counted either.",
        "This matches the assignment's rules.",
        "",
        "- **Current essay body: %d words**" % count,
        "- Target: about %d words" % target,
        "- Hard requirement: %d to %d words" % (lo, hi),
        "- Status: **%s**" % state,
        "",
        "Generated by `build.py` on %s." % date.today().isoformat(),
        "",
    ]
    (ROOT / "WORDCOUNT.md").write_text("\n".join(lines), encoding="utf-8")


def main():
    raw = SRC.read_text(encoding="utf-8")
    meta, body_md = split_front_matter(raw)
    md = re.sub(r"<!--.*?-->", "", body_md, flags=re.S)
    prompts = parse_prompts(PROMPTS.read_text(encoding="utf-8")) if PROMPTS.exists() else {}
    body, human_words, ai_words = render_html(md, prompts)
    essay_words = count_essay_words(md)
    lo, hi, target = word_limits(meta)
    DOCS.mkdir(exist_ok=True)
    (DOCS / "index.html").write_text(
        html_page(meta, "screen", body, human_words, ai_words, essay_words), encoding="utf-8"
    )
    (DOCS / "print.html").write_text(
        html_page(meta, "print", body, human_words, ai_words, essay_words), encoding="utf-8"
    )
    write_wordcount(meta, essay_words)
    print(
        "Built docs/index.html and docs/print.html: %d human words, %d AI words."
        % (human_words, ai_words)
    )
    print(
        "Essay body: %d words (target %d, required %d-%d) \u2014 %s."
        % (essay_words, target, lo, hi, word_state(essay_words, lo, hi))
    )
    build_pdf(meta, md)


if __name__ == "__main__":
    main()
