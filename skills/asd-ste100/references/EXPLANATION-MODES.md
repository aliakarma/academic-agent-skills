# Explanation modes

Choose the mode from the material, not from habit. A paper can need two modes, for example "research paper" plus "AI architecture". Keep a section only when the source gives content for it. Never add an empty section to complete a template.

The headings in this file are suggestions written in approved STE words or common technical nouns. Adapt them to the subject, then check them with `ste_tool.py`. Notes in brackets are for you, not for the page.

## How to choose

| The material is | Mode | Recognize it by |
|---|---|---|
| A paper with method, experiments, results | Research paper | Abstract, method section, results tables |
| A concept paper, proposal, or position paper | Research paper, proposal variant | "will", "planned", "we propose", no measured results |
| A survey or literature review | Research paper, survey variant | Taxonomy, many cited works, comparison tables |
| One concept, theory, or term | Concept | A request such as "explain X" with no source document |
| A project, product, or system under development | Research project | Repository, README, design notes, plans |
| An agentic AI or multi-agent system | AI architecture | Agents, tools, memory, orchestration, messages |
| An algorithm or a set of equations | Algorithm | Pseudocode, update rules, objective functions |
| Source code | Code | Files in a repository, a script, a notebook |
| Two or more methods | Comparison | "compare", "difference", "versus" |

## Source references

- PDF: page number plus section, figure, table, or equation number: "(Section 3.2, page 4)" or "(Table 2, page 7)".
- LaTeX: there are no page numbers. Use the section number and title, and figure, table, and equation numbers in the order that LaTeX gives them. IEEEtran uses Roman numerals for sections and tables. Keep `.tex` line numbers in `_qa/source-map.md` for your own checks. If page numbers are necessary, compile a copy in the scratchpad, never in the user's folder, and call them "page in the compiled PDF".
- Code: file path and line numbers: "(src/monitor.py, lines 40-72)".
- Web or general knowledge: give only sources that you opened in this run. If there is no source, say on the page that the text is general background.

## Research paper

Use the sections in this order when the source supports them. Merge or drop sections that the source does not support.

| No. | Section | Suggested heading | Content |
|---|---|---|---|
| 1 | Paper overview | The problem and the solution | The question, the problem, its effect, the aim, and the primary contribution. A lead paragraph that a reader can read alone. |
| 2 | Research background | Known methods and their problems | What is known, what known methods can do, the gap that the authors identify, and why new work is necessary. Define terms before later sections use them. |
| 3 | Important concepts | Important terms | One card for each difficult term: the exact term, a simple definition, its function in the paper, and an example. |
| 4 | Method | How the method operates | Each component: what it is, why it is there, how it operates, its input, its output, and its connections. Do not skip method details. |
| 5 | Architecture | The parts and how they connect | An interactive diagram of the real components and flows, the sequence of operation, and the decision logic. |
| 6 | Mathematics | The equations | Each important equation with the original notation, every symbol, each term, the purpose, the intuition, the connection to the method, and a worked example when it helps. |
| 7 | Experimental setup | Tests and data | Datasets, baselines, metrics, configurations, training, testing, implementation facts, and why each choice matters. |
| 8 | Results | Results | Reported values only, with charts from those values. What the values show, which method is better under which metric, what the metric measures, the conclusion of the authors, and what the results do not show. |
| 9 | Limitations and future work | Remaining problems | Limitations that the authors give (callout "From the source"), assumptions, open problems, and future work. Your own analysis goes in a "Not from the source" callout. |
| 10 | Overall understanding | All parts together | The central contribution, why it is useful, and the most important technical insight, in connected sentences. |
| 11 | Glossary | Glossary | Every technical term: the term, a simple definition, its function in the paper, and an example when useful. |
| | Final section | Important items to know | Three to seven items, each with one idea. |
| | References | Sources | The source document and any reference that the page cites, exactly as the source gives them. |

Proposal variant (concept papers, proposals, protocols): the work is planned, not done.

- Write planned work in the future tense ("The study will compare ..."). Never use the past tense or the present tense for planned work.
- Rename section 7 to "The tests that the authors will do". Replace section 8 with a gap callout: "The source does not give results." Keep hypotheses and expected effects as hypotheses, with the words of the source.
- Never draw a results chart. A chart of planned metrics is a table of names and definitions, with no values.

