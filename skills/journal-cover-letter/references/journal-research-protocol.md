# Journal research protocol (Stage 2)

Journal rules change. Research them for every letter, even for a journal handled before. Nothing in this file is a current policy. It tells you where to look and what to extract.

## Source hierarchy

Use the highest source that answers the question, and record which one did.

1. The journal's own Instructions for Authors or Guide for Authors page.
2. The publisher's general submission guidelines, when the journal page defers to them.
3. The journal's official Aims and Scope page.
4. The journal's official editorial-board page.
5. The publisher's publication-ethics policy pages.
6. Secondary sources (author-service blogs, university guides) only when 1 to 5 are silent. Label them secondary and never treat them as policy.

When the journal page and the publisher page conflict, the journal page wins. Record the conflict.

## Tools and fallbacks

1. WebSearch for `"<journal name>" guide for authors` and `"<journal name>" aims and scope`. Keep only official publisher domains.
2. WebFetch each official page. Read the cover-letter, submission-declaration, and article-type sections in full.
3. When WebFetch fails (403, an empty JavaScript shell, or a login wall), open the page in the browser tools (Claude in Chrome or playwright-cli) and read the rendered text.
4. When every route fails, use the journal documents the user supplied. Mark each requirement from them as "user-supplied, not independently verified". Never fill the gap from memory.

## Checklist

**A. Identity.** The official journal name as the journal writes it (capitalization, ampersands, "The"), publisher, the aims and scope text, subject areas, intended readership, accepted article types with their exact labels, and any stated editorial priorities.

**B. Submission requirements.** Answer each question with a quote or "not stated".

- Is a cover letter mandatory, optional, or not mentioned?
- Does the journal prescribe its content or structure?
- Is there a length limit?
- Which declarations must appear in the letter itself?
- Which declarations does the journal collect elsewhere (submission-system fields, title page, a separate form)?
- Does it require a novelty, significance, or highlights statement, and in the letter or separately?
- Must previous submissions, transfers, or prior interactions with the journal be disclosed?
- Must related or overlapping publications (conference versions, preprints, companion papers) be identified?
- Are suggested or opposed reviewers requested, and where?
- Are there extra rules for the article type, a special issue, or an extended conference paper?
- Does the journal ask for anything the letter must avoid (fee-waiver requests, for example)?

**C. Relevance.** Find two or three specific topics in the aims and scope that the manuscript serves, and the readership it reaches. When useful, find one or two recent articles in the journal on a close topic, recorded with DOI, as evidence that the topic is in scope. Do not cite them in the letter unless that genuinely helps the editor.

**D. Editor.** The Editor-in-Chief, or the handling or section editor for the manuscript's area, with the exact title as listed. Use a name only from the official editorial-board page opened in this run. Journals with many co-editors, or an editorial office that assigns editors, get "Dear Editor".

## Research record (scratchpad, not the project)

```
Journal: <official name>  | Publisher: <name>  | Accessed: <YYYY-MM-DD>
Sources:
  [S1] <URL>  established: <what>
  [S2] <URL>  established: <what>
Cover letter: <mandatory | optional | not stated> [S#], length limit: <value | not stated>
Prescribed content: <quote or "none stated"> [S#]
Declarations required IN the letter: <list with [S#]>
Declarations collected ELSEWHERE: <list with where, [S#]>
Disclosures that apply to this manuscript: <prior submission, conference version, preprint, special issue, transfer>
Article type: manuscript is <type> -> journal label "<label>" [S#]
Scope hooks: "<short quote 1>" [S#], "<short quote 2>" [S#]
Readership: <who> [S#]
Editor: <name, title> [S#]  |  or: not verified, use "Dear Editor"
Unverified or conflicting: <items>
```

## Publisher entry points

These are navigation leads observed on publisher sites. Confirm each one on the live site, and fall back to search when a pattern has moved.

| Publisher | Where the author instructions usually live |
|---|---|
| Elsevier | ScienceDirect journal page, "Guide for authors" (`sciencedirect.com/journal/<journal-slug>/publish/guide-for-authors`), which also carries the aims and scope. Editorial board under "About". WebFetch returned 403 here on 2026-11-14, so go straight to the browser. |
| Springer Nature | `link.springer.com/journal/<id>/submission-guidelines`. Editors under the journal's "Editors" page. |
| MDPI | `mdpi.com/journal/<journal>/instructions`, with aims and scope at `mdpi.com/journal/<journal>/about` and the board at `mdpi.com/journal/<journal>/editors`. WebFetch returned 403 on 2026-11-14, so go straight to the browser. |
| PLOS | `journals.plos.org/<journal>/s/submission-guidelines`, with scope and criteria at `journals.plos.org/<journal>/s/journal-information`. WebFetch worked on 2026-11-14. |
| Frontiers | Journal page, "For authors" then "Author guidelines". |
| IEEE | The journal's "Information for Authors" page on the IEEE or society site, and the IEEE Author Center. |
| Wiley | Journal homepage, "Author Guidelines". |
| Taylor & Francis | Journal page on tandfonline.com, "Instructions for authors". |
| ACM | Journal page on dl.acm.org, "Author Guidelines". |
| SAGE | Journal page on journals.sagepub.com, "Submission Guidelines". |

## Where policies usually differ

Check each of these instead of reusing an earlier letter's paragraph:

- Some journals list required letter content (originality, exclusivity, author agreement, prior submissions). Others say nothing and collect every declaration in the submission system.
- Competing interests, funding, ethics approval, and data availability usually belong in the manuscript or submission fields. Repeat them in the letter only when the journal asks.
- Extended conference papers often need the earlier paper named and the new material described, sometimes with a minimum share of new content.
- Special-issue submissions name the issue title, and sometimes the guest editors.
- Transfers between journals of the same publisher, and resubmissions of a previously declined manuscript, often must be stated.
- Preprints are welcome at many journals but must be disclosed at some.
