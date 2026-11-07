# Writing patterns

Read this file to diagnose a passage. It holds the full inventory of 36 writing patterns (B01 to B36) from Section B of `natural_academic_writing_guide.md`, plus crosswalks to the rhetorical examples, structural observations, and Wikipedia advice-page categories in `AI Detection.md`.

## 1. Status and the diagnostic rule

**Every record here is an editorial recommendation [E]. Every example is constructed [I].** Research references support only the narrower findings attributed to them. None of these patterns is a diagnostic marker of AI authorship. A human can write every one of them, and an AI system can write prose without any of them (Source A 6.4).

A pattern is worth revising only when it causes a specific loss of meaning, evidence, coherence, or usability in this text. Do not assume a passage contains every pattern. Look for the ones actually present, then rank them by the priority column below.

When you report a problem, name it by ID and by what it costs the reader ("B05: the conclusion extends a benchmark result to deployment"). Never label prose "AI-sounding."

Every improved example uses only facts already present in its original or stated context. Several deliberately withdraw an unsupported claim. That withdrawal is a substantive correction, and a report must say so.

Semicolons inside the guide's constructed examples were changed to full stops or colons to fit the user's house style. No example's teaching point depends on the semicolon.

## 2. Pattern index

Priority is this skill's triage default [E], not a source finding. P1 affects meaning, evidence, or integrity. P2 affects clarity and coherence. P3 affects style and format. Fix P1 first.

| ID | Pattern | Category | Priority | Quick test |
|---|---|---|---|---|
| B01 | Generic opening and vague scene-setting | Rhetorical | P2 | Could the opening introduce any report after swapping the topic noun? |
| B02 | Unsupported importance, novelty, or significance | Evidential | P1 | Where is the comparison that supports this scale of claim? |
| B03 | Decorative transitions | Rhetorical | P3 | What relation does the connector assert, and is it real? |
| B04 | Vague mechanisms or processes | Specificity | P2 | Which operation produces the outcome? |
| B05 | Inference beyond the evidence | Evidential | P1 | Does the conclusion's setting match the evaluated setting? |
| B06 | Empty contrast | Rhetorical | P2 | What observable distinction separates the two sides? |
| B07 | Repetitive three-part descriptions | Rhetorical | P3 | Does each adjective name a distinct, tested property? |
| B08 | Abstract praise and promotional description | Rhetorical | P2 | What requirement does the praised thing actually meet? |
| B09 | Generic limitations and future work | Evidential | P2 | Which constraint limits which inference? |
| B10 | Unspecified consensus | Evidential | P1 | Who agrees, on what outcome, and who disagrees? |
| B11 | Empty reinforcement | Rhetorical | P2 | Is any inference lost if the sentence is deleted? |
| B12 | Repeated paragraph endings | Structural | P2 | Read only the last sentence of each paragraph. Are they the same verdict? |
| B13 | Unspecified interactions | Specificity | P1 | Was an interaction estimated, or were variables only observed? |
| B14 | Universal guarantees | Evidential | P1 | Do "every," "all," "ensures" match the test set or proof? |
| B15 | Redundant hedging | Rhetorical | P2 | What distinct uncertainty does each hedge carry? |
| B16 | Source-shaped filler | Evidential | P2 | What does the reader learn about the subject, not the source's value? |
| B17 | Repeating the same argument | Structural | P2 | What new proposition does each sentence add? |
| B18 | Mechanically uniform paragraphs | Structural | P3 | Do repeated scaffolds displace explanation? |
| B19 | Excessive headings | Structural | P3 | Does each heading introduce a distinct question or function? |
| B20 | Excessive lists and emphasis | Structural | P3 | Read without formatting. What explanation is missing? |
| B21 | Incompatible markup or conversion residue | Format | P3 | Does the rendered output show literal syntax? |
| B22 | Terminology drift | Lexical | P1 | Does one term name one concept throughout? |
| B23 | Abrupt style changes | Consistency | P2 | Does register or density change without reason? |
| B24 | Drafting residue and conversational instructions | Integrity | P1 | Are placeholders, editor notes, or chat replies left in? |
| B25 | Tortured technical terminology | Lexical | P1 | Does the wording match the discipline's established term? |
| B26 | Contradictions across methods, results, figures, conclusions | Integrity | P1 | Do counts, designs, and findings agree across locations? |
| B27 | Incorrect or incomplete bibliographic identity | Integrity | P1 | Do authors, title, year, venue, and DOI name the same work? |
| B28 | Citations that do not support the claim | Integrity | P1 | Does the cited source contain this result at this scope? |
| B29 | Removing necessary repetition | Lexical | P1 | Could readers infer two different objects from two labels? |
| B30 | Missing operational detail | Specificity | P1 | Could a competent reader reproduce the procedure? |
| B31 | Overloaded sentences and abstract noun chains | Syntactic | P2 | Which action verbs are hidden inside nouns? |
| B32 | Ambiguous referents or missing actors | Syntactic | P1 | List every plausible referent of the pronoun. |
| B33 | Mixing observation, interpretation, and speculation | Evidential | P1 | Which clause was observed, which tested, which proposed? |
| B34 | Misleading edit summaries and undocumented substantive changes | Integrity | P1 | Does the change log match what the edit did to the claim? |
| B35 | Unverifiable tool, performance, or privacy claims | Evidential | P1 | Is there implementation, test, or measurement evidence? |
| B36 | Artificial variation and universal style rules | Lexical | P1 | What reader need does the proposed change serve? |

