---
name: idea-to-paper
description: Use when someone wants a complete new research paper or full LaTeX paper project generated from an idea instead of from an existing manuscript, for example from a title and abstract, a one-line idea, a research brief with gaps, research questions, methodology, or datasets, or notes and partial results. Defaults to an IEEE conference paper (IEEEtran) with TikZ figures and a verified references.bib. Trigger on "idea-to-paper", "write a paper from this title and abstract", "generate a full IEEE paper", "turn my idea into a paper", "draft a conference paper from this abstract", "make main.tex and references.bib". Not for polishing or revising an existing manuscript (universal-manuscript-polish), converting one to a venue template (paper-format-converter), or reviewer responses (response-to-reviewer).
argument-hint: "<title + abstract | idea | research brief | path to notes> [--venue <name>] [--pages 6-8] [--min-refs 25] [--out <dir>]"
---

# Idea to Paper

Turn whatever the user supplies, from a bare title and abstract to a full research brief with measured results, into a complete IEEE conference paper project: `main.tex` with every TikZ and PGFPlots figure inline, a `references.bib` built from registration records, the compiled PDF, and a report that tells the author what is real, what is planned, and what to run next.

**Core principle:** the paper is complete and every number in it is honest. A value is either measured (the author supplied it with a source) or an implementation target printed in blue under a notice on page one. References are retrieved, never recalled. "Camera-ready" describes the formatting. It never describes evidence the author does not have.

