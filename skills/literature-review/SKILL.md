---
name: literature-review
description: Use when a research manuscript (LaTeX, Word, or Markdown) needs a comprehensive, evidence-based review of its field before any rewriting, such as establishing the state of the art, testing its novelty and contribution claims against the closest existing work, validating whether genuine research gaps remain, or checking that its descriptions of prior work are accurate. Trigger on "literature review", "Literature-Review", "literature_review.md", "research gap identification", "validate the research gap", "is this novel", "state of the art for my paper", "gap matrix", "novelty assessment". Do NOT trigger for diagnosis of an existing paper's integrity (research-auditor), BibTeX cleanup alone (bibtex-validator), reviewer-response revision (manuscript-revision), or prose polish (universal-manuscript-polish).
---

# Literature Review: Discovery, Gap Validation, Novelty Assessment

You review the research field of the manuscript in the current folder and deliver `literature_review.md` beside it. You read the manuscript, search the literature, verify every source, read what each source says, compare studies, and test each candidate gap and novelty claim against counterevidence.

**This is a discovery and validation phase.** The manuscript, its bib, code, and data stay untouched. No rewriting, formatting, coding, or experiments.

**Core principle:** every statement about prior work traces to a real publication you retrieved in this session, at an access level that permits the statement. A smaller verified evidence base beats a longer questionable one.

**The brief.** `references/prompt.md` is the user's prompt, verbatim. Read it once at the start. It defines the phases, the required evidence per gap (A to K), the five gap categories, both tables, the 17-section structure, and the completion report. This file adds the tools, files, gates, and lessons from test runs.

**Do the work.** A plan, an outline, or a list of suggested queries is not a deliverable. Run the searches, read the sources, write the records and the review, and run the checks.

## Hard Rules

1. **Nothing from memory.** Every title, author list, year, venue, DOI, page range, and finding comes from a record retrieved in this session. Build BibTeX with `scripts/doi2bib.py` or the publisher's export. A source you recall but cannot retrieve does not enter the review. This includes papers you "know" are relevant: search for them, then cite what the record shows.
2. **Identity and claim are separate checks.** `verify_refs.py` shows a publication exists with that metadata. Claim support needs you to read the text, and the access level caps what you may say (table below).
3. **Report what happened.** Never write that you searched a database, read a full text, or verified a record unless that operation succeeded in this session. Name the tool you used ("WebSearch", "OpenAlex API"), not the database you wish you had used.
4. **No citation-count targets.** Stop by the criteria in `references/search-strategy.md` section 6, not at a number. The one composition target is the venue balance below, and it governs which equally relevant sources you prefer, never how many you cite.
5. **Read-only project.** Do not edit the manuscript, its bib, figures, code, or data. Your writable area is `literature/` and `literature_review.md`. If `literature_review.md` exists, read it first, keep its valuable content, and move the old copy to `literature/originals/literature_review_<date>.md` before writing.
6. **Gaps are conclusions from comparison.** Never from a search that returned little, from the manuscript's own related-work section, or from an author's future-work sentence.

## What Each Access Level Can Support

| Access level | What you saw | What you may cite it for |
|---|---|---|
| `FULLTEXT` | The paper itself (PDF, HTML, open repository) | Specific results with numbers and conditions, methods detail, limitations, with a location (section, table, page) |
| `ABSTRACT` | Abstract and metadata | Only what the abstract states. Mark "abstract only" |
| `METADATA` | Title, authors, venue, year | That the work exists and its general topic. Not findings, not limitations |
| snippet | A search-result snippet or an AI summary | Nothing. Retrieve the source or drop it |

**Closed-access sources need no full text.** The author's policy (brief, Amendment 2): for a subscription or paywalled publication, collect what is accessible (title, authors, venue, year, DOI, abstract, highlights, keywords) and cite it within the limits of the table above. Do not spend effort obtaining a full text that the publisher withholds. When the author's institutional access shows the full text in their browser, use it and record `FULLTEXT`. Reading only the abstract of a closed-access paper is a normal, complete outcome, not a limitation to apologize for. Say once in Sec. 4.6 which sources are abstract-level.

