# Review Dimension Checklists

Detailed checklists for each of the 10 review dimensions. Read the relevant sections based on manuscript type and review focus.

## Table of Contents

1. [Novelty & Contribution](#1-novelty--contribution)
2. [Technical Soundness](#2-technical-soundness)
3. [Cross-Document Consistency](#3-cross-document-consistency)
4. [Experimental Rigor & Reproducibility](#4-experimental-rigor--reproducibility)
5. [Literature & Positioning](#5-literature--positioning)
6. [Writing & Structure](#6-writing--structure)
7. [Scientific & Ethical Integrity](#7-scientific--ethical-integrity)
8. [LaTeX & Presentation](#8-latex--presentation)
9. [Claim Strength Audit](#9-claim-strength-audit)
10. [Fatal Flaw Detection](#10-fatal-flaw-detection)

---

## 1. Novelty & Contribution

### What to determine

- Is the contribution genuinely novel, or incremental?
- What type of novelty? (theoretical / architectural / methodological / empirical / application-level)
- Does the work substantially advance the field?
- Do claims exceed actual contribution?

### Red flags to check

- Repackaged existing methods under new terminology
- Weak differentiation from prior work (surface-level changes only)
- Overclaimed novelty ("first to..." without adequate literature search)
- Incremental engineering presented as innovation (combining known components without insight)
- Missing comparison to the most relevant prior work
- "Novelty by application domain" only — applying known method X to domain Y without methodological insight

### Calibration

Compare contribution strength explicitly against:
- Recent SOTA approaches in the same problem space
- Recent Q1 publications on similar topics
- Standards at the target venue

State concretely: what is truly novel, what resembles prior work, and what is integration engineering.

---

## 2. Technical Soundness

### What to evaluate

- Mathematical correctness of derivations and proofs
- Logical consistency of arguments throughout the paper
- Algorithmic validity — does the described algorithm achieve what is claimed?
- Realism of assumptions — are simplifying assumptions reasonable for the domain?
- Methodological rigor — is the method sound and well-justified?
- Complexity analysis — time/space complexity, scaling behavior
- Implementation clarity — could someone reproduce this from the description?
- Theoretical justification — is the method motivated by theory or just intuition?

### What to flag

- Unsupported derivations (steps skipped without justification)
- Hidden assumptions (conditions required but not stated)
- Unjustified design choices ("we use X" without explaining why X over Y)
- Invalid comparisons (comparing against inappropriate baselines or metrics)
- Weak theoretical grounding (method works "because it does" with no analysis)
- Ambiguous methodology (multiple interpretations of described procedure)
- Unverifiable implementation details (critical details omitted)
- Circular reasoning in arguments

---

## 3. Cross-Document Consistency

This dimension catches errors authors miss across drafts and revisions. It is high-value and often overlooked.

### Numerical consistency

Cross-check ALL numbers across: abstract, introduction, methods, results, discussion, conclusion, tables, figures.

Flag:
- Conflicting percentages (e.g., "12% improvement" in abstract vs. "11.8%" in results)
- Inconsistent dataset counts (e.g., "10,000 samples" in methods vs. "9,847" in table)
- Metric mismatches (different metrics or scales used inconsistently)
- Contradictory claims (e.g., "outperforms all baselines" but table shows losses)
- Impossible statistics (percentages > 100%, negative counts)
- Rounding inconsistencies that change interpretation

### Figure & table forensics

Verify:
- Every figure/table is cited in text before it appears
- Captions accurately describe content
- Axes are labeled with clear units
- Values in figures match values in text and tables
- Trends claimed in text are supported by the visualization
- No misleading scaling (truncated axes, non-linear scales without disclosure)
- No duplicated visuals across figures
- All figures are readable at print resolution
- Consistent notation across figures
- Legends are present and complete
- Visualizations are not cherry-picked to show only favorable results

### Cross-reference integrity

Check:
- All equation references resolve correctly
- All figure references point to the right figure
- All table references are correct
- Section references are accurate
- Bibliography entries are complete and correctly cited
- No duplicate labels
- No missing labels
- No broken references (??  in LaTeX output)

---

## 4. Experimental Rigor & Reproducibility

### Baseline fairness

- Same data splits used for all methods?
- Equivalent training budgets (epochs, compute time)?
- Hyperparameters tuned with comparable effort for all methods?
- Evaluation protocol identical across all compared methods?
- Baselines properly tuned (not strawman implementations)?
- Are baselines from official codebases, or reimplemented? If reimplemented, is performance validated?

### Statistical reliability

- Confidence intervals reported?
- Variance / standard deviation across runs?
- Statistical significance tests applied?
- Multiple random seeds used? How many?
- Robustness tested across different conditions?
- Sensitivity analysis for key hyperparameters?
- Ablation studies covering key components?

### Reproducibility

- Hardware disclosed (GPU model, memory, cluster size)?
- Software versions listed (framework, libraries)?
- Code availability (repo link, or promised upon acceptance)?
- Dataset accessibility (public, or restricted with access instructions)?
- Hyperparameter values fully specified?
- Random seeds reported?
- Training details sufficient for reproduction (batch size, learning rate schedule, etc.)?

### AI/ML-specific checks

- Train/test data contamination? (are test examples present in training data?)
- Benchmark memorization? (model trained on data from the benchmark's domain)
- Prompt leakage? (for LLM-based methods: test prompts or answers in training)
- Overfitting indicators? (perfect train accuracy, large train-test gap)
- Cherry-picked datasets? (only favorable benchmarks reported)
- Unfair baseline comparisons? (old baselines, different scales, smaller models)
- Suspiciously perfect results? (e.g., 99.9% accuracy on hard tasks)
- Compute budget disclosure?

---

## 5. Literature & Positioning

### What to evaluate

- Are foundational papers in the area cited?
- Is recent literature (last 2–3 years) adequately covered?
- Are citations relevant (not citation padding)?
- Is the paper properly positioned relative to related work?
- Do authors show understanding of how the field has evolved?

### What to flag

- Missing foundational papers (seminal works in the area)
- Missing recent SOTA (competing methods published in last 1–2 years)
- Citation padding (irrelevant references inflating the bibliography)
- Weak comparative analysis ("X did Y" without explaining the relationship to this work)
- Outdated references as primary baselines (>5 years old when newer work exists)
- Mischaracterized prior work (incorrect descriptions of what others did)
- Self-citation bias (disproportionate citation of authors' own work)
- Uncited directly relevant concurrent work

---

## 6. Writing & Structure

### What to evaluate

- Logical flow from section to section
- Clarity of technical descriptions
- Precision of language (no ambiguous pronouns, vague quantifiers)
- Section organization (standard and logical for the paper type)
- Readability for the target audience
- Professional presentation quality

### What to flag

- Ambiguous statements that could be interpreted multiple ways
- Weak transitions between sections
- Redundancy (same point made in multiple places)
- Repetitive phrasing
- Weak motivation (why should the reader care?)
- Notation inconsistencies (same symbol meaning different things)
- Grammar problems affecting comprehension
- Overly long sentences that obscure meaning
- Missing definitions for key terms
- Jargon without explanation

### Standard

The manuscript should read like a polished Q1 publication. If it reads like a draft, flag this as a material weakness. Unclear writing is a technical problem because it prevents verification of claims.

---

## 7. Scientific & Ethical Integrity

### What to evaluate

- Credibility of all claims
- Realism of reported results
- Ethical implications of the work
- Transparency about limitations
- Reproducibility commitments

### What to flag

- Unrealistic claims (results too good for the problem difficulty)
- Unsupported conclusions (conclusions not following from evidence)
- Benchmark manipulation risk (metrics chosen to favor the proposed method)
- Data leakage concerns (test information available during training)
- Ethical risks (dual-use potential, fairness concerns, privacy issues)
- Missing limitations section or inadequate limitations
- Potential misuse of the method
- Undisclosed conflicts of interest
- Undisclosed funding sources

### Language guidance

Do not accuse misconduct. Use:
- "Please verify that..."
- "This pattern warrants clarification..."
- "Additional evidence would strengthen..."
- "The reviewers request confirmation that..."

---

## 8. LaTeX & Presentation

### What to inspect

- Equation formatting (numbered correctly, aligned, readable)
- Bibliography consistency (consistent author name format, complete entries)
- Citation formatting (matches venue style: numbered vs. author-year)
- Float placement (figures/tables near their first reference)
- Acronym consistency (defined on first use, used consistently)
- Symbol consistency (same symbol = same meaning throughout)
- Section hierarchy (logical nesting, not too deep)
- Figure quality (resolution, readability, professional appearance)
- Table formatting (clean, readable, not overly complex)
- No overfull/underfull hbox warnings creating ugly output

### Common problems

- Mixed citation styles
- Figures placed far from their references
- Tables breaking across pages poorly
- Missing or inconsistent units
- Unclear figure fonts (too small, wrong typeface)
- Color-only distinctions in figures (not accessible to colorblind readers)

---

## 9. Claim Strength Audit

### Classification scheme

For every major claim in the paper, assign one:

| Classification | Definition |
|---------------|-----------|
| **Fully Supported** | Direct evidence from experiments/theory, statistically significant, no contradictions |
| **Partially Supported** | Some evidence exists but incomplete, or evidence supports a weaker version of the claim |
| **Weakly Supported** | Minimal evidence, logical but not demonstrated |
| **Unsupported** | No evidence provided, or evidence is irrelevant to the claim |
| **Contradicted** | Available evidence contradicts the claim |

### What to flag specifically

- Exaggerated impact claims ("revolutionary", "paradigm-shifting" without evidence)
- Unsupported generalization ("works for all domains" tested on one)
- Speculative conclusions presented as findings
- Causation claimed without causal evidence (correlation ≠ causation)
- Superlatives without comparative evidence ("best", "first", "only")

---

## 10. Fatal Flaw Detection

### Possible fatal flaws

- Fundamentally invalid experimental design (no valid comparison possible)
- Severe data leakage making all results unreliable
- Irrecoverable reproducibility failure (method cannot be reproduced from description)
- Invalid statistical methodology (wrong tests, violated assumptions)
- Unsupported core conclusions (main claims not following from evidence)
- Non-comparable experiments (apples-to-oranges comparisons)
- Missing critical baselines (the obvious comparison everyone would ask for)
- Contradictory central results (tables/figures conflict with text)
- Ethical violations (undisclosed data sources, consent issues)

### Assessment protocol

If a fatal flaw is found:
1. Identify it explicitly with location reference
2. Explain why it is fatal (not just a weakness)
3. Determine if the work is salvageable at all
4. Classify: fixable revision issue vs. fundamentally broken methodology
5. If salvageable, outline what would need to change
