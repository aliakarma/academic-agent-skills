---
name: repo-forensic-audit
description: >
  Forensic audit of research GitHub repositories for scientific integrity,
  reproducibility, and fraud detection. Combines Q1-level code review, ACM
  artifact evaluation, fraud fingerprint detection, and ML anti-pattern hunting.
  Use whenever the user wants to audit a research repo, check for fabricated
  results, verify reproducibility, detect hardcoded metrics or disconnected
  eval pipelines, or assess trustworthiness of code. Trigger on "audit this
  repo", "forensic audit", "check for fabrication", "is this repo legit",
  "reproducibility check", GitHub URLs with review requests, or pasted repo
  files for integrity checks. Also trigger for partial audits like "check the
  eval pipeline" or "look for hardcoded metrics". Do NOT trigger for
  manuscript peer review (use peer-review skill) or general code review
  without a scientific integrity angle.
---

# Repository Forensic Audit

A structured multi-phase protocol for auditing research repositories. The goal
is to determine whether a repo's results can be trusted, reproduced, and
published. Default posture: skepticism.

## Hard Constraints

These are non-negotiable throughout the entire audit:

- **No hallucination.** If a file is not listed or visible, it does not exist. Never infer the presence of files you haven't seen.
- **Assume incorrectness.** Every component is guilty until proven innocent. Do not give benefit of the doubt to code that could be fabricating results.
- **Trace every number.** Every quantitative claim must be traced back to a live computation in runnable code. Hardcoded values in result files do not count as verification.
- **Cite evidence.** Every claim in the review must reference a specific file, function, or line. Generic feedback without evidence is prohibited.
- **Admit uncertainty.** If you cannot determine something, say so explicitly. Uncertainty is a finding, not a weakness.

## Step 1 — Determine Audit Mode

Infer from the user's request, or ask if ambiguous:

| Mode | When to Use | What It Covers |
|------|------------|----------------|
| **Full Audit** | Default. Comprehensive integrity assessment | All 7 phases, full output report |
| **Quick Triage** | User wants a fast read on trustworthiness | Phase 0 (repo map + claim ledger) + Phase 1 (fraud fingerprints) only. Produces a GO / NO-GO / SUSPICIOUS verdict with key flags |
| **Targeted Audit** | User names specific concerns | Run only the relevant phases (e.g., "check the eval pipeline" → Phase 2 + Phase 4) |
| **Remediation Verification** | User has a previously audited repo with fixes applied | Re-run phases that previously flagged issues, verify fixes, produce delta report |

## Step 2 — Acquire Repository Contents

The repo can arrive in several ways. Adapt accordingly:

**GitHub URL provided:** Use `web_fetch` to retrieve the repository page. Then fetch the raw contents of key files: README, all Python scripts, config files, requirements.txt, and any evaluation/results files. Start with the repo root to get the file tree, then fetch individual files. Prioritize: README → training scripts → evaluation scripts → model definitions → config files → results files.

**Files uploaded:** Read from `/mnt/user-data/uploads/`. If a zip/tar is uploaded, extract it first. Build the file tree from the extracted contents.

**Files pasted in conversation:** Work directly from the pasted content. Note which files you have and which are missing.

In all cases, before proceeding, confirm what you have access to and flag what's missing. An incomplete view of the repo should be stated upfront — it limits audit depth.

## Step 3 — Phase 0: Mandatory Pre-Analysis

This phase MUST be completed before writing any evaluation. It produces two artifacts.

### 0A: Repository Map

List every file in the repository as a structured tree. For each file note:
- File path
- Inferred purpose (one sentence)
- Whether it is actually imported/called by any other file (or is dead code)

Flag immediately:
- Files referenced in README but absent from the repo
- Config files with no corresponding script that reads them
- Evaluation scripts that are never called by any runnable entry point
- Result files (.csv, .json, .pkl, figures) with no generation script
- Model checkpoint files with no training script that produces them
- Empty `__init__.py` files masking non-functional packages

### 0B: Claim Ledger

