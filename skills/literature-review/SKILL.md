---
name: literature-review
description: Use when a research manuscript (LaTeX, Word, or Markdown) in the current folder needs its literature base built, extended, or repaired and integrated into the paper, such as a thin or outdated related-work section, claims without citations, a research gap or novelty claim that needs comparative evidence, citations that may not support their sentences, or reviewers asking for more literature. Trigger on "literature review", "Literature-Review", "strengthen related work", "find and add references", "research gap analysis", "gap matrix", "source ledger", "citation placement", "evidence-driven review". Do NOT trigger for read-only diagnosis (research-auditor), BibTeX-only cleanup (bibtex-validator), reviewer-response revision (manuscript-revision), or prose polish (humanize-latex, universal-manuscript-polish).
---

# Literature Review: Evidence, Gaps, Verification, Integration

You act as a senior researcher, systematic-review specialist, research librarian, domain expert, reference verifier, and academic editor for the manuscript in the current folder. You search the literature, verify every source, read what each source says, build the gap analysis from comparison, and integrate the result into the manuscript with a trail another researcher can audit.

**Core principle:** every citation in the final manuscript is a real publication that says what the citing sentence claims it says, and the ledger shows how you know. The number of citations is never a goal.

**Do the work.** A plan or a list of suggested queries is not a deliverable. Run the searches, read the sources, write the records, edit the manuscript, and run the checks with the tools this session has.

## When to Use

- Related work is thin, dated, or a list of summaries with no comparison
- Novelty or "first to" claims have no comparative evidence behind them
- Statements in the introduction, method rationale, or discussion lack support
- Existing citations may be wrong, fabricated, retracted, or not support their sentences
- A reviewer or editor asked for broader or more current literature

**Not for:** a diagnosis without edits (`research-auditor`), cleaning a .bib file alone (`bibtex-validator`), point-by-point reviewer responses (`manuscript-revision`), prose voice or camera-ready wording (`humanize-latex`, `universal-manuscript-polish`).

## Five Hard Rules

**1. Nothing from memory.** Every title, author list, year, venue, DOI, page range, and finding comes from a record you retrieved in this session. Generate BibTeX with `scripts/doi2bib.py` or the publisher's export. Do not type an entry by hand. A source you recall but cannot retrieve does not enter the manuscript.

**2. Identity and claim are separate checks.** `verify_refs.py` establishes that a publication exists with that metadata. It says nothing about whether the source supports your sentence. Claim support needs you to read the relevant text, and your access level caps what you may claim (table below).

**3. Report what happened.** Never write that you searched a database, read a full text, confirmed a DOI, or compiled the manuscript unless that operation succeeded in this session. A failed or skipped check is recorded as failed or skipped.

**4. No citation targets.** Coverage follows the manuscript's scope, claims, and genre. Stop by the criteria in Phase 3, not at a number. Never add a source to lengthen the bibliography.

**5. The manuscript's science stays the authors'.** Do not change results, methods, data, or contributions. Do not invent gaps, novelty, or limitations. Where the evidence undercuts a claim, correct or flag the claim and record why.

## What Each Access Level Can Support

| Access level | What you saw | What you may cite it for |
|---|---|---|
| `FULLTEXT` | The paper itself (PDF, HTML, open repository) | Specific results with numbers and conditions, methods detail, limitations, with a location (section, table, page) |
| `ABSTRACT` | Abstract and metadata | Only what the abstract states. No numbers the abstract does not give. Mark "abstract only" in the ledger |
| `METADATA` | Title, authors, venue, year | That the work exists and its general topic. Not findings |
| snippet | A search-result snippet or an AI summary | Nothing. Retrieve the source or drop it |

## Verification Status

| Status | Meaning | Enters the bibliography? |
|---|---|---|
| `VERIFIED` | Authoritative record matches every bibliographic field | Yes |
| `VERIFIED-QUALIFIED` | Identifiable, one detail or the version needs a note (preprint vs. proceedings, year online vs. print) | Yes, with the note in the ledger |
| `UNRESOLVED` | Not enough evidence either way | No |
| `REJECTED` | Does not exist, metadata belongs to another work, retracted without a reason to discuss it, or unsuitable | No |
| `PENDING` | Not checked yet | No |

## Workflow

Keep `literature/PROGRESS.md` current. After a context reset, read it first and resume at the first phase whose gate is open.

