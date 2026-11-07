# Source coverage

A maintenance record. It maps every section of the two source documents to its location in this skill, lists where the sources differ and how each difference was resolved, and gives the checks to rerun after editing the skill. Normal editing tasks do not need this file.

## 1. Sources

| Source | File | Size and checksum at build | Nature |
|---|---|---|---|
| A | `AI Detection.md` (*How AI Writing Detection Works*) | 71,419 bytes, 722 lines, SHA-256 `ad20ea254bc63f79b95c29c40f3d7a3cc68d32856b0f6dfc8160c0e1836409b8` | Documentary review, research snapshot 24 October 2026. 15 sections, 53 references. Prepared with AI assistance and web research. No detector test performed. |
| B | `natural_academic_writing_guide.md` (*Clear, Precise, Author-Driven Academic Writing*) | 146,935 bytes, 1,402 lines, SHA-256 `972cc88ebe98c6911f7db718d7fac20adbc00800b34b290339cd51ab68e4da66` | Editorial guide synthesized from Source A. Sections A to K and the same 53 references. Prepared with AI assistance. No new detector experiment or literature search. |

Both files were located in a local folder on the author's machine at build time (24 October 2026). The skill was built so that it does not need them at run time. They were read in full and not modified.

Neither source independently re-verified its external URLs for this skill, and this skill did not revisit them. The references are reproduced for traceability.

## 2. Coverage map: Source A

| Source A section | Content | Location in this skill |
|---|---|---|
| Executive summary | Five defensible conclusions, scope boundary | `detection-principles.md` 14, `SKILL.md` limits |
| 1 Terms and evidence levels | 10 terms, 4 evidence labels | `detection-principles.md` 0, 1 |
| 2 Similarity versus AI detection | Comparison table, four combinations, exclusion settings, no adding percentages | `detection-principles.md` 2 |
| 3.1 Pipeline | Seven stages, context and PDF order | `detection-principles.md` 3 |
| 3.2 Perplexity | Formula, predictability limits, GLTR | `detection-principles.md` 3, 15 |
| 3.3 Burstiness | Loose term, GPTZero migration 2023 | `detection-principles.md` 3, 15 |
| 3.4 Supervised classifiers | Training choices, held-out evaluation, Turnitin and GPTZero | `detection-principles.md` 3 |
| 3.5 Stylometric classifiers | Feature distributions, random forests | `detection-principles.md` 3 |
| 3.6 Zero-shot detection | DetectGPT, Fast-DetectGPT, Binoculars | `detection-principles.md` 3 |
| 3.7 Watermarking | Green-list method, absence not proof | `detection-principles.md` 3, 13.5 |
| 3.8 Retrieval and provenance | Record coverage, drafts and histories | `detection-principles.md` 3, `academic-integrity.md` 4, 7 |
| 4.1 to 4.6 Turnitin and iThenticate | AIW-2, AIR-1, windows, three objects, iThenticate add-on and credits, file and language requirements, display table, change history | `detection-principles.md` 4 |
| 5.1 to 5.2 Measurable patterns | Eight levels, Zanotto, Kuznetsov, apparent contradictions | `detection-principles.md` 5, `vocabulary-and-phrases.md` 8 |
| 6.1 Trigger-word question | No disclosed list | `detection-principles.md` 6.1, `vocabulary-and-phrases.md` 1 |
| 6.2 Corpus vocabulary | Kobak study, six words | `detection-principles.md` 6.2, `vocabulary-and-phrases.md` 1, 3 |
| 6.3 Wikipedia vocabulary | 21 words | `detection-principles.md` 6.3, `vocabulary-and-phrases.md` 3 |
| 6.4 Sixteen constructed rhetorical examples | Pattern, wording, review question | `writing-patterns.md` 3 (all 16 rows), mapped to B01 to B16 |
| 6.5 Ten structural observations | Inspect column, plausible non-AI explanation | `writing-patterns.md` 4 (all 10 rows) |
| 6.5 Tortured phrases | Cabanac study | `detection-principles.md` 6.5, B25 |
| 6.6 Citations and factual consistency | Existence, identity, support | `academic-integrity.md` 3, `detection-principles.md` 6.6 |
| 7 Wikipedia pages | Advice page and encyclopedia assessments | `detection-principles.md` 7, `writing-patterns.md` 5 |
| 8 Additional sources | Ten-row quality table, blog policy, unretrieved links | `detection-principles.md` 8 |
| 9 Accuracy | Confusion matrix, base rates, sentence versus document, reliability evidence, fairness, disagreement | `detection-principles.md` 9 |
| 10 Mixed authorship | Seven workflows, proofreading study, academic repetition, four questions | `academic-integrity.md` 5, 6 |
| 11.1 Flagged document review | Nine steps | `academic-integrity.md` 7 |
| 11.2 Detector evaluation | Nine design points | `academic-integrity.md` 8 |
| 11.3 Quality versus detection | Improve substance, disclose, no inserted errors | `academic-integrity.md` 9, 12 |
| 12 Misconceptions | 14 rows | `detection-principles.md` 11 (rows 1 to 14) |
| 13 Unknowns | Seven items | `detection-principles.md` 12 |
| 14.1 to 14.8 Turnitout-Humanizer review | Scope, documented design, JavaScript observations, router, ZipPy, watermark table, preservation, privacy, overall assessment | `detection-principles.md` 13, `academic-integrity.md` 2.2, 10, B35, I12 |
| 15 References | 53 entries | `bibliography.md` |

## 3. Coverage map: Source B

