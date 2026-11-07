# Detection principles

Read this file when you need to explain how AI-writing detection works, interpret a Turnitin, iThenticate, or GPTZero result, judge a claim made by a detector or a "humanizer" tool, or decide whether a writing feature says anything about authorship. It is not a guide to changing a score. Section 15 states what the findings mean for editing.

**Sources.** `AI Detection.md` (*How AI Writing Detection Works*, research snapshot 24 October 2026, Saudi Arabia time) and Section H of `natural_academic_writing_guide.md`. Bracketed numbers point to `bibliography.md`. The source report is a documentary review. It ran no detector experiment and submitted nothing to Turnitin or iThenticate.

## Contents

0. Evidence labels
1. Terms
2. Similarity checking versus AI detection
3. How detectors work
4. Turnitin and iThenticate (dated snapshot)
5. Measurable patterns that can distinguish texts
6. Words, phrases, and rhetorical patterns
7. The two Wikipedia pages
8. Source quality
9. Accuracy, false positives, and statistical interpretation
10. Mixed authorship and review procedures (pointer)
11. Misconceptions about detection and interpretation
12. What remains unknown
13. Turnitout-Humanizer repository review
14. Summary of the evidence boundary
15. What these findings mean for writing review

## 0. Evidence labels

Every finding below carries one of these labels. Keep the label when you repeat a finding to a user. Do not upgrade a vendor claim or a community observation into a research finding.

| Label | Meaning | What it cannot establish |
|---|---|---|
| [V] Provider documentation | What a vendor, maintainer, or standards body says about its own product or specification | Independent validation of performance claims |
| [P] Project documentation | What a project says it does or intends (documented design) | That the code exists or behaves as described |
| [O] Verified source observation | Public code that the source report inspected directly at a pinned commit | Behavior of private code or a hosted service |
| [R] Research finding | A result reported by a named study under its stated conditions | A universal rule about every writer, model, or detector |
| [C] Community observation | The Wikipedia advice page and encyclopedia overview | A product specification or a validated test |
| [E] Editorial observation or recommendation | A feature a reader can inspect, or a reasoned test of clarity, evidence, or coherence | A validated test of AI authorship |
| [I] Illustrative | A constructed example, hypothetical calculation, or recommended procedure | A measured result or a detector experiment |
| [U] Unknown | Not established by the reviewed public evidence | Anything. Leave the gap visible. |

The source report used four labels (vendor documentation, research evidence, editorial observation, illustrative analysis). The guide used four (research finding, vendor or project documentation, editorial recommendation, constructed illustration). This file keeps vendor and project documentation apart because the source's repository review separates documented design from verified code observations.

**Snapshot warning.** Product facts in Section 4 describe the 24 October 2026 snapshot. Before anyone relies on them for a current decision (eligibility, display rules, languages, account features), say that they need rechecking against the provider's current documentation.

## 1. Terms

| Term | Meaning |
|---|---|
| AI-generated text | Wording produced by a generative model, whether or not a person later edits it |
| AI-assisted writing | A broader workflow that can include brainstorming, translation, proofreading, rewriting, or generation. These activities are not interchangeable. |
| Similarity | Measured overlap with other text available to a matching system |
| Plagiarism | A judgment about inappropriate appropriation or attribution. It requires contextual review. |
| Detection score | A system-specific output. Its meaning must be read from that system's documentation. |
| Qualifying text | The material a particular detector actually analyzes and includes in its reported proportion |
| Provenance | Evidence about a document's creation and revision history |
| Stylometry | Quantitative analysis of writing characteristics, such as vocabulary and syntax |
| False positive | Human text classified as AI under the evaluation's labeling rules |
| False negative | AI text classified as human under those rules |

## 2. Similarity checking versus AI detection

| Dimension | Similarity checking | AI writing detection |
|---|---|---|
| Main question | Does this text overlap with material the system can compare? | Does this text resemble examples associated with AI generation? |
| Main evidence | Matching passages and identified sources | Statistical classification of submitted text |
| Typical output | Similarity percentage and source matches | AI indicator, percentage, and passage highlights |
| What it does not establish | Whether a match is improper or adequately attributed | The drafting process, permission status, or intent |

- iThenticate says quotations and referenced material can still produce matches. Reviewers must inspect matches rather than equate a percentage with plagiarism. [1, 2] [V]
- Exclusion settings can remove selected material from the similarity calculation, so two reports can differ because of their settings. Do not assume those settings control the separate AI analysis. [35] [V]
- A paraphrase can still require citation even when few words match. Low overlap does not remove attribution duties. [E]

Four combinations (conceptual examples, not measured results) [I]:

| Similarity | AI indicator | Possible interpretation |
|---|---|---|
| Low | Low | Original human writing, or AI writing the detector missed |
| Low | High | Newly generated wording with few source matches, or a false positive |
| High | Low | Quoted, formulaic, reused, or copied text. Attribution still needs review. |
| High | High | Both source overlap and AI-like features. Each finding needs its own investigation. |

The two percentages cannot be added to produce a misconduct percentage. They measure different properties and can use different denominators.

## 3. How detectors work