Survey variant: add a taxonomy diagram (concept map), a timeline when the survey is historical, and a comparison table with the columns that the survey uses. Research gaps are the gaps that the authors state. Do not add surveyed works that the source does not cite.

## Concept

| Section | Suggested heading |
|---|---|
| What it is | The function of [term] |
| Why it exists and what problem it solves | The problem and the solution |
| How it works | How [term] operates |
| Main components | The primary parts |
| Practical example | An example |
| Advantages and limitations | Where [term] helps and where it does not help |
| Applications | Examples [list the applications] |
| Related concepts | Related terms |

Visuals: a concept diagram or a flowchart, and one interactive example (a diagram with selectable parts, or a small worked example).

## Research project

| Section | Suggested heading |
|---|---|
| Overview, problem statement, motivation | The problem and the solution |
| Objectives | The tasks of the project |
| Proposed solution and main components | The parts and how they connect |
| Workflow | The sequence of operation |
| Technical implementation | Tools and software |
| Expected results | Results that the team wants to get [label them as expected, never as measured] |
| Challenges and limitations | Remaining problems |
| Future improvements | Next steps |

Visuals: an architecture diagram, a workflow flowchart, and a timeline when the project has phases.

## AI architecture

For each agent or subsystem, give: its task, its tools and data, its input and output, the messages it sends and receives, its decision logic, the control that limits it, and its feedback loops.

| Section | Suggested heading |
|---|---|
| Purpose of the system | The problem and the solution |
| Agents and responsibilities | The agents and their tasks |
| Tools and resources | Tools and data for each agent |
| Communication and data flow | Communication between agents |
| Decision processes | How the system makes decisions |
| Control mechanisms, feedback loops | How the system controls its agents |
| End-to-end run | The full sequence |

Visuals: an interactive architecture diagram (one node for each agent, tool, and store), a sequence diagram for one request, and a decision flowchart for each gate or policy.

## Algorithm

| Section | Suggested heading |
|---|---|
| Problem | The problem |
| Input and output | Input and output |
| Core idea | How the algorithm operates |
| Step-by-step operation | Step by step |
| Pseudocode | Pseudocode [exact, in `<pre><code>`] |
| Mathematical formulation | The equations |
| Time and space complexity | Time and memory [only when the source gives it or you can derive it, and say which] |
| Practical example | An example with numbers |
| Advantages and limitations | Where the algorithm helps and where it does not help |

Visuals: a flowchart of the loop, and a step table that shows the state after each step of a small example.

## Code

Identify the language, the purpose, the architecture, the important functions and classes, the execution order, the inputs and outputs, and the dependencies. Explain the difficult parts. Do not modify the code. Run code only if it is safe, needs no install, and changes no files, and say that you ran it.

| Section | Suggested heading |
|---|---|
| Overall purpose | The function of the program |
| Architecture | Files and their functions |
| Execution order | The sequence of operation |
| Important functions and classes | Important functions and classes [declare "function" and "class" as technical nouns, category 19] |
| Inputs, outputs, dependencies | Inputs, outputs, and dependencies |
| Difficult sections | Parts of the code that are not easy |
| Execution example | Example: one operation of the program |

Visuals: a module diagram, a call-sequence flowchart, and exact code excerpts with copy buttons.

## Comparison

Do not say that two methods are equivalent unless the source shows it. Compare only on dimensions that the sources support, and give the source of each cell.

| Section | Suggested heading |
|---|---|
| Methods | The methods |
| How each works | How each method operates |
| Architectural differences | Important differences |
| Strengths and weaknesses | Where each method helps and where it does not help |
| Suitable applications | Which method to use for each task |
| Comparison table | Methods compared |

Visuals: a side-by-side diagram with the same layout for each method, and a comparison table.

## Words to avoid in headings

"What", "why", "overview", "summary", "introduction", "conclusion", "objectives", "purpose", "advantages", "limitations", "key", and "points" are not approved, or have a different approved meaning. The suggested headings above avoid them.