Extract EVERY quantitative claim from: README, paper PDF (if provided), docstrings, comments, and any results files. Fill this table:

| # | Claim | Value | Source location | Verified? | Evidence or gap |
|---|-------|-------|-----------------|-----------|-----------------|

A claim is "Verified" ONLY if you can trace the exact number to a live computation in runnable code. "Unverifiable" if the number appears only as a literal or in a results file with no generation path. "Suspicious" if the number appears hardcoded in evaluation code.

**Fabrication threshold:** If >30% of claims are unverifiable, flag as POTENTIAL FABRICATION and escalate this finding to the top of the report.

## Step 4 — Phase 1: Fraud Fingerprint Audit

Read `references/fraud-fingerprints.md` for the complete checklist of 14 fraud fingerprints to check. For each item, state: **PRESENT** / **ABSENT** / **UNCERTAIN** with file-level evidence.

The checklist covers: hardcoded metrics, constant model outputs, reverse-engineered evaluation fixtures, disconnected evaluation pipelines, unreachable training code, orphan result files, suspiciously perfect numbers, seed sensitivity concealment, test set contamination, label leakage, metric implementation bugs, fabricated datasets, phantom ablation studies, and mock/stub inference.

After completing the checklist, compute a fraud risk summary:
- 0 flags → LOW risk
- 1–3 flags → MEDIUM risk (may be engineering debt)
- 4–6 flags → HIGH risk (pattern suggests intentional manipulation)
- 7+ flags → CRITICAL risk (systematic fabrication likely)

## Step 5 — Phase 2: Pipeline Reconstruction

Reconstruct the exact execution pipeline:

```
[raw data] → [preprocessing] → [splits] → [training] → [evaluation] → [metrics]
```

For each arrow:
- Name the exact script and function responsible
- State whether it is runnable as written (check imports, paths, dependencies)
- Flag broken dependencies, missing imports, hardcoded paths, or placeholder code

Then answer these questions with evidence:

1. **Reproducibility**: Can someone clone this repo and reproduce the main result in < 2 hours? What is the exact command sequence?
2. **Determinism**: Are random seeds fixed at every stochastic operation (Python, NumPy, PyTorch/TF, CUDA)?
3. **Split integrity**: Is train/val/test split performed before any feature engineering or data transformation?
4. **Eval independence**: Is the evaluation script genuinely independent from training, or does it rely on artifacts that embed training-time information?
5. **Metric fidelity**: Do reported metrics match what the code would actually compute if run end-to-end?

## Step 6 — Phase 3: Statistical Validity Gate

The following are mandatory for a publishable result. Check each:

