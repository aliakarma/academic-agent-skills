# The editorial-schematic style

This is the visual language to reach for when the user supplies a reference
render and says "use this style", and the default target when they ask for a
figure that looks professional rather than like a slide.

It is the house style of editorial infographics: a **quiet, near-neutral page**
with a small number of **muted accents**, organised into **labelled columns**,
where the reader's eye is carried by **numbered step badges** rather than by
colour shouting. Nothing is saturated. Nothing is 3-D. Nothing has a drop
shadow. The information does the work.

Sample the palette from the user's render; do not copy the hex values below
verbatim unless sampling produced them. What generalises is the **structure**,
not the exact colours.

---

## 1. The palette has five roles, not five colours

| Role | Typical value | Used for |
|---|---|---|
| Ink | `272B2E` near-black | headings, numerals, box strokes that matter |
| Mute | `8A9095` warm grey | column headers, secondary labels, the flow line |
| Rule | `D6D9DC` | hairline separators, inactive strokes |
| Panel | `F4F6F6` | panel fills, enclosures |
| Empty | `D9DCE1` | unfilled capacity blocks |

Then **at most three accents**, each with a pale variant for fills:

| Accent | Typical | Pale | Means |
|---|---|---|---|
| Teal | `3C7D85` | `B2CBC5` | the primary subject of the figure |
| Green / sage | `7FA86B` | `CAD5C5`, sage `CDD8D4` | the secondary stream |
| Coral | `E2795E` | `EBC6B4` | attention, control paths, the bad news |
| Slate | `5A6B7D` | — | ordinary data connectors |

Rules that keep it from going gaudy:

- **Strokes are the accent, fills are the pale variant**, usually further
  diluted (`fill=fgTealL!40`). A saturated fill instantly looks like a slide.
- **Coral is a budget.** One or two elements per figure. It is the colour of
  the thing the reader must not miss — the failure, the control loop, the
  dominant cost.
- **Never colour-code more than three things.** If the figure needs more
  distinctions, distinguish them by shape, stroke weight, or badge number.

---

## 2. Columns with grey headers over hairline rules

The page is divided into 3–5 vertical columns, one per stage of the story.

```latex
\foreach \x in {4.86, 13.42} {\draw[colrule] (\x,-1.30) -- (\x,8.05);}
\node[colhdr] at (2.15,8.42) {TRAINING PROTOCOL};
\node[colhdr] at (8.95,8.42) {EVALUATION LADDER};
```

- Headers are **uppercase, bold, small, and grey** — `\scriptsize\bfseries`
  in Mute. They are signposts, not titles; they must recede.
- The rule is a **hairline** (0.6pt) in Rule grey, running the full height of
  the content, ending *above* the header so the header floats free of it.
- Each header is centred **over its own column's content**, which is rarely
  the midpoint between two rules. Centre it on the content, then check the
  render.
- There is **no title**, no frame around the figure, no background tint.

## 3. Numbered step badges carry the sequence

A single flow line threads circular numbered badges down or across the figure.

```latex
\node[badge]  (n1) at (5.40,7.28) {01};   % sage   -- the reference case
\node[badgeG] (n2) at (5.40,5.52) {02};   % green
\node[badgeT] (n3) at (5.40,3.76) {03};   % teal
\node[badgeC] (n4) at (5.40,1.62) {04};   % coral  -- the operational reality
```

- Two-digit zero-padded numerals (`01`, not `1`). This is the single strongest
  signal of the style.
- ~5.4 mm circles, ink stroke, pale accent fill, `\tiny\bfseries` ink numerals.
- **Let the fill deepen along the sequence** when the sequence is an argument:
  sage → green → teal → coral says "this is getting more serious" without a
  word of text. If the badges are merely an inventory, keep them one colour.
- The flow line is Mute, 0.7 pt, with a small `Latex[length=1.7mm]` head. It
  enters each badge from the spine and leaves for the content.
