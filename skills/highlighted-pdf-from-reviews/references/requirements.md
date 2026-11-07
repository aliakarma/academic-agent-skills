# Requirements for a Highlighted Revised Manuscript

The full specification this skill implements. SKILL.md gives the workflow; this
file is the contract the result is checked against.

Inputs: the revised manuscript source, the supplementary material (if any) and
the finalized Response to Reviewers. The current files are the authoritative
source for the revised manuscript; the Response to Reviewers is the authoritative
mapping between reviewer comments and the revisions made in response to them.

The highlighted manuscript is NOT a new revision of the scientific content. Do
not rewrite, improve, paraphrase, shorten, expand or otherwise alter the
scientific content, except to add reviewer-identification tags, highlighting
markup, navigation aids, or the front-matter change map.

## 1. Core objective
- Every substantive passage changed in response to a reviewer comment is visibly marked.
- Every highlighted revision carries the correct reviewer-comment ID.
- Every comment addressed in the Response to Reviewers is traceable to the revised material.
- An editor can move easily between comment ID, highlighted revision, manuscript location and the Response to Reviewers entry.
- The result stays essentially identical in scientific and structural content to the clean revised manuscript. Introduce no change that is not in the revised manuscript.

## 2. Full cross-check before editing
1. Read the complete Response to Reviewers.
2. Identify every reviewer.
3. Identify every comment ID: numbered comments, sub-comments, issue/weakness identifiers, reproducibility and editorial comments, and any special identifiers the letter uses.
4. Read the complete revised manuscript.
5. Read the complete supplementary material.
6. For every letter entry determine what changed; whether it is in the main manuscript or the supplement; the exact passage, paragraph, section, table, figure, equation, algorithm, appendix, reference or other element; and whether it occurs in one or several locations.
7. Verify every claimed revision against the actual revised files. A location stated in the letter is not by itself evidence that the text changed.

## 3. Comment-to-revision mapping
- Preserve the exact IDs established in the letter (e.g. R1.1, R1.Rep, R2.1, R3-04). Do not invent IDs unless absolutely necessary.
- When one revision addresses several comments, attach all IDs: `R1.3 · R2.5 · R3.2`.
- Do not split one continuous revision into many annotations, and do not merge unrelated revisions because they share a section.

## 4. What must be highlighted
Every substantive change made in response to peer review: revised sentences, clauses or phrases; new explanations and paragraphs; substantially rewritten paragraphs; replaced statements whose revised wording remains visible; new limitations or scope statements; revised methods or experimental details; new statistical analyses, datasets, experiments, ablations, validation procedures and error analyses; revised claims or conclusions; references added in response to reviewers; revised and new tables, figures, captions, equations, algorithms and appendices; supplementary revisions.

Do NOT highlight text merely adjacent to a revision, unchanged background text, or the whole manuscript. The objective is precise change tracking, not decoration.

## 5. Passage-level highlighting
Consistent yellow highlight with the ID immediately before it (`R1.3 · R2.4 [passage]`). IDs must be visually distinct annotation metadata and must not sit inside sentences in a way that changes their meaning.

## 6. Paragraph-level and large-element highlighting
A new or substantially revised paragraph gets a yellow annotation box with a small ID tab at its top left. Use it for new paragraphs, rewritten paragraphs, large blocks of revised methods, new discussion, limitations or interpretation, and other major revisions where sentence-level highlighting would be excessive. No nested highlighting inside a box.

## 7. Tables, figures, equations, algorithms and other objects
Mark the whole revised or new element with its ID(s) (box or similarly clear treatment) with the ID visible at the top left without obscuring content. Preserve the element's formatting, numbering, captions and labels; do not alter its content for highlighting. When only a caption changed, highlight the revised part of the caption. New tables or figures are marked in full.

## 8. Reviewer-ID traceability
A front-matter section such as "Revision Highlighting Guide and Reviewer Comment Map" explains the annotation system and contains a table with at least: ID | Reviewer | Comment / Issue | Highlighted Manuscript Pages. Preserve exact IDs, give a concise description from the letter, and list every highlighted page for each ID. Never invent page numbers; take them from the compiled highlighted manuscript. Distinguish supplementary locations from main-manuscript pages.

