---
name: project-report-to-github
description: Use when a research folder holds a PROJECT_REPORT.md (or project_report.md, usually from paper-to-project-report) plus the paper's .tex and the user wants a runnable, tested, GitHub-ready code repository built from them in a Github/ folder. Trigger on "project report to github", "project-report-to-github", "build the repo from my report", "make a Github folder for this paper", "implement this paper as a repository", "turn the project report into code".
---

# Project Report to GitHub Repository

> **Paths.** `${CLAUDE_SKILL_DIR}` is the folder that holds this SKILL.md. Claude Code fills it in. In other agents, replace it with that folder's path. `${CLAUDE_SKILL_DIR}/../<skill>` is a sibling skill from the same collection, so install that skill too.

## Overview

Builds a real, executed, academically honest research repository in `./Github/` from two sources: the engineering report (the spec) and the `.tex` paper (the scientific truth). The governing instructions are the user's own prompt, stored verbatim in `references/prompt.md`. That file is the contract. This page adds the run notes and the final gate that keep the output honest.

**REQUIRED:** Read `references/prompt.md` in full before reading any project file. Follow its 33 sections, its A/B/C/D decision rule, and its required files exactly.

Pipeline position: `paper-to-project-report` writes the report, this skill builds the repository, and `repo-forensic-audit` can audit the result if the user asks.

## Run notes

1. **Find the inputs.** The report may be `PROJECT_REPORT.md` or `project_report.md`, in the working directory. The paper may sit beside it or one level down (for example `Paper/`). Take the `.tex` with `\documentclass`, plus everything it pulls in through `\input`, `\include` and supplements. Read the `.aux` for compiled numbers. If the report is missing, stop and offer `paper-to-project-report`. If two candidate papers exist, ask which one.
2. **Existing `Github/`.** Never delete or overwrite it silently. Inspect it, then ask: update in place, or rename it to `Github.bak-<YYYY-MM-DD>` and rebuild. Never open an existing `.env`. It stays out of the deliverable.
3. **Reuse the report's IDs.** When the report defines `REQ-`, `EXP-`, `METRIC-`, `DEC-` and `ASM-` IDs, they are the traceability keys. Every REQ, EXP and METRIC gets a row in `docs/paper_implementation_mapping.md`. Every DEC and ASM appears in `docs/assumptions.md`. New assumptions get `IMPL-ASM-001` onward so they never collide. Build in the order of the report's phases.
4. **Inventory before writing code.** List code, data, logs and results already in the folder (for example `code_and_data/` or a simulator directory). Reuse real code with a provenance note instead of rewriting it. Existing measured logs are evidence to cite, never numbers to restate as "reproduced locally".
5. **Classify every paper number before it enters a doc.** A number can be measured (label "Reported in the paper"), an implementation target (`\tgt{}`, blue text, "target", "projected", "expected": label "Target stated in the paper, not a measured result"), a cited-work number (label "Cited from prior work"), or illustrative. For a paper with no measured results, the README says "The paper reports no measured results."
6. **Paid APIs and LLMs.** Put the provider behind one client interface. Add a deterministic offline stub (fake or replay client) that tests, smoke runs and CI use. Read keys only from environment variables, with the names listed in `.env.example`. Never spend API credits during validation without asking. The live path is recorded as NOT RUN.
7. **Environment.** Create the venv outside the deliverable: `python -m venv .venv-github` in the working directory, never inside `Github/`. If the `py` launcher fails, use `python`. Install CPU wheels for heavy frameworks. A failed or oversized install is BLOCKED with the error tail quoted. Never swap the paper's library for another one just because it installs.
8. **Build order.** Config and core domain logic, then data, then models and algorithms, then the train, evaluate and infer entry points, then tests, then the validation loop. Write the docs and status files last, from the code that exists.
9. **Tests pin the paper.** Every key equation or algorithm gets at least one test that checks a hand-computed value or invariant from the paper (for example a reward formula on a 3-agent toy input), not just shapes or imports.
10. **Evidence for the smoke report.** Save each command's output to a log in the scratchpad. Quote the real summary line (for example `37 passed in 4.12s`) into `SMOKE_TEST_REPORT.md`. Status values are exactly PASS, FAIL, NOT RUN or BLOCKED. Record the Python version and OS. Write `<repo>` instead of absolute paths, because user names in paths leak identity.
11. **Anonymous review.** If the paper is under double-anonymous review (an `anonymous` or `review` class option, "Anonymous Author(s)", or the user says so), `Github/` carries no author names, affiliations, emails, GitHub user names or institutional URLs. CITATION.cff uses "Anonymous" and LICENSE names "The Authors". Run the checker with `--forbid`.
12. **Citation and license.** Build `CITATION.cff` from the paper's title and authors. Never invent a DOI, arXiv ID or acceptance status. Default the license to MIT and log it as an assumption for the author to confirm. Never vendor a dataset whose license forbids redistribution. Ship a download script instead.
13. **Git stays local.** Do not run `git init`, commit, add a remote or push unless the user asks. Offer it in the handoff.
14. **House style.** Apply the user's prose rules, if they have any, to every doc (for example, no em dashes and no semicolons). Without such rules, use standard punctuation. Code, commands and quoted paper text are exempt.
15. **Clean before the gate.** Delete `__pycache__`, `.pytest_cache`, `.mypy_cache`, `.ruff_cache`, `*.pyc`, `*.egg-info` and logs inside `Github/`. Smoke outputs go to a gitignored `results/` path or get removed.

## Final gate (run before replying)

```bash
python "${CLAUDE_SKILL_DIR}/scripts/check_repo.py" Github --report PROJECT_REPORT.md
# anonymous review: add --forbid "Author One,Author Two,Institution,github-user"
# the user's style rules forbid em dashes and semicolons: add --style
```

The checker covers R01 to R16: required files, status sections, smoke statuses, caches, secrets, large files, placeholder bodies, doc commands, broken links, ID traceability, machine paths, house style, identity strings, undeclared imports, README provenance and overclaims, smoke config and CI. It must print `0 errors`. Fix each WARN or explain it under Technical Debt in `IMPLEMENTATION_STATUS.md`. After any edit to the checker, rerun `check_repo.py --selftest`. It must pass every case. Log each real run of this skill in `evals/test-cases.md`.

Then reply in the format of prompt section 32, and add the checker's final line, the venv location, and anything that needs the author (license, open DEC items, datasets to download).

## Common mistakes

| Mistake | Fix |
|---|---|
| A `.env` file with real keys ships inside `Github/` | Only `.env.example`, and `.env` is in `.gitignore` |
| `__pycache__`, `.mypy_cache`, `.ruff_cache` left after validation | Clean, then run the checker last |
| Result JSON embeds `C:\Users\<name>\...` | Write paths relative to the repository root |
| A stub such as `def apply_shock(...): pass` presented as implemented | Implement it, or list it under Not Implemented with the reason |
| A blue `\tgt{}` target number labelled "Reported in the paper" | Label it a target, not a measured result |
| A README command names a file, make target or module that does not exist | The checker's R08 lists them. Fix the docs or the code |
| Docs link to `../paper.tex` outside `Github/` | Links break on GitHub. Describe the paper in text instead |
| Tests that only assert imports or shapes | Add a paper-derived numeric check per key equation |
| Calling a paid LLM API during smoke tests | Use the offline stub. The live path is NOT RUN |
| Launching the full experiment during the build | Run the smoke config only. Full runs are the user's call |
