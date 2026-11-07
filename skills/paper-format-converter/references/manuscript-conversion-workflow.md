# Manuscript conversion workflow

Read this before Phase 4. It covers the baseline, the LaTeX, Word, Markdown, and PDF routes, required statements, and anonymization.

## 1. Baseline the original

Copy the original project into the session scratchpad and build it there with its own configuration. Record the page count, errors, undefined references and citations, and warnings. The report needs this baseline to separate defects the author already had from defects the conversion caused. If the original does not build, record why and continue.

## 2. LaTeX route

1. Copy the template's sample `.tex` to `manuscript/main.tex`, or to the file name the venue requires. Keep its document class line, class options, required packages, front matter commands, and back matter order. Delete its demonstration text, figures, tables, and bibliography.
2. Choose class options that match the verified rules: journal or conference mode, review or anonymous mode, one or two columns, draft or final.
3. Move the content in. Keep the author's section files as `\input` children when the class allows it. Copy figure, table, and bibliography files with relative paths intact. A dependency outside the original folder gets copied into `manuscript/`, and its new path goes into the change log.
4. Front matter: title, authors in the original order, affiliations, corresponding author, emails, ORCID iDs, and funding notes go into the template's own macros. Leave out what the original lacks, unless the venue requires it. Then use a placeholder.
5. Packages: keep content packages (amsmath, amssymb, graphicx, booktabs, algorithm packages, tikz, pgfplots, siunitx). Remove packages that override what the class controls (geometry, fullpage, setspace, titlesec, fancyhdr, caption formatting, font packages), unless the guidelines allow them. Read the class documentation for packages it loads itself or forbids. Copy the author's macro definitions. Rename a macro only when it clashes with the class, consistently, and log it.
6. Citations: keep every citation key. Switch to the venue's bibliography style (`.bst` or biblatex style) and citation package. When the class has no natbib support, rewrite `\citet{key}` as the author name from the `.bib` entry followed by `\cite{key}`, and `\citep` as `\cite`. Convert between biblatex and BibTeX only when the venue requires it, and keep the same `.bib` data. Correct a reference only from authoritative bibliographic data, and log each correction. Never add, drop, or substitute an entry.
7. Figures: keep every image file unchanged. Set widths for the layout (`\columnwidth` in a two-column float, `figure*` with `\textwidth` for wide figures) and follow the venue's caption position. Convert a file format only when the venue demands it and the conversion is lossless. Otherwise log it.
8. Tables: keep every cell value. Follow the venue's caption position and table style. Prefer `table*` or a reflow over `\resizebox`, and never shrink text below the venue's minimum font size.
9. Equations and algorithms: keep the content. Change an environment only when the class requires it.
10. Back matter: follow the venue's required order and headings, through the class macros or environments the sample shows. Move each existing statement into its required section verbatim.
11. Appendices and supplements: follow the venue's placement rule. Move material to a separate supplementary file only when the venue requires it, and record the move.

## 3. Word route

1. Work on a copy of the original `.docx` inside `manuscript/`.
2. With Microsoft Word available on Windows, apply the template through COM automation. Turn macros off before opening anything, because downloaded templates are untrusted. When the official template is a `.docx`, first save a copy as `.dotx` (`SaveAs2` with format 14) in the scratchpad.

   ```powershell
   $word = New-Object -ComObject Word.Application
   $word.Visible = $false
   $word.AutomationSecurity = 3   # force-disable macros in every file opened here
   $doc = $word.Documents.Open("<copy in manuscript folder>")
   $doc.AttachedTemplate = "<official template .dotx>"
   $doc.UpdateStyles()
   $doc.Save()
   $doc.ExportAsFixedFormat("<output .pdf>", 17)
   $doc.Close()
   $word.Quit()
   ```

   Styles do not carry page layout, so copy margins, paper size, orientation, and column count from the template's `PageSetup` and `TextColumns` as well.
3. Without Word, edit the OOXML through the docx skill: bring in the template's styles and section properties (`w:sectPr`), then remap paragraph styles. Keep the original's images, equations, and relationships intact.
4. Map paragraphs to the template's styles: title, authors, affiliations, abstract, keywords, headings by level, body, captions, references, and statements.
5. Keep Office Math equations as equations. Never turn them into images.
6. Reference-manager fields (Zotero, Mendeley, EndNote) stay in place. Changing their style needs the reference manager itself, so log a Major issue when the venue's citation style differs. Rewrite plain-text citations only when the mapping is mechanical and checkable.
7. Tracked changes and comments stay untouched. List them as an issue when the venue expects a clean file.
8. Render the result to PDF for the checks: Word's `ExportAsFixedFormat`, or LibreOffice when installed.

## 4. Markdown route

Convert with pandoc when it is installed: to LaTeX inside the official template, or to Word with `--reference-doc` pointing at the official Word template. Map pandoc citations to the venue's citation system and keep the keys.

## 5. PDF-only source

This route loses information, so say so in every report and log a Critical issue.

1. Extract the text with `pdftotext`. Rebuild the manuscript text in the template exactly as written.
2. Retype each equation and table by reading the rendered pages, and mark each one with a `% [VERIFY AGAINST SOURCE PDF]` comment. List every one of them in the issue.
3. Extract embedded images with `pdfimages` when it is installed. Otherwise insert a labeled figure placeholder and ask the author for the original files.

## 6. Required statements and metadata

- Move each statement the original already has into the venue's required section verbatim.
- A required statement with no source text gets a visible placeholder at its required position, for example `\textbf{[AUTHOR INPUT REQUIRED: Funding statement. The venue requires one (G-12).]}` in LaTeX, or highlighted text in Word. Open one remaining issue per placeholder.
- Silence is not a statement. Never write "no funding", "no conflicts", "not applicable", or an ethics approval on the author's behalf.
- Classification metadata the venue requires (ACM CCS concepts, MSC, JEL, PACS, subject areas) is author input. You may suggest candidates in the issue, labeled as suggestions.
- Before delivery, search the converted files for every `AUTHOR INPUT REQUIRED` and confirm that each one has its issue.

## 7. Anonymization

Apply it only when the venue's rules require it at the selected stage.

1. Prefer the template's own switch, such as an anonymous or review class option, when it exists.
2. Remove or mask only what the policy names: author names, affiliations, emails, acknowledgments, funding details, self-identifying citations or wording, repository and project links, file names, and metadata.
3. Clear PDF metadata (`\hypersetup{pdfauthor={}}` or the class equivalent) and Word document properties (author, last modified by, comment authors).
4. When the venue asks for a separate title page, put the removed author block and statements there as their own file. The untouched original keeps everything else.
5. Check the compiled PDF text and the `pdfinfo` output for leftover names.

## 8. Change log

Keep a running list of every change for section C of `conversion-report.md`: markup, class, layout, citation commands, moved statements, renamed macros, inserted placeholders, anonymization edits, and every prose change a verified rule required.
