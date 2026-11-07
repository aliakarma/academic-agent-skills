---
name: reference-verify
description: Use when a scholarly, technical, standards, legal, software, dataset, or web reference (usually a BibTeX entry, often supplied one at a time with reviewer or automated-verifier comments such as "DEAD 202", "DOI not found", "title mismatch", "author mismatch", or "possibly hallucinated") must be independently checked against publisher, DOI, venue, repository, or issuing-body sources and returned as a corrected paste-ready BibTeX entry. Trigger on "reference-verify", "verify this reference", "check this BibTeX", "is this citation real", "fix this bib entry", "the verifier flagged this reference". Not for whole-file .bib formatting or style cleanup (bibtex-validator) or for finding new literature (Literature-Review).
---

# Reference verification

> **Paths.** `${CLAUDE_SKILL_DIR}` is the folder that holds this SKILL.md. Claude Code fills it in. In other agents, replace it with that folder's path. `${CLAUDE_SKILL_DIR}/../<skill>` is a sibling skill from the same collection, so install that skill too.

Verify each supplied reference independently. Treat the user's entry and any reviewer or automated-verifier comments as claims to investigate, not as evidence. Accuracy takes precedence over speed.

## Verification workflow

1. Identify the exact work and version from its DOI, official URL, title, and venue. Distinguish a journal version from a preprint, a conference paper from its extended article, a document from its hosting page, and a living website from a dated publication. If identity remains ambiguous, say so and do not assemble a purportedly verified entry.
2. Consult authoritative sources directly. Prefer the publisher's article or proceedings page and the source document itself; use a DOI registration record (such as Crossref) as a strong independent check. Relevant primary sources include IEEE Xplore, ACM Digital Library, SpringerLink, ScienceDirect, Wiley, PubMed/publisher records, and official journal, conference, institutional, and government sites. Use secondary indexes such as OpenAlex only to locate or cross-check, not to overrule stronger primary evidence without investigation. Do not interpret an automated `DEAD 202` flag alone as proof that a DOI URL is invalid; check the DOI resolution and publisher record.
3. Check every applicable field: author names and order; exact title and meaningful capitalization; container title; year; volume and issue; page span or article number; publisher; DOI; canonical URL; edition, editors, report number, version, and other source-specific details. Verify the source type (`@article`, `@inproceedings`, `@book`, `@techreport`, `@misc`, etc.). Check whether an apparent page span is a PDF page count or an actual published range. For online material, distinguish publication/update dates from access dates and inspect version-specific URLs where possible.
4. Compare the original entry field by field. Account for every changed, added, and removed field, including author parsing, name particles or compound surnames, conference naming, URL redirects, case-protection braces, and fields that are unsupported or not applicable. Preserve source facts; do not alter names or titles merely to fit a style preference. Keep the citation key unless the user requests a change.
5. If authoritative records disagree, inspect the actual work and venue/DOI metadata, explain which source governs the disputed field and why, and disclose unresolved conflict. Do not guess any missing metadata. Never invent a DOI, page range, issue, date, person, publisher, or version. A date inferred only from a filename or crawl timestamp is not a verified publication year.
6. Produce syntactically valid, paste-ready BibTeX containing only supported facts. Retain genuinely supported fields and omit unsupported ones, with each omission explicitly listed as **unverified** in Notes. Do not put placeholders such as `unverified` inside BibTeX fields. For a living webpage without a verified publication year, omit `year` and record the access date in `note` for classic BibTeX, or `urldate` if the user's entry/style uses BibLaTeX. If no authoritative source confirms the work's identity, do not output a corrected entry; explain what evidence is needed under the required BibTeX heading.

## Status and response

- **Verified:** The work's identity and all included substantive fields have direct authoritative support, with no material unresolved conflict.
- **Partially verified:** The work is identifiable, but one or more supplied or potentially important fields remain unverified or conflicting. Supply only the verified subset of metadata and disclose the gap.
- **Not verified:** No authoritative evidence establishes the exact work. Do not label the supplied entry as verified.

Use exactly this response structure for each reference:

**Verification status:** Verified / Partially verified / Not verified

**Source(s) checked:** Name and link each authoritative source actually consulted, with citations when available.

**Corrections made:** Briefly enumerate every difference from the original entry, including omissions and formatting changes. State “None” when appropriate.

**Final verified BibTeX:**

```bibtex
@type{originalKey,
  field = {verified value}
}
```

**Notes:** State unresolved uncertainty, source disagreement, and each field that could not be independently verified. If no authoritative source confirms the work, replace the code block with a brief statement that no verified BibTeX can yet be produced.

Never emit the final BibTeX before actually checking authoritative sources for that reference. If direct source access fails, say what was and was not independently inspected; a search snippet alone may support a limited fact but not an unexamined document's full metadata.

---

## Run procedure (how to apply the workflow above)

