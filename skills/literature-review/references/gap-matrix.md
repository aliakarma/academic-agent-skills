# Gap Matrix and Gap Records (Phase 7)

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
python scripts/gap_table.py literature/gap_matrix.csv --out literature/gap_matrix_out/tables.tex
```

## 3. Write one record per gap in `gaps.md`

```markdown
## G2: <precise gap statement>

1. Gap: <one sentence, testable>
2. Examined: <source_ids of every paper used to establish it, plus the search_ids>
3. What existing work does: <with source_ids>
4. What it does not do: <with source_ids>
5. Competing approaches: <source_ids>
6. Contrary or partial evidence: <work that addresses part of the gap>
7. Why it matters: <scientific or practical consequence, with evidence>
8. How the manuscript addresses it: <section reference>
9. What the manuscript leaves open: <honest residue>
Claim strength: <level from the ladder below>
```

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

For each novelty phrase found in Phase 1, record in `gaps.md`: phrase, location, the gap record that tests it, verdict (supported, overstated, contradicted), and the replacement wording when overstated. Change the manuscript text only in Phase 10, and list every change in the summary.
