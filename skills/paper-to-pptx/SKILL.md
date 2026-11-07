---
name: paper-to-pptx
description: Use when the user wants a research paper or manuscript (LaTeX .tex, optionally with its .bib, figures and compiled PDF) turned into an editable PowerPoint .pptx talk deck for a conference, seminar, defense or university presentation, with every slide faithful to the paper. Trigger on "paper-to-pptx", "make slides from my paper", "presentation from paper.tex", "conference talk deck", "15-slide presentation of this paper", "turn my manuscript into a PowerPoint". Do NOT trigger for decks with no source paper (pitch decks, coursework, business plans), for editing an existing .pptx only (pptx skill), for posters, or for converting a paper to another paper format.
---

# Paper to PPTX: Faithful Research Talk Deck

> **Paths.** `${CLAUDE_SKILL_DIR}` is the folder that holds this SKILL.md. Claude Code fills it in. In other agents, replace it with that folder's path. `${CLAUDE_SKILL_DIR}/../<skill>` is a sibling skill from the same collection, so install that skill too.

## Overview

Builds one editable `Research_Presentation.pptx` (15 slides, 16:9) from a research paper, plus a PowerPoint-rendered PDF, a slide montage, the generator source, and `VERIFICATION.md`. The governing instructions are the user's own prompt, stored verbatim in `references/prompt.md`. That file is the contract. This page adds the run notes and tools that make the contract checkable.

**REQUIRED:** Read `references/prompt.md` in full before reading the paper.
**REQUIRED SUB-SKILL:** Invoke `anthropic-skills:pptx` for the pptxgenjs gotchas, the structured-deck rules, `apply_theme.js` and `validate.py`. This skill does not repeat them.

Core rule: **every number, claim, equation and citation on a slide traces to a line of the paper.** A slide that cannot cite its source is cut or rewritten, never filled.

## Workflow

1. **Find the sources.** Use the path the user gives. Otherwise take the `.tex` with `\documentclass` in the working directory, plus every `\input`/`\include`/`\subfile`, the appendix, the supplement, the `.bib`, the `.aux`, the compiled PDF and the figure files. Read every file to the last line. Stop and ask if two candidate papers exist.
2. **Set up the output folder.** Create `Presentation/` beside the paper with `src/` and `assets/`. If `Research_Presentation.pptx` already exists there, ask before overwriting or write into `Presentation_<date>/`. Copy `templates/VERIFICATION.md` in and fill sections 1 to 4 **before** writing any slide code.
3. **Pin down what the paper can support.**
   - **Result status.** Find out whether results are measured, simulated, projected or marked implementation targets (for example `\tgt{}`, blue text, "target", "projected", "expected"). Unmeasured numbers keep that status on the slide: the `target` tag, a caption saying so, and wording that never says "achieves" or "shows". Theory stays theory. Proposed stays proposed.
   - **Numbering.** Take equation, theorem, figure and table numbers from the `.aux` (compiled numbering), not from source order. Shared theorem counters are common.
   - **Authorship.** Slide 1 shows exactly what the paper prints. For an anonymous submission, write "Anonymous authors" and the venue line. Never pull names from git, folder names, memory or the user's account.
   - **Gaps.** Record missing, ambiguous or inconsistent items in VERIFICATION.md section 7 instead of guessing.
4. **Plan, then choose a direction.** Fill the slide plan with a SOURCE for every row. Titles state the slide's point as a sentence. Pick a visual direction that fits the topic, with one meaning per color. Record the 25-point design audit decisions. Adapt the 15-slide structure to the paper. Do not force a "Results" slide onto a theory paper.
5. **Equations.** Copy each needed equation verbatim from the paper into `src/equations.tex` as `%% name` blocks, and the paper's macro definitions into `src/macros.tex`. **Write these with the Write tool.** A Bash heredoc can collapse `\\` and silently merge aligned lines. Then render them:
   ```bash
   python -I "${CLAUDE_SKILL_DIR}/scripts/render_equations.py" src/equations.tex assets/eq --preamble src/macros.tex
   ```
   Add `--ink D7DDE4` into another folder for equations on dark slides. Each image keeps its LaTeX as alt text.
