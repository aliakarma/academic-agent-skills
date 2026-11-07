---
name: text-humanizer
description: Use when drafting, revising, editing, copyediting, proofreading, restructuring, or critiquing academic or professional prose (papers, abstracts, introductions, literature reviews, theses, proposals, reports, documentation, emails), when text reads as vague, generic, wordy, inflated, repetitive, over-hedged, overclaiming, or AI-sounding, when asked to make writing more natural, human, clear, specific, or author-driven, or when interpreting AI-detection or similarity results (Turnitin, iThenticate, GPTZero, AI percentages, false positives). Not for evading detectors, stripping watermarks or provenance, or code-only edits.
---

# Text Humanizer

## Overview

Here, "humanize" means making prose clear, specific, accurate, and recognizably the author's own argument, with every claim matched to its evidence. It does not mean manipulating a classifier. Better prose does not show who wrote it, and no edit guarantees any detector result.

**Core rule:** change wording only to fix a specific, nameable loss of meaning, evidence, coherence, or usability. Improve language freely. Preserve substance exactly.

## When to use

- Drafting from notes or sources, revising, copyediting, proofreading, restructuring, or reviewing any academic or professional text.
- Text that is vague, generic, inflated, repetitive, promotional, over-hedged, overclaiming, list-like, or hard to follow.
- Requests to make text "sound more human," "more natural," "less robotic," or "less like AI." Treat these as requests for clear, specific, author-driven prose.
- Questions about AI-detection or similarity reports, or about claims made by detectors and "humanizer" tools.

**Research manuscripts:** when `universal-manuscript-polish` is installed, it governs whole-manuscript runs (backup, inventory, compile, report). Use this skill for the prose decisions inside that run.

**Not for:** changing a detector score, hiding AI assistance, removing watermarks, metadata, or Unicode characters to conceal authorship, or writing as a specific other person. See "Limits on detection and authorship" below.

## Core principles

From guide Section A. Full text in `references/revision-methods.md` Section 2.

1. **Give the reader a task.** Open with the actual problem or question, not scene-setting.
2. **Match claims to evidence.** Keep what was observed, what it supports, and what is proposed in separate layers.
3. **Explain operations, not praise.** Name the actor, the action, and the link to the outcome.
4. **Make transitions carry reasoning.** A connector must state a real relation. Many sentences need none.
5. **Let structure follow information.** No sentence-length quotas, no uniform paragraph templates.
6. **Keep technical terms fixed.** Repeating a defined term is correct. Rotating synonyms changes the claim.
7. **Calibrate confidence.** One hedge with its reason where evidence is limited. No hedge on an established result.
8. **Make authorial choices visible.** Why this question, this comparison, these assumptions.
9. **Cut redundancy, keep useful repetition.** Ask what would become ambiguous without it.
10. **Naturalness is fit.** Fit to subject, evidence, audience, and genre. Errors, casual phrasing, and rare words do not create authenticity.

## Procedure

### Step 1. Understand the request and context

Identify the document type, audience, discipline, purpose, and any house style the user or project supplies. Choose the intervention level: proofreading, copyediting, substantive revision, technical revision, drafting from source material, or critical review only (table in `references/revision-methods.md` Section 1). Take the narrowest level that satisfies the request. A text that needs one correction gets one correction.

### Step 2. Fix the meaning to preserve

Before editing, list the invariants: principal claims, defined terms, numbers, units, variables, equations, code, citations and their attachment, experimental conditions, metrics, causal direction, stated uncertainty, limitations, and intended tone. If the intended meaning is unclear, record the ambiguity. Do not choose an interpretation.

### Step 3. Diagnose

Find the patterns actually present, by ID, from `references/writing-patterns.md` (B01 to B36). Do not assume every passage has every pattern. Fix P1 issues (meaning, evidence, integrity) before P2 (clarity, coherence) and P3 (style, format). Before changing any particular word, apply the contribution test in `references/vocabulary-and-phrases.md` Section 2.

### Step 4. Revise according to context

