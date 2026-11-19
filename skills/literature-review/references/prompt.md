# User Brief (verbatim)

This is the user's literature-review prompt, kept word for word. It governs the run. SKILL.md maps it to tools, files, and checks, and adds the lessons from test runs. Where SKILL.md is more specific, follow SKILL.md. Where they conflict, this brief wins. `@main.tex` means the manuscript identified in Phase 0.

---

# Comprehensive Literature Review and Evidence-Based Research Gap Identification

## 1. Role and Objective

Act as a senior academic researcher, systematic literature review specialist, and research-gap analyst with expertise in the scientific field addressed by my manuscript.

Your first task is to thoroughly understand the existing manuscript in `@main.tex`. Based on its actual research topic, objectives, proposed methodology, technical contributions, and claims, conduct a comprehensive, evidence-based literature review of the relevant research field.

The primary objective is to establish the current state of the art, identify what existing research has already accomplished, critically evaluate the limitations of previous studies, and determine whether genuine, defensible research gaps remain that could support a meaningful scientific contribution.

**This is a research-discovery and validation phase, not a paper-writing or implementation phase.**

Do not begin converting the manuscript to a journal-specific format, rewriting the paper, developing code, conducting experiments, or designing a new framework. Those activities will be addressed in later stages after the literature review has been completed and evaluated.

The final deliverable must be a comprehensive, well-structured Markdown document named `literature_review.md`.

## 2. Phase One: Understand the Existing Manuscript

Before searching the literature, carefully read the entire `@main.tex` file from beginning to end.

If the manuscript references a bibliography file, figures, tables, appendices, supplementary materials, or other project files that are available, inspect them when relevant.

Extract and document the following:

1. The primary research problem and the motivation behind it.
2. The research objectives, questions, hypotheses, and intended outcomes.
3. The central concepts, theoretical foundations, and technical terminology.
4. The proposed approach, architecture, framework, model, or methodology.
5. The specific contributions and novelty claims made in the manuscript.
6. The assumptions, constraints, application domains, and evaluation criteria.
7. The related work already discussed and the references already cited.
8. The limitations acknowledged by the authors.
9. The claims that require independent verification against existing literature.
10. The differences between what the manuscript actually demonstrates and what it merely proposes or anticipates.

Do not accept the manuscript's novelty claims or descriptions of existing research as established facts. Treat them as claims that must be independently verified.

Develop a concise research profile from this analysis. Use it to define the scope of the literature review and guide the subsequent search.

## 3. Phase Two: Conduct a Comprehensive Literature Search

Conduct a structured, reproducible, and sufficiently broad search of the relevant research field.

Use available academic search engines, scholarly databases, publisher websites, bibliographic metadata services, and other credible scientific sources. Depending on the topic and available access, consider:

- Google Scholar
- Semantic Scholar
- OpenAlex
- Crossref
- Scopus
- Web of Science
- IEEE Xplore
- ACM Digital Library
- SpringerLink
- ScienceDirect
- Wiley Online Library
- PubMed
- arXiv and other relevant preprint repositories

Select databases that are appropriate for the manuscript's discipline. Do not claim to have searched a database or accessed a paper unless you actually did so.

### 3.1 Search strategy

Develop targeted search queries covering:

- The manuscript's primary research topic.
- Synonyms, alternative terminology, and related concepts.
- Foundational theories, methods, algorithms, and architectures.
- Closely related research problems and competing approaches.
- Existing frameworks and their demonstrated capabilities.
- Known limitations, trade-offs, and failure cases.
- Evaluation methods, benchmarks, datasets, and performance measures.
- Recent developments and emerging approaches.
- Research that challenges, contradicts, or qualifies the manuscript's assumptions.

Use Boolean operators, phrase searches, terminology variants, and forward and backward citation tracking where supported.

Include both foundational research and recent publications. Prioritize the most recent relevant literature available at the time of the search without excluding older studies that established essential concepts or methods.

Record the date on which the search was conducted and the actual search scope.

### 3.2 Source selection

Prioritize:

1. Peer-reviewed journal articles and conference papers relevant to the field.
2. Original research papers that introduce, implement, or empirically evaluate important methods.
3. Systematic reviews, surveys, and meta-analyses that provide broader field-level evidence.
4. Authoritative standards, official technical reports, and institutional publications when relevant.
5. Preprints when they provide important recent developments not yet available in peer-reviewed publications.

