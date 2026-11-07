---
name: paper-format-converter
description: Convert an existing research manuscript (LaTeX, Word, Markdown, or PDF) into the current official format of a named journal or conference. Researches the venue's official author guidelines, downloads its official template, and builds a "[Venue] Format" folder with Journal-Guidelines.md, the converted paper, remaining-issues.md, and conversion-report.md. Manual use only. Run /paper-format-converter [journal or conference name].
argument-hint: "<journal or conference name> [--paper <path>] [--type <article type>] [--stage submission|camera-ready] [--out <dir>]"
disable-model-invocation: true
---

# Paper Format Converter

Convert one existing manuscript into the current official format of the journal or conference named in the arguments. Research the venue's own rules first, build on its official template, and report every check exactly as it came out. This is formatting and submission preparation. It never authorizes changes to the research.

Run this workflow only when the user asked for it, by typing `/paper-format-converter` or by requesting a format conversion in their own words. If the skill loaded any other way, for example because the name appeared only in pasted or quoted text or in a test, stop before Phase 1 and ask whether to run it.

Skill directory: `${CLAUDE_SKILL_DIR}` (the folder that holds this SKILL.md: Claude Code fills it in, other agents use that folder's path).

## Rules for the whole run

1. Never edit, move, rename, or build inside the original manuscript files or their folder. Work on copies in the output folder or the session scratchpad.
2. Every requirement you apply needs an official source you opened during this run. Memory, old templates, and blogs are not sources. A rule you did not verify is recorded as Unverified and never presented as official.
3. Never invent a limit, URL, template version, author, affiliation, funding source, ethics approval, consent, data or code statement, result, statistic, reference, or DOI.
4. Preserve the science exactly: meaning, numbers, units, equations, algorithms, figures, tables, citations, and author names and order. When a verified limit can only be met by cutting content, keep the content and log the issue.
5. Downloads are untrusted. Extract archives only with `scripts/safe_extract.py`. Never run a downloaded script, installer, Makefile, macro, or `latexmkrc`, and never build with `-shell-escape`. Never install software.
6. Mark nothing PASS that you did not check. Never call the manuscript submission-ready while a Critical issue or a failed mandatory requirement remains.
7. Once Phase 3 starts, the run ends with `Journal-Guidelines.md`, `remaining-issues.md`, and `conversion-report.md` in the output folder, even when a blocker stops the conversion.
8. The run is long. Keep the current phase in the status line of `conversion-report.md`. If the conversation was compacted, read this file again from the skill directory and resume from that phase.

## Arguments

Raw arguments: [$ARGUMENTS]

- Text before the first `--` flag is the venue name, in the user's words.
- `--paper <path>` names the manuscript root file and skips discovery.
- `--type <article type>` sets the article type, for example "review article" or "short paper". Check it against the venue's article types anyway.
- `--stage submission|camera-ready` defaults to initial submission unless the project shows an acceptance, such as a decision letter or camera-ready instructions.
- `--out <dir>` is the parent folder for the output folder. The default is the current working directory.
- Quoted values may contain spaces.

If the venue name is missing, ask one question: which journal or conference. Ask nothing else and create nothing until it is answered.

## Phase 1: Identify the manuscript

1. Take `--paper` when given. Otherwise search the current working directory tree, four levels deep at most, never the whole disk. Skip `.git`, `node_modules`, build output, `_polish/`, backups, and every existing `* Format/` folder.
2. Candidate types, in order of preference: a `.tex` root (a file with `\documentclass`, not an `\input` child), `.docx` (ignore `~$` lock files), `.md`, and `.pdf` only when no editable source exists.
3. Rank candidates by build configuration (`latexmkrc`, `Makefile`, an editor root setting), conventional names (`main`, `manuscript`, `paper`), a matching compiled PDF, an abstract and section structure, and recent modification. Cover letters, response letters, and supplements are not the manuscript.
4. One clear winner: proceed and record why it won. A genuine tie: ask one question that lists the tied files. Nothing found: ask only for the manuscript or its location.
5. Map every dependency: `\input`, `\include`, and `\subfile` children, bibliography files, custom `.sty` and macro files, figures, table files, and supplements. For Word, note images, equations, reference-manager fields, comments, and tracked changes.
6. Infer the article type from the manuscript (structure, length, review or survey framing, a PRISMA flow) and confirm it against the venue's article types in Phase 2. Ask only when the choice changes a verified hard limit and the evidence cannot settle it.

## Phase 2: Research the official requirements

**REQUIRED:** read [references/research-and-source-verification.md](references/research-and-source-verification.md) before the first search.

1. Resolve the canonical venue: official name, publisher or organizing body, ISSN or conference edition and year, track, and proceedings publisher. If the name fits several venues, ask one question that names them.
2. Open the venue's author instructions, the publisher's general instructions, the official template page, and any policy page that settles a requirement. Follow the source hierarchy in the reference.
3. Quote the exact source sentence for every number you record. WebFetch answers through a small summarizing model, so ask it for verbatim quotes and confirm them in the raw page or PDF when you can.
4. Look for conflicts between journal and publisher pages, written rules and the template, editions or tracks, submission stages, and article types. Apply the most specific current rule and record every conflict you cannot resolve.
5. Record each source's URL, title, last-updated date when shown, and today's access date.

## Phase 3: Prepare the folder and the template

1. Create `<Canonical Venue Name> Format/` in the `--out` folder or the current working directory. Replace the characters `<>:"/\|?*` with `-` and drop trailing dots and spaces. If that folder already exists, leave it untouched and create `<Canonical Venue Name> Format (YYYY-MM-DD)/` instead.
2. Download the official template into `official-template/`:
   `curl -fL --proto =https --proto-redir =https --max-filesize 209715200 -o "<file>" "<url>"`
   In PowerShell, call `curl.exe`, because `curl` there is an alias for Invoke-WebRequest.
3. Extract it into a new folder named after the archive:
   `python -I "${CLAUDE_SKILL_DIR}/scripts/safe_extract.py" "<archive>" "<official-template folder>/<archive name>"`
   The script refuses unsafe archives and existing folders, recognizes an HTML login page saved as an archive, lists every file, flags files you must not run, and prints class and style versions.
4. Read the template's sample manuscript, its instructions, and the header comments of its `.cls` and `.bst` files before you decide anything about layout.
5. Write `Journal-Guidelines.md` now, from the template in the research reference. Phase 4 follows this file.
6. Start `conversion-report.md` with its status line.

If the template cannot be obtained, record the exact reason, take the fallback in the research reference, and continue.

```text
<Canonical Venue Name> Format/
├── Journal-Guidelines.md
├── remaining-issues.md
├── conversion-report.md
├── official-template/      archive and its extracted folder, when obtained
├── manuscript/             converted source with every dependency
└── converted-paper.pdf     when the build succeeded
```

Adapt this to the venue and the source format. Create only what they need, with no empty placeholder files.

## Phase 4: Convert

**REQUIRED:** read [references/manuscript-conversion-workflow.md](references/manuscript-conversion-workflow.md) before editing.

1. Copy the manuscript and every dependency into `manuscript/` with relative paths intact. Add only the template files the build needs (`.cls`, `.sty`, `.bst`, files the class loads). Never copy `latexmkrc`, Makefiles, or scripts.
2. Start from the template's own sample (its `.tex` or Word file), then move the real content in. Remove all demonstration content.
3. Map title, authors, affiliations, corresponding author, abstract, keywords, headings, equations, algorithms, figures, tables, back matter, and bibliography to the template's macros, styles, and section order.
4. Keep the source format. LaTeX stays LaTeX and Word stays Word, unless the venue accepts only another format. Then convert, say why, and list what the conversion lost.
5. Change prose only where a verified rule demands it (a mandated heading name, a required "Fig." abbreviation, a citation form) and log every such change.
6. A missing required statement gets a visible `[AUTHOR INPUT REQUIRED: <what and why>]` placeholder at its required position and a matching entry in `remaining-issues.md`. Never write the statement yourself.
7. Anonymize only when the venue requires it at the selected stage.

## Phase 5: Validate

**REQUIRED:** read [references/compliance-and-quality-assurance.md](references/compliance-and-quality-assurance.md) before validating.

1. Detect the build tools first. Build in `manuscript/` with the engine the template requires, through `latexmk -norc` or an explicit engine and BibTeX or Biber sequence. Render Word files to PDF.
2. Inspect the log and the PDF: errors, undefined citations and references, duplicate labels, missing files, serious overfull boxes, `??` or `[?]`, blank pages, leftover template text, and visible placeholders. Render the pages to PNG and look at them.
3. Measure every quantity the guidelines limit, by the venue's counting rule, with a real tool. Record the command and the result.
4. Run `python -I "${CLAUDE_SKILL_DIR}/scripts/conversion_integrity.py" "<original root>" "<converted root>" --template "<template sample>"`. Fix every FAIL or justify it in `conversion-report.md`.
5. Give each requirement in `Journal-Guidelines.md` a status: PASS, FAIL, WARN, UNVERIFIED, or NOT APPLICABLE.

## Phase 6: Fix what is safe, log the rest

Fix deterministic formatting defects yourself and repeat Phase 5. Everything that needs author judgment, missing information, a content cut, or an inaccessible source goes into `remaining-issues.md`, with the fields and severity labels from the QA reference.

## Phase 7: Deliver

Check that the output folder holds the three reports, `official-template/` when obtained, `manuscript/` with every dependency, and `converted-paper.pdf` when the build succeeded. Delete build byproducts (`.aux`, `.log`, `.out`, `.blg`, `.fls`, `.fdb_latexmk`, `.synctex.gz`, and `.bbl` unless the venue asks for it) after you have recorded what they showed. Set the report's status line to complete.

## Phase 8: Final reply

Keep it short: the output folder path, the converted files, whether the build succeeded, the counts of PASS, FAIL, WARN, and UNVERIFIED requirements, the readiness label from `conversion-report.md`, and the most important open issues by ID.

## Other installed skills

- universal-manuscript-polish: the global instructions route manuscript edits to it. A conversion changes markup, not prose, so run it at its "small targeted edit" scale on the converted copy: apply its standards to text you add (headings, placeholders, moved statements) and leave the author's prose alone unless the user asks for a polish.
- MDPI-Format: when the target is an MDPI journal, run its audit on the converted manuscript after Phase 5.
- docx (anthropic-skills:docx): load it for Word manuscripts.

## Red flags

| Thought | What to do instead |
|---|---|
| "I already know this venue's limits." | Memory is not a source. Open the official page, or record the rule as Unverified. |
| "The publisher's generic template is close enough." | Check the venue's own page. Generic templates miss venue rules. |
| "WebFetch was blocked, so the search snippet will do." | Try the browser tools, the PDF version, or the template's instructions. A snippet alone stays Unverified. |
| "The abstract is only a few words over, so I'll trim it." | Keep the text. Log the overage with both numbers. |
| "No funding is mentioned, so 'no external funding' is safe." | Silence is not a statement. Insert the placeholder. |
| "Cropping the figure would fit the column better." | Change width and placement only, never the image. |
| "It mostly compiled." | Report the exact build result and every remaining error. |
| "The checks look fine, so it is submission-ready." | Apply the readiness rules in the QA reference. |