## 3. Crosswalk: Source A rhetorical examples (Section 6.4)

Source A constructed these sixteen examples for close reading. They are not quotations, validated AI indicators, or predictions of Turnitin scores. The review questions concern meaning and evidence whoever wrote the text. [I]

| Pattern | Illustrative wording | Useful review question | Record |
|---|---|---|---|
| Vague scene-setting | "Across today's changing technical environment, this subject has become essential." | What specific change makes the subject relevant? | B01 |
| Importance without evidence | "The approach represents a pivotal advance for the entire field." | What result supports that scale of importance? | B02 |
| Unspecified mechanism | "The system improves efficiency by enhancing the overall workflow." | Which operation changes, and how does that save effort? | B04 |
| Decorative transitions | "Furthermore, the device weighs 20 grams." | Is this an additional argument, or another fact? | B03 |
| Unsupported inference | "The classifier scored well, therefore deployment will succeed." | What bridges benchmark performance and deployment? | B05 |
| Unnecessary contrast | "The method is not merely a tool: it is a new way of thinking." | Is there a substantive distinction? | B06 |
| Repeated three-part descriptions | "It is flexible, efficient, and effective." | Are these separate evaluated properties? | B07 |
| Abstract praise | "The framework offers a comprehensive and sophisticated solution." | What requirements does it actually satisfy? | B08 |
| Generic limitation | "Despite the challenges, further work could unlock its potential." | Which limitation and which next experiment? | B09 |
| Unspecified consensus | "Researchers agree that the technique is superior." | Which studies, and superior on which criterion? | B10 |
| Empty reinforcement | "This observation clearly emphasizes the importance of the result." | Does the sentence add an explanation? | B11 |
| Repeated closing claim | Each subsection ends by declaring the approach promising. | Does each ending contribute a distinct implication? | B12 |
| Inflated relation | "A complex interplay connects the relevant dimensions." | Which variables interact, and what evidence shows it? | B13 |
| Unearned certainty | "The system ensures reliable performance in every environment." | Were those environments actually evaluated? | B14 |
| Excessive qualification | "The result may perhaps potentially suggest some improvement." | What uncertainty is supported, and what is redundant? | B15 |
| Source-shaped filler | "Available sources offer valuable insights into this topic." | Which source supports which statement? | B16 |

Several examples sound formulaic because they omit substantive information. That is a writing-quality diagnosis, nothing more.

## 4. Crosswalk: Source A structural and formatting observations (Section 6.5)

Additional editorial checks, not classifier specifications. The third column matters: every observation has an ordinary explanation, so none supports an authorship inference.

