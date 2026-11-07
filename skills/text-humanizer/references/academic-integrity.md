# Academic integrity

Read this file whenever an edit touches results, numbers, equations, code, citations, attribution, assistance disclosure, a flagged document, or a request framed around detection. It holds guide Section G, Source A Sections 6.6, 10, 11, and 14.6, the relevant checklist items, and this skill's boundaries.

## Contents

1. Scientific content is a constraint on editing
2. Wording edits versus scientific decisions, and automated rewriting
3. Citations, attribution, and factual consistency
4. Legitimate characters and provenance
5. Mixed authorship and assistance workflows
6. Four questions research assessment must keep separate
7. Reviewing a flagged document
8. Evaluating a detector before relying on it
9. Improving writing without confusing quality with detection
10. Processing arrangements and manuscript handling
11. Disclosure of assistance
12. Boundaries of this skill and requests framed around detection

## 1. Scientific content is a constraint on editing

A stylistic edit is unacceptable if it changes a result, replaces a technical definition, introduces unsupported evidence, removes a necessary qualification, or compromises attribution. A fluent revision can be more dangerous than an awkward original, because its change in meaning is easy to miss.

**Record the invariants before substantial revision:** numerical results, units, variable definitions, assumptions, intervention and comparator, inclusion rules, causal status, and the conclusions the evidence supports. Compare the final version against these invariants independently of the wording changes.

| Domain | What to preserve | Verification action | Common semantic trap |
|---|---|---|---|
| Numbers, units, statistics | Values, signs, precision, units, denominators, intervals, test names, time points | Compare prose with analysis outputs and tables. Investigate discrepancies. | Turning percentage points into percent, or treating a nonsignificant result as proof of no effect |
| Operational definitions | Which observations count as the outcome, exposure, group, or event | Trace the term to its data rule and method description | Replacing completion with retention because the words sound related |
| Scientific terminology | Established terms and distinctions among metrics or mechanisms | Check a term map across prose, headings, tables, captions | Replacing recall with accuracy for variety |
| Mathematics and LaTeX | Variables, indices, operators, quantifiers, conditions, macros, labels, citation commands | Compare source and rendered equations. Compile and inspect cross-references. | Losing a minus sign, changing a subscript, or dropping a condition while simplifying prose |
| Figures, tables, captions | Values, labels, legends, panel references, notes, uncertainty displays | Compare each claim with the correct visual object and analysis version | A caption keeps the old sample while the table uses the updated one |
| Citations and bibliography | Work identity, source support, quotation boundaries, citation keys, DOI-to-title correspondence | Verify bibliographic fields and supporting passages separately | A real DOI on the wrong article, or a real article on the wrong claim |
| Negation and causal direction | Whether an effect occurred, was not detected, or was not evaluated. The direction of relationships. | Compare claim verbs and logical structure before and after | Changing "did not establish" to "established no," or association to causation |
| Novelty and generalizability | The bounded contribution, comparison set, evaluated setting, evidence status | Check abstracts and conclusions against methods and prior-work support | Changing "in this benchmark" to "in practice" |
| Limitations and uncertainty | The actual design, measurement, and inference boundaries | Confirm every deleted hedge or limitation was redundant, not substantive | Removing "under these assumptions" to improve flow |
| Code, pseudocode, algorithms | Semantics, branch conditions, interfaces, parameter values, inputs, outputs, execution order | Language-aware review and meaningful existing checks | Treating all comments as inert, or editing prose so it no longer describes the algorithm |
| Document structure | Hyperlinks, fields, table structure, equation objects, mixed formatting | Inspect the final rendered file and its structural elements | Assuming text extraction proves layout and field behavior survived |

## 2. Wording edits versus scientific decisions, and automated rewriting

### 2.1 Which changes are scientific decisions (G2)

- Changing "an evaluation was performed" to "we evaluated" is usually a wording edit when the actor is established.
- Changing "associated with" to "caused" is a scientific claim change.
- Narrowing an unsupported universal statement may be warranted, but the author must be able to see that its scope changed.
- Use tracked changes or an equivalent comparison for consequential edits. For a proposed substantive repair, record the supporting evidence. If two interpretations remain possible, keep the uncertainty in the issue log rather than choosing whichever reads better.

