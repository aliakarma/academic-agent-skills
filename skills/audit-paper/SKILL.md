---
name: audit-paper
description: Use when the user wants a line-by-line forensic audit of the writing of a research manuscript (LaTeX .tex, Word .docx, or Markdown) that diagnoses AI-rewrite damage, clarity loss, terminology drift, claim and scope inflation in the wording, math-prose mismatch, and other academic-writing weaknesses, and writes the full diagnosis to audit.md without editing the paper. Trigger on "audit-paper", "audit the writing of my paper", "writing audit", "forensic writing audit", "find AI-rewrite damage", "line-by-line writing audit", "diagnose the writing before I edit". A bare "audit my paper" belongs here only when the request is about the prose. Do NOT trigger for the research substance (real claims, research gap, novelty, prior work, or journal fit, which is research-auditor), simulated peer review (peer-review), code or fabrication audits (repo-forensic-audit), or requests to actually revise or polish the text (universal-manuscript-polish, text-humanizer).
---

# Audit Paper: Forensic Academic Writing Audit

> **Paths.** `${CLAUDE_SKILL_DIR}` is the folder that holds this SKILL.md. Claude Code fills it in. In other agents, replace it with that folder's path. `${CLAUDE_SKILL_DIR}/../<skill>` is a sibling skill from the same collection, so install that skill too.

## Overview

Produces one `audit.md` that maps every writing weakness in a manuscript, line by line, without changing the manuscript. The governing instructions are the user's own prompt, stored verbatim in `references/prompt.md`. That file is the contract. This page adds only the run notes that keep the audit complete, verifiable, and honest.

**REQUIRED:** Read `references/prompt.md` in full before reading the manuscript. Follow its 61 rules, its six categories (A to F), its severity and priority systems, its exact issue format (rule 49), and its 15-section output order (rule 61).

**Diagnosis only.** Never edit the manuscript during this skill, even for an obvious typo. Fixes come later, in a separate request.

## Run notes

1. **Find the manuscript.** Use the path the user gives. Otherwise take the `.tex` file containing `\documentclass` in the working directory, plus every file it pulls in through `\input`, `\include`, `\subfile`, and any appendix or supplement. For `.docx`, extract the text with paragraph numbers first and say that locations are paragraph numbers. Read every file completely, including tables, listings, captions, `%` comments, and back matter.
2. **Fix the line convention before writing.** For `.tex`, cite source line numbers. Most paragraphs sit on one source line, so add a sentence ordinal (`L232, s3`). State the convention at the top of `audit.md`, and say that the PDF's `lineno` margin numbers differ. Never mix the two systems.
3. **Read sequentially, in chunks, to the last line.** Read the file in consecutive ranges and keep a coverage ledger. Template boilerplate and commented-out class text still count as reviewed regions. Check them for rendered residue such as placeholders, `TO COMPLETE`, or e-mail stubs.
4. **Read the figures, not just the captions.** If the figures are TikZ, pgfplots, or other source files, read the source. If they are images, view them. Rule 43 needs the figure content to compare with the caption and the text.
5. **Cross-check every number.** Recompute every total, product, and split the paper states, for example families × replicas = fixtures, or the sum of the subsets. Compare the abstract, methods, tables, results, and conclusion. A count whose unit changes between sections (conditions vs. trials) is an evidence issue.
6. **Count patterns with searches, not impressions.** After the first instance of a pattern, grep the whole manuscript: contractions, "therefore/thus/however", each variant of a key term, "does not establish", quote styles, dashes. Report the counts in Section 7.
7. **Check meaning against the formal anchors.** Compare every safety rule, quantifier, preposition (to/from), negation, and causal verb against the paper's own equations, tables, pseudocode, and listings. Reversed meanings are the highest-value findings and are usually rated Critical.
8. **Pattern IDs.** When text-humanizer is installed, tag issues with its pattern IDs (B01 to B36, from `${CLAUDE_SKILL_DIR}/../text-humanizer/references/writing-patterns.md`, Section 2) so habits can be traced. The prompt's own categories remain primary.
9. **Queries, not guesses.** Author identity, affiliations, funding, AI-tool disclosure, and anything that needs data you do not have become explicit queries for the author. Never invent an earlier version of the text (rule 54), and never judge who or what wrote the text (rule 52).
10. **Artifact claims.** If the folder contains code, figure sources, data, or logs, check the paper's reproducibility and data-availability statements against what actually exists. Report mismatches as evidence issues.
11. **Write the file.** Save `audit.md` next to the manuscript. If an `audit.md` already exists, read it and ask before overwriting, or write `audit-<date>.md`. Use the issue ID format `I-001`, the pattern format `P-01`, the issue heading `**Issue I-001**` on its own line, and a master-index table whose rows begin `| I-001 |`, so that the checker can parse the file.
12. **House style.** Apply any style rules the user keeps on record to the audit's own prose (for example, a rule against em dashes and semicolons). Without such rules, use standard punctuation. Never alter quoted manuscript text to meet them.

## Final checks (run before replying)

```bash
python -I "${CLAUDE_SKILL_DIR}/scripts/check_audit.py" audit.md   # must print "0 problems"
```

The checker verifies:
- the 15 sections are present and in order
- every issue has all 11 fields
- every issue sits in the section that matches its severity
- the body and the master index agree
- every `I-NNN` and `P-NN` reference exists
- the stated totals match the counted ones

Then answer the 12 questions in prompt section 61.15. Any "no" means more reviewing before replying.

## Reply to the user

Keep it short. State:
- the path of `audit.md`
- the counts by severity
- the Critical findings in one line each
- which items need the author
- what was not checked (for example, bibliographic verification, which rule 44 excludes unless the user asks).

The audit itself carries the detail.

## Common mistakes

| Mistake | Fix |
|---|---|
| Stopping after many findings, or sampling later sections | Read to the last line, and record the coverage ledger in Section 2 |
| Quoting PDF line numbers for some issues and source lines for others | Use one convention, stated at the top |
| Suggesting replacement wording | Say what to restore or check, never the new sentence (rule 58) |
| Folding 20 instances into one issue | Log the individual instances and add a P-pattern (rules 50 and 59) |
| Inflating severity to look thorough | Critical only when meaning, evidence, or validity changes (rule 47) |
| Calling text "AI-generated" | Name the pattern and its cost to the reader. Never estimate an AI probability. |
| Overwriting an earlier audit | Ask first, or date the new file |
| Fixing a typo "while you are there" | The manuscript stays untouched in this skill |
