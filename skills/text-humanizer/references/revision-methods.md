# Revision methods

Read this file to choose how much to change and how to change it. It holds the intervention levels, the ten principles (guide Section A), the ten sentence-level methods (Section D), the paragraph and document methods (Section E), drafting rules, house-style reconciliation, and the writing-practice misconceptions from Section J.

All examples are constructed [I]. Each example supplies its own factual boundary and adds no measurement. Semicolons in the guide's examples were changed to full stops to fit the user's house style.

## 1. Intervention levels

Decide the level before editing. Do not rewrite text that needs only a narrow correction. If the request is ambiguous and the difference matters (for example, "fix this paragraph" on a passage with both typos and an unsupported causal claim), do the narrower level and list the larger issues as offers or queries.

| Level | What may change | What must not change | Output |
|---|---|---|---|
| Proofreading | Spelling, grammar, agreement, punctuation, typos, obvious formatting slips | Wording that is already correct, sentence structure, claims, tone | The corrected text. Add one line only if you notice a factual or consistency problem. |
| Copyediting | The above, plus clarity, concision, redundancy, terminology consistency, house style, local flow | Claims, scope, certainty, argument structure, technical terms | Revised text, then any substantive changes and author queries |
| Substantive revision | The above, plus paragraph structure, ordering, transitions, openings and endings, calibration of claims to the evidence present | Findings, numbers, citations, defined terms, the author's argument | Revised text, a short list of substantive decisions, author queries |
| Technical revision | Precision of methods, definitions, metrics, equations in prose, reproducibility wording | Values, equations, code semantics, experimental conditions | Revised text with every technical change listed, and queries for anything needing records |
| Drafting from source material | New prose built only from supplied notes, data, sources, and instructions | Anything not in the supplied material | The draft, with gaps marked as queries, never filled |
| Critical review only | Nothing in the text | Everything | Diagnosis: issue log by pattern ID, with locations and needed evidence |

## 2. Principles of natural academic writing (guide Section A)

### A1. Give the reader a specific intellectual task

A useful paragraph explains a problem, establishes a distinction, reports an observation, develops an inference, or identifies a limitation. "This topic is increasingly important" usually delays that work. State what is unresolved, for whom, and under which conditions. An introduction can still give broad context, but each contextual claim should help the reader understand the particular question.

Specificity is not a license to fabricate detail. If a draft says a method is "efficient" without an outcome, do not invent a runtime reduction. Ask what was measured. Until the answer exists, describe the method's known operation or remove the unsupported performance claim.

### A2. Match claims to evidence

Separate three layers: what was observed, what the observation supports, and what remains a proposal. A benchmark result supports a statement about that evaluation. It does not automatically support deployment success. A source's existence establishes neither its relevance nor its support for a particular sentence.

For consequential statements, build a claim-to-evidence map: the table, analysis, passage, or reference, and the conditions under which it applies. If no support can be found, classify the statement as an unanswered question, a hypothesis, or an unsupported assertion requiring repair.

### A3. Explain an actual mechanism when one is known

"The system improves the workflow" names a desired outcome without an operation. A mechanism identifies the actor or component, the action, and the link to the outcome. "The script copies the entered value into both forms" explains an operation without claiming an unmeasured productivity gain.

Do not supply a plausible causal story as though it were demonstrated. If a mechanism is proposed, say so and identify the evidence needed to test it. If the study measures association only, preserve that boundary.

### A4. Make transitions carry reasoning

"Therefore" signals an inference, "however" a contrast, "additionally" a relevant further point. Check the actual relation before adding the marker. A sentence may need no transition because its subject and content already connect it to the previous one.

Useful transitions can name the link: "Because the evaluation used one site, the next question is transfer to other sites." This conveys more than "Furthermore." Keep explicit signposting when it helps readers navigate a complex argument or long report.

### A5. Let structure follow information

Sentence and paragraph lengths should reflect their jobs. A short sentence can state a result. A longer sentence can preserve the conditions needed to interpret it. Variation should emerge from these differences, not from a quota.

The source reports different lexical-diversity results for generation and revision tasks, and variation across domains and models. These findings do not justify manipulating vocabulary richness, syntactic complexity, or sentence length to resemble an imagined human distribution. [19–21]

### A6. Preserve technical precision

A defined term is a stable reference to a concept. Repeating it may be clearer than cycling through synonyms. "Recall," "precision," and "accuracy" are different quantities, and replacing one with another for variety changes the claim. The same holds for named algorithms, experimental groups, attack models, and operational definitions.

