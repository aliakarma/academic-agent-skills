# MASTER_PAPER_ASSESSMENT.md — Structure and Section Contracts

Write the report to the project folder as `MASTER_PAPER_ASSESSMENT.md`. All 17 sections appear, in this order, with these headings. A section with nothing to report states that explicitly and says why — never omitted, never silently empty.

Apply the evidence tags from the skill (`[AUTHORS' CLAIM]`, `[VERIFIED]`, `[CONTRADICTED]`, `[UNVERIFIED]`, `[AUDITOR JUDGMENT]`) throughout. Cite sources for substantive literature and journal statements.

Open the file with a header block: manuscript title, target journal, files audited, date of audit, and date range of the literature search.

---

## 1. Executive Summary

The whole audit in one page, written so a reader who stops here still knows what to do. Include: what the paper is, the single most important finding of the audit, the gap verdict in one line, journal-fit verdict in one line, count of Critical / Major / Minor issues, and the top three actions. State the readiness verdict here, not only in Section 13.

## 2. What the Paper Really Is

The reconstructed paper, not the advertised one. What it actually does, what kind of contribution it actually makes, and where the paper's self-description and its content diverge. Name the contribution type plainly: new method, integration, application, extension, replication, framework, or system description.

## 3. Problem, Objectives, and Research Questions

Central problem and motivation. Objectives. Each research question, explicit or implied, with: what it is trying to establish, how the paper attempts to answer it, and whether that design can answer it. Flag questions that are posed but never answered, and answers given to questions never posed.

## 4. Paper's Claimed Contributions

Every claimed contribution as stated, each tagged `[AUTHORS' CLAIM]`, then assessed. Use a table: contribution, where claimed, what it actually is (novel / integration / extension / application / implementation), and the evidence offered for it. Do not inflate; do not deflate. State what genuinely is new.

## 5. Independent Research-Gap Validation

The centerpiece. One entry per gap, following `gap-verification.md`: gap statement, manuscript location, claimed gap type vs. actual gap type, verdict from the five, evidence with citations, challenging papers, remaining residue, searches performed.

Include the trigger-phrase audit table: every "first", "novel", "no studies", "existing approaches fail" in the manuscript, with its individual verdict.

Close with a plain statement of what gap the paper can actually defend.

## 6. Literature and Field Positioning

Current state of the field, major research directions, dominant methods and frameworks, important recent developments, and the major competing approaches. Then: what the field currently considers important, whether this paper addresses a meaningful current problem, and whether its novelty would be recognized by researchers in the field. Cite sources.

## 7. Closest Existing Studies and Differentiation

The closest 5-15 papers. For each: citation, what it does, and precisely how this manuscript differs — mechanism, scope, data, evaluation, or claim. State whether that difference constitutes a contribution or only a variation. Identify the single nearest paper and treat it as the paper's hardest comparison; if the manuscript does not cite it, that is a Critical finding.

## 8. Methodology and Evidence Assessment

Methodology, assumptions, datasets, experimental design, baselines, metrics, statistical treatment, validation, reproducibility, and ablation. Assess whether the evidence produced can support the claims made, independent of whether the results are favorable.

## 9. Major Findings and What They Actually Support

The paper's findings, each paired with what it genuinely establishes versus what the paper says it establishes. Use a claim ledger table: claim, location, supporting evidence, verdict (strongly supported / weakly supported / unsupported), and what would be needed to support it properly.

## 10. Full Weakness and Risk Audit

All findings from `weakness-audit.md`, grouped as **Critical**, **Major**, **Minor**. Each Critical and Major finding carries: what is wrong, why it matters, evidence with file and location, and how it should be improved. Include the cross-cutting sweep results (number trace, terminology drift, figure-text agreement, citation spot-check).

## 11. Target Journal Analysis

The journal, how it was identified, and its current official profile with URLs and access dates: scope, aims, article types, recent topics, methodological and novelty expectations, submission requirements, limits, required checklists. Summarize the recent comparable papers reviewed and what bar they reveal.

## 12. Journal-Fit Assessment

The seven-dimension fit assessment from `journal-fit.md`, each dimension justified by evidence. Name the binding constraint. Include the desk-rejection risk checklist. If fit is weak, name better-matched alternatives and what each would require.

## 13. Submission Readiness Assessment

Evidence-based, not impressionistic. Cover: what is already strong, what must be fixed before submission, what should improve but is not blocking, what will attract reviewer criticism, whether current evidence supports the claims, whether the contribution is sufficiently differentiated, and whether the journal is appropriate. State the estimated effort to reach submittable, and be specific about what "submittable" means for this paper.

## 14. Required Improvements Before Submission

Only blocking items. Numbered, each with: what to do, why it is blocking, which section or file it touches, what evidence or new work it requires, and how to verify it is resolved. This section is the work order.

## 15. Recommended Revision Priorities

Everything, blocking and non-blocking, ordered by impact per unit of effort. Table: priority, item, impact, effort, dependencies. Make sequencing explicit — say which items must precede others, especially where new experiments feed claims that appear in the abstract.

## 16. Final Master Assessment

The auditor's integrated judgment. What this paper is, what it can honestly claim, what it needs, where it should go, and the realistic outcome if submitted as-is versus after the required improvements. State residual uncertainty honestly, including anything tagged `[UNVERIFIED]` that could change the assessment.

## 17. Key References and Sources

Every source used in the audit, grouped: literature consulted for gap verification, closest-work papers, field-positioning sources, and journal and publisher pages with access dates. Mark any source that could not be retrieved and say what it was needed for. This section is what makes the audit checkable.