6. **Figures.**
   - **Reuse a figure the paper already draws well.** Convert vector PDFs with `pdftocairo -png -r 300 -singlefile`. Take raster files as they are. If a figure is TikZ inside the .tex, crop it from the compiled PDF at 300 dpi or compile it standalone.
   - **Rebuild a dense chart as a native PowerPoint chart** with values copied from the paper's table or data source. Keep its units and axis meaning. If an axis does not start at zero, say so in the caption.
   - **Rebuild a diagram with native shapes and connectors.** Draw only the boxes and arrows the paper describes. For a diagram that needs a full redraw, `figure-rebuild` applies.
7. **Build.** Copy `templates/build_deck.js` to `src/`. It holds the theme, two layouts, a 0.6 in grid, and the helpers `runs`/`paras`/`text`/`eq`/`figure`/`line`/`box`/`tag`/`contentSlide`. Replace every `FILL`. Put a `// SOURCE:` comment above every data block. Give every slide speaker notes drawn from the paper's own text, 60 to 150 words, so the presenter has a grounded script. Then run:
   ```bash
   node src/build_deck.js        # NODE_PATH=$HOME/node_modules if pptxgenjs is not found
   ```
8. **Render with PowerPoint.** This PC has no LibreOffice.
   ```bash
   powershell.exe -NoProfile -ExecutionPolicy Bypass -File "${CLAUDE_SKILL_DIR}/scripts/export_pdf.ps1" -Pptx Research_Presentation.pptx
   ```
9. **QA until clean.**
   ```bash
   python -I "${CLAUDE_SKILL_DIR}/scripts/qa_check.py" Research_Presentation.pptx --tex <paper.tex> <included .tex> <paper.bib> --pdf Research_Presentation.pdf
   python "<pptx skill dir>/scripts/office/validate.py" Research_Presentation.pptx   # no -I: it imports sibling helpers
   ```
   - **`qa_check.py` must report 0 errors.** It checks slide count, notes, house punctuation, shapes past the edge, stretched or full-slide images, tiny fonts and leftover `FILL`.
   - **Resolve every warning in VERIFICATION.md.** `W02` lists each number on a slide or in the notes that does not appear verbatim in the sources. Fix it, or record the source line that justifies it (for example a rounded value or a computed difference the paper states).
   - **Inspect every slide image individually** (`pdftoppm -png -r 80`), not only the montage. Look for overflow, clipping, overlap, contrast, equation quality and alignment. The XML checks cannot see these.
   - **Fix, rebuild and re-render.** At least two visual rounds. Record both in section 6.
10. **Finish VERIFICATION.md** and answer: does every slide row have a SOURCE, does every W02 have a resolution, does every target or simulated number carry its label? Any "no" means more work.

## Quick reference

| Need | Tool |
|---|---|
| pptxgenjs API, theme colors, XML validation | `anthropic-skills:pptx` (`apply_theme.js`, `office/validate.py`) |
| Equation images with true scale | `scripts/render_equations.py` + `eq()` helper |
| PPTX to PDF | `scripts/export_pdf.ps1` (PowerPoint COM) |
| Fidelity and layout checks, montage | `scripts/qa_check.py` (`--selftest` proves the 11 checks fire) |
| Redrawing a paper figure | `figure-rebuild` skill |
| Prose in notes and on slides | house style: no em dashes, no semicolons, no banned words (checked by `qa_check.py`) |

## Common mistakes

| Mistake | Fix |
|---|---|
| Writing slides after reading the abstract and results only | Read every source file to the end first (prompt section 1) |
| Presenting projected or target numbers as results | `target` tag, caption, and wording that names the status |
| Equation numbers that differ from the PDF | Take them from the `.aux` |
| Author names added to a double-blind deck | Slide 1 shows only what the paper prints |
| A slide of bullets copied from the paper | One point per slide, a title stating it, a visual that carries it |
| Shrinking a dense figure until it is unreadable | Native chart or faithful simplified redraw |
| Generic closing "Thank you" slide | Closing message drawn from the conclusion, then Q&A |
| Trusting the montage | Read each slide image, at least two rounds |
| Calling the deck done when the file was written | Done = 0 QA errors, every warning resolved, VERIFICATION.md complete |

## Reply to the user

Keep it short:
- the four deliverable paths
- the slide count
- QA error and warning counts
- what was rebuilt rather than reused
- the items for the author (VERIFICATION.md section 7)
- anything not checked, such as fonts on another machine or citation accuracy beyond the paper's own `.bib`
