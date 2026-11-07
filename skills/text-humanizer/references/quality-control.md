# Quality control

Read this file for any whole-document review, and before you deliver any revision. It holds the ten-pass workflow (guide Section F), the review checklist for a revised version, the issue log, the final submission checklist (guide Section K), and the reporting contract.

## Contents

1. Choosing the depth
2. The ten-pass workflow
3. Review checklist for any revised version
4. Issue log, statuses, and author queries
5. Final submission checklist
6. Reporting contract

## 1. Choosing the depth

| Request | Run |
|---|---|
| Proofread a sentence or paragraph | Section 3 items 1, 8, and 9 only. No report. |
| Copyedit or revise a passage | Section 3 in full on the changed text and anything it touches |
| Revise or review a whole document | Section 2 (all ten passes), then Section 3, then Section 5 if it is a submission |
| Full research manuscript (.tex or .docx) | If `universal-manuscript-polish` is installed, it governs the run (backup, inventory, compile, report). Use this file's passes and checklists inside it. |

## 2. The ten-pass workflow

Preserve an unchanged baseline before editing. Keep the manuscript, relevant tables, analysis outputs, references, and any supplied submission requirements together. Keep a short issue log (Section 4). An unresolved scientific question should stay visible rather than disappear into smoother prose.

Run the passes in order, because later wording decisions depend on earlier factual decisions. On a large manuscript, work section by section within each pass, then check the whole document for recurring problems. Do not repeatedly polish paragraphs whose central claims are still unsettled.

### Pass 1. Factual and technical accuracy

- **Inspect:** numbers, units, denominators, group labels, eligibility rules, statistical results, equations, algorithms, and procedural order against the supplied authoritative records.
- **Ask:** Does each statement describe what was actually done or observed? Do counts refer to enrollment, analysis, or a subset? Are time points and comparison groups consistent?
- **Look for:** transposed values, inconsistent units, changed signs, missing negation, mislabeled metrics, results from an obsolete analysis, and descriptions that confuse flagging with removal.
- **Successful output:** a reconciled fact sheet and a list of unresolved discrepancies. Every edited factual statement has an identifiable basis. Do not choose between conflicting values without evidence. Continue other repairs while that issue stays open.

### Pass 2. Argument structure and logical consistency

- **Inspect:** research question, contribution, hypotheses, section purposes, paragraph purposes, and the path from evidence to conclusion.
- **Ask:** Does the method address the question? Does the conclusion answer it? What premise connects each inference? Are alternatives or assumptions omitted?
- **Look for:** benchmark-to-deployment leaps, association presented as causation, unsupported novelty, conclusions that answer a different question, and sections that repeat rather than develop the argument.
- **Successful output:** a brief argument map in which each main claim connects to evidence and qualifications. Remove or label unsupported steps. Move a paragraph only when doing so restores that relation, not because a familiar template suggests another order.

### Pass 3. Evidence quality and citation verification

- **Inspect:** every consequential external claim, citation placement, bibliographic identity, and source passage used as support.
- **Ask:** Does the source exist? Is this the intended work? Does it support this exact claim at this scope? Is a vendor claim presented as independent evidence?
- **Look for:** correct DOI with wrong title, citations attached to a whole paragraph but supporting one sentence, real but irrelevant references, inaccessible evidence, and historical performance presented as current.
- **Successful output:** a claim-to-source map with verified support, appropriately narrowed claims, and explicitly unresolved references. A reference-manager import or a plausible-looking citation is not verification. Keep the original numbering unless the citation system requires an authorized update.

### Pass 4. Sentence clarity and specificity

- **Inspect:** subjects, verbs, pronouns, clause relationships, mechanism descriptions, and abstract noun chains.
- **Ask:** Who does what to which object? What does "this" refer to? Does the sentence explain an operation or merely praise an outcome?
- **Look for:** ambiguous agents, generic openings, nested qualifications far from the claims they limit, and vague phrases such as "enhancing the process."
- **Successful output:** sentences whose important relations are explicit. Keep useful technical language and essential conditions. When a referent or mechanism is unknown, write a precise author query instead of guessing. Check sentence revisions against the Pass 1 fact sheet.

### Pass 5. Redundancy and unnecessary wording

- **Inspect:** repeated arguments, empty reinforcement, overlapping modifiers, duplicate table narration, and recurring paragraph endings.
- **Ask:** What information, orientation, or qualification would be lost if this phrase or sentence were removed? Does the repetition serve a new function here?
- **Look for:** "then subsequently," repeated praise, a limitation restated without context, and conclusions that replay the introduction.
- **Successful output:** each retained sentence makes a distinct contribution or provides necessary reinforcement. Keep repeated technical terms and reporting details required for interpretation. Do not remove denominators or limitations because they add length.

