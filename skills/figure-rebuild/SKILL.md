---
name: figure-rebuild
description: Convert an AI-generated or raster research figure (JPEG/PNG from an image model, a screenshot, or a legacy diagram) into a publication-quality LaTeX/TikZ figure with fully selectable vector text, while preserving the original pictograms, matching a reference visual style, and auditing every claim the figure makes against the project's measured results. Use whenever the user wants a figure redrawn for a paper, wants figure text to be selectable or searchable, wants a figure title removed and turned into a caption, wants an image-model figure made submission-ready, wants two figures restyled to match a reference image or each other, or wants figures checked for claims the work does not support. Trigger on "rebuild my figure", "convert this figure to TikZ", "make the figure text selectable", "vectorise this diagram", or image files supplied with a LaTeX manuscript. Not for plotting CSV data, prose editing, or image editing with no paper.
---

# Rebuild a raster figure as a publication-quality TikZ figure

Image models produce handsome research diagrams with three defects that make
them unusable in a journal: the text is rasterised, so it is not selectable,
searchable, or in the body font; they render a **title** into the artwork, where
a journal expects a caption; and, because they draw whatever the prompt said,
they confidently render **claims the work does not support**.

This skill fixes all three without discarding the artwork. The pictograms are
extracted and reused unchanged. Everything else is redrawn in TikZ.

## The rule that governs everything

> **Keep the icons. Keep the style. Replace the text. Verify the claims.**

The user chose that visual language. Do not substitute your own taste for it.
Sample their palette, match their type scale, copy their layout idioms. The only
things that change are the ones that are wrong.

A correction to the *content* is never a licence to change the *style*. If you
fix an arrow direction and the figure comes back looking like your own default
diagram, you have failed the task even though every fact is now right.

## Bundled files

| File | Use |
|---|---|
| `references/editorial-style.md` | **Read this when the user supplies a reference render, says "use this style", or asks for a professional look.** The full editorial-schematic style guide: palette roles, column headers, numbered badges, capacity blocks, chevron chains, hatched inactive arms, connector semantics, type scale, and a pre-flight checklist. |
| `assets/figstyle.tex` | Drop-in shared style file: palette, `figbase` tikzset (`colhdr`, `colrule`, `badge`/`badgeG`/`badgeC`/`badgeT`, `stepflow`, `panel`, `card`, `dashbox`, `dataflow`, `hairflow`, `tealflow`, `corflow`, `callout`), `\capblocks`, `\ficon`. Copy next to the figures, then re-sample the palette. |
| `scripts/extract_icons.py` | Crop, auto-trim, upscale and contact-sheet the pictograms out of the source render. |
| `scripts/verify_selectable.py` | Probe the compiled PDF to prove the figure text is real text. |

## Workflow

### Phase 1 — Locate and inspect

1. Find the source images. If the user says "in Downloads", sort by
   modification time, newest first, and filter to image extensions. Do not
   guess which file they mean when several are close in time; show the
   candidates.
2. **View every image before touching it.** You cannot rebuild what you have
   not seen.
3. Copy them into the repository under `figures/source/` with stable names.
   The rebuild must be reproducible from a checkout.

When the user supplies a *second* set of images later and says "use this
style", those are **style references, not content**. Their content belongs to
somebody else's figure; only the visual language transfers. Keep the audited
content from Phase 2 exactly as it stands and re-dress it.

### Phase 2 — Audit the figure against the evidence

Do this **before** drawing anything, because it changes what you draw.

Read the project's results, decision register and validation harness. Then ask
of every element in the figure:

- Does this assert a measurement that was taken?
- Does it assert apparatus that exists?
- Are quantities consistent with the generated tables?
- Do arrows point the way the data actually flows?
- Are "not done" items visibly marked as not done?

Prompt text leaks into renders. Watch for layout instructions rendered as
headings ("LEFT SPINE", "RIGHT SIDE", "PANEL A"), and for confident labels on
things that were never run ("measured latency", "deployed on hardware").

Write the findings down. Every correction goes in the figure's header comment,
naming what the render claimed and what the evidence says.

### Phase 3 — Extract the pictograms

`scripts/extract_icons.py` is the starting point. The method:

1. View a zoomed crop of each region to read exact pixel coordinates. Estimating
   from a downscaled view puts text inside the crop.
