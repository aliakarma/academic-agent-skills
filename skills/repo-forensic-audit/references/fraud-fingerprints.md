# Fraud Fingerprint Checklist

For each item below, state: **PRESENT** / **ABSENT** / **UNCERTAIN** + evidence.

---

## 1. Hardcoded Metrics

Search for metrics assigned as literals instead of computed from predictions.

**Grep patterns:**
```
return 0.9    accuracy = 0.    f1 = 0.    auc = 0.
asr = 0.      precision = 0.   recall = 0.
assert metric ==    assert accuracy ==
"accuracy": 0.     "f1_score": 0.
```

**What to check:**
- Are final metric values ever assigned as constants?
- Are metrics written to results files without a preceding computation?
- Do evaluation functions return hardcoded dicts instead of computed values?
- Are ablation results suspiciously precise (e.g., each variant differs by exactly 0.01)?

**Red flag pattern:** A function named `evaluate()` or `compute_metrics()` that never receives model predictions as input, or receives them but ignores them.

---

## 2. Constant Model Outputs

Does the model always predict the same class or produce identical outputs regardless of input?

**What to check:**
- Trace `forward()` or `predict()` — does output actually depend on input?
- Are there models that return fixed tensors or always argmax to the same class?
- If predictions are saved, do they have zero or near-zero variance?
- For generative models: is output always the same string/sequence?

---

## 3. Reverse-Engineered Evaluation Fixtures

Do "predicted" values suspiciously match "ground truth" with near-zero error?

**What to check:**
- If test predictions are saved (.npy, .csv, .json), compare against ground truth
- Compute the error distribution — is variance unrealistically low?
- Are predictions perfectly ordered or correlated with labels in a way no real model would produce?
- Do confusion matrices show implausibly clean diagonals?

---

## 4. Disconnected Evaluation Pipeline

Is there a live, executable path from raw data → trained model → test metrics?

**What to check:**
- Does `eval.py` load a model that `train.py` actually produces?
- Do file paths, model class names, and checkpoint formats match between train and eval?
- Does the eval script use the same preprocessing as training?
- Are there placeholder paths like `model_best.pt` that no training script generates?
- Does eval load from a hardcoded results file instead of running inference?

**Red flag pattern:** Train and eval scripts that share no imports, no config, and no data pipeline code — they look like two unrelated programs.

---

## 5. Unreachable Training Code

Model definitions, loss functions, or training loops that exist but are never actually instantiated or called.

**What to check:**
- Are there model classes defined but never imported by any entry point?
- Do `if __name__ == "__main__"` blocks exist but with broken imports that prevent execution?
- Are there training loops that reference undefined variables or missing configs?
- Is there a sophisticated model definition that the actual training script replaces with something simpler?

---

## 6. Orphan Result Files

Figures, tables, CSV/JSON result files, or pickle files that have no generation script.

**What to check:**
- For every file in `results/`, `figures/`, `outputs/`, or similar: can you find the script that creates it?
- Do filenames in result directories match any output path in any script?
- Are there pre-baked visualization images with no plotting code?
- Do result timestamps (if available) predate the repo's creation?

---

## 7. Suspiciously Perfect Numbers

Accuracy of exactly 0.90, 0.95, 1.00, or metrics that are implausibly round.

**What to check:**
- Are all reported metrics round to 2 decimal places with no variance?
- Compare claimed performance against known SOTA for the task — does the claim exceed all published baselines by a suspicious margin?
- Do ablation variants show implausibly small, regular improvements (e.g., each component adds exactly +2%)?
- For multi-task results: are all tasks suspiciously close in performance?

**Context matters:** Some metrics on easy benchmarks legitimately round. The question is whether the pattern across ALL reported numbers is statistically plausible.

---

## 8. Seed Sensitivity Concealment

Results reported from a single run with no variance information.

**What to check:**
- Is there only one random seed used (often `seed=42`)?
- Are results reported as single numbers with no std dev or confidence interval?
- If multiple seeds are defined, are they all actually used in reported experiments?
- Is there evidence that many seeds were tried and only the best reported?
- Does performance change dramatically with different seeds (fragile result)?