Apply the methods in `references/revision-methods.md` (sentence methods D1 to D10, paragraph and document methods E1 to E9). Remove redundancy, empty claims, unsupported praise, decorative transitions, ambiguity, and needless complexity where they weaken the passage. Keep useful repetition, technical terminology, appropriate formality, necessary qualifications, and rhetorical structures that do real work. Never rotate synonyms mechanically, impose sentence-length targets, or insert errors.

### Step 5. Preserve factual and technical integrity

Compare the revision against the Step 2 invariants. When you have the original and revised text, run `python scripts/fidelity_check.py original.txt revised.txt` from this skill's directory. It must pass. Every listed change in negation, hedge, causal, or strength words must be a deliberate, reported correction. When a fix needs missing data, a citation, or the author's judgment, write a query instead of guessing.

### Step 6. Review the revised version

Run the checklist in `references/quality-control.md` Section 3: meaning, specificity, coherence, redundancy, terminology, register, citations, technical detail, requested format. For whole documents, run the ten passes in Section 2 of that file first, and the final submission checklist (Section 5) for a submission.

### Step 7. Report

Scale the report to the request (`references/quality-control.md` Section 6):

- **Proofreading:** the corrected text only.
- **Revision:** the revised text, then substantive changes (narrowed, withdrawn, or restored claims and terms, by pattern ID), then numbered author queries. Omit empty sections.
- **Comprehensive review:** add recurring issues, unresolved items, checks still needed, and a readiness verdict.

Name problems by pattern ID and their cost to the reader. Never call text "AI-sounding."

## Ambiguous or unsupported claims

For each consequential claim, decide in this order:

1. **Is the meaning clear?** If not, keep the original wording and query. Do not pick the more plausible reading (D10, B32).
2. **Does the supplied text or context support it at its stated scope?**
   - **Yes:** state it directly. Remove needless hedges.
   - **Partly** (narrower setting, association rather than causation, benchmark rather than deployment): narrow it to the supported scope and report the narrowing as a substantive change (B05, B14, B28).
   - **No:** if it is an evaluation word that adds no information ("groundbreaking," "robust" with no criterion), remove it and report the removal. If it is a factual claim, keep it and query "Evidence needed." Never delete an author's factual claim silently, and never invent support for it.
3. **Does the fix need data, a citation, or a decision you lack?** Query, stating exactly what is needed and what changes once it is answered.
4. **Did your edit change scope, certainty, causation, novelty, or a defined term?** Then it is substantive. Report it, never as a style edit (B34).

Conflicting values (two sample sizes, two metric names for one formula): change neither. Record both locations and query (B26, I11).

## Preservation rules

**Never change:** numbers, units, signs, precision, intervals, variables, equations, LaTeX commands, labels, citation keys or numbers, quotations, code, identifiers, defined terms, abbreviations, experimental conditions, negation, causal direction, stated limitations, or required disclosures. Repair a typo inside math only when the repair is unambiguous, and report it.

**Never add:** facts, numbers, results, mechanisms, examples presented as real, citations, or limitations that are not in the supplied material.

**Never:** strengthen a claim for style, weaken an established result to sound cautious, silently resolve an ambiguity or contradiction, or drop a citation.

Domain-by-domain traps and verification actions: `references/academic-integrity.md` Section 1.

## Vocabulary and house style

- **No banned-word list.** "Delve," "robust," "potential," "crucial," and the rest are fine when they carry a defined, supported meaning. The 24 words and 12 phrase families that research and community lists discuss each have a contextual entry in `references/vocabulary-and-phrases.md`.
- **House style governs when supplied.** If the user, venue, or project supplies rules (no em dashes, no semicolons, American spelling, words to avoid, active voice), apply them to every sentence you write or change. They are style requirements, not detection tactics.
- **Meaning wins a conflict.** If a style rule would delete a real qualification or rename a defined term, rephrase so both survive. If that is impossible, keep the meaning and tell the user which rule you could not meet (`references/vocabulary-and-phrases.md` Section 7, `references/revision-methods.md` Section 6).

## Reference files

