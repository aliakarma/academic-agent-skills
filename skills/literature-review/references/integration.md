# Writing and Integration (Phases 9 and 10)

## 1. Structure the review around an argument

Organize by research question, approach family, or the field's development, whichever serves the manuscript's argument. Move through:

1. Foundations the work builds on
2. The main approaches and how they differ
3. What the evidence shows when the approaches are compared
4. Where results conflict, and why (data, assumptions, evaluation, problem definition)
5. The specific unresolved problem
6. How the manuscript responds to it

Draft in `literature/review_body.md` first when the change is large.

## 2. Paragraph recipe

A comparative paragraph has these parts in order:

1. A claim about a group of studies (the point of the paragraph)
2. Evidence from two or more studies, each cited at the clause it supports
3. The difference between them and its cause
4. What this means for the manuscript's problem

Before:
> Smith et al. [1] proposed method A. Lee et al. [2] proposed method B. Kim et al. [3] proposed method C.

After:
> Perturbation-based attribution methods agree poorly with each other on the same model. On ImageNet classifiers, Smith et al. [1] report rank correlations below 0.3 between LIME and SHAP attributions, and Lee et al. [2] observe the same disagreement on tabular credit data. Kim et al. [3] trace part of it to the choice of baseline input, which neither earlier study fixed. Faithfulness comparisons that do not control the baseline therefore conflate method and configuration.

(The example illustrates the shape only. Its claims are not real findings.)

## 3. Citation placement rules

- Cite at the clause the source supports, not at the end of the paragraph.
- One claim, the sources that each add evidence for it. No clusters of five for a general statement unless the sentence states that many studies report it, and then choose representative ones.
- Every number carries its condition: dataset, setting, baseline, metric.
- Never combine numbers from incomparable experiments into one comparison.
- Use natbib's `\citet` for author-as-subject and `\citep` for parenthetical, or the biblatex equivalents (`\textcite`, `\parencite`), matching the manuscript's existing use.
- Strengthen sections beyond related work where evidence is thin: introduction motivation, method design rationale, discussion comparisons with prior results, limitations.

## 4. Editing a LaTeX manuscript

- The originals are in `literature/originals/`. Edit the working file in place.
- Keep the document class, packages, macros, labels, and cross-references. Do not add packages unless needed, and note any you add.
- Move verified entries from `literature/references_lit.bib` into the active bib (the one `\bibliography{}` or `\addbibresource{}` names). Check with `audit_citations.py` before and after.
- BibTeX hygiene: escape `%`, `&`, `_`, `#`, `$` in non-URL fields. An unescaped `%` comments out the rest of the line in the `.bbl` and silently truncates the reference. Protect acronyms and proper nouns in titles with braces (`{SHAP}`, `{Bayesian}`). Use `--` for page ranges.
- Compile with the project's build (latexmk, or pdflatex, bibtex, pdflatex, pdflatex) and read the log for undefined citations and BibTeX warnings. Report the result as it is.

## 5. Editing a Word manuscript

- Use the docx skill. Keep headings, styles, tables, figures, and the reference style.
- If citations are Zotero or EndNote fields, do not flatten them to text. Add new references the same way, or list them for the author with exact insertion points when field codes cannot be edited safely.
- Save the revised manuscript as a new file next to the original with a clear suffix (for example `_litreview`), and name it in the summary as the final version.

## 6. Correcting existing claims

When the evidence contradicts or overstates a manuscript claim:

- Narrow the claim to what the evidence supports and cite the evidence.
- Record each change (location, old text, new text, reason, source_ids) in `summary.md`.
- Do not change the manuscript's own results, methods, or data. If those look inconsistent with the literature, report it to the author instead.

## 7. Language

American English unless the venue requires otherwise. Apply the user's writing-style rules (memory, CLAUDE.md) to every inserted sentence. Keep the manuscript's voice, tense conventions, and terminology. Introduce no new acronyms without definition.
