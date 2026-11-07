# Evidence Records, Citation Map, and Workspace Layout (Phases 6, 8, 11)

## Workspace layout

`init_workspace.py` creates what is marked (init). Create the rest when it has content. Never create an empty file to tick a box.

```
literature/
  PROGRESS.md                 (init) phase gates, open questions, access limits
  baseline_citations.json     Phase 0 snapshot from audit_citations.py
  baseline_diagnosis.md       Phase 1
  search_strategy.md          Phase 2 concept table and query plan
  search_log.csv              (init) every executed query
  source_ledger.csv           (init) one row per unique publication screened
  extraction_sheet.csv        (init) one row per included source
  citation_map.csv            (init) one row per claim that gets a citation
  references_lit.bib          staging bib, verified entries move to the manuscript bib
  gap_matrix.csv              Phase 7 comparison matrix
  gaps.md                     Phase 7 per-gap evidence records
  review_body.md              Phase 9 synthesis draft
  qa_report.md                Phase 12
  summary.md                  Phase 12 final report
  originals/                  dated copies of the manuscript and bib before editing
  gap_matrix_out/             (init) tables.tex from gap_table.py
  raw/source_records/         (init) <source_id>.md per included source
  raw/evidence_notes/         (init) longer reading notes when needed
  raw/verification/           (init) verify CSVs and raw API responses
```

If the project already has its own layout for these records, extend it and note the mapping in PROGRESS.md.

## Identifier rule

`source_id` = the BibTeX key, in every file. New keys follow `surnameYEARword` (what `doi2bib.py` generates). Keep existing keys unchanged, since renaming a key means editing every `\cite`.

## source_ledger.csv

One row per unique publication you screened, included or not. Statuses come from fixed vocabularies, and `check_ledger.py` rejects other values.

| Column | Values or content |
|---|---|
| source_id | BibTeX key |
| title, authors, year, venue, pub_type | From the verified record |
| doi, url | Canonical identifiers |
| peer_review_status | peer-reviewed, preprint, report, standard, thesis, book, other, unknown |
| version_note | e.g. "arXiv v2, published at ICLR 2021" |
| verification_status | VERIFIED, VERIFIED-QUALIFIED, UNRESOLVED, REJECTED, PENDING |
| verification_date | ISO date |
| verification_evidence | Saved response filenames, landing-page URL |
| access_level | FULLTEXT, ABSTRACT, METADATA |
| screening_decision | candidate, included, excluded |
| exclusion_reason | Required when excluded |
| relevance | essential, useful, optional |
| themes | Themes separated by " / " |
| cited_in_manuscript | yes, no |
| notes | Anything a later reader needs |

## extraction_sheet.csv

One row per included source. Keep source-derived content and your judgment in separate columns.

| Column | Content |
|---|---|
| problem, objectives, theory | As the authors state them |
| method, data, metrics | Architecture or design, datasets or sample, evaluation measures |
| key_findings | Exact reported values with their conditions |
| source_location | Section, table, figure, or page for each finding |
| author_limitations | Limitations the authors state |
| reviewer_limitations | Limitations you observe, labeled as yours |
| contributions | Authors' stated contributions |
| relevance_to_manuscript | Which claim or section it serves |
| evidence_strength | strong, moderate, weak, with one reason |
| conflicts | Sources it disagrees with, by source_id |
| uncertainty | Access limits, ambiguous reporting |

## raw/source_records/<source_id>.md

```markdown
# <source_id>

**Citation:** <authors> (<year>). <title>. <venue>. https://doi.org/<doi>
**Status:** VERIFIED (2026-10-22, Crossref record, raw/verification/<id>.crossref.json)
**Access:** FULLTEXT (publisher HTML) | Peer review: peer-reviewed

## What the source reports
- <finding with exact value and conditions> [Sec. 4.2, Table 3]
- <finding> [Sec. 5]

Short supporting excerpt (under 40 words, only when wording matters):
> "<excerpt>" [p. 7]

## What it does not establish
- <limits relevant to how the manuscript uses it>

## Use in the manuscript
| Claim id | Section | Supports | Qualification |
|---|---|---|---|
| C07 | 2.3 | full | on ImageNet only |

## Reviewer notes (my interpretation, not the authors')
- <assessment of rigor, conflicts with other sources>
```

Keep excerpts short and few. Do not copy large portions of copyrighted text.

## citation_map.csv (Phase 8)

Build it before editing the manuscript. One row per claim.

| Column | Values |
|---|---|
| claim_id | C01, C02, ... |
| section, location_hint | Section number and paragraph or the sentence's first words |
| claim_text | The claim as it will read |
| claim_type | definition, fact, method, comparison, result, limitation, gap, novelty |
| source_ids | Comma-separated keys |
| support | full, partial (partial needs a second source or a narrower claim) |
| qualification | Conditions the sentence must carry |
| priority | essential, useful, optional |
| status | planned, inserted, dropped |

Rules for the map:

- Each source in a row contributes distinct evidence. If two sources say the same thing, keep the stronger or the primary one, or synthesize them in the sentence.
- `result` and `comparison` claims need FULLTEXT sources, or the claim is limited to what the abstract states.
- `gap` and `novelty` claims point to the gap record in `gaps.md`, not to a single paper.
- Set `status` to inserted only after the citation is in the manuscript. `check_ledger.py` verifies it.