### Pass 6. Vocabulary and terminology consistency

- **Inspect:** defined terms, abbreviations, metric names, group labels, technical synonyms, and evaluative vocabulary.
- **Ask:** Does one term consistently identify one concept? Does "robust" have a stated meaning? Is a synonym genuinely equivalent in this discipline?
- **Look for:** accuracy substituted for recall, participant groups renamed between sections, tortured phrases, overformal substitutions, and unsupported adjectives.
- **Successful output:** a controlled terminology list with definitions and permitted abbreviations. Revise vocabulary for precision and reader fit, not to remove words a blog associates with AI. Check headings, captions, tables, and supplementary text too.

### Pass 7. Paragraph flow and transitions

- **Inspect:** topic progression, paragraph boundaries, ordering of evidence and explanation, and connectors such as "therefore" and "however."
- **Ask:** What job does each paragraph do? Does its opening represent its content? Is a transition stating a real relationship? Does the reader know why the next point follows?
- **Look for:** study lists without synthesis, abrupt shifts, mechanically identical paragraphs, unsupported concluding sentences, and excessive microheadings.
- **Successful output:** a sequence of substantive paragraphs whose relationships are evident. Combine overlapping material and split genuinely distinct functions. Do not enforce equal lengths or require every paragraph to end with a summary.

### Pass 8. Uncertainty and scope

- **Inspect:** causal verbs, universal quantifiers, uncertainty markers, generalization, novelty, reliability, and the distinctions among observed results, interpretation, and proposal.
- **Ask:** What exactly is uncertain? Which population and conditions were evaluated? Is each limitation attached to the claim it constrains? Does a cautious sentence still imply an unsupported mechanism?
- **Look for:** "ensures," "proves," and "all" beyond the evidence, redundant hedges, nonsignificance described as proof of no effect, and prospective benefits stated as findings.
- **Successful output:** confidence proportionate to evidence, with the type and scope of uncertainty explicit. Keep directly supported statements free of unnecessary hedging. Recheck the title, abstract, highlights, and conclusion for stronger versions of repaired claims.

### Pass 9. Formatting and document integrity

- **Inspect:** heading hierarchy, tables, figures, captions, equation numbering, links, fields, citation commands, markup, and the rendered submission file.
- **Ask:** Do cross-references resolve to the intended objects? Did conversion change reading order? Are labels, symbols, and mixed formatting intact? Does every list serve a parallel or sequential function?
- **Look for:** literal Markdown in an incompatible file, broken LaTeX commands, orphaned labels, lost italics or subscripts, missing table notes, unresolved placeholders, and instructions left in captions or comments.
- **Successful output:** a readable document whose technical and navigational structures survive the final export. Compile LaTeX when applicable and inspect the rendered output. A successful build is evidence of syntax, not proof that equations or claims are correct.

### Pass 10. Final proofreading and disclosure compliance

- **Inspect:** the complete final version, its differences from the baseline, the resolved and unresolved issue log, acknowledgments, assistance statement, and supplied institutional or venue requirements.
- **Ask:** Does any polished sentence now change the science? Are names and identifiers correct? Is the description of assistance accurate? Are unresolved facts blocking submission?
- **Look for:** new regressions, unreviewed automatic rewrites, overstated "grammar-only" descriptions, residual draft notes, and privacy assumptions about external tools.
- **Successful output:** a verified final document, an honest account of assistance where required, and a concise record of remaining author decisions. Do not call the manuscript submission-ready while a required sample size, contradictory result, or unsupported central citation remains unresolved.

## 3. Review checklist for any revised version

Run this on every revision before delivering it. Items 1 to 9 are judgments. Item 10 is mechanical.

1. **Meaning.** Every claim in the revision appears in the original or its supplied context. Nothing was invented, strengthened, or silently weakened.
2. **Specificity and clarity.** Each changed sentence states who does what, or what was observed. Vague evaluations were specified from supplied facts, removed, or queried.
3. **Logical coherence.** Connectors match the actual relations. The order of claims still follows from evidence to interpretation.
4. **Redundancy.** Repetition that adds nothing is gone. Repetition that stabilizes a term or condition stays.
5. **Vocabulary and terminology.** Defined terms are unchanged and consistent. No synonym rotation. Evaluative words have criteria or were removed.
6. **Tone and register.** Consistent with the document and audience. No casual insertions, no inflated formality.
7. **Evidence and citations.** Citation markers, keys, numbering, and placement survive. Each citation still sits on the claim it supports.
8. **Technical detail.** Numbers, units, signs, intervals, variables, equations, code, conditions, negation, causal direction, and stated limitations all survive.
9. **Requested format.** The output matches the requested level, length, and format, and applies any supplied house style.
10. **Mechanical fidelity check.** When the original and the revision are available as text, save them to files and run:

    ```
    python <skill-dir>/scripts/fidelity_check.py original.txt revised.txt
    ```

    It fails if any number, math expression, or citation marker differs, and it lists changes in negation, hedge, causal, and universal words for review. A listed word change is acceptable only when it is a reported substantive correction (for example, withdrawing "proves"). Resolve every failure before delivering. The script does not strip LaTeX comments, so run it before inserting inline author queries, or keep numbers and citation commands out of query comments. For `.tex` manuscripts, also run the `verify_edit.py` checker from `universal-manuscript-polish` if it is installed.

