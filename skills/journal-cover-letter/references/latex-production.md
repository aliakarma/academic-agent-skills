# LaTeX production (Stage 7)

## Filling the template

Copy `templates/cover-letter-template.tex` to `<out>/cover_letter.tex`. Fill every field in the LETTER DETAILS block and replace the five `[[Paragraph ...]]` lines between `% ---- BODY START ----` and `% ---- BODY END ----`.

| Field | Content |
|---|---|
| `\LetterDate` | Submission date as a fixed string ("November 14, 2026" in American style, "14 November 2026" in British). Never `\today`, which changes on every recompile. |
| `\RecipientName` | "Prof. Jane Doe, Editor-in-Chief" when verified, else "Editor-in-Chief" or "Editorial Office" |
| `\JournalName` | The official name exactly as the journal writes it |
| `\Publisher` | Publisher name |
| `\Salutation` | "Dear Editor" or a verified "Dear Professor Doe" (no comma, the template adds it) |
| `\ArticleType` | The journal's own label ("Research Article", "Review", "Original Paper") |
| `\ManuscriptTitle` | The exact title from the manuscript, with the manuscript's capitalization |
| `\AuthorName`, `\AuthorDept`, `\AuthorInstitution`, `\AuthorEmail` | The corresponding author as the manuscript lists them |

The subject line prints the title, unhyphenated. Where the body names the journal (or, rarely, the title), use `\emph{\JournalName}` and `\ManuscriptTitle` instead of retyping them, so they cannot drift. Write `\ArticleType` only where its grammar fits ("a Research Article" against "an Original Paper").

Fields with no verified value stay as `[[...]]` until resolved. The check script refuses to pass them.

## Escaping and characters

| Character | Write |
|---|---|
| `&` `%` `$` `#` `_` `{` `}` | `\&` `\%` `\$` `\#` `\_` `\{` `\}` |
| `~` `^` `\` | `\textasciitilde{}` `\textasciicircum{}` `\textbackslash{}` |
| Quotation marks | ` ``text'' ` (never straight `"`) |
| Number range | `2015--2025` (en dash). Never `---`, since em dashes fail the check |
| Non-breaking space | `Fig.~3`, `Dr.~Doe` |
| Greek letters and math in a title | `$\alpha$`, `$k$-means`, `$F_1$` |
| Accented Latin names (é, ü, ç, ł) | Type them directly. pdfLaTeX reads UTF-8 |
| Names in Chinese, Japanese, Korean, Arabic, or other non-Latin scripts | Switch to XeLaTeX (below) |

Email addresses with `_` need `\_` inside `\AuthorEmail`. The template wraps it in `\href{mailto:...}`, so test the link in the PDF when the address has special characters.

## Fonts

- Default: XCharter, a readable serif designed for print, loaded through `\IfFileExists`, with Latin Modern as the automatic fallback. The check script's font warning shows when the fallback was used.
- A journal that asks for Times: replace the font line with `\usepackage{newtxtext}`.
- Non-Latin scripts: switch to XeLaTeX. Change the first line to `% !TEX program = xelatex`, remove `\usepackage[T1]{fontenc}` and the font line, and add `\usepackage{fontspec}` with a font that covers the script (for example `\setmainfont{Noto Serif}` plus `\newfontfamily` for the script). Confirm the font is installed with `fc-list` or `kpsewhich` first. The check script detects `fontspec` and compiles with XeLaTeX.

## Design limits

The design is a restrained academic letter. Keep it that way.

- Body 11 pt. Never below 10.5 pt.
- A4 by default. Use `letterpaper` in the geometry options, and `--paper letter` in the check, only when the journal or the author's country calls for US Letter.
- Margins 25 mm left and right, 22 mm top and bottom. Never below 18 mm.
- Color: navy `#1F3A5F` on the sender name, the rule, and the "Re:" label only. Charcoal `#4A5361` for contact lines. Body text black.
- One thin rule under the sender block. No boxes, shading, icons, logos, decorative fonts, or page numbers.
- A journal logo only when the user supplies it and the journal permits its use. A signature image only when the user supplies one (`\includegraphics[height=1.2cm]{signature.png}` above the name). Never draw or generate a signature.

## Fitting one page

Cut text first (order in `editorial-guidelines.md`). Then, one step at a time, recompiling after each:

1. `\setlength{\parskip}{0.45\baselineskip}`
2. Margins to 20 mm
3. `\fontsize{10.5}{13}\selectfont` right after `\begin{document}`

If the letter still overflows, cut more text. A sparse page (the script warns when the text ends above 55% of the page height) is fine for a short letter. Do not pad it.

## Manual compile (when the script cannot run)

```
latexmk -pdf -norc -interaction=nonstopmode -halt-on-error cover_letter.tex
latexmk -c -norc cover_letter.tex
```

Use `-xelatex` instead of `-pdf` for fontspec letters. Without latexmk, run `pdflatex -interaction=nonstopmode -halt-on-error cover_letter.tex` twice. Never compile with `-shell-escape`. Then check the page count with `pdfinfo` and the text with `pdftotext` yourself, and say in the reply that the check script did not run.
