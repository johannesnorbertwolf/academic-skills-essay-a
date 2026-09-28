# Working rules for this repository

How the AI assistant should work on this project, so the process stays
transparent and consistent. This project is about showing exactly how the essay
was made, so the rules matter as much as the essay.

## Commits

- Make exactly **one commit after each user prompt**, unless that prompt caused
  no change to any file. Never batch several prompts into one commit.
- The commit message should plainly describe what the prompt asked for.
- The body of the commit message must quote the user's prompt **verbatim**, so
  the git history is a faithful record of every instruction, not a paraphrase.

## Never commit copyrighted material

- The course materials and papers in `sources/` are gitignored and must never be
  committed. `SOURCES.md` is the public record of what they are.

## The master text and generated files

- `essay.md` is the single source of truth for the essay text.
- Never edit anything in `docs/` by hand. Regenerate it with `build.py`
  (coloured web page, printable page, APA PDF).
- Cite sources as `[@key]`, with entries in `refs.bib`.

## Word count

- The essay body must be **700 to 1000 words**; aim for about 800, without being
  strict. This is a hard requirement.
- Only the essay body counts. Headings are excluded, and so is everything from
  the appendix onward (the reflection and the statement on AI use). The
  reference list does not count either.
- `build.py` reports the count and writes it to `WORDCOUNT.md`. Keep an eye on
  it while writing and keep the file current.

## Transparency record

- Record every prompt sent to the AI in `PROMPTS.md`, together with the AI's
  reply.
- Record the AI's planning questions and the user's answers in `PROMPTS.md` too.
- Keep `DIALOGUE.md` current by running `dialogue.py`: it records every prompt
  Johannes typed and the AI's concluding answer, without the reasoning or tool
  activity.
- Keep `COSTS.md` current by running `costs.py`.