| Finding | Meaning | Source and level | Limits | Relevance to writing review |
|---|---|---|---|---|
| General pipeline | Extract text, identify supported language and eligible content, split into tokens, sentences, or overlapping passages, compute features or neural representations, score units, apply thresholds and aggregate, display an interpretation | Source A 3.1 [I] (conceptual, not Turnitin source code) | Every stage can change the result. A sentence scored with surrounding context is a different input from the same sentence pasted alone. A PDF's extracted reading order can differ from its visual layout. | Reproducing an analysis requires the actual file and processing conditions, not only the visible words |
| Perplexity | PPL(x) = exp(-(1/N) Σ log p_θ(x_i given x_<i)). Lower perplexity means the sequence is more predictable to the scoring model. | Source A 3.2 [R] (standard measure) | Depends on the model, tokenizer, context length, and genre. A standard methods phrase can be predictable because many researchers use it. A rare technical term can be unpredictable because it is rare in the model's data. Low perplexity does not mean false, unoriginal, or machine-generated. | Never edit to raise perplexity. Predictable, conventional reporting language can be correct human prose. |
| GLTR | Visualizes token probability and rank patterns so people can inspect generated text | [11] [R] | An early research tool. Not a description of current Turnitin. | Shows why runs of likely choices can be informative in aggregate, nothing more |
| Burstiness | Used loosely for variation in sentence-level predictability, and sometimes for variation in sentence length or structure. These are only loosely related. | Source A 3.3 [E] | GPTZero states it moved away from perplexity and burstiness to a deep-learning architecture in autumn 2023. A numerical cutoff from an old article is not a universal test. [12] [V] | Do not set sentence-length or variation targets |
| Supervised classifiers | Learn a mapping from labeled passages to a score. A neural model can combine contextual features without exposing a simple rule list. | Source A 3.4 [E] | Training choices (human genres, generation models, prompts, languages, editing workflows) define what the detector has seen. Only genuinely held-out evaluation shows it learned more than topic or dataset artifacts. | No list of rules exists to "write around" |
| Turnitin and GPTZero architectures | Turnitin describes transformer classifiers [4]. GPTZero's 2026 technical report describes a hierarchical, multi-task system with granular predictions and automated adversarial testing [13]. | [4, 13] [V] | Provider descriptions. They do not establish correct classification of every unseen document or workflow. | Report these as vendor claims |
| Stylometric classifiers | Explicit measurements: word frequencies, part-of-speech distributions, punctuation, syntactic constructions, lexical diversity. Bagdasarov and Alves compared scientific writing from humans and three LLMs and tested lexical and syntactic features with random forests. | [19] [R] | Supports studying distributions of features, not treating one stylistic habit as decisive | A single habit (a word, a punctuation mark) proves nothing about one document |
| Zero-shot statistical detection | Detects without training a separate classifier on labeled data for the target task. The underlying language models were still trained. DetectGPT compares a passage's log probability with perturbed versions (probability curvature) [14]. Fast-DetectGPT uses conditional probability curvature for efficiency [15]. Binoculars contrasts scores from two related pretrained models [16]. | [14–16] [R] | Results depend on the scoring model and evaluation setting. These are research methods, not evidence that a commercial product uses them. | Signals can come from relationships among probabilities, not from an inventory of suspicious words |
| Watermarking | A detectable statistical signal inserted during generation. Kirchenbauer and colleagues softly favor a pseudorandom subset of tokens, then test whether a sequence has the expected excess. | [17] [R]. SynthID modifies token-generation probabilities and can withstand some editing [47] [V]. | Requires compatible generation and detection. Absence of a watermark does not prove human authorship. The reviewed Turnitin materials describe classification, not a universal watermark reader. No reviewed evidence supports the claim that all ChatGPT prose carries a hidden marker that Turnitin retrieves. | Watermarks, Unicode characters, metadata, and classification are different mechanisms (Section 13.5) |
| Retrieval-based detection | Compares a passage against available records of generated text | [25] [R] | Coverage depends on which records exist and can be searched | None for wording. It is a records question. |
| Provenance | Dated drafts, revision histories, research notes, or a disclosed generation transcript can reconstruct a workflow | Source A 3.8 [E] | Answers questions a final-text classifier cannot, but still needs context. A large paste may come from the author's own offline draft. | Advise authors to retain drafts and notes. Never strip provenance as a "quality" step. |

## 4. Turnitin and iThenticate (dated snapshot)

### 4.1 Disclosed architecture (historical, August 2024) [4] [V]

- AIW-2 classifies writing. AIR-1 identifies paraphrasing within flagged text.
- Both are transformers trained with human, generated, and edited examples.
- Windows span roughly five to ten sentences and advance one sentence at a time. They contribute to weighted sentence scores assessed against tuned thresholds.
- This goes beyond simple perplexity or burstiness measures. Weights and a complete feature dictionary are not disclosed.
- These are historical details. Later updates do not establish that every deployment retains identical internals. [9]

### 4.2 From passage to report [10] [V]

Turnitin's later public explanation describes overlapping sections, segment scores between zero and one, pooling of scores for sentences that appear in several sections, and aggregation into a document result.

