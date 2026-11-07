# Paper Blueprint and Section Recipes

Write the blueprint into `PAPER_REPORT.md` before drafting any LaTeX. The draft follows the blueprint. When the draft needs a change, change the blueprint first.

## Blueprint contents

1. **Problem.** One paragraph: who has the problem, at what scale, and what it costs. Each fact cites a retrieved source.
2. **Gap.** What the reviewed work leaves open, naming the papers that show it (from `_build/sources.csv`). Calibrate the wording to the search: "none of the N reviewed systems combines X with Y" beats "no prior work". Use "first" only when the search supports it, and then name the search.
3. **Research questions.** Two to four, each answerable by one experiment. Supplied questions are used verbatim.
4. **Contributions.** Three to five. Each names a concrete artifact (a framework, an algorithm, a formal model, a protocol, an evaluation) and the section that delivers it. The last contribution is usually the evaluation.
5. **Method.** Components, their inputs and outputs, and how data flows between them. This drives Fig. 1 and Sections III to V.
6. **Notation.** Every symbol with its meaning and type. Equations use only these symbols.
7. **Equations.** Six to twelve numbered equations: system model, objective or loss, the key update or scoring rule, constraints, a complexity or cost expression, and the metric definitions the paper relies on.
8. **Algorithms.** One or two, each with inputs, outputs, and a complexity statement.
9. **Figure plan and table plan.** See the minimum sets below.
10. **Target sheet.** `_build/targets.py`, built by the rules in results-and-targets.md.
11. **Page budget.** The table below, adjusted to the user's page range.

## Section recipes (7-page IEEE conference paper)

The order below is the default. A structure the user supplies wins.

| Section | Pages | Must contain |
|---|---|---|
| Title, authors, abstract, index terms | 0.35 | Abstract 150 to 250 words: problem, gap, method, evaluation setting, headline result with its comparison point, one implication. Four to six index terms |
| I. Introduction | 0.9 | Motivation with cited facts, the gap, the research questions, the contribution list (`itemize`), one sentence on the evaluation. Skip the "rest of the paper is organized" paragraph unless space is free |
| II. Related Work | 0.8 | Three or four thematic subsections that compare approaches, then a comparison table of prior work against the paper's design dimensions. End with the gap |
| III. Proposed Framework | 0.7 | Design goals, assumptions, threat or trust model when security is in scope, method overview, workflow figure |
| IV. System Architecture | 0.6 | Full-width architecture figure, each component in data-flow order, interfaces between components |
| V. Mathematical Model and Algorithms | 0.9 | Problem formulation, equations, algorithm, complexity analysis. Define every symbol before its first use |
| VI. Experimental Setup | 0.6 | Datasets (with verified statistics and citations), splits, baselines with citations, metrics with definitions, implementation and hyperparameter table, hardware (marked), seeds, experimental pipeline figure |
| VII. Results and Discussion | 1.2 | Main comparison table and figure, convergence or learning curves, ablation, scalability, robustness or security analysis, runtime and overhead. One paragraph answers each research question by number |
| VIII. Comparative Analysis | 0.35 | Against the strongest prior systems on accuracy, cost, and assumptions, including where the method loses |
| IX. Limitations | 0.2 | Specific to this design and evaluation: data scope, threat model limits, simulation versus deployment, cost |
| X. Conclusion and Future Work | 0.25 | What the paper showed with the headline number, two or three specific next steps. No new claims |
| References | 0.9 | 25 to 40 verified entries |

About 4,000 to 4,600 words of prose fit seven pages with this float load. Count with `texcount` when it is installed, or estimate from the PDF.

## Minimum figure and table set

Figures (all TikZ or PGFPlots, recipes in latex-and-figures.md):

1. Architecture, full width (`figure*`).
2. Workflow: the flow that matters for the topic (agent orchestration, data flow, governance loop, security flow, training pipeline).
3. Experimental pipeline: data, preprocessing, splits, training, evaluation.
4. Main comparison chart (bars) matching the main table.
5. A curve: convergence, accuracy against rounds or epochs, or latency against load.
6. Ablation, scalability, or robustness chart.
7. Confusion matrix when the task is classification.

Tables:

1. Prior-work comparison (qualitative, check marks).
2. Dataset summary (verified statistics, `% SOURCE:` tag).
3. Hyperparameters and configuration (`% CONFIG:` tag).
4. Main results.
5. Ablation.
6. Runtime, overhead, or complexity.

Merge or drop items only to meet the page range, and log what was cut.

## Writing rules

- One paragraph per line in the `.tex` file. Press Enter only between paragraphs.
- The user's style rules apply to every sentence: no em dashes, no semicolons, active voice where it reads naturally, specific numbers over adjectives, no stock phrasing ("delve", "leverage", "pivotal", "in conclusion", "not only"). The checker fails em dashes and semicolons. `scan_manuscript.py` lists stock phrasing.
- Tense: present for what the paper proposes and shows ("the framework assigns"), past for what the experiments did ("we trained").
- Cross-references: `Fig.~\ref{}`, `Table~\ref{}`, `Section~\ref{}`, `Algorithm~\ref{}`, `Equation~\eqref{}`. Every float and every numbered equation is referenced in the text, near where it appears.
- Use `itemize` for the contribution list. Use it elsewhere only when items are truly parallel (research questions, design goals). Prose carries the argument.
- Define each acronym once at first use and use it consistently after that. One term per concept.
- Compare studies in related work. A paragraph that summarizes one paper after another is a list, not a review.
- State target results plainly in the paper text. The blue mark and the page-one notice carry their status, so the prose does not need hedging.