Use ordinary language around necessary technical terms. Make the concept accessible without diluting it. Explain a term for the intended audience when needed, then use it consistently.

### A7. Calibrate confidence

Qualify a claim where the evidence is limited, and state a supported observation directly. "The result may perhaps potentially suggest" stacks uncertainty markers without explaining the source of uncertainty. "The association was observed in this sample. Its persistence at other sites is unknown" identifies the boundary.

Keep statistical uncertainty, measurement uncertainty, causal uncertainty, and uncertainty about generalization distinct. One vague hedge cannot replace all four. Conversely, do not weaken a directly established procedure or result merely to sound cautious.

### A8. Make authorial choices visible

Author-driven writing shows why a question was selected, why a comparison matters, which assumptions were adopted, and how evidence was interpreted. Voice can be restrained and formal. It need not be conversational, eccentric, or full of personal opinion.

Use first person when it clarifies responsibility and fits the document's conventions. Use passive voice when the procedure or material deserves focus. Keep a consistent level of technical detail and an honest account of decisions. Without earlier drafts, no editor can establish that a particular voice has been lost. The assessable issue is the current document's coherence.

### A9. Distinguish repetition from redundancy

Necessary repetition stabilizes terminology, reminds the reader of a condition, or connects a result to a later interpretation. Redundancy restates a point without adding evidence, explanation, qualification, or orientation. A conclusion may restate the answer to the research question while adding its scope and implications. It need not introduce a new result.

Before deleting a repeated phrase, ask what would become ambiguous without it. Before keeping a repeated paragraph, identify its new contribution, more specifically than "emphasis."

### A10. Treat naturalness as fit, not performance

Natural academic prose fits its subject, evidence, audience, and purpose. It can be grammatically polished, technically dense where necessary, and conventional in its reporting. Errors, rare words, casual expressions, and artificially complicated syntax do not create authenticity.

Writing assistance varies in scope. The source distinguishes spelling correction, substantial rewriting, translation, brainstorming, and generation, and its cited proofreading study found broader lexical and syntactic changes in LLM proofreading under the tested conditions [34]. Authors should review the actual changes and disclose assistance as required, rather than assume a tool's "proofreading" label describes every intervention.

## 3. Sentence-level methods (guide Section D)

These methods expose the reasoning behind a revision. They do not require every sentence to be short or active.

### D1. Replace an abstract evaluation with a stated operation

- **Original:** "The advanced module enhances administrative efficiency by copying the entered address into the second form."
- **Weakness:** The copying operation is specified, but "advanced" and "efficiency" imply evaluations not supported here.
- **Steps:** (1) Identify the verifiable action. (2) Separate it from praise and outcome claims. (3) Keep the action. Request time or effort evidence before restoring an efficiency claim.
- **Revision:** "The module copies the entered address into the second form."
- **Why it works:** The reader understands the operation. This is an explicit narrowing of an unsupported claim, not evidence that the module has no benefit.

### D2. State a supported dependency without inventing causation

- **Original:** "The procedure ensures matching through an effective process, because it uses the shared record identifier as the join key."
- **Weakness:** "Ensures" overstates correctness. "Effective process" adds no mechanism.
- **Steps:** (1) Keep the specified join key. (2) Describe the operation directly. (3) Keep correctness separate from implementation, since duplicate or missing keys would need their own checks.
- **Revision:** "The procedure joins records on the shared record identifier."
- **Why it works:** It exposes the mechanism without claiming perfect matching. The possible key issues explain why verification matters. They are not alleged defects in this scenario.

### D3. Remove redundant wording while keeping the condition

- **Original:** "After the final collection stage had been completed, the records were then subsequently reviewed."
- **Weakness:** "Then subsequently" duplicates the temporal relation that "after" already establishes.
- **Steps:** (1) Preserve that review followed final collection. (2) Remove duplicate sequence markers. (3) Keep passive voice if the reviewer is not relevant to this sentence.
- **Revision:** "The records were reviewed after final collection."
- **Why it works:** The sequence stays explicit. If reviewer qualifications matter to reproducibility, supply them from the method records elsewhere.

### D4. Unpack an overloaded sentence without losing a distinction

- **Original:** "The team, which used the prespecified coding scheme after training and retained unresolved disagreements for adjudication, coded the interviews and did not treat adjudicated decisions as independent initial ratings."
- **Weakness:** Several method details interrupt the main action.
- **Steps:** (1) Identify coding, disagreement handling, and the distinction between initial and adjudicated ratings. (2) Group the first two as the procedure. (3) State the analytical distinction separately.
- **Revision:** "After training, the team coded the interviews with the prespecified scheme and retained unresolved disagreements for adjudication. Adjudicated decisions were not treated as independent initial ratings."
- **Why it works:** Every procedural element and the negation survive. Two sentences are used because the analytical distinction deserves attention, not because long sentences are inherently weak.