Consequences [E]:
- A highlighted sentence may have been evaluated together with neighboring material.
- A highlight does not reveal a single offending word.
- Do not assume every highlighted sentence was independently assessed with certainty.

Keep three objects apart. They are not interchangeable:
1. An internal classifier score for a passage.
2. A decision about whether a text unit passes a classification threshold.
3. The displayed proportion of qualifying text classified as likely AI.

The displayed proportion is not a calibrated probability of misconduct.

### 4.3 What iThenticate includes [3, 5, 6] [V]

- AI detection is an add-on available with iThenticate 2.0. Its AI report uses Turnitin's detection capability and is independent of the similarity score.
- Availability depends on the account and on whether the feature was enabled when the document was submitted.
- Individual credit submissions generate Similarity Reports but do not include AI writing reports or Doc-to-Doc comparisons. Buying a credit-based similarity check does not buy AI detection.

### 4.4 File and language requirements [7] [V]

| Requirement | Documented value |
|---|---|
| Minimum prose | 300 words of long-form prose |
| Maximum length | 30,000 words |
| File size | Less than 100 MB |
| Formats | DOCX, PDF, TXT, RTF |
| Languages listed | English, Spanish, Japanese, Arabic, German, Dutch, Turkish |

- These are AI-report requirements. An upload accepted elsewhere in the product may still be ineligible for AI analysis. The iThenticate guide lists the same seven languages. [3]
- Guidance centers on paragraph-based prose. Code, poetry, scripts, brief bullets, and annotated bibliographies are outside reliable coverage. A low result does not authenticate such material. [8, 9]
- Distinguish short table entries from full prose inside table cells. Historical release notes describe support for the latter. [9]

### 4.5 Reading the displayed result [28] [V]

| Display | Meaning | What it does not mean |
|---|---|---|
| 0% | No qualifying text was identified as likely AI by that analysis | Proven human authorship |
| `*%` | A nonzero result below 20%. The precise percentage and highlights are suppressed. | Exactly zero, or a known precise percentage |
| 20–100% | The displayed share of qualifying text classified as likely AI | The probability that the author cheated |
| Unavailable, error, or ineligible | The analysis produced no usable report | A clean result |

Illustrative reading [I]: if an eligible prose section receives 40%, the system classified roughly that share of its qualifying text. It is not a 40% chance of cheating, and it says nothing about 40% of the equations, references, tables, and other file content.

### 4.6 Report changes that make older guides misleading [9, 29] [V]

| Date | Documented change | Why it matters |
|---|---|---|
| July 2024 | Separate AI generation and AI paraphrasing categories introduced. Low nonzero scores suppressed. | Explains older screenshots |
| August 2025 | Detection expanded to likely use of AI bypasser tools | Older capability summaries may be incomplete |
| 4 August 2026 | A single blue category replaced separate blue and purple categories for the specified Feedback Studio offering | Absence of purple no longer means paraphrasing analysis is absent |
| 14 October 2026 | English detection model updated | Scores from different processing dates may reflect different models |

- The August 2026 notice names Feedback Studio with the Originality add-on. Do not assign that rollout date to every iThenticate interface.
- Current guidance states that paraphrasing and bypasser detection are English-only. [3]
- An AI highlight does not identify the editing service used.
- Previously generated reports do not automatically receive model updates. Preserve the original report date when comparing results.

## 5. Measurable patterns that can distinguish texts

These are feature families used or investigated in text analysis, not a leaked Turnitin specification. [11, 18–21, 32]

| Level | Measurements or observations | Interpretation limit |
|---|---|---|
| Token probability | Likelihood, rank, entropy-related statistics | Depends on the scoring model and domain |
| Vocabulary | Word frequencies, word length, lexical diversity | Specialized human writing also has recurrent vocabulary |
| Word sequences | Repeated combinations and local phrase patterns | Conventional academic expressions are legitimate |
| Grammar | Part-of-speech distributions and modifier patterns | Language and genre change the baseline |
| Syntax | Clause structure, dependency length, construction frequencies | Complexity is neither a quality score nor proof of AI |
| Variation | Changes in measured features across sentences and documents | Editing and templates can reduce variation in human work |
| Semantics | Diversity of subject matter and expression | A narrow assignment naturally limits diversity |
| Learned representations | Neural features combining context at several levels | Usually not reducible to a human-readable word list |

- Zanotto and Aroyehun examined 11 LLMs across eight domains and reported differences in syntax, semantics, and feature variability. The findings are distributional tendencies in the studied samples, not rules for every author. [20] [R]
- Kuznetsov and colleagues used sparse autoencoders to study interpretable internal features for artificial-text detection. This supports the importance of features beyond visible vocabulary and stresses generalization difficulties with unseen text and models. It does not reveal Turnitin's internal features. [32] [R]

### 5.1 Why apparently contradictory claims can both arise [R]

- A study of scientific abstracts found greater lexical variability in LLM outputs but greater syntactic variability in human writing. [19]
- A study of LLM-revised scientific passages reported lower lexical diversity and longer, more complex words. [21]

