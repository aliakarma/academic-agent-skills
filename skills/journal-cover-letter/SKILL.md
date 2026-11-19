---
name: journal-cover-letter
description: Use when the user wants a cover letter, submission letter, or letter to the editor for submitting a research manuscript (.tex, .docx, .pdf, .md, .txt) to a journal, including a new submission after a rejection elsewhere, or wants an existing submission cover letter rewritten or checked. Researches the target journal's current author instructions and scope, writes a journal-specific letter grounded in what the manuscript shows, and produces a compiled, verified one-page LaTeX/PDF pair (cover_letter.tex, cover_letter.pdf). Not for reviewer response or rebuttal letters (use response-to-reviewer).
argument-hint: "<journal name> [--paper <path>] [--type <article type>] [--out <dir>] [--editor <name>]"
---

# Journal Cover Letter

Write one submission cover letter for one manuscript and one target journal. The deliverable is a compiled, checked, one-page `cover_letter.pdf` with its editable `cover_letter.tex`. Drafted text alone is not the deliverable.

A cover letter is the editor's brief for the desk decision. It states what was studied, which gap it closes, what is new, why this journal's readers need it, and any declaration the journal wants in the letter. It is not an abstract, an introduction, or an advertisement.

Skill directory: `${CLAUDE_SKILL_DIR}` (the folder that holds this SKILL.md: Claude Code fills it in, other agents use that folder's path). Stage 5 calls the sibling `text-humanizer` skill from the same collection, so install it too.

## Integrity rules for every stage

1. Every scientific claim traces to a passage, table, or figure in the manuscript. Never invent results, numbers, contributions, capabilities, or implications. Write "first", "novel", or "unique" only when the manuscript makes that claim against named prior work, and then attribute it ("To our knowledge, ...").
2. Every journal requirement comes from an official page opened during this run. Memory, older letters, and the hints in this skill are leads, not sources. Anything not verified is reported as unverified.
3. Every declaration (originality, exclusive submission, author approval, funding, competing interests, ethics, prior or related publications, preprints, permissions) comes from the manuscript, the project files, or the user. Never assume one.
4. Name an editor only after seeing the name on the journal's official editorial-board page during this run. Otherwise write "Dear Editor".
5. Never edit, move, or overwrite the manuscript or an existing cover letter (Stage 8 preserves old letters).
6. Never report a compilation, page count, or visual inspection that did not happen.

## Arguments

Raw arguments: [$ARGUMENTS]

- Text before the first `--` flag is the journal name.
- `--paper <path>` names the manuscript and skips discovery.
- `--type <article type>` sets the article type. Match it to the journal's own category name in Stage 2.
- `--out <dir>` sets the output folder. The default is the folder that holds the manuscript.
- `--editor <name>` names the addressee. Verify it in Stage 2 like any other editor name.

No journal in the arguments or the request: look in the project (template class, README, submission notes, earlier letters). Still none: ask one question, which journal.

## Workflow

Track the ten stages as a to-do list. The run ends at Stage 10, not at the draft.

**Stage 1. Identify the submission.** Use `--paper`, else search the working directory (four levels deep at most). Prefer a `.tex` root containing `\documentclass`, then `.docx`, `.md`, `.txt`, then `.pdf`. Cover letters, response letters, highlights, and supplements are not the manuscript. If two files tie, ask once and list them. Read `.docx` with python-docx or pandoc and `.pdf` with `pdftotext -layout`. Record the exact title, article type, authors, corresponding author (name, affiliation, email), and any declarations, earlier letters, correspondence, or journal instructions in the folder.

**Stage 2. Research the journal.** Follow `references/journal-research-protocol.md`. Write the research record it defines to the session scratchpad, never into the project.

**Stage 3. Analyze the manuscript.** Read the full text, not only the abstract: the introduction and gap, the objectives, the method, the results, the discussion, the conclusion and limitations, and the declarations. Write a fact sheet in the scratchpad. Give each candidate claim a source location and one tag: DEMONSTRATED (shown by the paper's own results), CLAIMED (asserted by the authors), INFERRED (your reading), or UNVERIFIED. Only DEMONSTRATED items and attributed CLAIMED items may enter the letter.

**Stage 4. Build the editorial argument.** Write one sentence each for the problem, the gap, the contribution, the strongest evidence, the journal fit, and the readers who benefit. The fit sentence must engage specific wording from the journal's aims and scope. Match the strength of each verb to the evidence (calibration table in `references/editorial-guidelines.md`).

**Stage 5. Draft, then humanize (mandatory, every run).** Follow `references/editorial-guidelines.md` for the structure, length, tone, article-type adaptations, and declarations. Then invoke the `text-humanizer` skill with the Skill tool on every sentence of the body, the subject line, and any other prose you wrote. Diagnose by its pattern IDs (B01 to B36), revise, and save the pre-humanizer body. Run `python "${CLAUDE_SKILL_DIR}/../text-humanizer/scripts/fidelity_check.py" <before> <after>`, which must print `RESULT: PASS`. Any later text change, including cuts made to fit one page, goes through the same humanizer pass and fidelity check before the final compile. The Stage 10 reply lists the pattern IDs fixed. A letter that skipped this stage is not finished.

**Stage 6. Verify facts.** Check every sentence against the fact sheet and the research record. Cut or rephrase any sentence that fails. List each included declaration with its source.

**Stage 7. Generate LaTeX.** Copy `templates/cover-letter-template.tex`, fill the LETTER DETAILS block, and write the body between the BODY markers. Follow `references/latex-production.md` for escaping, Unicode, fonts, and design limits.

**Stage 8. Save safely.** Write to `--out`, else the manuscript folder. If `cover_letter.tex` or `cover_letter.pdf` already exists there, read it first, because it can hold verified details. Then rename the old pair to `cover_letter_v<N>.tex` and `cover_letter_v<N>.pdf` with the next free N, and tell the user. Never delete it.

**Stage 9. Compile and check.**

```
python "${CLAUDE_SKILL_DIR}/scripts/check_letter.py" "<out>/cover_letter.tex" \
  --require "<exact title>" --require "<journal name>" \
  --require "<corresponding author>" --require "<email>" \
  --png "<scratchpad>/cover_letter_page1.png"   [--paper letter]
```

The script compiles with latexmk and fails the letter on more than one page, a wrong paper size, leftover `[[...]]` placeholders, missing glyphs, lines in the margin, em dashes, semicolons, or a missing required string. It reports the body word count and page fill, renders a PNG, and deletes build files after a pass. Then Read the PNG and walk the visual checklist in `references/quality-control.md`. Fix and rerun until the script prints `RESULT: PASS` and the page looks right. When the text overflows, cut words in the order in `references/editorial-guidelines.md` before touching layout. Exit code 2 means no TeX compiler: deliver the `.tex`, say plainly that the PDF is blocked, and claim nothing about pages.

**Stage 10. Deliver.** Reply in the format in `references/quality-control.md`. Give both file paths, the research summary with source URLs, the contributions emphasized, the QA results, and every item that could not be verified. Keep it short.

## When to ask the user

Ask only for facts that block the letter and are absent from the files. Typical cases are a missing corresponding-author email, a declaration the journal requires in the letter (for example exclusive submission or prior submission history), the journal when none can be found, and the article type when it changes the requirements. Put all questions in one message. Never ask what the files already answer.

## Red flags. Stop and fix.

| Symptom | Fix |
|---|---|
| A sentence that would fit any journal ("well within the scope of your esteemed journal") | Engage a named scope topic and readership from the research record |
| A number or claim you cannot locate in the manuscript | Delete it or restate what the manuscript shows |
| "All authors approved", "not under consideration elsewhere", "no competing interests" with no source | Ask the user, or omit it if the journal does not require it in the letter |
| An editor name not seen on the official site during this run | "Dear Editor" |
| The letter reads like the abstract | Rebuild from the Stage 4 argument |
| "It compiled" without `RESULT: PASS`, or "it looks fine" without reading the PNG | Run the script and read the render |

## Files

| File | Use |
|---|---|
| `references/journal-research-protocol.md` | Stage 2: sources, checklist, research record, publisher entry points |
| `references/editorial-guidelines.md` | Stages 4 to 6: structure, length, language, article types, declarations, shortening order |
| `references/latex-production.md` | Stage 7: template fields, escaping, fonts, layout limits, manual compile |
| `references/quality-control.md` | Stages 9 and 10: script checks, visual checklist, final reply format |
| `templates/cover-letter-template.tex` | Stage 7: the letter design |
| `scripts/check_letter.py` | Stage 9: compile and check. `--selftest` proves the checks fire |
| `evals/test-cases.md` | Scenarios for re-testing the skill after edits |

## Related skills


Run order and the full map: `research-workflow-map`. Invoke these with the Skill tool. If one is not installed, say so and continue with this skill's own steps.

- **Paper cycle:** step 14 of 14, the last step.
- **Needs first:** the final paper with verified references (steps 1 to 13) and the target journal. `research-auditor` gives journal fit, and `paper-format-converter` handles a different journal template.
- **Uses during the run:** `text-humanizer` (required, Stage 5).
- **Hands on to:** submission. Revision letters belong to `response-to-reviewer`.