---

## 9. Test Set Contamination

The same data object is used for both fitting (scaler, encoder, imputer) and evaluating.

**What to check:**
- Trace `fit()` vs `fit_transform()` vs `transform()` calls — is the scaler/encoder fit on the full dataset before splitting?
- Is `sklearn.Pipeline` fit on the complete dataset?
- Are feature selection or dimensionality reduction steps (PCA, feature importance) computed on the full dataset?
- Is cross-validation used correctly, or are transformations applied outside the CV fold?

---

## 10. Label Leakage

Labels available to the model at inference time, either directly or through proxy features.

**What to check:**
- Is `y_test` passed anywhere into the prediction function or feature engineering?
- Are target-encoded features computed using the test set's labels?
- Does the feature set include variables that are proxies for or derived from the target?
- For time-series: is future information used to predict past events?
- For graphs: do node features encode label information?

---

## 11. Metric Implementation Bugs

Metrics computed incorrectly, inflating or deflating apparent performance.

**What to check:**
- Is accuracy computed correctly for imbalanced classes? (macro vs micro vs weighted)
- Is F1's averaging mode appropriate for the task? (binary vs macro vs weighted)
- For AUC: is `predict_proba` used (correct) or `predict` (wrong — gives degenerate AUC)?
- Is the metric computed on the right split? (not accidentally on training data)
- For ranking metrics: is the ranking computed correctly?
- For segmentation/detection: are IoU thresholds applied correctly?

---

## 12. Fabricated or Unrealistic Dataset

Synthetic data with unrealistic separability, or unverifiable real data.

**What to check:**
- If synthetic: what is the generation process? Is it documented? Does it produce unrealistically separable classes?
- If real: is the source verifiable? Is a license or citation included?
- Does the data loader actually load the claimed dataset, or a different one?
- Are feature distributions plausible for the claimed domain?
- Is the dataset size consistent between README claims and what the code loads?

---

## 13. Phantom Ablation Studies

Ablation tables that exist in README/paper but have no corresponding code that runs the ablated variants.

**What to check:**
- For each row in the ablation table: does a code path exist that implements that variant?
- Are ablation variants merely described, or actually instantiable via config/flags?
- Do ablation scripts differ meaningfully from the full model, or are they copies with hardcoded results?
- Are ablation results suspiciously regular (each component adds exactly the same delta)?

**This is a very common fabrication pattern.** Ablations are tedious to run, so authors sometimes fabricate plausible-looking ablation tables. Scrutinize carefully.

---

## 14. Mock or Stub Inference

The inference/prediction function doesn't actually run the model — it returns pre-computed or random values.

**What to check:**
- Does the `predict()` or `inference()` function actually load and execute the model?
- Are there `pass` statements, `NotImplementedError`, or `TODO` comments in critical prediction paths?
- Does the function read from a pre-computed results cache instead of running the model?
- For API-based models (LLM calls): are responses hardcoded or mocked?
- For agent systems: does the agent loop actually execute, or does it return pre-scripted actions?

---

## Fraud Risk Scoring

After evaluating all 14 fingerprints, compute:

| Flags Triggered | Risk Level | Interpretation |
|----------------|------------|----------------|
| 0 | LOW | No integrity concerns detected |
| 1–3 | MEDIUM | May be engineering debt or sloppiness; warrants closer inspection |
| 4–6 | HIGH | Pattern suggests intentional manipulation; require explanation from authors |
| 7+ | CRITICAL | Systematic fabrication likely; recommend rejection |

When assessing risk, consider:
- **Clustering matters.** Five flags concentrated in the eval pipeline is worse than five scattered minor issues.
- **Intentionality signals.** Hardcoded metrics + disconnected pipeline + phantom ablations = deliberate. Missing seeds + no CI = sloppy but honest.
- **State your judgment directly.** "This combination of flags is consistent with deliberate result fabrication" or "These appear to be engineering oversights rather than fraud."
