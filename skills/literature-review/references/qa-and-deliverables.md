# Quality Control and Deliverables (Phases 8 and 9)

The task is complete when `literature_review.md` passes the mechanical checks, the judgment audit is recorded, and the completion report states only counts the files support.

## 1. Mechanical checks

```
python "$S/check_review.py" literature_review.md --ledger literature/source_ledger.csv --search-log literature/search_log.csv
python "$S/verify_refs.py" literature/references_lit.bib --strict \
    --out literature/raw/verification/final_verify.csv --raw-dir literature/raw/verification
python "$S/audit_citations.py" <main.tex> --compare literature/baseline_citations.json
```

The last command proves the manuscript's citations did not change during the review. Copy each command's exit status and its error and warning counts into `literature/qa_report.md`. If a command could not run, say so and why.

Every `check_review.py` ERROR is fixed before reporting. Every WARN is fixed or listed in `qa_report.md` with the reason it stands (for example, W05 on a sentence that says the review is not a PRISMA review).

## 2. Judgment audit (brief section 10)

Record each line as pass, fail with location, or not checked with reason.

**Scientific accuracy**
- [ ] Terminology and technical explanations match the sources
- [ ] Every reported number matches its source, with its conditions, at an access level that permits it
- [ ] Contributions and limitations of each study are attributed to the right authors, and reviewer-observed limitations are labeled as such
- [ ] Disagreements and contradicting findings are stated
- [ ] Speculation is labeled

**Research-gap validity**
- [ ] Each gap has a logged counterevidence search
- [ ] Each gap's category and confidence follow the gap-matrix.md section 3a table
- [ ] Gap statements are narrow enough to test
- [ ] Resolved and tentative gaps are not presented as established
- [ ] If no gap is strongly supported, the review says so in Sec. 2 and Sec. 9

**Reference integrity**
- [ ] Every Sec. 15 entry is VERIFIED or VERIFIED-QUALIFIED in the ledger, with raw verification evidence on disk
- [ ] No entry was written from memory
- [ ] Preprint versus published versions resolved, retractions and corrections checked
- [ ] Every unverifiable source is in Sec. 16 with the reason
- [ ] The manuscript's own bib was machine-checked and its problems reported

**Coverage and reproducibility**
- [ ] Foundational work and the last 24 to 36 months covered per core concept
- [ ] Closest-competitor, neighboring-field, and counterevidence sweeps ran
- [ ] Sec. 17 or `search_log.csv` lets another researcher rerun the main searches
- [ ] Databases not searched are named as not searched
- [ ] Closed-access versus open-access venue split is within 40-60%, or the imbalance and its reason are reported

**Deliverable integrity**
- [ ] `literature_review.md` sits beside the manuscript, and an earlier version (if any) is preserved
- [ ] The manuscript, bib, code, and data are unchanged (`audit_citations.py --compare` and file timestamps)
- [ ] The document is a review with evidence, not an outline

## 3. Deliverables

| # | Deliverable | Where |
|---|---|---|
| 1 | The review | `<project>/literature_review.md` |
| 2 | Research profile and claim list | `literature/research_profile.md` |
| 3 | Search strategy and log | `literature/search_strategy.md`, `literature/search_log.csv` |
| 4 | Source ledger | `literature/source_ledger.csv` |
| 5 | Evidence records | `literature/extraction_sheet.csv`, `literature/raw/source_records/` |
| 6 | Staging bib of verified sources | `literature/references_lit.bib` (for a later integration stage) |
| 7 | Verification evidence | `literature/raw/verification/` |
| 8 | QA report | `literature/qa_report.md` |

Do not create empty files to tick a row. If a deliverable does not apply, say why in `qa_report.md`.

## 4. Completion report (in chat)

Short, in this order, with numbers copied from the `check_review.py` SUMMARY line and the ledger:

1. Path of `literature_review.md`
2. Themes covered
3. Sources: included and cited, VERIFIED, VERIFIED-QUALIFIED, unverified (Sec. 16), by access level (FULLTEXT, ABSTRACT, METADATA), and the closed-access versus open-access venue split with percentages
4. Gaps: count by category and by confidence
5. The novelty verdict in one sentence
6. Major limitations (tools that failed, paywalls, scope cuts)
7. Open verification issues, and manuscript problems the author must decide on