| Observation | What to inspect | Plausible non-AI explanation | Record |
|---|---|---|---|
| Nearly identical paragraph shapes | Whether each paragraph develops its own point | A teaching template or journal convention | B18 |
| Many headings for very little content | Whether organization helps the reader | A presentation outline adapted into prose | B19 |
| Heavy bolding or frequent lists | Whether formatting fits the genre | Personal preference or an accessibility choice | B20 |
| Markdown symbols in an incompatible file | Whether conversion was incomplete | Copying from an ordinary Markdown editor | B21 |
| Sudden terminology changes | Whether one concept is renamed inconsistently | Several coauthors or inconsistent editing | B22 |
| Abrupt style changes | Whether revisions or contributions explain them | Copyediting, translation, or coauthorship | B23 |
| Unresolved drafting placeholders | Whether the document is unfinished | A human working draft | B24 |
| Conversational instructions inside a paper | Whether quoted material or drafting notes were left in | A transcription or editing mistake | B24 |
| Strange substitutions for standard terms | Whether the terminology still makes technical sense | Translation problems or automated paraphrasing (tortured phrases predate ChatGPT [33]) | B25 |
| Internally inconsistent methods and results | Whether the claimed experiment can be reconstructed | An ordinary revision error, or a more serious research problem | B26 |

## 5. Crosswalk: Wikipedia advice-page categories [26] [C]

The *Signs of AI writing* page is community advice, not policy and not a detector specification. Its categories help locate problems. Interpret them in the document's genre: a reference guide needs headings and lists, and a methods section needs repeated terminology.

| Advice-page category | Where this skill handles it |
|---|---|
| Exaggerated importance | B02, B08 |
| Shallow analysis | B04, B11, B16, B17, and literature synthesis (`revision-methods.md` E2) |
| Promotion | B07, B08, vocabulary entries for boasts, showcase, garner, vibrant |
| Vague attribution | B10, B16 |
| Formulaic rhetoric | B01, B03, B06, B07, B09, B12 |
| Formatting | B19, B20 |
| Conversational leftovers | B24 |
| Markup | B21 |
| Citations | B27, B28 |
| Edit summaries | B34 |
| Style changes | B23 |
| Historical punctuation observations (heavy em-dash use) | `vocabulary-and-phrases.md` Section 7. Punctuation does not establish provenance. |

## 6. Pattern records

Each record gives the definition, why the pattern can weaken writing, a diagnostic test, the revision principle, a constructed example, and the qualification that says when to leave the feature alone. Read the qualification before you edit.

### B01. Generic opening and vague scene-setting

- **Definition:** Broad context that does not identify the actual problem.
- **Why it weakens writing:** It consumes attention before giving the reader a reason to continue.
- **Diagnosis:** Could the opening introduce almost any report after changing the topic noun?
- **Revision principle:** Begin with the supplied problem. Add context only if it explains that problem.
- **Example:** "In today's changing environment, record management is increasingly important. This report examines duplicate entries in the intake register." → "This report examines duplicate entries in the intake register."
- **Keep when:** Readers need the context to understand the specific question. Do not delete relevant historical or disciplinary framing.

### B02. Unsupported importance, novelty, or significance

- **Definition:** Calling a contribution pivotal, unprecedented, or field-changing without the comparison needed to support that scale.
- **Why it weakens writing:** It replaces an assessable contribution with a reputation claim.
- **Diagnosis:** Locate the literature search or direct comparison supporting "unprecedented."
- **Revision principle:** State the documented contribution. Keep novelty only when its scope is substantiated.
- **Example:** "This unprecedented study compares the two coding schemes." → "This study compares the two coding schemes."
- **Keep when:** The novelty claim has a stated comparison and scope. Removing "unprecedented" narrows an unsupported claim. It is a substantive correction, not an assertion that the work lacks novelty. Statistical significance needs its own statistical meaning and evidence.

### B03. Decorative transitions

- **Definition:** A connector that adds no useful logical relation or signals the wrong one.
- **Why it weakens writing:** It creates artificial argumentation or distracts from a plain fact.
- **Diagnosis:** Identify what preceding proposition the new sentence extends, contrasts with, or follows from.
- **Revision principle:** Keep the connector only if that relation matters in context.
- **Example:** "Furthermore, the device weighs 20 grams." → "The device weighs 20 grams."
- **Keep when:** The relation is real. "Furthermore" is useful if weight is a second reason in a portability argument. The number and unit stay unchanged either way.

