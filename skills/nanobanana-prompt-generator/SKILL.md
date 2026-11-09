---
name: nanobanana-prompt-generator
description: Use when a paper's TikZ diagrams (architecture, framework, pipeline, workflow, flow, system, or concept diagrams in figures/tikz/ or inline in the manuscript) need NanoBanana prompts for Google Gemini or Google Flow, to produce reference images for figure-rebuild, or when one TikZ snippet, diagram image, or description must become a NanoBanana prompt. Trigger on "nanobanana", "nano banana prompts", "prompts for my TikZ figures", "Gemini prompts for my figures", "reference images for figure-rebuild". Never for results figures (plots, charts, curves, or any diagram that shows measured or computed values).
---

# NanoBanana Prompt Generator

> **Paths.** `${CLAUDE_SKILL_DIR}` is the folder that holds this SKILL.md. Claude Code fills it in. In other agents, replace it with that folder's path.

## Overview

This skill turns a paper's TikZ diagrams into NanoBanana prompts and guides the user through the whole pipeline:

```
figures/tikz/<name>.tex  --this skill-->  figures/nanobanana/<name>.txt  (prompt)
   --user, Google Gemini or Google Flow-->  figures/<name>.jpg  (reference image)
   --figure-rebuild-->  figures/<name>.tex + figures/<name>.pdf  (final vector figure)
```

**The most important rule: results figures never get a prompt.** An image model redraws whatever it is given, so on a results figure it would invent bars, curves, and numbers. Only architecture, framework, pipeline, workflow, flow, system, and concept diagrams are eligible.

## Results figures are never eligible

Run the scanner first. It lists every TikZ figure with a status:

```
python "${CLAUDE_SKILL_DIR}/scripts/find_tikz.py" .
```

| Status | Meaning | What to do |
|---|---|---|
| EXCLUDE | Plot code: pgfplots axis, `\addplot`, plotted coordinates or files, bar or pie charts, error bars | Results figure. No prompt, ever. Do not read it further |
| REVIEW | A results hint in the caption, label, or node text (accuracy, comparison, ablation, `94\%`, `\pm`) | Read the code and the caption, then apply the test below |
| CANDIDATE | No results signal | Read it anyway, then apply the test below |

A figure is a results figure, and gets no prompt, when any of these is true:
- it shows a measured or computed value: a metric, score, error, timing, count from an experiment, or a percentage that is an outcome;
- it compares methods, settings, or conditions by their outcomes, including rankings and "better than" arrows;
- its caption presents it as results, evaluation, performance, comparison, ablation, or analysis of outcomes;
- it is a diagram with even one result value in it (for example a pipeline box reading "Acc. 94.2%"). Exclude the whole figure. Never delete the numbers to make it eligible.

These are not results: a box labeled "Results" or "Evaluation" with no values in it, layer sizes, a 70/30 data split, and hyperparameter values in a configuration box. **When in doubt, exclude** and give the reason. If the user asks for an excluded figure, read it again. Write a prompt only when it holds no result at all, and never for an EXCLUDE figure.

## Batch mode (the skill is invoked without a specific diagram)

1. Run the scanner from the project root. If it finds nothing, say so in one line and stop.
2. Read every CANDIDATE and REVIEW figure in full, with its caption, and decide eligibility by the test above.
3. For each eligible figure, write `figures/nanobanana/<name>.txt` holding the prompt only: no code fence and no commentary, so the user can select all and copy. If the file already exists, keep the old one as `<name>.txt.bak` first.
4. Write `figures/nanobanana/GUIDE.md` in the format below.
5. Reply with the number of prompts written, the excluded figures and the reason for each, the steps from the guide, and the guide's path.

Do not edit `figures/tikz/`, the manuscript, or any figure file.

## Single mode (the user gives one TikZ snippet, diagram image, or description)

Apply the results test first. If it is a results figure, reply in one line that results figures get no prompt, and why. Otherwise reply with only the NanoBanana prompt in a single code block. Do not generate TikZ and do not explain the diagram.

## Writing each prompt

### Adaptation (before writing)

- Understand the diagram deeply: identify every component, grouping, data/control flow, and hierarchy.
- Preserve technical meaning exactly: component names, directionality, loops, feedback paths, and labels that carry meaning.
- Improve clarity where needed: regroup into logical stages, remove redundancy, untangle crossing flows, shorten labels to keywords.
- Enhance visual hierarchy: main pipeline vs. auxiliary modules, inputs vs. core vs. outputs.
- Optimize for NanoBanana output quality: concrete spatial positions, explicit counts, explicit arrow sources and targets.

### Fidelity (figure-rebuild audits the image against the TikZ)

- Use the component names and labels from the TikZ, shortened to keywords but never renamed.
- Always improve the design, never the content. Improving means layout, grouping, hierarchy, and icons. Never add a component, arrow, data value, number, or claim that the TikZ does not contain.
- Choose the aspect ratio from the figure's width: 16:9 for a wide figure (`figure*`, `\textwidth`), 4:3 for a single-column figure. The scanner reports `wide` or `column`.

### Output requirements (STRICT)

