# Website design guidelines

The starter in `templates/starter/` implements this design system and every interaction listed here. Build on it. Do not rewrite `app.js` or the base of `styles.css` for each site. Add site-specific CSS at the end of `styles.css` under a comment `/* Site-specific */`.

## 1. Direction: academic editorial, not a dashboard

The page must read like a well-edited long-form article from a scientific publisher, with figures that teach.

| Do | Do not |
|---|---|
| Warm paper background, white figure cards, one teal accent, amber only for interpretation and worked examples | Gradients, glassmorphism, neon accents, a different color for each card |
| Serif display headings, sans-serif body, monospace for numbers in labels | Decorative fonts, web fonts from a CDN, more than three families |
| A text column of about 68 characters, generous space between sections | Full-width text, dense card grids for prose |
| Numbered sections (01, 02, ...) from CSS counters | Emoji or icons as section markers |
| Visuals that show the real structure of the source | Stock illustrations, decorative diagrams, invented data |
| Quiet motion: none, except the progress bar | Animations on scroll, parallax, auto-playing elements |

You can change the accent hue for a subject (for example a dark green for an ecology paper). Change `--accent` and `--accent-soft` in both themes and keep text contrast at 4.5:1 or more. Change nothing else in the token set without a reason.

## 2. Tokens

All colors are CSS custom properties on `:root`, redefined in `:root[data-theme="dark"]` and in the `prefers-color-scheme: dark` fallback. Never write a hex color in markup or in an SVG attribute. Use the classes in section 5, which read the tokens, so that dark mode works everywhere.

| Token | Use |
|---|---|
| `--paper`, `--surface`, `--surface-2` | page, cards and figures, code and inner panels |
| `--ink`, `--ink-2`, `--ink-3` | body text, secondary text, captions and labels |
| `--rule` | borders and grid lines |
| `--accent`, `--accent-soft`, `--accent-ink` | links, nodes, active states, text on accent |
| `--mark`, `--mark-soft` | interpretation callouts, worked examples, focus ring of diagram nodes |
| `--warn`, `--warn-soft` | gap callouts, failure paths in diagrams |

Type: `--font-body` (system UI), `--font-display` (Palatino and Georgia family), `--font-mono`. Body 17 px on desktop and 16 px on phones, line height 1.65.

## 3. Layout and responsive rules

- Mobile first. The page has a 16 px gutter at every width and never scrolls sideways.
- At 980 px and wider, the section list is a sticky sidebar. Narrower, it is a closed disclosure at the top of the page.
- Wide figures scroll inside `.diagram-scroll` or `.table-wrap`, never the page. Give a wide SVG a minimum width with `style="--diagram-min: 640px"` so that its labels stay at 12 px or larger on a phone.
- Prefer diagrams that flow from top to bottom, with a viewBox of about 560 to 640 units wide. They scale down well. Use a wide layout only for architectures that are wide by nature.
- Check every page at 375 px, 768 px, and 1280 px.

## 4. Components

Every component is in `templates/starter/index.html` with a comment that tells when to use it. Delete what the source does not need.

| Component | Use it for | Rules |
|---|---|---|
| Lead paragraph `.lead` | the first paragraph of a section | It must make sense alone. |
| Two levels `.explain` | any idea with a simple and a technical form | `.simple` first and always visible. `details.technical` holds the exact terms, notation, and references. The technical text must keep the scientific meaning. |
| Concept cards `.concepts` | 3 to 9 difficult terms | Term, simple meaning, function in the source, example. The term links to its glossary entry. |
| Callouts `.callout` | source claims, interpretation, missing information, limits | Use `from-source` with a reference, `interpretation` for your analysis, `gap` for missing information, `limit` for limits. Never put your analysis in a `from-source` callout. |
| Diagram `figure.diagram` | architectures, pipelines, frameworks | See section 5. |
| Steps `ol.steps` | methods, workflows, algorithms | One step for each item, with input, output, and a reference. |
| Equation `figure.equation` | each important equation | See section 6. |
| Code `figure.code` | exact excerpts | `app.js` adds the copy button. Give the file and the lines. |
| Data table `table.data` | results, comparisons | Real values only. `data-bar-max` adds value bars. See section 7. |
| Glossary `dl.glossary` | every technical term | `id="g-<term>"`. The first `<p>` is the tooltip text, so it must be short. |
| Term link `a.term-ref` | first use of a term in a section | `href="#g-<term>"`. `app.js` shows the definition on hover and focus. |
| Important items `ol.takeaways` | the last content section | 3 to 7 items, one idea each. |
| Sources `ol.sources` | references | `data-ste="skip"`. Exact references only. |