### B04. Vague mechanisms or processes

- **Definition:** Explaining an outcome with another general outcome word.
- **Why it weakens writing:** Readers cannot reconstruct how the system operates.
- **Diagnosis:** Underline the actual operation separately from the benefit claim.
- **Revision principle:** Describe the operation and drop an unmeasured benefit.
- **Example:** "The macro improves efficiency by enhancing the workflow. It copies the entered address into the second form." → "The macro copies the entered address into the second form."
- **Keep when:** A measured time or error benefit exists. Report it separately with its evidence. The revision intentionally removes the unsupported efficiency claim.

### B05. Inference beyond the evidence

- **Definition:** Moving from an evaluated observation to an untested conclusion.
- **Why it weakens writing:** It hides the assumptions the inference needs.
- **Diagnosis:** Compare the evaluation setting with the setting named in the conclusion.
- **Revision principle:** State the observation and identify the untested extension.
- **Example:** "The classifier performed well on the benchmark, so it will succeed in deployment." → "The classifier performed well on the benchmark. Deployment performance remains untested."
- **Keep when:** The extension is itself evaluated. Note that "performed well" still needs a metric and comparator in a real manuscript. The revision corrects the inference but cannot supply missing evaluation details.

### B06. Empty contrast

- **Definition:** A rhetorical opposition with no operational distinction.
- **Why it weakens writing:** It makes a modest statement sound deeper without explaining it.
- **Diagnosis:** Ask what observable distinction separates the two sides.
- **Revision principle:** Keep the actual function, or explain a real conceptual contrast.
- **Example:** "The index is not merely a tool: it is a new way of thinking. It groups records by topic." → "The index groups records by topic."
- **Keep when:** The contrast is substantive, for example association versus causation or two competing explanations. The problem is unsupported opposition, not the grammatical construction.

### B07. Repetitive three-part descriptions

- **Definition:** Recurrent triplets of overlapping adjectives presented as substance.
- **Why it weakens writing:** The rhythm can conceal missing definitions and evidence.
- **Diagnosis:** For each adjective, name a distinct property and its supporting test.
- **Revision principle:** Replace unevaluated labels with supplied capabilities.
- **Example:** "The interface is flexible, efficient, and effective. It accepts text and spreadsheet files." → "The interface accepts text and spreadsheet files."
- **Keep when:** Three distinct measured outcomes are reported together. There is no objection to the number three. The issue is unsupported or overlapping content.

### B08. Abstract praise and promotional description

- **Definition:** Labels such as sophisticated, comprehensive, or excellent without defined criteria.
- **Why it weakens writing:** Readers cannot assess which requirements are met.
- **Diagnosis:** Do the adjectives name any capability beyond the stated functions?
- **Revision principle:** Describe the verified scope of the system.
- **Example:** "The sophisticated framework provides a comprehensive solution for sorting and filtering records." → "The framework sorts and filters records."
- **Keep when:** "Comprehensive" is justified against an explicit, bounded requirement set. Removing the adjective does not imply the system is simple or inadequate.

### B09. Generic limitations and future work

- **Definition:** Admitting unspecified challenges and recommending unspecified research.
- **Why it weakens writing:** It does not tell readers which conclusions are limited or how uncertainty could be reduced.
- **Diagnosis:** Identify the constraint, the affected inference, and the relevant next comparison.
- **Revision principle:** Connect an actual limitation to an appropriately framed next step.
- **Example:** "Further research is needed to unlock the method's potential. The evaluation used one site." → "The evaluation used one site. Evaluation at other sites would help assess transferability."
- **Keep when:** Never invent limitations to fill a section. The proposed evaluation is a recommendation, not a completed experiment.

### B10. Unspecified consensus

