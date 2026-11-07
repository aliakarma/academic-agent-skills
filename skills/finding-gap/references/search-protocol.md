# Search and Evidence Protocol

How to build an evidence base that can carry a gap claim.

## Contents

1. Tool roster, strengths, and limits
2. Query construction
3. Search passes
4. Saturation and stopping
5. Source Ledger
6. Search Log
7. Extraction sheet coding guide
8. Running gap_matrix.py
9. Coverage-limitations statement
10. No-tools fallback

---

## 1. Tool roster, strengths, and limits

Connector tools may be deferred. Load them with `tool_search` before first use and use the exact parameter names returned.

**Consensus (`mcp__Consensus__search`).** Broad discovery across a very large index (its own description says it covers Semantic Scholar, PubMed, Scopus, and arXiv). Returns titles, authors, year, venue, abstracts, citation counts, and links.
- Useful filters: `year_min` / `year_max` (use them when the user gave a year range, which is exactly the explicit request the tool asks for), `study_types` (for M4 or when the user asks for specific designs), `exclude_preprints` (only when peer-reviewed-only is wanted; for AI topics usually keep preprints and label them), `country` (M5, when a country is named), `domain` (for example `cs`, when the field needs restricting), `duration_min` (M8 longitudinal searches).
- Limits: a limited number of results per call on some plans; abstracts only unless full-text excerpts are available on the user's plan; citation counts lag. Follow the tool's display instructions (numbered references, links, and any required notice) when presenting its results.

**Scholar Gateway (`mcp__Scholar_Gateway__semanticSearch`).** Full-text passage retrieval with citation metadata and DOIs. Best source for limitations, discussion, and future-work passages (M3) and for checking what a paper actually did.
- Write queries as complete natural-language questions; expand acronyms. Use `start_year` / `end_year` and `topN` (up to 20).
- Limits: its corpus coverage is publisher-dependent and not universal (see the coverage link it returns), so silence from Scholar Gateway is weak evidence of absence. Follow its render contract (provenance line per search, footer once per response).

**web_search / web_fetch.** Required for: arXiv and OpenReview (recency sweep), ACL Anthology, DBLP, publisher landing pages for verification, regulatory and standards texts (M11), lab or project pages, and any URL the user provides. `web_fetch` works only on URLs that appeared in the conversation or in search results.

**User materials.** Uploaded PDFs, .bib files, reading lists, and prior reviews are high-value evidence. Read PDFs with the pdf-reading skill. Treat user-provided metadata as `[U]` until checked.

**Researcher context.** For the user's own work, fetch the portfolio or profile URL the user gives and use what the user provides.

## 2. Query construction

- Build from the M0 concept blocks: core phenomenon AND context AND (method OR outcome). Run several narrower queries rather than one long one.
- Expand terminology: synonyms, acronyms spelled out, older and newer names for the same idea, and terms from neighboring communities (for example, "AI governance" vs "algorithmic accountability" vs "responsible AI"; "digital twin" vs "cyber-physical model"). Construct-name mismatch (the same construct under different names, or different constructs under the same name) is the most common reason a gap turns out to be false.
- Lens-specific query patterns:
  - Reviews: "systematic review [topic]", "survey of [topic]", "meta-analysis [topic]", "research agenda [topic]", "open challenges [topic]"
  - M2: "[X] [Y] mixed evidence", "inconsistent findings [topic]", "fails to replicate [claim]", "re-evaluation of [method]"
  - M3 (Scholar Gateway, question form): "What limitations and future research directions do studies of [topic] identify?"
  - M4: "[topic] longitudinal", "[topic] field experiment", "[topic] simulation study", "[topic] user study", "[topic] formal verification"
  - M5: "[topic] [country or sector]", "cross-cultural [topic]", "[topic] low-resource settings"
  - M6: "[theory] [topic]", "theoretical framework [topic]", "[topic] unexpected findings"
  - M7: "[variable A] [variable B] [topic]" with synonyms for each
  - M8: "[topic] before and after [event]", "[topic] panel data", "[topic] post-[event]"
  - M11: official text of the regulation or standard; "[requirement] technical implementation evaluation"
  - Disconfirmation: the candidate research question itself, phrased several ways, plus "[method] for [problem] in [context]"

## 3. Search passes

Run the passes relevant to the mode, logging every query.

- **Pass A: Reviews and seeds.** Reviews, surveys, meta-analyses, evidence-and-gap maps, research agendas, plus any user seed papers. Record the gaps these reviews already named; a gap already stated in a recent review is not novel as a *finding*, though work that addresses it can still be novel.
- **Pass B: Cluster searches.** One to three queries per emerging cluster (M1).
- **Pass C: Lens searches.** Patterns from section 2 for each selected module.
- **Pass D: Snowballing.** From 3–5 key papers, check what they cite (backward) and what cites them (forward), using Consensus, Scholar Gateway, or web search for "cited by" pages. Snowballing guidelines are commonly attributed to Wohlin (2014, EASE) `[B]`; retrieve it before citing.
- **Pass E: Recency sweep.** The last 12–18 months, including arXiv and OpenReview for AI and CS topics. This is where gaps most often die.
- **Pass F: Disconfirmation.** Actively try to find the paper that answers the candidate question. Use the research question itself as a query, alternative terminology, and adjacent domains. Report what was tried even when nothing is found.