Do not treat all sources as equally reliable. Clearly distinguish peer-reviewed research from preprints, technical reports, opinion pieces, and other non-peer-reviewed material.

Use primary research whenever possible to validate specific technical claims. Use reviews to understand broader trends, taxonomies, disagreements, and research directions.

Do not rely solely on search-engine snippets, abstracts, secondary summaries, or AI-generated summaries when stronger evidence is available. Examine the full text of important papers whenever accessible. If the full text is unavailable, state what evidence was actually accessible.

### 3.3 Search completeness

Continue searching until the scope is adequately covered and additional searches produce diminishing returns. The objective is not to accumulate an arbitrary number of references. It is to build a sufficiently comprehensive evidence base for reliable conclusions.

Document the search process, including:

- Databases and repositories actually searched.
- Search queries and important variations.
- Search dates and publication date ranges.
- Inclusion and exclusion criteria.
- Screening and source-selection decisions.
- Any major access limitations or areas where the evidence remains incomplete.

Do not invent search counts, screening results, or systematic review statistics. If you use a formal systematic review process, report only the steps and counts that were actually performed and documented.

If a full PRISMA-style process is not feasible, describe the work honestly as a structured or comprehensive literature review rather than claiming compliance with a systematic review protocol.

## 4. Phase Three: Build a Verified Research Evidence Base

Create a structured evidence inventory of the most relevant and informative publications.

For each important paper, extract the following wherever the information is available:

| Field | Required information |
|---|---|
| Full reference | Complete, verified bibliographic citation |
| DOI or stable identifier | Verified DOI, publisher URL, or repository identifier |
| Publication details | Authors, title, venue, year, volume, issue, pages or article number when applicable |
| Research objective | Problem the study addresses |
| Research contribution | What the authors actually proposed, developed, or demonstrated |
| Methodology | Methods, models, architectures, experiments, or analytical techniques |
| Evaluation | Datasets, benchmarks, experimental setup, and evaluation metrics |
| Main findings | Results supported by the original publication |
| Limitations | Limitations explicitly reported or demonstrated by the available evidence |
| Relationship to our manuscript | Direct relevance to the research question, methodology, or contribution |
| Verification status | What was verified and which details remain uncertain |

Every substantive entry must be traceable to its source.

Distinguish carefully between:

- Findings explicitly reported by the original authors.
- Interpretations supported by the reported evidence.
- Your own critical analysis of the paper.
- Information that could not be verified.

Do not infer experimental results from an abstract when the necessary details are unavailable. Do not assign a study's limitations to its authors unless the paper supports that interpretation. Analytical limitations may be identified separately, with a clear explanation of the evidence and reasoning behind them.

## 5. Phase Four: Critically Synthesize the Literature

Do not produce a simple paper-by-paper summary. Organize the literature into meaningful research themes based on the manuscript's actual subject.

For each major theme:

1. Explain the central research problem and why it matters.
2. Describe the principal approaches that researchers have used.
3. Compare representative studies and their contributions.
4. Identify areas of agreement and disagreement.
5. Compare methodologies, assumptions, technical capabilities, and evaluation practices.
6. Identify recurring limitations and unresolved trade-offs.
7. Explain how the approaches have evolved over time.
8. Identify competing explanations or methods that challenge the dominant approach.
9. Assess which problems have already been addressed successfully.
10. Explain the implications for the research problem in `@main.tex`.

Where appropriate, construct comparative tables to make differences explicit.

Avoid generic statements such as "existing studies lack scalability," "few studies address explainability," or "there is limited research on this topic" unless the evidence supports them.

When comparing studies, consider whether their research objectives, experimental settings, datasets, assumptions, and evaluation criteria are sufficiently similar to permit a fair comparison.

Do not compare numerical performance values across incompatible experiments without explaining the limitations.

## 6. Phase Five: Identify and Validate Genuine Research Gaps

This is the most important part of the entire task.

Identify research gaps that are directly relevant to the manuscript and could potentially support a meaningful original contribution.

Do not invent gaps simply to make the manuscript appear novel. Do not assume that a topic is unexplored because a few search queries returned limited results. Do not confuse an author's future-work statement with proof that a genuine field-wide gap exists.