The tasks, datasets, models, and measures differ. Generating an abstract and revising an existing passage are different operations. Claims such as "AI always has low vocabulary diversity" or "AI always writes longer sentences" exceed the evidence.

## 6. Words, phrases, and rhetorical patterns

### 6.1 No disclosed trigger-word list

No exhaustive list was disclosed in the reviewed official sources. A learned classifier may respond to lexical patterns, but its decision depends on context and feature combinations. "Turnitin flags the word X" requires controlled evidence about that implementation. A blogger's impression does not supply it. It is equally unwarranted to promise that removing a list of words will establish human authorship or produce a particular score. Treat wording as evidence to interpret, not a substitution recipe. [4] [V], [E]

### 6.2 Vocabulary supported by corpus research [18] [R]

Kobak and colleagues studied more than 15 million biomedical abstracts. They found unusual increases in certain stylistic words after widespread LLM adoption and estimated a lower bound on LLM-assisted abstracts at the population level. The study was not designed to prove AI authorship of individual papers.

| Examples documented in that research | What was measured |
|---|---|
| `delves`, `underscores`, `showcasing` | Large increases relative to estimated historical frequencies |
| `potential`, `findings`, `crucial` | Increased usage of already common words |
| Grammatical variants | Related forms need careful counting. They are not independent authorship proofs. |

Nobody can reasonably ban "findings" or "potential." Corpus-level excess usage is different from one author's word choice.

### 6.3 The broader community observation list [26] [C]

The Wikipedia community guide discusses `additionally`, `align`, `boasts`, `bolstered`, `delve`, `enduring`, `enhance`, `fostering`, `garner`, `interplay`, `intricate`, `landscape`, `meticulously`, `pivotal`, `robust`, `showcase`, `tapestry`, `testament`, `underscore`, `valuable`, and `vibrant`. These are descriptive examples, not a commercial detector's published rules.

The practical question is whether a word communicates an accurate, supported meaning. "Robust" can be a precise technical description when the tested perturbations and results are stated. It becomes uninformative praise when the reader cannot tell what robustness means or how it was tested. Every listed word has a contextual entry in `vocabulary-and-phrases.md`.

### 6.4 Rhetorical and structural observations

The source's sixteen constructed rhetorical examples (vague scene-setting, importance without evidence, unspecified mechanism, and others) and its ten structural observations (uniform paragraph shapes, heading excess, markdown residue, and others) are preserved with their review questions and plausible non-AI explanations in `writing-patterns.md`, Sections 3 and 4. The source states that these are writing-quality diagnoses: "A human can write every one of them, and an AI system can generate prose without any of them." [I], [E]

### 6.5 Tortured phrases [33] [R]

Cabanac and colleagues documented "tortured phrases" in scientific publications, including awkward replacements for established terminology. Their work predates the public release of ChatGPT. Suspicious rewriting is not synonymous with use of a recent chatbot.

### 6.6 Citations and factual consistency [E]

Check separately whether a reference exists, whether its fields identify the right work, and whether it supports the associated claim. A real DOI attached to the wrong title is a bibliographic problem. A real paper cited for a result it does not contain is a support problem. Neither is a stylistic issue. Compare numerical claims with tables, captions, methods, and datasets. A polished paragraph can contain unsupported findings, and an awkward one can describe valid research. Keep the classification question and the factual-quality question separate. Procedures: `academic-integrity.md`, Section 3.

## 7. The two Wikipedia pages

### 7.1 Wikipedia: Signs of AI writing [26] [C]

A WikiProject advice page, neither an encyclopedia article nor adopted Wikipedia policy. It covers exaggerated importance, shallow analysis, promotion, vague attribution, formulaic rhetoric, formatting, conversational leftovers, markup, citations, edit summaries, and style changes. It distinguishes historical observations, including heavy em-dash use, and cautions against treating clues as proof.

Assessment: useful for contextual editorial triage, particularly on Wikipedia. It does not document Turnitin's algorithms or validate a scoring rubric. Its Wikipedia-specific observations should not be transferred mechanically to research manuscripts, where headings, conclusions, and references serve different purposes.

### 7.2 Artificial intelligence content detection [27] [C]

An encyclopedia article surveying detection across text and other media, including false positives, false negatives, bias concerns, and resistance to detection. The retrieved page carried an update notice. Several prominent examples and quantitative claims refer to early detector versions.

Assessment: a useful map of the debate and its sources, insufficient as a current product specification. Historical error rates must keep their dates, datasets, and definitions. Numbers from different studies cannot be merged into one universal commercial-detector accuracy rate.

Neither page supplies a proprietary trigger-word list.

## 8. Source quality

