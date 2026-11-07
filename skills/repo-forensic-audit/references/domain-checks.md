# Domain-Specific Audit Checks

Apply these additional checks when the repository falls into one of the following domains. These supplement (not replace) the general audit phases.

---

## Agentic AI / LLM-Based Systems

Repos involving autonomous agents, multi-agent systems, tool-using LLMs, or agentic workflows.

### Architecture Verification
- Does the agent loop actually execute? Trace from entry point through observation → reasoning → action → environment feedback.
- Are claimed components (planner, executor, critic, memory) all instantiated and called, or are some defined but unused?
- If multi-agent: do agents actually communicate, or does each agent operate in isolation?

### LLM Integration Integrity
- Are LLM API calls real or mocked? Check for `mock`, `fake`, hardcoded response strings.
- Is the claimed model actually used? (e.g., README says GPT-4 but code uses GPT-3.5 or a local model)
- Are prompts shown in the paper the same ones in the code?
- Is temperature / sampling configuration consistent between described and implemented?

### Tool-Use Verification
- Do tool functions execute real operations or return stubs?
- Is tool selection based on LLM output, or hardcoded per scenario?
- Are tool results actually fed back into the agent loop?

### Evaluation Realism
- Are evaluation scenarios diverse and unseen during development?
- Is success measured by task completion, not just LLM output quality?
- Are failure cases analyzed and reported?
- Is cost (API calls, tokens, latency) reported alongside performance?

---

## Reinforcement Learning

Repos involving policy learning, value estimation, or sequential decision-making.

### Environment Integrity
- Is the environment standard (Gym/Gymnasium) or custom? If custom, is it documented?
- Does `env.step()` implement correct dynamics, or does it return fixed transitions?
- Are observations and actions in the correct space/range?
- Is the reward function documented and does it match the described objective?

### Training Verification
- Do training curves show actual learning (not flat or suspiciously smooth)?
- Is the replay buffer / trajectory storage implemented correctly?
- Are target networks updated at the claimed frequency?
- Is exploration noise / epsilon-greedy actually applied?

### Evaluation Protocol
- Is the policy evaluated in a separate process from training (no information leakage)?
- Are evaluation episodes run with exploration disabled?
- Are results averaged over multiple evaluation episodes and seeds?
- Are learning curves reported, not just final performance?

### Reward and Environment Manipulation
- Is the reward scale reasonable for the task?
- Are environment parameters set to make the task trivially easy?
- Is the horizon (max steps) tuned to guarantee success?
- Are stochastic elements removed during evaluation to inflate scores?

---

## Federated Learning

Repos involving distributed training across simulated or real clients.

### Federation Integrity
- Are clients genuinely independent, or do they share data/state?
- Is the data partition (IID vs non-IID) implemented as claimed?
- Does the number of clients match the README/paper claims?
- Are communication rounds actually simulated, or is it centralized training in disguise?

### Aggregation Verification
- Is the aggregation algorithm (FedAvg, FedProx, etc.) correctly implemented?
- Are client weights proportional to dataset size (if claimed)?
- Does the global model actually receive aggregated updates?
- After aggregation, is the global model distributed back to clients?

### Privacy Claims
- If differential privacy is claimed: is noise calibrated to a stated epsilon? Is the privacy accountant tracking cumulative budget?
- If secure aggregation is claimed: is cryptographic aggregation implemented, or just simulated?
- Are privacy guarantees validated (not just claimed)?

### Heterogeneity
- Is data heterogeneity actually present and measurable?
- Are system heterogeneity (different compute, bandwidth) claims reflected in code?
- Is convergence measured under the claimed heterogeneity level?

---

## Digital Twin / Simulation-Based Systems

Repos involving simulated environments, cyber-physical systems, or digital twin architectures.

### Simulation Fidelity
- Is the simulation calibrated against real-world data?
- Are physical models (dynamics, sensor noise, communication delay) realistic?
- Is the simulation timestep appropriate for the dynamics?
- Are boundary conditions and failure modes modeled?

### Sim-to-Real Gap
- Is there any real-world validation, or only simulation results?
- If simulation-only: is this limitation clearly stated?
- Are transfer learning or domain adaptation techniques applied?
- Is the sim-to-real gap quantified?

### Architecture Claims
- If "digital twin" is claimed: is there actually a bidirectional data flow between physical and digital, or is it just a simulation?
- Are IoT/sensor integrations real or simulated?
- Are real-time claims validated with latency measurements?
- Does the "twin" actually update from real data, or is it static?

### Scalability
- Are scalability claims tested at the claimed scale?
- Is the simulation parallelized as described?
- Are resource requirements (memory, compute) documented at different scales?
