# Regression cases

Eight behavioral cases for checking this skill after any edit. Each case gives the input, the intervention level, what a passing revision must do, the failure signals to look for, and the result of the last recorded run.

**Success criterion.** Quality, fidelity, and usefulness of the revision. Never a detector score.

**How to run.** Give each input to an agent with this skill loaded and the stated request. Save the input and the agent's revised text to files and run `python scripts/fidelity_check.py input revised` from the skill directory. Then read the revision against the pass criteria. A case passes only when the hard checks pass, every flagged word change is a reported substantive correction, and every pass criterion holds.

**Last run.** 24 October 2026, by the session that built the skill, which applied the skill's procedure itself. This verifies that the instructions produce correct revisions when followed. It does not verify how a fresh agent with no prior context interprets the skill. A cold-start run by a separate agent is still pending.

All inputs are constructed [I]. Their facts belong to the test scenario only.

---

## T1. Vague academic introduction

**Request:** "Make this introduction sound more natural."

**Input:**
> In today's rapidly evolving digital landscape, cybersecurity has become more crucial than ever. Organizations across the globe face an intricate web of ever-growing threats, and robust solutions are essential. This paper examines phishing emails sent to staff at one university between January and June 2025 and classifies them by lure type.

**Pass criteria:**
- Opens with the study's actual task (B01).
- Removes the unsupported importance claims (B02, B08) and reports the removal.
- Keeps "one university," "January and June 2025," and "lure type" exactly.
- Invents no prevalence statistic, threat figure, or citation to replace the opening.
- Offers a query for verified motivating evidence.
- Makes no claim about detectors or authorship.

**Failure signals:** an invented statistic ("Phishing accounts for 90% of breaches"), a new uncited motivation, a reworded but still generic opening ("Cyber threats are increasing worldwide").

**Last-run revision:**
> This paper examines phishing emails sent to staff at one university between January and June 2025 and classifies them by lure type.

- **Substantive change:** removed the two opening sentences (B01, B02). They asserted importance without evidence.
- **Q1:** If you have a sourced figure on phishing volume or impact at this university or in higher education, one sentence of that evidence can motivate the study before this sentence.
- **Fidelity:** PASS (numbers 1). No flagged word changes.
- **Verdict:** PASS.

---

## T2. Redundant transitions and repetitive conclusions

**Request:** "Tighten this paragraph."

**Input:**
> Furthermore, the survey was distributed to 412 nurses. Moreover, 287 responses were received. Additionally, the response rate was 69.7%. These findings are highly important and clearly demonstrate the promise of the approach. In conclusion, the survey results demonstrate the promise of the approach.

**Pass criteria:**
- Removes the decorative connectors (B03).
- Removes the empty reinforcement and the repeated verdict (B11, B12, B17).
- Keeps 412, 287, and 69.7% exactly. (287/412 = 69.66%, so the rate is internally consistent.)
- Does not invent what "the approach" is or what result shows promise.
- Queries the missing referent and evidence.

**Failure signals:** a new claim about what the results show, a changed number, a rounded rate, or a kept "promise" verdict.

**Last-run revision:**
> The survey was distributed to 412 nurses, and 287 responses were received (response rate 69.7%).

- **Substantive change:** removed two sentences asserting that the results demonstrate promise (B11, B12). The passage states no result that supports promise.
- **Q1:** "The approach" has no referent here, and a response rate alone does not show promise. Needed: which approach, and which result supports the claim. Effect: a sentence stating that result can replace the removed verdict.
- **Fidelity:** PASS (numbers 3). REVIEW: "demonstrate" removed twice, which is the reported withdrawal.
- **Verdict:** PASS.

---

## T3. Technical paragraph with defined terms

**Request:** "Copyedit this methods paragraph."

**Input:**
> We define a session as a sequence of HTTP requests from one client IP address with no gap longer than 30 minutes. Each session is labeled benign or malicious by two analysts. These visits are then grouped by user agent, and each browsing episode is assigned to one of k = 8 clusters. Session-level F1 is reported in Table 4.

**Pass criteria:**
- Restores the defined term "session" where "visits" and "browsing episode" drift from it (B22, B29), and reports the assumption.
- Introduces no new synonym for "session."
- Keeps 30 minutes, k = 8, F1, Table 4, and "two analysts" exactly.
- Leaves correct sentences unchanged (copyedit level, no voice rewrites for their own sake).
- Queries whether the drifting terms were meant to be the same unit.

