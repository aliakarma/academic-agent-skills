# Verification Summary: FILL paper short title

Deck: `Research_Presentation.pptx` (FILL slide count) · Built FILL date · Source: FILL paper path

## 1. Source inventory

| Item | Path | Read in full? | Notes |
|---|---|---|---|
| Main .tex | FILL | FILL yes, lines 1 to N | |
| Included files (`\input`, appendix, supplement) | FILL | | |
| .bib | FILL | | |
| .aux (compiled numbering) | FILL or "not found, numbering from source order" | | |
| Compiled PDF | FILL | | |
| Figures | FILL | | |

Result status in the paper: FILL (measured / simulated / projected / implementation targets, with the paper's own wording and line).
Authorship on slide 1: FILL (as printed / anonymous for double-blind review).

## 2. Slide plan and source map

| # | Section | Slide title (its point) | Content and visual | SOURCE (lines, table, figure, equation) | Claim type |
|---|---|---|---|---|---|
| 1 | Opening | FILL | | | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |
| 6 | | | | | |
| 7 | | | | | |
| 8 | | | | | |
| 9 | | | | | |
| 10 | | | | | |
| 11 | | | | | |
| 12 | | | | | |
| 13 | | | | | |
| 14 | | | | | |
| 15 | Closing | FILL | | | |

Claim type is one of: theory, method, evidence, target (unmeasured), context. Deviations from the suggested 15-slide structure and why: FILL.

## 3. Visual direction

- Direction and why it fits this paper: FILL
- Palette, one meaning per color: FILL (for example accent1 = attack or failure, accent2 = proposed method)
- Fonts: FILL heading / FILL body, both installed with Office
- Grid: 13.333 x 7.5 in, 0.6 in side margins, title band at 0.66 in, footer at 7.06 in
- Layout families in use and the content each serves: FILL

## 4. Design-quality audit (decided before building, rechecked after rendering)

| # | Consideration | How this deck handles it | Rechecked after render |
|---|---|---|---|
| 1 | Repetitive slide layouts | | |
| 2 | Card-based compositions on every slide | | |
| 3 | Rounded rectangles and decorative containers | | |
| 4 | Stock-style illustrations unrelated to the research | | |
| 5 | Icons that add no scientific information | | |
| 6 | Gradients, shadows, glows, effects | | |
| 7 | Inconsistent spacing, alignment, typography | | |
| 8 | Unbalanced composition and awkward whitespace | | |
| 9 | Overcrowding and small text | | |
| 10 | Vague, repetitive or generic titles | | |
| 11 | Long paragraphs copied from the manuscript | | |
| 12 | Repeated text that adds nothing | | |
| 13 | Decorative charts with little analytical value | | |
| 14 | Inconsistent or meaningless color coding | | |
| 15 | Symmetry that ignores the content | | |
| 16 | Inconsistent diagram and connector styles | | |
| 17 | Poorly rendered equations, symbols, special characters | | |
| 18 | Misleading emphasis or unsupported numbers | | |
| 19 | Low-quality, stretched or pixelated figures | | |
| 20 | Generic opening and closing slides | | |
| 21 | Truncated chart axes not disclosed | | |
| 22 | Equation and theorem numbers differ from the compiled paper | | |
| 23 | Text and background contrast below WCAG AA (4.5:1 body) | | |
| 24 | Speaker notes missing or not grounded in the paper | | |
| 25 | Unmeasured or simulated results styled like measured ones | | |

## 5. Number fidelity

Every number on a slide or in the notes, checked against the source. List each `W02` from `qa_check.py` with its resolution.

| Slide | Number | Source location | Resolution |
|---|---|---|---|
| | | | |

## 6. QA results

- `qa_check.py`: FILL errors 0, warnings N (each warning resolved above or below)
- `validate.py` (pptx skill): FILL
- PowerPoint export: FILL slides, opened without a repair prompt
- Visual pass, round 1: FILL issues found per slide
- Fixes: FILL
- Visual pass, round 2: FILL
- Editability: FILL (text, charts and tables native, images limited to equations and paper figures)

## 7. Items for the author

FILL every missing, ambiguous or inconsistent item found in the paper, with its line. Write "none" only after checking.

## 8. Deliverables

- `Research_Presentation.pptx`
- `Research_Presentation.pdf` (PowerPoint export)
- `Slide_Montage.png`
- `src/` (build_deck.js, equations.tex, macros.tex) and `assets/`
- this file
