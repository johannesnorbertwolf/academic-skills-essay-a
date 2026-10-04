#!/usr/bin/env python3
"""Build every reader-facing output from the master text (essay.md).

Produces:
  docs/index.html   color-coded, word-level attribution (web)
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
        block = re.search(r"\*\*Prompt sent:\*\*\s*\n((?:>.*(?:\n|$))+)", parts[i + 1])
        snippet = ""
        if block:
            lines = [ln[1:].strip() for ln in block.group(1).splitlines()]
            snippet = "\n".join(lines).strip()
        prompts[num] = snippet
    return prompts


_APA_REFS = {}


def load_refs(path):
    """Return {key: (author_field, year)} from refs.bib, for rendering citations."""
    refs = {}
    if not path.exists():
        return refs
    raw = path.read_text(encoding="utf-8")
    lines = [ln for ln in raw.splitlines() if not ln.lstrip().startswith("%")]
    text = "\n".join(lines)
    for m in re.finditer(r"@\w+\s*\{\s*([^,\s]+)\s*,(.*?)\n\}", text, re.S):
        key, body = m.group(1), m.group(2)

        def field(name):
            fm = re.search(r"\b" + name + r"\s*=\s*\{(.*?)\}", body, re.S)
            return fm.group(1).strip() if fm else ""

        refs[key] = (field("author"), field("year"))
    return refs


def apa_author(author_field):
    names = [n.strip() for n in re.split(r"\band\b", author_field) if n.strip()]
    surnames = []
    for n in names:
        surnames.append(n.split(",")[0].strip() if "," in n else n.split()[-1])
    if not surnames:
        return ""
    if len(surnames) == 1:
        return surnames[0]
    if len(surnames) == 2:
        return surnames[0] + " & " + surnames[1]
    return surnames[0] + " et al."


def apa_cite(key, refs, prose):
    authors, year = refs.get(key, ("", ""))
    name = apa_author(authors)
    if prose:
        return "%s (%s)" % (name, year)
    return "%s, %s" % (name, year)


def render_cites_html(text, refs):
    """Replace [@key] (parenthetical) and @key (narrative) with APA text for the page."""

    def parenthetical(m):
        keys = [k for k in re.findall(r"[\w:.\-]+", m.group(1)) if k]
        return "(" + "; ".join(apa_cite(k, refs, False) for k in keys) + ")"

    text = re.sub(r"\[@([^\]]+)\]", parenthetical, text)
    text = re.sub(r"@([A-Za-z][A-Za-z0-9_\-]*)", lambda m: apa_cite(m.group(1), refs, True), text)
    return text


# --------------------------------------------------------------------- HTML

def emphasize(text):
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<em>\1</em>", text)
    return text


def inline_text(text):
    return emphasize(html.escape(render_cites_html(text, _APA_REFS)))


def plain(text):
    if text == "":
        return ""
    return '<span class="human">' + inline_text(text) + "</span>"


def ai_span(text, num, prompts):
    prompt = prompts.get(num, "").strip()
    tip_body = html.escape(prompt).replace("\n", "<br>") if prompt else "(prompt text not available)"
    tip = (
        '<span class="tip"><span class="tip-h">Prompt %d &mdash; click to read the full exchange'
        "</span>%s</span>" % (num, tip_body)
    )
    return (
        '<a class="ai" href="prompts.html#prompt-%d" data-prompt="%d">%s%s</a>'
        % (num, num, inline_text(text), tip)
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


def slugify(text):
    text = html.unescape(re.sub(r"<[^>]+>", "", text)).lower()
    text = re.sub(r"[^\w\s-]", "", text)
    return re.sub(r"[\s_]+", "-", text).strip("-")


def md_inline(text):
    text = html.escape(text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\[([^\]]+)\]\((https?://[^\s)]+)\)", r'<a href="\2">\1</a>', text)
    text = re.sub(r"&lt;(https?://[^\s&]+)&gt;", r'<a href="\1">\1</a>', text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<em>\1</em>", text)
    return text


def render_markdown(md):
    """Render the plain Markdown of the record files to HTML for the site."""
    lines = md.split("\n")
    out = []
    i, n = 0, len(lines)
    while i < n:
        s = lines[i].strip()
        if s == "":
            i += 1
            continue
        if re.match(r"^(?:-{3,}|\*{3,}|_{3,})$", s):
            out.append("<hr>")
            i += 1
            continue
        m = re.match(r"^(#{1,6})\s+(.*)$", s)
        if m:
            lvl = len(m.group(1))
            out.append(
                '<h%d id="%s">%s</h%d>' % (lvl, slugify(m.group(2)), md_inline(m.group(2)), lvl)
            )
            i += 1
            continue
        if s.startswith("|") and i + 1 < n and re.match(r"^\s*\|?\s*:?-{2,}", lines[i + 1]):
            header = [c.strip() for c in s.strip("|").split("|")]
            i += 2
            rows = []
            while i < n and lines[i].strip().startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            thead = "".join("<th>%s</th>" % md_inline(c) for c in header)
            body = "".join(
                "<tr>%s</tr>" % "".join("<td>%s</td>" % md_inline(c) for c in r) for r in rows
            )
            out.append(
                '<div class="table-wrap"><table><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>'
                % (thead, body)
            )
            continue
        if s.startswith(">"):
            paras, cur = [], []
            while i < n and lines[i].strip().startswith(">"):
                content = lines[i].strip()[1:].strip()
                if content == "":
                    if cur:
                        paras.append(" ".join(cur))
                        cur = []
                else:
                    cur.append(content)
                i += 1
            if cur:
                paras.append(" ".join(cur))
            out.append(
                "<blockquote>%s</blockquote>" % "".join("<p>%s</p>" % md_inline(p) for p in paras)
            )
            continue
        if re.match(r"^[-*]\s+", s):
            items = []
            while i < n and re.match(r"^[-*]\s+", lines[i].strip()):
                items.append(md_inline(re.sub(r"^[-*]\s+", "", lines[i].strip())))
                i += 1
            out.append("<ul>%s</ul>" % "".join("<li>%s</li>" % it for it in items))
            continue
        if re.match(r"^\d+\.\s+", s):
            items = []
            while i < n and re.match(r"^\d+\.\s+", lines[i].strip()):
                items.append(md_inline(re.sub(r"^\d+\.\s+", "", lines[i].strip())))
                i += 1
            out.append("<ol>%s</ol>" % "".join("<li>%s</li>" % it for it in items))
            continue
        para = []
        while i < n:
            t = lines[i].strip()
            if (
                t == ""
                or t.startswith("#")
                or t.startswith(">")
                or t.startswith("|")
                or re.match(r"^[-*]\s+", t)
                or re.match(r"^\d+\.\s+", t)
                or re.match(r"^(?:-{3,}|\*{3,}|_{3,})$", t)
            ):
                break
            para.append(t)
            i += 1
        out.append("<p>%s</p>" % md_inline(" ".join(para)))
    return "\n".join(out)


def strip_ai_tags(text):
    return re.sub(r"\s+", " ", AI_OPEN.sub(" ", text).replace(AI_CLOSE, " "))


APPENDIX_RE = re.compile(r"\b(appendix|reflection|disclosure)\b|ai (usage|use)|use of ai", re.I)


def split_appendix(md):
    """Split the text at the first appendix/reflection/disclosure heading."""
    lines = md.split("\n")
    for i, line in enumerate(lines):
        m = re.match(r"^(#{1,6})\s+(.*)$", line.strip())
        if m and APPENDIX_RE.search(m.group(2)):
            return "\n".join(lines[:i]), "\n".join(lines[i:])
    return md, ""


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


def author_counts(text):
    """Return (human_words, ai_words) for one block of inline text."""
    human = ai = 0
    pos = 0
    for m in AI_OPEN.finditer(text):
        human += len(text[pos:m.start()].split())
        close = text.find(AI_CLOSE, m.end())
        if close == -1:
            ai += len(text[m.end():].split())
            return human, ai
        ai += len(text[m.end():close].split())
        pos = close + len(AI_CLOSE)
    human += len(text[pos:].split())
    return human, ai


def count_attribution(md):
    """Count human/AI words in the essay text only.

    This is the share that matters: headings are excluded, and so is everything
    from the first appendix/reflection/AI-statement heading onward.
    """
    lines = md.split("\n")
    human = ai = 0
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
                h, a = author_counts(" ".join(block))
                human += h
                ai += a
            continue
        if re.match(r"^[-*]\s+", s) or re.match(r"^\d+\.\s+", s):
            while i < n and (
                re.match(r"^[-*]\s+", lines[i].strip())
                or re.match(r"^\d+\.\s+", lines[i].strip())
            ):
                item = re.sub(r"^[-*]\s+", "", lines[i].strip())
                item = re.sub(r"^\d+\.\s+", "", item)
                if not in_appendix:
                    h, a = author_counts(item)
                    human += h
                    ai += a
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
            h, a = author_counts(" ".join(para))
            human += h
            ai += a
    return human, ai


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
--ai-line:#2f6fd0;--ink:#1a1a1a;--link:#2f6fd0;}
*{box-sizing:border-box;}
body{margin:0;font-family:Georgia,'Times New Roman',serif;color:var(--ink);line-height:1.6;background:#fafafa;}
nav.top{background:#fff;border-bottom:1px solid #ddd;padding:.5rem 1.5rem;font-family:system-ui,sans-serif;font-size:.85rem;}
nav.top ul{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:.3rem 1.1rem;}
nav.top a{color:var(--link);text-decoration:none;}
nav.top a:hover{text-decoration:underline;}
nav.top a[aria-current=page]{color:#111;font-weight:600;}
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
.explore{font-family:system-ui,sans-serif;font-size:.92rem;color:#1b3a5b;background:#eef5ff;
border:1px solid #cfe1fb;border-radius:8px;padding:.7rem .9rem;margin:.2rem 0 .7rem;max-width:60rem;}
.explore a{color:var(--link);font-weight:600;}
main{max-width:46rem;margin:2rem auto;background:#fff;padding:2rem 2.2rem 3rem;border:1px solid #e6e6e6;border-radius:8px;}
main h1,main h2,main h3{font-family:system-ui,sans-serif;line-height:1.25;}
main h1{font-size:1.7rem;margin-top:0;}
main h2{font-size:1.25rem;margin-top:2rem;border-bottom:1px solid #eee;padding-bottom:.2rem;}
main p{margin:0 0 1rem;}
.human{background:var(--human-bg);border-radius:2px;}
.ai{background:var(--ai-bg);border-radius:2px;border-bottom:2px dashed var(--ai-line);cursor:pointer;
color:inherit;text-decoration:none;position:relative;}
.ai:hover,.ai:focus{background:var(--ai-bg-hover);}
.ai .tip{display:none;position:absolute;left:0;top:1.7em;z-index:60;width:min(32rem,86vw);
background:#141821;color:#f5f5f5;padding:.7rem .85rem;border-radius:8px;font-family:system-ui,sans-serif;
font-size:.82rem;line-height:1.45;box-shadow:0 10px 30px rgba(0,0,0,.3);white-space:normal;text-align:left;}
.ai .tip .tip-h{display:block;font-weight:600;color:#9dc2f0;margin-bottom:.35rem;}
.ai:hover .tip,.ai:focus .tip{display:block;}
.record blockquote{border-left:3px solid #cdd7e5;background:#f7f9fc;margin:.6rem 0;
padding:.5rem .9rem;border-radius:0 6px 6px 0;font-size:.95rem;}
.record blockquote p{margin:.35rem 0;}
.table-wrap{overflow-x:auto;margin:1rem 0;}
.record table{border-collapse:collapse;width:100%;font-family:system-ui,sans-serif;font-size:.85rem;margin:0;}
.record th,.record td{border:1px solid #dde3ec;padding:.4rem .6rem;text-align:left;vertical-align:top;overflow-wrap:anywhere;}
.record th{background:#f2f4f7;}
.record code,code{background:#eef1f6;padding:.05rem .3rem;border-radius:3px;font-size:.9em;}
.record hr{border:none;border-top:1px solid #e0e4ea;margin:2rem 0;}
.record ul,.record ol{margin:0 0 1rem;padding-left:1.4rem;}
.record li{margin:.2rem 0;}
footer{max-width:46rem;margin:0 auto 3rem;padding:0 2.2rem;font-family:system-ui,sans-serif;
font-size:.8rem;color:#666;}
footer a{color:var(--link);}
@media print{
 body{background:#fff;}
 nav.top{display:none;}
 header{border-bottom:1px solid #000;}
 main{border:none;margin:0;padding:0;max-width:none;}
 footer{max-width:none;padding:0;}
 .human,.ai{-webkit-print-color-adjust:exact;print-color-adjust:exact;}
 .ai .tip{display:none !important;}
}
"""