| Source B section | Content | Location in this skill |
|---|---|---|
| Front matter, evidence labels, how to use | Four labels, constructed-illustration rule | `detection-principles.md` 0, `writing-patterns.md` 1, `examples/before-and-after.md` status |
| Source coverage inventory | Guide's own map of Source A | Superseded by Sections 2 and 3 of this file |
| A1 to A10 | Ten principles | `revision-methods.md` 2, compressed in `SKILL.md` |
| B01 to B36 | 36 pattern records, all fields | `writing-patterns.md` 6, index in 2 |
| C1 | Vocabulary research and decision sequence | `vocabulary-and-phrases.md` 1, 2 |
| C2 | 24-word inventory | `vocabulary-and-phrases.md` 3 (all 24 rows) |
| C3 | 12 phrase families | `vocabulary-and-phrases.md` 4 (all 12 rows) |
| C4 | No numerical style goals | `vocabulary-and-phrases.md` 8 |
| Phrases only inside examples (D, E, I, B) | Further evaluative wording | `vocabulary-and-phrases.md` 5 (compiled for this skill) |
| D1 to D10 | Sentence methods | `revision-methods.md` 3 |
| E1 to E9 | Paragraph and document methods | `revision-methods.md` 4 |
| F Passes 1 to 10, status table | Ten-pass workflow | `quality-control.md` 2, 4.2 |
| G1 | Preservation table (11 domains), invariants | `academic-integrity.md` 1 |
| G2, G3 | Wording versus scientific decisions, automated rewriting | `academic-integrity.md` 2 |
| G4 | Legitimate characters and provenance | `academic-integrity.md` 4 |
| G5 | Processing arrangements | `academic-integrity.md` 10 |
| H1 to H8 | Detection, similarity, provenance, interpretation | `detection-principles.md` 2 to 13, `academic-integrity.md` 7 |
| I1 to I12 | Twelve worked cases | `examples/before-and-after.md` 1 |
| J | 35 misconception rows | `detection-principles.md` 11 (25 rows) and `revision-methods.md` 7 (10 rows) |
| K | Final submission checklist, ten groups | `quality-control.md` 5 (all items) |
| References | Same 53 entries | `bibliography.md` |

## 4. Where the sources differ, and how this skill resolved it

| # | Difference | Resolution |
|---|---|---|
| 1 | Source B calls its source `report.md`. The file is now `AI Detection.md`. | Same document: the size (71,419 bytes) matches. Treated as one source. |
| 2 | The sources use different four-label evidence schemes. Source A's Section 14 also separates documented design from verified code observations. | Unified into eight labels (`detection-principles.md` 0) without merging levels: vendor, project, verified observation, research, community, editorial, illustrative, unknown. |
| 3 | Source A's 16 rhetorical examples are bare specimens. Source B's pattern records give local facts and revisions bounded by those facts. | Both kept. Revisions follow Source B's stricter rule: use only supplied facts, and label withdrawals as substantive. |
| 4 | Source A is about what detectors do. Source B is about editorial decisions and restates Source A in Section H. | Source A's wording governs detection facts. Source B's wording governs editing decisions. Section H material is merged into `detection-principles.md` without strengthening any claim. |
| 5 | Source B adds recommendations Source A does not make (for example B29 to B34, the issue-status table, the checklist). | Kept as editorial recommendations [E], never presented as empirical findings. |
| 6 | Source B Section J has 35 rows. Its first 14 restate Source A Section 12. | All 35 kept once, split by topic between two files with row numbers so the count can be audited. |
| 7 | This skill adds content of its own: the priority column (`writing-patterns.md` 2), the rules in `detection-principles.md` 15, the compiled phrase table, the claim-strength table, the intervention levels, the drafting rules, the boundaries table, the fidelity script, and the valid and invalid decision table. | Each is labeled as this skill's translation or construction, not a source finding. |
| 8 | The user's house-style rules (saved memory `writing-style-rules`: no em dashes, no semicolons, a list of words to avoid, prefer active voice, vary sentence length) versus the sources, which say punctuation and vocabulary prove nothing about provenance and warn against blanket word bans, voice rules, and length quotas. | House style is applied as a style requirement with a meaning-preservation override (`vocabulary-and-phrases.md` 7, `revision-methods.md` 6). It is never presented as a detection tactic. Semicolons in source examples and annotations were changed to full stops or colons. |
| 9 | The installed `humanize-latex` skill describes "low burstiness" and uniform rhythm as telltale AI weaknesses. Source A Section 3.3 and Section J row 4 say burstiness is loosely defined and not a universal test. | Not modified (outside this skill's scope). Flagged to the user at build time. |
| 10 | The installed `universal-manuscript-polish` skill governs research-manuscript runs under the user's global instructions. | This skill defers to it for whole manuscripts and supplies the pattern, vocabulary, and integrity references within that run. |
| 11 | The research snapshot date equals the build date. | Product facts are labeled as dated, with an instruction to recheck before relying on them. |

## 5. Maintenance

After any edit to this skill:

1. Keep evidence labels on every finding you add. Do not promote [V], [P], or [C] material to [R].
2. Keep reference numbers aligned with `bibliography.md`.
3. Keep both house-style properties: no em dashes and no semicolons in prose. Check with:

   ```
   grep -rn $'\u2014' <text-humanizer skill folder>
   grep -rn ';' <text-humanizer skill folder> --include=*.md
   ```

4. Check that every relative path in `SKILL.md` resolves.
5. Rerun the cases in `tests/regression-cases.md` and compare against their pass criteria. Run `scripts/fidelity_check.py` on each case pair.
6. If the source documents are updated, compare their new checksums with Section 1 and update the affected sections listed in Sections 2 and 3.
