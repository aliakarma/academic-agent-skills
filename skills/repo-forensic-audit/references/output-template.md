# Audit Report Output Template

Use this exact structure for the Full Audit output. Save the final report as a Markdown file.

---

```markdown
# 🧠 OVERALL VERDICT

**Score:** X/10
**Decision:** Reject | Major Revision | Minor Revision | Accept

[3–5 sentences. Each sentence must make a specific, evidence-backed claim.
The first sentence must name the single most critical flaw, or confirm that
none was found. Do not write generic summaries.]

---

# 📋 PHASE 0 — REPOSITORY MAP

## File Tree

[Structured tree of all files with purpose and import status]

## Dead Code / Orphan Files

[List files that are never imported or called]

## Claim Ledger

| # | Claim | Value | Source location | Verified? | Evidence or gap |
|---|-------|-------|-----------------|-----------|-----------------|

**Fabrication threshold:** X/Y claims unverifiable (Z%).
[If >30%: FLAG AS POTENTIAL FABRICATION]

---

# 🔍 PHASE 1 — FRAUD FINGERPRINT AUDIT

| # | Fingerprint | Status | Evidence |
|---|-------------|--------|----------|
| 1 | Hardcoded metrics | PRESENT/ABSENT/UNCERTAIN | [file:line or explanation] |
| 2 | Constant model outputs | ... | ... |
| 3 | Reverse-engineered fixtures | ... | ... |
| 4 | Disconnected eval pipeline | ... | ... |
| 5 | Unreachable training code | ... | ... |
| 6 | Orphan result files | ... | ... |
| 7 | Suspiciously perfect numbers | ... | ... |
| 8 | Seed sensitivity concealment | ... | ... |
| 9 | Test set contamination | ... | ... |
| 10 | Label leakage | ... | ... |
| 11 | Metric implementation bugs | ... | ... |
| 12 | Fabricated dataset | ... | ... |
| 13 | Phantom ablation studies | ... | ... |
| 14 | Mock/stub inference | ... | ... |

**Flags triggered:** N/14
**Fraud risk level:** LOW / MEDIUM / HIGH / CRITICAL

---

# 🔬 PHASE 2 — PIPELINE RECONSTRUCTION

## Execution Pipeline

```
[raw data] → [preprocessing] → [splits] → [training] → [evaluation] → [metrics]
   ↑              ↑                ↑           ↑              ↑             ↑
 script/fn     script/fn       script/fn   script/fn      script/fn    script/fn
 runnable?     runnable?       runnable?   runnable?      runnable?    runnable?
```

## Pipeline Questions

| # | Question | Answer | Evidence |
|---|----------|--------|----------|
| Q1 | Reproducible in <2h? | Yes/No | [commands or blockers] |
| Q2 | Seeds fixed everywhere? | Yes/No | [which seeds set, which missing] |
| Q3 | Split before feature eng? | Yes/No | [code path] |
| Q4 | Eval independent from train? | Yes/No | [shared artifacts] |
| Q5 | Reported metrics match code? | Yes/No | [discrepancies] |

---

# 🧪 PHASE 3 — STATISTICAL VALIDITY GATE

| Requirement | Present? | Evidence |
|-------------|----------|----------|
| ≥3 seeds with mean + std | | |
| Confidence intervals | | |
| Significance tests vs baselines | | |
| Effect size | | |
| Ablation with significance | | |
| No cherry-picking | | |
| Compute budget documented | | |

**Verdict:** [If all absent: CRITICAL — no statistical foundation]

---

# 🔗 PHASE 4 — CROSS-FILE CONSISTENCY MATRIX

| Pair | Status | Evidence |
|------|--------|----------|
| README metrics ↔ eval script | CONSISTENT/INCONSISTENT | |
| Config hyperparams ↔ train script | CONSISTENT/INCONSISTENT | |
| Architecture description ↔ model code | CONSISTENT/INCONSISTENT | |
| Dataset description ↔ data loader | CONSISTENT/INCONSISTENT | |
| requirements.txt ↔ imports | CONSISTENT/INCONSISTENT | |
| Baseline descriptions ↔ baseline code | CONSISTENT/INCONSISTENT | |
| Ablation descriptions ↔ ablation code | CONSISTENT/INCONSISTENT | |

---

# 🚨 CRITICAL ISSUES (rejection-level)

## Issue 1: [Short title]

- **Problem**: [One precise sentence]
- **Evidence**: [`file.py`, line XX — paste relevant snippet]
- **Why it invalidates results**: [Mechanism of failure]
- **Exact fix**:
  ```python
  # BEFORE (file.py, line XX)
  [current broken code]

  # AFTER
  [corrected code]
  ```

## Issue 2: ...

---

# ⚠️ MODERATE ISSUES

## Issue 1: [Short title]

- **Problem**: [One precise sentence]
- **Evidence**: [`file.py`, line XX]
- **Impact**: [What this affects]
- **Fix**: [File-level guidance, no code snippet required]

---

# 🟢 MINOR ISSUES

- `file.py`: [specific change]
- `config.yaml`: [specific change]
- ...

---

# 🔬 MISSING EXPERIMENTS

For each:

### Experiment 1: [Title]

- **What**: [Exactly what to run]
- **How**: [Script name or pseudocode, datasets, hyperparams]
- **Why**: [What scientific question it answers]
- **Expected outcome**: [What a sound result looks like vs. a suspicious one]

---

# 🛠️ ACTION PLAN (prioritized fix roadmap)

Order by dependency: fix first → blocks everything else.

### Step 1 — [Title] (Est. effort: Xh)
- **Files**: `file1.py`, `config.yaml`
- **Changes**: [Specific implementation-level description]
- **Validates**: [Which claim or experiment this unblocks]

### Step 2 — ...

---

# 📊 FINAL SCORECARD

| Dimension | Score | Key reason (one sentence) |
|-----------|-------|---------------------------|
| Reproducibility | /10 | |
| Experimental validity | /10 | |
| Model/algorithm correctness | /10 | |
| System design realism | /10 | |
| Baselines & comparisons | /10 | |
| Code quality | /10 | |
| Logging & observability | /10 | |
| Robustness | /10 | |
| Claim–implementation alignment | /10 | |
| Statistical validity | /10 | |
| **Overall** | **/10** | |

---

# ⚖️ FRAUD RISK ASSESSMENT

**Risk level:** LOW / MEDIUM / HIGH / CRITICAL

[Summarize which fraud fingerprints were triggered. State whether the
combination suggests innocent engineering debt or deliberate result
manipulation. Be direct — this section is non-negotiable.]

---

# 🐛 SILENT BUG HUNT RESULTS

| # | Anti-pattern | Status | Evidence |
|---|-------------|--------|----------|
| 1 | Off-by-one in sequences | FOUND/NOT FOUND | |
| 2 | sklearn fit before split | FOUND/NOT FOUND | |
| ... | ... | ... | ... |

[Include domain-specific anti-patterns if applicable]
```

---

## Quick Triage Output Template

For Quick Triage mode, produce only:

```markdown
# 🧠 QUICK TRIAGE VERDICT

**Decision:** GO / NO-GO / SUSPICIOUS
**Confidence:** High / Medium / Low

[2–3 sentences with the most important findings]

## Top Flags

1. [Most critical finding with evidence]
2. [Second most critical]
3. [Third most critical]

## Fraud Risk: LOW / MEDIUM / HIGH / CRITICAL

[One paragraph summary]

## Recommendation

[What to do next: proceed to full audit, fix specific issues, or reject]
```