NAV = [
    ("index", "The essay", "index.html"),
    ("prompts", "Prompt log", "prompts.html"),
    ("costs", "Costs", "costs.html"),
    ("wordcount", "Word count", "wordcount.html"),
    ("sources", "Sources", "sources.html"),
    ("method", "How it was made", "method.html"),
    ("pdf", "The PDF", "essay.pdf"),
]


def nav_html(active, repo):
    items = []
    for key, label, href in NAV:
        cur = ' aria-current="page"' if key == active else ""
        items.append(
            '<li><a href="%s"%s>%s</a></li>'
            % (html.escape(href, quote=True), cur, html.escape(label))
        )
    items.append('<li><a href="%s">Source code (GitHub)</a></li>' % html.escape(repo, quote=True))
    return '<nav class="top"><ul>%s</ul></nav>' % "".join(items)


def page_shell(meta, active, title, header_html, main_html):
    repo = meta.get("repo", DEFAULT_REPO)
    header_block = "<header>%s</header>" % header_html if header_html else ""
    return """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%s</title>
<style>%s</style>
</head>
<body>
%s
%s
<main>
%s
</main>
<footer>
<p>This page is generated from the master text on %s. Source code, the full history
and every raw file: <a href="%s">%s</a></p>
</footer>
</body>
</html>
""" % (
        html.escape(title),
        STYLE,
        nav_html(active, repo),
        header_block,
        main_html,
        date.today().isoformat(),
        html.escape(repo, quote=True),
        html.escape(repo),
    )