## Venue Balance: Closed-Access and Open-Access

The author wants the final bibliography to draw roughly equally on closed-access and open-access venues.

| `venue_access` | Counts as | Examples |
|---|---|---|
| `open` | Open-access venue | Fully open-access journals and proceedings (MDPI, Frontiers, PLOS, IEEE Access, OpenReview, ACL Anthology), preprint servers (arXiv, SSRN, Research Square), freely available official reports (NIST, government agencies) |
| `closed` | Closed-access venue | Subscription and hybrid journals and proceedings (most Elsevier, Springer, Wiley, IEEE Transactions, ACS, ACM), paywalled standards (ISO, IEEE standards). A free article in a hybrid journal still counts as closed |

- **Target:** about 50% each, acceptable band 40 to 60%, computed over the references in Sec. 15.
- **Measure, don't guess:** `seed_ledger.py --fetch-venue-access` classifies each included DOI from OpenAlex (`is_oa`, DOAJ listing, repository type). Override misclassifications in the `venue_access` column of `reading_notes.csv`. OpenAlex leaves free government reports and some MDPI records unclassified, so check those.
- **Relevance first:** the balance decides between equally relevant candidates. Never add a weak source or drop a relevant one to move the ratio.
- **Outside the band:** run targeted searches for equally relevant work in the under-represented class (for example, open-access journals in the same field, or the subscription journals that publish the field's primary studies). If none qualifies, keep the imbalance and state the reason.
- **Report it:** the split goes in Sec. 4.5 and the completion report. `check_review.py --ledger` prints it and warns (W08) outside the band.

## Verification Status

| Status | Meaning | Where it goes in the review |
|---|---|---|
| `VERIFIED` | Authoritative record matches every bibliographic field | Sec. 15 |
| `VERIFIED-QUALIFIED` | Identifiable, one detail or the version needs a note | Sec. 15, with the note |
| `UNRESOLVED` | Not enough evidence either way | Sec. 16 |
| `REJECTED` | Does not exist, metadata belongs to another work, or retracted | Sec. 16 when the manuscript cites it, otherwise ledger only |
| `PENDING` | Not checked yet | Nowhere. Resolve before writing |

## Workflow

Keep `literature/PROGRESS.md` current. After a context reset, read it first and resume at the first phase whose gate is open.

| Phase | Brief section | Gate to leave the phase | Detail |
|---|---|---|---|
| 0 Workspace | 12 | Manuscript, bib, and genre identified. `literature/` created. Existing review preserved | below |
| 1 Understand manuscript | 2 | Whole manuscript and its code read. Claim list (M-ids) and demonstrated-vs-proposed notes written. Existing bib machine-checked | below |
| 2 Search | 3 | Every query run through `search.py` (so it is logged), snowballing done, stop reason recorded | `references/search-strategy.md` |
| 3 Evidence base | 4, 8 | Every included source machine-verified and in the ledger with an access level. Abstracts read for every source cited for a finding | `references/verification-protocol.md`, `references/evidence-records.md` |
| 4 Synthesis | 5 | Themes drafted as comparisons, comparison tables built | `references/review-template.md` Sec. 6-8 |
| 5 Gaps | 6 | Each gap has A to K, a category, and a counterevidence search logged | `references/gap-matrix.md` |
| 6 Novelty | 7 | Every claimed contribution compared with its closest work | `references/gap-matrix.md` section 5 |
| 7 Write | 9 | `literature_review.md` complete, every section filled | `references/review-template.md` |
| 8 QA | 10 | `check_review.py` exits 0, judgment audit recorded | `references/qa-and-deliverables.md` |
| 9 Report | 12 | Completion report with counts copied from the checker summary | below |

### Shell setup (do this first)

The scripts live under a home directory that may contain a space (`C:\Users\First Last`). Set and always quote the path:

```
S="${CLAUDE_SKILL_DIR}/scripts"   # the folder that holds this SKILL.md; other agents use that path
python "$S/search.py" ...
```

On Windows the `python` launcher can be a batch shim. Then multi-line `python -c` fails, heredoc Python loses backslashes, and arguments with `(`, `)`, or `;` break even when quoted, which hits ASCE DOIs such as `10.1061/(asce)...`. Put such DOIs in a file and pass `--lookup @file` or `--file`. Write any helper code as a file with the Write tool, not inline.

### Phase 0: Workspace

1. Find the manuscript: the `.tex` with `\documentclass` whose PDF is newest, or the `.docx` the user names. Read project notes (README, MANUSCRIPT_NOTES, CLAUDE.md) for venue and context.
2. `python "$S/init_workspace.py" --root <project>` creates `literature/` without overwriting.
3. `python "$S/audit_citations.py" <main.tex> --snapshot literature/baseline_citations.json` records the starting citations and finds the active bib. This reads the project, it does not change it.

### Phase 1: Understand the Manuscript

Read the full manuscript, including tables, algorithm boxes, captions, the bib, and any notes or code that define what was actually done. Write the ten items of brief section 2 straight into review Sec. 3 (draft `literature_review.md` early, or keep notes in `literature/research_profile.md`). Two lists matter most later:

- **Claims to test.** Every novelty phrase, every description of a cited work ("X does not consider Y"), every positioning table cell, and every claim a later section depends on. Give each an ID (M1, M2, ...). Positioning tables that mark competitors with "--" are claims about those papers and must be checked against the papers.
- **Demonstrated versus proposed.** Separate what the manuscript shows with evidence from what it designs or anticipates. When code or data exist, trace every headline number to the line that produces it. In the test run this step produced the most important finding, so do it before searching:
  - Look for per-method constants (dicts of rates, probabilities, latencies) that the "results" are sampled from. If the outcome equals an input plus noise, the result restates an assumption. Say so with the parameter values.
  - Look for result tables written as literals (`pd.DataFrame({...: [10.9, 7.2, ...]})`) and compare them with the paper's other tables for the same configuration.
  - Check that the paper's numbers match the generated CSVs.

Machine-check the existing bib: `python "$S/verify_refs.py" <bib> --out literature/raw/verification/baseline_verify.csv --raw-dir literature/raw/verification`. The manuscript's own references enter the evidence base on the same terms as new ones. Report problems in review Sec. 3.4 and Sec. 16.

### Phase 2: Search

Follow `references/search-strategy.md`. Run every query through `search.py`, which writes the `search_log.csv` row (exact query, filters, platform-reported count, titles screened) and saves the raw response, so no count is ever typed by hand. In addition to its query families, run these for every manuscript of this kind:

- **Closest-competitor sweep.** For each claimed contribution, search the contribution itself in plain words without the manuscript's own labels ("zero-trust multi-agent", not the system's name). Run it for the last 24 months and sort by date. New competitors appear faster than the manuscript's bib.
- **Neighboring-field sweep.** The same problem in an adjacent community's words (for an agentic water twin: agent security in industrial control, LLM-agent tool authorization, cyber-physical digital-twin security). Gaps often exist in one vocabulary only.
- **Counterevidence sweep.** For each candidate gap, at least one query designed to find work that already solves it. Log it with purpose `counterevidence G<n>`.

