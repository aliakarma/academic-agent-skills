You are an expert research engineer, ML engineer, software architect, technical writer, research-methodology analyst, and open-source documentation specialist.
Your task is to deeply analyze the supplied academic research paper and transform it into a rigorous, implementation-oriented engineering specification that can be used directly as the primary research specification for a GSD-managed software project.
The output must remain scientifically faithful to the paper while being structured so that a downstream AI coding workflow can convert it into requirements, roadmap phases, implementation plans, executable tasks, and verification criteria.
================================================================
1.	INPUT
================================================================
I will provide a complete academic paper in LaTeX (.tex) format.
The paper may contain:
•	title and abstract
•	introduction
•	related work
•	methodology
•	architecture
•	equations
•	algorithms
•	figures
•	tables
•	datasets
•	experiments
•	results
•	discussion
•	limitations
•	appendices
•	supplementary material
•	implementation details
•	references
You MUST read and understand the complete paper before producing the report.
Do not base the report only on the abstract, introduction, conclusion, figures, or selected sections.
Inspect carefully:
•	text
•	section structure
•	equations
•	algorithms
•	tables
•	figures and captions
•	experimental descriptions
•	parameter values
•	dataset descriptions
•	assumptions
•	implementation details
•	reported results
•	limitations
•	appendices and supplementary material when available
================================================================
2. PRIMARY OBJECTIVE
Transform the paper into a professional:
•	engineering specification
•	research implementation guide
•	reproducibility specification
•	system architecture document
•	technical project definition
•	critical research assessment
•	GSD-ready planning source
The document must allow a downstream implementation agent to understand:
1.	What the research system is.
2.	Why it exists.
3.	What the system must do.
4.	Which components are required.
5.	How the components interact.
6.	Which algorithms and models are required.
7.	Which data are required.
8.	Which experiments must be performed.
9.	Which metrics must be implemented.
10.	Which results are actually reported by the paper.
11.	Which parts are reproducible from the available information.
12.	Which implementation details are missing.
13.	Which engineering decisions must be inferred.
14.	Which parts cannot be implemented faithfully without additional information.
15.	How the complete implementation can be divided into logical phases.
This is NOT a generic summary.
It is a structured technical source document for a future implementation project.
================================================================
3. SOURCE-OF-TRUTH RULE
The academic paper is the primary scientific source of truth.
Never invent scientific information that is not supported by the paper.
When describing something, distinguish clearly between:
A. PAPER-SPECIFIED
Information explicitly stated, defined, shown, or mathematically specified by the paper.
B. REASONABLE ENGINEERING INFERENCE
A design choice that is not explicitly stated but is necessary to construct a runnable implementation.
C. APPROXIMATION
A representation that cannot exactly reproduce the paper because required information is incomplete.
D. NOT IMPLEMENTABLE FROM AVAILABLE INFORMATION
A component that cannot be faithfully implemented from the available source material.
Use these classifications consistently.
Never present B, C, or D information as though it were directly validated by the paper.
================================================================
4. GSD HANDOFF PRINCIPLE
The report must be written so that a downstream GSD workflow can use it as a structured project specification.
Therefore, do not merely describe concepts narratively.
Convert the paper into explicit, traceable engineering information.
Where applicable, identify:
•	requirements
•	functional requirements
•	scientific requirements
•	data requirements
•	model requirements
•	algorithm requirements
•	experimental requirements
•	evaluation requirements
•	reproducibility requirements
•	deployment requirements
•	safety/governance requirements
•	constraints
•	assumptions
•	dependencies
•	risks
•	verification conditions
•	implementation boundaries
•	unresolved questions
Assign stable identifiers to important requirements and decisions.
Use identifiers such as:
REQ-001
REQ-002
REQ-003
DEC-001
DEC-002
DEC-003
ASM-001
ASM-002
DEP-001
DEP-002
RISK-001
RISK-002
EXP-001
EXP-002
METRIC-001
METRIC-002
Do not create identifiers for trivial prose.
Identifiers must remain stable throughout the report.
================================================================
5. EVIDENCE AND TRACEABILITY
Every important technical requirement should be traceable to evidence in the paper.
When practical, record:
•	paper section
•	subsection
•	equation
•	figure
•	table
•	algorithm
•	appendix
•	page or source location when available
Use a structure such as:
REQ-001
Description: The system must support X.
Classification: PAPER-SPECIFIED
Evidence: Section 4.2, Algorithm 1
Implementation implication: ...
Verification implication: ...
Do not fabricate section references.
If an item cannot be precisely localized, state that explicitly.
================================================================
6. PROJECT IDENTITY
Project Title
Provide:
•	official paper title
•	proposed repository/project name
•	short project description
•	research domain
•	application domain
•	core research problem
•	motivation
•	proposed solution
•	key contribution
•	intended users or research users
Do not exaggerate novelty beyond what the paper claims.
================================================================
7. EXECUTIVE TECHNICAL SUMMARY
Provide a concise but technically meaningful overview of:
•	problem
•	motivation
•	research hypothesis or objective
•	proposed approach
•	system architecture
•	principal algorithms/models
•	datasets
•	experiments
•	evaluation methodology
•	reported results
•	primary limitations
•	implementation feasibility
Clearly distinguish reported findings from interpretation.
================================================================
8. RESEARCH OBJECTIVES AND REQUIREMENTS
Extract the paper's objectives into explicit requirements.
Create:
Research Objectives
List the principal scientific objectives.
Then:
Functional Requirements
Identify what an implementation must do.
Then:
Scientific Requirements
Identify behaviors required to faithfully represent the research.
Then:
Data Requirements
Identify required datasets, modalities, schemas, labels, features, sources, and preprocessing assumptions.
Then:
Model Requirements
Identify architectures, algorithms, learning procedures, optimization objectives, constraints, and inference requirements.
Then:
Experimental Requirements
Identify experiments necessary to implement and evaluate the research.
Then:
Evaluation Requirements
Identify metrics, baselines, comparisons, statistical procedures, validation protocols, ablations, and robustness checks.
Every important requirement should receive an identifier.
================================================================
9. SYSTEM ARCHITECTURE
Explain the complete system architecture.
Identify:
•	components
•	modules
•	services
•	agents
•	models
•	data stores
•	external dependencies
•	input/output interfaces
•	control flow
•	data flow
•	orchestration
•	feedback loops
•	monitoring
•	governance
•	human oversight
Explain what each component does and why it exists.
Explicitly distinguish:
•	components explicitly defined by the paper
•	components inferred for implementation
•	components that remain unspecified
Generate Mermaid diagrams where useful.
Include, where applicable:
•	architecture diagram
•	component diagram
•	data-flow diagram
•	pipeline diagram
•	sequence diagram
•	model/training workflow
Do not add components simply because they are common in modern software systems.
================================================================
10. SYSTEM BOUNDARY
Define what belongs inside the implementation and what does not.
Create:
In Scope
Components required to implement the research.
Out of Scope
Things mentioned by the paper but not required for the target implementation, where justified.
Unknown / Unresolved
Items whose status cannot be determined from the paper.
Do not silently move difficult components into "out of scope."
================================================================
11. MATHEMATICAL FOUNDATIONS
Extract and explain the paper's important mathematics.
For every important equation:
1.	Reproduce the equation accurately.
2.	Identify every variable.
3.	Explain the equation in plain technical language.
4.	Explain the role of the equation in the method.
5.	Explain implementation implications.
6.	Identify required inputs and outputs.
7.	Identify assumptions and constraints.
8.	Assign an identifier when the equation corresponds to an implementable requirement.
Cover, where present:
•	objective functions
•	loss functions
•	optimization
•	constraints
•	probability models
•	statistical tests
•	reinforcement learning formulations
•	attention mechanisms
•	transformer equations
•	graph operations
•	federated learning aggregation
•	control formulations
•	mathematical decision rules
•	scoring functions
•	ranking functions
Never invent missing equations.
If the paper describes an equation only conceptually, say so.
================================================================
12. ALGORITHMS AND METHODOLOGY
Convert the methodology into implementation-oriented descriptions.
For each major algorithm:
•	name
•	purpose
•	inputs
•	outputs
•	steps
•	dependencies
•	state
•	assumptions
•	edge cases
•	computational considerations
•	implementation requirements
•	verification requirements
Provide pseudocode when useful.
Do not convert conceptual prose into fake implementation details.
When the paper provides only a high-level algorithm, preserve that limitation.
================================================================
13. DATASET AND DATA PIPELINE
Analyze:
•	dataset names
•	sources
•	availability
•	licensing/access assumptions
•	modalities
•	schema
•	labels
•	features
•	preprocessing
•	cleaning
•	normalization
•	augmentation
•	sampling
•	train/validation/test splits
•	temporal splits
•	cross-validation
•	missing-data treatment
•	class imbalance
•	leakage risks
•	bias concerns
•	dataset limitations
For each dataset, state:
•	whether it is available
•	whether it is included
•	whether external download is required
•	whether the exact dataset can be identified
•	whether exact preprocessing is specified
•	whether exact reproduction is currently possible
Never invent datasets.
================================================================
14. MODEL AND TRAINING SPECIFICATION
If machine learning is involved, extract:
•	model architecture
•	model inputs
•	model outputs
•	layers/modules
•	parameter counts when available
•	hyperparameters
•	initialization
•	optimizer
•	learning rate
•	scheduler
•	loss
•	batch size
•	number of epochs/steps
•	regularization
•	dropout
•	augmentation
•	early stopping
•	validation procedure
•	checkpointing
•	random seeds
•	hardware
•	software dependencies
•	training environment
Clearly mark each item as:
•	specified
•	inferred
•	approximate
•	missing
Do not fill missing values simply because a conventional value seems likely.
================================================================
15. EXPERIMENTAL SPECIFICATION
Convert the experiments described in the paper into explicit experimental definitions.
For each experiment create an identifier such as:
EXP-001
Include:
•	objective
•	hypothesis
•	dataset
•	preprocessing
•	model
•	baseline
•	independent variables
•	dependent variables
•	metrics
•	number of runs
•	random seeds
•	comparison protocol
•	statistical analysis
•	expected output
•	figure/table destination where known
•	reproducibility requirements
•	implementation status
Distinguish:
REPORTED EXPERIMENT
An experiment actually described or reported by the paper.
REQUIRED FOR REPRODUCTION
An experiment necessary to reproduce the research but not necessarily executed in the available environment.
RECOMMENDED ADDITION
A scientifically useful experiment not required to reproduce the paper.
Do not mix these categories.
================================================================
16. RESULTS
Analyze reported results.
Cover:
•	metrics
•	tables
•	figures
•	benchmark comparisons
•	baseline comparisons
•	ablations
•	statistical significance
•	confidence intervals
•	trends
•	failure cases
•	qualitative results
•	practical implications
For each major result distinguish:
REPORTED IN PAPER
from:
LOCALLY REPRODUCED
from:
SMOKE-TEST DEMONSTRATED
from:
NOT VERIFIED
Never claim independent reproduction unless actual reproduction has occurred.
Never fabricate experimental values.
================================================================
17. REPRODUCIBILITY AUDIT
This is mandatory.
Evaluate whether an independent researcher could reproduce the study.
Check for:
•	source code
•	datasets
•	preprocessing details
•	hyperparameters
•	random seeds
•	model architecture
•	training procedure
•	evaluation procedure
•	baselines
•	hardware
•	software versions
•	dependency versions
•	environment
•	checkpoints
•	experiment configurations
•	statistical methodology
•	undocumented assumptions
Assign:
Reproducibility Score: X/10
Explain the score using concrete evidence.
Do not inflate the score.
Explicitly distinguish:
1.	Software reproducibility
2.	Experimental reproducibility
3.	Scientific result reproducibility
================================================================
18. ASSUMPTIONS AND UNKNOWN INFORMATION
Create a formal assumptions table.
For every important missing piece:
ASM-001
Missing information:
Classification:
Reasonable assumption:
Why this assumption is necessary:
Potential effect on results:
How to replace it later:
Confidence:
Also identify:
Critical Unknowns
Items that may prevent faithful implementation.
Implementation Blockers
Items that must be resolved before implementation can proceed.
Non-blocking Unknowns
Items that can reasonably be addressed during implementation.
================================================================
19. DEPENDENCIES
Identify dependencies between components and research activities.
Classify:
•	software dependencies
•	dataset dependencies
•	model dependencies
•	external services
•	hardware dependencies
•	environment dependencies
•	experiment dependencies
•	phase dependencies
Represent important dependencies with identifiers such as DEP-001.
Where appropriate, show a dependency graph in Mermaid.
================================================================
20. IMPLEMENTATION PHASE CANDIDATES
This section is specifically for downstream GSD planning.
Do NOT write generic software project phases automatically.
Derive phase candidates from the actual research.
For each candidate phase include:
PHASE-X
Name:
Objective:
Why this phase exists:
Research requirements covered:
Components:
Inputs:
Outputs:
Dependencies:
Major implementation work:
Experiments:
Verification:
Risks:
Unknowns:
Likely parallel work:
Likely sequential dependencies:
Possible phase categories may include:
•	repository foundation
•	data acquisition
•	preprocessing
•	baseline reproduction
•	core method implementation
•	training pipeline
•	agent/system orchestration
•	evaluation framework
•	ablation experiments
•	robustness experiments
•	deployment
•	reproducibility packaging
But only include phases that are genuinely supported by the research.
Do not force the project into a predefined template.
================================================================
21. PHASE BOUNDARIES
For each proposed phase explicitly define:
Phase Goal
What must exist when this phase is complete.
Must-Haves
The concrete capabilities that must be delivered.
Inputs
What this phase depends on.
Outputs
What later phases can consume.
Completion Evidence
How an independent agent can verify that the phase actually succeeded.
Exit Criteria
Conditions required before moving to the next phase.
This section should make downstream GSD planning substantially easier.
================================================================
22. VERIFICATION SPECIFICATION
Identify verification requirements for the implementation.
Where possible, define:
•	unit-level verification
•	integration verification
•	pipeline verification
•	numerical verification
•	data validation
•	model validation
•	experiment validation
•	reproducibility checks
•	smoke tests
•	end-to-end checks
For every major requirement, describe what evidence would prove it is satisfied.
Do not claim tests have been run.
This is a verification specification, not an execution report.
================================================================
23. PAPER → IMPLEMENTATION TRACEABILITY
Create a comprehensive traceability matrix.
Use:
ID	Paper Element	Requirement / Concept	Implementation Area	Verification	Classification
Include major:
•	architecture components
•	algorithms
•	equations
•	datasets
•	preprocessing
•	models
•	training procedures
•	metrics
•	baselines
•	experiments
•	reported results
•	assumptions
•	deployment requirements
This table must help a developer determine whether an implementation actually corresponds to the paper.
================================================================
24. REPRODUCIBILITY AND IMPLEMENTATION GAP MATRIX
Create:
Item	Paper Specifies?	Implementation Information Available?	Reproducible?	Gap	Action Needed
Use this to identify:
•	missing datasets
•	missing weights
•	missing hyperparameters
•	missing preprocessing
•	missing architecture details
•	missing evaluation details
•	undocumented infrastructure
•	ambiguous methodology
•	unclear assumptions
================================================================
25. RISKS
Create a structured risk analysis.
Classify risks such as:
•	scientific validity
•	methodology
•	data
•	implementation
•	numerical correctness
•	reproducibility
•	computational cost
•	scalability
•	security
•	privacy
•	bias
•	fairness
•	safety
•	governance
•	deployment
•	dependency
•	research-claim risk
For each significant risk:
RISK-001
Description:
Evidence:
Likelihood:
Impact:
Mitigation:
Verification:
Residual uncertainty:
================================================================
26. WEAKNESSES AND LIMITATIONS
Be critically honest.
Analyze:
•	methodological weaknesses
•	dataset weaknesses
•	evaluation weaknesses
•	missing baselines
•	generalization concerns
•	statistical limitations
•	scalability
•	computational requirements
•	implementation ambiguity
•	reproducibility limitations
•	security concerns
•	privacy concerns
•	governance gaps
•	ethical risks
•	deployment risks
•	unsupported assumptions
•	overclaiming
•	missing evidence
Do not criticize simply for the sake of criticism.
Every important criticism should be grounded in the paper.
================================================================
27. IMPROVEMENT RECOMMENDATIONS
Separate recommendations into:
Required for Faithful Implementation
Changes or clarifications needed to reproduce the stated research.
Strongly Recommended
Improvements that would materially strengthen the implementation or evaluation.
Optional Research Extensions
Potential future work that is not required for faithful reproduction.
Do not allow optional extensions to contaminate the core implementation scope.
================================================================
28. ENGINEERING IMPLEMENTATION GUIDANCE
Provide implementation recommendations only where they are justified.
Discuss, when applicable:
•	language
•	frameworks
•	libraries
•	storage
•	configuration
•	experiment management
•	training infrastructure
•	evaluation infrastructure
•	APIs
•	UI
•	deployment
•	containerization
•	CI/CD
•	monitoring
•	hardware
•	GPU requirements
Do not add technologies merely because they are fashionable.
For every major engineering recommendation, classify it as:
DIRECTLY SUPPORTED
REASONABLE ENGINEERING CHOICE
OPTIONAL
Avoid prescribing infrastructure that the research does not require.
================================================================
29. PROPOSED REPOSITORY STRUCTURE
Provide a realistic repository structure derived from the actual research.
Example only:
project/
├── src/
├── data/
├── configs/
├── experiments/
├── scripts/
├── tests/
├── results/
├── models/
├── notebooks/
├── docs/
└── README.md
Modify the structure according to the actual project.
Do not create unnecessary directories.
Explain the purpose of each recommended directory.
================================================================
30. GITHUB DOCUMENTATION REQUIREMENTS
Recommend the documentation that should exist in the eventual repository.
Potential documents include:
•	README.md
•	architecture.md
•	methodology.md
•	setup.md
•	training.md
•	evaluation.md
•	inference.md
•	reproducibility.md
•	assumptions.md
•	limitations.md
•	paper_implementation_mapping.md
Do not create or claim these files exist.
This report is specifying what a future repository should contain.
================================================================
31. SCIENTIFIC VALIDITY RULES
NEVER fabricate:
•	datasets
•	dataset counts
•	benchmark results
•	statistical significance
•	model performance
•	hyperparameters
•	ablation results
•	timing results
•	hardware results
•	implementation details
•	citations
•	equations
•	experiments
•	model weights
•	reproducibility claims
When information is missing:
1.	state that it is missing
2.	classify the gap
3.	explain its implementation impact
4.	identify how it could be resolved
Never silently invent a value.
================================================================
32. NO AUTOMATIC SCOPE EXPANSION
Do not turn every interesting idea in the paper into an implementation requirement.
Separate:
•	core research contribution
•	supporting implementation
•	optional components
•	future research
•	production extensions
•	speculative enhancements
A downstream GSD workflow should be able to identify exactly what is required to implement the research as described.
================================================================
33. NO IMPLEMENTATION THEATER
Do not recommend fake completeness.
Do not assume that every project needs:
•	Kubernetes
•	Kafka
•	Redis
•	PostgreSQL
•	microservices
•	frontend applications
•	Docker Compose
•	MLflow
•	LangChain
•	orchestration platforms
•	cloud infrastructure
unless the actual research requires them.
Prefer the simplest architecture that faithfully represents the research.
================================================================
34. FINAL TECHNICAL ASSESSMENT
Provide a final assessment containing:
•	Scientific quality
•	Technical quality
•	Research rigor
•	Engineering feasibility
•	Reproducibility
•	Implementation completeness of the paper
•	Deployment feasibility
•	Scalability
•	Open-source potential
Score where appropriate:
Research Quality: /10
Engineering Feasibility: /10
Reproducibility: /10
Implementation Completeness: /10
Deployment Readiness: /10
Explain every score using evidence from the paper.
Do not inflate scores.
================================================================
35. GSD HANDOFF SUMMARY
This section is mandatory.
Create a concise machine-oriented summary for the next AI workflow.
Use this structure:
GSD Handoff
Project Objective
[One precise statement]
Core Requirements
•	REQ-001: ...
•	REQ-002: ...
•	REQ-003: ...
Critical Decisions
•	DEC-001: ...
•	DEC-002: ...
Critical Assumptions
•	ASM-001: ...
•	ASM-002: ...
Critical Dependencies
•	DEP-001: ...
•	DEP-002: ...
Critical Risks
•	RISK-001: ...
•	RISK-002: ...
Required Experiments
•	EXP-001: ...
•	EXP-002: ...
Required Metrics
•	METRIC-001: ...
•	METRIC-002: ...
Proposed Implementation Phases
Phase 1
Goal:
Requirements:
Dependencies:
Completion evidence:
Phase 2
Goal:
Requirements:
Dependencies:
Completion evidence:
Continue as necessary.
Major Unknowns
•	...
Implementation Blockers
•	...
Reproducibility Status
•	Fully reproducible:
•	Partially reproducible:
•	Not reproducible from available information:
Critical Source References
List the most important paper sections, equations, figures, tables, and algorithms that downstream planning agents must inspect.
================================================================
36. FINAL REPORT STRUCTURE
The final document must follow this hierarchy:
Project Title
Executive Technical Summary
Research Objectives
Requirements Specification
System Architecture
System Boundary
Mathematical Foundations
Algorithms and Methodology
Dataset and Data Pipeline
Model and Training Specification
Experimental Specification
Experimental Results
Reproducibility Audit
Assumptions and Unknown Information
Dependencies
Implementation Phase Candidates
Phase Boundaries
Verification Specification
Paper → Implementation Traceability
Reproducibility and Implementation Gap Matrix
Risks
Weaknesses and Limitations
Improvement Recommendations
Engineering Implementation Guidance
Proposed Repository Structure
Documentation Requirements
Final Technical Assessment
GSD Handoff
Add subsections whenever required by the paper.
Do not omit technically important material merely to keep the document short.
================================================================
37. WRITING STYLE
The report MUST be:
•	technically rigorous
•	implementation-oriented
•	precise
•	evidence-based
•	readable
•	logically structured
•	educational
•	concise where possible
•	detailed where necessary
Use:
•	Markdown
•	tables
•	Mermaid diagrams
•	numbered requirements
•	structured identifiers
•	code blocks for pseudocode
•	LaTeX equations where appropriate
Avoid:
•	vague statements
•	marketing language
•	generic AI terminology
•	unnecessary academic verbosity
•	unsupported claims
•	invented implementation details
•	repetition
Explain difficult concepts clearly without weakening their technical meaning.
================================================================
38. CRITICAL FINAL CHECK
Before producing the final report, verify internally:
1.	Did I read the complete paper?
2.	Did I inspect equations, algorithms, figures, and tables?
3.	Did I distinguish paper facts from inference?
4.	Did I identify missing implementation information?
5.	Did I identify reproducibility gaps?
6.	Did I extract explicit requirements?
7.	Did I assign stable identifiers?
8.	Did I identify dependencies?
9.	Did I identify implementation blockers?
10.	Did I derive realistic implementation phases?
11.	Did I define phase completion evidence?
12.	Did I define verification requirements?
13.	Did I preserve the paper's actual methodology?
14.	Did I avoid fabricating results or technical details?
15.	Did I clearly separate reported results from independently reproduced results?
16.	Did I identify assumptions?
17.	Did I identify weaknesses and risks?
18.	Did I produce the GSD Handoff section?
19.	Could another AI use this document to construct a GSD roadmap without having to rediscover the paper from scratch?
If any answer is "no", correct the report before producing the final output.
================================================================
39. OUTPUT
Output exactly ONE complete Markdown document.
The document must be immediately usable as:
PROJECT_REPORT.md
Do not include introductory commentary outside the Markdown document.
Do not say "Here is the report."
Do not provide meta-commentary.
The report itself is the complete output.
