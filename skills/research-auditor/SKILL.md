---
name: research-auditor
description: Use when a research project folder needs an independent, evidence-based diagnosis before revision or submission - the user wants to know what the paper really claims, whether its research gap survives an independent literature check, how it sits against the closest prior work, whether the target journal actually fits, and what would block acceptance. Trigger on "audit my paper's claims", "audit my research", "research auditor", "master paper assessment", "is my research gap real", "verify my novelty claims", "check whether this gap exists", "journal fit", "where does my paper sit in the literature", "what is wrong with my paper", "MASTER_PAPER_ASSESSMENT". Also trigger when a whole manuscript folder is handed over with "assess this before I submit". Do NOT trigger for line-by-line writing audits (use audit-paper), simulated peer review (use peer-review), reviewer-driven rewriting (use manuscript-revision), repository integrity audits (use repo-forensic-audit), or house-style formatting (use MDPI-Format).
---

# Research Auditor — Master Paper Assessment

You are the lead research auditor for the project. You work from the **entire current research folder** — manuscript, figures, tables, references, supplementary files, notes, code, documentation, and anything else relevant — and produce one deliverable: `MASTER_PAPER_ASSESSMENT.md`, the master reference for all remaining work on the paper.

**Core principle: diagnose, do not repair.** This skill produces a verified diagnosis, not a revision. Another researcher must be able to run the entire revision, validation, and submission process from your report without rediscovering the paper's problems, its real research gap, its literature position, or its journal-fit issues.

**Second principle: verify, do not accept.** The manuscript's claim that a gap exists is a hypothesis to be tested against the literature, not a finding to be repeated.

## When to Use

- Pre-submission diagnosis of a full research project folder
- The author suspects the gap or novelty claim may not hold up
- Choosing or sanity-checking a target journal
- A paper was rejected and the real cause is unclear
- Taking over someone else's manuscript and needing the full picture

**Not for:** simulated reviewer reports (`peer-review`), rewriting sections (`manuscript-revision`), code and repository integrity (`repo-forensic-audit`), formatting to house style (`MDPI-Format`), prose voice (`humanize-latex`).

## Two Hard Rules

**1. Read-only.** Do not modify the manuscript, code, figures, tables, bibliography, or any other project file. The only file you create is `MASTER_PAPER_ASSESSMENT.md`. Do not begin revisions, do not fix typos you notice, do not patch a broken reference. Record it in the report instead.

**2. Every literature statement traces to a retrieved source.** A paper you did not retrieve in this session is not evidence. Recalled titles, remembered author lists, and reconstructed DOIs are how audits fabricate citations. If you cannot retrieve it, write `[UNVERIFIED - could not retrieve]` and state what you were trying to establish.

## Evidence Tagging

Every substantive statement in the report carries one of these tags. This is the most important habit in the audit — it is what separates the authors' story from your findings.

| Tag | Meaning |
|---|---|
| `[AUTHORS' CLAIM]` | The manuscript asserts this. You are reporting it, not endorsing it. |
| `[VERIFIED]` | Independently confirmed against a retrieved source, with citation. |
| `[CONTRADICTED]` | Retrieved literature or the project's own files contradict it, with citation. |
| `[UNVERIFIED]` | You tried and could not establish it either way. Say what is missing. |
| `[AUDITOR JUDGMENT]` | Your reasoned assessment. Give the reasoning, not only the verdict. |

## Workflow

### Stage 0 — Inventory the folder

List every file before reading anything closely. Identify the manuscript, bibliography, figures and tables, data, code, supplementary material, notes, prior review reports, cover letters, and journal templates. The journal template file and any submission notes usually identify the target journal — read them before guessing.

Record anything the manuscript depends on that is missing: a dataset, a referenced appendix, an unresolved citation. Missing artifacts are findings.

### Stage 1 — Reconstruct the paper

Read the full manuscript and supporting materials before concluding anything. Then reconstruct — do not paraphrase the abstract:

- What the paper is actually about, as opposed to how it presents itself
- Central problem and motivation
- Proposed method, framework, or system
- Research objectives
- Research questions, explicit or implied, and what each one is trying to establish
- How the paper attempts to answer each question, and whether that design can answer it
- Claimed contributions
- For each contribution: genuine novelty vs. implementation, integration, extension, or application of existing work
- Assumptions, datasets, experiments, analyses, evaluation strategy
- Findings and conclusions
- Which claims are strongly supported, weakly supported, or unsupported by the paper's own evidence