### D5. Preserve a technical term and define its denominator

- **Original:** "Recall, the proportion of actual positive cases identified as positive, was reported as detection success."
- **Weakness:** The final label obscures the precise quantity just defined.
- **Steps:** (1) Keep "recall." (2) Keep its denominator explicit for the intended audience. (3) Remove the ambiguous relabeling.
- **Revision:** "We reported recall, the proportion of actual positive cases identified as positive."
- **Why it works:** The quantity is retained, not replaced by a vague synonym. Adding "we" attributes the reporting action only. It does not alter the metric.

### D6. Choose voice according to responsibility and focus

- **Original:** "The analysis was conducted by the statistician."
- **Weakness:** None is inherent. The right revision depends on the paragraph's focus.
- **Steps:** (1) Decide whether the paragraph concerns personnel or analysis. (2) Put that subject first. (3) Preserve the named actor if responsibility matters.
- **Revision emphasizing responsibility:** "The statistician conducted the analysis."
- **Version emphasizing the procedure:** "The analysis was conducted by the statistician."
- **Why both work:** Active voice makes responsibility prominent. Passive voice keeps "analysis" as the topic. Deleting the actor would be harmful if specialist involvement matters to the method.

### D7. Keep uncertainty, remove duplication

- **Original:** "The result may perhaps potentially suggest a change, although the interval includes no change."
- **Weakness:** Multiple hedges obscure the supplied reason for caution.
- **Steps:** (1) Preserve the interval's inclusion of no change. (2) Keep one uncertainty marker. (3) Do not turn inconclusiveness into evidence that no change exists.
- **Revision:** "The result may suggest a change, but the interval includes no change."
- **Why it works:** The sentence names a concrete uncertainty. The actual estimate, interval, interval type, and level still belong in the full results report. None can be invented during a language edit.

### D8. Make scope explicit

- **Original:** "The procedure is reliable across institutions. The evaluation was conducted at one institution."
- **Weakness:** The first sentence extends beyond the supplied evaluation.
- **Steps:** (1) Identify the observed setting. (2) Remove the unsupported cross-institution conclusion. (3) State the unresolved extension.
- **Revision:** "The evaluation was conducted at one institution. Reliability across institutions remains unestablished by this evaluation."
- **Why it works:** It separates scope from aspiration. This deliberately changes an overclaim and does not imply the procedure failed at the evaluated institution.

### D9. Separate observation, interpretation, and speculation

- **Original:** "Participation increased after the reminder, showing that improved motivation caused the increase." **Supplied context:** motivation was not measured, and the design did not isolate the reminder's effect.
- **Weakness:** Temporal order is presented as a demonstrated causal mechanism.
- **Steps:** (1) State the observed sequence. (2) Mark the mechanism as a possible explanation. (3) Keep the design limitation.
- **Revision:** "Participation increased after the reminder. Improved motivation is one possible explanation, but motivation was not measured, and the design does not isolate the reminder's effect."
- **Why it works:** The longer revision is more accurate. It preserves the observation and withdraws unsupported causation.

### D10. Resolve ambiguity before polishing

- **Original:** "After comparing the baseline model with the revised model, we changed its threshold."
- **Weakness:** "Its" could refer to either model.
- **Steps:** (1) Identify both readings. (2) Check the analysis record or ask the author which threshold changed. (3) Replace the pronoun with the verified model name.
- **Conditional revision:** if the record identifies the revised model: "After comparing the baseline model with the revised model, we changed the revised model's threshold."
- **Why it works:** It makes the action reproducible. Without verification, a fluent revision could silently describe the wrong experiment.

## 4. Paragraph and document methods (guide Section E)

### E1. Introductions: connect the known problem to the actual question

- **Before:** "Record management is a vital component of modern organizations. Its importance cannot be overstated. Our report examines duplicate entries in an intake register and the rules used to identify them."
- **After:** "This report examines duplicate entries in an intake register and the rules used to identify them."
- The opening now names the document's task without inventing the prevalence or cost of duplication. A full introduction can then explain why duplicates matter with verified operational evidence, what existing rules leave unresolved, and what the report contributes. If those facts are absent, the paragraph stays modest rather than filling the gap with generalized importance.
- At document scale, check that the research question in the introduction is answered by the results and conclusion. Do not promise a deployment evaluation when the methods describe only a benchmark.

