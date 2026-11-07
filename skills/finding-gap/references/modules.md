# Module Protocols

Detailed procedures for every module. Each section has the same parts: purpose, inputs, search moves, procedure, output template, and quality bar. Read only the sections for the modules being run.

Throughout: tag claims `[S]`, `[U]`, `[B]`, `[I]`; cite only Source Ledger entries; use counts only from the coded corpus. See `search-protocol.md` for tools and logging and `gap-evaluation.md` for scoring.

## Contents

- M0 Scope and Search Strategy (added)
- M1 Map the Literature Before Finding the Gap
- M2 Find Contradictions Between Studies
- M3 Find What Researchers Keep Recommending but Nobody Solves
- M4 Find the Methodology Gap
- M5 Find the Population or Context Gap
- M6 Find the Theory Gap
- M7 Find the "Everyone Studies X, Nobody Studies Y" Gap
- M8 Find the Time / Data Gap
- M9 Stress-Test a Possible Research Gap (pointer)
- M10 Turn the Literature Into One Defensible PhD-Level Gap
- M11 Practice and Policy Gap (added)
- M12 Assumption Gap / Problematization (added)
- Triangulation worksheet

---

## M0 Scope and Search Strategy (added)

**Purpose.** A gap claim is only as good as the search behind it. M0 makes the search explicit and reproducible so that later claims ("I found no study that...") have a defined scope.

**Inputs.** Topic, field, year range, purpose, any seed papers.

**Procedure.**
1. Restate the topic as a precise scope sentence. Where it helps, structure it with a framework suited to the field: PICOS (population, intervention, comparison, outcome, setting) for empirical and health work; TCCM (theories, contexts, characteristics, methods) for framework-based reviews; or a concept-block layout (core phenomenon × context × method/outcome) for engineering and AI work.
2. Build concept blocks with synonyms, acronyms spelled out, and adjacent terminology from neighboring communities (for example "multi-agent reinforcement learning", "MARL", "decentralized POMDP", "cooperative multi-agent learning"). Terminology mismatch is the most common way a "gap" turns out to be an illusion.
3. Define inclusion and exclusion criteria: document types (journal, conference, preprint, grey literature), languages, year range, study types.
4. Draft the query plan for each search pass (see `search-protocol.md`).
5. Identify existing reviews, surveys, meta-analyses, evidence-and-gap maps, and research agendas on the topic. If a recent one already lists the gap being considered, that changes the novelty claim and must be reported.

**Output template.**
- Scope sentence
- Concept-block table (block, core terms, synonyms, excluded senses)
- Inclusion/exclusion criteria
- Query plan per pass
- Existing reviews found `[S]`, with their year, coverage, and the gaps they already named

**Quality bar.** Someone else could rerun the search from this section.

---

## M1 Map the Literature Before Finding the Gap

**Purpose.** Understand the field's structure before claiming anything is missing. Gaps found without a map tend to be gaps in the searcher's knowledge rather than in the literature.

**Inputs.** [TOPIC], [FIELD], [YEAR RANGE].

**Stance.** Act as a senior academic researcher who has read widely in [FIELD].

**Search moves.** Reviews and surveys first; then broad topic queries within the year range; then one or two queries per emerging cluster to confirm it is a real cluster and not an artifact of one search.

**Procedure.**
1. For each relevant paper, record: research theme, theory or formal framework, methodology, population or setting, variables or constructs, key conclusion. For a Deep analysis, code these into the extraction sheet and run `gap_matrix.py`.
2. Group papers into 5–8 research clusters. A cluster is a set of papers that share a question, not just keywords. Name each cluster with a descriptive phrase.
3. For each cluster determine:
   - **Well understood:** findings replicated across independent groups, methods, or settings `[S]`.
   - **Uncertain:** findings from few studies, conflicting results, weak designs, or narrow contexts `[S]`/`[I]`.
   - **Surprisingly neglected question:** an important question adjacent to the cluster's core that the retrieved papers rarely or never address. Explain why it is important and why its neglect is surprising `[I]`, and state the search that failed to find it.
4. Note influential theories, dominant methods, commonly studied populations, and common variables across the whole map (these feed M4–M7).
5. Derive exactly 3 research gaps that follow from the map. Each must point back to specific cells in the map.

**Output template.**

| Cluster | Core question | Representative papers | Dominant theory / method | Well understood | Uncertain | Neglected question |
|---|---|---|---|---|---|---|

Then: cross-cutting observations (theories, methods, populations, variables), then the 3 gaps, each with: gap statement, supporting map cells, search scope, preliminary strength (Strong / Moderate / Weak, untested).

