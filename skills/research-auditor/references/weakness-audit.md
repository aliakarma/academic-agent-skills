# Full Weakness and Risk Audit

Work every checkpoint. Record each as **Pass**, **Critical**, **Major**, or **Minor**, with the file and location as evidence. Checkpoints that do not apply are marked N/A with a reason — not skipped silently.

For every Critical and Major finding, write four parts:

**What is wrong → Why it matters → Evidence (file, section, line) → How it should be improved.**

A finding without a proposed fix is an observation, not an audit finding.

## Severity Rules

| Severity | Test |
|---|---|
| **Critical** | A competent reviewer could reject on this alone, or it invalidates a central claim |
| **Major** | Substantially weakens the paper; likely to trigger major revision |
| **Minor** | Should be corrected but will not by itself change the outcome |

Severity comes from consequence, not from how hard the fix is. An easily fixed missing ethics statement can still be Critical.

## Foundation

1. **Research problem and motivation** — Is the problem clearly defined, and does it matter to someone beyond the authors?
2. **Gap justification** — Is the gap supported by cited evidence, and does it survive the verification in `gap-verification.md`?
3. **Research questions** — Are they explicit, answerable, and actually answered by the work performed?
4. **Novelty** — Is the claimed novelty genuine, or is it integration, extension, or application presented as new?

## Literature

5. **Literature review** — Current, balanced, and representative, or padded and one-sided?
6. **Related work** — Are the closest competing approaches present and fairly characterized? Missing rivals are a Critical risk.
7. **Citation support** — Does each cited source actually support the statement attached to it? Spot-check the load-bearing citations.
8. **References** — Complete, correctly formatted, resolvable, no broken DOIs, no phantom entries, no excessive self-citation.

## Method and Rigor

9. **Methodology** — Sufficiently described to be understood and repeated? Appropriate to the research questions?
10. **Theoretical / analytical rigor** — Are derivations, proofs, and formal claims correct and complete?
11. **Assumptions** — Stated explicitly, justified, and tested for sensitivity? Unstated assumptions are the most common hidden Critical.
12. **Dataset and data quality** — Provenance, size, representativeness, preprocessing, class balance, leakage between splits.
13. **Experimental design** — Controls, splits, randomization, repetition, hyperparameter selection protocol.
14. **Baselines** — Are they current, strong, and fairly tuned? Weak or outdated baselines undermine every comparative claim.
15. **Evaluation metrics** — Appropriate to the task and the claims; not selectively reported.
16. **Statistical analysis** — Significance testing, variance across runs, confidence intervals, multiple-comparison handling, adequate sample size.
17. **Validation** — Does the validation design support the claims, or only demonstrate feasibility?
18. **Reproducibility** — Code, data, seeds, environment, hyperparameters, compute budget. Does a reader have what they need?
19. **Ablation and sensitivity analysis** — Is each component's contribution isolated? Are results stable under parameter variation?
20. **Generalizability** — Do the conclusions hold beyond the tested setting, and does the paper claim more than the evidence permits?

## Claims and Consistency

21. **Logical consistency** — Does each conclusion follow from its stated evidence?
22. **Internal contradictions** — Do numbers, claims, and statements agree across abstract, body, tables, figures, and conclusions? Cross-check every reported number against its source table.
23. **Overclaiming** — Language stronger than the evidence: "proves", "guarantees", "significantly outperforms" without a test, "real-time" without latency measurement.
24. **Conclusions** — Supported, proportionate, and responsive to the research questions.
25. **Abstract and title alignment** — Do they describe what the paper actually delivers?
26. **Limitations** — Present, honest, and covering the real weaknesses rather than decorative ones.

## Presentation

27. **Figures and tables** — Readable, self-contained captions, correct units, consistent with the text, no misleading axes, referenced in order, licensed for reuse.
28. **Structure and writing** — Does the argument flow, and is anything essential missing or buried?

## Compliance

29. **Journal requirements** — Template, length, structure, mandatory statements, required checklists (see `journal-fit.md`).
30. **Ethics and research integrity** — Approvals, consent, data protection, dual-use considerations, conflicts of interest, authorship, prior publication and self-overlap, and any declaration of AI assistance the venue requires.

## Cross-Cutting Sweeps

Run these across the whole manuscript rather than per section:

- **Number trace** — every number in the abstract and conclusions traced back to the table or figure it comes from
- **Claim ledger** — every claim in the abstract and conclusions mapped to the specific evidence supporting it, tagged strong / weak / unsupported
- **Terminology drift** — the same concept named consistently throughout
- **Figure-text agreement** — each figure's message matches what the text says about it
- **Citation spot-check** — a sample of load-bearing citations opened and confirmed to say what is claimed