- **Definition:** Attributing agreement to researchers, experts, or the literature without identifying evidence.
- **Why it weakens writing:** It launders an assertion through an unnamed authority.
- **Diagnosis:** Identify who agrees, the outcome compared, and any relevant disagreement.
- **Revision principle:** Supply support, or recast the statement as the question actually under investigation.
- **Example:** "Researchers agree that method A is superior to method B." → "Whether method A outperforms method B on the target outcome requires evidence."
- **Keep when:** Agreement is verified. State it with scope and citations. This revision withdraws an unsupported claim. It is not a substitute for a supported literature synthesis.

### B11. Empty reinforcement

- **Definition:** A sentence announces that the previous sentence is important without explaining why.
- **Why it weakens writing:** It adds length without advancing the argument.
- **Diagnosis:** Delete the second sentence and check whether any inference is lost.
- **Revision principle:** Delete it, or replace it with a supported explanation.
- **Example:** "The two estimates differ. This clearly emphasizes the importance of the finding." → "The two estimates differ."
- **Keep when:** It carries a real implication. The size, uncertainty, and meaning of the difference still need discussion elsewhere. Do not invent them to justify keeping a second sentence.

### B12. Repeated paragraph endings

- **Definition:** Several paragraphs end with the same general positive verdict.
- **Why it weakens writing:** It flattens distinct findings into one repeated conclusion.
- **Diagnosis:** Read only the final sentence of every paragraph in a section.
- **Revision principle:** End each paragraph with its own finding, implication, limitation, or necessary transition.
- **Example:** "The parser identifies missing dates. These findings demonstrate promise." (the next paragraph repeats the same verdict) → "The parser identifies missing dates."
- **Keep when:** A repeated caution prevents readers from misapplying separate results. The repetition must serve that identifiable need.

### B13. Unspecified interactions

- **Definition:** Invoking an interplay or relationship without naming the variables and the type of relation.
- **Why it weakens writing:** It blurs association, interaction effects, feedback, and causation.
- **Diagnosis:** Was an interaction estimated, or were the variables only observed?
- **Revision principle:** Report the established action. Reserve the stronger relation for supporting analysis.
- **Example:** "A complex interplay links temperature and growth. The study records both variables." → "The study records temperature and growth."
- **Keep when:** An interaction is estimated. Then define the model and scale. "Interplay" is not automatically a statistical interaction term.

### B14. Universal guarantees

- **Definition:** Extending a finding to every environment, input, or future use.
- **Why it weakens writing:** It conceals the boundary of testing or proof.
- **Diagnosis:** Compare universal words with the actual test set or formal assumptions.
- **Revision principle:** State what testing covered without implying an unreported result.
- **Example:** "The parser handles every document correctly. Testing covered the supplied sample files." → "Parser testing covered the supplied sample files."
- **Keep when:** A formal guarantee holds within its demonstrated assumptions. The revision does not claim the sample files passed, because the original gives no pass results.

### B15. Redundant hedging

- **Definition:** Several overlapping uncertainty markers without a clearer boundary.
- **Why it weakens writing:** Readers cannot tell what is uncertain or how much confidence is warranted.
- **Diagnosis:** Identify the uncertainty each hedge communicates.
- **Revision principle:** Keep the necessary uncertainty once and explain its basis nearby.
- **Example:** "The estimate may perhaps potentially indicate a reduction." → "The estimate may indicate a reduction."
- **Keep when:** Always keep one marker of real uncertainty. This is a local repair. A real report should say whether the uncertainty comes from interval width, measurement, design, or another documented issue.

### B16. Source-shaped filler

- **Definition:** Saying sources offer insights without stating what they establish.
- **Why it weakens writing:** The sentence resembles scholarship while contributing no finding.
- **Diagnosis:** What does the reader learn about the process, rather than about the source's value?
- **Revision principle:** State the source's specific contribution.
- **Example:** "The manual offers valuable insights into the scoring process. It defines the score's denominator." → "The manual defines the score's denominator."
- **Keep when:** The genre evaluates sources (an annotated bibliography). Even then, explain the basis of the evaluation.

### B17. Repeating the same argument

