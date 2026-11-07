# Gap Evaluation, Stress Testing, and Writing

## Contents

1. Gap taxonomy
2. Scoring rubric
3. Gates and kill criteria
4. Red flags for weak gaps
5. M9 stress-test protocol
6. Gap-statement formulas
7. Calibrated language bank
8. LaTeX snippets

A note on sources in this file: works named here were checked during skill creation (September 2026) unless tagged `[B]`. Re-retrieve any of them through the normal search protocol before citing them in a user deliverable; do not cite from this file.

---

## 1. Gap taxonomy

Use these to label candidates and to check that the analysis looked in all the usual places.

**By type** (a seven-part taxonomy commonly attributed to Miles, 2017 `[B]`; the same categories appear in recent reviews):
- Evidence gap: findings contradict or are inconsistent (M2)
- Knowledge gap: a question has not been studied, or not studied enough (M1, M3)
- Practical-knowledge gap: practice or policy diverges from, or is unsupported by, research (M11)
- Methodological gap: designs or measures limit what can be concluded (M4)
- Empirical gap: propositions or claims lack empirical evaluation (M3, M4)
- Theoretical gap: theory is missing, incomplete, or contradicted (M6, M12)
- Population gap: groups or contexts are under-represented (M5)
- Plus, for this skill: temporal/data gap (M8) and variable/relationship gap (M7)

**By reason the evidence falls short** (Robinson et al., 2011, Journal of Clinical Epidemiology, verified): insufficient or imprecise information; biased information; inconsistency or unknown consistency; not the right information. Characterize where the gap sits using PICOS elements (population, intervention, comparison, outcomes, setting). This is especially useful for health and applied work.

**By construction mode** (Sandberg and Alvesson, 2011, Organization, verified; subtype names `[B]`): confusion spotting (competing explanations), neglect spotting (overlooked area, under-researched area, lack of empirical support), and application spotting (extending a theory or perspective to a new area). The alternative is **problematization** (Alvesson and Sandberg, 2011, Academy of Management Review, verified): challenging assumptions (M12). Editorials in information systems have also criticized over-reliance on gap-spotting (Chatterjee and Davison, 2020, Information Systems Journal, verified), which is why significance is scored separately from existence below.

**Rigor frameworks** worth knowing: Müller-Bloch and Kranz (2015, ICIS proceedings; retrieved with incomplete author metadata, so verify) proposed a framework for identifying gaps rigorously in qualitative literature reviews; framework-based reviews such as TCCM, ADO, and 5W+H are summarized by Paul et al. (2023, Journal of Decision Systems, verified).

## 2. Scoring rubric

Score each candidate on six strength dimensions (0–3 each, total 0–18). Show the score table with a one-line justification per cell.

| Dim | Name | 0 | 1 | 2 | 3 |
|---|---|---|---|---|---|
| E | Verified insufficiency | a located study answers it | thin search, or one source suggests the gap | documented searches across 2+ tools find it unanswered or answered weakly | full passes A–F, saturated, including the recency sweep and disconfirmation |
| T | Theoretical significance | none stated | adds a data point | tests or extends a boundary condition, mechanism, or construct | challenges or integrates theory, or resolves a documented contradiction |
| P | Practical significance | none | plausible but vague | clear stakeholder and decision affected | high-stakes, documented need (policy, safety, health, equity) `[S]` |
| N | Non-triviality | pure context, dataset, or keyword swap | swap with a weak rationale | mechanism-based reason to expect a different answer | the answer is genuinely uncertain and either outcome is informative |
| C | Convergence | one source | one lens, several sources | two independent lenses | three or more independent lenses |
| R | Recency robustness | closed by recent work | sweep not done | sweep done, partially overlapping recent work found and differentiated | sweep done, no closing or overlapping work found |

**Classification.**
- **Strong Gap:** total 14–18 and E ≥ 2, N ≥ 2, R ≥ 2, with no kill criterion.
- **Moderate Gap:** total 10–13, or 14+ but failing one gate, with no kill criterion.
- **Weak Gap:** total 6–9, with no kill criterion.
- **Not a Gap:** any kill criterion applies, or total ≤ 5.

