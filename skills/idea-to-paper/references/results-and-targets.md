# Results, Implementation Targets, and Consistency

The results section must read like a strong conference paper: full tables, curves, ablations, runtime, and scalability, with believable values. When the author has not measured anything, those values are implementation targets. They show the author what level of result the paper needs and what experiments to run. They are never presented as measurements.

## The marking contract

| Element | How to mark it |
|---|---|
| A target number in prose, a table cell, or the abstract | `\tgt{92.2}` (the `%` stays outside: `\tgt{92.2}\%`) |
| A float whose data are targets | Caption starts with `\tgtcap` |
| A PGFPlots figure with target data | Caption starts with `\tgtcap` (coordinates cannot be colored) |
| The paper as a whole, while any target remains | `\title{...\thanks{\textcolor{tgtblue}{\tgtnotice}}}` |
| A float with author-measured data | `% MEASURED: <file, log, or "author input, <date>">` inside the float |
| A float with configuration or design choices | `% CONFIG: <what it is>` inside the float |
| A float with facts from cited sources (dataset statistics, prior-work features) | `% SOURCE: <citation keys>` inside the float |
| A prose paragraph with author-measured numbers | A comment line `% MEASURED: <source>` directly above the paragraph |

Mark hardware, software versions used for a run, run times, participant counts, and statistical test results the same way, because each claims that something happened. Hyperparameters are design choices (`% CONFIG:`) and stay black.

## Build the target sheet first

Write `_build/targets.py` before any results text. It holds every target value once and computes every derived number, so the abstract, introduction, tables, plots, and conclusion all print the same figures.

```python
# _build/targets.py: single source of every target value. Run it and paste its output.
methods = {  # precision, recall in percent, latency in ms
    "Baseline A": (88.1, 85.4, 41.2),
    "Baseline B": (89.6, 87.9, 38.5),
    "Baseline C": (90.8, 89.2, 52.9),
    "Proposed":   (92.7, 91.7, 44.6),
}
f1 = {m: 2 * p * r / (p + r) for m, (p, r, _) in methods.items()}
best_base = max((m for m in methods if m != "Proposed"), key=f1.get)
gain = f1["Proposed"] - f1[best_base]
assert 0 < gain < 4, "gain outside the plausible band for a mature benchmark"
assert methods["Proposed"][2] > min(v[2] for v in methods.values()), "the method should cost something"
for m, (p, r, lat) in methods.items():
    print(f"{m} & \\tgt{{{p:.1f}}} & \\tgt{{{r:.1f}}} & \\tgt{{{f1[m]:.1f}}} & \\tgt{{{lat:.1f}}} \\\\")
print(f"F1 gain over {best_base}: {gain:.1f} points")
```

Extend it for ablations, curves, scalability, and the confusion matrix. Keep the asserts: they encode the plausibility rules below.

## Plausibility rules

1. **Anchor on the literature.** Where a cited baseline reports a result on the same dataset, the baseline target sits close to it and the source goes in the register. Saturated benchmarks (MNIST, many IDS datasets) leave little room, so gains there are small.
2. **Modest gains.** On a mature benchmark the method beats the strongest baseline by about 0.5 to 3 points absolute. Larger gains need a stated reason (a new capability the baselines lack, a harder setting they were not built for).
3. **No perfect scores.** No 100%, no 99.9x, no zero false positives unless the cited literature shows the task is saturated.
4. **A real trade-off.** The method loses on at least one axis (latency, memory, communication, energy, setup cost), and the text says so.
5. **Variance.** Report mean and standard deviation over at least five seeds. Typical standard deviations are 0.2 to 1.5 points for accuracy-type metrics and 3 to 10% of the mean for latency.
6. **Ablation.** The full model is best. Each removed component costs about 0.5 to 3 points. Drops may sum to more than the total gain (components interact), but no single removal beats the full model.
7. **Curves.** Training curves rise fast and then flatten, with small noise. Scalability grows linearly or sublinearly for the method, and the baseline that lacks the method's mechanism grows faster. Final curve points equal the table values.
8. **Units and hardware.** Latency, throughput, and energy fit the stated hardware (an edge device is slower than an A100). Throughput and latency agree with each other.
9. **Statistics.** A claim of significance names the test and the p-value, both marked. With five paired seeds, the exact two-sided Wilcoxon signed-rank test cannot go below p = 0.0625, so use at least six seeds (minimum 0.03125), a paired t-test with its assumptions stated, or confidence intervals instead.

## Consistency rules

- F1 equals 2PR/(P+R) for every row unless the caption says the scores are macro-averaged over classes. `check_paper.py` fails violations (E18).
- Accuracy-type metrics stay at or below 100 (E19).
- A row-normalized confusion matrix has rows summing to 1, and its mean diagonal equals the macro recall in the main table.
- Every number appears with the same value and the same rounding everywhere: abstract, introduction, tables, figures, conclusion.
- Improvement claims ("2.2 points higher", "37% lower latency") are computed in `targets.py`. Say whether a change is absolute points or relative percent.
- The research question answers in the results match the numbers in the tables.

## Metric families by topic

| Topic | Core metrics | Usual extra analyses |
|---|---|---|
| Classification, detection, medical or vision models | Accuracy, precision, recall, F1 (macro when classes are imbalanced), AUC-ROC, false positive rate | Confusion matrix, per-class results, inference latency |
| Federated learning | Global accuracy against rounds, rounds to a target accuracy, communication per round and total (MB) | Non-IID settings (Dirichlet alpha), Byzantine fraction sweep, privacy budget epsilon, spread of client accuracy |
| Blockchain-integrated AI | Throughput (TPS), confirmation latency, gas or fee per operation, storage overhead | Consensus time against node count, attack cost |
| Agentic AI and LLM agents | Task success rate, tool-call accuracy, steps per task, tokens and cost per task, latency per task | Policy violation or hallucination rate, human evaluation with agreement (Cohen's kappa) |
| Digital twins | State estimation error (RMSE, MAE), synchronization latency, prediction accuracy over the horizon | Update frequency against fidelity, what-if scenario accuracy |
| Cybersecurity | Detection rate, false positive rate, time to detect, attack success rate | Adversarial robustness against perturbation size, unseen-attack generalization |
| Trustworthy AI | Calibration (ECE), explanation faithfulness, trust score, fairness gaps (demographic parity, equalized odds) | Robustness under distribution shift, audit cost |
| Accessibility technology | Task completion rate, time on task, error rate, SUS (average about 68), NASA-TLX | Participant study design. Participant counts are targets, and the paper states that the protocol needs ethics approval. Never claim an approval |
| Edge and energy-aware systems | Energy per inference (J), power (W), memory footprint, latency | Battery life, accuracy against energy trade-off curve |

## Author-measured data

When the author supplies logs or CSVs, read the files, compute the reported statistics with a script saved in `_build/`, and use those exact values. Record the computation in the report. Use targets only for metrics the data does not cover, and say which in the report. If the measured values contradict a claim in the author's abstract, keep the measured values and flag the conflict to the author.

## What the report must say about targets

- The count of target values and target floats (printed by `check_paper.py`).
- The register file `_build/target_register.md`.
- "What to run": each experiment the targets imply, with dataset, baselines, seeds, metric, and the acceptance level the target sets.
- The rule: replace a target only with a measured value, then rewrite any claim the measured value no longer supports.