**Failure signals:** a new synonym ("connection," "trace"), a changed value, the definition rewritten, or silent assumption of identity.

**Last-run revision:**
> We define a session as a sequence of HTTP requests from one client IP address with no gap longer than 30 minutes. Each session is labeled benign or malicious by two analysts. These sessions are then grouped by user agent, and each session is assigned to one of k = 8 clusters. Session-level F1 is reported in Table 4.

- **Substantive change:** replaced "visits" and "browsing episode" with the defined term "session" (B22). This assumes both words referred to the defined session.
- **Q1:** Confirm that "visits" and "browsing episode" meant the defined session. If either is a different unit (for example, a single page load), define it and the original word can be restored.
- **Fidelity:** PASS (numbers 4). No flagged word changes.
- **Verdict:** PASS.

---

## T4. A scientific claim that exceeds the evidence

**Request:** "Improve this sentence for the abstract."

**Input:**
> Our detector reduced false alarms by 23% on the CICIDS2017 test split, proving that it will eliminate alert fatigue in real-world security operations centers.

**Pass criteria:**
- Keeps "23%" and "CICIDS2017 test split" exactly.
- Withdraws "proving," "will eliminate," and the real-world generalization (B05, B14), and reports the narrowing as substantive.
- Does not assert an untested fact as fact (for example, "the detector was never deployed").
- Queries the comparator and whether 23% is relative or in percentage points.
- Offers to restore a deployment claim if a deployment evaluation exists.

**Failure signals:** a hedged version of the same overclaim ("may substantially reduce alert fatigue in practice"), an invented baseline, or a deleted number.

**Last-run revision:**
> Our detector reduced false alarms by 23% on the CICIDS2017 test split. This result does not establish an effect on alert fatigue in operational security operations centers.

- **Substantive change:** narrowed the claim from operational proof to the evaluated test split (B05, B14).
- **Q1:** 23% relative to which baseline, and is it a relative reduction or percentage points? Effect: the sentence can name the comparison.
- **Q2:** If the detector was evaluated in a live security operations center, cite that evaluation and the claim can be restored at its tested scope.
- **Fidelity:** PASS (numbers 2). REVIEW: "proving" removed, "not" and "establish" added, which together are the reported narrowing.
- **Verdict:** PASS.

---

## T5. A literature-review paragraph that lists sources without synthesis

**Request:** "Revise this related-work paragraph."

**Input:**
> Smith et al. [12] used a convolutional neural network for malware detection. Lee and Park [15] applied a transformer to the same task. Gomez [18] proposed a graph neural network. All of these studies provide valuable insights and show that deep learning is the best approach for malware detection.

**Pass criteria:**
- Synthesizes by a shared dimension present in the input (architecture) (E2).
- Keeps [12], [15], and [18] attached to the right authors and works.
- Removes "valuable insights" (B16) and withdraws "deep learning is the best approach," which no supplied comparison supports (B10, B05).
- Invents no dataset, metric, or result for any study.
- Queries for the details needed for a real comparison, and flags that the input does not state Gomez's task.

**Failure signals:** an invented result ("Lee and Park reported 97% accuracy"), a citation moved to a different claim, a dropped author name or citation, or a softened but kept superiority claim.

**Last-run revision:**
> Prior neural approaches to malware detection use three architectures: Smith et al. [12] used a convolutional neural network, Lee and Park [15] a transformer, and Gomez [18] a graph neural network. Establishing which approach performs best would require results on a shared dataset and metric.

- **Substantive change:** withdrew the claim that deep learning is the best approach (B10). The paragraph supplies no comparison.
- **Q1:** To synthesize further, supply each study's dataset, metric, and main result, or cite a study that compares these architectures directly.
- **Q2:** The input does not say that Gomez [18] applied the graph neural network to malware detection. Confirm, since the revision groups it with the other two.
- **Fidelity:** PASS (numbers 3, citations 3). REVIEW: "all" removed, "would" added (a conditional about what a comparison requires).
- **Verdict:** PASS.

---

## T6. A fluent rewrite that could change causation or uncertainty

**Request:** "Make this results passage read more smoothly."

**Input:**
> Patients who used the app at least three times per week had lower HbA1c at 6 months than less frequent users (mean difference −0.4%, 95% CI −0.9 to 0.1). App use may be associated with improved glycemic control, although adherence was self-reported.

**Pass criteria:**
- Keeps the comparison groups, 6 months, the Unicode minus signs, −0.4%, and the full interval exactly.
- Keeps "may be associated" and the self-report limitation. Adds no causal verb ("lowered," "improved," "reduced").
- May state that the interval includes no difference, since that follows from the supplied numbers, and reports it.
- Queries whether −0.4% is in percentage points.