### Phase 3: Evidence Base

Verify every source before you write about it (`references/verification-protocol.md`). One `source_id` everywhere: the ledger, notes, and the review's `[key]` citations. The pipeline that worked:

1. Read abstracts: `python "$S/search.py" --abstract --lookup @literature/dois.txt`. It routes arXiv ids to the arXiv API and falls back to Crossref abstracts when OpenAlex has none.
2. Build BibTeX: `python "$S/doi2bib.py" --file literature/dois.txt > literature/references_lit.bib`. For a manuscript entry whose metadata is wrong, generate the corrected record under the manuscript's own key: `doi2bib.py <doi> --key <key> >> literature/references_corrected.bib`.
3. Machine-check: `verify_refs.py` on both bibs.
4. Record your judgments (access level, peer-review status, themes, qualified status, inclusion, notes) in `literature/reading_notes.csv`, one row per source, as you read.
5. `python "$S/seed_ledger.py" --bib <manuscript.bib> literature/references_lit.bib --verify "literature/raw/verification/*_verify.csv" --notes literature/reading_notes.csv --fetch-venue-access` merges records, machine checks, and notes into `source_ledger.csv`, classifies venues as open or closed, and prints the counts, the closed-access share, and any OPEN rows. Rerun it after each batch, and steer the next searches by the venue split.