## 4. Saturation and stopping

A pass is saturated when two consecutive, genuinely different queries return no new relevant papers. Stop Deep analyses when all selected passes are saturated or the budget in SKILL.md is reached; report which condition applied. If the budget is reached before saturation, lower the evidence-confidence rating.

## 5. Source Ledger

The only sources that may be cited. Keep it as `source_ledger.csv` for Deep analyses and as a compact table in chat for Quick ones.

| Field | Content |
|---|---|
| key | BibTeX key, e.g., `sandberg2011ways` |
| title | exactly as retrieved |
| authors | as retrieved; mark "et al." if the tool truncated |
| year | |
| venue | as retrieved; "unknown" if the tool did not return one |
| doi_or_url | as retrieved |
| retrieved_via | Consensus / Scholar Gateway / web_search / web_fetch / user upload |
| retrieved_on | date |
| verification_level | V1 metadata and abstract from a tool; V2 landing page or DOI confirmed; V3 full text or passage read |
| used_for | which claims or modules |
| preprint | yes / no |

Rules:
- Claims about a paper's findings need at least V1 with the abstract supporting the claim.
- Claims about a paper's methods detail, limitations, or future-work statements need V3 (full text or a retrieved passage) or must be labeled "per abstract".
- Build BibTeX entries only from ledger fields; leave a field out rather than guessing it. Recommend a bibtex-validator pass.
- If a tool result looks inconsistent (for example, an author list that seems truncated to one name), record what was returned and flag it.

## 6. Search Log

`search_log.csv` for Deep analyses; a compact table in chat for Quick ones.

| # | date | pass | tool | query | filters | results returned | new relevant | notes |
|---|---|---|---|---|---|---|---|---|

## 7. Extraction sheet coding guide

Template: `assets/extraction_template.csv`. One row per paper.

- Multi-valued fields use `;` as the separator.
- Build a small controlled vocabulary per project and reuse the exact strings; the script counts exact matches (case-insensitive, trimmed).
- Fields:
  - `id`, `citation_key`, `title`, `authors` (separate authors with `;`), `year`, `venue`, `doi_or_url`, `source_tool`, `verification_level`, `preprint`
  - `cluster`: the M1 cluster name(s)
  - `study_type`: for example empirical, simulation, formal, review, position, system
  - `method`: specific methods, for example survey; interviews; RCT; MARL simulation; offline benchmark; red teaming
  - `data_source`, `data_end_year` (last year of data collected, if reported; blank if unknown)
  - `population`, `country` (ISO codes or names, consistently), `setting`
  - `theory`: theories or formal frameworks used
  - `predictors`, `mediators`, `moderators`, `outcomes`
  - `relations`: tested relations with signs, `X->Y:+` / `X->Y:-` / `X->Y:0` (no effect) / `X->Y:~` (mixed or nonlinear), separated by `;`. Use the same variable names as in the role fields.
  - `key_finding`: one-line paraphrase
  - `limitations_tags`, `future_work_tags`: normalized tags
  - `notes`
- Code what the paper reports. When the abstract is all that was read, say so in `verification_level`.

## 8. Running gap_matrix.py

```bash
python3 /path/to/finding-gap/scripts/gap_matrix.py extraction_sheet.csv \
  --out gap_matrix_out \
  --crosstab cluster:method --crosstab cluster:country \
  --anchor-year 2023 \
  --top-k 8 --recur-min-papers 3 --recur-min-groups 2 --recur-min-years 2
```

Outputs: `summary.md` (readable report) and `tables.tex` (booktabs tables for the LaTeX report). The script's results describe only the coded corpus; carry that caveat into every sentence that uses them.

## 9. Coverage-limitations statement

Adapt this for every deliverable:

> This analysis searched [tools] between [dates], using [N] queries (Search Log), and screened [M] records, of which [K] were coded. Coverage is limited by [connector coverage, results per query, paywalled full texts, English-only queries, limited grey literature, single-analyst coding by an AI system without inter-rater agreement]. Statements that a topic is understudied describe this search, not the entire literature. Claims tagged [B] or [I] should be verified before use.

## 10. No-tools fallback

If search connectors and web search are unavailable:
- State this at the top of the response.
- Present candidate gaps as provisional hypotheses tagged `[B]`/`[I]`, with no citations and no numbers.
- Provide search strings tailored to Scopus, Web of Science, IEEE Xplore, ACM Digital Library, Google Scholar, and arXiv, plus the extraction sheet so the user can code results and return them for analysis.
