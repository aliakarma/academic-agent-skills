# Reference Verification Protocol (Phase 5)

Mandatory for every source proposed for the final manuscript, new or pre-existing. Two separate checks: identity (8.1 to 8.4 of the brief) and claim support (8.5). A source passes only when both pass.

## A. Identity check

### Step 1. Machine check

```
python scripts/verify_refs.py literature/references_lit.bib \
    --out literature/raw/verification/verify_<date>.csv \
    --raw-dir literature/raw/verification
```

The raw API responses saved in `--raw-dir` are the verification evidence. Cite their filenames in the ledger's `verification_evidence` column. Never write a verification record by hand that no tool produced.

### Step 2. Act on each machine_check value

| machine_check | Action |
|---|---|
| MATCH, no updates | Open the record URL once to confirm it is the intended work. Status `VERIFIED` |
| MATCH with a retraction, withdrawal, or expression of concern | `REJECTED`, unless the manuscript discusses that paper's retraction. Corrections and errata: keep, cite the corrected version, note it |
| PARTIAL | Read `issues`. Fix the bib field from the authoritative record (title wording, author count, year). Re-run. `VERIFIED-QUALIFIED` when a real difference remains (online vs. print year, version) and the note says which |
| MISMATCH | The DOI or id points to another work. Find the right identifier from the publisher page, re-run. Never "fix" by editing the title to match the wrong record |
| DOI_NOT_FOUND | The DOI does not exist. Search by title. If the work exists, replace the DOI. If nothing exists, `REJECTED` and record it as a possible fabrication |
| NO_DOI_CANDIDATE | Confirm the candidate on its landing page. Add the DOI only when `candidate_status` says confirmed or the record came from Crossref and you checked the landing page |
| NO_DOI_NO_MATCH | Look for the official record (proceedings site, standards body, government page, institutional repository). If found, `VERIFIED` with that URL as evidence. If not, `UNRESOLVED` |
| ERROR | The check did not happen. Retry later or verify by hand. Never record it as passed |

### Step 3. Metadata conflicts

When records disagree, use this order of authority and record the resolution:

1. Publisher landing page or the official proceedings page
2. Registration agency record (Crossref, DataCite, mEDRA, JaLC, KISTI)
3. Bibliographic indexes (PubMed, DBLP web page, ACL Anthology)
4. Aggregators (OpenAlex, Semantic Scholar, Google Scholar)

Known traps:

| Trap | What to do |
|---|---|
| Aggregator DOI points at an unrelated paper | Confirm at the agency. Seen in testing: Semantic Scholar lists a 2024 journal DOI for the 2017 SHAP paper |
| Crossref splits title and subtitle | Compare against both. `verify_refs.py` handles it |
| arXiv DOI (`10.48550/...`) on a conference or journal citation | Version mismatch. Cite the published version with its own DOI or URL, or cite the preprint as a preprint |
| Conference paper later extended into a journal article | Separate works. Cite the one whose content you use |
| Preprint superseded by the published version | Cite the published version unless the content differs. Note it |
| Year off by one | Online-first vs. issue year, or arXiv year vs. venue year. Use the venue's year and note it |
| NeurIPS, ICML, ICLR, many ACL papers | Often no DOI. The official proceedings or OpenReview page is the authority |
| LNCS and other series | Book title and series sometimes swapped in Crossref. `doi2bib.py` reorders them |
| Corporate or group authors | BibTeX needs double braces: `{{World Health Organization}}` |
| DOI registered with mEDRA, JaLC, KISTI, CNKI | `verify_refs.py` reports the agency. Check at `https://doi.org/<doi>` |

### Step 4. Non-DOI sources

Standards, policy documents, reports, theses, software, and datasets: verify on the issuing body's own page (ISO, IEEE SA, NIST, OECD, WHO, a university repository, Zenodo, Software Heritage). Record the URL and the access date. Do not invent a DOI. Do not cite a blog repost of a report when the original is reachable.

## B. Claim check

For each sentence a source will support (from the citation map):

1. Retrieve the best accessible version. Record `access_level` (FULLTEXT, ABSTRACT, METADATA).
2. Find the passage, table, or figure that supports the claim. Record its location in the source record (section, page, table number).
3. Compare the claim with the passage: the same quantity, the same conditions (dataset, setting, baseline), the same direction and strength. "Improves accuracy" from a source that reports one dataset becomes "improved accuracy on <dataset>".
4. Record what the source does not establish when the manuscript could be read as implying it.
5. If access is abstract only, limit the claim to the abstract's words and mark the record "abstract only". If only metadata, the source supports existence and topic, nothing more.

A claim check fails when the source says something different, says it under different conditions, or does not say it. Fix the sentence, find a source that does support it, or drop the claim.

## C. Recording

Ledger columns set in this phase: `verification_status`, `verification_date`, `verification_evidence` (filenames of the saved responses, landing-page URL), `access_level`, `peer_review_status`, `version_note`.

`raw/verification/` holds the machine-check CSVs and raw responses. Never delete them when re-running. Add a new dated CSV instead.