**Quality bar.** Every cluster has at least two retrieved papers behind it. Every "well understood" claim cites more than one independent source. If the year range yields few papers, say so and consider widening it.

---

## M2 Find Contradictions Between Studies

**Purpose.** Contradictions are among the most defensible gaps because the literature itself demonstrates the uncertainty.

**Inputs.** [TOPIC]; optionally a specific relationship or claim to examine.

**Search moves.** Queries combining the relationship with terms such as "mixed evidence", "inconsistent findings", "conflicting results", "fails to replicate", "boundary conditions", "no significant effect", "does not generalize". Search for meta-analyses and replication studies. In ML, search for re-evaluations, reproducibility studies, and papers reporting that a claimed improvement disappears under different baselines or tuning.

**Procedure.**
1. Identify relationships or claims where retrieved studies report different directions, magnitudes, or significance. Code signs in the extraction sheet (`X->Y:+`, `-`, `0`, `~`) so `gap_matrix.py` can flag conflicts.
2. Check that the contradiction is genuine: are the studies measuring the same construct, at the same level of analysis, with comparable outcomes? If not, label it an **apparent contradiction** and explain the mismatch; that mismatch can itself be a gap (construct or measurement gap).
3. For each genuine contradiction, record:
   1. What Study Group A generally finds `[S]`
   2. What Study Group B finds instead `[S]`
   3. Plausible reasons for the disagreement, checked against the papers' actual designs: sample, geography, measurement or operationalization, methodology and design, timeframe, theoretical assumptions, and also level of analysis, unmeasured moderators, construct definitions, publication or reporting bias, statistical power, and (for ML) datasets, baselines, hyperparameter budgets, compute, random seeds, and evaluation protocols. Mark each reason as evidenced in the papers `[S]` or conjectured `[I]`.
   4. A study that could resolve it: moderator test, multi-site or multi-dataset replication, measurement-invariance test, meta-analysis, adversarial collaboration, controlled ablation, or a design that holds the suspected cause fixed while varying one factor.
4. Rank the resulting opportunities from strongest to weakest using: size and clarity of the contradiction, number and quality of studies on each side, theoretical stakes, practical stakes, and resolvability with available methods.

**Output template.** For each contradiction:

| Element | Content |
|---|---|
| Relationship / claim | |
| Group A finds | papers `[S]` |
| Group B finds | papers `[S]` |
| Genuine or apparent | with justification |
| Likely explanations | each tagged `[S]` or `[I]` |
| Resolving study | design, key manipulation or moderator, data needed |
| Rank and rationale | |

**Quality bar.** At least two papers per side. No contradiction built on a single outlier without saying so.

---

## M3 Find What Researchers Keep Recommending but Nobody Solves

**Purpose.** When many authors independently name the same missing study, the gap is pre-validated by the community. The risk is that someone has since done it.

**Inputs.** [TOPIC]; window of [LAST 5 or 10 YEARS].

**Search moves.** Scholar Gateway queries phrased as questions about limitations and future research (for example "What limitations and future research directions do studies of [topic] report?"), restricted by `start_year`. Consensus queries such as "[topic] limitations future research". Read discussion, limitations, and future-work passages rather than abstracts where possible. Record the verification level: a recommendation drawn only from an abstract is weaker than one read in the full text.

**Procedure.**
1. Extract each future-work recommendation and limitation, paraphrased, with its paper. Code them into normalized tags (for example `longitudinal-design`, `real-world-deployment`, `non-WEIRD-samples`, `adaptive-adversary-eval`).
2. Count recurrence with `gap_matrix.py` or by hand: number of papers, number of distinct first authors or groups, and year span. A recommendation counts as recurring when it appears in at least 3 papers from at least 2 independent groups across at least 2 years. State the threshold used.
3. For each recurring recommendation, run a targeted search for studies that attempted it. Classify the status: unaddressed, partially addressed (attempted but limited), or addressed (drop it, or reframe as an extension).
4. Explain why it matters and what is still missing after the attempts.
5. Write a precise research question for each.

**Output template.**

| Repeated recommendation | Recurrence (papers / groups / years) | Why it matters | What was attempted `[S]` | What is still missing | Research question |
|---|---|---|---|---|---|

**Quality bar.** Distinguish a limitation stated by authors from Claude's reading of a limitation. Do not count the same author group's papers as independent confirmation.

---

## M4 Find the Methodology Gap