2. Crop generously, then **auto-trim** near-white margin.
3. Upscale 2x with LANCZOS so the icon stays crisp at print size.
4. Build a **contact sheet** and view it. Iterate on any icon that carries a
   stray glyph or a neighbouring arrowhead. Two passes is normal.
5. Commit the extraction script. The icons must be regenerable.

Harvest icons from the *style* references too. A warning triangle or a
distribution-shift curve lifted from a reference render is how you honour
"you can add more icons" without inventing clip-art.

### Phase 4 — Sample the palette

Do not eyeball colours. Sample them:

```python
from collections import Counter
c = Counter(im.crop(box).getdata())
# skip near-white; take the dominant remaining fill
```

Sample every distinct fill, every accent line, every ribbon. Map them onto the
five neutral roles and at most three accents described in
`references/editorial-style.md`.

### Phase 5 — Factor the visual language into one shared style file

Copy `assets/figstyle.tex` into `figures/`, replace its palette with the
sampled values, and have **every** standalone figure file `\input` it before
`\begin{document}`.

This is not tidiness. Two figures that each define their own colours will
drift — one ends up with a different teal, a different corner radius, a
different arrowhead — and a reviewer sees it immediately. One style file makes
that drift impossible, and it makes a later restyle a single-file edit instead
of a rewrite.

### Phase 6 — Rebuild in TikZ as a standalone file

**Never write TikZ code into the manuscript.** Each figure is its own
standalone document, `figures/<name>.tex`, compiled to `figures/<name>.pdf`.
The paper includes only the PDF. This keeps the manuscript free of TikZ
packages and figure code, makes each figure compile and preview on its own,
and gives the journal a plain PDF figure to work with.

Skeleton for `figures/<name>.tex`:

```latex
% <name>: rebuilt from figures/source/<file>. Corrections vs. the render:
%   - ...
\documentclass[border=2pt]{standalone}
\usepackage{xcolor} % before tikz; the class's [tikz] option breaks \colorlet on TeX Live 2024
\usepackage{tikz}
\usepackage{graphicx}
\usepackage{newtxtext,newtxmath} % match the paper's body font
\usetikzlibrary{arrows.meta,positioning,calc,fit,backgrounds,
                shapes.geometric,shapes.symbols,patterns}
\input{figstyle}
\begin{document}
\begin{tikzpicture}
  ...
\end{tikzpicture}
\end{document}
```

`shapes.symbols` is needed for chevron stage chains, `patterns` for hatching
the arm that was not executed. Missing either produces an error far from its
cause. Load the same font packages as the manuscript, or the figure text will
not be in the body font.

Compile it from inside `figures/` so `\input{figstyle}` and the icon paths
resolve:

```bash
cd figures && latexmk -pdf -interaction=nonstopmode <name>.tex
```

Then in the manuscript, with only `graphicx` needed:

```latex
\begin{figure*}[t]
  \centering
  \includegraphics[width=\textwidth]{figures/<name>.pdf}
  \caption{...}
  \label{fig:<name>}
\end{figure*}
```

If the manuscript already holds inline TikZ for this figure (from an older
run of this skill), move that code into `figures/<name>.tex`, replace the
inline block with the `\includegraphics` above, and remove TikZ libraries and
`\input{figstyle}` from the manuscript preamble once no inline TikZ remains.

Design the figure at its **final printed width** (e.g. ~18cm for a
double-column IEEE `figure*`) and include it at `width=\textwidth` or
`\columnwidth`. If the include scales the PDF far from 1:1, the type scale is
wrong in print, so fix the drawing, not the scale factor.

The drawing constraints:

Follow `references/editorial-style.md` for the idioms. The constraints that
are not negotiable:

- **Sizing.** Match the figure to its column. Double-column IEEE is ~18cm.
  Dense diagrams almost always need `figure*`.
- **Type scale.** Three sizes, never below `\tiny`. A figure whose text is
  smaller than the body's footnote size is unreadable in print.
- **No title.** The title becomes the caption.
- **Layer the geometry** so connectors never cross text: give converging lines
  a common abscissa clear of the longest label, and route links around boxes
  rather than through them. Where a label must sit on artwork, give it
  `fill=white, inner sep=1.5pt` and let it knock the line out.
- **Mark the unsupported.** Anything not measured is drawn in a visually
  distinct, obviously-inactive style (hollow, dashed, hatched, greyed) and
  labelled, with a legend entry explaining the distinction. Do not delete it:
  showing what was intended and not achieved is more honest than silence.
