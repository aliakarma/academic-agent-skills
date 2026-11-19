# literature_review.md Template

Copy this skeleton into `<project>/literature_review.md` and replace every `<...>` slot with content. `scripts/check_review.py` enforces the parts marked REQUIRED. Section headings are `## N. Name`. Keep the numbers and names so the checker and later skills can find them. You may add subsections, and you may drop a subsection that does not apply as long as you write one line saying why.

## Citation convention (REQUIRED)

- Cite with the ledger `source_id` (the BibTeX key) in square brackets: `[wang2026epanet]`, several as `[wang2026epanet; mu2026leakagent]`. Never use bare numbers like `[3]`. The checker treats any `[lowercase+digits...]` token as a citation.
- Every cited key has exactly one entry in Section 15 (verified) or Section 16 (unverified). A body sentence that rests on a Section 16 source says so in the sentence ("an unverified preprint reports ...").
- Mark what kind of statement a sentence is when it matters: what the authors report, what you infer from it ("This suggests ..."), and what you could not check ("not verifiable from the abstract").

---

```markdown
# <Review title>

## 1. Title and Review Metadata

| Field | Value |
|---|---|
| Manuscript examined | `<path>` (<title>), <N> pages, <N> references in `<bib>` |
| Date of review | <YYYY-MM-DD> |
| Search cutoff date | <YYYY-MM-DD> (last executed query) |
| Review type | Structured literature review (not a PRISMA systematic review) |
| Scope | <topics in scope> |
| Out of scope | <topics excluded and why> |
| Tools actually used | <e.g. WebSearch, Crossref API, OpenAlex API, arXiv API, WebFetch> |
| Tools unavailable or failed | <e.g. Scopus (no access), IEEE Xplore (blocked scripted access)> |

## 2. Executive Summary

<Research problem in 2-3 sentences.>

**Main findings.** <3-6 findings, each with citations.>

**Strongest candidate gaps.** <G-ids, category, and confidence for each.>

**Preliminary novelty assessment.** <defensible / needs refinement / substantial overlap, and why in two sentences.>

**Priorities.** <numbered list>

## 3. Understanding the Original Manuscript

### 3.1 Research profile
| Item | Manuscript says | Location |
|---|---|---|
| Problem and motivation | | Sec. |
| Objectives / research questions | | |
| Central concepts | | |
| Proposed approach | | |
| Claimed contributions | C1 ... Cn | |
| Assumptions and constraints | | |
| Evaluation criteria | | |
| Acknowledged limitations | | |

### 3.2 Claims requiring verification
| ID | Claim (quoted or close paraphrase) | Location | Type (novelty, prior-work description, empirical, positioning) | Tested in |
|---|---|---|---|---|
| M1 | | | | Sec. 9/11 |

### 3.3 Demonstrated versus proposed
<What the manuscript shows with evidence versus what it only designs, formalizes, or anticipates.>

### 3.4 Existing bibliography check
<Result of verify_refs.py on the manuscript's bib: how many MATCH, PARTIAL, MISMATCH, not found. Problems found, by key. Whether the manuscript's descriptions of its cited works match those works.>

## 4. Review Scope and Methodology

### 4.1 Review questions
RQ-L1 ... RQ-Ln

### 4.2 Sources actually searched
<Platform, how accessed, date. Say which listed databases were NOT searched.>

### 4.3 Search strategy
<Concept table and query families. Full strings go to Section 17.>

### 4.4 Inclusion and exclusion criteria

### 4.5 Screening and verification procedure
<Counts only from the ledger and search log: executed queries, unique records screened, included, excluded (top reasons), and the closed-access versus open-access venue split. Say "not recorded" for anything you did not count.>

### 4.6 Known limitations of the search

## 5. Background and Conceptual Foundations
<Definitions with citations. Foundational works.>

## 6. Comprehensive Thematic Literature Review

### 6.N <Theme name>
<For each theme: the problem and why it matters, principal approaches, comparison of representative studies, agreement and disagreement, evaluation practices, recurring limitations, evolution over time, competing approaches, what is solved, implications for the manuscript. Prose that compares, not one paragraph per paper.>

## 7. Critical Comparison of Existing Approaches

| Study | Problem | Method | Data / setting | Evaluation | Reported result (with conditions) | Limitations (author-stated / reviewer) | Access |
|---|---|---|---|---|---|---|---|

<Caveats on comparability of the numbers.>

## 8. Established Knowledge and Solved Problems
| Problem | Solved by | Conditions of applicability | What the manuscript must not claim |
|---|---|---|---|

## 9. Evidence-Based Research Gaps

### G1: <short name>
- **Category:** <Established research gap | Context-dependent gap | Emerging research gap | Potential or tentative gap | Unsupported or resolved gap>
- **A. Gap statement:**
- **B. Supporting evidence:**
- **C. Counterevidence:**
- **D. Existing solutions:**
- **E. Residual uncertainty:**
- **F. Research significance:**
- **G. Potential research direction:**
- **H. Verification confidence:** <Strongly supported | Moderately supported | Tentative | Unsupported> because ...
- **I. Novelty risk:** <Low | Medium | High> because ... Searches still needed: ...
- **J. Relationship to the manuscript:** <Addressed | Partially addressed | Unresolved> ...
- **K. Appropriate claim boundary:** May claim: "..." Requires further investigation: ...
- **Examined:** <source_ids and search_ids used to establish this gap>

## 10. Research-Gap Evidence Matrix

| Candidate gap | Supporting studies | Counterevidence or existing solutions | Remaining unresolved issue | Relevance to manuscript | Confidence | Novelty risk |
|---|---|---|---|---|---|---|

## 11. Novelty and Contribution Assessment

| Manuscript claim | Closest related work | Verified similarities | Potentially distinctive aspect | Evidence required | Current assessment |
|---|---|---|---|---|---|

<Novelty type per claim: conceptual, methodological, empirical, or application-specific. Then the qualified overall verdict.>

## 12. Recommended Research Directions
<Per direction: the question, what must be demonstrated, risks and prerequisites. No designs or code.>

## 13. Implications for the Existing Manuscript

### 13.1 Claims requiring correction or qualification
| Location | Current wording | Problem | Evidence | Suggested boundary |
|---|---|---|---|---|

### 13.2 Missing related work
### 13.3 Possible revisions to research questions and contributions
### 13.4 Additional evidence or evaluation needed
### 13.5 Overlap risks

## 14. Limitations of This Literature Review

## 15. Complete Verified References

- **[key]** Authors (Year). Title. *Venue*, Vol(Issue), pages or article number. https://doi.org/<doi> (or stable URL). Status: VERIFIED | Peer review: peer-reviewed | Access: FULLTEXT | Venue: closed

## 16. Unverified Sources and Open Questions

### 16.1 Unverified Sources Requiring Manual Verification
- **[key]** <what is known>. Problem: <what could not be verified and why>.

### 16.2 Metadata discrepancies
### 16.3 Open questions

## 17. Reproducibility Appendix
<Search strings with platform, date, filters, and result counts as reported, or a pointer to literature/search_log.csv plus the key strings. Selection criteria. Verification notes.>
```

## Field vocabularies (REQUIRED)

| Field | Allowed values |
|---|---|
| Category | Established research gap, Context-dependent gap, Emerging research gap, Potential or tentative gap, Unsupported or resolved gap |
| H. Verification confidence | Strongly supported, Moderately supported, Tentative, Unsupported |
| I. Novelty risk | Low, Medium, High |
| J. Relationship | Addressed, Partially addressed, Unresolved |
| Reference Status | VERIFIED, VERIFIED-QUALIFIED (Section 15 only) |
| Peer review | peer-reviewed, preprint, report, standard, book, thesis, other |
| Access | FULLTEXT, ABSTRACT, METADATA |
| Venue | open, closed (see SKILL.md Venue Balance) |
