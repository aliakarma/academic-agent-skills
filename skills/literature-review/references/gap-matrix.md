# Gap Matrix, Gap Records, and Novelty Table (Phases 5 and 6)

A research gap is a conclusion drawn from comparing what the literature does. It is never inferred from the manuscript's own citation list or from a search that returned nothing.

## 1. Choose the dimensions

Derive them from the manuscript's research questions and contributions. Use only dimensions that separate the studies. Candidates:

problem formulation, theoretical basis, method or architecture, data and setting, evaluation design, metrics, reported outcomes, reproducibility (code, data), assumptions, deployment constraints, scalability or generalization, treatment of uncertainty, human involvement, governance or accountability, and the specific aspect the manuscript claims to add.

Five to eight dimensions is usually readable. More belongs in a supplementary table.

## 2. Fill the matrix

`literature/gap_matrix.csv`: first column `source_id`, one column per dimension, and a final row `THIS_WORK` for the manuscript. Cell values: `yes`, `partial`, `no`, `n.r.` (not reported), or short text.

Every cell traces to an extraction_sheet row. `n.r.` and `no` differ: `no` means the source shows it does not do this, `n.r.` means the source does not say. Do not fill `no` for things you did not check.

Include the closest competitors and the strongest counter-examples, not only the studies that make the manuscript look new. Render with:

```
python "$S/gap_table.py" literature/gap_matrix.csv --out literature/gap_matrix_out/tables.tex
```

## 3. Write one record per gap in `gaps.md`

Use the A to K record in `review-template.md` Sec. 9 and write it straight into `literature_review.md`. `gaps.md` is optional scratch space. Each record ends with an **Examined** line listing the source_ids and the search_ids (including the `counterevidence G<n>` query) that established it.

Fill the fields from evidence, in this order of work:

1. **C and D first.** Run the counterevidence sweep before writing A. What existing work already does decides how narrow A must be.
2. **A** is the residue after D: one testable sentence naming the setting and the missing capability. "No trust layer for agentic water twins" is too broad if agent-security frameworks exist elsewhere. "No reported evaluation of compromised-agent messages against a hydraulic action guard in a water twin" is testable.
3. **B** cites what the supporting studies did (their methods, evaluations, stated limits), not only that they exist.
4. **E to G** name what remains, why it matters, and how one might investigate it, without designing the solution.
5. **H to K** come last, from the table below.

## 3a. Category, confidence, and novelty risk

| Evidence you hold | Category | H. Confidence | I. Novelty risk |
|---|---|---|---|
| Two or more FULLTEXT or ABSTRACT sources show the problem, counterevidence sweep in this and neighboring vocabularies found no adequate solution | Established research gap | Strongly supported | Low or Medium |
| Solutions exist in some settings, and sources show where they stop working | Context-dependent gap | Moderately or Strongly supported | Medium |
| A recent development (last 24 months) creates the problem, and a dated search of recent work found little | Emerging research gap | Moderately supported or Tentative | Medium or High |
| Suggestive evidence, but the search was narrow, access was abstract-only, or the field moves too fast to be sure | Potential or tentative gap | Tentative | High |
| The counterevidence sweep found work that solves it within the claimed scope, or support is only the manuscript's own say-so | Unsupported or resolved gap | Unsupported | High |

Downgrade one step when the main supporting sources are preprints, METADATA-only, or the manuscript's own citations described by the manuscript. A gap resting on one source is never "Established".

The research-auditor skill's `references/gap-verification.md` has a five-way verdict and gap taxonomy. Use it when a gap's status is contested.

## 4. Calibrate the wording

Choose the strongest wording the evidence earns, and no stronger.

| Evidence | Wording you may use |
|---|---|
| Systematic search with documented protocol, no study found | "No study identified in our systematic search of <databases, dates> addresses ..." |
| Broad multi-family search plus snowballing, no study found | "We found no study that ...", "The reviewed approaches do not ..." |
| Some studies touch it partially | "Few identified studies examine ...", "Existing work addresses X but not Y (refs)" |
| Studies exist but are limited in a stated way | "Evidence is limited to <setting> (refs)" |
| Studies address it | Not a gap. Reframe around what the manuscript adds beyond them |

Never write "first", "only", "no prior work", or "most comprehensive" without the top row's evidence. "To the best of our knowledge" does not excuse a missed paper. Search before writing it.

## 5. Novelty claims in the manuscript

Each claimed contribution and each novelty phrase from Phase 1 (M-ids) gets one row in the Sec. 11 novelty table of `literature_review.md`:

| Column | How to fill it |
|---|---|
| Manuscript claim | M-id plus the claim, quoted or closely paraphrased, with its location |
| Closest related work | The 1 to 3 nearest works by what they do, found by the closest-competitor sweep, not only the manuscript's citations |
| Verified similarities | What those works demonstrably share with the claim, at the access level you hold |
| Potentially distinctive aspect | What remains different, worded as a hypothesis |
| Evidence required | The comparison, experiment, or argument that would establish the difference |
| Current assessment | One of: Supported, Supported with narrower wording, Overstated, Contradicted, Not assessable. Then the novelty type (conceptual, methodological, empirical, application-specific) |

Do not edit the manuscript in this phase. Suggested replacement wording goes into Sec. 13.1 of the review.