**Evidence confidence** (reported next to the classification): High (Deep search, saturated, V2+ on key sources), Medium (Quick search or partial saturation), Low (limited tools, abstracts only, or mostly `[B]`).

**Feasibility and fit** (reported separately, not part of the score): data access, compute, timeline, ethics approval, skills, supervision, cost. Verdict: Go / Conditional (state the conditions) / No-go. Mark "unassessed" if constraints are unknown.

## 3. Gates and kill criteria

Kill criteria (any one makes it Not a Gap in its current form, though it may be reframed):
1. **Already answered.** A located study answers the question with a comparable design and context, and the proposal adds nothing beyond repetition. (A deliberate replication is legitimate if framed as one, with a stated reason such as low power, contested results, or reproducibility concerns.)
2. **Terminology illusion.** The question is well studied under different names.
3. **Superficial novelty.** Novelty is only a new country, sector, dataset, or model with no mechanism predicting a different result.
4. **Closed by recent work.** A recent paper or preprint answers it.
5. **Single-source limitation already addressed.** The gap rests on one paper's stated limitation that later work has addressed.

Gates for Strong: E ≥ 2, N ≥ 2, R ≥ 2.

## 4. Red flags for weak gaps

Treat each as a prompt to dig further, not as automatic rejection.
- "Few studies have examined..." with no search behind it
- "No study has used [method] for [problem]" without explaining what the method reveals
- "First study in [country]" with no mechanism for difference
- Combining two popular technologies or keywords because the combination is unpublished
- A gap drawn from one paper's limitation section
- A gap that exists only within a very narrow year filter
- A gap whose answer is obvious in advance (if every outcome is predictable, the study is not informative)
- A question that cannot be answered with any feasible design
- Novelty that depends on ignoring preprints or adjacent fields
- For the user's own work: overlap with their prior papers that could look like salami slicing

## 5. M9 stress-test protocol

**Stance.** A skeptical PhD supervisor: rigorous, specific, and on the student's side. The goal is a stronger gap, not a demolished one.

**Step 1: Parse the claim.** Restate the proposed gap in one sentence. Extract its components: phenomenon, population or context, method, variables, claimed novelty, and implied contribution. If the claim is ambiguous, list the plausible readings and test the most likely one (say which).

**Step 2: Run the attacks.** For each, report the searches run and what was found.

