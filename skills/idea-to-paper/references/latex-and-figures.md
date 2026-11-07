# LaTeX, Figures, Tables, and Build

`templates/main.tex` is the compile-tested starting point. Its DEMO blocks are the figure, table, algorithm, and equation recipes: each was compiled and inspected as rendered pages. Reuse their styles and change the content.

## Formatting rules

- Each paragraph is one line. Enter starts a new paragraph and nothing else. This holds for the abstract, list items, and captions.
- Escape `%` as `\%`, `&` as `\&`, `_` as `\_`, and `#` as `\#` in text.
- No `\\` or `\newline` inside paragraphs. Paragraph spacing comes from blank lines.
- Every figure, table, and algorithm has `\caption{}` followed by `\label{}`. Every numbered equation has a `\label{}`. Every label is referenced in the text.
- Label prefixes: `fig:`, `tab:`, `eq:`, `alg:`, `sec:`. Labels and citation keys are unique.
- Load each package once. The skeleton preamble is complete for the recipes. Add a package only when the paper uses it, and never `hyperref` unless the venue asks for it (IEEE PDF eXpress dislikes link annotations in some workflows).
- Keep `\title` and `\author` in the preamble, as in the skeleton.

## Floats

- Use `[t]` for every float and define it after the paragraph that first references it.
- `figure*` and `table*` span both columns and can only go to the top of a page. Use them for the architecture figure and for tables that do not fit one column.
- IEEE places table captions above tables and figure captions below figures (the checker warns otherwise).
- When a float lands above the abstract on page 1, move its definition later in the source.
- "Too many unprocessed floats" means floats are bunched: interleave them with text.

## TikZ diagrams

Styles from the skeleton: `blk` (rounded box), `flow` (solid arrow), `dflow` (dashed arrow), `grp` (dashed group frame on the background layer), `lbl` (small edge label). Pastel fills `boxA` to `boxE`, line color `lineC`.

- Size: one column is about 88 mm wide (`\columnwidth`), and `figure*` is about 181 mm (`\textwidth`). Plan the node count, node width, and gaps to fit. Five 21 mm boxes with 13 mm gaps fill a `figure*` row with room for edge labels.
- Text: `\footnotesize` in boxes and `\scriptsize` on edges. Nothing smaller.
- Place nodes with the `positioning` library (`right=of a`), not absolute coordinates.
- Label every arrow that carries something specific (data, model updates, alerts, feedback).
- Icons: `fontawesome5` vector icons above the box title, for example `\faDatabase`, `\faServer`, `\faMicrochip`, `\faBrain`, `\faRobot`, `\faCogs`, `\faProjectDiagram`, `\faNetworkWired`, `\faCloud`, `\faLock`, `\faUserShield`, `\faShieldAlt`, `\faEye`, `\faCheckCircle`, `\faChartLine`, `\faChartBar`, `\faUsers`, `\faUser`, `\faLink`, `\faCube`, `\faWifi`, `\faMobileAlt`, `\faHospital`, `\faCar`, `\faIndustry`, `\faBolt`, `\faWater`, `\faLeaf`, `\faWheelchair`, `\faBlind`, `\faFileAlt`, `\faSearch`, `\faBell`, `\faExclamationTriangle`. An unknown name fails with "Undefined control sequence": check the fontawesome5 manual (`texdoc fontawesome5`).
- When the author supplied a raster or AI-generated figure for the same diagram, use the figure-rebuild skill instead.

## PGFPlots charts

All use the `ieee` style from the skeleton (full column width, 4.4 cm high, small fonts, light grid) and the Okabe-Ito colors `plotA` to `plotE`, which stay distinguishable for color-blind readers. Also vary marks and dash patterns so the chart survives grayscale printing.

Recipes in the skeleton: single-series bars with value labels (`fig:bars`), a two-line curve (`fig:curve`), and a row-normalized confusion matrix (`fig:confusion`). Two more, compile-tested:

Grouped bars (for example, ablation across metrics):