**Purpose.** Some questions stay open because the dominant methods cannot answer them. A method-based gap is defensible only when the new method produces a kind of evidence the old ones cannot.

**Inputs.** [TOPIC]; [METHOD YOU WANT TO USE] (optional but needed for the final step).

**Search moves.** Topic queries filtered or scanned by study type; queries naming specific designs (for example "longitudinal", "field experiment", "randomized", "simulation", "formal verification", "user study", "red teaming"). Methodological critiques and reviews of methods in the field.

**Procedure.**
1. Profile the methods in use (surveys, interviews, experiments, longitudinal studies, case studies, secondary datasets, machine learning, simulation, formal methods, mixed methods, and field-specific designs). Use corpus counts where available.
2. Build a question–method fit analysis: for each dominant method, what kinds of questions it answers well and which it cannot answer (causal identification, temporal dynamics, mechanisms, lived experience, generalizability, scale, adversarial robustness, real-world validity, emergent multi-agent behavior).
3. List important questions in the field that current methods leave unanswered, with evidence that the question matters `[S]` and evidence that current designs cannot address it `[S]`/`[I]`.
4. Propose 3 methodology-based gaps using [METHOD]. For each, state exactly what the method adds: identification strategy, temporal resolution, ecological validity, granularity, causal leverage, scalability, or formal guarantees. If [METHOD] does not add something real, say so and suggest the method that would.

**Output template.**
- Method profile table (method, share of corpus, typical questions, blind spots)
- Question–method fit matrix
- 3 gaps, each: unanswered question, why current methods fail, how [METHOD] answers it, what new evidence it yields, main threats to validity

**Quality bar.** "Nobody used method X" is not a gap by itself (see red flags in `gap-evaluation.md`). The added value must be epistemic.

---

## M5 Find the Population or Context Gap

**Purpose.** Findings often rest on a narrow set of populations, regions, sectors, or environments. A context gap is valuable only when there is a reason the finding might change there.

**Inputs.** [TOPIC]; [TARGET POPULATION / COUNTRY / INDUSTRY] (optional).

**Search moves.** Topic queries plus context terms; Consensus `country` filter when the user names a country; searches for cross-cultural, cross-national, or cross-sector comparisons.

**Procedure.**
1. Profile studied contexts with corpus counts: populations, industries, countries and regions, age groups, organization types and sizes, cultures, socioeconomic groups, deployment environments, languages.
2. Identify under-researched contexts. Do not call something a gap simply because fewer studies exist.
3. For each candidate, state a mechanism that makes the context matter: institutional or regulatory differences, cultural values, infrastructure, resource constraints, language, market structure, risk profile, data availability. Tie the mechanism to theory or prior evidence `[S]`, and say whether studying the context would **challenge** (theory predicts a different result), **extend** (tests a boundary condition), or **refine** (adds a moderator) existing findings.
4. Generate 5 defensible context-based gaps and rank them by research significance.

**Output template.**
- Context profile table (dimension, most studied, least studied, counts)
- 5 ranked gaps, each: context, mechanism for difference, challenge / extend / refine, expected contribution, evidence tags, feasibility notes (access, data, ethics)

**Quality bar.** Every gap has a mechanism. A gap that says only "not yet studied in [country]" is Weak by default.

---

## M6 Find the Theory Gap

**Purpose.** Theory gaps produce the most influential contributions: explaining what current theories cannot.

**Inputs.** [TOPIC]; [THEORY A], [THEORY B] (optional).

**Search moves.** Queries naming theories with the topic; theory-review articles; papers reporting anomalies or unexpected findings. For AI and CS, include formal frameworks.