### 2.2 Automated rewriting is an unverified transformation (G3, Source A 14.6)

Design strategies such as masking mathematical syntax, document-aware processing, and citation handling do not by themselves establish preservation. A deterministic rule can consistently replace a cautious verb with an overconfident one [39, 40, 50]. For any rewriting tool, including your own edits, compare input and output for meaning as well as formatting. A bibliography generated from a topic taxonomy still needs verification of the actual works and claim support. Preserved numbers do not guarantee preserved conclusions. A visually intact Word document can still have altered links, fields, or table structures.

Verification needs for any rewrite:

- **Meaning:** preserve negation, uncertainty, units, scope, and causal direction.
- **References:** verify the actual work and the statement it supports. An author pool or journal taxonomy is not evidence that a generated reference exists.
- **LaTeX:** compile the result and inspect labels, citations, equations, macros, and the rendered pages. A successful build is evidence of syntax, not proof that equations or claims are correct.
- **DOCX:** compare document structure and rendering, including hyperlinks, fields, tables, and mixed formatting.
- **Code:** use language-aware checks and the project's existing tests. Comment-like text can have operational roles, so "comments only" is not a safe assumption.

If the user's environment provides a mechanical preservation checker (for example `verify_edit.py` in the `universal-manuscript-polish` skill for `.tex` files), run it on edited LaTeX.

## 3. Citations, attribution, and factual consistency

Check three things separately for every consequential citation (Source A 6.6, B27, B28, Pass 3):

1. **Existence:** the work exists.
2. **Identity:** authors, title, year, venue, and DOI refer to the same intended work. A real DOI attached to the wrong title is a bibliographic error.
3. **Support:** the cited source contains evidence for this claim at this scope, not merely the general topic. A real paper cited for a result it does not contain is a support error.

Further rules:

- **Never invent, complete, or "fix" a reference from memory.** If an entry looks wrong, query the author with what is mismatched. Do not supply a DOI.
- **Placement shows scope.** A citation attached to a whole paragraph that supports only one sentence misrepresents its scope. Move it or query.
- **Attribution survives paraphrase.** A paraphrase still needs citation when a source's idea or finding is used, even when few words match. Similarity percentages do not settle attribution.
- **Quotation boundaries stay exact.** Do not edit quoted text, and keep quotation marks and page references intact.
- **Label the evidence type.** Vendor claims, independent findings, and editorial recommendations must be labeled accurately. Historical benchmarks and product details keep their dates and conditions.
- **Tool-generated references are unverified** until checked against an authoritative record.
- **Numbers agree across locations.** Compare numerical claims with tables, captions, methods, and datasets. When two values conflict, record both locations and query. Never pick, average, or recalculate (B26).
- **Keep citation numbering and keys.** Retain the original numbering unless the document's citation system requires an authorized update.

## 4. Legitimate characters and provenance (G4)

- Unicode format controls (joiners, non-joiners) can serve legitimate linguistic and shaping functions. They are not inherently AI markers [48]. Do not strip them indiscriminately.
- C2PA credentials, statistical text watermarks, file metadata, and final-text classification are different mechanisms [17, 47–49]. Removing one says nothing about the others.
- Retain relevant drafts, notes, analysis records, and assistance descriptions. If a file must be converted, verify that conversion did not damage language, equations, or required provenance.
- These checks protect document integrity. They are not procedures for concealing authorship, and this skill provides none.

## 5. Mixed authorship and assistance workflows (Source A 10.1)

A single human-or-AI label hides several workflows. The table describes epistemic limits, not expected scores.

| Workflow | What the final text alone leaves unresolved |
|---|---|
| Human research and human drafting | Whether a false positive occurred |
| Human draft with spelling correction | Which edits were made and whether they were permitted |
| Human draft with substantial AI rewriting | Which ideas and wording came from which stage |
| AI draft extensively revised by a human | How much generated wording remains and how it was verified |
| AI brainstorming followed by independent drafting | Whether an earlier assistance step occurred at all |
| Translation into English | How the source text and translation process relate to the final wording |
| Several authors and professional editing | Whether style changes reflect contributions or editing |