1. **Prior-work attack.** Search for the claim directly (Pass F) in 2+ tools with 3+ phrasings. Has it already been studied?
2. **Synonym attack.** Rerun with alternative terminology from adjacent communities.
3. **Superficial-novelty attack.** Is the novelty only geographic, sectoral, dataset, or model substitution? Is there a mechanism that predicts a different result?
4. **Already-connected attack.** Have the proposed variables or components already been linked, directly or through a close proxy?
5. **Theoretical "so what" attack.** What would the field believe differently after the study, under each possible outcome?
6. **Practical "so what" attack.** Who would decide or act differently, and is that need documented?
7. **Recency attack.** Recent papers and preprints (last 12–18 months).
8. **Answerability attack.** Can the question be answered with a feasible design, data, and ethics approval?
9. **Self-overlap attack** (when it is the user's own project). Compare with the user's prior work (portfolio and anything the user shared).

**Step 3: Score and classify** using sections 2 and 3. Report evidence confidence and feasibility.

**Step 4: Strengthen.** State concretely what would make the gap more defensible: narrower scope, a mechanism, a competing-theory framing, a different comparison, a design that yields new evidence, or positioning against the closest prior work found.

**Step 5: Rewrite.** Produce an improved gap statement in LaTeX using section 6, citing only ledger sources, and a one-paragraph positioning against the closest prior work.

**Output template.**

```
Verdict: [Strong / Moderate / Weak / Not a Gap]   Evidence confidence: [High / Medium / Low]   Feasibility: [Go / Conditional / No-go / unassessed]

Claim as understood: ...

Attack results
| Attack | Searches run | Finding | Effect on claim |

Score
| E | T | P | N | C | R | Total | Gates passed | Kill criteria |

Closest prior work: [ledger entries] and how the proposal differs

What would make it more defensible: ...

Rewritten gap statement (LaTeX): ...

Remaining uncertainty and what the user should verify: ...
```

## 6. Gap-statement formulas

**Standard (neglect or insufficiency).**
Although [established knowledge] (cites), [specific unresolved question] remains [unexamined / insufficiently examined / unresolved] because [reason: design, context, theory, data limitation] (cites). This matters because [theoretical stake] and [practical stake]. This study addresses the gap by [approach], contributing [contribution type].

**Contradiction.**
Evidence on [relationship] is inconsistent: [group A finding] (cites), whereas [group B finding] (cites). These studies differ in [suspected factor], but no study has [isolated / tested] [factor] directly, based on [search scope]. This study tests whether [factor] explains the divergence.

**Method.**
Existing studies of [phenomenon] rely mainly on [dominant design] (cites), which cannot establish [what is missing: causality, dynamics, real-world validity]. By using [method], this study provides [new kind of evidence].

**Theory.**
[Theory A] explains [X] but assumes [assumption], which leaves [anomaly] unexplained (cites). Integrating [Theory B], which accounts for [mechanism], this study proposes and tests [model].

**Practice/policy.**
[Requirement or need] (primary source) calls for [capability], yet available methods have been evaluated only [limitation] (cites). This study develops and evaluates [approach] against [criteria derived from the requirement].

## 7. Calibrated language bank

Prefer:
- "Based on searches of [tools] through [month year], we found no study that..."
- "To the best of our knowledge, [claim], although work on [adjacent topic] (cite) is related."
- "Evidence on [X] remains limited to [context/design] (cites)."
- "Findings are mixed (cites), and the source of this divergence has not been tested directly."

Avoid:
- "No study has ever..." / "This is the first study to..." without a scoped search statement
- "It is well known that..." without citations
- "Most studies..." without counts from a defined corpus
- Superlatives (novel, groundbreaking, unprecedented) as substitutes for evidence

## 8. LaTeX snippets

**Gap statement box.**

```latex
\begin{quote}
\textbf{Research gap.} Although ... \citep{keyA,keyB}, ... remains unresolved because ... \citep{keyC}.
This matters because ... . This study addresses the gap by ... .
\end{quote}
```

**Research questions and hypotheses.**

```latex
\begin{enumerate}[label=\textbf{RQ\arabic*.}, leftmargin=*]
  \item ...
\end{enumerate}
\begin{enumerate}[label=\textbf{H\arabic*.}, leftmargin=*]
  \item ... (direction and rationale)
\end{enumerate}
```

**Evidence matrix.**

```latex
\begin{table}[t]
\centering
\small
\caption{Synthesis matrix supporting the research gap.}
\label{tab:synthesis}
\begin{tabularx}{\linewidth}{@{}lX@{}}
\toprule
Dimension & Evidence \\
\midrule
Established & ... \citep{} \\
Disputed & ... \citep{} \\
Understudied & ... \citep{} \\
Methodological limitations & ... \citep{} \\
Theoretical failures & ... \citep{} \\
\bottomrule
\end{tabularx}
\end{table}
```

**Conceptual model (TikZ).**

```latex
\begin{figure}[t]
\centering
\begin{tikzpicture}[
  node distance=1.2cm and 2.2cm,
  box/.style={draw, rounded corners, align=center, minimum width=2.8cm, minimum height=0.9cm, font=\small},
  arr/.style={-Stealth, thick}]
  \node[box] (x) {Predictor $X$};
  \node[box, right=of x] (m) {Mediator $M$};
  \node[box, right=of m] (y) {Outcome $Y$};
  \node[box, above=of m] (w) {Moderator $W$};
  \draw[arr] (x) -- node[above, font=\scriptsize]{P1 (+)} (m);
  \draw[arr] (m) -- node[above, font=\scriptsize]{P2 (+)} (y);
  \draw[arr] (w) -- node[right, font=\scriptsize]{P3} ($(x)!0.5!(m)$);
  \draw[arr, dashed] (x) to[bend right=25] node[below, font=\scriptsize]{P4 (direct)} (y);
\end{tikzpicture}
\caption{Conceptual model. Propositions P1--P4 are derived in Section~X.}
\label{fig:model}
\end{figure}
```

Required packages: `booktabs`, `tabularx`, `enumitem`, `tikz` with `\usetikzlibrary{arrows.meta,positioning,calc}`, and `natbib` (or the venue's citation package).