## 9. Navigation and hyperlinks
Where practical: IDs in the text link to their map entry; page numbers in the map link to the highlighted page; section, table, figure and equation references and all internal cross-references keep working. Use hyperref, cleveref, hypertarget and anchors. Do not break existing references or journal macros.

## 10. Page numbers and location verification
Compile, inspect the pagination, fill the map with the actual pages, recompile, verify. Use the highlighted manuscript's own page numbers, not the clean version's.

## 11. Preserve journal format
Keep the journal class, document structure, section hierarchy, title, authors, affiliations, abstract, keywords, references, tables, figures, equations, algorithms, appendices, supplementary structure, bibliography and citation style, and journal macros. The highlighting layer sits on top of the journal's structure. The clean revised manuscript remains a separate clean version.

## 12. Supplementary material
Apply the same principles: identify the ID for each supplementary revision, highlight it, preserve supplementary numbering and formatting, and give the supplementary location in the map. Distinguish main-manuscript from supplementary revisions.

## 13. Scientific integrity
Never invent revisions, IDs or locations; add claims; modify numbers, equations or references; change conclusions or terminology; silently correct content; rewrite unchanged sections; or drop reviewer-relevant revisions because they look minor. If the letter claims a revision that cannot be found in the supplied files, do not fabricate a highlight: flag it in a verification section with its ID and say that it could not be verified from the provided files.

## 14. Letter versus highlighted manuscript
The letter explains the revisions; the highlighted manuscript shows them. Use the letter for WHY, the revised manuscript for WHAT, and both together for WHICH ID. Highlight only material that was actually revised, not every location the letter mentions.

## 15. Multiple locations
Mark every location where a comment is addressed (abstract, introduction, methods, results, discussion, conclusion, tables, figures, supplement) with the same ID, and list all of them in the map.

## 16. New or major revisions
New experiments, tables, figures, ablations, subsections, statistical tests, robustness analyses, expanded limitations or revised theory get prominent boxed treatment; smaller textual changes get inline highlighting. Keep the result readable and professional.

## 17. Visual style
Restrained academic style: light yellow highlight, small consistent ID labels, subtle borders, clean typography, good contrast, readable in print and in grayscale. No excess colors; not a poster or decorative report.

## 18. Introductory note
Open with a concise note adapted to the journal, similar in purpose to: "This highlighted revised manuscript identifies changes made in response to the reviewers' comments. The clean revised manuscript is submitted separately. Reviewer-comment IDs correspond to the Response to Reviewers document. Yellow highlighting indicates revised text or passages, while boxed annotations identify substantially revised or newly added paragraphs, tables, figures, algorithms, or other major elements."

## 19. Completeness check
Before finalizing, audit every ID: Does the comment exist in the letter? Is the revision present? Is every revised location highlighted, with the correct and complete set of IDs? Are supplementary revisions included? Are the map's page numbers correct after compilation? Are new or revised tables and figures marked? Is any comment without a highlight, or any highlight without a comment?

## 20. Final quality control
Compile successfully; check LaTeX errors, broken references and hyperlinks, missing figures and tables; check that highlighting obscures nothing and IDs stay legible; check map page numbers; compile the supplement; verify that the clean manuscript's scientific content was not changed. If the journal class conflicts with highlighting packages, adapt the implementation, never the content or structure.

## 21. Final output
1. `[PaperName]_Highlighted.tex`
2. `[PaperName]_Supplementary_Highlighted.tex`, when the supplement is a LaTeX document
3. Supporting style/macro files (`rvhighlight.sty`)
4. `[PaperName]_Highlighted.pdf`

Never overwrite the clean revised manuscript. The result must be complete, compilable, professionally annotated, fully traceable to the Response to Reviewers, faithful to the revised manuscript, and precise enough for direct resubmission: every substantive revision traceable to at least one ID, and every ID traceable to its highlighted revision(s).