| Source | Contribution | Necessary qualification |
|---|---|---|
| Turnitin technical white paper, 2024 [4] | Disclosed architecture and evaluation design | Vendor-authored and historical |
| Current Turnitin and iThenticate guides [3, 7–9, 28–29] | Eligibility, interpretation, display, and updates | Account configuration and rollout can vary |
| Turnitin explanatory blog, 2026 [10] | Readable account of overlapping-segment scoring | Vendor explanation, not independent validation |
| GPTZero support and technical report [12–13] | Corrects outdated perplexity-only explanations | Provider evidence about its own system |
| Weber-Wulff et al., 2023 [22] | Comparative testing of 14 tools, including Turnitin | Cannot establish performance of October 2026 versions |
| Liang et al., 2023 [23] | False positives for non-native English writing in tested detectors | Not a direct audit of today's Turnitin |
| RAID, 2024 [24] | Broad benchmark across models, domains, and transformations | Conclusions depend on evaluated detector versions |
| GenAI shared task, 2025 [30] | Strong performance in a fixed, represented set of domains and models | The operating false-positive rate remains consequential |
| BAID, 2026 [31] | Benchmark designed to assess subgroup-related detector fairness | Not a universal fairness verdict on every product |
| Scientific-language studies [18–21, 34] | Distinguish vocabulary, syntax, and rewriting effects | Group differences do not determine individual authorship |

- Vendor blogs were used only where they explain the vendor's own products. General blogs selling rewriting or "humanizing" services were not treated as evidence about undisclosed detector internals. A commercial interest does not invalidate a claim, but the claim still needs a reproducible method or primary documentation.
- Some Turnitin blog and FAQ links could not be retrieved fully. Their contents were not used to fill gaps.

## 9. Accuracy, false positives, and statistical interpretation

### 9.1 Confusion matrix [standard definitions]

| Actual class | Detector flags AI | Detector does not flag AI |
|---|---|---|
| AI | True positive (TP) | False negative (FN) |
| Human | False positive (FP) | True negative (TN) |

- Recall = TP / (TP + FN): how much AI text was caught.
- False-positive rate (FPR) = FP / (FP + TN): how much human text was wrongly flagged.
- Precision = TP / (TP + FP): how many flagged cases were AI under the evaluation's labels.
- Accuracy = (TP + TN) / (TP + FP + TN + FN).

These have different denominators. Accuracy can hide poor performance when classes are unbalanced. In a dataset that is 99% human, a classifier that always says "human" achieves 99% accuracy and detects none of the AI cases. [I]

### 9.2 Why a 1% false-positive rate is not 99% certainty [I]

Hypothetical: 10,000 documents, 1% AI-generated, a detector with 90% recall and a 1% false-positive rate.

- Of 100 AI documents, it flags 90.
- Of 9,900 human documents, it wrongly flags 99.
- It produces 189 flags in total.
- Of those flags, 90/189, about 47.6%, are correct.

With prevalence π, recall r, and false-positive rate f: P(AI given flag) = rπ / (rπ + f(1 − π)).

This illustrates the base-rate effect. It does not estimate any institution's prevalence or Turnitin's precision. Even this posterior concerns the defined AI class, not misconduct. Permission, disclosure requirements, and the type of assistance need separate information.

### 9.3 Document errors and sentence errors [E]

A document can be correctly flagged while some highlighted sentences are wrong. A document can contain generated sentences without crossing the document threshold. Report performance at the unit being judged. When neighboring context contributes to scoring, inspect highlights as parts of a passage, not as independently established facts.

### 9.4 What the evidence says about reliability

| Finding | Level | Appropriate conclusion | Overreach to avoid |
|---|---|---|---|
| Turnitin reports a document false-positive risk below 1% for the higher-score regime it describes [10] | [V] | A provider claim tied to its testing and operating threshold | A universal probability that a flagged author used AI |
| Weber-Wulff and colleagues tested 14 tools in 2023 and found substantial reliability problems, including missed AI text and poorer performance after transformations [22] | [R] | Those versions and conditions showed limitations | Claiming it measures every October 2026 version |
| RAID covers more than six million generations across 11 models, eight domains, four decoding strategies, and 11 attacks, and found weaknesses under changed generation and unseen models [24] | [R] | Robustness testing is essential | Assuming an in-domain score transfers to unseen conditions |
| Binoculars detected over 90% of generated samples at a 0.01% false-positive rate in its evaluations [16] | [R] | Useful detection is possible under evaluated conditions | Universal reliability across generators and workflows |
| The 2025 GenAI shared task reported over 99% performance on machine-generated examples for several submissions at a 5% false-positive rate, with domains and generators represented in training [30] | [R] | Detection rates and operating error rates must be reported together | Quoting the detection rate without the false-positive rate |
| Sadasivan and colleagues analyze limits to reliable detection as human and generated distributions become harder to distinguish [25] | [R] | Universal detection guarantees are not established | Concluding every detector is useless in every setting |

### 9.5 Language and demographic fairness

- Liang and colleagues found that tested detectors disproportionately misclassified non-native English writing. Test subgroup performance rather than assume an overall metric applies to all writers. [23] [R]
- Turnitin reports no statistically significant difference in false-positive behavior for its tested English-language-learner data. This is a vendor result for a particular evaluation, not proof that bias is impossible. [4] [V]
- BAID constructs a benchmark for demographic and linguistic subgroup assessment. Fairness evaluation should identify the texts and labeling procedures used. Demographic labels alone do not explain a detector's behavior. [31] [R]

### 9.6 Why tools disagree [E]