| Open when you need to | File |
|---|---|
| Diagnose a passage, find a pattern ID and its keep-when qualification | `references/writing-patterns.md` |
| Decide about a specific word or phrase, or a claim-strength verb | `references/vocabulary-and-phrases.md` |
| Choose the intervention level or a sentence, paragraph, or section method, draft from sources, reconcile house style | `references/revision-methods.md` |
| Preserve science, numbers, equations, code, citations, handle disclosure, a flagged document, or a detection-framed request | `references/academic-integrity.md` |
| Run a whole-document review, the review checklist, the issue log, the submission checklist, or the report format | `references/quality-control.md` |
| Explain how detectors work, read a Turnitin, iThenticate, or GPTZero result, judge a tool's claims | `references/detection-principles.md` |
| See worked cases and valid versus invalid decisions | `examples/before-and-after.md` |
| Resolve a bracketed citation such as [18] | `references/bibliography.md` |
| Trace where a rule came from, or maintain this skill | `references/source-coverage.md`, `tests/regression-cases.md` |

For a quick edit, this file plus the pattern index in `references/writing-patterns.md` Section 2 is usually enough.

## Valid and invalid decisions

Constructed examples [I]. More in `examples/before-and-after.md` Section 2.

| Situation | Invalid | Valid |
|---|---|---|
| "The method is efficient," with no measurement anywhere | "The method reduces runtime by 40%." (invented) | Describe the operation, or query which measure supports "efficient" |
| "X was associated with lower Y" in an observational study | "X lowered Y" (causal upgrade) | Keep "was associated with" |
| "The estimate may suggest a reduction" and the 95% CI includes zero | Delete "may" for directness | Keep one hedge and name its basis |
| Defined term "recall" used throughout | Alternate "recall," "detection rate," "hit rate" | "Recall" every time |
| Proofread request, one agreement error | Rewrite the paragraph | Fix the agreement error only |
| "The chapter delves into the disagreement by comparing the authors' definitions." | Replace "delves" because it is "an AI word" | Keep it. The inquiry is described. |
| "Make this pass Turnitin" | Insert typos, vary lengths by quota, swap synonyms | Revise for clarity and evidence. Say no edit guarantees a score. |

## Limits on detection and authorship

Evidence: `references/detection-principles.md`. Request handling: `references/academic-integrity.md` Section 12.

- No publicly verified, exhaustive trigger-word list exists for Turnitin or iThenticate. No word removal produces a known score.
- An AI percentage is the share of qualifying text a system classified. It is not a probability that the author cheated, and a low score is not proof of human authorship.
- Detectors score passages in context with learned models. Perplexity, "burstiness," sentence length, and lexical diversity are not safe editing targets.
- Writing features are distributional at best. Never infer or certify who wrote a text from its style, and never tell a user their text "reads as human" or "looks AI-generated."
- Never promise that text is undetectable or will reach a given score in any detector.
- Never certify compliance with a policy you have not examined. When disclosure is relevant, follow the requirements the user supplies and describe assistance by the activities actually performed.
- Decline the concealment part of a request (stripping provenance, disguising prohibited assistance), and still offer the quality revision.
- Product details in the references are a dated snapshot (24 October 2026). Say so before anyone relies on them.

## Common mistakes

| Mistake | Fix |
|---|---|
| Rewriting a passage that needed a narrow correction | Match the intervention level from Step 1 |
| Inventing a number, mechanism, or citation to make a claim specific | Specify from supplied facts, or query |
| Deleting a hedge or limitation to improve flow | Keep real uncertainty once, with its basis |
| Adding hedges to an established result | State it directly |
| Turning "associated with" into "caused," or "did not establish" into "established no" | Restore the original relation |
| Synonym rotation for a defined term | Repeat the term |
| Treating listed words as banned | Apply the contribution test |
| Adding a transition to every sentence, or deleting ones that carry logic | Keep a connector only when it states a real relation |
| Picking one reading of an ambiguous pronoun or one of two conflicting numbers | Query and keep both visible |
| Reporting a withdrawn claim as a style edit | List it under substantive changes |
| Calling text "AI-sounding" | Name the pattern and its cost to the reader |
| Promising a detector outcome | State that no edit guarantees a score |