**Procedure.**
1. Inventory the main theories and frameworks used to explain the phenomenon. For each: core constructs, key propositions, assumptions (explicit and implicit), what it explains well `[S]`, what it fails to explain `[S]`/`[I]`, and boundary conditions.
2. Collect anomalies: relationships, behaviors, or outcomes observed in studies that the dominant theories cannot account for.
3. Propose 3 theory gaps using one of these contribution types: theory elaboration (adding constructs or mechanisms), boundary extension, competing-theory test (derive rival predictions and test them), or theory integration (combining [THEORY A] and [THEORY B] where each covers the other's blind spot).
4. For each gap, give a conceptual model: constructs, propositions P1..Pn with directions, boundary conditions. Provide it as a TikZ figure in LaTeX (see `gap-evaluation.md` for a snippet) and, if helpful, a Mermaid version for quick viewing.

**Output template.**
- Theory inventory table (theory, constructs, assumptions, explains well, fails to explain)
- Anomaly list with sources
- 3 gaps, each: theoretical problem, contribution type, integration logic, propositions, conceptual model figure, how it could be tested

**Quality bar.** Integration must be justified by complementary blind spots, not by combining two popular names. If the field uses no explicit theory, that is itself a finding; say so rather than inventing theory use.

---

## M7 Find the "Everyone Studies X, Nobody Studies Y" Gap

**Purpose.** Research communities converge on familiar variables. Neglected variables or links can change the picture, but only if there is a reason to expect them to matter.

**Inputs.** [TOPIC].

**Search moves.** Topic queries; reviews listing antecedents and outcomes; targeted searches for each candidate neglected link, combining both variable names with synonyms (to confirm the link is actually rare).

**Procedure.**
1. Build a variable inventory with roles: predictors, mediators, moderators, outcomes, controls. Use `gap_matrix.py` for frequencies and for the predictor–outcome co-occurrence matrix, which highlights common variables whose pairwise link is rarely tested in the coded corpus.
2. For each promising empty or sparse cell, run a targeted search to confirm rarity beyond the coded corpus.
3. For each confirmed neglected relationship, explain why it should matter based on existing evidence `[S]`, what researchers currently assume about it (often implicitly), and how testing it could change understanding of the topic.
4. Produce 5 testable ideas.

**Output template.** For each idea: relationship (with role of each variable), rationale `[S]`/`[I]`, current assumption, hypothesis, operationalization of each variable, suitable data or design, what a positive and a null result would each mean.

**Quality bar.** An empty matrix cell is a lead, not a finding. Confirm with targeted searches and report them.

---

## M8 Find the Time / Data Gap

**Purpose.** Conclusions age. Findings built on data from before a major technological, policy, or social shift may no longer hold.

**Inputs.** [TOPIC]; [START YEAR] to [CURRENT YEAR]; [MAJOR EVENT / TECHNOLOGY / POLICY CHANGE] (optional; propose candidates if absent).

**Search moves.** Queries spanning the period; queries on the anchor event itself (verify its date and scope from a primary or authoritative source rather than memory); searches for longitudinal studies, panel data, and re-evaluations.

**Procedure.**
1. Trace how knowledge evolved across the period: phases, shifts in dominant questions and methods, landmark findings. Use per-year counts from the corpus.
2. Identify candidate anchor events and verify their dates `[S]`.
3. Flag conclusions that rest on: data collected before the anchor event, cross-sectional designs, short observation windows, deprecated systems or models, retired benchmarks, or datasets with known contamination. Use the `data_end_year` field and `gap_matrix.py --anchor-year`.
4. For each flagged conclusion, assess decay risk: what about the anchor event could plausibly change the result, and what evidence (if any) already suggests it has changed.
5. Suggest 3 gaps addressable with newer data, longitudinal or panel data, real-time or streaming data, or before/after comparisons (including natural-experiment designs around the anchor event where appropriate).

**Output template.**
- Timeline of knowledge (phase, years, dominant questions, key findings)
- Anchor events with verified dates
- At-risk conclusions table (conclusion, sources, data period, design, decay risk, reasoning)
- 3 gaps with design and data sources

**Quality bar.** Do not claim a finding "no longer holds" without evidence; say it "may no longer hold" and explain why.

---

## M9 Stress-Test a Possible Research Gap

**Purpose.** Try to disprove the proposed gap before a reviewer does.

The full protocol, attack checklist, scoring, classification thresholds, and rewrite procedure are in `gap-evaluation.md` (section "M9 stress-test protocol"). Read it in full before running M9.

**Inputs.** [PROPOSED GAP] as the user wrote it; optionally the paper or proposal it belongs to.

**Stance.** A skeptical PhD supervisor who wants the student to succeed and therefore refuses to let a weak claim through. Be direct and specific, not dismissive.

---

## M10 Turn the Literature Into One Defensible PhD-Level Gap

**Purpose.** Converge on the single strongest opportunity and specify it well enough to start a research plan.

**Inputs.** [TOPIC], [FIELD / CONTEXT], results of M1 and selected lenses (run them first if they have not been run), researcher constraints for feasibility.

**Procedure.**
1. Build the synthesis matrix with five columns, each entry tagged and cited:
   - Established (replicated, consistent)
   - Disputed (from M2)
   - Understudied (from M1, M3, M5, M7)
   - Persistent methodological limitations (from M4, M8)
   - Theoretical failures (from M6, M12)
2. Find the intersection: the question that sits where several columns meet (for example, a disputed relationship, in an understudied context, that current methods cannot resolve, and that current theory cannot explain). List the top 3 intersections, score them (`gap-evaluation.md`), and select one.
3. Stress-test the selected gap with M9 and revise it.
4. Specify the gap:
   - Precise research gap statement (LaTeX)
   - Evidence needed to justify it, split into evidence already in hand `[S]` and evidence still to collect
   - Why the gap matters: theoretical and practical significance
   - Novelty claim, with calibrated scope ("to the best of our knowledge, based on...")
   - Contribution type (empirical, methodological, theoretical, artifact, dataset, policy)
   - 3 research questions
   - Hypotheses or propositions, with directions and the reasoning behind them
   - Suitable methodology and why it fits the questions
   - Key variables or constructs with roles and candidate operationalizations
   - Scope boundaries (what the study will not claim)
   - Falsification: what finding or discovered paper would show this is not a gap
   - Feasibility and fit: data access, compute, timeline, ethics, skills; Go / Conditional / No-go
   - Types of papers to search to validate the gap, with ready-to-run search strings per database (reviews, the closest prior studies, recent preprints, papers using the proposed method in adjacent domains, papers under alternative terminology)
   - The two runner-up gaps with one-line reasons they ranked lower

**Output.** Deep deliverables as described in SKILL.md Step 6.

**Quality bar.** Every element traces back to the matrix. The novelty claim survives M9 at Moderate or better; if not, say so and present the best available option honestly.

---

## M11 Practice and Policy Gap (added)

**Purpose.** In applied and governance research, the most important gaps often lie between what regulators, standards bodies, or practitioners require and what research has validated. This lens matters for AI governance work aimed at Europe and North America.

**Inputs.** [TOPIC]; relevant jurisdictions or sectors.

**Search moves.** Primary regulatory and standards texts via `web_search` and `web_fetch` (official legislative portals, standards bodies, government agencies); guidance documents; industry or practitioner reports (mark them as grey literature); academic work evaluating whether proposed methods meet those requirements.

**Procedure.**
1. List concrete requirements or practitioner needs (for example, obligations to assess, document, monitor, or explain), each cited to the primary source `[S]`. Verify dates, article numbers, and status from the source itself.
2. For each requirement, map the research evidence: validated methods, partially validated methods, proposals without evaluation, nothing found.
3. Identify translation gaps: requirements without validated methods, methods validated only in lab settings, metrics that do not correspond to the legal or practical concept, and research that practitioners cannot adopt (cost, data, expertise).
4. Frame each as a research question with a clear user (regulator, auditor, developer, affected community).

**Output template.** Requirement → source → research evidence status → translation gap → research question.

**Quality bar.** Never paraphrase legal requirements from memory; cite the text. Note that Claude is not providing legal advice and that interpretations of requirements may differ.

---

## M12 Assumption Gap / Problematization (added)

**Purpose.** Gap-spotting extends existing work; problematization questions the assumptions beneath it and tends to produce more interesting theory (Alvesson and Sandberg, 2011, Academy of Management Review; Sandberg and Alvesson, 2011, Organization; both verified during skill creation, but re-retrieve them before citing). Use this lens when the field seems saturated or when many studies share an unexamined premise.

**Procedure.**
1. Identify the domain of literature and a small set of key texts.
2. Surface assumptions at several levels: within a line of work (in-house), shared by a school of thought, root metaphors, paradigm-level (ontological, epistemological), and field-level (ideological or institutional).
3. Evaluate each assumption: what evidence supports it, what it hides, who it serves, and what would change if it were false.
4. Develop alternative assumptions and the research questions they generate.
5. Assess whether the alternatives would be seen as interesting (challenging something the audience holds) rather than obvious or absurd.

**Output template.** Assumption → where it appears `[S]` → why it is questionable `[S]`/`[I]` → alternative assumption → research question → likely audience reaction.

**Quality bar.** An assumption must be shown to be actually held in the literature, with citations, not attributed to the field in general terms.

---

## Triangulation worksheet

Use this after running the lenses to merge and compare candidates before scoring.

| Candidate gap | M1 | M2 | M3 | M4 | M5 | M6 | M7 | M8 | M11 | M12 | Lenses supporting | Key sources |
|---|---|---|---|---|---|---|---|---|---|---|---|---|

Mark each cell with ✓ (supports, with a source), ~ (weak or indirect support), or blank. Merge candidates that describe the same underlying question in different words. Candidates supported by three or more independent lenses are usually the strongest; carry them into scoring.