Tools differ in training data, labels, thresholds, languages, eligible-text rules, and document aggregation. A tool trained to catch any substantial AI rewriting is not solving the same problem as one trained on fully generated essays. A majority vote among detectors is not automatically sound: shared training sources and similar architectures can produce correlated errors. Averaging percentages with different meanings is particularly misleading.

## 10. Mixed authorship and review procedures (pointer)

The workflow table for mixed authorship (human drafting, AI rewriting, translation, coauthorship), the proofreading study [34], the four questions research assessment must keep separate, the procedure for reviewing a flagged document, and the design for evaluating a detector all live in `academic-integrity.md`, Sections 5 to 8.

## 11. Misconceptions about detection and interpretation

This table holds 25 of the 35 rows in guide Section J (rows 1 to 14, 23 to 25, and 27 to 34). The 10 rows about writing practice are in `revision-methods.md`, Section 7.

| # | Misconception | Correction | Practical implication |
|---|---|---|---|
| 1 | High similarity proves AI use | Similarity measures overlap, not generative origin [1–3] | Inspect matches and attribution separately from any AI report |
| 2 | A 70% AI score means a 70% chance of cheating | The percentage concerns classified qualifying text [3] | Identify the denominator. Examine process evidence and policy separately. |
| 3 | Each use of "delve" automatically triggers Turnitin | No universal trigger-word rule is disclosed. Contextual classification is more complex. [4] | Evaluate the word's contribution in context. Keep no blacklist. |
| 4 | Perplexity and burstiness fully explain all detectors | Architectures differ, and providers describe learned models [4, 12, 13] | Avoid universal numerical or stylistic recipes |
| 5 | Perfect grammar indicates AI authorship | Skilled authors and editors produce polished prose | Correct errors. Never add them to simulate authenticity. |
| 6 | Em dashes prove AI use | Punctuation alone does not establish provenance. The related Wikipedia observation is contextual and historical. [26] | Choose punctuation for meaning, readability, and the applicable house style |
| 7 | A low detector score proves no AI assistance | False negatives and unsupported workflows remain possible [22, 24, 25] | A low score is not an authorship certificate |
| 8 | The asterisk means zero | It denotes a suppressed nonzero result below 20% [28] | Preserve the actual report state |
| 9 | Paraphrasing must produce purple highlights | Current reporting combines categories for the documented offering [29] | Interpret colors by product and date |
| 10 | Every iThenticate purchase includes AI analysis | Credit-based submissions exclude AI reports in the reviewed documentation [6] | Confirm what the account and submission include |
| 11 | A 2023 test establishes today's product accuracy | Versions, data, and conditions change [9, 22] | Keep dates and tested conditions with performance claims |
| 12 | A real reference guarantees support | Work identity and claim support are distinct checks | Verify the passage supporting the statement |
| 13 | Agreement among three detectors proves authorship | Errors can be correlated, and scores can mean different things | A majority vote is not conclusive independent evidence |
| 14 | Removing formulaic wording proves human authorship | Quality and provenance are different properties | Revise for substance and document assistance honestly |
| 23 | A high accuracy figure proves a detector is dependable | Class balance, recall, false-positive rate, and operating conditions matter | Report denominators and error tradeoffs |
| 24 | A 1% false-positive rate means a flag is 99% certain | Precision also depends on prevalence and recall | Apply the base-rate illustration (Section 9.2) |
| 25 | A correct document flag validates every highlighted sentence | Sentence and document performance differ | Review passages in context and keep unit-specific uncertainty |
| 27 | Rewriting guarantees a chosen detector outcome | No universal outcome guarantee is established | Set quality and integrity goals, not score targets |
| 28 | A humanizer's internal score is a commercial detector result | The reviewed compression scorer lacks demonstrated calibration, and the public demo uses scripted values [41, 44, 45] | Require reproducible evidence for performance claims |
| 29 | Deterministic rules preserve all scientific meaning | A fixed rule can repeat the same semantic error | Compare negation, scope, causal verbs, and definitions before and after |
| 30 | Invisible characters, watermarks, and provenance are the same thing | Unicode controls, statistical watermarks, C2PA, and classification serve different roles [17, 47–49] | Preserve legitimate characters and provenance. No indiscriminate cleanup. |
| 31 | Paraphrasing removes the need for citation | Attribution concerns ideas and sources as well as exact wording | Cite the source when its contribution is used |
| 32 | "Processed in memory" means "never leaves my browser" | Hosted server memory and client memory differ [51, 52] | Verify the actual processing arrangement |
| 33 | A documented design proves deployed behavior | Intended architecture, inspectable demo code, and an unavailable engine are different things [38–43, 50] | Label design claims and measured observations separately |
| 34 | Missing revision history proves misconduct | Authors draft offline or keep limited history | Evaluate available evidence without treating absence as conclusive |

## 12. What remains unknown [U]

The reviewed public evidence does not provide:

- The full current model weights and architecture for every Turnitin language detector.
- Every training example, generation prompt, preprocessing rule, or aggregation parameter.
- A complete, stable list of words that cause flags.
- An exact explanation for every individual highlight.
- Independent October 2026 performance estimates across all academic fields and mixed writing workflows.
- A universal mapping from an AI percentage to the probability of prohibited conduct.
- A guarantee that future models, extensive editing, or unfamiliar languages and genres will behave like the tested cases.

