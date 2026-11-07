# PAPER_REPORT: <paper title>

**Status:** Step 0 of 6 (Input Map). Update this line at every step.
**Readiness:** <Blueprint with implementation targets | Measured draft>
**Built:** <YYYY-MM-DD> by the idea-to-paper skill

## 1. Input Map

| Element | Supplied by the author | Used as | Inferred by the skill |
|---|---|---|---|
| Title | | | |
| Abstract | | | |
| Idea or problem | | | |
| Research gap | | | |
| Research questions | | | |
| Method | | | |
| Datasets | | | |
| Baselines and metrics | | | |
| Measured results | | | |
| Authors | | | |
| Venue and page limit | | | |
| Must-cite references | | | |
| Figures supplied | | | |

## 2. Decisions and assumptions

Each inference or choice the input did not settle, with the reason. Conflicts inside the input and how they were resolved.

## 3. Blueprint

Problem, gap (with the papers that show it), research questions, contributions with their sections, method components, notation, equation list, algorithms, figure plan, table plan, page budget.

## 4. Literature and references

- Concept families and queries run, with the tool used for each.
- Candidates found, entries verified (MATCH), entries dropped and why.
- Path to `_build/verify.csv` and `_build/sources.csv`.
- Shortfall against the minimum, if any.

## 5. Verification results

| Check | Command | Result |
|---|---|---|
| Build | `latexmk -pdf -norc ...` | |
| Paper rules | `check_paper.py ...` | errors, warnings, targets |
| Citations | `audit_citations.py ...` | |
| Reference identity | `verify_refs.py ... --strict` | |
| Prose scan | `scan_manuscript.py ...` | |
| Page count | `pdfinfo` | |
| Visual inspection | page PNGs | issues found and fixed |
| Polish | universal-manuscript-polish Stage 3 | |

Record any check that did not run as NOT RUN, with the reason.

## 6. Implementation targets

Count: <N values, M floats>. Full register: `_build/target_register.md`. Source of every value: `_build/targets.py`.

### What to run

| Experiment | Dataset | Baselines | Seeds | Metric | Target it must reach or test |
|---|---|---|---|---|---|

## 7. Author to confirm

- Numbers the author supplied without saying they were measured.
- Author names, affiliations, funding, ethics approval, data and code availability.
- Any inferred method choice the author may want to change.
- Venue conversion (`/paper-format-converter <venue>`) when the venue is not an IEEE conference.
