# Quality control and delivery (Stages 9 and 10)

## Script checks

`scripts/check_letter.py` exits 0 (`RESULT: PASS`), 1 (`RESULT: FAIL`), or 2 (`BLOCKED`, no TeX compiler).

| Check | FAIL when |
|---|---|
| compile | latexmk or the engine stops with an error |
| overfull lines | any line runs more than 1 pt into the margin |
| glyphs | the log reports a missing character |
| references | an undefined `\ref` or `\cite` |
| pages | the PDF has anything but exactly one page |
| paper | the page size differs from `--paper` (default a4) |
| text | fewer than 50 words can be extracted |
| placeholders | `[[`, `]]`, TODO, TBD, XXX, lorem ipsum, or `??` survive |
| required text | a `--require` string is missing (hyphenation and line breaks are ignored) |
| em dashes, semicolons | either appears outside the required strings |

It also reports, without failing: the body word count against the 250 to 350 advisory range, font substitutions, and page fill. Run `python check_letter.py --selftest` after editing the script or the template. It proves that the placeholder, page-count, em-dash, semicolon, and required-text checks fire, and that a clean letter passes.

## Visual checklist (read the PNG)

The script cannot judge appearance. Read the render and check:

- Balance: the body sits comfortably on the page, with no cramped block at the top and no empty half-page caused by layout (short content is fine).
- Hierarchy: name, then contact lines, rule, date, recipient, subject line, salutation, body, signature, in that order and clearly separated.
- Typography: one body font, consistent size, no stray bold or italics, no widow line of one or two words closing a paragraph when a small edit fixes it.
- Alignment: a ragged-right or justified body with no rivers of white space. The left edges of every block line up.
- Spacing: even gaps between paragraphs. The signature block is not crammed against the bottom margin.
- Characters: no boxes, question marks, or wrong accents in names.
- Proper nouns: the journal name and personal names never break across lines with a hyphen. Add the affected words to the template's `\hyphenation{...}` line and recompile.
- Content: the title, journal, and names render exactly as recorded in Stage 1.

Fix what you find, rerun the script, and read the new render.

## Fact verification (before delivery)

- Every sentence in paragraphs 2 to 4 maps to a fact-sheet item tagged DEMONSTRATED, or to an attributed CLAIMED item.
- Every number matches the manuscript, including units, dataset, and conditions.
- Every declaration maps to its source in the declaration table of `editorial-guidelines.md`.
- Every journal-specific statement maps to a source in the research record.
- The editor's name, if used, was seen on the official page in this run.

## Final reply format

```
**Files**
- PDF: <absolute path>/cover_letter.pdf
- LaTeX: <absolute path>/cover_letter.tex
- Earlier letter preserved as: <path> (only if Stage 8 renamed one)

**Editorial research**
- Requirements applied: <cover letter mandatory or optional, prescribed content, in-letter declarations> [URL]
- Fit argument: <scope topics engaged and readership> [URL]
- Contributions emphasized: <2 or 3 items with manuscript locations>

**Quality assurance**
- Pages: 1 (pdfinfo) | Engine: <latexmk (pdflatex)> | Check script: PASS, <n> warnings
- Humanizer: text-humanizer run, patterns fixed <B-IDs>, fidelity_check PASS
- Visual inspection: done on the rendered PNG | not done because <reason>
- Declarations: <each, with source> | Manuscript details: verified against <file>

**Needs your confirmation**
- <every unverified item, or "None">
```

State only what happened. If the script was not run, the PNG not read, or a source not reachable, say so in that section.