Interaction features and when to keep them:

| Feature | Keep it when |
|---|---|
| Section list with active section, progress bar, go-to-top control | always |
| Dark mode control | always |
| "Show all technical explanations" control | the page has `details.technical` (`app.js` hides it otherwise) |
| Interactive diagram | the source has components that connect |
| Glossary filter and tooltips | the glossary has 6 or more terms (tooltips always help) |
| Copy buttons | the page shows code |
| Value bars | a table shows comparable numbers |

## 5. Diagrams

A diagram must show the real structure of the source. Every node is a component that the source names, and every arrow is a flow that the source describes. If you combine or simplify parts, say so in the figure note.

Build:

1. List the nodes and edges first, with a source reference for each, in `_qa/source-map.md`.
2. Put nodes on a grid. Node height 56 to 72 units. Node width about 7.5 units for each character of the longest label plus 32. Keep 40 units or more between nodes. Labels have a maximum of about 22 characters. Put a second line in `<text class="sub">` or `<tspan>`.
3. Draw orthogonal connectors (`H` and `V` path commands, with small `Q` corners). Label each edge with what flows: data, a signal, a decision.
4. Give each figure its own marker id (`arrow-<figure id>`), because ids must be unique on the page.
5. Group a subsystem with `<rect class="group">` and a `<text class="group-label">`.

Classes (they use the tokens): `.node` with `data-node="<id>"`, `.edge`, `.edge.alt` (dashed: optional or fallback path), `.edge.warn` and `.arrowhead.warn` (failure or block path), `.edge-label`, `.group`, `.group-label`, `.sub`.

Accessibility: the `<svg>` has `role="img"`, a `<title>`, and a `<desc>` that tells the full flow in one or two sentences. `app.js` makes each `.node` a keyboard button. Each node has a `.node-info` block with the same name, its function, input, output, and a reference. Without JavaScript all blocks stay visible, so the diagram is never the only place where information is.

Labels: every figure needs a figure number and caption, and a `.figure-note` with its source. When the figure is not a reproduction of a source figure, write the note in STE: "This diagram shows the structure of Section 3 of the source. It is not a copy of a figure of the source." ("Conceptual illustration based on" is not STE: "conceptual" is not in the dictionary and "base" is not approved.) Never reproduce a figure from a paper as an image. Redraw the structure.

Node variants: `.node.key` (the central component, amber), `.node.ok` (a decision that continues), `.node.hold` (dashed: wait or escalate), `.node.stop` (red: block or fallback). Pair each with a label, because color must not carry the meaning alone.

Screen-reader text: `.sr-only` spans are absolutely positioned. The starter makes every scroll container `position: relative` so that these spans stay clipped. Keep that rule, or a wide table widens the whole page on a phone.

Source references: `.src` is for short references such as "(Section 3, page 4)". Write longer notes as normal text.

Flowcharts: decisions are `<polygon>` diamonds inside a `.node`. Label the exits "Yes" and "No", or with the condition. Mermaid needs a script from the network, so do not use it unless the user agrees to network access.

## 6. Mathematics

- Display equations with native MathML (Chrome, Edge, Firefox, Safari). Keep the LaTeX of the source in `<annotation encoding="application/x-tex">`.
- Copy the notation exactly. Do not rename symbols. If you must add explanatory notation, say so.
- Give every symbol in the symbols table, with its name, function, and unit or type. If the source does not define a symbol, say so in the table.
- A worked example uses values from the source when they exist. Otherwise label the inputs "example values, not from the source", and calculate the result correctly. Check the arithmetic with Python.
- Chromium supports MathML Core, which ignores `mathvariant="bold"` and similar values. For bold or blackboard letters, write the Unicode mathematical characters: 𝐱, 𝐖, 𝔼, ℝ, 𝒩.

MathML patterns:

