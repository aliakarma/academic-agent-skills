# Research and source verification

Read this before Phase 2. It explains how to find the venue's official rules, how to record the evidence, and what `Journal-Guidelines.md` must contain.

## 1. Pin down the venue

- Record the official name and abbreviation, the publisher or organizing body, and the print and online ISSN for a journal. For a conference, record the edition, year, dates, track, paper category, and proceedings publisher.
- Rule out look-alikes before you research: a society journal and a publisher title with a similar name, a "Letters" or "Open" variant, a conference and its co-located workshops. Confirm the venue on its official homepage, not from a search result title.
- For a conference, research the edition the author targets. When the project does not name one, take the next open submission cycle and say so. A past edition's rules prove nothing about the current one.

## 2. Source hierarchy

1. The venue's own author instructions: the journal's guide or instructions for authors, or the conference call for papers and author kit.
2. The publisher's general manuscript preparation and submission pages.
3. The official template package or template page.
4. Official policy pages and submission-system help that settle a specific requirement.
5. Anything else, only when sources 1 to 4 are silent or unreachable, and labeled secondary.

Rules on the venue's own page override the publisher's general rules for that venue. A generic publisher template proves layout only, never the venue's limits or policies. Take templates from official channels, never from mirrors. CTAN counts as official for a class its publisher maintains there. An Overleaf template counts when the publisher published it or links to it from its own site.

## 3. Search and fetch

- Start with WebSearch in standard mode. Useful queries: `"<venue>" author guidelines`, `"<venue>" guide for authors`, `"<venue>" submission guidelines template`, and for a conference `"<venue> <year>" call for papers` and `"<venue> <year>" author kit`. Switch to extended mode when results are thin, outdated, or unofficial.
- Open each page with WebFetch and ask for the requirement sentences verbatim. Never ask for a summary of rules you will enforce.
- When WebFetch is blocked (403, 429, or an empty JavaScript page), try in order: the browser tools when connected (Claude in Chrome or Chrome DevTools, with page text extraction), the publisher's PDF version of the guide, the template's README or sample text, and a dated Wayback Machine snapshot of the official URL. Record which route produced each fact.
- A fact seen only in a search snippet is Unverified.

## 4. Verify every quantity

For each limit (abstract words, main-text words, pages, keywords, figures, tables, references, title length):

1. Quote the source sentence exactly.
2. Confirm the quote in the raw page or PDF when you can, for example with `curl.exe -sL "<url>"` and a text search, or with `pdftotext` on a downloaded guide.
3. Record what the limit covers (references, appendices, captions, tables, figure text, supplementary material) and when it applies (initial submission, final submission, or both).
4. If the source does not say how to count, write that down and state the counting method you will use.

## 5. What to establish

Check every row. Record what applies to this venue, article type, and stage. Write "Not stated in the official sources" for anything the sources do not cover.

| Area | Items |
|---|---|
| Structure | section order and mandatory headings, title page, abstract format (structured or unstructured), keywords (count and any controlled vocabulary such as ACM CCS or MeSH), highlights, graphical abstract, conclusions, acknowledgments, appendices, mandatory statements |
| Limits | pages, main-text words, abstract words, keywords, figures, tables, references, what each one counts, and how they differ by article type |
| Layout | document class or Word template, paper size, columns, font and size, margins, line spacing, line and page numbers, heading levels, title and author block, equations, algorithms, floats, captions, citation and reference style |
| Policies | review model (single-blind, double-blind, open), anonymization, funding, competing interests, ethics approval, informed consent, data and code availability, author contributions (CRediT or other), generative AI disclosure, reporting guidelines such as PRISMA or CONSORT when the article type calls for one, preprint policy |
| Submission | required source files, PDF, file formats and names, figure file specifications, supplementary files, whether the template is mandatory at this stage, submission system |

## 6. Conflicts

List every disagreement between sources. Settle it in this order: the more specific source wins (journal over publisher, track over conference), then the more recent dated source, then the written instructions for limits and policies and the template for the layout details it encodes. If a conflict survives all of that, record it as unresolved, apply the stricter reading, and open a remaining issue.

## 7. Get the template

- Find the direct download on the official page. Record its URL and any version or date shown, and later the `\ProvidesClass` version that `safe_extract.py` prints.
- Choose the package that matches the source format (LaTeX or Word) and the article type. Keep the archive in `official-template/`.
- If a guideline exists only as a PDF, keep that PDF in `official-template/` and cite its local path in the source register.
- If the download needs an account or a captcha, or fails, record exactly what happened. Then fall back in this order: the class on CTAN when the publisher maintains it there, or the written rules alone. Name the fallback in all three reports. Never claim an official template you did not obtain.

## 8. Template for Journal-Guidelines.md

Keep the file name `Journal-Guidelines.md` for conferences too. Fill every section. Quote only the sentence that carries each rule and summarize the rest, because the guidelines are copyrighted. The example rows show the format only. Replace them.

```markdown
# Journal Guidelines: <Canonical Venue Name>

## A. Venue identification

| Field | Value |
|---|---|
| Canonical venue name | |
| Publisher or organizing body | |
| Venue type | Journal, conference, or proceedings |
| Edition or publication cycle | |
| ISSN or proceedings series | |
| Article or submission type | <type>, chosen because <evidence> |
| Submission stage | Initial submission or camera-ready |
| Requirements checked on | YYYY-MM-DD |
| Official template | <name, version or date, URL>, or "Not obtained: <reason>" |

## B. Official source register

| ID | Source | Official URL | Information verified | Access date |
|---|---|---|---|---|
| S1 | <page title> | <URL you opened> | <what it established> | YYYY-MM-DD |

## C. Compliance requirements

| ID | Requirement | Official rule or limit | Level | Applicability | Source | Verification method |
|---|---|---|---|---|---|---|
| G-01 | Abstract length | "<quoted rule>" | Mandatory | <article types and stage> | S1 | <tool and method> |

Level is Mandatory, Recommended, Optional, or Unverified.

## D. Formatting rules

Class or template, layout, typography, headings, citations and references, figures, tables, equations, and algorithms. For LaTeX, name the class and bibliography style files.

## E. Structural requirements

Section order, abstract format, keywords, declarations, supplementary material, and rules for this article type.

## F. Quantitative limits

| Quantity | Limit | Includes | Excludes | Counting method | Source |
|---|---|---|---|---|---|

## G. Submission and review requirements

Review model, anonymization, source files, PDF, file formats, and supplementary files.

## H. Conversion implications

What this manuscript must change: class and packages, citation commands, missing declarations, structure, and length.

## I. Uncertainties and conflicts

| Topic | Sources | What is unclear | Resolution or status |
|---|---|---|---|
```