If any item fails, fix the revision, then rerun the failed items.

## 4. Issue log, statuses, and author queries

### 4.1 Issue log

For comprehensive reviews, keep one row per issue:

| Location | Pattern | Problem | Evidence needed | Action | Status |
|---|---|---|---|---|---|
| Section 3, para 2 | B05 | Benchmark result stated as deployment success | Deployment evaluation, if any | Narrowed to benchmark scope | Fixed |

### 4.2 Statuses

| Status | Use when | Example |
|---|---|---|
| Fixed | A supported change was applied and checked | Restore the defined metric name in the caption |
| Merged | Another documented repair resolves the same issue | Consolidate two duplicate explanation paragraphs |
| Requires author input | The intended meaning or scientific choice is ambiguous | Identify which model's threshold changed |
| Requires unavailable evidence | The claim needs records or sources not supplied | Verify the correct participant count |
| Acceptable in context | Review shows the feature serves a useful function | Keep repeated technical terminology |

Close issues by verifying outcomes, not by counting edits. A short, accurate passage left unchanged can be a successful result of review.

### 4.3 Author query format

Write each query so the author can answer it without rereading the whole document:

> **Q1** (Section 2, sentence 3): "reduced false alarms by 23%" has no stated comparator. **Needed:** the baseline system and whether 23% is relative or percentage points. **Effect:** the sentence can then name the comparison.

Place queries after the revised text. Inline queries belong only where comments are invisible in the output: `%` comments in LaTeX, comments in Word. When running inside `universal-manuscript-polish`, use its `% [HUMAN REVIEW REQUIRED] HR-nn:` marker instead.

## 5. Final submission checklist

Use this on the actual submission version, including the title, abstract, tables, figures, notes, appendices, and supplements. Mark an item complete only after checking it. Use "not applicable" where appropriate and record unresolved matters separately. An item that needs missing evidence cannot be completed through wording.

### Meaning and clarity

- [ ] The research question or professional decision is stated explicitly.
- [ ] Every consequential pronoun has an unambiguous referent.
- [ ] Each procedure identifies the relevant action, object, and actor when the actor matters.
- [ ] Abstract process descriptions have been checked for an actual operation or mechanism.
- [ ] Observation, interpretation, and proposed explanation are distinguishable.
- [ ] Every substantive change in meaning is supported and visible in the revision record.

### Specificity and evidence

- [ ] Each major claim points to a result, analysis, example, or supporting source.
- [ ] Importance and novelty claims identify the relevant comparison and scope.
- [ ] Claims about mechanisms have support or are explicitly labeled as hypotheses.
- [ ] Evaluative terms such as "effective," "reliable," and "robust" have defined criteria or have been removed.
- [ ] Unsupported generalizations have been narrowed rather than dressed in cautious language.
- [ ] Missing facts remain identified as unresolved. No plausible detail has been substituted for evidence.

### Vocabulary and expression

- [ ] Defined concepts keep consistent names and abbreviations throughout.
- [ ] Synonym substitutions have been checked for technical equivalence.
- [ ] Words in `vocabulary-and-phrases.md` were evaluated in context, not automatically deleted.
- [ ] Claims of consensus identify relevant sources and do not hide material disagreement.
- [ ] Formal language serves meaning rather than replacing a direct action with an abstract noun chain.
- [ ] The document keeps a consistent register appropriate to its audience.

### Sentence structure

- [ ] Long sentences preserve necessary conditions and remain understandable on a careful first reading.
- [ ] Shortening has not removed negation, timing, comparison groups, or uncertainty.
- [ ] Active and passive voice are chosen by focus and responsibility.
- [ ] "Therefore," "because," and similar connectors express a supported inference or causal relation.
- [ ] Duplicate hedges have been removed while substantive uncertainty remains.
- [ ] No errors or arbitrary variations were inserted to imitate an assumed human style.

### Paragraph coherence