def essay_page(meta, mode, body, human_words, ai_words, essay_words):
    title = meta.get("title", "Essay")
    total = human_words + ai_words
    if total:
        hp = round(100 * human_words / total)
        summary = (
            "Essay text (headings and appendix excluded): %d words &middot; "
            "<strong>%d (%d%%) written by Johannes Wolf</strong> "
            "&middot; %d (%d%%) written by the AI &middot; goal: at least 70%% by Johannes"
            % (total, human_words, hp, ai_words, 100 - hp)
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
    if mode == "print":
        lede = (
            "<strong>Printable version.</strong> Print this page and enable "
            "&ldquo;background graphics&rdquo; so the colors are kept. Light green is the "
            "human author; light blue with a dashed underline is the AI."
        )
    else:
        lede = (
            "Every word is labeled. Light green is written by Johannes Wolf; light blue with a "
            "dashed underline is written by the AI. This page is generated from the master text "
            "(<code>essay.md</code>) and cannot disagree with it. <strong>Hover</strong> a blue "
            "passage to preview the prompt that produced it, and <strong>click</strong> it to "
            "read the full exchange in the prompt log."
        )
    if mode == "print":
        explore = ""
    else:
        explore = (
            '<p class="explore">Have a look around &mdash; the links at the top are meant to be an '
            "enjoyable way to see exactly how this assignment was written. You can read every prompt "
            "and every reply, check the sources, and see for yourself "
            '<a href="costs.html">how many tokens the AI used and how much money it cost</a>.</p>'
        )
    header = (
        "<h1>%s &mdash; who wrote what</h1>"
        '<p class="lede">%s</p>'
        "%s"
        '<div class="legend">'
        '<span class="item"><span class="swatch human"></span> Written by Johannes Wolf</span>'
        '<span class="item"><span class="swatch ai"></span> Written by the AI</span>'
        "</div>"
        '<p class="summary">%s</p>'
        '<p class="summary">%s</p>'
        % (html.escape(title), lede, explore, summary, essay_line)
    )
    return page_shell(meta, "index", title, header, body)


def content_page(meta, active, lede, md_text):
    first = md_text.strip().split("\n", 1)
    head = re.match(r"^#\s+(.*)$", first[0].strip())
    title = re.sub(r"\*\*|\*", "", head.group(1)).strip() if head else active.title()
    if head and len(first) > 1:
        md_text = first[1]
    header = "<h1>%s</h1><p class=\"lede\">%s</p>" % (html.escape(title), lede)
    main = '<div class="record">\n%s\n</div>' % render_markdown(md_text)
    return page_shell(meta, active, title, header, main)


def write_record_pages(meta):
    pages = [
        (
            "prompts",
            "Every prompt sent to the AI and every reply it gave, in order, plus the planning "
            "questions and Johannes\u2019s answers. The numbers match the blue passages in the "
            "essay.",
            PROMPTS,
        ),
        (
            "costs",
            "What the AI assistance actually cost, in tokens and in dollars, read from the "
            "tool\u2019s own records rather than estimated.",
            ROOT / "COSTS.md",
        ),
        (
            "wordcount",
            "The running word count of the essay body, and how the words split between Johannes "
            "and the AI.",
            ROOT / "WORDCOUNT.md",
        ),
        (
            "sources",
            "The course syllabus and the two papers the essay draws on. The files themselves are "
            "not published, for copyright reasons; this is the public record of what they are.",
            ROOT / "SOURCES.md",
        ),
        (
            "method",
            "The full explanation of how this was made: what the record contains and how anyone "
            "can verify it.",
            ROOT / "README.md",
        ),
    ]
    written = []
    for key, lede, path in pages:
        if not path.exists():
            continue
        (DOCS / ("%s.html" % key)).write_text(
            content_page(meta, key, lede, path.read_text(encoding="utf-8")), encoding="utf-8"
        )
        written.append(key)
    print("Built %s." % ", ".join("docs/%s.html" % k for k in written))


# -------------------------------------------------------------- PDF (LaTeX)

LATEX_SPECIAL = {
    "\\": r"\textbackslash{}",
    "&": r"\&",
    "%": r"\%",
    "$": r"\$",
    "#": r"\#",
    "_": r"\_",
    "{": r"\{",
    "}": r"\}",
    "~": r"\textasciitilde{}",
    "^": r"\textasciicircum{}",
}


def lesc(text):
    return "".join(LATEX_SPECIAL.get(c, c) for c in text)


def latexify_urls(text):
    return re.sub(r"(https?://[^\s)]+)", r"\\url{\1}", text)


def load_bib(path):
    """Return {key: {field: value}} from the simple BibTeX file."""
    entries = {}
    if not path.exists():
        return entries
    raw = path.read_text(encoding="utf-8")
    lines = [ln for ln in raw.splitlines() if not ln.lstrip().startswith("%")]
    text = "\n".join(lines)
    for m in re.finditer(r"@\w+\s*\{\s*([^,\s]+)\s*,(.*?)\n\}", text, re.S):
        fields = {}
        for fm in re.finditer(r"(\w+)\s*=\s*\{(.*?)\}", m.group(2), re.S):
            fields[fm.group(1).lower()] = fm.group(2).strip()
        entries[m.group(1)] = fields
    return entries


def apa_name(name):
    parts = [p.strip() for p in name.split(",")]
    family = parts[0]
    given = parts[1] if len(parts) > 1 else ""
    suffix = parts[2] if len(parts) > 2 else ""
    initials = " ".join(tok[0].upper() + "." for tok in re.split(r"[\s.]+", given) if tok)
    out = family
    if initials:
        out += ", " + initials
    if suffix:
        out += ", " + suffix + "."
    return out


def apa_authors(author_field):
    names = [apa_name(n.strip()) for n in re.split(r"\band\b", author_field) if n.strip()]
    if not names:
        return ""
    if len(names) == 1:
        return names[0]
    if len(names) == 2:
        return names[0] + ", \\& " + names[1]
    return ", ".join(names[:-1]) + ", \\& " + names[-1]


def apa_reference(entry):
    ref = "%s (%s). %s. " % (
        apa_authors(entry.get("author", "")),
        entry.get("year", ""),
        entry.get("title", "").rstrip("."),
    )
    journal = entry.get("journal", "")
    volume = entry.get("volume", "")
    if journal:
        ref += "\\textit{%s, %s}" % (journal, volume) if volume else "\\textit{%s}" % journal
        if entry.get("number"):
            ref += "(%s)" % entry["number"]
        if entry.get("pages"):
            ref += ", %s" % entry["pages"]
        ref += "."
    if entry.get("doi"):
        ref += " https://doi.org/%s" % entry["doi"]
    return ref


def fmt_chunk_latex(text, refs):
    pattern = re.compile(r"\*\*(.+?)\*\*|\*(.+?)\*|\[@([^\]]+)\]|@([A-Za-z][A-Za-z0-9_\-]*)", re.S)
    pieces = []
    pos = 0
    for m in pattern.finditer(text):
        pieces.append(("text", text[pos:m.start()]))
        if m.group(1) is not None:
            pieces.append(("bold", m.group(1)))
        elif m.group(2) is not None:
            pieces.append(("italic", m.group(2)))
        elif m.group(3) is not None:
            pieces.append(("cite", m.group(3)))
        else:
            pieces.append(("cite_prose", m.group(4)))
        pos = m.end()
    pieces.append(("text", text[pos:]))
    out = []
    for kind, value in pieces:
        if kind == "text":
            out.append(lesc(value))
        elif kind == "bold":
            out.append("\\textbf{%s}" % lesc(value))
        elif kind == "italic":
            out.append("\\textit{%s}" % lesc(value))
        elif kind == "cite":
            keys = [k for k in re.findall(r"[\w:.\-]+", value) if k]
            out.append(lesc("(" + "; ".join(apa_cite(k, refs, False) for k in keys) + ")"))
        else:
            out.append(lesc(apa_cite(value, refs, True)))
    return latexify_urls("".join(out))


def inline_latex(text, refs):
    text = AI_OPEN.sub(" ", text).replace(AI_CLOSE, " ")
    text = re.sub(r"[ \t]+", " ", text)
    return fmt_chunk_latex(text, refs)


def render_latex_body(md, refs, page_break_h1=False):
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
            out.append("\\noindent\\rule{\\linewidth}{0.4pt}")
            i += 1
            continue
        m = re.match(r"^(#{1,6})\s+(.*)$", s)
        if m:
            level = len(m.group(1))
            cmd = {1: "section", 2: "subsection"}.get(level, "subsubsection")
            prefix = "\\newpage\n" if (page_break_h1 and level == 1) else ""
            out.append("%s\\%s{%s}" % (prefix, cmd, inline_latex(m.group(2), refs)))
            i += 1
            continue
        if s.startswith(">"):
            block = []
            while i < n and lines[i].strip().startswith(">"):
                block.append(lines[i].strip()[1:].strip())
                i += 1
            out.append("\\begin{quote}%s\\end{quote}" % inline_latex(" ".join(block), refs))
            continue
        if re.match(r"^[-*]\s+", s):
            out.append("\\begin{itemize}")
            while i < n and re.match(r"^[-*]\s+", lines[i].strip()):
                item = re.sub(r"^[-*]\s+", "", lines[i].strip())
                out.append("\\item %s" % inline_latex(item, refs))
                i += 1
            out.append("\\end{itemize}")
            continue
        if re.match(r"^\d+\.\s+", s):
            out.append("\\begin{enumerate}")
            while i < n and re.match(r"^\d+\.\s+", lines[i].strip()):
                item = re.sub(r"^\d+\.\s+", "", lines[i].strip())
                out.append("\\item %s" % inline_latex(item, refs))
                i += 1
            out.append("\\end{enumerate}")
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
        out.append(inline_latex(" ".join(para), refs))
    return "\n\n".join(out)


LATEX_TEMPLATE = r'''\documentclass[stu,12pt,@@PAPERSIZE@@]{apa7}
\usepackage{fontspec}
\setmainfont{@@FONT@@}
\usepackage[american]{babel}
\title{@@TITLE@@}
\author{@@AUTHOR@@}
\affiliation{@@AFFILIATION@@}
\course{@@COURSE@@}
\professor{@@INSTRUCTOR@@}
\duedate{@@DATE@@}
\begin{document}
\maketitle

@@BODY@@

@@REFERENCES@@

@@APPENDIX@@
\end{document}
'''

LATEX_PAPER_SIZES = {
    "a4": "a4paper",
    "letter": "letterpaper",
    "us-letter": "letterpaper",
    "usletter": "letterpaper",
}


def latex_document(meta, body, references, appendix):
    replacements = {
        "@@PAPERSIZE@@": LATEX_PAPER_SIZES.get(meta.get("papersize", "a4").lower(), "a4paper"),
        "@@FONT@@": meta.get("font", "Times New Roman"),
        "@@TITLE@@": lesc(meta.get("title", "Essay")),
        "@@AUTHOR@@": lesc(meta.get("author", "")),
        "@@AFFILIATION@@": lesc(meta.get("affiliation", "")).replace(",", "{,}"),
        "@@COURSE@@": lesc(meta.get("course", "")),
        "@@INSTRUCTOR@@": lesc(meta.get("instructor", "")),
        "@@DATE@@": lesc(meta.get("date", "")),
        "@@BODY@@": body,
        "@@REFERENCES@@": references,
        "@@APPENDIX@@": appendix,
    }
    doc = LATEX_TEMPLATE
    for key, value in replacements.items():
        doc = doc.replace(key, value)
    return doc


def build_pdf(meta, md):
    if shutil.which("tectonic") is None:
        print("Tectonic not found; skipping the APA PDF.")
        return
    main_md, appendix_md = split_appendix(md)
    bib = load_bib(REFS)
    body = render_latex_body(main_md, _APA_REFS)
    appendix = (
        render_latex_body(appendix_md, _APA_REFS, page_break_h1=True)
        if appendix_md.strip()
        else ""
    )
    has_cites = bool(bib) and bool(re.search(r"\[@|(?<![@\w])@[A-Za-z]", main_md))
    references = ""
    if has_cites:
        entries = sorted(bib.values(), key=lambda e: e.get("author", ""))
        references = (
            "\\newpage\n\\section*{References}\n\n"
            "\\begingroup\n\\parindent=0pt \\hangindent=0.5in \\hangafter=1\n"
            + "\n\n".join("\\noindent " + apa_reference(e) for e in entries)
            + "\n\\endgroup"
        )
    BUILD.mkdir(exist_ok=True)
    DOCS.mkdir(exist_ok=True)
    tex_path = BUILD / "essay.tex"
    tex_path.write_text(latex_document(meta, body, references, appendix), encoding="utf-8")
    out = DOCS / "essay.pdf"
    result = subprocess.run(
        ["tectonic", "-X", "compile", str(tex_path), "--outdir", str(DOCS)],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print("Tectonic could not build the PDF:")
        print(result.stderr.strip())
    else:
        print("Built docs/essay.pdf")


def write_wordcount(meta, count, human, ai):
    lo, hi, target = word_limits(meta)
    state = word_state(count, lo, hi)
    total = human + ai
    hp = round(100 * human / total) if total else 0
    goal = "met" if hp >= 70 else "not met yet"
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
        "## Attribution (essay text only)",
        "",
        "Headings are excluded, and so is the appendix (the statement on AI use and",
        "the reflection). Only the essay text counts toward this ratio.",
        "",
        "- Written by Johannes: **%d words (%d%%)**" % (human, hp),
        "- Written by the AI: %d words (%d%%)" % (ai, 100 - hp),
        "- Goal: at least 70%% by Johannes \u2014 **%s**" % goal,
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
    global _APA_REFS
    _APA_REFS = load_refs(REFS)
    main_md, appendix_md = split_appendix(md)
    main_html, _, _ = render_html(main_md, prompts)
    appendix_html, _, _ = render_html(appendix_md, prompts) if appendix_md.strip() else ("", 0, 0)
    body = main_html + ("\n" + appendix_html if appendix_html else "")
    essay_words = count_essay_words(md)
    human_words, ai_words = count_attribution(md)
    lo, hi, target = word_limits(meta)
    DOCS.mkdir(exist_ok=True)
    (DOCS / "index.html").write_text(
        essay_page(meta, "screen", body, human_words, ai_words, essay_words), encoding="utf-8"
    )
    (DOCS / "print.html").write_text(
        essay_page(meta, "print", body, human_words, ai_words, essay_words), encoding="utf-8"
    )
    write_wordcount(meta, essay_words, human_words, ai_words)
    write_record_pages(meta)
    print("Built docs/index.html and docs/print.html.")
    total = human_words + ai_words
    if total:
        print(
            "Essay text (headings and appendix excluded): %d human words, %d AI words "
            "(%.0f%% human, goal 70%%)." % (human_words, ai_words, 100 * human_words / total)
        )
    print(
        "Essay body: %d words (target %d, required %d-%d) \u2014 %s."
        % (essay_words, target, lo, hi, word_state(essay_words, lo, hi))
    )
    build_pdf(meta, md)


if __name__ == "__main__":
    main()