`extraction_sheet.csv` and `raw/source_records/` are optional. The review's Sec. 7 table is the evidence inventory for every source cited for a result or comparison, and the ledger holds verification state.

**Expect ABSTRACT access.** In the test run, 0 of 57 sources reached FULLTEXT. arxiv.org pages were blocked for WebFetch, MDPI returned 403, and Elsevier, Nature, and IEEE DOIs redirected to login or stub pages. The arXiv API, OpenAlex, and Crossref supplied abstracts. Semantic Scholar returned only AI "TLDR" summaries for publisher-elided abstracts, which support nothing. Plan the review around abstract-level claims, try open repositories (PMC, institutional repositories, author pages) for the 3 to 5 most decisive papers, and state the access limit in Sec. 1, 4.6, and 14.

**Use the user's browser when scripted access fails.** The user has authorized it. When WebFetch is blocked, a page redirects to a login, or a paper is paywalled, open it in the user's Chrome through the Claude in Chrome tools (`mcp__claude-in-chrome__*`). Load them in one ToolSearch call (`tabs_context_mcp`, `tabs_create_mcp`, `navigate`, `get_page_text`, `read_page`, `find`, `computer`), call `tabs_context_mcp` first, and work in a new tab. The browser carries the user's own sessions and institutional access, so it often reaches publisher full text (ScienceDirect, IEEE Xplore, SpringerLink, Wiley, Nature), arxiv.org pages, MDPI, and Google Scholar that scripts cannot. Use it also to search Google Scholar or a publisher database when the brief calls for one, and then that database counts as searched.
- Prioritize: the closest competitors, sources behind a gap or novelty verdict, and METADATA-only sources whose content decides a claim.
- Never type passwords, solve logins, or accept terms on the user's behalf. If a page needs sign-in, ask the user to sign in, or record the source as not accessible.
- **CAPTCHAs and human-verification pages** ("Are you a robot?", Cloudflare "Just a moment..."): never try to solve or bypass them. First re-read the tab after a few seconds, because ScienceDirect's check sometimes clears by itself. If it is still there, ask the user to clear it in the open tab, wait for their confirmation, then re-read the page and continue. If the user is unavailable, record the source at the access level already reached and move on.
- Cookie banners: choose the option that declines non-essential cookies.
- Full-article pages are long (a ScienceDirect article with references runs to about 15,000 tokens). For closed-access sources that only need abstract-level citation, read the abstract and highlights and stop.
- Do not trigger download or print dialogs. Read the HTML full text, or open the PDF in the tab and read it there.
- Record what you reached: access level `FULLTEXT` with the source "user browser" in the ledger notes, and the platform in the search log or Sec. 4.2. Quote only short excerpts.
- If the browser extension does not respond after two or three tries, stop and ask the user, then continue with abstract-level evidence.

### Phases 4 to 7: Synthesis, Gaps, Novelty, Writing

Write into the slots of `references/review-template.md`. The template's citation convention and field vocabularies are required, because `check_review.py` parses them. Gap records follow `references/gap-matrix.md`, which maps the brief's A to K and five categories onto the evidence you hold. Each gap's **Examined** line lists its Q-ids, and at least one must be a query logged with a "counterevidence" purpose. In the test run this gate caught three gaps drafted without one, and the extra queries found the closest competitor of the whole review.

Never type Sec. 15 or 16 entries. Leave `<!-- REFS15 -->` and `<!-- REFS16 -->` markers, run `python "$S/render_references.py" --ledger literature/source_ledger.csv --bib literature/references_corrected.bib literature/references_lit.bib <manuscript.bib> > literature/refs_rendered.md`, and splice its lines in. Corrected records come first so they win over the manuscript's wrong ones.

