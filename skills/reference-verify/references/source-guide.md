# Source guide: which source governs which field

Read the row for the reference's type before you look anything up. "Governs" means the source wins a disagreement unless the document itself shows otherwise. Registry records (Crossref, DataCite) are strong cross-checks. Indexes (Google Scholar, Semantic Scholar, DBLP, OpenAlex, ResearchGate) only help you locate a work. Never let an index overrule a primary source.

## Scholarly works

| Type | Governing source | Watch for |
|---|---|---|
| Journal article | Publisher article page and the PDF's first page. Crossref as cross-check. | Early-access or online-first versions have no volume, issue, or pages yet. The year of the version of record can differ from the online year. Report both dates and say which one the entry uses. |
| Article-number journals (MDPI, Elsevier, Frontiers, PLOS, IEEE Access, Nature family, Wiley e-journals) | Publisher page | The "page" is an article number (`pages = {1234}` or `eid`). A range like `1--15` is usually a PDF page count, so do not use it. |
| IEEE conference | IEEE Xplore page and Crossref | The proceedings title carries the year and the acronym, e.g. "2016 IEEE Conference on Computer Vision and Pattern Recognition (CVPR)". The CVF open-access version has no DOI or pages. Say which version is cited. |
| ACM conference | ACM DL page | The booktitle is "Proceedings of the ...". Since about 2017, many ACM papers carry an article number and a page count instead of a page range. |
| Springer LNCS, CCIS, LNAI | SpringerLink chapter page | `@inproceedings` with `series`, `volume`, `editor`, and the chapter page range. The year comes from the volume, not the event. |
| NeurIPS / NIPS | proceedings.neurips.cc paper page | Volume number (e.g. Advances in Neural Information Processing Systems 30). The page numbers in older citations came from the old printed proceedings. Check them against the official page. Most papers have no DOI. Never invent one. |
| ICML, AISTATS, COLT, CoRL | proceedings.mlr.press | `series = {Proceedings of Machine Learning Research}`, PMLR volume, pages. |
| ICLR | openreview.net forum page | Conference year. No volume, pages, or DOI. Accepted-paper status (oral, spotlight, poster) is not a bibliographic field. |
| AAAI | ojs.aaai.org article page | Volume, number, pages, DOI `10.1609/aaai.v{vol}i{num}.{id}`. |
| ACL, EMNLP, NAACL, Findings | aclanthology.org | The Anthology's own BibTeX is the reference export. Check it against the page anyway. |
| arXiv preprint | arXiv abs page and the arXiv API | v1 submission date versus last revision date. `journal_ref` or a `doi` that points to a published version means a version-of-record exists. Report it and do not silently swap versions. The arXiv DOI is `10.48550/arXiv.{id}`. |
| Other preprints (bioRxiv, medRxiv, SSRN, TechRxiv, Research Square) | Server page and DataCite or Crossref (posted-content) | Later journal publication. Version suffixes such as `.v1`. |
| Book | Publisher catalogue page, then the copyright page | Edition, ISBN (print versus e-book), publisher, year of that edition. A reprint year is not the original year. |
| Book chapter | Publisher chapter page | Chapter authors versus volume editors, book title, chapter page range. |
| Thesis | University repository record | Degree type (`@phdthesis` or `@mastersthesis`), institution, year of award. |

## Technical, standards, and legal

| Type | Governing source | Watch for |
|---|---|---|
| Technical report | Issuing institution's page | Report number, `institution`, `type`. |
| NIST publication | csrc.nist.gov or nvlpubs.nist.gov | Revision suffix (SP 800-53 Rev. 5), DOI `10.6028/NIST...`, withdrawn or superseded status. |
| ISO / IEC standard | iso.org catalogue page | The edition year is part of the identifier (ISO/IEC 27001:2022). Confirmed and withdrawn status. |
| IEEE standard | IEEE Xplore standard page | Standard number, year, DOI `10.1109/IEEESTD...`, superseded status. |
| RFC | rfc-editor.org info page | `number`, `series = {Request for Comments}`, DOI `10.17487/RFC{n}`, month and year, obsoleted-by. |
| W3C, IETF draft, other spec | Dated, version-specific URL (`/TR/YYYY/...`) | A dated recommendation is not the same as the living "latest" URL. A draft is a draft. |
| Statute or regulation | Official legislation site (legislation.gov.uk, eur-lex.europa.eu with CELEX number and OJ reference, govinfo.gov, eCFR, national gazette) | Enactment versus amended or consolidated version. Use the official title and number. |
| Court decision | Official court site or official reporter | Neutral citation, court, decision date, case number. |
| Government or agency report | Issuing body's page | Report number, publishing body as author when no person is named. |

## Software, data, and web

| Type | Governing source | Watch for |
|---|---|---|
| Software | CITATION.cff in the repository, Zenodo record, release page | A version DOI versus the concept DOI. The release date of the cited version. Authors listed in CITATION.cff, not GitHub usernames. |
| Dataset | Repository landing page (Zenodo, Figshare, Dryad, Kaggle, UCI, PhysioNet) and DataCite | Version, publisher (the repository), DOI. Many datasets ask you to cite a paper instead. Report that request. |
| Webpage, blog, documentation | The page itself | A living page has no publication year unless the page states one. Wayback captures can show a page existed on a date. They do not establish the publication date. Record the access date. |

## Integrity signals (report them, never fix them silently)

- The DOI is not registered (doi.org handle 404) or it resolves to a different work.
- A title search returns only near-miss titles, or the author list belongs to a different paper.
- The volume does not match the year for that journal, the page range lies outside the issue, or the venue did not exist that year.
- The publisher's record or Crossref `update-to` shows a retraction, an expression of concern, or a correction.
- Reviewer or automated-verifier comments contradict each other. Test each claim on its own.

Any of these makes the identity question unresolved until you inspect the actual work. A reference with no authoritative trace is **Not verified**, even if it looks plausible.