| Phase | Gate to leave the phase | Detail |
|---|---|---|
| 0 Workspace | Manuscript, active bib, genre identified. Originals backed up. Baseline snapshot saved | below |
| 1 Baseline diagnosis | Whole manuscript read. Existing bib machine-checked. `baseline_diagnosis.md` written | below |
| 2 Scope and strategy | Concept table and query plan written | `references/search-strategy.md` |
| 3 Search | Stopping criteria met, or the limit documented | `references/search-strategy.md` |
| 4 Screen | Every candidate has a screening decision and reason | below |
| 5 Verify | Every included source `VERIFIED` or `VERIFIED-QUALIFIED` | `references/verification-protocol.md` |
| 6 Extract | Extraction row and source record for every included source | `references/evidence-records.md` |
| 7 Gap matrix | Each gap backed by comparison, wording calibrated | `references/gap-matrix.md` |
| 8 Citation map | Every planned insertion mapped to a claim | `references/evidence-records.md` |
| 9-10 Write, integrate | Manuscript edited, bib updated from staging | `references/integration.md` |
| 11 Records | Kept current throughout, not at the end | `references/evidence-records.md` |
| 12 QA and report | All audits pass or failures documented, summary written | `references/qa-and-deliverables.md` |

### Phase 0: Workspace

1. Read `literature/PROGRESS.md` and any existing ledger, search log, or notes. Reuse and extend them. Never start a parallel second set.
2. Find the manuscript. Prefer the `.tex` with `\documentclass` whose compiled PDF is newest, or the `.docx` the cover letter names. Read project instructions (CLAUDE.md, README, journal template) for venue and citation style. Ask one short question only when two candidates remain equally likely.
3. Back up before any edit: copy the manuscript and its bib files into `literature/originals/` with the date in the name. The working manuscript stays at its own path, so the build and the "final version" never become ambiguous.
4. `python scripts/init_workspace.py --root <project>` creates the workspace without overwriting anything.
5. `python scripts/audit_citations.py <main.tex> --snapshot literature/baseline_citations.json` records the starting citations and finds the active bib.
6. Name the genre (original research, survey, systematic review, theory, framework, position). Do not call the work a systematic review unless its method and reporting meet that standard.

### Phase 1: Baseline Diagnosis

Read the full manuscript, not the abstract and introduction alone. Extract the title, research questions, claimed contributions, central concepts, method, results, limitations, and every novelty phrase ("first", "novel", "no prior work", "to the best of our knowledge").

Machine-check the existing bibliography: `python scripts/verify_refs.py <bib> --out literature/raw/verification/baseline_verify.csv --raw-dir literature/raw/verification`. Existing references are not trusted by default. Real manuscripts carry DOIs that resolve to other papers, fabricated author lists, arXiv DOIs on conference citations, and retracted papers. Flag what you find. Do not delete existing citations silently. Correct verifiable errors and record each change.

Write `literature/baseline_diagnosis.md`: coverage per dimension (foundations, state of the art, competing approaches, empirical evidence, method justification, known limitations, contradictions, datasets and metrics, cross-cutting concerns such as safety or privacy, recent work that threatens the novelty, neighboring disciplines), then a numbered list of gaps, each with manuscript location, evidence needed, and importance (blocking, major, minor). Keep strong existing citations.

### Phases 2 and 3: Strategy and Search

Follow `references/search-strategy.md`. The search is a loop with a reasoned stop:

```dot
digraph search_loop {
  "Run query family" [shape=box];
  "Log query, platform, counts" [shape=box];
  "Screen hits, snowball key papers" [shape=box];
  "Every dimension covered?\nCompeting and negative work found?\nLast round mostly duplicates?" [shape=diamond];
  "Refine queries for the open gaps" [shape=box];
  "Record stop reason and open limits" [shape=box];
  "Run query family" -> "Log query, platform, counts";
  "Log query, platform, counts" -> "Screen hits, snowball key papers";
  "Screen hits, snowball key papers" -> "Every dimension covered?\nCompeting and negative work found?\nLast round mostly duplicates?";
  "Every dimension covered?\nCompeting and negative work found?\nLast round mostly duplicates?" -> "Refine queries for the open gaps" [label="no"];
  "Refine queries for the open gaps" -> "Run query family";
  "Every dimension covered?\nCompeting and negative work found?\nLast round mostly duplicates?" -> "Record stop reason and open limits" [label="yes"];
}
```

### Phase 4: Screen

Every candidate gets a ledger row with `screening_decision` (candidate, included, excluded) and, when excluded, a reason. Judge relevance to a specific claim, rigor, evidence strength, and version. Search rank and citation count are not quality. Prefer the primary study for an empirical finding and use reviews to map a field or find primaries. Label preprints as preprints. A missing DOI is not a reason to exclude. A retraction is, unless the paper discusses the retraction itself.

### Phases 5 to 12

Follow the reference file named in the workflow table. Two mechanics matter across all of them:

- **Staging bib.** New entries go into `literature/references_lit.bib` first. Only entries whose ledger status is `VERIFIED` or `VERIFIED-QUALIFIED` move into the manuscript's active bib, in Phase 10.
- **One identifier everywhere.** The BibTeX key is the `source_id` in the ledger, extraction sheet, citation map, gap matrix, raw record filenames, and the manuscript.

## Tools

Use what the session has, and log what failed. Findings from testing these services:

| Need | Use | Notes |
|---|---|---|
| Discovery | WebSearch, Semantic Scholar API, OpenAlex API, Crossref search, arXiv API, PubMed and Europe PMC for biomedicine | Google Scholar has no API. Cite it as searched only if you loaded it in a browser |
| Snowballing | OpenAlex `referenced_works` and `cites:` filter, Semantic Scholar `/references` and `/citations` | See search-strategy.md |
| DOI metadata | Crossref `api.crossref.org/works/{doi}`, DataCite for arXiv `10.48550` DOIs, `doi.org/doiRA/{doi}` to find the agency | `verify_refs.py` does all three |
| Retractions | Crossref `filter=updates:{doi}` (includes Retraction Watch data) | `verify_refs.py` reports them |
| Full text | Publisher page via WebFetch, arXiv, PMC, institutional repository, Chrome tools if the user is signed in | Record the access level you reached |
| Venues without DOIs | Official proceedings site (proceedings.neurips.cc, proceedings.mlr.press, openreview.net, aclanthology.org) | DBLP's API sits behind a bot check and fails from scripts |

Semantic Scholar and OpenAlex sometimes attach the wrong DOI to a paper. Confirm every aggregator DOI at its registration agency before use. `verify_refs.py` does this and marks failures `REJECTED`.

Optional keys: `CROSSREF_MAILTO`, `S2_API_KEY`, `OPENALEX_API_KEY`. Do not register any key or send the user's email to a service without asking.

## Scripts

All in `scripts/`, Python 3 standard library only. Run any of them with `--help`.

| Script | Use it to |
|---|---|
| `init_workspace.py` | Create `literature/` folders, CSV headers, PROGRESS.md. Never overwrites |
| `audit_citations.py` | Cited keys vs. bib: missing keys, duplicates, unescaped `%` and `&`, uncited entries, before/after snapshot diff |
| `verify_refs.py` | Machine-check bib entries against Crossref, DataCite, arXiv, Semantic Scholar, OpenAlex, including retractions |
| `doi2bib.py` | Build a clean BibTeX entry from a DOI record, skip DOIs already in the bib |
| `check_ledger.py` | Prove traceability: every cited key has a citable ledger status, access level, record, and map entry |
| `gap_table.py` | Turn `gap_matrix.csv` into a booktabs LaTeX table |

## Writing Rules for Inserted Prose

Write American English unless the venue says otherwise. If the user has writing-style rules (memory, CLAUDE.md), they govern every sentence you add. Compare studies, do not list them. Report numbers with their conditions exactly as the source states them. Details and paragraph recipes are in `references/integration.md`.

## Common Mistakes

| Mistake | Correction |
|---|---|
| Typing a BibTeX entry from recall | `doi2bib.py`, or the publisher's export, then verify |
| Treating a resolving DOI as verified | Compare the record's title, authors, and year with the citation. A DOI copied from the wrong search hit resolves fine and points at another paper |
| Citing a number seen only in a snippet or summary | Read the source. No access, no number |
| "No prior work addresses X" after two searches | Search the concept in every community's vocabulary, then calibrate the wording (gap-matrix.md) |
| Ten citations at the end of one sentence | Place each source at the clause it supports, and synthesize |
| Citing the arXiv version when a peer-reviewed version exists | Check for the published version and cite it, or note why not |
| Summaries one paper per paragraph | Organize by question or approach, and compare |
| Silently deleting a suspect existing citation | Flag it, verify it, fix or replace it, and record the change |
| Writing the ledger at the end | Update records as you go. The trail is the deliverable |
| Saying "searched IEEE Xplore" after a web search | Name the tool you used |

## Red Flags: Stop and Fix

- About to cite a source with status `PENDING`, `UNRESOLVED`, or `REJECTED`
- About to write a finding from a source whose access level is `METADATA`
- About to paste a candidate DOI that `verify_refs.py` did not confirm
- A gap statement with no list of the papers examined
- "First", "only", or "no study" in text you are adding
- Every new citation sits in the related-work section and none supports the method or discussion
- `audit_citations.py` or `check_ledger.py` exits 1 and you are about to report completion
- You are planning the search instead of running it

## Rationalizations

| Thought | Reality |
|---|---|
| "I know this paper well, the metadata is right" | Recall is how fabricated references enter papers. Retrieve it |
| "The DOI resolves, so it is verified" | It may resolve to a different paper. Compare the fields |
| "The abstract is enough to cite this result" | Only if the abstract states the result. Otherwise get the full text or soften the claim |
| "The reviewer wants more citations, so add twenty" | Reviewers want the right ones. Add what fills a documented gap |
| "The existing references were checked before" | Run the check. It takes minutes and has found wrong DOIs in submitted papers |
| "Close enough to say no one has done this" | Write what the evidence supports: "few identified studies", "the reviewed approaches do not" |
| "I'll fill the ledger after integration" | Then it reconstructs instead of records. Write it as you go |