- A **vertical spine** dropped from the source node, with a `callout` label at
  its top (`ONE TRAINED DETECTOR`), tells the reader that everything hanging
  off it shares one origin. Very cheap, very legible.

## 4. Cards, panels and enclosures

- `card` — white, 0.9 pt ink-70 stroke, 2.4 pt rounded corners. The things the
  figure is *about*.
- `panel` — Panel grey fill, Rule stroke. Supporting commentary, legends, the
  "how to read this figure" box.
- `dashbox` — dashed Mute enclosure over a Panel fill. A boundary that groups
  (a platform, a trust domain), not a thing in itself.
- Corner radius is **2.4 pt everywhere**. Mixed radii look accidental.
- Heading line in `\textbf{}`, detail lines in `\tiny`. Two type sizes inside
  a card, never three.

## 5. The four idioms that make it look designed

**Capacity blocks** — a row of small squares, *n* filled in an accent and the
rest in Empty, for "this stage is 8/10 of the budget". Far more legible at
figure scale than a pie or a bar, and it echoes the badge numerals.

```latex
\capblocks{13.78}{3.12}{8}{10}{fgCor}
\node[font=\tiny, text=fgMute, anchor=west] at (16.08,3.14) {feature construction};
```

**Chevron chains** — `shapes.symbols`'s `signal` shape for a pipeline of
stages, with exactly one chevron in coral where the cost or the risk sits.

```latex
chev/.style   ={draw=fgSlate!70, fill=fgPanel, signal, signal to=east,
                signal pointer angle=120, font=\tiny, align=center},
chevhot/.style={chev, draw=fgCor, fill=fgCorL!55, line width=1.3pt},
```

**Hatching for the inactive arm** — anything designed and not executed is
drawn with `patterns`' `north east lines` in Mute-40 behind a dashed Mute
stroke, and labelled in words. It stays in the figure; it just cannot be
mistaken for something that happened.

**Callouts on the rules** — a `\tiny` ink label with `fill=white, inner sep=1.5pt`
placed directly on a rule or a connector, which knocks out the line behind it.
This is how the style annotates without leader lines. Use it any time a label
must sit on top of artwork.

## 6. Connectors

| Style | Weight | Meaning |
|---|---|---|
| `dataflow` | Slate 0.8 pt, small arrowhead | ordinary data movement |
| `hairflow` | Slate-55 0.45 pt, no head | many-to-one fan-in (device populations) |
| `tealflow` | Teal 1.0 pt | the path the figure is arguing about |
| `corflow` | Coral 0.9 pt **dashed** | control, feedback, mitigation |
| `stepflow` | Mute 0.7 pt | the badge sequence |

Dashing means *control or hypothetical*, never merely "another kind of data".
Keep it consistent or the legend becomes a lie.

## 7. Type scale

`\scriptsize` bold for column headers and card headings; `\scriptsize` for
primary labels; `\tiny` for detail lines, callouts and legends. **Three sizes
total.** Never smaller than `\tiny`, and check legibility at the printed
column width, not on screen.

## 8. Icons

Pale, line-drawn, roughly uniform optical weight, 4–6 mm high, always with a
`\tiny` label beneath or beside. They sit *next to* boxes rather than inside
them, so the box text stays a clean rectangle.

The user's "you can add more icons" means: give every named entity a
pictogram, and give the abstract transitions one too — a distribution-shift
curve beside the corpus that shifted, a warning triangle on the arm that was
not executed. An icon with no label, or an icon floating between two things it
does not connect, reads as decoration and should be moved or cut.

---

## Checklist before you call it done

- [ ] No title inside the artwork.
- [ ] Column headers uppercase, grey, above the rules, centred on content.
- [ ] Badges zero-padded, one consistent size, fills ordered if the order means
      something.
- [ ] At most three accents; coral spent on at most two elements.
- [ ] One corner radius throughout; three type sizes at most.
- [ ] Every label that crosses a line has `fill=white`.
- [ ] Nothing unexecuted drawn in the same style as something executed.
- [ ] Both figures in the paper `\input` the same style file.