- [ ] Results over ≥3 independent seeds (with both mean and std dev)
- [ ] Confidence intervals on all primary metrics
- [ ] Statistical significance test vs. each baseline (t-test, Wilcoxon, bootstrap)
- [ ] Effect size reported (Cohen's d or equivalent)
- [ ] Ablation study with statistical significance per component
- [ ] No cherry-picked "best run" — all runs reported or fairly aggregated
- [ ] Compute budget documented (GPU hours, hardware spec)

If ALL are absent: flag as **CRITICAL** — the results have no statistical foundation.

## Step 7 — Phase 4: Cross-File Consistency Matrix

Verify these pairs agree. State **CONSISTENT** / **INCONSISTENT** with evidence:

| Pair | What to check |
|------|--------------|
| README metrics ↔ eval script output | Same metric names, formulas, and data splits? |
| Config hyperparams ↔ training script | Are config values actually loaded and used, or overridden inline? |
| Paper/README architecture ↔ model code | Layers, dimensions, activations match exactly? |
| Dataset description ↔ data loader | Claimed size, classes, features match what code actually loads? |
| requirements.txt ↔ import statements | All imports covered? Versions pinned and compatible? |
| Claimed baselines ↔ baseline implementations | Are baselines actually implemented and run, or are numbers copy-pasted from other papers? |
| Ablation descriptions ↔ ablation code | Does code for each ablation variant actually exist and differ meaningfully? |

## Step 8 — Phase 5: Evaluation Dimensions

Score each dimension 1–10 using these anchors:

| Score | Meaning |
|-------|---------|
| 9–10 | Exemplary. Among the best research repos. |
| 7–8 | Strong. Publishable with minor fixes. |
| 5–6 | Borderline. Notable gaps but salvageable. |
| 3–4 | Below threshold. Significant flaws. |
| 1–2 | Fundamentally broken or fabricated. |

For any score ≤ 6, a corresponding CRITICAL or MODERATE issue entry is mandatory.

**Dimensions:**

1. **Reproducibility** — Environment recreation, dependency pinning, one-command entry point, determinism enforcement
2. **Experimental Validity** — Dataset realism, leakage absence, metric appropriateness for class distribution, calibration
3. **Model & Algorithm Correctness** — Loss function correctness, gradient flow, label encoding consistency, imbalance handling
4. **System Design Realism** — Architectural claims validated, compute/memory/latency constraints stated, generalization beyond toy scenarios
5. **Baselines & Comparisons** — Strong contemporary baselines, equal hyperparameter tuning, SOTA references from same benchmark
6. **Code Quality** — Modularity, readability, no unexplained magic numbers, error handling
7. **Logging & Observability** — Training curves logged, run reproducibility, debuggability
8. **Robustness & Failure Modes** — Distribution shift testing, adversarial/noisy inputs, graceful degradation
9. **Claim–Implementation Alignment** — Every abstract claim has a code path, numbers traceable to eval runs

## Step 9 — Phase 6: Silent Bug Hunt

Read `references/silent-bugs.md` for the full checklist of ML anti-patterns to hunt. Report **FOUND** / **NOT FOUND** with file and line evidence for each.

Covers: off-by-one in sequence modeling, sklearn fit-before-split, DataFrame index leakage, train metrics labeled as test, missing class weights, double softmax, augmentation on val/test, LR scheduler misuse, and additional patterns for agentic AI, RL, and federated learning repos.

## Step 10 — Domain-Specific Checks (if applicable)

If the repository falls into one of these domains, read `references/domain-checks.md` for additional targeted checks:

- **Agentic AI / LLM-based systems** — agent loop execution, tool-calling verification, prompt/response fabrication
- **Reinforcement Learning** — reward shaping validity, environment interaction, policy evaluation
- **Federated Learning** — aggregation correctness, client simulation, privacy claims
- **Digital Twin / Simulation** — simulation fidelity, real-world mapping, synthetic data realism

## Output Format

Deliver the audit as a Markdown file saved to `/mnt/user-data/outputs/`. Use the template in `references/output-template.md` for the exact structure.

The output must contain these sections in order:

1. **Overall Verdict** — Score X/10, Decision (Reject / Major Revision / Minor Revision / Accept), 3–5 evidence-backed sentences
2. **Critical Issues** — Rejection-level flaws with evidence, mechanism, and exact fix
3. **Moderate Issues** — Significant but fixable, with file-level fix guidance
4. **Minor Issues** — Bullet list, each with file + specific change
5. **Missing Experiments** — What to run, how, why, and what sound vs. suspicious results look like
6. **Action Plan** — Prioritized fix roadmap ordered by dependency
7. **Final Scorecard** — All 9 dimensions + statistical validity + overall
8. **Fraud Risk Assessment** — LOW / MEDIUM / HIGH / CRITICAL with summary of triggered fingerprints

For **Quick Triage** mode: produce only the Overall Verdict + Fraud Risk Assessment + top 3 flags.

## Core Rules

- Prioritize integrity over diplomacy. If results appear fabricated, say so directly with evidence.
- Distinguish innocent engineering debt (sloppy but honest) from deliberate result manipulation (systematic fabrication patterns). State which you believe is more likely and why.
- Never recommend acceptance of a repo with unresolved CRITICAL fraud fingerprints.
- If the repo is clean, say so clearly — false accusations are also harmful.
- The audit report must be self-contained: a reader unfamiliar with the repo should understand every finding from the report alone.
