# Quality Assurance and Deliverables (Phase 12)

The task is not complete when citations are in. It is complete when these audits pass, or their failures are documented, and `summary.md` reports both.

## 1. Run the mechanical checks

```
python scripts/audit_citations.py <main.tex> --compare literature/baseline_citations.json
python scripts/verify_refs.py <active.bib> --keys <every newly added key> --strict \
    --out literature/raw/verification/final_verify.csv --raw-dir literature/raw/verification
python scripts/check_ledger.py --lit literature --tex <main.tex> --baseline literature/baseline_citations.json
```

Then compile the manuscript with its own build and read the log. Copy the exit status and the error and warning counts of each command into `qa_report.md`. If a command could not run, say so and why.

## 2. Judgment audits

Work through these and record each result in `qa_report.md`. Each line is pass, fail with location, or not checked with reason.

**Reference audit**
- [ ] Every new citation is VERIFIED or VERIFIED-QUALIFIED in the ledger
- [ ] Every DOI, title, author list, and year matches its authoritative record
- [ ] No entry was written from memory or inferred without a retrieved record
- [ ] Duplicates and versions (preprint vs. published, conference vs. journal) resolved
- [ ] UNRESOLVED and REJECTED sources are absent from the bibliography
- [ ] Retractions, corrections, and expressions of concern handled

**Evidence audit**
- [ ] Each added factual claim has a source whose access level permits it
- [ ] Each reported number matches the source, with its conditions
- [ ] Each citation supports the sentence where it sits (spot-check every `result`, `comparison`, `gap`, and `novelty` claim in the citation map)
- [ ] No finding is attributed to the wrong authors
- [ ] Contradictory evidence and qualifications survive in the text
- [ ] No abstract-only source is presented as read in full
- [ ] No unsupported gap or novelty wording was added

**Citation and bibliography audit**
- [ ] `audit_citations.py` reports no errors
- [ ] Citation style matches the manuscript's existing style
- [ ] Keys unique, no unescaped special characters, no padding clusters

**Manuscript integrity audit**
- [ ] Contributions, methods, and results unchanged except documented corrections
- [ ] The related work argues toward the gap, and the gap follows from the matrix
- [ ] The discussion does not overstate what prior work implies
- [ ] Cross-references, labels, figures, and tables intact
- [ ] Manuscript compiles or renders (state the command and result)

## 3. Deliverables

Report each one in `summary.md` with its path. If one does not apply, say why. Do not create empty files.

| # | Deliverable | Where |
|---|---|---|
| 1 | Revised manuscript | Its own path, named as the final version. Originals in `literature/originals/` |
| 2 | Literature synthesis | `literature/review_body.md` or the revised sections |
| 3 | Verified bibliography | The active bib, plus `literature/references_lit.bib` staging |
| 4 | Source ledger | `literature/source_ledger.csv` |
| 5 | Evidence records | `literature/extraction_sheet.csv`, `literature/raw/source_records/` |
| 6 | Gap matrix | `literature/gap_matrix.csv`, `literature/gaps.md`, `literature/gap_matrix_out/tables.tex` |
| 7 | Citation map | `literature/citation_map.csv` |
| 8 | Search and verification logs | `literature/search_log.csv`, `literature/raw/verification/` |
| 9 | QA report | `literature/qa_report.md` |
| 10 | Change summary | `literature/summary.md` |

## 4. summary.md contract

Sections, in this order:

1. **Scope.** Manuscript, genre, venue, date range of the work.
2. **Searches.** Platforms actually used, number of executed queries, snowballing done, platforms that failed or were unreachable.
3. **Sources.** Counts from the ledger: screened, included, excluded (top reasons), cited. Counts by status and access level.
4. **Themes and evidence.** The main themes, the strongest evidence, and the main disagreements in the field.
5. **Gaps.** Each gap with its claim strength and the gap record it rests on.
6. **Existing-reference problems.** Wrong DOIs, fabricated or mismatched entries, retractions, version mismatches found in the original bib, and what was done about each.
7. **Manuscript changes.** Section by section, with old and new wording for every changed claim.
8. **Files.** Created and modified, with paths.
9. **QA results.** Command results and checklist outcome.
10. **Open items for the author.** Unresolved sources, inaccessible full texts, claims that need the author's decision.