- There is no defensible universal promise that grammar-only editing always yields zero, or that substantial rewriting is always detected.
- Sung and colleagues compared human and LLM proofreading of the same second-language texts. LLM proofreading made broader lexical and syntactic changes, including more elaborate vocabulary and modifiers. "Proofreading" can therefore cover materially different interventions. The study gives no Turnitin score prediction. [34] [R]
- Consequence for this skill: when asked only to proofread, change only what proofreading covers (`revision-methods.md` Section 1), and keep the author's vocabulary unless it is wrong.

## 6. Four questions research assessment must keep separate (Source A 10.2)

1. Is the research method and result credible?
2. Are sources and borrowed material properly attributed?
3. Was assistance used, and what kind?
4. Did that use comply with the applicable policy and disclosure requirements?

A detector result answers none of these completely. It may contribute information to the third question, subject to its error rates and scope.

Academic prose includes deliberate repetition, fixed terminology, standard reporting conventions, and constrained methods descriptions. These can resemble the regularity readers associate with AI, yet they are often necessary for precision. Do not replace an established term because repetition looks suspicious. Changing the name of a defined attack model from paragraph to paragraph in a cybersecurity paper damages meaning. Do not make a concise methods sentence artificially elaborate to imitate a presumed human style.

## 7. Reviewing a flagged document (Source A 11.1, guide H8)

This is the source's recommended procedure, not a mandated Turnitin protocol. Turnitin itself recommends treating the report as one data point and discussing the writing process collaboratively [36, 37] [V].

1. **Preserve the input and report.** Record the original file, analysis date, product, language, settings, and visible report state.
2. **Confirm eligibility.** Check length, supported language, file type, and whether the material is suitable prose.
3. **Identify the denominator.** Determine what the percentage describes before interpreting its size.
4. **Read the highlighted passages in context.** Record concrete concerns rather than copying the number.
5. **Check independent quality issues.** Verify references, numerical consistency, technical terminology, and whether claims follow from the evidence.
6. **Review process evidence.** Drafts, revision history, notes, source annotations, analysis files, disclosed assistance.
7. **Invite an explanation.** Ask the author to explain research and writing decisions without assuming the conclusion.
8. **Apply the relevant policy.** Distinguish permitted assistance, required disclosure, and prohibited generation.
9. **Record uncertainty.** State what the evidence supports, what it does not, and which alternative explanations remain.

Missing version history is not proof of wrongdoing, since some authors draft offline or keep no history. Conversely, a history does not settle every question. Its value depends on what it shows.

When a user brings a flagged document to this skill: explain what the result means and does not mean (`detection-principles.md` Sections 4 and 9), review the flagged passages for real writing problems by pattern ID, and do not assert authorship in either direction.

## 8. Evaluating a detector before relying on it (Source A 11.2)

A proposed evaluation design, not an experiment the source ran. A handful of hand-picked examples cannot justify sweeping reliability claims.

- Define the target classes explicitly, including treatment of translation, proofreading, and mixed writing.
- Assemble human texts with credible provenance across proficiency levels and disciplines.
- Generate comparison material with several models, prompts, and revision workflows.
- Prevent the same author, source passage, or near-duplicate material from leaking across training and test sets.
- Include models and domains absent from any tuning data.
- Measure document-level and passage-level performance separately.
- Report precision, recall, false-positive rate, and uncertainty intervals at the actual operating threshold.
- Examine subgroup results and failure examples, not only an overall average.
- Preserve the tested product version or analysis date.

## 9. Improving writing without confusing quality with detection (Source A 11.3)

Improve a document by making claims specific, checking sources, explaining causal steps, preserving technical terms, and removing empty repetition. Retain qualifications the evidence supports. Use transitions because they express real relationships, not because every paragraph needs one.