### E2. Literature reviews: synthesize the basis of disagreement

- **Before:** "Study A used generated abstracts and reported greater lexical variability in model outputs. Study B examined revised scientific passages and reported lower lexical diversity after revision. Both studies provide important insights."
- **After:** "The two studies address different writing operations. The abstract-generation comparison reported greater lexical variability in model outputs, whereas the passage-revision study reported lower lexical diversity after revision. These results should not be treated as a single rule about all AI-associated writing. [19, 21]"
- The revision synthesizes by task and preserves each direction of effect. The task difference makes a universal conclusion unjustified, but it does not by itself prove which design difference caused the contrast. A longer review should also compare measures, models, samples, and limitations where verified.
- **Method for a list-like review:** group sources by the question, method, condition, or finding they share. State what the group shows together and where sources disagree. Attribute each claim to the source that supports it. Where the supplied summaries lack the details needed to compare (dataset, metric, result), say what comparison is missing and query the author. Never invent a study's result to complete a synthesis.

### E3. Methods: replace evaluation words with reproducible operations

- **Before:** "We carefully processed the records with a rigorous procedure. Duplicate identifiers were marked for review, and the original records were retained. Review decisions were recorded in a separate log."
- **After:** "We marked duplicate identifiers for review and retained the original records. Review decisions were recorded in a separate log."
- Three operational details survive: flagging, retention, and logging. Self-assessment is removed without implying the method is deficient. A complete method may still need the definition of a duplicate, who reviewed cases, and the decision rules. Those are author queries if absent.
- Check that code, pseudocode, and prose describe the same treatment of flagged records. "Marked for review" must not become "removed" during revision.

### E4. Results: guide readers through the evidence without duplicating it

- **Before:** "Table 2 reports runtime and memory use. Runtime and memory use are shown in Table 2. The table therefore provides important results."
- **After:** "Table 2 reports runtime and memory use."
- The local revision removes duplication without inventing a trend. To develop a full results paragraph, consult the actual table and select the result that answers the research question, with its effect size and uncertainty. Do not recite every cell unless the genre requires it.
- Some journals combine results and discussion, others separate them. In a separate results section, identify contrasts and patterns supported by the analysis without importing speculative mechanisms.

### E5. Discussion: state what the design permits

- **Before:** "The association between training attendance and completion proves that training improves completion. Attendance was self-selected, and the design did not isolate the effect of training."
- **After:** "Training attendance was associated with completion. Because attendance was self-selected and the design did not isolate training's effect, this association does not establish that training caused higher completion."
- The conclusion now matches the supplied design limitations. It does not claim training has no effect. If the discussion considers a mechanism, frame it as a proposed explanation and say what evidence would distinguish it from alternatives.
- After this repair, read the abstract and conclusion. A qualified discussion cannot rescue an abstract that still claims causal proof.

### E6. Limitations: identify the affected inference

- **Before:** "The study has limitations, and further research is necessary. Data were collected at one site, and no follow-up was conducted."
- **After:** "The single-site data leave transferability to other sites unresolved. The absence of follow-up also limits conclusions about persistence over time."
- Each supplied constraint now has an interpretive consequence, and no limitation is invented. A recommendation for multisite or longitudinal data can follow as a proposed response, without promising that those designs would confirm the finding.
- Distinguish a limitation of available evidence from a defect in execution. A cross-sectional design may answer its descriptive question well while being unsuitable for claims about change over time.

### E7. Conclusions: answer the question at the supported scale

- **Before:** "Record management is important, as noted in the introduction. This report has discussed record management. The proposed rules identify records for manual review, but their effect on review time has not been evaluated."
- **After:** "The proposed rules identify records for manual review. Their effect on review time remains unevaluated."
- The conclusion states the contribution and its boundary instead of restating the opening theme. It can name the next necessary evaluation if that follows from the report's purpose. Never add a new empirical result in a conclusion or silently convert a proposed rule into a validated system.

### E8. Whole-document consistency: a concept and claim map

- **Before:** the methods define "completion" as submitting the final task, the results call the same outcome "retention," and the conclusion claims the program reduced dropout.
- **Procedure:** locate the outcome variable and its operational definition. If the analysis measures only final-task submission, use "completion" consistently and remove or qualify the dropout claim. If retention is a distinct measured outcome, define and report it separately rather than merging the terms.
- **After (under the completion-only definition):** "The analysis concerns final-task completion. It does not establish an effect on dropout."
- This is a substantive alignment, not a global find-and-replace. Map each consequential term to its definition, data column, analysis, table, and conclusion. Map each claim to its evidence. Any broken link requires investigation before polishing.