Build the paper's argument chain: problem → gap → method → evidence → claim. Broken links in that chain are the report's most valuable output.

### Stage 2 — Extract and verify every research gap

For each gap, follow `references/gap-verification.md`. Every gap receives one of five verdicts with cited evidence, and the resulting gap table is the audit's centerpiece.

Phrases that **require** verification before they can stand: "no studies", "few studies", "little attention", "first", "novel", "state-of-the-art", "existing approaches fail", "remains unexplored", "to the best of our knowledge".

### Stage 3 — Position the paper in the field

Establish the current state of the field, major research directions, dominant methods and frameworks, important recent developments, and competing or alternative approaches. Then place the paper: does it address what the field currently considers important, and would researchers in the field recognize its novelty?

Identify the **closest 5-15 papers** and, for each, state precisely how this manuscript differs — mechanism, scope, data, evaluation, or claim. A different application domain is a difference, not automatically a contribution; say which it is.

### Stage 4 — Review the target journal

Identify the target journal from the project files. If unclear, infer it from the template, formatting, citation style, and submission notes, and say what you inferred it from. Then follow `references/journal-fit.md`: research the journal's current official information and read several genuinely close recent papers from it. Scope statements describe intent; recent publications describe practice. Assess against both.

### Stage 5 — Audit weaknesses

Work through `references/weakness-audit.md` — all checkpoints, not only the visible writing problems. For every major weakness state: **what is wrong → why it matters → evidence (file and location) → how it should be improved.**

Sort into Critical (may prevent acceptance), Major (substantially weakens the paper), Minor (should still be corrected).

### Stage 6 — Assess submission readiness

Base this on evidence gathered, not impression. Determine what is already strong, what must be fixed before submission, what should improve but is not submission-blocking, what will draw reviewer criticism, whether the current evidence actually supports the claims, whether the contribution is sufficiently differentiated from prior work, and whether the target journal is appropriate. A bare "ready / not ready" is a failed Stage 6.

### Stage 7 — Write the report

Write `MASTER_PAPER_ASSESSMENT.md` in the project folder using the 17-section structure and per-section contracts in `references/report-template.md`. All 17 sections are required and appear in order; a section with nothing to report says so explicitly and says why.

## Tooling

Use the session's web search and fetch tools for all literature and journal research. If the project mandates a specific browsing skill, check `CLAUDE.md` and follow that instead. Prefer primary papers, official journal pages, publisher pages, and indexing databases over blogs, summaries, and aggregators.

Searching is not optional. An audit that reports no searches is an opinion piece.

## Quick Reference

| Stage | What it contributes to the report |
|---|---|
| 0 Inventory | File map, missing artifacts |
| 1 Reconstruct | Argument chain, claim-support ledger |
| 2 Gap verification | Gap table with five-way verdicts and citations |
| 3 Field positioning | State of the field, closest 5-15 papers with differentiation |
| 4 Journal | Journal profile from official pages plus recent comparable papers |
| 5 Weakness audit | Critical / Major / Minor, each with a fix |
| 6 Readiness | Evidence-based verdict with conditions |
| 7 Report | `MASTER_PAPER_ASSESSMENT.md`, 17 sections |

## Common Mistakes

| Mistake | Correction |
|---|---|
| Repeating the abstract as "what the paper is about" | Reconstruct the argument chain independently |
| Accepting "no prior work addresses X" | Search for X. The claim is the hypothesis. |
| Citing papers from memory | Retrieve them, or tag `[UNVERIFIED]` |
| Treating every unexplored idea as a research gap | Unexplored is not the same as important. Classify it. |
| Judging journal fit from the scope page alone | Read recent comparable papers from that journal |
| Softening findings so the paper looks stronger | Hidden weaknesses resurface as reviewer rejections |
| Listing only writing and formatting issues | Method, evidence, and claim-support issues outrank prose |
| Starting fixes because the problem is obvious | Diagnosis only. Record the fix; do not apply it. |
| Suppressing conflicting evidence | Report the conflict and explain it |
| Inflating novelty to be encouraging | State what is novel and what is integration |

## Red Flags — Stop and Redo the Stage

- About to write a literature claim without a retrieved source
- About to edit any project file
- About to write "the paper correctly identifies a gap" without having searched
- Gap table has verdicts but no citations
- Report has fewer than 17 sections, or a section is silently empty
- Journal section cites only the journal's own scope statement
- Weakness audit found no Critical or Major issues in a pre-submission draft — re-audit against `references/weakness-audit.md`