Detection can supply useful statistical evidence under defined conditions. Its value depends on those conditions and on how the result is used. For an individual manuscript, source verification, technical review, and credible process evidence remain necessary alongside any detector output.

## 13. Turnitout-Humanizer repository review

### 13.1 Scope and principal finding

- Repository: AhmadHassan-BTed/Turnitout-Humanizer. Snapshot `7997aa186e0d6b1c5d45dfcff65a4f38146c0c58`, committed 22 October 2026. Method: read-only inspection of files, public documentation, commit history, and website JavaScript. No manuscript was uploaded and no commercial detector was run. [38]
- The project describes a rule-based rewriting application with document parsing, citation generation, and a local scorer. The inspected public snapshot holds documentation and website assets, not the advertised Python engine. It lacks the referenced `src/turnitout/` implementation, `rules/` JSON files, and Python test suite. None of the 42 commits reachable from main tracked Python or JSON implementation files. [38–40] [O]
- This concerns the inspected public history, not any private repository or deployed server. The engine description is documented design [P]. The JavaScript findings are verified observations [O]. The public material does not support a full audit of the hosted application's transformations, preservation guarantees, or deletion behavior.

### 13.2 The advertised engine (documented design) [39, 40] [P]

| Component | Documented purpose | Verification boundary |
|---|---|---|
| Protected-region parser | Temporarily preserve LaTeX commands, equations, and formatting-sensitive content | Parser source and regression tests are unavailable |
| Transformation pipeline | Apply phrase substitutions, grammatical restructuring, and discourse changes | Architecture descriptions state intended operations, not correctness |
| External rule assets | Keep language mappings and academic taxonomies in JSON | The referenced rule files are absent from the snapshot |
| Document writer | Preserve DOCX structures while updating prose | Needs real before and after files and structural tests |
| Citation module | Select citation locations and export BibTeX, LaTeX, and JSON | Bibliographic authenticity and claim support are separate checks |
| ZipPy checker | Estimate text characteristics through compression | No demonstrated calibration to Turnitin or iThenticate scores |

- The architecture rules separate Python logic from JSON vocabulary assets and describe metadata prompts for future contributors, filtered out when rules load. Such development instructions do not imply that an LLM is called during processing. [40]
- Version inconsistencies: the README describes 15 stages, the architecture document 16, and an implementation-planning document a proposed 17-step flow. Only an executable implementation could settle the order. [38, 39, 43]

### 13.3 What the public website JavaScript does [41] [O]

| Code location | Observed behavior | Meaning |
|---|---|---|
| Replacement array and notebook click handler | Applies regular-expression phrase replacements to sample text | A small demonstrator, not the unavailable engine |
| `resetToRaw` and sample handlers | Use preset initial values of 96 or 98 | Initial scores are not inferred from a commercial detector |
| Input handler | Sets the meter to 94 in a specified state transition | The number is assigned by UI logic |
| Transformation timeout | Sets the meter to 4 after 350 milliseconds | The displayed reduction is scripted, not measured |
| Desk dial click handler | Sets its display to 0 and changes the status label | A visual state change, not a detection result |

- The relevant handlers contain no Turnitin or iThenticate inference call. This is limited to the public demonstration.
- `docs/cluster-balancer.js` selects among eight hosted Streamlit destinations by random weighted selection: seven mirrors at weight 13 each, the main destination at weight 9. It respects explicitly selected mirror links. It does not measure server load or probe health, so "load balancing" here means probabilistic traffic distribution. [42] [O]

### 13.4 Why ZipPy is not a Turnitin verification [44, 45]

- The changelog says ZipPy uses Python's `zlib` and `lzma` compression to estimate predictability. The scoring implementation is unavailable, so its formula, normalization, and thresholds cannot be verified. [44] [P]
- A compressor captures repeated byte patterns. A compression-derived score is not automatically language-model perplexity, and neither is a probability of AI authorship. [45] [V]
- Counterexamples [I]: repeating a paragraph many times creates compressible material whoever wrote it. A list of random identifiers is hard to compress without being meaningful prose.
- A low internal score cannot certify a low score from an independent detector. Testing that relationship needs paired results on a representative held-out dataset with dates, detector versions, and uncertainty estimates. No such validation was found.

### 13.5 Similarity and watermark claims [38, 46–49]

- The repository's similarity analysis proposes lexical fingerprints, syntax-tree comparisons, and semantic embeddings as a three-layer model of commercial similarity systems, with numerical thresholds and assumptions about citation markers. These are the project's assumptions, not reverse-engineered facts. [46] [P]
- Changing wording can reduce exact overlap with an input. That does not establish a predictable reduction against a large proprietary database, and it does not settle attribution. A paraphrase can still need citation.
- The README groups invisible characters, statistical watermarks, and C2PA provenance together and claims broad removal guarantees. These are distinct mechanisms. [38]

