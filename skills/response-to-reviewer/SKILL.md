---
name: response-to-reviewer
description: Use when creating, drafting, updating, restructuring, or verifying a Response to Reviewers document, rebuttal letter, point-by-point reply, or author response for a revised manuscript or journal/conference resubmission, especially when reviewer comments and revised manuscript or supplementary files (.tex, .pdf, .docx) are provided. Also use when a manuscript changed after the response letter was written and its page or line references may be stale.
---

# Response to Reviewer

> **Paths.** `${CLAUDE_SKILL_DIR}` is the folder that holds this SKILL.md. Claude Code fills it in. In other agents, replace it with that folder's path. `${CLAUDE_SKILL_DIR}/../<skill>` is a sibling skill from the same collection, so install that skill too.

## Overview

Every response is a claim about the revised files. Nothing enters the letter unless it can be pointed to on a page (and line) of the compiled revised manuscript or in a named supplementary file, and nothing in the reviewer reports goes unanswered.

**REQUIRED:** Read `references/requirements.md` in full at the start of every run. It is the user's own specification, verbatim, and it overrides anything below.

**REQUIRED SUB-SKILL:** Use text-humanizer for the prose decisions. Apply the house style from universal-manuscript-polish: American English and its punctuation policy (STANDARD by default, STRICT when the user asks for no semicolons or em dashes in author prose; verbatim reviewer text and quotations are always exempt).

**Not for:** simulating a peer review or planning rebuttal strategy before revising (peer-review), or revising the manuscript itself (manuscript-revision, universal-manuscript-polish). This skill does not edit the manuscript. If a request was not implemented, report it to the user instead of writing it up as addressed.

## Workflow

### 1. Locate inputs and inventory every reviewer item
- Find the reviewer file(s), the revised manuscript source, its **compiled PDF with line numbers** and `.aux`, the supplementary files, any editor letter, and any existing response letter. If the PDF is older than the source, recompile it before anything else.
- Back up an existing letter to the scratchpad before overwriting it.
- Look for the original submission (backup folders, git history). It is only needed for statements about what the original said.
- Write `inventory.tsv` in the scratchpad, one item per line in report order: `R1-01<TAB>topic`. Use `R{k}-00` for a general assessment or language rating, letters for sub-comments (`R2-03a`), and `E-01` for editor requests. Split distinct requests and keep inseparable ones together. Note review-form ratings for the introductory note.

### 2. Read the whole revised manuscript with real positions
```
python scripts/build_line_index.py main.pdf --out <scratch>/main_idx.txt
python scripts/aux_labels.py main.aux            # section/eq/fig/table numbers and pages
```
Read the full index. Text extraction drops Greek letters and scrambles table columns, so take table values and equations from the `.tex` source. If the PDF has no line numbers, cite section, paragraph, table and figure instead of lines.

### 3. Map evidence for each item
For each inventory item, record every passage that addresses it (main manuscript and supplementary listed separately), the numbers it reports, and a status:
`Acknowledged` (general remarks) | `Addressed` | `Addressed, data need stated` | `Corrected` (an error the reviewer found) | **not implemented: stop and report to the user.**

### 4. Draft from `templates/response_template.tex`
The front matter is the title block, an introductory note to the editor and reviewers, a summary-of-changes table and a "How to read this letter" note. The end is "Further corrections" (only if present in the files), the completeness index and the closing.

Each item has four parts, in this order:
1. `reviewercomment` box with the comment verbatim. Allow only typographic fixes, and declare them in the "How to read" note.
2. `\response`: acknowledge a valid concern, say what was done with the key numbers from the revised files, and state any limit plainly.
3. `\actiontaken`: bullets beginning with a bold verb (**Added**, **Revised**, **Removed**, **Corrected**, **Clarified**, **Stated**, **Recomputed**, **Not done**, **Not determined**).
4. `location` box: `\mainms` list, then `\suppl` list when relevant, e.g. `Section~4.3, pp.~21--22, ll.~699--739; Table~A5 (p.~53)`.

Cite whole paragraph ranges starting at the paragraph's first line. Use `pp.` when a range crosses a page. Cite floats and captions by number and page, since they carry no line numbers. When the reviewer uses old numbering ("Table 8"), name the new number in the response.

### 5. Flag what the files cannot prove
- A statement about the original submission with no original file available: add `% AUTHOR CHECK: <reason>` at the end of that line, and list it in the final report.
- A process claim ("re-ran", "verified", "reproduces"): verify it if feasible, running scripts into a scratch output directory and never over the user's files. Otherwise flag it the same way.

### 6. Verify (every item must pass before the letter is called final)
```
python scripts/check_completeness.py <scratch>/inventory.tsv letter.tex   # 0 structural problems
python scripts/check_locations.py <scratch>/main_idx.txt letter.tex      # 0 problems
python scripts/check_numbers.py letter.tex main.tex <scratch>/main_idx.txt [supp/results files]
latexmk -pdf -interaction=nonstopmode letter.tex                        # log: 0 errors, overfull, undefined
grep -n fillin letter.tex                                               # only the two \newcommand lines
```
Review every number `check_numbers.py` reports and every prose-style note. Run the project's own verification scripts if they exist. Render at least the first page, a comment page and the index to PNG and look at them.

### 7. Report to the user
Start with one "Written for:" line. Then give the files written, the verification results with counts, the AUTHOR CHECK list, items not implemented or only partly addressed, and the backup location.

## Updating a letter after the manuscript changed
Recompile the manuscript, rebuild the index, and rerun `check_locations.py`. Find each mismatched passage again by searching its text in the index, never by shifting numbers. Then rerun `check_numbers.py` and recompile the letter.

## Common mistakes
| Mistake | Fix |
|---|---|
| Citing a line in mid-paragraph, or the wrong page at a page break | Cite from the paragraph start; let `check_locations.py` catch page breaks |
| Trusting a stale PDF | Compare modification times and recompile first |
| Reading table numbers from extracted PDF text | Read them from the `.tex` source |
| Claiming what the original submission said, without the original | Keep only if the author vouches for it; mark `% AUTHOR CHECK` |
| "We have revised this accordingly" | Name the change, its numbers and its location |
| Merging two reviewer points to save space | One box per distinct request |
| Prose list with semicolons ("restrictive, ...; the reference; and ...") | Restructure into sentences |
| Python one-liners with backslashes in shell heredocs (Windows) | Write scripts to files; use `chr(92)` for backslashes |
| Script path with a space (`C:/Users/Jane Doe/...`) breaks the call | Always quote the path: `python "${CLAUDE_SKILL_DIR}/scripts/..."` |
| Letter says 556,000 USD where the table says 556 kUSD | Fine if the unit is right; `check_numbers.py` lists these separately for confirmation |
| Wide `longtable` columns overflow | Column widths + 2(n-1) `\tabcolsep` must fit `\textwidth` |

## Red flags: stop
- "The change is probably in there": find it on a page and line, or flag it.
- Writing "addressed" for a comment with no implemented change.
- A page or line number recalled from the `.tex` source instead of read from the PDF index.
- Finishing with a verification step skipped "because it passed last time".
