---
name: highlighted-pdf-from-reviews
description: Use when a journal resubmission needs a highlighted revised manuscript, marked-up version, "changes highlighted" PDF or reviewer-comment change map built from a LaTeX manuscript and its Response to Reviewers, especially when every revision must carry reviewer-comment IDs (R1.1, R2-05) and an editor must trace comments to pages. Not for writing the response letter itself or for Word (.docx) manuscripts.
---

# Highlighted PDF from Reviews

## Overview

A highlighted revised manuscript is the clean revised `.tex` plus an **annotation layer** and nothing else: ID tags, yellow highlights, boxes, and a front guide with a reviewer comment map whose page numbers come from the compiled PDF. The layer is applied by a build script of exact-match operations, and the build fails unless stripping the layer gives back the clean source byte for byte. That check proves no scientific content changed.

The Response to Reviewers says **why** and **which ID**. The revised manuscript (or a diff against the original) says **what** changed. A location cited in the letter is not, by itself, proof that the text there is new.

**REQUIRED:** Read `references/requirements.md` before starting. It is the full contract the result is checked against.

## Workflow

1. **Inputs and outputs.** Identify the clean main `.tex`, the supplementary material, the letter (`.tex` or PDF) and, if present, the original submission. Outputs go next to the clean file as `<Paper>_Highlighted.tex` and `<Paper>_Highlighted.pdf`, with `scripts/rvhighlight.sty` copied beside them. Never edit the clean files.
2. **Inventory the IDs.** List every comment ID in the letter, including general assessments and language comments. If the letter also lists numbered author-initiated corrections that have no IDs, label them `AC-1`, `AC-2`, … and explain this in the guide intro. Do not invent any other IDs.
3. **Establish what changed, per ID.**
   - *Original submission available:* use `latexdiff old.tex new.tex` or `git diff --word-diff` as the evidence of change, then attach IDs from the letter.
   - *Original not available:* resolve the letter's page and line citations on the clean PDF with `python scripts/pdf_lines.py main.pdf 281-292 1371` and map them to source sentences.
   - **Reviewer-quote rule:** if a reviewer's comment quotes or describes text as already present (for example "the reach function ψ = …"), that text predates the revision. Highlight only what was added around it, and list the excluded locations in the guide's *cannot be shown* section.
   - If a claimed revision is absent from the files, add no highlight. Record it, with its ID, in that same section as not verifiable.
4. **Pick a treatment per element** (see Quick Reference). Use sentence or clause precision for edits to existing paragraphs, boxes for new or rewritten paragraphs, and float boxes for new or revised tables and figures.
5. **Write the build script.** Start from `examples/example_build.py`: it runs on the synthetic project in `examples/demo/` and shows the main operations, the comment list, the map and the guide. Use the Quick Reference for the operations it does not show (`R`, `BAR`) and the class presets for the guide. Run your script. A non-unique match or a failed strip check stops the build, so lengthen the string or fix the operation.
6. **Compile twice** with `latexmk -pdf`. The second run fills the map pages from the `.aux`. Then check all of these:
   - no `^!` errors in the log;
   - no overfull boxes beyond those in the clean build;
   - no `destination with the same identifier` warnings;
   - no undefined references;
   - the table and figure caption numbers in `pdftotext` output match the clean PDF;
   - the PDF Title matches the clean PDF (`pdfinfo`).
7. **Audit per ID.** Run `hl_build.report(aux, COMMENTS)`. Every ID needs pages, except those the letter records as having no separate change. Compare each ID's "Highlighted in" against the elements its letter entry cites, and justify every gap in the guide. Render the guide pages and several boxed, table and figure pages with `pdftoppm -r 60`, and look at them.
8. **Report to the user:** the files, the checks you ran, the judgment calls (AC IDs, reviewer-quote exclusions, uncited text that looks new but was left unhighlighted) and any claims you could not verify.

## Quick Reference

| Revised element | Operation (`hl_build`) |
|---|---|
| Sentence, clause, caption passage or table cell | `W(text, 'R1.2', 'Sec. 3.4')` |
| New or rewritten paragraph(s), preceded by a blank line | `BOX('First words…', ids, where, last='First words of last para…')` |
| New or revised table or figure | `FLOAT('tab:label', ids, 'Table 5')` |
| Row group or row inside a table | `T(r'\emph{Group}}', ids, 'Table 13')` |
| Further cells of a row already tagged | `H(text)` |
| Corrected or new display equation | `EQ('eq:label', ids, 'Eq. (7)')` |
| Longtable or other element spanning pages | `BAR(r'\begin{longtable}{…}', ids, 'Table A4', note)` |
| Annotation inside a non-unique context (e.g. a table header) | `R(old, new_with_\rv, ids, where)` |
| New or renamed section heading | `W('Heading text', ids, 'Sec. 4.3 (new)')` |

The `where` labels fill the map's "Highlighted in" column automatically. Supplementary material: if it is a LaTeX document, give it its own build script (`<Paper>_Supplementary_Highlighted.tex`) and label its map entries "Suppl."; if it is code or data, describe its revisions in the guide's `supplementary=` paragraph.

## Class presets for `guide()`

- **MDPI (`mdpi.cls`):** `wide_open=r'\begin{adjustwidth}{-\extralength}{0cm}'`, `wide_close=r'\end{adjustwidth}'`, `lt_left=r'-\extralength'`, `map_width=r'\textwidth+\extralength'`, `pdfmeta=r'\hypersetup{pdftitle={\@Title},pdfsubject={\@abstract},pdfkeywords={\@keyword},pdfauthor={\@AuthorNames}}'`.
- **article, elsarticle, IEEEtran, Springer:** leave `wide_*` empty and set `pdfmeta=r'\hypersetup{pdftitle={<title>}}'`. If the class does not load hyperref, add `\usepackage{hyperref}` before the layer. Check that `\maketitle` is called; if it isn't, pass `anchor=` to `finish()` so the layer and guide are placed explicitly.

## Common Mistakes

| Symptom | Cause | Fix (already in the tools) |
|---|---|---|
| `Missing \endcsname inserted` at `\begin{document}` or in a caption | A fragile highlight in a moving argument (PDF metadata, caption) | Robust `\rv`/`\rvtag` plus `\pdfstringdefDisableCommands` |
| Every table number shifted by one | The guide's longtable steps the table counter | `\addtocounter{table}{-1}` before it; never use `\caption*` in that table |
| Journal headers replaced on every page | `\fancypagestyle` for the guide page style | A standalone `\ps@rvguide`, then `\pagestyle{fancy}` restored |
| PDF Title empty | The guide ships page 1 before the class's `\maketitle` sets metadata | `pdfmeta` set before the guide |
| Guide table overfull | longtable ignores `adjustwidth` | Set `lt_left` |
| Boxed paragraph loses its indent | tcolorbox defaults | `parbox=false, before upper=\indent` |
| Paragraph break after an equation | `BOX` used on text continuing after a display | Use `W` for continuation text |
| Bar marker stranded at a page foot | Long table starts on the next page | `\needspace` inside `\rvbar` |
| Highlights cover whole letter ranges, including old text | Letter location taken as proof of change | Reviewer-quote rule and sentence-level `W` |
| `soul` error on `\cite`/`\cref` inside a highlight | Command not registered with soul | `\soulregister\<cmd>7` in `rvhighlight.sty` |