- [ ] Each paragraph has an identifiable function in the argument or procedure.
- [ ] Its opening accurately represents the content that follows.
- [ ] Literature-review paragraphs compare findings, methods, or conditions where comparison is needed.
- [ ] Paragraph endings add a useful implication, boundary, transition, or result instead of repeated praise.
- [ ] Transitions connect actual ideas rather than merely announce another paragraph.
- [ ] Paragraph lengths reflect their functions instead of a rigid template.

### Repetition and redundancy

- [ ] Repeated arguments have been consolidated unless they serve a distinct purpose.
- [ ] Repeated technical terms remain where needed to preserve identity.
- [ ] Results prose guides the reader through important findings without reproducing every table cell.
- [ ] Discussion explains implications rather than restating the results section.
- [ ] The conclusion answers the research question and states its scope.
- [ ] Deleting filler has not removed required methods or reporting details.

### Academic rigor

- [ ] Methods supply the operational rules needed to understand or reproduce the analysis.
- [ ] Results and conclusions refer to the same groups, measures, and analysis versions.
- [ ] Association has not become causation during revision.
- [ ] A result not statistically established is not described as proof of no effect.
- [ ] Generalization stays within evaluated conditions or is explicitly identified as untested.
- [ ] Each limitation names a real constraint and the inference it affects.
- [ ] Proposed future work is distinguished from completed research.
- [ ] Abstract, title, and conclusion make no stronger claims than the main evidence supports.

### Citations and factual verification

- [ ] Every cited work can be identified from verified bibliographic fields.
- [ ] DOI, title, authors, venue, and year refer to the same intended work.
- [ ] The cited source supports the particular claim, not merely the general topic.
- [ ] Citation placement makes its scope clear.
- [ ] Quotations and paraphrases keep appropriate attribution.
- [ ] Vendor claims, independent findings, and editorial recommendations are labeled accurately.
- [ ] Historical benchmarks and product details keep their dates and conditions.
- [ ] No unverified reference generated by a tool has been accepted as genuine.

### Technical and document integrity

- [ ] Numerical values, units, denominators, precision, intervals, and signs match authoritative outputs.
- [ ] Inconsistent counts have been resolved from records rather than guessed.
- [ ] Equations, variable definitions, assumptions, and quantifiers keep their original meaning.
- [ ] Figure and table labels, captions, notes, and cross-references identify the correct objects.
- [ ] Code and pseudocode still express the described algorithm and parameters.
- [ ] Applicable compilation or document-generation checks have completed successfully.
- [ ] The final rendered file has been inspected for lost symbols, broken fields, and conversion residue.
- [ ] Placeholders, drafting instructions, unresolved comments, and unintended markup are absent from submission content.
- [ ] Legitimate linguistic characters and required provenance have not been indiscriminately removed.

### Authorship transparency and policy compliance

- [ ] Assistance is described by the activities actually performed, not only a tool's marketing label.
- [ ] Required disclosures follow the applicable institutional or venue instructions.
- [ ] Substantive generated or rewritten passages have received factual and technical review.
- [ ] Available drafts, analysis records, source notes, and revision decisions are retained appropriately.
- [ ] Detector results, if reviewed, are kept separate from judgments about factual quality and policy compliance.
- [ ] Similarity matches have been assessed for attribution rather than treated as an automatic verdict.
- [ ] Tool processing and manuscript-handling claims have not been assumed from a score display or interface phrase.
- [ ] No unresolved scientific or citation problem has been hidden by polished wording.

## 6. Reporting contract

Scale the report to the request. Omit any section that would be empty.

| Request | Deliver |
|---|---|
| Proofreading | The corrected text only. Add one line if you noticed a factual or consistency problem you did not fix. |
| Copyediting, substantive or technical revision | 1. The revised text. 2. **Substantive changes:** only edits that narrowed, withdrew, or restored a claim or term, each with its pattern ID and reason. 3. **Author queries** in the Section 4.3 format. |
| Comprehensive review | 1. Revised text or edited files. 2. Recurring issues by pattern ID with locations. 3. Substantive changes. 4. Author queries and unresolved items. 5. Verification still required (citations not checked, compilation not run). 6. Readiness: ready, ready with author queries, or not ready. Never "ready" while a required fact, contradiction, or unsupported central citation is open. |
| Critique only | Findings by priority (P1 first), each with location, pattern ID, and what it costs the reader. One example revision per pattern if helpful. No full rewrite unless asked. |
| Detection or authorship question | What the result measures and does not, with evidence labels and dates. Any writing problems in the flagged passages by pattern ID. No authorship verdict. |

Rules for every report:

- Name problems by pattern ID and effect on the reader. Never describe text as "AI-sounding" or "robotic."
- List trivial edits (grammar, punctuation, word order) only if the user asks for a change log.
- Never claim a check you did not perform: compilation, citation verification, data reconciliation, or the fidelity script.
- Never promise a detector outcome or certify authorship.