The sections above are the contract. Everything below explains how to meet it with the tools in this environment.

1. **Save the entry.** Write the user's entry, unchanged, to a file in the session scratchpad (`entry.bib`). Write any reviewer or verifier comments down as a numbered list of claims to test.
2. **Pull registry evidence.** Run `python "${CLAUDE_SKILL_DIR}/scripts/fetch_metadata.py" <scratchpad>/entry.bib`. You can also pass `--doi <DOI>`, `--arxiv <id>`, or `-` for stdin. The script reports:
   - DOI registration through the doi.org handle API, which never contacts the publisher. A 200 response there settles a `DEAD 202`, 403, or 418 flag: those flags come from publisher sites that block bots. A 404 means the DOI is not registered.
   - The registration agency (Crossref, DataCite, mEDRA, and so on).
   - The Crossref, DataCite, or arXiv record, including type, every date, relations, and retraction or correction updates.
   - A field-by-field diff labeled `match`, `DIFF`, `BIB-ONLY`, `REGISTRY-ONLY`, or `TRUNCATED (and others)`.
   - Crossref title-search candidates when no DOI exists. A candidate is a lead, not an identity match.
3. **Open the governing source.** Look up the reference's type in [references/source-guide.md](references/source-guide.md), then open that page: the publisher page, the proceedings page, OpenReview, the ACL Anthology, the standards body, or the official legislation site. Use WebFetch, or the `web-fetch` agent if WebFetch is missing. Use WebSearch only to find the page. If the site blocks automated fetches (IEEE Xplore, ScienceDirect, and ACM often do), use the Chrome browser tools. If every route fails, say exactly that under **Source(s) checked**. Never present the Crossref record as if you had seen the publisher page.
4. **Check the document when fields are disputed.** A PDF's first page or the copyright page settles author spelling, title, and the page range of the version of record.
5. **Account for every field.** Go through the diff and the source page one field at a time. Name each changed, added, or removed field under **Corrections made**. Answer each reviewer or verifier claim in **Notes** with "confirmed", "refuted", or "unresolved", plus the evidence.
6. **Run the format check.** Save the drafted response to the scratchpad and run `python "${CLAUDE_SKILL_DIR}/scripts/check_response.py" <file> --key <originalKey>`. Fix every ERROR. A WARN needs a deliberate decision. Then send the response.

## Input handling

- **Several entries at once.** Handle them in the order given. Give each one its own complete response block and its own lookups. Separate blocks with `---`. Evidence for one entry never counts for another.
- **Encoding.** Keep the user's LaTeX conventions (`{\"u}` or a literal `ü`, `--` page ranges, the field order) unless a convention is wrong. Use case-protection braces for acronyms and proper nouns that the source title capitalizes (`{IoT}`, `{B}ayesian`). Never lowercase or re-case a title to match a style.
- **BibTeX or BibLaTeX.** Match the user's dialect: `journal` versus `journaltitle`, `year` versus `date`, `note` versus `urldate`. Do not convert dialects unless the user asks.
- **Preprint and published version both exist.** Verify the version the entry cites. Report the other version in Notes and let the user choose. Do not swap versions silently.
- **Integrity signals.** If the DOI is not registered, the DOI resolves to a different work, the authors belong to another paper, or only near-miss titles turn up, treat the reference as possibly fabricated. Report it under **Not verified** and name the evidence that would settle it.
- **Prose.** Apply the user's house style, if they supply one, to Notes and Corrections (for example, no em dashes and no semicolons). Never change quoted titles to meet a style rule.

## Common mistakes

| Mistake | Correction |
|---|---|
| Treating the Crossref record as the final word | Crossref is a strong check. The publisher page or the document governs disputed fields. |
| Calling a DOI dead because a checker returned 202 or 403 | Check the doi.org handle API. Bot blocks are not dead DOIs. |
| Keeping `pages = {1--15}` for an article-number journal | That range is the PDF page count. Use the article number. |
| Expanding `and others` from memory | Take the full author list only from a source you opened, then report the change. |
| Writing a NeurIPS, ICLR, or arXiv DOI that you never saw | Omit the field and list it as **unverified** in Notes. |
| Giving a living webpage the crawl year as its `year` | Omit `year`. Record the access date in `note` or `urldate`. |
| Marking an entry Verified while Notes lists unverified fields | Use Partially verified. |
| Editing the citation key or the title's wording to match a style | Keep the key and the source's wording. |
| Applying one entry's lookup to the next entry in a batch | Look each entry up again from scratch. |

## Files

- `scripts/fetch_metadata.py`: registry lookup and field diff. Run `--selftest` for the offline tests.
- `scripts/check_response.py`: checks the response structure. Run `--selftest` for the offline tests.
- `references/source-guide.md`: which source governs which field, by reference type, plus integrity signals.