Examine potential gaps across relevant dimensions, including:

- Theoretical and conceptual limitations.
- Methodological shortcomings.
- Technical and architectural constraints.
- Missing empirical validation.
- Generalization and external validity.
- Scalability, robustness, reliability, and efficiency.
- Evaluation and benchmarking limitations.
- Data availability, reproducibility, and reporting quality.
- Security, privacy, safety, and failure handling.
- Explainability, transparency, and accountability.
- Human oversight, governance, and operational constraints.
- Real-world deployment and domain-specific requirements.
- Conflicting results and unresolved scientific questions.

These are possible analytical dimensions, not mandatory gaps. Investigate only those relevant to the manuscript's field.

### 6.1 Required evidence for every proposed gap

For each candidate research gap, provide:

**A. Gap statement:** Express the unresolved problem precisely and narrowly.

**B. Supporting evidence:** Cite multiple relevant studies when available. Explain what their actual findings, methods, limitations, or evaluation designs reveal about the gap.

**C. Counterevidence:** Search for studies that may already address the proposed gap. Include contrary evidence, competing methods, and recent advances that weaken the claim.

**D. Existing solutions:** Explain how much of the problem has already been solved and under which conditions.

**E. Residual uncertainty:** Identify what remains unresolved after accounting for existing solutions.

**F. Research significance:** Explain why the unresolved issue matters scientifically or practically.

**G. Potential research direction:** Describe a plausible way the problem could be investigated without prematurely designing or implementing the solution.

**H. Verification confidence:** Classify the gap as strongly supported, moderately supported, tentative, or unsupported, and justify the classification.

**I. Novelty risk:** Explain how likely it is that a similar contribution already exists and which additional searches or comparisons are needed to resolve that risk.

**J. Relationship to `@main.tex`:** State whether the manuscript already addresses the gap, partially addresses it, or leaves it unresolved.

**K. Appropriate claim boundary:** Specify exactly what can be claimed based on the evidence and what would require further investigation.

### 6.2 Distinguish gap categories

Classify each candidate into one of the following categories:

1. **Established research gap:** Multiple sources provide convincing evidence of an unresolved problem, and the available literature does not reveal an adequate existing solution within the defined scope.
2. **Context-dependent gap:** Existing methods address the problem in some settings but have demonstrated limitations under specific assumptions, environments, or requirements.
3. **Emerging research gap:** Recent developments create a newly relevant problem that has not yet received sufficient investigation, supported by a verified search of recent research.
4. **Potential or tentative gap:** The available evidence suggests a possible limitation, but the literature search is insufficient to establish its novelty.
5. **Unsupported or resolved gap:** Evidence is inadequate, or existing research already addresses the issue sufficiently within the claimed scope.

Do not present tentative gaps as established facts. Do not recommend unsupported or resolved gaps as the primary novelty claim.

### 6.3 Research-gap evidence matrix

Create a table containing at least the following columns:

| Candidate gap | Supporting studies | Counterevidence or existing solutions | Remaining unresolved issue | Relevance to manuscript | Confidence | Novelty risk |
|---|---|---|---|---|---|---|

Every row must be grounded in identified sources. Use concise source identifiers linked to complete references in the bibliography.

If no strong research gap is supported by the evidence, state that conclusion explicitly. Recommend refining the research question, narrowing the scope, or conducting further investigation rather than manufacturing novelty.

## 7. Phase Six: Evaluate the Manuscript's Novelty and Research Positioning

Compare the manuscript's claimed contributions against the closest existing studies.

Identify the most relevant competing or overlapping work, including papers that may have been published after the manuscript's existing bibliography was assembled.

For each claimed contribution, assess:

- What is already known.
- What existing studies have demonstrated.
- What is genuinely different about the manuscript's approach.
- Whether the difference is substantive, incremental, methodological, contextual, or primarily presentational.
- Whether the current manuscript provides sufficient evidence for the claim.
- Which experiments, theoretical arguments, comparisons, or clarifications would be required to establish the claim more convincingly.

Produce a novelty assessment table with the following columns:

| Manuscript claim | Closest related work | Verified similarities | Potentially distinctive aspect | Evidence required | Current assessment |
|---|---|---|---|---|---|