- **Definition:** Restating a rationale across sentences or sections without a new function.
- **Why it weakens writing:** It obscures the progression of the argument.
- **Diagnosis:** Map each sentence to the proposition it adds.
- **Revision principle:** State the decision and its reason once, in the relevant location.
- **Example:** "We excluded incomplete records because their outcome was missing. Records without the outcome were excluded because they were incomplete." → "We excluded records with missing outcomes."
- **Keep when:** The rule must appear in a flow diagram or a critical limitation for interpretation. Do not remove required reporting because the information appears elsewhere.

### B18. Mechanically uniform paragraphs

- **Definition:** Every paragraph gets the same opening, evidence count, and closing verdict regardless of purpose.
- **Why it weakens writing:** The template can displace explanation or force filler.
- **Diagnosis:** Compare each paragraph's function with its repeated scaffolding.
- **Revision principle:** Keep the substantive unit and develop it only as far as the evidence allows.
- **Example:** "First, speed matters. The report measures runtime. This is important." → "The report measures runtime."
- **Keep when:** A template helps novice writers or standardizes reports. Add the metric definition and comparison if available. Do not invent them to make paragraphs equally long.

### B19. Excessive headings

- **Definition:** Labels divide content more finely than the reader's tasks require.
- **Why it weakens writing:** Fragmentation interrupts relations that belong together.
- **Diagnosis:** Does each heading introduce a distinct question or function?
- **Revision principle:** Combine overlapping sections under one informative heading.
- **Example:** Three one-sentence sections titled "Runtime," "Runtime Finding," and "Runtime Summary" that repeat one observation → one "Runtime" section holding the observation and its qualification.
- **Keep when:** The document is a reference guide, protocol, or accessibility-oriented text. Heading density depends on how the document will be used.

### B20. Excessive lists and emphasis

- **Definition:** Formatting gives every item equal visual weight or turns connected reasoning into fragments.
- **Why it weakens writing:** Readers cannot see which point is central or how statements connect.
- **Diagnosis:** Read the text without formatting and identify the missing explanation.
- **Revision principle:** Use emphasis for navigation or a few consequential distinctions.
- **Example:** "**Important result:** **The estimate changed.** **This matters.**" → "The estimate changed."
- **Keep when:** Items are parallel criteria or procedural steps. In a final paper, say how and why the estimate changed if the evidence permits. Formatting cannot supply that information.

### B21. Incompatible markup or conversion residue

- **Definition:** Literal formatting commands appear where the output format should render them.
- **Why it weakens writing:** It can obscure headings, equations, references, or emphasis.
- **Diagnosis:** Inspect the rendered submission format, not only the editing source.
- **Revision principle:** Convert syntax to the destination's actual structure.
- **Example:** A Word heading that visibly reads "## Results" → a heading styled "Results" at the correct level.
- **Keep when:** The markup is correct for the format: code samples, or Markdown headings in a Markdown file. Judge compatibility, not the characters.

### B22. Terminology drift

- **Definition:** Renaming one concept, or using one name for distinct concepts, without explanation.
- **Why it weakens writing:** Readers cannot trace measurements or groups across sections.
- **Diagnosis:** Build a term-to-definition map and look for collisions.
- **Revision principle:** Restore the stated term while checking the underlying calculation.
- **Example:** "We define R as recall. The accuracy R is reported below." → "We define R as recall. Recall R is reported below."
- **Keep when:** Never by preference. If the calculation actually measures accuracy, a wording repair is insufficient. Resolve the definition and analysis with the author.

### B23. Abrupt style changes

- **Definition:** Unexplained changes in register, technical density, or perspective.
- **Why it weakens writing:** Readers may mistake a change of tone for a change of scope or evidence.
- **Diagnosis:** Read the transitions between coauthor contributions and edited passages.
- **Revision principle:** Use a consistent register while preserving the known sequence.
- **Example:** "Specimens were stored in sealed containers. Then we did the cool part: microscopy." → "Specimens were stored in sealed containers and then examined by microscopy."
- **Keep when:** The material is quoted speech, field notes, or an audience-specific section. Coauthorship and translation are plausible explanations. A style change is not proof of AI use.

### B24. Drafting residue and conversational instructions

