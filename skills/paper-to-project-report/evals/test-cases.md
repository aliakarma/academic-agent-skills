# paper-to-project-report test cases

Status values: PASS, FAIL, NOT RUN. Log each real run here with the date, paper and checker result.

Evaluation Cases A to D are private research projects that the checker was run against. Their files are not distributed, and the labels are neutral on purpose. Only the checker outcomes are recorded.

## Checker (scripts/check_report.py)

| ID | Case | Status | Evidence |
|---|---|---|---|
| CK-01 | `--selftest`: clean fixture has zero findings, 12 seeded faults detected | PASS | 2026-11-07, `selftest: 13/13 passed`, mypy clean |
| CK-02 | Evaluation Case A report (first run of the skill, follows the contract) with `--aux main.aux` | PASS | 2026-11-07, 0 errors, 1 true warning (23 METRIC IDs defined only in the handoff), no false P08 hits on Roman-numeral tables |
| CK-03 | Evaluation Case B report (free-form layout, no IDs) | PASS (detects) | 2026-11-07, 18 errors: 16 missing sections, no REQ IDs, unlabeled results |
| CK-04 | Evaluation Case C report (free-form layout, no IDs) | PASS (detects) | 2026-11-07, 19 errors |
| CK-05 | Unfilled `templates/skeleton.md` | PASS | 0 structure errors, only the 43 FILL markers fail (P10) |

## Behavioral (full skill runs)

| ID | Scenario | What must happen | Status |
|---|---|---|---|
| TC-01 | IEEE paper with `.aux`, measured results | Section 36 layout from the skeleton, IDs in the body, checker 0 errors | NOT RUN |
| TC-02 | Concept paper, no results | Results section says the paper reports no measured results | NOT RUN |
| TC-03 | Paper with blue `\tgt{}` targets | Targets labelled as targets, never REPORTED IN PAPER | NOT RUN |
| TC-04 | Older free-form PROJECT_REPORT.md already present | Agent asks before overwriting and rebuilds from the skeleton | NOT RUN |
| TC-05 | Paper in a `Paper/` subfolder, no `.aux` | Paper found, numbers marked uncompiled, checker run without `--aux` | NOT RUN |