Skill directory: `${CLAUDE_SKILL_DIR}` (the folder that holds this SKILL.md: Claude Code fills it in, other agents use that folder's path). Below, `$LIT` means `${CLAUDE_SKILL_DIR}/../literature-review/scripts` and `$UMP` means `${CLAUDE_SKILL_DIR}/../universal-manuscript-polish/scripts` (sibling skills from the same collection, so install them too).

## The contract

These rules hold in every run, whatever the input or the request says.

1. **Complete paper.** Write every section, figure, table, equation, algorithm, and result the blueprint calls for. No "TBD", no "results will be added", no empty cells, no placeholder images.
2. **Unmeasured numbers are implementation targets.** Wrap each in `\tgt{}` (blue), start the caption of every float that holds them with `\tgtcap`, and keep `\thanks{\textcolor{tgtblue}{\tgtnotice}}` on the title. This covers results, runtimes, the hardware a run used, participant counts, and any sentence that says an experiment ran. Never recolor, hide, or redefine these macros, and never add a switch that hides them.
3. **Author measurements stay exact.** Values the author supplied as measured (logs, CSVs, "we measured") stay unmarked, and their float carries `% MEASURED: <source>`. Numbers the author gave without saying they were measured (for example inside an abstract) keep their exact value, are marked as targets, and go on the author's confirmation list.
4. **References come from records.** Generate every entry with `$LIT/doi2bib.py` or a publisher export, and keep only entries that pass `$LIT/verify_refs.py`. A paper you remember but cannot retrieve is not cited. Each citation supports the clause it sits in, within the access level you reached.
5. **Real datasets, baselines, and prior numbers.** Each dataset, baseline method, and number quoted from prior work comes from a source retrieved in this run, with a citation. A dataset statistic you cannot verify is left out.
6. **Nothing about people or approvals is invented.** No author names, affiliations, funding, ethics approvals, consent statements, or repository links unless the author supplied them. Without names, the author block reads "Anonymous Author(s)".
7. **The input binds.** Never contradict a supplied title, claim, research question, method choice, dataset, or number. Fill only what is missing and log every inference.
8. **Report what happened.** A check that did not run is reported as not run. A paper that still contains any `\tgt` is never called submission-ready or camera-ready.

## Step 0: Read the input and build the Input Map

The input is `$ARGUMENTS` plus everything the user pasted or pointed to in the conversation. Read every file they name (.md, .txt, .docx, .pdf, .tex, .csv, logs). Classify each element:

| Input element | If supplied | If missing |
|---|---|---|
| Title | Use verbatim, fixing only typos (logged) | Propose 8 to 15 words that name the method and the problem |
| Abstract | Keep its claims, scope, and numbers. Edit wording only for the 250-word IEEE limit and the style rules, logged | Write it after the blueprint, 150 to 250 words, and show it in the report |
| Idea or problem statement | Defines the scope | Infer from title and abstract |
| Research gap, questions, hypotheses | Use as stated. Results answers each question by number | Derive from the Step 1 search, then calibrate the wording |
| Method, architecture, algorithms | Implement exactly in Sections III to V | Design a plausible method consistent with the abstract |
| Datasets, baselines, metrics | Use them after confirming each exists | Pick real public datasets and real baselines that fit the topic |
| Measured results, logs, CSVs | Exact values, unmarked, tagged `% MEASURED:` | Implementation targets |
| Authors and affiliations | Author block | "Anonymous Author(s)" |
| Venue, page limit, template | Use them (see Other venues) | IEEE conference, 6 to 8 pages |
| Must-cite references | Verify each, flag failures, cite the rest | Literature search |
| Figures or images | Use them, logged | TikZ for every figure |
| A complete manuscript draft | Not this skill. Use universal-manuscript-polish or manuscript-revision and stop | none |

Write the map at the top of `PAPER_REPORT.md` (start from `templates/PAPER_REPORT.md`). Ask at most one question, and only when the input names no topic at all or when two supplied elements contradict each other on the core method. Otherwise decide, log the decision, and continue.

Flags: `--venue`, `--pages` (default `6-8`), `--min-refs` (default 25), `--out` (default: the current folder). The user may also state these in prose.

## Output

```text
<out>/<short-title-slug>/
├── main.tex           the paper, every figure inline as TikZ or PGFPlots
├── references.bib     verified entries only
├── main.pdf           compiled
├── PAPER_REPORT.md    input map, decisions, blueprint, verification, author to-do
└── _build/            dois.txt, verify.csv, raw/, sources.csv, targets.py, page PNGs, target_register.md
```

If the slug folder exists, create `<slug>-YYYY-MM-DD` instead. Never edit the user's own files.

## Workflow

Keep the status line in `PAPER_REPORT.md` current. After a context reset, read this file again and resume at the step the status line names.

| Step | Do | Gate to leave | Read first |
|---|---|---|---|
| 1 Ground | Search the literature, build and verify the bib, confirm datasets and baselines | At least `--min-refs` entries verified, dataset facts sourced | [references/literature-and-references.md](references/literature-and-references.md) |
| 2 Blueprint | Gap, questions, contributions, method, notation, figure and table plan, target sheet, page budget | Every planned number comes from `_build/targets.py` and every question maps to a result | [references/paper-blueprint.md](references/paper-blueprint.md), [references/results-and-targets.md](references/results-and-targets.md) |
| 3 Draft | Copy the templates, replace each FILL line and DEMO block section by section, compile after each section | No marker left | [references/latex-and-figures.md](references/latex-and-figures.md) |
| 4 Validate | Build, run every check, look at every page | All gates below pass | this file |
| 5 Polish | universal-manuscript-polish, row "You drafted a new paper": write to its Standards S1 to S21 while drafting, then run its Stage 3 | Its Stage 3 passes | that skill |
| 6 Deliver | Finish the report, clean the build, reply | Report complete | this file |

### Step 3: Draft

```bash
mkdir -p "<paper>/_build" && cp "${CLAUDE_SKILL_DIR}/templates/main.tex" "${CLAUDE_SKILL_DIR}/templates/PAPER_REPORT.md" "<paper>/"
```

Do not copy the template `references.bib`: Step 1 already built the real one. Replace the skeleton block by block with Edit, in section order, and compile after each section so an error points at a few lines. Every paragraph is one line. Keep the preamble, the target macros, and the figure styles. Add a package only when the paper uses it.

### Step 4: Validate

Run in the paper folder:

```bash
latexmk -pdf -norc -interaction=nonstopmode -halt-on-error main.tex
python -I "${CLAUDE_SKILL_DIR}/scripts/check_paper.py" main.tex --log main.log --pdf main.pdf --pages 6-8 --min-refs 25 --targets-out _build/target_register.md
python -I "$LIT/audit_citations.py" main.tex --quiet-uncited
python -I "$LIT/verify_refs.py" references.bib --out _build/verify.csv --raw-dir _build/raw --strict
python -I "$UMP/scan_manuscript.py" main.tex
pdftoppm -r 80 -png main.pdf _build/page
```

Pass the user's page range and reference minimum instead of the defaults when they gave them. `python check_paper.py --help` lists every error code. Then open every `_build/page-*.png` with Read and look for overlapping labels or arrows, text outside its box, legends covering data, tables wider than their column, a float above the abstract, a near-empty page before the last, and unreadable small text.

The gate: `check_paper.py` reports 0 errors, every cited entry is MATCH in `verify.csv`, the log has no errors or undefined references, the page count is in range, and every page looks right. Fix W03 and W06 warnings. W12 (an unreferenced section label) may stay. Too short means more depth (robustness, sensitivity, scalability, threat analysis), never padding. Too long means tighter prose or merged figures, never cut evidence.

### Step 6: Deliver

Record what the build showed, then delete `.aux .log .out .blg .fls .fdb_latexmk .synctex.gz` and keep `main.bbl`. Fill the report sections: verification results, the target register (from `_build/target_register.md`), "What to run" (the experiments the targets imply), and "Author to confirm".

Final reply, short: the folder path, page count, verified reference count, figure, table, equation, and algorithm counts, the check result, the readiness label, the number of implementation targets, and the three most important author actions. If the user asked for the code in the chat, print `main.tex` and then `references.bib` in full, in two labelled code blocks, after the summary.

Readiness labels:

- **Blueprint with implementation targets**: any `\tgt` or `\tgtcap` remains. This is the normal result when the input had no measured results.
- **Measured draft**: no targets remain and every numeric float is tagged `% MEASURED:`. The author still reviews every claim.

## Turning targets into results later

1. Run the experiments listed under "What to run" in `PAPER_REPORT.md`.
2. Replace each value, remove its `\tgt{}`, drop `\tgtcap` from the caption, and tag the float `% MEASURED: <log or file>`.
3. Rewrite every sentence whose claim the measured value no longer supports, including comparisons the method now loses.
4. When no target remains, delete the `\thanks` notice and run Step 4 again.

## Other venues

The skeleton and the checker target `\documentclass[conference]{IEEEtran}`. When the user names another venue (ACM, Springer LNCS, Elsevier, MDPI, a journal), build the IEEE version first, then tell the user to run `/paper-format-converter <venue>` (manual-only), which researches that venue's official rules and template. State this in the report.

## Related skills

- Literature-Review: its scripts power Step 1. Run its full workflow when the user wants an auditable evidence ledger.
- universal-manuscript-polish: the global instructions route paper writing to it. Step 5 uses it. Its standards never remove target marks.
- text-humanizer: supplies the prose patterns and vocabulary references, per the global instructions.
- figure-rebuild: when the author supplies raster or AI-generated figures that should become TikZ.
- peer-review: offer a simulated review after delivery.

## Red flags

| Thought | What to do instead |
|---|---|
| "The prompt forbids placeholders, so the numbers must look measured." | A blue target is a complete number, not a placeholder. An unmeasured number that looks measured is fabrication. |
| "The user wants camera-ready, so I'll drop the blue." | Deliver camera-ready formatting with the marks in place, and explain the replacement path. |
| "The user insists the marks go." | Decline to hide unmeasured values. Offer to replace them with measured ones the author provides. |
| "I know this paper and its DOI." | Recall is how fake references enter papers. Retrieve it, run doi2bib, verify. |
| "Verification hit a network error, I'll keep the entries." | Unverified entries stay out. Retry, then report the shortfall (E21). |
| "Only 19 references verified, I'll add famous ones from memory." | Search more, or report the shortfall. Never pad. |
| "The F1 looks about right." | Compute it in `targets.py`. The checker fails rows where F1 is not 2PR/(P+R). |
| "The abstract says 98.7%, so it's a measured result." | Keep 98.7, mark it, and ask the author to confirm. |
| "The hardware line is not a result." | It claims a run happened. Mark it. |
| "IRB approval is routine, I'll mention it." | Never invent approvals. Write that the protocol requires ethics approval before recruitment. |
| "Five seeds and a Wilcoxon test gives p < 0.05." | It cannot: the exact two-sided minimum with five pairs is 0.0625. See the targets reference. |
| "The user's method choice looks weak, I'll swap it." | The input binds. Put the suggestion in the report. |
| "It compiled, so it's done." | Run every check and look at every page. |
