# Compliance and quality assurance

Read this before Phase 5. It covers tool detection, the build, log and PDF checks, measurements, the integrity check, the two report files, and the readiness label.

## 1. Detect tools

Bash:

```bash
for t in latexmk pdflatex xelatex lualatex bibtex biber texcount pdfinfo pdffonts pdftotext pdftoppm pdfimages pandoc; do
  command -v "$t" >/dev/null && echo "found $t" || echo "MISSING $t"
done
```

PowerShell:

```powershell
'latexmk','pdflatex','xelatex','lualatex','bibtex','biber','texcount','pdfinfo','pdffonts','pdftotext','pdftoppm','pdfimages','pandoc' |
  ForEach-Object { if (Get-Command $_ -ErrorAction SilentlyContinue) { "found $_" } else { "MISSING $_" } }
```

A missing tool is a finding, never a reason to install anything. Record it, skip the checks that need it, mark them UNVERIFIED, and open an issue.

## 2. Build

1. Take the engine and the bibliography tool from the template's instructions: pdfLaTeX unless the class needs XeLaTeX or LuaLaTeX, and BibTeX or Biber as the template's bibliography setup implies.
2. Run in `manuscript/`:

   ```bash
   latexmk -norc -pdf -interaction=nonstopmode -file-line-error main.tex
   ```

   Swap `-pdf` for `-pdfxe` or `-pdflua` when the engine requires it. `-norc` stops latexmk from reading any `latexmkrc`, including one the template shipped.
3. Without latexmk: the engine, then `bibtex main` or `biber main`, then the engine twice more.
4. Never add `-shell-escape` or `--enable-write18`. The default restricted mode covers normal templates. If the template truly needs shell escape, skip that step and log a Major issue.
5. Fix the errors the conversion caused and rebuild until the log is stable. Report a missing package. Never install it.
6. Copy the final PDF to `converted-paper.pdf` in the output folder.

## 3. Log checks

Search `main.log`, and `main.blg` from BibTeX or Biber, for:

| Pattern | Meaning |
|---|---|
| lines starting with `!`, or `file:line: error` | errors |
| `Citation ... undefined`, `There were undefined citations` | unresolved citations |
| `Reference ... undefined`, `There were undefined references` | broken cross-references |
| `multiply defined` | duplicate labels |
| `not found` | missing files |
| `Overfull \hbox` | overflow. Report anything over 10pt and anything visible on the page |
| `Font Warning`, `Missing character` | substituted fonts or missing glyphs |
| `Rerun to get` | the build has not settled. Rebuild |
| `Warning--`, `I didn't find a database entry`, `Repeated entry`, `ERROR` in the `.blg` | bibliography problems |

Compare against the baseline log of the original. Sort every warning as pre-existing, caused by the conversion, or harmless, and fix the ones the conversion caused.

## 4. PDF checks

- `pdfinfo converted-paper.pdf`: page count, page size (A4 or US Letter as required), and metadata. Author and Title matter for anonymization.
- `pdffonts converted-paper.pdf`, when installed: fonts embedded where the venue requires it.
- `pdftotext converted-paper.pdf -`: search for `??`, `[?]`, `AUTHOR INPUT REQUIRED`, and distinctive strings from the template sample (its title, its author names, its first sentence, "Lorem ipsum").
- `pdftoppm -png -r 50 converted-paper.pdf "<scratchpad>/page"`: look at every page. Check columns, floats, caption position, equations, tables, page breaks, blank pages, clipped content, and the title block. Render a single page at higher resolution where something looks wrong.
- `pdftotext` separates pages with form feeds, so the page that holds the references heading gives the length of the main text.

## 5. Measurements

Measure only what the guidelines limit, by the venue's counting rule. Record the tool, the command, and the number.

| Quantity | LaTeX | Word |
|---|---|---|
| Words | `texcount -inc -total main.tex` reports text, headers, and captions separately. Add the categories the venue counts | Word `ComputeStatistics(0)` on the document or a range, or the text through python-docx |
| Abstract words | copy the abstract text into a scratch `.tex` file and run `texcount -1 -sum` on it | `ComputeStatistics(0)` on the abstract paragraphs |
| Pages | `pdfinfo` | `ComputeStatistics(2)` or the exported PDF |
| Figures and tables | `\contentsline {figure}` and `\contentsline {table}` entries in `main.aux`, and the source environments | images, tables, and captions in the document |
| References | `\bibitem` entries in `main.bbl` | entries in the reference list |
| Keywords | items in the keyword command or environment | items in the keyword paragraph |

When the counting rule is ambiguous, state the method you chose and the uncertainty. Never present an estimate as a measurement.

## 6. Content integrity

```bash
python -I "<skill dir>/scripts/conversion_integrity.py" "<original root>" "<converted root>" --template "<template sample>"
```