```html
<mfrac><mi>a</mi><mi>b</mi></mfrac>                                   <!-- a/b -->
<msub><mi>x</mi><mi>t</mi></msub>   <msup><mi>x</mi><mn>2</mn></msup>   <!-- x_t, x^2 -->
<msubsup><mi>σ</mi><mi>i</mi><mn>2</mn></msubsup>                     <!-- σ_i^2 -->
<munderover><mo>∑</mo><mrow><mi>i</mi><mo>=</mo><mn>1</mn></mrow><mi>N</mi></munderover>
<mover><mi>x</mi><mo>^</mo></mover>   <mover><mi>x</mi><mo>¯</mo></mover>   <!-- hat, bar -->
<munder><mi>arg max</mi><mrow><mi>a</mi><mo>∈</mo><mi>𝒜</mi></mrow></munder>
<mrow><mo>‖</mo><mi>𝐱</mi><mo>‖</mo></mrow>                            <!-- norm -->
<mrow><mo>{</mo><mtable>
  <mtr><mtd><mn>1</mn></mtd><mtd><mtext>if </mtext><mi>x</mi><mo>≥</mo><mn>0</mn></mtd></mtr>
  <mtr><mtd><mn>0</mn></mtd><mtd><mtext>otherwise</mtext></mtd></mtr>
</mtable></mrow>                                                        <!-- cases -->
```

Use Unicode operators: ≤ ≥ ≠ ≈ ∈ ∉ ⊆ ∀ ∃ → ⇒ ∞ ∂ ∇ · × ∧ ∨ ¬ ∑ ∏ ∫. Inline math in a sentence: `<math><msub><mi>p</mi><mi>t</mi></msub></math>`.

## 7. Charts and results

- Use only values that are in the source. Copy them exactly, with their units, signs, and uncertainty (for example "87.3 ± 0.4"). Give the table, figure, and page.
- For a few values, a `table.data` with value bars is the best chart: the numbers stay exact and readable, and the bars show size. Set `data-bar-max` to a round axis maximum and `data-bar-min` when the axis does not start at zero. Say in the caption which direction is better.
- For series (training curves, time series), draw an inline SVG line chart from the source values. Give axes, ticks, units, a legend, and the data table in a `details` element. Never smooth, fit, or extrapolate.
- If the source gives results only as a plot without numbers, do not read values from the plot as if they were exact. Describe the trend in words and cite the figure.
- If the `dataviz` skill is installed, read it before you draw a chart.

## 8. Accessibility (WCAG 2.2 AA basics)

- One `h1`, then `h2` for sections and `h3` inside them. No skipped levels.
- `lang="en"`, a skip link, `<nav aria-label>`, `<main>`, and `<footer>` landmarks.
- Text contrast 4.5:1 or more in the two themes, 3:1 for large text and for graphic parts that carry meaning.
- Every control works with a keyboard and shows a visible focus ring. Touch targets are 24 by 24 px or larger.
- Color never carries information alone. Pair it with a label, a line style, or text.
- Images have `alt`. SVGs have `role="img"` with `<title>` and `<desc>`, or `aria-hidden="true"` when they are decoration.
- Tooltips open on focus as well as hover, stay open while the pointer is on them, and close with Escape. The same text is in the glossary.
- `prefers-reduced-motion` turns off smooth scrolling.

## 9. Offline and size

- No request to the network: no CDN script, web font, or remote image. The page must work from `file://`.
- Diagrams are inline SVG, so that they follow the theme and can be interactive. Put a file in `assets/` only when it is a static image that needs no theme, and reference it with a relative path.
- Keep `index.html` below about 1 MB.

## 10. Visual check in a browser

Open the page with `playwright-cli` or a browser tool when one is available. Check at 1280 px, 768 px, and 375 px:

- No console errors. No sideways page scroll.
- The section list builds, the active section changes on scroll, and the links go to their sections.
- The dark mode control changes the theme, the choice stays after a reload, and diagrams and tables stay readable in the two themes.
- Each diagram node opens its panel with a click and with Enter.
- Technical explanations open, and the "Show all" control opens all of them.
- The glossary filter hides terms that do not agree with the filter. A term link shows its tooltip on hover and on focus, and Escape closes it.
- The copy button copies the code.
- MathML renders as mathematics, not as raw text.

Take screenshots of the light and dark themes at desktop and phone widths, look at them, and fix what looks wrong. If no browser tool is available, say which checks you could not do.

Optional design help: when the `design-taste-frontend` or `impeccable` skill is installed and the user wants extra polish, you can use it for a critique pass. The rules in this file still apply.