### E9. Check reasoning independently of surface flow

Write a one-sentence purpose beside each paragraph and read the purposes in order: does a question lead to a method, then evidence, then a proportionate interpretation? Next, read each paragraph without its opening sentence. Can its evidence and reasoning still be recognized, or does the opening promise an argument that never appears?

These are diagnostics, not rigid templates. A methods paragraph may explain a sequence rather than argue a position. A literature-review paragraph may compare several studies. Preserve those differences. Headings help readers find functions. Transitions explain relations among functions.

## 5. Drafting from source material

The guide addresses revision. When asked to draft new prose, apply the same principles to what you write [E]:

1. Build only from supplied notes, data, sources, and instructions. Do not import facts, results, or citations from memory into a document the user will submit as their own work.
2. Open with the specific task or question (A1). State each claim at the scale its supplied evidence supports (A2).
3. Where the material lacks a fact the draft needs (a sample size, a result, a citation), mark it as a visible query in the draft, not a plausible invention. In LaTeX, use a `%` comment. In other formats, list the queries after the draft.
4. Cite only works the user supplied or that you have verified exist and support the claim. Never generate a reference to fill a gap.
5. Apply the applicable house style while drafting, then run the review checklist in `quality-control.md` Section 3 on the draft.

## 6. House style and user rules

- When the user, venue, or project supplies style rules, apply them to every sentence you write or change. Typical examples: no em dashes, no semicolons, American spelling, a list of words to avoid, a preference for active voice, a preference for varied sentence length.
- These are legitimate style requirements. Never describe them as detection tactics, and never extend them into the prohibited behaviors in B36 (inserted errors, arbitrary synonym rotation, quota-driven variation).
- Reconciling common rules with the principles here:
  - **"Prefer active voice."** Apply it where the actor matters or the passive hides responsibility. Keep passive voice where the procedure or material is the topic and the actor is irrelevant (D6). That still satisfies "where possible."
  - **"Vary sentence length."** Let variation follow information (A5). Fix runs of sentences that share one structure because the structure obscures relations, not to hit a ratio.
  - **"Avoid word X."** Follow the reconciliation rule in `vocabulary-and-phrases.md` Section 7: rephrase so the meaning survives, and never delete a qualification or rename a defined term to satisfy a list.
  - **"No semicolons or em dashes."** Replace each by the relation between clauses (full stop, colon, comma, parentheses, or restructuring). Check that no claim merges or splits in scope.
- If a style rule and meaning preservation truly conflict, preserve meaning and tell the user which rule you could not satisfy and why.

## 7. Misconceptions about writing practice

This table holds the 10 writing-practice rows of guide Section J (rows 15 to 22, 26, and 35). The other 25 rows are in `detection-principles.md`, Section 11.

| # | Misconception | Correction | Practical implication |
|---|---|---|---|
| 15 | Short sentences are inherently natural or human | Useful length depends on information and conditions. Linguistic studies do not establish that rule. [19–21] | Split when relationships are obscured, not to meet a quota |
| 16 | Long sentences establish expertise | Length can preserve complexity or conceal confusion | Check whether the reader can follow dependencies and qualifications |
| 17 | Every paragraph needs a transition word | Relations may already be clear from content | Add a connector only when it clarifies the actual relation |
| 18 | Natural writing must be informal | Register should fit the audience and genre | Keep professional tone and discipline-specific language |
| 19 | Lexical diversity should always be maximized | Findings vary by task, and repeated terminology can be necessary [19, 21] | Keep stable terms instead of rotating synonyms |
| 20 | Active voice is always better | Voice changes focus and the visibility of responsibility | Choose the voice that makes the relevant actor or procedure clear |
| 21 | Hedging every claim makes it rigorous | Excessive hedging conceals what is known and what is uncertain | State observations directly and qualify only the appropriate inference |
| 22 | "Robust" is an inherently suspicious word | It can have a precise technical meaning | Define the perturbations, assumptions, or criterion and report the evidence |
| 26 | Proofreading always means only grammar correction | The scope of edits varies. The cited study reports broader LLM changes under its conditions. [34] | Inspect the actual diff and describe the assistance accurately |
| 35 | A smoother revision necessarily preserves meaning | Fluency can conceal changes to scope, certainty, and causation | Compare the final claims against the baseline and research records |