- **Definition:** Placeholders, editor requests, or chat responses left in submitted prose.
- **Why it weakens writing:** They reveal unfinished content and may leave claims unsupported.
- **Diagnosis:** Search for placeholders. Read tables, captions, appendices, and comments as well as prose.
- **Revision principle:** Resolve missing facts from records and remove instructions that do not belong.
- **Example:** "Insert the sample size here. Let me know if you want a shorter version." → delete the conversational sentence and log "Sample size requires verification" as an author query until verified.
- **Keep when:** The instruction is research material under study, clearly marked as a quotation. The log entry is not submission-ready prose.

### B25. Tortured technical terminology

- **Definition:** Replacing an established term with a semantically unreliable paraphrase.
- **Why it weakens writing:** The replacement can describe a different concept or no recognized concept.
- **Diagnosis:** Compare the wording against the operational definition and the discipline's terminology.
- **Revision principle:** Restore the established term rather than search for a more unusual synonym.
- **Example:** "The synthetic reasoning web" (where the methods define an artificial neural network) → "The artificial neural network."
- **Keep when:** Never for a defined object. This invented example is not a quotation from the tortured-phrases study [33], which documents a broader problem that predates ChatGPT. Awkward substitution does not identify its cause.

### B26. Contradictions across methods, results, figures, and conclusions

- **Definition:** Different locations describe incompatible counts, designs, or findings.
- **Why it weakens writing:** The study cannot be reconstructed or interpreted reliably.
- **Diagnosis:** Reconcile each value with its population, stage, and authoritative record.
- **Revision principle:** Resolve the discrepancy before editing either number.
- **Example:** Methods say "20 participants," results say "22 participants," with no explanation → author query: "Verify whether 20 and 22 refer to analyzed and enrolled participants. Do not assign these meanings without records."
- **Keep when:** Different denominators may both be correct. No numerical replacement is justified until the facts are known.

### B27. Incorrect or incomplete bibliographic identity

- **Definition:** Authors, title, year, venue, DOI, or other fields point to incompatible or unverified works.
- **Why it weakens writing:** Readers cannot locate the source, or locate the wrong one.
- **Diagnosis:** Compare the fields with an authoritative record.
- **Revision principle:** Identify the intended work before correcting the entry.
- **Example:** "Article A" paired with a DOI whose record names "Article B" → author query: "Verify the intended article and replace the mismatched identifier with its verified record."
- **Keep when:** Never guess. The editor cannot invent the correct DOI. A real identifier is not enough: it must belong to the intended work.

### B28. Citations that do not support the claim

- **Definition:** A real source is cited for a finding, population, or certainty it does not establish.
- **Why it weakens writing:** It gives an unsupported claim the appearance of evidence.
- **Diagnosis:** Locate the exact supporting result and compare scope word by word.
- **Revision principle:** Narrow the claim to the verified contribution, or obtain appropriate evidence.
- **Example:** "The method works in all hospitals," supported only by a single-site evaluation → "The cited study evaluates the method at one hospital."
- **Keep when:** The source supports the claim at that scope. This correction intentionally removes the unsupported success and generalization claims and keeps the citation.

### B29. Removing necessary repetition

- **Definition:** Introducing synonyms to avoid repeating a term whose identity matters.
- **Why it weakens writing:** Artificial variety makes objects appear to change.
- **Diagnosis:** Could readers reasonably infer two different populations or objects?
- **Revision principle:** Repeat the stable term when identity is the point.
- **Example:** "The control group received no intervention. This reference population was assessed again." (both labels denote one defined group) → "The control group received no intervention and was assessed again."
- **Keep when:** A pronoun is clear because only one referent is possible. Defined terms, legal wording, and standard methods often need repetition.

### B30. Missing operational detail

- **Definition:** A method names a general action but omits the rule needed to reproduce it.
- **Why it weakens writing:** Readers cannot tell which observations or procedures the result depends on.
- **Diagnosis:** Could a competent reader reproduce exclusions and transformations from the description?
- **Revision principle:** Retrieve the actual rules from code or records. Never substitute plausible details.
- **Example:** "We cleaned the data using appropriate procedures." → author query: "Specify the actual exclusion, missing-data, and transformation rules used."
- **Keep when:** The rules appear in an accessible appendix. A precise cross-reference may then suffice. This is a reproducibility issue, not only a style defect.