```latex
\begin{axis}[ieee, ybar, bar width=6pt, ymin=80, ymax=96, ylabel={Score (\%)}, symbolic x coords={Precision,Recall,F1}, xtick=data, enlarge x limits=0.25, legend columns=3, legend style={at={(0.5,1.03)}, anchor=south}]
\addplot[fill=plotA!70, draw=plotA] coordinates {(Precision,92.7) (Recall,91.7) (F1,92.2)};
\addplot[fill=plotB!70, draw=plotB] coordinates {(Precision,91.1) (Recall,89.6) (F1,90.3)};
\addplot[fill=plotC!70, draw=plotC] coordinates {(Precision,90.2) (Recall,88.9) (F1,89.5)};
\legend{Full model, Without A, Without B}
\end{axis}
```

Scalability on a log-2 axis with error bars:

```latex
\begin{semilogxaxis}[ieee, xlabel={Number of clients}, ylabel={Round latency (s)}, log basis x=2, xtick={8,16,32,64,128}, xticklabels={8,16,32,64,128}, legend pos=north west]
\addplot[plotA, thick, mark=*, mark size=1.2pt, error bars/.cd, y dir=both, y explicit] coordinates {(8,1.9) +- (0,0.1) (16,2.4) +- (0,0.1) (32,3.3) +- (0,0.2) (64,5.0) +- (0,0.3) (128,8.6) +- (0,0.5)};
\addplot[plotD, thick, dashed, mark=triangle*, mark size=1.4pt] coordinates {(8,2.1) (16,3.6) (32,6.7) (64,12.9) (128,25.4)};
\legend{Proposed, Baseline C}
\end{semilogxaxis}
```

Rules: label both axes with units, start bar axes where the differences stay visible but say so when the axis does not start at zero, print bar values with `fixed zerofill` so 90.0 does not show as 90, and keep plotted values identical to the table values. Coordinates cannot be colored, so a target chart is marked by `\tgtcap` in its caption.

## Tables

- `booktabs` rules only (`\toprule`, `\midrule`, `\bottomrule`). No vertical lines.
- Units in the header, best value in bold, mean and deviation as `92.2 $\pm$ 0.4`.
- Fit the column with short headers, abbreviations defined in the caption, and `\setlength{\tabcolsep}{3.5pt}`. Do not wrap tables in `\resizebox`, because it shrinks the font below the body size. Use `table*` when a table needs more width.
- Every numeric table is a target table (`\tgtcap`) or carries `% MEASURED:`, `% CONFIG:`, or `% SOURCE:`. The checker fails untagged numeric floats (E17).

## Algorithms and equations

- `algorithm` plus `algpseudocode`: `\Require`, `\Ensure`, `\State`, `\For`/`\EndFor`, `\If`/`\EndIf`, `\Return`. Keep lines short enough for one column. State time and communication complexity in the text.
- Number every equation the text discusses, label it, and reference it with `Equation~\eqref{}`. Use `equation*` or `\nonumber` for unreferenced displays. Define every symbol in the sentence after the equation, consistent with the notation list.

## Build and inspect

```bash
latexmk -pdf -norc -interaction=nonstopmode -halt-on-error main.tex
pdftoppm -r 80 -png main.pdf _build/page
```

Without latexmk, run `pdflatex`, `bibtex`, `pdflatex`, `pdflatex`. Never use `-shell-escape`. Open every page image and check the visual list in SKILL.md Step 4.

| Symptom | Usual cause and fix |
|---|---|
| `Undefined control sequence` at an icon | Wrong fontawesome5 name. Check the manual |
| `Missing $ inserted` | `_` or `^` in text. Escape it or put it in math |
| Text vanishes after a number | Unescaped `%`. Write `\%` |
| `Misplaced alignment tab character &` | `&` in text. Write `\&` |
| `Package pgfplots Error: ... symbolic x coords` | A coordinate name is missing from the `symbolic x coords` list |
| `Dimension too large` in a plot | Axis range far from the data. Set `ymin` and `ymax` |
| Overfull hbox in a table | Shorter headers, smaller `\tabcolsep`, or `table*` |
| `Citation ... undefined` after a full build | Key missing from `references.bib` or a BibTeX error. Read `main.blg` |
| `File ended while scanning use of \caption` | Unbalanced brace in the caption |