Pass `.tex` roots for LaTeX and the `.docx` files for Word. For a PDF-only source, pass the `pdftotext` output of the original and expect page numbers and running headers among the missing numbers and sentences.

| FAIL | Action |
|---|---|
| sentences missing | Restore them, or justify each one: a phrase the venue mandates, anonymization, a citation command rewritten into author names |
| numbers or math missing | Restore them. Only layout values with no scientific meaning may go, and each one is listed |
| cite, label, ref, urls, or graphics missing | Restore them |
| fewer figures, subfigures, tables, algorithms, or captions | Restore them |
| sections missing | Restore them, or cite the venue rule that renamed or moved them |
| template text | Delete the leftover template sentences |
| inputs | Copy the missing files into `manuscript/` |

WARN lines list added content. Expected additions are placeholders that each have an issue, headings the venue requires, and template metadata the venue requires at this stage. Remove or explain everything else.

Then check by hand that the title, the author names and order (unless anonymized), and the abstract text match the original, and that every statement from the original is present.

## 7. remaining-issues.md

Severity labels:

- **Critical**: a known mandatory requirement is unmet or cannot be verified, with a material risk of rejection or policy noncompliance.
- **Major**: a significant format, structure, or content requirement is unresolved, and its impact depends on editorial or author decisions.
- **Minor**: a limited formatting or verification gap that would not decide eligibility by itself.

Every FAIL and every UNVERIFIED Mandatory requirement gets an issue. Record a numerical mismatch with both the observed count and the limit. Record a rule only after you verified it, or label it Unverified. Number issues R-001, R-002, and so on.

```markdown
# Remaining Issues: <Venue>

| Field | Value |
|---|---|
| Target venue | |
| Conversion date | YYYY-MM-DD |
| Check status | <for example: build PASS, 18 of 22 requirements checked, 4 UNVERIFIED> |
| Basis | Compliance is assessed against the requirements in Journal-Guidelines.md and the checks in conversion-report.md. Passing them does not guarantee editorial acceptance. |
| Open issues | Critical: <n>, Major: <n>, Minor: <n> |

## R-001: <short title>

| Field | Value |
|---|---|
| Severity | Critical, Major, or Minor |
| Category | Length, structure, references, metadata, ethics, template, anonymization, build, or other |
| Official requirement | <rule> (G-xx, Sx) |
| Observed state | <what the converted manuscript has, with numbers> |
| Reason unresolved | <what blocked an automatic fix> |
| Required action | <the exact next step> |
| Responsible party | Author, or Claude in a follow-up run |
| Submission impact | Blocks submission, or creates uncertainty |
```

With no open issue, replace the issue sections with: "No unresolved issues were identified in the checks performed. Checks run: <list>. This does not guarantee editorial acceptance or cover requirements outside Journal-Guidelines.md."

## 8. conversion-report.md

The example row shows the format only. Replace it.

```markdown
# Conversion Report: <Venue>

Run status: Phase <n> of 8, <phase name> (updated YYYY-MM-DD HH:MM)

## A. Conversion summary

Target venue, original manuscript and source folder, article type and the evidence for it, submission stage, output folder, and conversion date.

## B. Source and template

Source files used. Official template: name, URL, version, and the class version line, or why it was not obtained. Files kept, added, or adapted. Template parts that were unavailable.

## C. Changes made

Formatting and structural changes from the change log: class and layout, title and author block, headings, abstract and keywords, figures, tables, equations, bibliography and citations, statements, and anonymization. List any content change separately and say why it was necessary.

## D. Compliance verification

| Requirement | Expected | Observed | Status | Evidence |
|---|---|---|---|---|
| G-01 Abstract length | <limit from G-01> | <measured value> | PASS | <command and output> |

## E. Build and validation

| Check | Result | Evidence |
|---|---|---|
| Build | | engine, command, exit status |
| PDF generated | | path, page count |
| Citations and bibliography resolved | | log lines |
| Figures and tables present | | page view, counts |
| Cross-references resolved | | log lines |
| Quantitative limits checked | | section D |
| Content integrity | | conversion_integrity.py result |
| Remaining warnings | | sorted list |

## F. Final assessment

Readiness label, what is complete, what remains by R-ID, and the blockers.
```

## 9. Status words and readiness

Status words for section D:

- **PASS**: checked and compliant. PASS requires a check you ran.
- **FAIL**: a confirmed requirement is not met.
- **WARN**: a possible problem, or an incomplete check.
- **UNVERIFIED**: no reliable evidence either way.
- **NOT APPLICABLE**: the requirement does not apply to this manuscript.

Give exactly one readiness label:

- **SUBMISSION-READY**: the build succeeded, every Mandatory requirement is PASS or NOT APPLICABLE, and no Critical or Major issue is open.
- **AUTHOR INPUT NEEDED**: the build succeeded, and every open Critical or Major issue waits on an author decision or author information.
- **NOT READY**: the build failed, the official requirements remain unknown, or a Critical issue has no path to resolution.