**Failure signals:** "Frequent app use lowered HbA1c by 0.4%," a dropped minus sign, a dropped interval, or a deleted hedge.

**Last-run revision:**
> Patients who used the app at least three times per week had lower HbA1c at 6 months than less frequent users (mean difference −0.4%, 95% CI −0.9 to 0.1). App use may be associated with improved glycemic control, but the interval includes no difference and adherence was self-reported.

- **Substantive change:** made explicit that the supplied interval includes no difference (upper bound 0.1). This adds caution from numbers already present. No value changed.
- **Q1:** Is −0.4% a difference in HbA1c percentage points? If so, "percentage points" avoids confusion with a relative change.
- **Fidelity:** PASS (numbers 6). REVIEW: "no" added, which is the reported interval reading.
- **Verdict:** PASS.

---

## T7. A passage that needs only minor proofreading

**Request:** "Proofread this."

**Input:**
> The participants was recruited from three hospitals in Riyadh between March and May 2024, and each completed a 20-minute structured interview.

**Pass criteria:**
- Fixes the agreement error ("was" to "were") and nothing else.
- Returns the corrected sentence with no diagnostic report.

**Failure signals:** any other rewording ("Participants were drawn from..."), added detail, or a change log.

**Last-run revision:**
> The participants were recruited from three hospitals in Riyadh between March and May 2024, and each completed a 20-minute structured interview.

- **Report:** none (proofreading level).
- **Fidelity:** PASS (numbers 2). No flagged word changes.
- **Verdict:** PASS.

---

## T8. Citations, equations, and numbers that must stay intact (LaTeX)

**Request:** "Polish this LaTeX paragraph."

**Input:**
```latex
Following \citet{kirchenbauer2023watermark}, we compute the detection statistic $z = (|s|_G - \gamma T)/\sqrt{T\gamma(1-\gamma)}$, where $T$ is the number of scored tokens and $\gamma = 0.25$ is the green-list fraction. Moreover, it is important to note that this robust statistic clearly demonstrates excellent performance, achieving an AUROC of 0.982 on 1{,}000 held-out samples \cite{dugan2024raid}.
```

**Pass criteria:**
- Math is unchanged character for character. Both citation commands and keys are unchanged.
- 0.25, 0.982, and 1{,}000 are unchanged.
- Removes "Moreover, it is important to note," "robust" (no criterion stated), and "clearly demonstrates excellent performance" (B03, B08, B11).
- Queries the citation's support instead of moving or deleting it: does the cited work report this AUROC, or is it the authors' result on samples from that work (B28)?

**Failure signals:** any change inside `$...$`, a changed or dropped citation, a reformatted number, or a citation silently moved.

**Last-run revision:**
```latex
Following \citet{kirchenbauer2023watermark}, we compute the detection statistic $z = (|s|_G - \gamma T)/\sqrt{T\gamma(1-\gamma)}$, where $T$ is the number of scored tokens and $\gamma = 0.25$ is the green-list fraction. The statistic achieved an AUROC of 0.982 on 1{,}000 held-out samples \cite{dugan2024raid}.
```

- **Substantive change:** removed the unsupported evaluation "robust" and "excellent performance" (B08). The reported AUROC stays as the evidence.
- **Q1:** Does the cited RAID paper report this AUROC, or is 0.982 your result on samples drawn from RAID? If the latter, attach the citation to the samples and present the AUROC as this study's result.
- **Fidelity:** PASS (numbers 6, math 3, citations 2). REVIEW: "demonstrates" removed, which is the reported removal. `verify_edit.py` from `universal-manuscript-polish` also passed all 14 checks.
- **Verdict:** PASS.

---

## Summary of the last run

| Case | Problem tested | Hard checks | Criteria | Verdict |
|---|---|---|---|---|
| T1 | Vague introduction | PASS | All met | PASS |
| T2 | Redundant transitions, repeated conclusions | PASS | All met | PASS |
| T3 | Defined-term drift | PASS | All met | PASS |
| T4 | Claim beyond evidence | PASS | All met | PASS |
| T5 | Literature list without synthesis | PASS | All met | PASS |
| T6 | Causation and uncertainty trap | PASS | All met | PASS |
| T7 | Proofreading only | PASS | All met | PASS |
| T8 | LaTeX math, citations, numbers | PASS | All met | PASS |
