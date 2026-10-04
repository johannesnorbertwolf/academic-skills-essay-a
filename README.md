# Academic Skills Essay A — who wrote what

## **[Read the color-coded essay here: who wrote what →](https://johannesnorbertwolf.github.io/academic-skills-essay-a/)**

This repository contains an essay, and a complete, word-level record of which
parts were written by the human author (Johannes Wolf) and which parts were
written by an AI.

The point is simple: the author is **not** hiding that AI was used. Instead,
every single word is labeled, every prompt is published, and the whole process
is visible to anyone.

## How to read the essay

Three versions are produced automatically from the same master text:

- **Colored web page:** open the published website,
  <https://johannesnorbertwolf.github.io/academic-skills-essay-a/> (or `docs/index.html`).
  Hover over any blue passage to preview the prompt that produced it; click it to
  jump to the full exchange in the prompt log.
- **Printable version:** open `docs/print.html` and print it (enable
  "background graphics" so the colors show). It works on paper too.
- **The submission file:** `docs/essay.pdf` is the clean, APA 7 formatted essay
  that is handed in. It carries no coloring — the transparency lives in this
  repository, and the PDF points readers to it.

## Explore the record on the website

The published website is the friendly front door to everything. Besides the
color-coded essay, it has a page for each part of the record:

- **Prompt log** — every prompt sent to the AI and every reply it gave, plus the
  planning questions and Johannes's answers. Clicking any blue passage in the
  essay jumps straight to the prompt that produced it.
- **Costs** — the token usage and API spend, read from the tool's own records.
- **Word count** — the running essay-body count and the human/AI split.
- **Sources** — what was used and how to cite it.
- **How it was made** — this document.

The repository stays the technical source of truth; the website is generated
from it, so the two cannot disagree.

## The legend

| Color | Meaning |
| --- | --- |
| Plain / light green | Written by **Johannes Wolf** |
| Light blue with a dashed underline | Written by the **AI** |

The AI passages also carry a dashed underline on purpose, so the distinction
survives black-and-white printing and color blindness.

A summary at the top of the rendered page states exactly how many words each
side wrote, and what share of the essay that is.

## Where the truth lives

Everything is generated from three things:

1. **`essay.md`** — the master text. Words written by Johannes appear as normal
   text. Words written by the AI are wrapped in a small tag that names the prompt
   that produced them. Anything untagged is counted as Johannes's.
2. **`PROMPTS.md`** — the single, generated log of the conversation: every prompt
   sent to the AI with its answer, and every planning question with Johannes's
   answer, in order. The numbers match the AI tags in `essay.md`.
3. **The git history** — each change is a dated commit, so the process can be
   checked step by step.
4. **`COSTS.md`** — the token usage and API spend for the AI used in this
   project, read automatically from the tool's own records.
5. **`WORDCOUNT.md`** — the running word count of the essay body, kept against
   the required 700–1000 words. Headings and the appendix (reflection, statement
   on AI use) do not count.

`build.py` turns the master text into the colored web page, the printable
version, the APA PDF, and `WORDCOUNT.md`. `costs.py` regenerates `COSTS.md`, and
`prompts.py` regenerates `PROMPTS.md`. Nobody edits any of those by hand, so
they cannot quietly disagree with the master text.

## Sources

The course syllabus and the two papers the essay draws on are listed in
`SOURCES.md`, with full references. The files themselves are kept in the
`sources/` folder of the working copy but are deliberately **not committed**,
because they are copyrighted course and publisher materials. The two papers are
also entered in `refs.bib`, so they can be cited in the essay and appear in the
reference list automatically.

## Authorship statement

I, Johannes Wolf, am the author of this essay. I designed its structure, chose
what to argue, wrote the untagged text, directed the AI, and take full
responsibility for the final result — including every word the AI contributed,
which I reviewed and approved. The AI is a tool I used openly, not a hidden
co-author. This repository exists so that any reader can verify that claim word
by word.

## Verifying it yourself

- The colored page and the master text always agree, because the page is
  generated from the master text.
- The prompt log shows exactly what was asked and what came back.
- The git history shows when each piece was added.
- The APA PDF and its reference list are generated from `essay.md` and
  `refs.bib`, so the citations and the references always match.
- `COSTS.md` is read from the tool's own usage records, not estimated.
- Each commit corresponds to a single instruction, so the history reads as a
  step-by-step log of how the essay was made.

## Rebuilding everything

`build.py` regenerates the web page, the printable page and the APA PDF;
`costs.py` regenerates `COSTS.md`. Both are run from the project folder. No
output file is ever edited by hand.
