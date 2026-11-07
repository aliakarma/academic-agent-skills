# Search Strategy and Execution (Phases 2 and 3)

## 1. Build the concept table from the manuscript

Write it to `literature/search_strategy.md` before the first query. One row per concept the manuscript depends on.

| Concept | Role in the paper | Synonyms and community variants | Older terms | Acronyms | Boundary (what is out of scope) |
|---|---|---|---|---|---|
| e.g. post-hoc feature attribution | core method family | saliency, attribution maps, explanation methods, relevance propagation | sensitivity analysis | XAI, SHAP, LIME, LRP | intrinsically interpretable models |

Sources for synonyms: the manuscript's own terms, the keywords of its closest papers, the index terms in PubMed (MeSH) or IEEE (INSPEC) records, and the vocabulary of neighboring fields that solve the same problem under another name. A gap often exists only in one community's vocabulary.

## 2. Plan query families

Cover each family that applies to the paper. Record the purpose of each query in the search log, so a reader can see why it was run.

| Family | Purpose | Example pattern |
|---|---|---|
| Foundations | Seminal formulation of each core concept | concept + "original", sort by citation, no date limit |
| State of the art | Last 24 to 36 months | concept + method family, date filter, sort by date |
| Direct comparators | Work solving the same problem | problem phrase + setting + method family |
| Competing approaches | Different method for the same problem | problem phrase without the paper's method terms |
| Empirical validation | Evaluations, benchmarks, replications | concept + benchmark / evaluation / user study / replication |
| Method foundations | Justification of each design choice | design choice + its rationale term |
| Reviews and surveys | Maps of the field and primary-study discovery | concept + survey / review / meta-analysis |
| Limitations and negative results | Contradictions and failures | concept + limitation / failure / "does not" / sanity check / critique |
| Standards and policy | Normative documents | standard bodies (ISO, IEEE SA, NIST), regulators, OECD, WHO |
| Interdisciplinary | Same problem elsewhere | the problem stated in the other field's words |

Apply a date limit only for a stated reason (for example, "the method did not exist before 2017"). Record the reason.

## 3. Query each service the way it expects

Use the services that respond in this session. Log every attempt, including failures.

**Crossref** (metadata, DOIs, no abstracts for many publishers)
`https://api.crossref.org/works?query.bibliographic=<terms>&rows=20&filter=from-pub-date:2022-01-01,type:journal-article`
Add `&mailto=<address>` only with an address the user approved.

**Semantic Scholar** (abstracts, citations, references, TLDRs)
`https://api.semanticscholar.org/graph/v1/paper/search?query=<terms>&limit=20&fields=title,year,venue,authors,externalIds,abstract,citationCount,openAccessPdf`
Bulk search with boolean syntax: `/paper/search/bulk?query=("feature attribution" | saliency) + faithfulness`.
Without `S2_API_KEY`, expect HTTP 429 under load. Wait and retry. Its DOIs are sometimes wrong.

**OpenAlex** (broad coverage, filters, citation graph)
`https://api.openalex.org/works?search=<terms>&filter=publication_year:>2021,type:article&per-page=25`
Without a key, requests share a small daily budget per IP. If it runs out, say so in the log. Do not register a key with the user's email without asking.

**arXiv** (preprints, slow, allow 60 s)
`https://export.arxiv.org/api/query?search_query=abs:%22feature%20attribution%22%20AND%20cat:cs.LG&max_results=50&sortBy=submittedDate`

**PubMed** (biomedical)
`https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=<terms>[tiab]&retmax=50&retmode=json`, then `esummary` or `efetch` for records. Europe PMC: `https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=<terms>&format=json`.

**Publisher platforms** (IEEE Xplore, ACM DL, ScienceDirect, SpringerLink, Wiley): reach them with WebSearch and WebFetch, or the Chrome tools if the user is signed in. Many block scripted access. Say which platform you actually reached.

**Google Scholar** has no API and blocks scripts. List it as searched only if you used it through a browser in this session.

**DBLP** search API is behind a bot challenge for scripts. Use the web page in a browser when needed.

## 4. Snowball from the key papers

Pick the 5 to 15 papers closest to the manuscript after the first round.

- Backward: OpenAlex `https://api.openalex.org/works/doi:<doi>?select=referenced_works`, or Semantic Scholar `/paper/DOI:<doi>/references?fields=title,year,externalIds`. Semantic Scholar misses some DOIs (the KDD 2016 LIME paper returned 404 in testing). Fall back to `/paper/search/match?query=<title>` for its paperId, or use OpenAlex.
- Forward: OpenAlex `filter=cites:<OpenAlex W-id>&sort=publication_year:desc`, or Semantic Scholar `/paper/DOI:<doi>/citations`.
- Reviews: read their tables of included studies, then retrieve the primaries.
- Newer work: search for papers that appeared after your newest closest source.

Log snowballing as its own search_log row with `discovery_method` = backward or forward.

## 5. Search log

`literature/search_log.csv`, one row per query actually executed.

| Column | Content |
|---|---|
| search_id | Q001, Q002, ... |
| date | ISO date of the search (not the publication date) |
| platform | Service actually queried, e.g. "Semantic Scholar API", "WebSearch" |
| query | Exact query string |
| filters | Date, type, field filters as sent |
| results_reported | The count the platform returned, or "not reported". Never estimate |
| results_screened | How many you screened |
| discovery_method | database, backward, forward, review, manual, author-provided |
| purpose | The query family and the gap it serves |
| notes | Failures, rate limits, surprises |

## 6. Stopping

Stop when all of these hold, and write the reasoning into PROGRESS.md:

- Each dimension in the baseline diagnosis has sources, or a documented reason it has none.
- Foundational work and the last 24 to 36 months were searched for each core concept.
- Competing approaches and at least one search for negative or contradictory findings ran per core claim.
- The novelty claims were tested against direct comparator searches.
- The last full round, across families, added few new included sources and no new evidence category.

When access limits stop you first (rate limits, paywalls, an unreachable service), record the limit, the searches it blocked, and what a follow-up would need. This is a documented limitation, not a reason to claim saturation.