Do not equate combining existing technologies, changing an application domain, adding a new label, or rearranging known components with a strong scientific contribution unless the combination produces a demonstrable, meaningful advantage.

Distinguish between conceptual novelty, methodological novelty, empirical novelty, and application-specific contribution.

Conclude with a carefully qualified assessment of whether the manuscript's current positioning appears defensible, needs refinement, or faces substantial overlap with existing work. This is a preliminary literature-based assessment, not a guarantee of originality or acceptance.

## 8. Phase Seven: Verify Every Reference and Citation

Reference authenticity is a strict requirement.

**Never fabricate a paper, author, title, publication venue, publication year, DOI, URL, volume, issue, page range, article number, quotation, experimental result, or bibliographic detail.**

For every source included in the final bibliography:

1. Confirm that the publication exists using an authoritative or otherwise credible scholarly record.
2. Check the title and author list against the publisher's page, an official repository, or a reliable bibliographic record.
3. Verify the publication year and venue.
4. Verify the DOI or stable URL when available.
5. Confirm that the source actually supports the specific claim for which it is cited.
6. Check whether the source is a preprint, peer-reviewed publication, corrected version, retraction, or other publication status, whenever verifiable.
7. Check for duplicate records, duplicate versions, corrections, and retractions where relevant.
8. Preserve the original meaning of the authors' findings. Do not attribute a claim to a source based only on its title.
9. Record unresolved discrepancies instead of guessing which metadata is correct.

Use DOI resolver pages, Crossref metadata, official publisher pages, and authoritative repositories as appropriate. These services can help verify publication records, but bibliographic metadata alone does not establish that a paper supports a scientific claim. Content-level verification is also required.

When a DOI is unavailable, use a verified stable publisher or repository URL. Never construct a DOI or guess a URL.

### 8.1 Citation integrity

Use consistent author-year citations or numbered citations throughout the document, with complete matching bibliography entries.

Every important factual assertion, comparison, research-gap statement, and claim about previous studies must have appropriate supporting citations.

For direct quotations, verify the exact wording and provide a page number or another precise locator when available. Prefer paraphrasing the source accurately.

Citations must support the statements immediately associated with them. A citation to a broad review is not sufficient when the claim requires evidence from a specific experiment or primary study.

If a reference cannot be verified adequately, exclude it from the confirmed bibliography or place it in a separate section clearly labeled "Unverified Sources Requiring Manual Verification." Explain what could not be verified and why.

Do not silently fill missing metadata with plausible guesses. Do not describe the entire document as fully verified if even one material claim or citation remains unresolved.

## 9. Phase Eight: Write the Final `literature_review.md`

Create a detailed, publication-quality Markdown document with the following structure:

1. **Title and Review Metadata**
   - Review title.
   - Manuscript examined.
   - Date of review.
   - Search cutoff date.
   - Scope and limitations.

2. **Executive Summary**
   - Research problem.
   - Main findings from the literature.
   - Strongest candidate research gaps.
   - Preliminary novelty assessment.
   - Recommended priorities for further research.

3. **Understanding the Original Manuscript**
   - Research objectives and questions.
   - Proposed methodology and claimed contributions.
   - Core assumptions and novelty claims.

4. **Review Scope and Methodology**
   - Research questions guiding the review.
   - Databases and sources actually searched.
   - Search queries and date ranges.
   - Inclusion and exclusion criteria.
   - Screening and verification procedures.
   - Known limitations of the search process.

5. **Background and Conceptual Foundations**
   - Definitions and terminology.
   - Essential theories, concepts, and technical foundations.

6. **Comprehensive Thematic Literature Review**
   - Major research themes.
   - Foundational studies.
   - Recent developments.
   - Comparative analysis.
   - Agreements, disagreements, and unresolved technical questions.

7. **Critical Comparison of Existing Approaches**
   - Comparative tables.
   - Methods, assumptions, results, limitations, and evaluation differences.

8. **Established Knowledge and Solved Problems**
   - Problems already addressed.
   - Existing techniques and their conditions of applicability.
   - Areas in which the manuscript must not overstate novelty.

9. **Evidence-Based Research Gaps**
   - Detailed analysis of each candidate gap.
   - Supporting evidence and counterevidence.
   - Existing solutions and remaining limitations.
   - Confidence and novelty-risk assessments.

