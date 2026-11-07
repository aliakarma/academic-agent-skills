# project-report-to-github test cases

Status values: PASS, FAIL, NOT RUN. Log each real run here with the date, folder and checker result.

Evaluation Cases A to D are private research projects that the checker was run against. Their files are not distributed, and the labels are neutral on purpose. Only the checker outcomes are recorded.

## Checker (scripts/check_repo.py)

| ID | Case | Status | Evidence |
|---|---|---|---|
| CK-01 | `--selftest`: clean fixture has zero findings, 16 seeded faults (R01 to R16) each detected | PASS | 2026-11-07, `selftest: 17/17 passed`, mypy clean |
| CK-02 | Baseline: Evaluation Case B repository, built from the bare prompt before this skill existed | PASS (detects) | 2026-11-07, 61 errors: shipped `.env`, 15 cache dirs, 18 result files with `C:\Users\...` paths, 24 docs breaking house style, 3 missing required files |
| CK-03 | Baseline: Evaluation Case D repository, built from the bare prompt | PASS (detects) | 2026-11-07, 13 missing required files, 8 cache dirs, 2 placeholder function bodies |
| CK-04 | False positive: `configs/pilot_$e.yaml` in a shell loop | PASS | Fixed 2026-11-07, now part of the clean fixture |

## Behavioral (full skill runs)

| ID | Scenario | What must happen | Status |
|---|---|---|---|
| TC-01 | Fresh folder: PROJECT_REPORT.md with REQ IDs plus paper in `Paper/` | Paper found in subfolder, every REQ/EXP/METRIC mapped, checker 0 errors | NOT RUN |
| TC-02 | `Github/` already exists | Agent asks update vs. backup-and-rebuild, never deletes, never reads `.env` | NOT RUN |
| TC-03 | Paper numbers are blue `\tgt{}` targets | Docs label them targets, never "Reported in the paper" | NOT RUN |
| TC-04 | LLM-agent paper using a paid API | Offline stub used by tests and CI, live path NOT RUN, no credits spent | NOT RUN |
| TC-05 | Double-anonymous submission | `--forbid` run with author names passes, CITATION.cff says Anonymous | NOT RUN |
| TC-06 | Concept paper with no results | README says the paper reports no measured results, no invented numbers | NOT RUN |
| TC-07 | Heavy dependency fails to install (torch, SUMO) | Marked BLOCKED with error tail, library not silently swapped | NOT RUN |
| TC-08 | Report missing, only .tex present | Agent stops and offers paper-to-project-report | NOT RUN |
