---
name: asd-ste100
description: ASD-STE100 Visual Research Explainer. Turns a research paper, concept, project, AI or software architecture, algorithm, equations, source code, or method comparison into an interactive offline HTML learning site. Visible text follows ASD-STE100 Issue 9 rules adapted for teaching, and every claim traces to the source. Manual only. Run /asd-ste100 <what to explain>.
argument-hint: "<what to explain, and the source file if it is not obvious>"
disable-model-invocation: true
user-invocable: true
---

# ASD-STE100 Visual Research Explainer

Complex research in. Clear explanations, meaningful visuals, and an interactive learning website out.

This skill explains technical material in simplified English based on ASD-STE100 Issue 9 and builds an offline website whose visuals show the real structure of the material. Accuracy comes first, clarity second, design third.

**Request:** $ARGUMENTS

Run this workflow only when the user typed `/asd-ste100` or asked in their own words for an ASD-STE100 visual explanation. If the skill loaded any other way, for example because its name appeared only in pasted text, ask before you build anything. If the request is empty, inspect the working directory and explain its primary source document when there is exactly one.

## Skill files

All paths start at `${CLAUDE_SKILL_DIR}` (the folder that holds this SKILL.md: Claude Code fills it in, other agents use that folder's path).

**Setup.** This skill does not include the ASD-STE100 specification or any reference guide made from it. Get your own authorized copy of ASD-STE100 Issue 9 from ASD, the publisher, through its official website (www.asd-ste100.org), and follow ASD's current terms. Then tell the skill where the copy is: save it as `references/ASD-STE100_ISSUE9.pdf`, set the environment variable `ASD_STE100_PDF` to its path, or pass `--pdf <path>` to `ste_tool.py`. Never commit the PDF, or notes copied from it, to a public repository. Details: [REFERENCES.md](REFERENCES.md). If the PDF is not available, tell the user that `ste_tool.py` cannot run, and check the text by hand against the rules below.

| File | When to read it |
|---|---|
| `references/STE-ISSUE9-REFERENCE-GUIDE.md` | Optional and user-supplied: a rule index that you keep yourself. If it exists, read it on every run before you write text. If it does not exist, read the rule pages of the standard where a step names the guide. |
| `references/EXPLANATION-MODES.md` | Step 3. Section blueprints and STE headings for each type of material. |
| `templates/WEBSITE-DESIGN-GUIDELINES.md` | Steps 5 and 6. Design system, diagram and math rules, browser checks. |
| `templates/starter/` | Step 6. Copy it: tested `index.html`, `styles.css`, `app.js`, and `_qa/ste-terms.tsv`. |
| `scripts/ste_tool.py` | `lookup <word>` while you write, `check <page>` in step 7. |
| `scripts/validate_html.py` | Step 7. |
| `references/ASD-STE100_ISSUE9.pdf` (or the path in `ASD_STE100_PDF`) | User-supplied. Read only the pages that a step needs. Never read it whole. Never copy it or its text into an output. |

## Rules that override everything else

1. Explain only what the source says. Never invent a fact, citation, result, number, equation, component, dataset, baseline, or conclusion.
2. Keep the strength of each claim. "Suggests" stays a suggestion, "will test" stays planned work, and an uncertain finding stays uncertain.
3. Separate the claims of the authors from your interpretation. Your analysis goes in a "Not from the source" callout.
4. When the source does not give a detail, write "The source does not give this information." Do not fill the gap.
5. Charts use only values from the source. A worked example with values that you chose says that they are example values.
6. Give a source reference for each important claim, number, equation, and figure: section, page, figure, table, or equation number.
7. Keep technical terms and notation exact. Simplify the explanation around a term, never the term.
8. Never call a page "ASD-STE100 compliant" or "certified", and never present STE as a teaching method. The page can say that its text "was written with ASD-STE100 Issue 9 rules". Stronger wording needs the strict review below.
9. Never copy the ASD-STE100 PDF, a reference guide made from it, or long passages of the standard into a website or a shared file. The standard carries ASD's copyright notice. Check ASD's current terms before you reuse any of its text.
10. Never modify the source files or code of the user. Work in the output folder and the scratchpad.

## Workflow

Do every step. Do not stop after a plan or an outline.

### 1. Identify the source and the task

- Read the request. Find the source in the working directory: papers (.pdf, .tex, .docx, .md), code, notes. Use the one that the request names. If several match, choose by the request. Ask only when an essential detail cannot be found.
- Without a source document (for example "explain RAG"), explain from general knowledge, say so on the page, and cite only sources that you opened in this run.

### 2. Read the source completely and build a source map

- Read all of it: abstract, every section, equations, figures, tables, appendices, and captions. For a PDF, extract the text with page markers (`pdftotext -layout` or PyMuPDF) and look at figure pages as images. For LaTeX, read the `.tex` file and the files that it includes. For code, map the files, entry points, and call order.
- Write `_qa/source-map.md` in the output folder: one line for each claim, number, equation, component, dataset, baseline, metric, result, limitation, and future-work item, with its location. Mark each item as measured, done, planned, or assumed, as the source says. List the information that the source does not give.
- Decide the status of the work. Measured results get a results section. A proposal or concept paper gets no results section and no results chart.

### 3. Plan

- Choose the mode, or modes, in `references/EXPLANATION-MODES.md`. Keep only the sections that the source supports.
- Plan one visual for each idea that has structure (table in step 5).
- Start the terminology register: the starter copy of `_qa/ste-terms.tsv`. Add every technical noun and verb of the source with its Rule 1.5 or Rule 1.12 category. Use one term for each concept (Rule 1.11).

### 4. Write the text with the STE writing engine

All visible text follows this engine: headings, paragraphs, captions, diagram labels, glossary entries, tooltips, buttons, navigation, table text, and math explanations.

| Text | Rules |
|---|---|
| Explanations, captions, figure notes, glossary definitions, panel text | Descriptive writing (Section 6). A maximum of 25 words in a sentence, one topic for each sentence, a maximum of six sentences in a paragraph, a topic sentence first, no imperative. |
| Buttons, navigation, steps that tell the reader what to do | Procedural writing (Section 5). Imperative, a maximum of 20 words, one instruction in each sentence, a condition first and then a comma. |
| Headings, labels, table headers | Short noun phrases with approved words or technical nouns. A heading counts as one word (Rule 8.6). |
| Math, code, symbols, units, proper names, titles, verbatim quotes, references | Outside vocabulary control. Keep them exact. Put them in MathML, `<code>`, `<blockquote>`, `<q>`, or an element with `data-ste="skip"`. |

Sentence rules:

- Only the simple present, simple past, and simple future. No "has shown", no "is computing". The past participle as an adjective is correct: "the trained model".
- Active voice. Use the passive only in descriptive text when the agent is not known (Rule 3.6). If you know who or what does the action, make it the subject.
- Verbs for actions: "the monitor examines the action", not "the monitor performs an examination".
- "-ing" words only as technical nouns or parts of them ("reinforcement learning", "training data").
- No semicolons, contractions, omitted articles, or Latin abbreviations. Write "for example", not "e.g.". Use "that" after "show", "make sure", and "recommend". No gendered pronouns.
- Multi-word nouns of three words or fewer. Write a longer official name once in full, then its abbreviation.
- Not an STE rule: when the user supplies a house style (for example, no em dashes), apply it too.

Words:

- Use approved words with their approved meaning and part of speech. When you are not sure, run `python "${CLAUDE_SKILL_DIR}/scripts/ste_tool.py" lookup <word>`. The dictionary has traps: "explain" is not approved, AGENT means a material, POINT means a sharp end.
- When a word is not approved, try the alternative from the dictionary. If it changes the meaning, use a different sentence construction (Rule 9.1). Never accept a replacement that changes the science.
- The technical nouns and verbs of the source stay. Declare each one in `_qa/ste-terms.tsv` and give the important ones a glossary entry. Declare a word only when it has a technical meaning in the subject field. Rewrite general words.
- Many research words are not approved. "Action", "state", "evidence", and "probability" are technical nouns only in their technical sense. "Say", "claim", "actual", "still", "need", "comparison", and "test" as a verb need a rewrite. Run `ste_tool.py lookup` on each word to see its alternatives.
- Wrap cited names such as "Smith et al." in `<cite>` (Rule GR-6 does not apply to quoted names). Wrap labels and phrases copied from the source in `<q>` or `data-ste="skip"`.
- The checker accepts numbers, units, and colors (Rule 1.5, categories 9 and 17), CamelCase names, and approved multi-word entries such as AWAY FROM without a declaration.

Technical term protocol: introduce the exact term, give its meaning in approved words, add an example when it helps, then use the same term every time. Mark the first use with `<dfn>` and link later uses to the glossary with `<a class="term-ref">`.

Example. Source wording: "Epistemic uncertainty describes uncertainty that comes from a lack of knowledge or incomplete information." In STE, "describe", "lack", and "incomplete" are not approved, "knowledge" is not in the dictionary, and COME means "to move to your location". Write:

> **Epistemic uncertainty** is uncertainty that occurs because the available information is not sufficient. For example, if a traffic model has data for only 3 winter days, its epistemic uncertainty about winter traffic is high. More winter data can decrease this uncertainty.

With "uncertainty", "model", "traffic", "winter", and "day" in the register, `ste_tool.py check` gives 0 errors for this text. The term stays exact, and the meaning stays the same.

Two levels: put the simple explanation first and the technical explanation in `details.technical`. The technical text keeps the full scientific meaning, notation, and references.

### 5. Build the visuals

| Content | Visual |
|---|---|
| Agentic systems, multi-agent frameworks, software and data architectures, digital twins, RAG pipelines | Interactive architecture diagram |
| Algorithms, workflows, decisions, training and data pipelines, experimental procedures | Flowchart or `ol.steps` |
| Theories, abstract concepts, relations between variables, research gaps | Concept diagram |
| Equations, objectives, reward functions, distributions | Equation block with a symbols table and a worked example |
| Experimental results, comparisons, ablations | Data table with value bars, or an SVG chart of source values |
| Development history, multi-stage processes | Timeline |

Every important visual has a title, readable labels, a short explanation, an accessible description, and its source. The figure note of a redrawn structure is in STE too, for example: "This diagram shows the structure of Section 3 of the source. It is not a copy of a figure of the source." The rules and SVG patterns are in sections 5 to 7 of `templates/WEBSITE-DESIGN-GUIDELINES.md`.

### 6. Build the website

- Output folder: `./explanations/<topic-slug>/` in the working directory, unless the user names another place. If the folder exists, do not overwrite it. Use `<topic-slug>-2` (or the next free number) unless the user asked to update that site.
- Copy `templates/starter/` into the folder. Fill every `{{...}}` slot. Delete the unused components and the starter comment block. Keep `app.js` as it is.
- Make one self-contained `index.html` (inline CSS and JS) only when the user asks for one file.
- No network requests and no new packages. The page must open from `file://`.

### 7. Verify

Run the two checks and fix every error. Repeat until they pass.

```bash
python "${CLAUDE_SKILL_DIR}/scripts/validate_html.py" "explanations/<slug>/index.html"
python "${CLAUDE_SKILL_DIR}/scripts/ste_tool.py" check "explanations/<slug>/index.html"
```

- `validate_html.py` checks structure, ids, links, local files, offline use, accessibility basics, leftover slots, and JavaScript syntax.
- `ste_tool.py check` reports semicolons, sentence and paragraph length, contractions, passive voice with a known agent, perfect tenses, Latin abbreviations, gendered pronouns, not-approved words with their alternatives, and a review list of unknown words. Decide each review item: replace the word, or declare a real technical term in `_qa/ste-terms.tsv`.
- Content review against `_qa/source-map.md`: every number, equation, claim, reference, and component. Planned work stays planned.
- Browser check: section 10 of the design guidelines, with `playwright-cli` or a browser tool when one is available. Look at screenshots of the two themes at 1280 px and 375 px.

Report only the checks that you ran.

### 8. Report to the user

1. The exact path of `index.html`.
2. The mode, the sections, and the visuals.
3. Source coverage: what the page explains, and what the source does not give.
4. STE status: the error count of the last check, the number of declared terms, and each review item that you kept, with its cause.
5. Validation and browser results, and each check that you could not do.

## Strict mode (formal compliance review)

Use it only when the user asks for formal ASD-STE100 compliance, a compliance review, or strict STE. Follow the compliance procedure of your reference guide if you have one, otherwise the rules of the standard itself, and write `_qa/STE-COMPLIANCE.md`. Say "checked against ASD-STE100 Issue 9 within the stated scope" only when no item is unresolved. Never write "certified".

## Common mistakes

| Mistake | Correct action |
|---|---|
| A results section for a proposal or concept paper | Planned work in the future tense, and a gap callout: "The source does not give results." |
| A chart with values that "look right" | Only source values. No source values, no chart. |
| An approved word in place of a technical term | Keep the term. "Statistically significant" never becomes "important". |
| "This page is STE compliant" | "The text was written with ASD-STE100 Issue 9 rules." |
| A diagram node that the source does not name | Remove it, or say in the figure note that the figure simplifies the source. |
| Starter components left empty | Delete them. |
| A check reported as passed without a run | Run it, or say that you did not run it. |