10. **Research-Gap Evidence Matrix**
    - A concise comparison of all significant candidate gaps.

11. **Novelty and Contribution Assessment**
    - Claim-by-claim comparison with the closest related research.
    - Overlap, differentiation, and evidence requirements.

12. **Recommended Research Directions**
    - The most promising defensible research directions.
    - The scientific questions worth investigating.
    - What would need to be demonstrated to support each contribution.
    - Risks, prerequisites, and unresolved assumptions.

13. **Implications for the Existing Manuscript**
    - Claims requiring correction or qualification.
    - Missing related work.
    - Potential revisions to research questions and contribution statements.
    - Additional evidence or evaluation needed.
    - Areas where the current approach may overlap with existing work.

14. **Limitations of This Literature Review**
    - Database coverage.
    - Full-text access.
    - Search and screening limitations.
    - Remaining uncertainties and unverified claims.

15. **Complete Verified References**
    - Full bibliographic details for every cited source.
    - Verified DOI or stable URL when available.
    - Clear identification of preprints or other non-peer-reviewed sources.

16. **Unverified Sources and Open Questions**
    - Sources that could not be fully verified.
    - Outstanding metadata discrepancies.
    - Important questions that require additional searches or manual inspection.

17. **Reproducibility Appendix**
    - Search strings.
    - Search dates.
    - Selection criteria.
    - Verification notes and other relevant methodological details.

Adapt the structure to the actual research topic. Remove irrelevant subsections, and add topic-specific sections when necessary.

The final document must contain the actual review, comparisons, evidence, and full references, not merely a plan or outline.

## 10. Phase Nine: Final Quality-Control Audit

Before declaring the task complete, audit the entire `literature_review.md` file.

### Scientific accuracy
- Are the research topic, terminology, and technical explanations accurate?
- Are claims consistent with the original sources?
- Are results, limitations, and contributions represented fairly?
- Are disagreements and contradictory findings acknowledged?
- Are speculative conclusions explicitly labeled?

### Research-gap validity
- Is each major gap supported by evidence?
- Have relevant existing solutions and counterexamples been investigated?
- Are the gaps specific enough to guide meaningful research?
- Are resolved and tentative gaps clearly distinguished?
- Is the claimed novelty limited to what the evidence supports?

### Reference integrity
- Does every in-text citation have a matching reference entry?
- Is every cited reference associated with a real publication or explicitly identified scholarly record?
- Have titles, authors, years, venues, DOIs, and URLs been checked?
- Have duplicate, retracted, corrected, and superseded records been handled appropriately?
- Are all unsupported or unverifiable sources clearly disclosed?

### Coverage and reproducibility
- Does the review cover foundational and recent relevant work?
- Does it include the closest competing approaches?
- Are the search methods and limitations documented honestly?
- Could another researcher reproduce the main search steps?
- Are any important research themes or counterarguments missing?

### Deliverable integrity
- Is the document saved as `literature_review.md`?
- Is the Markdown structure clean and readable?
- Are tables, citations, and references consistent?
- Does the file contain a complete literature review rather than superficial summaries?
- Are unresolved issues explicitly documented?

Correct all identified problems before delivering the file. If a problem cannot be resolved with the available tools or sources, document it instead of concealing it.

## 11. Working Rules and Constraints

Follow these rules throughout the task:

1. **Accuracy takes priority over completeness.** A smaller verified evidence base is preferable to a longer bibliography containing questionable references.
2. Never invent facts to fill gaps in the evidence.
3. Never fabricate citations or bibliographic metadata.
4. Never infer that a research gap exists solely because a search returned few results.
5. Never misrepresent an author's findings, conclusions, or limitations.
6. Never treat correlation as causation or reported performance as independently established fact.
7. Never claim to have read full papers, searched databases, or verified metadata when you have not.
8. Clearly distinguish evidence, interpretation, uncertainty, and recommendation.
9. Use American English throughout the document.
10. Write in clear, precise academic language. Avoid unnecessary jargon, repetition, vague claims, and unsupported superlatives.
11. Preserve the original manuscript. Do not modify `@main.tex`, existing bibliography files, code, datasets, or other project files.
12. Do not begin implementation, coding, experiments, journal selection, journal-specific formatting, or manuscript conversion during this phase.
13. Do not stop after producing an outline, a preliminary search, or a generic summary. Complete the review to the extent supported by available resources.
14. If a tool, database, or full-text source is unavailable, continue with the available evidence and explicitly document the limitation.
15. Do not claim absolute certainty. Scientific literature searches have boundaries, and the review must make those boundaries transparent.