| Mechanism | What primary documentation establishes | Assessment of the repository's claim |
|---|---|---|
| Statistical text watermark | SynthID modifies token-generation probabilities and can withstand some editing [47] [V] | Altering phrases does not by itself demonstrate universal watermark removal |
| Unicode format controls | Joiners and non-joiners have legitimate shaping and orthographic functions [48] [V] | Invisible characters are not inherently evidence of AI tracking. Indiscriminate removal can change valid text. |
| C2PA Content Credentials | Signed provenance assertions can be bound to an asset, including through durable bindings [49] [V] | Removing embedded metadata is not removing every provenance link or changing linguistic classification |
| AI text classification | The detector evaluates statistical features of writing | A file without metadata can still be classified as likely AI |

The reviewed material does not substantiate universal deployment of the claimed hidden tracking layers across every named provider. A reference to a regulation is not evidence that all products implement the same mechanism. The source makes no legal determination.

### 13.6 Preservation claims [50]

Deterministic execution does not guarantee factual correctness. A fixed rule can make the same mistake every time, for example changing a cautious verb to a stronger one without altering any number. The technical-decision document describes protecting mathematical zones, format-aware Word processing, and discipline-specific citation taxonomies. These are plausible strategies that need implementation tests before becoming guarantees. The verification needs (meaning, references, LaTeX, DOCX, code) are listed in `academic-integrity.md`, Section 2. The available material justifies neither "it always corrupts documents" nor "it always preserves them."

### 13.7 Privacy and the hosted application [51–53]

- The privacy policy says manuscripts are processed in memory without permanent storage and describes GitHub-based verification and short-lived session cookies. These are provider commitments, not audit results. [51] [P]
- Standard Streamlit applications execute Python on the server. The browser is the client. A hosted Streamlit interface does not establish that uploads stay on the user's device. Local deployment is a different arrangement. [52] [V]
- Hosting logs, runtime retention, and the code deployed at each mirror could not be verified. The project's terms provide the service without warranties, which should be weighed against stronger promotional guarantees. [53] [P]

### 13.8 Overall assessment

- **Supported:** a working phrase-replacement demonstration and a weighted link router in the public site, plus documentation of a broader rule-driven design.
- **Not established:** reliable evasion of current Turnitin or iThenticate detection, universal watermark removal, preservation of every scientific claim and document structure, authentic generated references, or independently verified server-side privacy.
- **Decisive limitation:** reproducibility. A documented workflow and an animated percentage reduction do not replace executable source, preservation tests, and independently measured detector outcomes.

## 14. Summary of the evidence boundary

1. No publicly verified, exhaustive Turnitin or iThenticate trigger-word dictionary exists. Individual words are not automatic flags.
2. An AI percentage is not a probability that an author cheated. It concerns the portion of qualifying text the system classified. [3]
3. Patterns can be informative in aggregate and inconclusive for one document. Vocabulary research and detector benchmarking answer different questions. [18–23]
4. Performance depends on language, genre, length, generation model, editing history, test design, and decision threshold. [16, 20–25]
5. Documentation dates matter. Current language support and report presentation differ from many older explanations. [7–10]
6. Proprietary weights, undisclosed training data, and future features are unknown. State the boundary rather than fill it.

## 15. What these findings mean for writing review

Each item translates a finding into an editing rule. Labels show where the rule comes from.

1. **Never edit toward a feature target.** Do not change text to raise perplexity, add "burstiness," vary sentence lengths by quota, increase lexical diversity, or alter punctuation frequency. The measures depend on the scoring model, their published relationships to authorship are task-specific, and the source supports no safe target. (Sections 3, 5.1) [R], [E]
2. **Judge a word by its contribution, never by list membership.** Corpus-level excess vocabulary [18] and community lists [26] locate words worth a second look. They do not make a word wrong. (Section 6) Procedure: `vocabulary-and-phrases.md`.
3. **Read flagged passages for substance.** A highlight reflects a passage scored with its neighbors. When a user shows highlighted text, review its claims, specificity, and evidence. No single word explains it. (Section 4.2)
4. **Name the writing problem, not a suspected origin.** Write "generic opening (B01)" or "unsupported causal claim (B05)," never "this sounds like AI." Editorial features are not validated authorship tests, and non-native English writers face documented false-positive risk in tested detectors [23]. (Sections 6.4, 9.5)
5. **Quality and provenance are separate.** A better revision does not certify human authorship. A flag does not prove misconduct. A low score is not a certificate. (Sections 9, 11)
6. **Keep four questions separate:** Is the research credible? Is borrowed material attributed? Was assistance used, and what kind? Did that use comply with the applicable policy? A detector result answers none of them completely. (`academic-integrity.md`, Section 6)
7. **Match the evidence to the property claimed.** Source availability, code inspection, preservation tests, measured outcomes, and processing arrangements answer different questions. A displayed score reduction answers none of them. (Section 13)
8. **Recheck dated product facts** before a user relies on them. (Section 4)
9. **Preserve legitimate characters and provenance.** Do not strip Unicode format controls, metadata, or drafts as a quality step. (Section 13.5, `academic-integrity.md` Section 4)
10. **Promise no detector outcome.** No source establishes that any rewrite produces a particular score in any detector. (Sections 6.1, 12)