### B31. Overloaded sentences and abstract noun chains

- **Definition:** Several operations or qualifications buried in nested clauses and nominalizations.
- **Why it weakens writing:** The reader must reconstruct actors, sequence, and dependencies.
- **Diagnosis:** Identify the action verbs hidden inside nouns and verify the sequence.
- **Revision principle:** Express the action directly without losing temporal conditions.
- **Example:** "The implementation of the evaluation of the records was performed by the team after the completion of collection." → "The team evaluated the records after collection."
- **Keep when:** A nominalization names an established concept, or a long sentence preserves essential conditions. Shortening helps only if the meaning stays intact.

### B32. Ambiguous referents or missing actors

- **Definition:** Pronouns or passive constructions leave a consequential object or agent unclear.
- **Why it weakens writing:** Different readers may infer different procedures.
- **Diagnosis:** List every plausible referent of the pronoun.
- **Revision principle:** Name the intended object after consulting the author or records.
- **Example:** "The analysts compared the surveys with the interviews and revised them." → only if the author confirms the surveys were revised: "The analysts compared the surveys with the interviews and revised the surveys."
- **Keep when:** The agent is clear or irrelevant, in which case passive voice is fine. The conditional example is not permission to assume the referent.

### B33. Mixing observation, interpretation, and speculation

- **Definition:** One declarative statement makes a proposed explanation look like an observed result.
- **Why it weakens writing:** It conceals which parts of the argument were tested.
- **Diagnosis:** Assign each clause to observation, tested explanation, or hypothesis.
- **Revision principle:** State the observation and label the untested explanation.
- **Example:** "The response rate increased because the reminder improved motivation." (only the increase was observed) → "The response rate increased. Improved motivation is one possible explanation, but it was not measured."
- **Keep when:** The explanation was tested. In a real draft, verify that motivation was not measured before adding the qualification. Other explanations may also remain possible.

### B34. Misleading edit summaries and undocumented substantive changes

- **Definition:** A revision described as stylistic even though it changes the claim.
- **Why it weakens writing:** Coauthors cannot review what actually changed.
- **Diagnosis:** Compare verbs, scope, negation, and evidence before and after the edit.
- **Revision principle:** Restore the supported claim and describe substantive changes accurately.
- **Example:** An edit replaces "was associated with" with "caused" while the change log says "grammar only" → keep "was associated with" and record any separate wording change without claiming a causal finding.
- **Keep when:** Never. This applies to your own edits too: a narrowed or withdrawn claim must be reported as substantive. Revision histories are contextual evidence, not authorship tests.

### B35. Unverifiable tool, performance, or privacy claims

- **Definition:** Treating documentation, interface animation, or a provider promise as a measured property.
- **Why it weakens writing:** It confuses stated design with tested behavior.
- **Diagnosis:** Locate the executable implementation, preservation tests, and actual external measurements.
- **Revision principle:** Attribute the visible behavior and separate what remains unverified.
- **Example:** "The demo score fell, proving that the application preserves every fact and passes external detection." → "The demo displays a lower score. That display does not establish preservation or external detector performance."
- **Keep when:** The interface displays real measurements from a verified data source. The source's repository review documents scripted meters as a counterexample [38–44].

### B36. Artificial variation and universal style rules

- **Definition:** Altering sentence lengths, vocabulary, grammar, or punctuation to fit an assumed authorship profile.
- **Why it weakens writing:** The change can damage precision without solving a communication problem.
- **Diagnosis:** Ask what reader need each proposed change serves.
- **Revision principle:** Change wording only for a documented improvement in meaning or usability.
- **Example:** "Replace every repeated technical term with a different synonym and insert occasional errors." → "Keep defined technical terms consistent and revise sentences whose structure obscures their meaning."
- **Keep when:** Genuine repetition and complexity problems still deserve attention. Research on feature distributions does not establish a universal human style or a safe detector target [19–21, 34]. A house style the user supplies (for example, no em dashes) is a legitimate requirement, but it is applied as house style, never as a detection tactic.
