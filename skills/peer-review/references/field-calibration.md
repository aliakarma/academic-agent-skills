# Field-Specific Review Calibration

Different research fields have different norms. Use this reference to calibrate review expectations based on the manuscript's domain and target venue.

## Table of Contents

1. [AI/ML Papers](#aiml-papers)
2. [Systems & Engineering Papers](#systems--engineering-papers)
3. [Survey & Review Papers](#survey--review-papers)
4. [Theoretical Papers](#theoretical-papers)
5. [Interdisciplinary Papers](#interdisciplinary-papers)
6. [Venue-Tier Calibration](#venue-tier-calibration)

---

## AI/ML Papers

### Mandatory expectations at Q1 venues

- **Ablation studies**: Every non-trivial component must be ablated. Missing ablations is a near-fatal weakness at top venues.
- **Multiple seeds**: Minimum 3 seeds, ideally 5+. Single-seed results are unacceptable at NeurIPS/ICML/ICLR tier.
- **Seed reporting**: Exact seeds used must be disclosed.
- **Error bars / confidence intervals**: Required on all reported metrics.
- **Compute budget**: Training time, GPU hours, hardware specification.
- **Hyperparameter sensitivity**: At minimum, sensitivity to key hyperparameters.
- **SOTA comparison**: Must compare against the most recent competitive baselines, not just convenient older ones.
- **Code availability**: Expected at top venues. Anonymous repo during review, public on acceptance.
- **Dataset details**: Exact splits, preprocessing, any filtering applied.

### Common weaknesses in AI/ML submissions

- Comparing against baselines from 3+ years ago when newer methods exist
- Reporting only the best run instead of average across seeds
- Using non-standard evaluation protocols that favor the proposed method
- Ablating only easy components (the ones that obviously matter)
- Claiming SOTA without comparing against all relevant recent work
- Overfitting to a specific benchmark without generalization evidence
- Missing failure case analysis
- No computational cost comparison with baselines

### LLM-specific checks

- Prompt sensitivity analysis (different prompt templates)
- Temperature / sampling parameter sensitivity
- Model version disclosure (exact checkpoint, API date)
- Token cost reporting
- Potential data contamination between training and eval sets
- Human evaluation protocol details (annotator count, agreement metrics)

### Reinforcement Learning–specific checks

- Environment version and configuration details
- Reward function fully specified
- Training curves (not just final performance)
- Multiple seeds mandatory (RL has high variance)
- Comparison under matched compute budgets
- Evaluation over sufficient episodes

---

## Systems & Engineering Papers

### Mandatory expectations

- **Scalability analysis**: How does performance change with scale? (data size, users, nodes)
- **Deployment considerations**: Latency, throughput, resource requirements
- **Real-world applicability**: Evidence beyond toy examples
- **Architecture justification**: Why this design over alternatives?
- **Failure mode analysis**: What happens when components fail?
- **End-to-end evaluation**: Not just component-level metrics

### Common weaknesses

- Evaluating only on toy/synthetic scenarios
- Missing latency / throughput measurements
- No discussion of deployment constraints
- Comparing against naive baselines instead of production systems
- Architecture described but not justified against alternatives
- Missing discussion of operational cost
- No fault tolerance analysis

---

## Survey & Review Papers

### Mandatory expectations

- **Systematic methodology**: PRISMA or equivalent protocol documented
- **Search strategy**: Databases searched, keywords, date ranges, inclusion/exclusion criteria
- **Completeness**: Coverage of foundational and recent work verified
- **Taxonomy**: Clear, well-motivated categorization of the literature
- **Critical analysis**: Not just summarizing papers — comparing, contrasting, identifying gaps
- **Research agenda**: Clear identification of open problems and future directions
- **Quantitative overview**: Paper counts by year, method, domain (if applicable)

### Common weaknesses

- Incomplete search strategy (missing key databases or venues)
- Narrative review disguised as systematic review
- Taxonomy that doesn't hold up (overlapping categories, missing important classes)
- Summarizing without analyzing (paper-by-paper summaries instead of synthesis)
- Missing recent key papers
- No clear contribution beyond listing papers
- Outdated or biased selection of literature
- Missing comparison tables

---

## Theoretical Papers

### Mandatory expectations

- **Proof correctness**: All proofs must be complete and verifiable
- **Assumption clarity**: All assumptions explicitly stated and justified
- **Complexity analysis**: Time and space complexity of proposed methods
- **Connection to practice**: At least discussion of practical implications
- **Lower bounds**: Where applicable, impossibility results or lower bounds
- **Empirical validation**: Even theoretical papers benefit from experiments confirming predictions

### Common weaknesses

- Proofs with gaps or hand-waving at critical steps
- Unrealistic assumptions that disconnect theory from practice
- No empirical validation of theoretical predictions
- Missing comparison to existing theoretical results
- Theorems stated more strongly than proofs support
- Notation overload making proofs unverifiable

---

## Interdisciplinary Papers

### Special considerations

- **Dual audience**: Must be accessible to both domain experts and method experts
- **Domain validity**: Methods must respect domain constraints and norms
- **Evaluation metrics**: Must use metrics meaningful to the application domain
- **Stakeholder relevance**: Must address practical needs, not just technical novelty
- **Domain expert validation**: Evidence that domain experts find the approach useful

### Common weaknesses

- Method experts ignoring domain constraints
- Domain experts applying methods without understanding limitations
- Evaluation metrics irrelevant to actual practitioners
- Overclaiming applicability without domain expert validation
- Ignoring existing domain-specific solutions
- Insufficient background for cross-disciplinary readers

---

## Venue-Tier Calibration

### Tier 1: Top conferences and flagship journals
(NeurIPS, ICML, ICLR, CVPR, ACL, AAAI, IEEE TPAMI, JMLR, Nature Machine Intelligence, etc.)

- Novelty must be substantial and clearly articulated
- Experiments must be comprehensive with statistical rigor
- Writing must be polished and precise
- All ablations and baselines expected
- Reproducibility requirements high
- Impact must be clearly significant
- Rejection rate: 70–85%

### Tier 2: Strong Q1 journals and respected conferences
(IEEE TDSC, IEEE Access (when selective), ACM Computing Surveys, IJCAI, ECML, KDD, etc.)

- Solid contribution required but can be more incremental
- Good experimental validation expected
- Writing should be clear and professional
- Main ablations and baselines expected
- Moderate reproducibility requirements
- Clear relevance to the community
- Rejection rate: 50–70%

### Tier 3: Good Q1/Q2 journals and specialized conferences
(MDPI Sustainability, Frontiers journals, specialized IEEE transactions, regional conferences)

- Contribution can be application-focused or incremental methodological
- Adequate experimental validation
- Clear writing expected
- Core baselines required
- Basic reproducibility information
- Relevance to the specific community
- Rejection rate: 30–60%

### Mismatch detection

If the paper's quality/novelty level doesn't match its target venue:
- State the mismatch explicitly
- Explain which dimensions are below venue expectations
- Suggest 2–3 alternative venues at the appropriate tier with brief justification for each