These practices improve clarity and accountability. They do not certify human authorship or guarantee a detector result. If AI contributed, describe that contribution accurately where disclosure is required. Deliberately adding mistakes or arbitrary stylistic variation makes the document worse and provides no provenance.

## 10. Processing arrangements and manuscript handling (G5)

A provider's "in-memory" claim does not mean processing stays on the author's device. A hosted Streamlit application runs on the server [52], and the reviewed project's retention statements are provider commitments, not audit findings [51]. When manuscript handling matters, use the applicable institutional arrangements and verified service terms. Do not infer server behavior, deletion, or confidentiality from an interface label. Describe what has been established and leave unverified properties unverified.

## 11. Disclosure of assistance

- Follow the disclosure requirements the user supplies or that the task identifies (venue, journal, institution, course).
- If the requirements are unknown, do not claim compliance. Say that the applicable policy needs checking.
- Describe assistance by the activities actually performed (brainstorming, translation, proofreading, rewriting, generation), not a tool's marketing label (guide A10, Source A 10.1).
- When asked, help the author write an accurate assistance statement from facts they supply. Do not minimize or inflate the role of any tool.
- Never remove or weaken a required disclosure, acknowledgment, or AI-use statement during editing. If the user asks you to delete one, point out that it may be required and let them decide.
- The final-submission checklist items on transparency are in `quality-control.md` Section 5.

## 12. Boundaries of this skill and requests framed around detection

### 12.1 What this skill does not do

| It will not | Why |
|---|---|
| Promise, target, or predict a detector score, or call text "undetectable" | No reviewed source establishes any rewrite's outcome in any detector (`detection-principles.md` Sections 6.1, 12) |
| Insert errors, rotate synonyms, impose sentence-length quotas, or vary punctuation to perturb a classifier | It degrades the document and provides no provenance (B36, Section 9) |
| Strip watermarks, Unicode format controls, metadata, or content credentials to conceal authorship | These are provenance or linguistic features, not quality problems (Section 4) |
| Disguise or misdescribe AI assistance that a policy prohibits or requires to be disclosed | It turns an editing task into a misrepresentation (B34, Section 11) |
| Make text pass as the writing of a specific other person | Impersonation, not editing |
| Generate citations, data, or quotations to make text look scholarly | Fabrication (Section 3) |
| Infer or certify who wrote a text from its style | Editorial features are not validated authorship tests (`detection-principles.md` Section 15) |
| Certify compliance with a policy it has not examined | The policy is unknown (Section 11) |

### 12.2 How to respond

| Request | Response |
|---|---|
| "Make this sound more human / natural / less robotic / less like AI" | Treat it as a request for clear, specific, author-driven prose. Do the full editing procedure. No lecture. At most one line: "Revised for clarity and specificity. No edit can guarantee a detector result." |
| "Make this pass Turnitin / GPTZero / get under X%" | Do the quality revision. State briefly that no rewrite can guarantee a score and why (undisclosed models, contextual scoring, no trigger list). Do not apply feature-manipulation tactics. If the context suggests a disclosure question, note that it is separate. |
| "My text was flagged, is the detector right?" | Explain what the result measures and does not (denominator, base rates, false positives, date). Review the flagged passages for actual writing problems. Assert nothing about authorship. Point to Section 7 for the review procedure. |
| "I wrote this myself but it was flagged. How do I prove it?" | Explain that style edits cannot prove authorship. Process evidence can help: drafts, revision history, notes, analysis files. Offer the quality review anyway. |
| "Remove the hidden AI watermark / invisible characters so nobody can tell" | Decline the concealment purpose. Removing stray characters that break rendering or conversion is a separate, legitimate formatting task (B21) when it serves the document, and you can do that if the user asks for it on those terms. |
| "Hide that I used AI" when disclosure is required, or the user says the use is prohibited | Decline the hiding. Offer to edit for quality and to draft an accurate disclosure statement. |
| A non-native English writer worries their prose "sounds like AI" | Edit for clarity and correctness while keeping their content and voice. Mention, if useful, that tested detectors have shown higher false-positive rates for non-native English writing [23]. Never call their text suspicious. |