- **Budget the columns before you place anything.** Fix the rule abscissae
  first, then place content inside them. Retro-fitting a column that overflows
  means moving twenty coordinates, and each move risks a new collision.

### Phase 7 — Verify

1. Compile `figures/<name>.tex` to `figures/<name>.pdf` and **view the
   render**. Do not trust the source.
2. Iterate on overlaps. Expect two or three passes. Recompile the figure PDF
   after every change: the manuscript picks up only the compiled PDF, so a
   stale PDF means a stale figure in the paper.
3. Compile the full document.
4. **Prove the text is selectable** with `scripts/verify_selectable.py`, or
   (the included vector PDF keeps its text, so probe both PDFs):

```python
import fitz
d = fitz.open("main.pdf")
for probe in ["O-RU", "harmonised", "emulated"]:
    hit = any(pg.search_for(probe) for pg in d)
    print(probe, "selectable" if hit else "MISSING")
```

5. Render the page in context and view it. Figures look different on the page
   than in isolation.

## Pitfalls that cost real time

| Pitfall | Avoidance |
|---|---|
| `t.index(r"\ifsynthdraft")` matches inside `\newif\ifsynthdraft` | Anchor replacements on something that cannot match its own declaration. This deleted a paper's title, authors and abstract. |
| Heredocs mangle `\t`, `\n`, `\\` | Write patch scripts to a file with the Write tool. Build backslashes as `chr(92)` when a literal fights the shell. |
| CRLF working copies break LF-anchored patterns | Normalise with `.replace("\r\n", "\n")` before matching; write bytes back. |
| Node referenced before definition | TikZ needs nodes defined before they are referenced in a path. Define all boxes, then draw connectors. |
| `\\[-1pt]` inside a node with `align` | Use plain `\\`, control spacing with `inner sep` and `minimum height`. |
| Icon crops contain neighbouring text | Always build and view a contact sheet. |
| Figure text at `\tiny` in an 18cm figure | Illegible in print. Scale type to the column. |
| A side label clipped by the next column | The label's `text width` plus its x must clear the next rule. Narrow the *boxes*, not the label — a truncated number is a wrong number. |
| An annotation wraps into an ugly break (`PPV 0.93 →` / `0.006`) | Break it yourself with `\\` at the meaningful place rather than letting the width decide. |
| An icon floating between two rows it does not belong to | Every pictogram must sit level with the thing it illustrates, and carry a label. Otherwise move it or cut it. |
| `\foreach \n in {...} {\draw (x,0) -\| (\n.west);}` | `-\|` routes through the shared y, producing a detour through the bottom of the figure. Iterate over node/ordinate pairs and draw straight. |
| Style file `\input` after `\begin{document}` | Colour and `\tikzset` definitions must precede the document body of the standalone figure file. |
| TikZ written inline in `main.tex` | Never. Figures live in `figures/<name>.tex`, compile to PDF, and the paper uses `\includegraphics`. |
| Figure compiled from the repo root | `\input{figstyle}` and the icon paths are relative to `figures/`. Compile from inside `figures/`. |
| Edited `figures/<name>.tex` but the paper shows the old figure | The manuscript reads the PDF. Recompile the figure before the paper. |

## What to report back

State plainly:

- which source images were used, and how they were chosen;
- the path of each `figures/<name>.tex` and its compiled `figures/<name>.pdf`;
- every **error found in the render**, with what the evidence says instead;
- any error found **elsewhere in the paper** while wiring the figure in — this
  is common, because rebuilding a figure forces you to check its numbers
  against the results, and hand-written tables nearby are often stale;
- confirmation that the text is selectable, with the probe output.

Never claim the figure is "publication ready" without having viewed the
rendered page.

## Trigger phrases

Moved here from the description so it fits the 1024-character limit of the Agent Skills specification. Use this skill on requests such as "rebuild my figure", "convert this figure to TikZ", "make the figure text selectable", "remove the title from the figure", "use the figure in downloads", "use this style for my figures", "make the figures match", "add more icons", "make my figure publication quality", "fix my figure", "vectorise this diagram", or when image files are supplied alongside a LaTeX manuscript. Do not use it for plotting data series from a CSV (write matplotlib/pgfplots directly), for prose editing, or for generic image editing with no paper attached.