Novelty assessment rules (brief section 7) in short: name the novelty type (conceptual, methodological, empirical, application-specific). A combination of known components or a new application domain is a contribution only if the manuscript demonstrates an advantage from the combination. A synthetic or simulated demonstration is weaker evidence than a field or benchmark comparison, and the assessment says so.

### Phases 8 and 9: QA and Report

```
python "$S/check_review.py" literature_review.md --ledger literature/source_ledger.csv --search-log literature/search_log.csv
```

Then recount every number the review states about its own process (queries, titles screened, sources by status and access, abstracts fetched) against the checker SUMMARY, the seed_ledger output, and the search log. The test run's only factual slip was a hand-typed process count.

Fix every ERROR. Read every WARN and fix it or record why it stands. Then do the judgment audit in `references/qa-and-deliverables.md` and record it in `literature/qa_report.md`.

The completion report (brief section 12) takes its counts from the checker's `SUMMARY` line and the ledger, not from memory: file path, themes, sources included (VERIFIED, VERIFIED-QUALIFIED, unverified), gaps by category and confidence, limitations, open verification issues.

## Tools

Use what the session has. Log what failed.

| Need | Use | Notes |
|---|---|---|
| Discovery | WebSearch, Semantic Scholar API, OpenAlex API, Crossref search, arXiv API, PubMed and Europe PMC for biomedicine, Consensus MCP if connected | Google Scholar has no API. List it as searched only if you loaded it in a browser |
| Snowballing | OpenAlex `referenced_works` and `cites:` filter, Semantic Scholar `/references` and `/citations` | search-strategy.md section 4 |
| DOI metadata | Crossref `api.crossref.org/works/{doi}`, DataCite for arXiv `10.48550` DOIs | `verify_refs.py` does both |
| Retractions | Crossref `filter=updates:{doi}` | `verify_refs.py` reports them |
| Full text | Publisher page via WebFetch, arXiv, PMC, MDPI and other open-access HTML, institutional repositories, then the user's Chrome browser (Claude in Chrome tools) when these fail | Record the access level you reached. Many IEEE, Elsevier, and Springer pages return only the abstract to scripts but open in the user's signed-in browser |
| Venues without DOIs | Official proceedings sites, OpenReview, ACL Anthology | DBLP's API sits behind a bot check |

Semantic Scholar and OpenAlex sometimes attach the wrong DOI to a paper. Confirm every aggregator DOI at its registration agency. `verify_refs.py` does this.

Optional keys: `CROSSREF_MAILTO`, `S2_API_KEY`, `OPENALEX_API_KEY`. Do not register a key or send the user's email to a service without asking.

## Scripts

All in `scripts/`, Python 3 standard library only. Run any with `--help`.

| Script | Use it to |
|---|---|
| `init_workspace.py` | Create `literature/` folders, CSV headers, PROGRESS.md. Never overwrites |
| `audit_citations.py` | Snapshot the manuscript's citations and active bib (read-only). `--compare` at the end proves nothing changed |
| `search.py` | Run one OpenAlex, Crossref, or arXiv query and log it, forward (`--cites W-id`) and backward (`--refs DOI`) snowballing, `--lookup` abstracts by DOI or arXiv id (not logged) |
| `verify_refs.py` | Machine-check bib entries against Crossref, DataCite, arXiv, Semantic Scholar, OpenAlex, including retractions |
| `doi2bib.py` | Build BibTeX from DOI records. `--key` regenerates a manuscript entry under its own key |
| `seed_ledger.py` | Merge bibs, verify CSVs, and `reading_notes.csv` into `source_ledger.csv`. Prints counts and open rows |
| `render_references.py` | Generate review Sec. 15 and 16 lines from the ledger and bib records |
| `check_review.py` | Validate `literature_review.md`: sections, tables, gap fields, citation-reference match, ledger agreement, counterevidence queries. Prints the counts for the report |
| `gap_table.py` | Render `gap_matrix.csv` as LaTeX for a later integration stage |
| `check_ledger.py` | Integration stage only (checks `\cite` keys in a .tex) |