**1. Structure.** Every prompt contains these sections, in this order: Title, Visual Style, Icon Requirements, Layout Structure, Component Breakdown, Flow Design, Layout Rules, Output Requirements, Final Instruction.

**2. Visual style (MANDATORY).** Minimalist academic infographic, white background, light pastel color palette, rounded containers, thin light-grey arrows, soft shadows, modern sans-serif typography, clean spacing and symmetry, publication quality (IEEE / Elsevier level).

**3. Icons (CRITICAL).** Colorful 2D flat icons: not 3D, not monochrome. Each component has an icon, and the prompt names a specific icon for each one. Icons are clearly visible and consistent. Always include this exact line: "Use clear, colorful 2D flat icons for all components with consistent style."

**4. Layout rules.** Perfectly aligned, symmetric spacing, no clutter, no crossing arrows, minimal text (keywords only), consistent box sizes.

**5. Style consistency.** Clean, modern, visually balanced, reviewer-friendly, and suitable for Q1 papers.

**6. Tone.** Professional, precise, and structured, with no unnecessary explanation and no emojis inside the prompt.

### Template

Fill this template for every diagram. Adapt the section contents, but never drop a section:

```
Title:
[Concise figure title]

Visual Style:
Create a minimalist academic infographic on a pure white background with a light pastel color palette ([assign pastel colors to each stage/group]). Use rounded containers, thin light-grey arrows, soft shadows, modern sans-serif typography, and clean spacing with symmetry. The figure must be publication-quality at IEEE / Elsevier level.

Icon Requirements:
Use clear, colorful 2D flat icons for all components with consistent style.
Icons must not be 3D and must not be monochrome. Every component includes one clearly visible icon:
- [Component]: [specific icon]
- ...

Layout Structure:
[Overall orientation (left-to-right / top-to-bottom), number of stages or panels, grouping containers, relative positions]

Component Breakdown:
[Stage/Group 1 name] ([pastel color] container):
- [Component]: [keyword label]
- ...
[Stage/Group 2 name] (...):
- ...

Flow Design:
- [Source] -> [Target]: [keyword label, if any]
- [Feedback/loop paths routed around the outside to avoid crossings]
- ...

Layout Rules:
- Perfectly aligned components with symmetric spacing
- No clutter and no crossing arrows
- Minimal text, keywords only
- Consistent box sizes within each group
- Clear visual hierarchy: [what is emphasized]

Output Requirements:
- High-resolution academic figure, [16:9 for a wide figure or 4:3 for a single-column figure]
- Clean, modern, visually balanced, reviewer-friendly
- Suitable for a Q1 journal paper
- All text legible at print size
- Render only the component and group labels listed above as text. Do not render a figure title, a caption, any number that is not in those labels, or the words of these instructions

Final Instruction:
Generate a clean academic figure with strong visual hierarchy, clear structure, and a consistent pastel design that is ready for publication in a high-impact journal.
```

## GUIDE.md format

Write `figures/nanobanana/GUIDE.md` with these parts, in this order:

1. A title and one sentence: results figures are excluded and stay as data-driven plots.
2. **Steps**, repeated for each figure in the table:
   1. Open Google Gemini (gemini.google.com) or Google Flow and choose image generation with a Nano Banana model. Start a new chat or project for each figure, so one figure's style does not carry into the next.
   2. Open the figure's prompt file, select all, copy, paste it into Gemini or Flow, and generate.
   3. Check the image against the "Must show" column: every component, every arrow direction, no extra boxes, and no numbers that the TikZ does not contain. Small spelling slips in labels are fine, because figure-rebuild retypes all text as vector text. Regenerate if a component is missing, renamed, or added.
   4. Download the full-resolution image and save it under the exact name in the "Save image as" column. A `.png` download is fine too, if you keep the same name.
   5. Tick the figure's box.
3. **What to do when all images are saved:** tell Claude "The NanoBanana images are in figures/. Check them and run figure-rebuild."
4. **The figure table**, one row per eligible figure, columns in this order: Done (`[ ]`), Figure name, Prompt file, Save image as (`figures/<name>.jpg`), TikZ source (the content source), and Must show (its components and arrows in a few keywords).
5. **The excluded table**, one row per excluded figure: TikZ source and reason.

## When the user has saved the images

1. List which `figures/<name>.jpg` or `.png` files exist and which figures in the guide still lack one.
2. View each image. Compare it with its TikZ source and list missing, renamed, or extra components, reversed arrows, and any number or result text. Ask for a regenerate only for those defects.
3. Tick the finished rows in `GUIDE.md`.
4. Hand off to figure-rebuild, one figure at a time. Tell it that `figures/<name>.jpg` is the reference render (layout, palette, and pictograms) and `figures/tikz/<name>.tex` (or the inline block) is the content source for its Phase 2 audit.

## Red flags: stop

- About to write a prompt for a figure the scanner marked EXCLUDE.
- Deleting numbers from a diagram so it qualifies.
- "It is mostly an architecture diagram, so the one score in it does not count."
- A prompt that names a component, value, or claim the TikZ does not contain.
- A prompt with a code fence inside a `.txt` file, which the user would copy along with the prompt.
