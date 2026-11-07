---
name: paper-to-project-report
description: Use when turning an academic paper (LaTeX .tex, any venue, concept paper or full study) into an implementation-oriented engineering specification, reproducibility audit, or GSD-ready PROJECT_REPORT.md, or when the user asks to convert a paper into requirements, roadmap phases, a project spec, or an implementation plan for a coding workflow. Trigger on "paper to project report", "paper-to-project-report", "paper to md", "paper-to-md", "make a project report from my paper", "engineering spec from this paper", "GSD handoff for this paper".
---

# Paper to Project Report

> **Paths.** `${CLAUDE_SKILL_DIR}` is the folder that holds this SKILL.md. Claude Code fills it in. In other agents, replace it with that folder's path. `${CLAUDE_SKILL_DIR}/../<skill>` is a sibling skill from the same collection, so install that skill too.

## Overview

Converts one research paper into a single `PROJECT_REPORT.md`, an evidence-traced engineering specification that a GSD workflow or the `project-report-to-github` skill can build from without rereading the paper. The governing instructions are the user's own prompt, stored verbatim in `references/prompt.md`. That file is the contract. This page adds the run notes and the final gate that keep the report faithful and machine-usable.

**REQUIRED:** Read `references/prompt.md` in full before reading the paper. Follow its 39 sections, its A/B/C/D classification, its ID scheme, and its section 36 hierarchy exactly.

Pipeline: `paper-to-project-report` writes the report, then `project-report-to-github` builds `Github/` from it. The second skill maps every REQ, EXP and METRIC ID into its traceability matrix, so a report without IDs breaks the pipeline.

## Run notes

1. **Start from the skeleton.** Copy `templates/skeleton.md` to `PROJECT_REPORT.md` and replace every `FILL`. It carries the section 36 headings in order, the classification legend, both accepted ID definition forms, and the ten GSD Handoff blocks. Add subsections freely. Never rename, merge or drop a top-level section.
2. **Find the paper.** Use the path the user gives. Otherwise take the `.tex` file with `\documentclass` in the working directory or one level down (for example `Paper/`), plus every file it pulls in through `\input`, `\include`, `\subfile`, and any appendix or supplement `.tex`. Read each one completely, including tables, TikZ figures, captions, and `%` comments. Author comments such as `% [HUMAN REVIEW REQUIRED]` often hold open method decisions. Report them. Read files over 2000 lines in consecutive chunks until the end.
3. **Get real numbering.** If a `.aux` file exists, read the `\newlabel` and toc lines to get the compiled section, table, figure, and equation numbers. Cite those plus `.tex` line ranges (for example `§V-D, L370-391`). Without an `.aux` file, cite labels and section titles and say the numbers are uncompiled. Never guess a number.
4. **Define each ID once, in the body.** Use a table row whose first cell is the ID (`| REQ-001 | ... | [A] | §III-B, Eq. (4) | ... |`) or a bold lead (`**REQ-001. Name.** Classification: [A]. Evidence: ...`). Every REQ carries its class and its evidence on that row or within the next lines. REQ, EXP and METRIC IDs live in the requirements and experimental sections. ASM, DEC, DEP and RISK IDs live in their own sections. The GSD Handoff only restates them.
5. **Inventory the folder.** Look for code, data, logs, configs, and result files before writing the reproducibility audit. The audit scores what exists, not what the paper promises.
6. **Classify every number.** Measured numbers get the section 16 labels (REPORTED IN PAPER, NOT VERIFIED). Implementation targets (`\tgt{}`, blue text, "target", "projected", "expected") are targets, never results. Numbers from related work go in a separate cited-work table. Never present either as the paper's findings.
7. **Concept papers.** If the paper reports no results, say so. The results section then holds the cited-numbers table plus a "does not exist" row. The labels PLANNED IN PAPER, REQUIRED FOR REPRODUCTION and RECOMMENDED ADDITION still apply.
8. **Hunt internal inconsistencies.** Compare equations against the workflow text, figures against the component list, hypotheses against the baseline set, and assumptions against the ethics section. Each mismatch becomes a weakness and usually a DEC item.
9. **Write the file.** Save `PROJECT_REPORT.md` next to the paper's working folder. If one exists, read it and ask before overwriting. An older report in a different layout is not a template. Rebuild it from the skeleton. The prompt's "no meta-commentary" rule binds the document. The chat reply is a short handoff: path, checker result, blockers, and what was not checked.
10. **House style.** Apply any style rules the user has on record to the report's prose (for example, a rule against em dashes and semicolons). Without such rules, use standard punctuation. Never alter quoted paper text or equations to meet them. Quote paper text as a `>` blockquote so the checker exempts it.

## Final gate (run before replying)

```bash
python "${CLAUDE_SKILL_DIR}/scripts/check_report.py" PROJECT_REPORT.md --aux <paper>.aux
# no compiled .aux: drop --aux (P08 is skipped). The user's style rules forbid em dashes and semicolons: add --style
```

The checker covers P01 to P11: the section 36 order, IDs present, every cited ID defined, the ten handoff blocks, REQ classification and evidence, results provenance labels, cited Table/Fig/Eq/Algorithm numbers against the `.aux`, house style, meta-commentary and leftover `FILL`, and Mermaid. It must print `0 errors`. Fix each WARN or name it in the reply. Then answer the 19 questions in prompt section 38. A "no" means fix the report first. After any edit to the checker, rerun `check_report.py --selftest`. Log each real run in `evals/test-cases.md`.

## Common mistakes

| Mistake | Fix |
|---|---|
| Free-form layout (Project Overview, Project Phases, Appendix) instead of section 36 | Start from the skeleton. The checker's P01 lists missing sections |
| No REQ/DEC/ASM IDs at all | Define them in the body (run note 4). P02 fails a report with no REQ IDs |
| IDs written only in the GSD Handoff | Define them in the body. The handoff restates them |
| Filling a missing hyperparameter with a conventional value | Mark it missing [D], add an ASM or DEC entry, state the effect |
| Citing section, table or equation numbers from memory | Read them from `.aux`. P08 flags numbers the paper does not have |
| Scoring reproducibility on the paper's promises | Score the code and data actually present |
| Treating related-work numbers or `\tgt{}` targets as results | Cited-work table for the first, target label for the second |
| Generic phases (setup, build, test, deploy) | Derive phases from the paper's own plan, milestones, and blockers |
| Adding Docker, MLflow, databases by habit | Recommend only what the research needs, classified per section 28 |
| Printing the whole report into chat | Write the file and give a short handoff |