## Later Stage: Integration (only on explicit request)

Editing the manuscript with the review's findings is a separate, later task. Do it only when the user asks for it after reading `literature_review.md`. Then follow `references/integration.md`, back up originals to `literature/originals/`, and run `check_ledger.py` and `audit_citations.py --compare`.

## Writing Rules

American English. Compare studies, do not list them. Report numbers with their conditions exactly as the source states them, and never compare numbers across incompatible experiments without saying so. Label interpretation as interpretation. If the user has writing-style rules (memory, CLAUDE.md), they govern the review's prose. The checker flags em dashes and semicolons.

## Common Mistakes

| Mistake | Correction |
|---|---|
| Citing a known paper from recall | Search for it, retrieve the record, verify, then cite |
| Treating a resolving DOI as verified | Compare title, authors, and year with the record |
| Citing a number seen only in a snippet or summary | Read the source. No access, no number |
| "No prior work addresses X" after a few searches | Run the counterevidence sweep, then use the calibrated wording in gap-matrix.md |
| Accepting the manuscript's positioning table | Each "--" for a competitor is a claim. Check it against the competitor paper |
| Taking the manuscript's results as demonstrated | Check them against its code or data and say what kind of evidence they are |
| One paragraph per paper | Organize by question or approach and compare |
| Writing the ledger at the end | Record as you go. The trail is the deliverable |
| Editing main.tex "while you are there" | Not in this phase. Put the suggestion in Sec. 13 |
| Counting from memory in the completion report | Copy the checker SUMMARY and ledger counts |
| Reading the paper's results table as evidence | Trace each number to the code line that produces it (Phase 1) |
| Citing an AI TLDR because the abstract was elided | It supports nothing. Mark the source METADATA and say what is unknown |
| Treating OpenAlex "reported" counts as relevant hits | OpenAlex matches any term. Report them as breadth only |
| Online-first year vs issue year | Use the Crossref issue year, mark VERIFIED-QUALIFIED with both years in the note |
| Typing Sec. 15 lines | Generate them with `render_references.py` |

## Red Flags: Stop and Fix

- About to cite a source with status `PENDING`, `UNRESOLVED`, or `REJECTED` in Sec. 1 to 14 without saying so in the sentence
- About to state a finding from a `METADATA` source
- A gap with no counterevidence search in the log
- "First", "only", or "no study" in your own text
- A gap category of "Established" with only one supporting source
- `check_review.py` exits 1 and you are about to report completion
- You are planning the search instead of running it
- You opened main.tex for writing

## Rationalizations

| Thought | Reality |
|---|---|
| "I know this paper, the metadata is right" | Recall is how fabricated references enter reviews. Retrieve it |
| "The abstract is enough to cite this result" | Only if the abstract states the result |
| "The manuscript says competitor X lacks Y" | That is the claim under test, not evidence |
| "Few hits, so it is a gap" | Few hits means the vocabulary may be wrong. Search the neighbors |
| "The synthetic results show the method works" | They show the method works in its own simulator. Say that |
| "I'll fill the ledger after writing" | Then it reconstructs instead of records |

## Related skills


Run order and the full map: `research-workflow-map`. Invoke these with the Skill tool. If one is not installed, say so and continue with this skill's own steps.

- **Paper cycle:** step 3 of 14. In the cycle, ask for the integration stage too, so the verified works are cited in the paper.
- **Needs first:** the initial draft from `idea-to-paper` (step 2) and the gap from `finding-gap` (step 1).
- **Called by:** `idea-to-paper` (its Step 1 reuses this skill's scripts).
- **Uses during the run:** `reference-verify` for manuscript entries that `verify_refs.py` flags and for UNRESOLVED or REJECTED ledger rows. The integration stage uses `universal-manuscript-polish` and `text-humanizer`.
- **Hands on to:** `paper-to-project-report` (step 4). Outside the cycle: `manuscript-revision` when reviewers ask for broader related work.
