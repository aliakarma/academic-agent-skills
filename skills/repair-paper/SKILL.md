---
name: repair-paper
description: Use when a research manuscript (LaTeX .tex, Word .docx, or Markdown) must be revised against an existing forensic writing audit, such as an audit.md from audit-paper with numbered issues (I-001...), and every audit issue must be repaired or accounted for. Trigger on "repair-paper", "repair my paper", "fix the issues in audit.md", "apply the audit", "restore clarity from the audit", "fix every audit issue". Do NOT trigger when no audit exists yet (audit-paper), for open-ended polishing (universal-manuscript-polish), for reviewer response letters (response-to-reviewer), or for reviewer-driven rewrites (manuscript-revision).
---

# Repair Paper: Audit-Driven Manuscript Repair

> **Paths.** `${CLAUDE_SKILL_DIR}` is the folder that holds this SKILL.md. Claude Code fills it in. In other agents, replace it with that folder's path. `${CLAUDE_SKILL_DIR}/../<skill>` is a sibling skill from the same collection, so install that skill too.

## Overview

Repairs the manuscript itself, issue by issue, using a forensic writing audit as the repair specification, and ends with a report that accounts for every audit ID. The governing instructions are the user's own prompt, stored in `references/prompt.md` (43 sections). That file is the contract. This page adds the run notes that keep a repair complete, traceable, and faithful to the science.

**REQUIRED:** Read `references/prompt.md` in full, then the entire audit, before editing anything.

**Core principle:** different wording, better communication, same scientific truth. When in doubt, flag the issue for the author instead of guessing.

This skill pairs with `audit-paper`, which diagnoses and writes the audit. When both apply, audit first, then repair. While this skill runs, it is the governing workflow. `universal-manuscript-polish` contributes only its backup, `verify_edit.py`, and compile-log conventions.

## Run notes

1. **Locate inputs.** Find the audit (default `audit.md` next to the manuscript, or the newest one if several exist, and say which) and the manuscript root (the `.tex` file with `\documentclass`, plus everything it `\input`s). Note any reviewer comments and the venue template.
2. **Back up and baseline.** Copy every file you will touch to `_polish/pre_repair/` (never overwrite an existing `_polish/original/`). Compile once and record the page count and the log warnings. They are the baseline.
3. **Build the repair map.** Read the whole audit, including its pattern section (P-01...) and its global editing rules. Note every issue whose fix needs code, data, a source paper, or an author decision.
4. **Look for the artifact before deciding code-dependent issues.** If the audit cites the implementation (release rules, message fields, experiment conditions), search the project for the code or data first. If nothing is there, take the reading that the manuscript's own tables, pseudocode, and results support, and add a human-review marker.
5. **Fix notation before prose.** If the audit reports symbol collisions, build a one-object, one-symbol table first. Rename only what collides, define every symbol next to its equation, and write formal conditions as statements that hold or fail. Never change an equation's logic.
6. **Repair in severity order, section by section.** Make exact-match edits per paragraph. For a term changed across the paper, use one script that asserts each target occurs the expected number of times. Re-read the edited paragraph against its tables and equations, especially negations, quantifiers (every vs. some), prepositions (to/from), and causal direction.
7. **Fix figures at their source.** If a figure's labels drift from the text, edit the figure source (TikZ, pgfplots, plotting script), recompile it, and look at the rendered image.
8. **Mark what you cannot resolve.** Put this comment in the source, never in rendered text: `% [HUMAN REVIEW REQUIRED] HR-NN: <what is missing and what the author must decide>`. Continue the numbering from markers that already exist. Mark title changes and policy choices too, even when you made them.
9. **Run the mandatory global search.** For every audit pattern, grep the whole manuscript again, then run `count_patterns.py`. Repairs often add connectors of their own. A guarded count that rises means connectors were swapped in rather than removed, so cut the decorative ones.
10. **Verify meaning.** Run `verify_edit.py` from universal-manuscript-polish against the backup. Changed math, labels, and table cells are expected FAILs, so justify each one. Every changed number must have a stated reason, such as a corrected date or a new symbol subscript.
11. **Compile and look.** Compile, compare the log with the baseline, and fix every new warning. Inline tuples that cannot break cause overfull boxes. Render the pages that hold changed equations and figures, and look at them.
12. **Check the page limit.** Apply prompt sections 28 to 30. Use the venue's stated limit. If none is given, keep the baseline length and say so.
13. **Write the report.** Save `_polish/REPAIR_REPORT.md` with sections A to F (prompt section 41) and one Section B row per audit ID: `| I-001 | FIXED | location | change |`. Use the statuses `FIXED`, `MERGED INTO I-xxx`, `NOT FIXED: REQUIRES AUTHOR INPUT`, `NOT FIXED: WOULD REQUIRE UNSUPPORTED INFORMATION`, or `NOT APPLICABLE AFTER CONTEXTUAL REVIEW`. In chat, give sections A to F with a grouped matrix (IDs grouped by status) and link to the file.
14. **House style.** Apply the user's writing-style rules, if they supply any (for example, no em dashes or semicolons in prose), to every sentence you write, and avoid inflated vocabulary. Never alter quoted manuscript text to meet them.
15. **Record it.** If a project memory exists for this manuscript, add the repair date, the report path, and the open HR markers.

## Common mistakes

| Mistake | Correction |
|---|---|
| Swapping one connector for another ("thus" to "therefore") and calling it repaired | Run `count_patterns.py` and remove connectors that assert no real relation |
| Marking an issue FIXED when only the wording changed and the underlying fact is still unverified | Use NOT FIXED: REQUIRES AUTHOR INPUT and add an HR marker |
| Fixing one instance of a term drift | Map every variant with grep, then change them all, including tables, captions, and figure sources |
| Renaming symbols in prose but not in equations or figures | Change the notation table in one pass across all of them |
| Inventing an example the audit suggests ("a crash") that the paper never states | Restate only what the manuscript supports |
| Deleting a caveat to smooth a paragraph | Keep every result-level caveat, and trim only exact restatements |
| Claiming page compliance from a word count | Compile and read the page count from the PDF |

## Final checks (run before replying)

```bash
S="${CLAUDE_SKILL_DIR}/scripts"
python -I "$S/check_report.py" audit.md _polish/REPAIR_REPORT.md        # must print "0 problems"
python -I "$S/count_patterns.py" _polish/pre_repair/<main>.tex <main>.tex  # must print "0 guarded patterns rose"
python -I "${CLAUDE_SKILL_DIR}/../universal-manuscript-polish/scripts/verify_edit.py" _polish/pre_repair/<main>.tex <main>.tex
```

`check_report.py` verifies that sections A to F are in order, that every audit ID appears exactly once with a valid status, that each MERGED row names an existing issue, and that the Section A counts match the matrix (`--selftest` exercises it). Quote the path in shell commands, because the home folder name contains a space.
