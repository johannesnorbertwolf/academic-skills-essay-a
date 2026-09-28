# Academic Skills Essay A — who wrote what

This repository contains an essay, and a complete, word-level record of which
parts were written by the human author (Johannes Wolf) and which parts were
written by an AI.

The point is simple: the author is **not** hiding that AI was used. Instead,
every single word is labelled, every prompt is published, and the whole process
is visible to anyone.

## How to read the essay

Three versions are produced automatically from the same master text:

- **Coloured web page:** open `docs/index.html` (or the published website).
  Hover over any coloured passage to see which prompt produced it.
- **Printable version:** open `docs/print.html` and print it (enable
  "background graphics" so the colours show). It works on paper too.
- **The submission file:** `docs/essay.pdf` is the clean, APA 7 formatted essay
  that is handed in. It carries no colouring — the transparency lives in this
  repository, and the PDF points readers to it.

## The legend

| Colour | Meaning |
| --- | --- |
| Plain / light green | Written by **Johannes Wolf** |
| Light blue with a dashed underline | Written by the **AI** |

The AI passages also carry a dashed underline on purpose, so the distinction
survives black-and-white printing and colour blindness.

A summary at the top of the rendered page states exactly how many words each
side wrote, and what share of the essay that is.

## Where the truth lives

Everything is generated from three things:

1. **`essay.md`** — the master text. Words written by Johannes appear as normal
   text. Words written by the AI are wrapped in a small tag that names the prompt
   that produced them. Anything untagged is counted as Johannes's.
2. **`PROMPTS.md`** — every prompt sent to the AI, in order, with the exact reply.
   It also records the AI's planning questions and Johannes's answers, so the
   decisions behind the project are visible too.
3. **The git history** — each change is a dated commit, so the process can be
   checked step by step.
4. **`COSTS.md`** — the token usage and API spend for the AI used in this
   project, read automatically from the tool's own records.

`build.py` turns the master text into the coloured web page, the printable
version, and the APA PDF. `costs.py` regenerates `COSTS.md`. Nobody edits any of
those by hand, so they cannot quietly disagree with the master text.

## Authorship statement

I, Johannes Wolf, am the author of this essay. I designed its structure, chose
what to argue, wrote the untagged text, directed the AI, and take full
responsibility for the final result — including every word the AI contributed,
which I reviewed and approved. The AI is a tool I used openly, not a hidden
co-author. This repository exists so that any reader can verify that claim word
by word.

## Verifying it yourself

- The coloured page and the master text always agree, because the page is
  generated from the master text.
- The prompt log shows exactly what was asked and what came back.
- The git history shows when each piece was added.
- The APA PDF and its reference list are generated from `essay.md` and
  `refs.bib`, so the citations and the references always match.
- `COSTS.md` is read from the tool's own usage records, not estimated.

## Rebuilding everything

`build.py` regenerates the web page, the printable page and the APA PDF;
`costs.py` regenerates `COSTS.md`. Both are run from the project folder. No
output file is ever edited by hand.