## 12. Final Deliverable and Completion Report

Save the completed review as:

`literature_review.md`

Place it in the current project directory alongside `main.tex`, unless the environment requires a different output location. Do not overwrite an existing file without first checking its contents and preserving any valuable work.

After creating the file, provide a concise completion report stating:

- The exact location of the Markdown file.
- The research themes covered.
- The number of publications actually included and verified, distinguishing fully verified records from partially verified ones.
- The number of candidate research gaps identified, separated by confidence category.
- The major limitations encountered.
- Any important unresolved verification issues.

Report only counts and actions that were actually completed. Do not exaggerate the review's depth, coverage, or verification status.

**Final instruction:** The purpose of this phase is to establish a trustworthy scientific foundation for all subsequent work on the manuscript. Prioritize evidence over assumptions, critical synthesis over superficial summaries, and defensible research gaps over novelty claims that merely sound impressive. The next phase will begin only after `literature_review.md` has been completed and its findings are available for review.

---

## Amendments from the first test run (2026-11-15)

These additions came from running this brief on an IEEE JSTARS manuscript (an agentic urban water digital twin). They extend the brief and do not replace any of its rules.

1. **Phase One, audit what produced the results.** When code or data are available, trace every headline number to the code that produces it. Report plainly when a "result" is an input parameter plus noise, or a table written as literal values. In the test run, the paper's 4.8% vs 66.2% attack result was a pair of hand-set block probabilities, and its ablation was a constant table that contradicted the main table.
2. **Phase One, check the manuscript's own bibliography with the same rigor as new sources.** The test manuscript had a wrong first author, a nonexistent DOI, and a wrong year among 23 entries.
3. **Phase Two, one dedicated counterevidence search per candidate gap, plus a neighboring-field sweep.** State the same problem in an adjacent community's words (for example, power-grid or robotics agents for a water paper). In the test run these searches found the closest competitor of the whole review.
4. **Phase Three, plan for abstract-level access.** Publisher pages often block automated reading. Say early which access level the review reached, limit claims to what abstracts state, and never use AI-generated summaries (such as search-engine "TLDRs") as evidence.
5. **Phase Five, a resolved gap is still a finding.** When existing work already solves a proposed contribution, record it as an "Unsupported or resolved gap" with the competing work, so the author sees the overlap.
6. **Phase Eight, every number the review states about its own process comes from a log.** That covers queries run, titles screened, sources by status, and access levels. Hand-typed counts were the only factual slip in the test run.
7. **Completion report, add the novelty verdict in one sentence**, next to the gap counts.

## Amendment 2: Source access and venue balance (2026-11-15)

These rules come from the author and apply to every run.

1. **Citing closed-access sources.** A closed-access publication does not need to be read in full before it is cited. Retrieve whatever the publisher or index makes available (title, author list, venue, year, DOI, abstract, highlights, keywords) and cite the source only for what that material states. A source known from its abstract may support a finding the abstract reports. A source known only from its bibliographic record may support only its existence and topic. When the author's own institutional access exposes the full text, use it and record full-text access.
2. **Balance of closed-access and open-access venues.** The final bibliography should draw roughly equally on closed-access venues (subscription and hybrid journals and proceedings) and open-access venues (fully open-access journals and proceedings, open preprint servers, and freely available official reports). Aim for 40 to 60 percent from each class, with about 50 percent as the target.
   - Relevance and evidential quality decide inclusion first. The balance shapes which equally relevant sources are preferred. It never justifies adding a weak source or dropping a relevant one.
   - When the split falls outside the band, run targeted searches for equally relevant work in the under-represented class. If none exists, keep the imbalance and report it with the reason.
   - Report the final split (counts and percentages) in the review's methodology and in the completion report.
3. **Access barriers in the author's browser.** When a page in the author's browser shows a CAPTCHA, a human-verification check, or a sign-in prompt, do not attempt to solve or bypass it. Ask the author to clear it in the open tab, wait for confirmation, and then continue. If the author is unavailable, record the source at the access level already reached.
