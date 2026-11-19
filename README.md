# Academic Agent Skills

An open collection of AI agent skills for academic research, scientific writing, peer review, and publishing.

[![Validate skills](https://github.com/aliakarma/academic-agent-skills/actions/workflows/validate.yml/badge.svg)](https://github.com/aliakarma/academic-agent-skills/actions/workflows/validate.yml)
[![Agent Skills format](https://img.shields.io/badge/format-Agent%20Skills-blue)](https://agentskills.io/specification)
[![License: CC BY 4.0](https://img.shields.io/badge/license-CC%20BY%204.0-lightgrey)](LICENSE)

## Overview

Academic Agent Skills gives a coding agent (Claude Code, OpenAI Codex, Google Antigravity, Cursor, and other agents
that read the open [Agent Skills](https://agentskills.io/) format) step-by-step procedures for research work that
generic assistants tend to do badly. These include finding a defensible research gap, verifying every reference
against its publisher record, answering reviewers point by point, and auditing a paper or a code repository for claims
the evidence does not support.

The collection is for researchers, graduate students, and research engineers who write in LaTeX or Word and want an
agent that checks its own work. Most skills include scripts that verify the output (a reference checker, a response
letter checker, an audit-report validator) before the agent reports back.

## Objectives

- **Honest output.** No skill fabricates citations, data, results, or test outcomes. Each one says what it did not
  verify, and unmeasured numbers stay marked as targets.
- **Checked work.** Wherever a result can be checked mechanically, a bundled script checks it.
- **One source for every agent.** There is one canonical copy of every skill in [`skills/`](skills/), and the same
  files serve every installer and agent.

## What the skills cover

The collection has **25 skills** in eight groups:

- **Workflow and routing.** One map of how the skills connect, the order to run them in, and what each needs first. Every skill's `Related skills` section points back to it (`research-workflow-map`). The paper cycle runs in 14 steps from a title and abstract to a submitted paper: `finding-gap` → `idea-to-paper` → `literature-review` → `paper-to-project-report` → `project-report-to-github` → `peer-review` → `manuscript-revision` → `nanobanana-prompt-generator` (then Google Flow) → `figure-rebuild` → `audit-paper` + `research-auditor` → `repair-paper` → `universal-manuscript-polish` → `text-humanizer` + `clean-user-facing-text` → `reference-verify` → `journal-cover-letter`.
- **Literature and research gaps.** Logged searches, source ledgers, gap matrices, novelty assessments, and verified BibTeX (`literature-review`, `finding-gap`).
- **Manuscript development.** From an idea to a full LaTeX paper project, staged polishing, conversion to a venue's official template, and a journal-specific submission cover letter (`idea-to-paper`, `universal-manuscript-polish`, `paper-format-converter`, `journal-cover-letter`).
- **Writing quality.** Prose revision, a line-by-line forensic writing audit, and audit-driven repair (`text-humanizer`, `audit-paper`, `repair-paper`, `clean-user-facing-text`).
- **Peer review and revision.** Simulated multi-reviewer review, complete reviewer-driven revision with the requested experiments, response letters with reference checks, and highlighted change PDFs (`peer-review`, `manuscript-revision`, `response-to-reviewer`, `highlighted-pdf-from-reviews`).
- **Research quality assurance.** Pre-submission diagnosis, repository forensics, and reference verification, one entry or a whole `.bib` (`research-auditor`, `repo-forensic-audit`, `reference-verify`).
- **Figures and talks.** NanoBanana prompts that turn TikZ diagrams into reference images, raster figures rebuilt as TikZ, paper-faithful PowerPoint decks, and Simplified Technical English explainers (`nanobanana-prompt-generator`, `figure-rebuild`, `paper-to-pptx`, `asd-ste100`).
- **Research engineering.** Paper to engineering spec to tested code repository, and README upgrades (`paper-to-project-report`, `project-report-to-github`, `readme-improvement`).

## Quick installation

### 1. Vercel Skills CLI (Claude Code, Codex, Antigravity, Cursor, and others)

Requires Node.js. Preview what the repository offers, then install:

```bash
npx skills add aliakarma/academic-agent-skills --list
npx skills add aliakarma/academic-agent-skills --skill '*' --agent claude-code --global --yes
```

Change `--agent` to `codex`, `antigravity`, or `cursor`, or repeat it to target several agents. Omit `--global` to
install into the current project instead. To install selected skills only:

```bash
npx skills add aliakarma/academic-agent-skills --skill literature-review --skill reference-verify --agent codex --global --yes
```

For Antigravity and Cursor, a global install writes the skills only to `~/.agents/skills/`. See
[docs/INSTALLATION.md](docs/INSTALLATION.md#antigravity-and-cursor-global-installs) before you rely on it.

### 2. Native Claude Code plugin

```bash
claude plugin marketplace add aliakarma/academic-agent-skills
claude plugin install academic-agent-skills@academic-agent-skills --scope user
```

Plugin skills are namespaced, for example `/academic-agent-skills:reference-verify`.

### 3. Manual installation

Copy a skill folder from `skills/` into your agent's skills directory, for example
`~/.claude/skills/reference-verify/` for Claude Code or `~/.agents/skills/reference-verify/` for Codex.

[docs/INSTALLATION.md](docs/INSTALLATION.md) covers every method, prerequisites, per-agent paths, updating,
uninstalling, and troubleshooting. Check [docs/PLATFORM_COMPATIBILITY.md](docs/PLATFORM_COMPATIBILITY.md) before
relying on a skill outside Claude Code.

## Skills catalog

<!-- catalog:start -->
| Skill | Description | Category |
|---|---|---|
| [`research-workflow-map`](skills/research-workflow-map/SKILL.md) | Routes work through the 14-step paper cycle, from a title and abstract to the cover letter, and the other-purpose skills: what each skill needs first and which runs next. | Workflow and Routing |
| [`finding-gap`](skills/finding-gap/SKILL.md) | Evidence-grounded research-gap discovery with logged searches and a verified source ledger. Stress-tests a proposed gap and drafts research questions, hypotheses, and methods. | Research Discovery and Literature |
| [`literature-review`](skills/literature-review/SKILL.md) | Read-only, evidence-based review of a manuscript's field written to literature_review.md: logged searches, a verified source ledger, gap validation against counterevidence, and a novelty assessment, checked by a bundled script. Edits the paper only on later request. | Research Discovery and Literature |
| [`idea-to-paper`](skills/idea-to-paper/SKILL.md) | Generates a complete LaTeX paper project (IEEE conference by default) from an idea, abstract, or brief, with TikZ figures, a verified references.bib, and unmeasured results marked as targets. | Manuscript Development |
| [`journal-cover-letter`](skills/journal-cover-letter/SKILL.md) | Writes a one-page submission cover letter for a named journal, grounded in the manuscript and the journal's current author instructions, compiled to LaTeX/PDF and checked by a bundled script. | Manuscript Development |
| [`paper-format-converter`](skills/paper-format-converter/SKILL.md) | Converts a manuscript to a named journal's or conference's current official template and guidelines, with a conversion report and a remaining-issues list. Manual only. | Manuscript Development |
| [`universal-manuscript-polish`](skills/universal-manuscript-polish/SKILL.md) | Staged, verified polishing of a LaTeX or Word manuscript for submission, resubmission, or camera-ready, with scan and edit-verification scripts. | Manuscript Development |
| [`audit-paper`](skills/audit-paper/SKILL.md) | Line-by-line forensic writing audit of a manuscript, written to audit.md without editing the paper, and checked by a bundled script. | Academic Writing Quality |
| [`clean-user-facing-text`](skills/clean-user-facing-text/SKILL.md) | Audits suspicious invisible Unicode and revises reader-facing prose while keeping facts, meaning, voice, code, citations, and quotations unchanged. | Academic Writing Quality |
| [`repair-paper`](skills/repair-paper/SKILL.md) | Revises a manuscript against audit.md and research-auditor's assessment so that every numbered issue and finding is repaired or accounted for. | Academic Writing Quality |
| [`text-humanizer`](skills/text-humanizer/SKILL.md) | Drafts, revises, and critiques academic and professional prose for clarity, specificity, and author voice. Also interprets AI-detection and similarity reports. | Academic Writing Quality |
| [`highlighted-pdf-from-reviews`](skills/highlighted-pdf-from-reviews/SKILL.md) | Builds a highlighted revised-manuscript PDF from a LaTeX paper and its response letter, with each change tagged by reviewer-comment ID and mapped to pages. | Peer Review and Revision |
| [`manuscript-revision`](skills/manuscript-revision/SKILL.md) | Revises a manuscript against every editor and reviewer comment, runs the experiments reviewers request, and writes a matching response letter, with a script that keeps the run going until each comment is addressed or its blocker is stated. | Peer Review and Revision |
| [`peer-review`](skills/peer-review/SKILL.md) | Simulates a three-reviewer Q1 journal peer review with an area-chair meta-review, for whole manuscripts or single sections. | Peer Review and Revision |
| [`response-to-reviewer`](skills/response-to-reviewer/SKILL.md) | Drafts, updates, or verifies a point-by-point response-to-reviewers letter, with scripts that check completeness, page and line references, and numbers. | Peer Review and Revision |
| [`reference-verify`](skills/reference-verify/SKILL.md) | Checks one reference against publisher, DOI, Crossref, arXiv, or issuing-body sources and returns a corrected, paste-ready BibTeX entry. Triages a whole .bib file by script first, with a Colab notebook front end. | Research Quality Assurance |
| [`repo-forensic-audit`](skills/repo-forensic-audit/SKILL.md) | Forensic audit of a research code repository for reproducibility, hard-coded metrics, disconnected evaluation pipelines, and other fabrication fingerprints. | Research Quality Assurance |
| [`research-auditor`](skills/research-auditor/SKILL.md) | Independent pre-submission diagnosis of a research project: its real claims, the research gap checked against the literature, closest prior work, journal fit, and acceptance blockers. | Research Quality Assurance |
| [`asd-ste100`](skills/asd-ste100/SKILL.md) | Builds an interactive offline HTML explainer of a paper, method, or codebase, with visible text written to ASD-STE100 Issue 9 Simplified Technical English rules. Needs your own authorized copy of the specification, which is not included. Manual only. | Figures, Slides and Explainers |
| [`figure-rebuild`](skills/figure-rebuild/SKILL.md) | Rebuilds a raster or AI-generated research figure as LaTeX/TikZ with selectable text and a matched style, plus an editable one-slide PowerPoint twin, and audits the figure's claims against measured results. | Figures, Slides and Explainers |
| [`nanobanana-prompt-generator`](skills/nanobanana-prompt-generator/SKILL.md) | Writes a NanoBanana prompt for every TikZ diagram in a paper, never for results figures, and a step-by-step guide for making reference images in Google Gemini or Flow that figure-rebuild then turns into vector figures. | Figures, Slides and Explainers |
| [`paper-to-pptx`](skills/paper-to-pptx/SKILL.md) | Turns a LaTeX paper into an editable 15-slide PowerPoint talk deck that stays faithful to the paper, with rendered equations and a number-fidelity check. | Figures, Slides and Explainers |
| [`paper-to-project-report`](skills/paper-to-project-report/SKILL.md) | Converts a paper into an implementation-oriented PROJECT_REPORT.md (engineering spec, reproducibility audit, roadmap phases), checked by a bundled script. | Research Engineering and Repositories |
| [`project-report-to-github`](skills/project-report-to-github/SKILL.md) | Builds a runnable, tested, GitHub-ready research code repository from a PROJECT_REPORT.md and the paper's .tex, checked by a bundled script. | Research Engineering and Repositories |
| [`readme-improvement`](skills/readme-improvement/SKILL.md) | Refactors a repository README.md to publication quality without changing the project's technical meaning. | Research Engineering and Repositories |
<!-- catalog:end -->

The [full catalog](docs/SKILLS_CATALOG.md) groups the skills by research workflow and marks which ones are manual only.

## Examples

Most skills start from a plain request. In Claude Code you can also call a skill by name (`/reference-verify`, or
`/academic-agent-skills:reference-verify` when installed as a plugin).

| You ask | Skill that runs | What you get |
|---|---|---|
| "The verifier flagged this reference as DOI not found" plus a BibTeX entry | `reference-verify` | A corrected, paste-ready BibTeX entry, checked against the DOI registry and the publisher page |
| "Check every reference in references.bib" | `reference-verify` | A field-by-field report on the whole file (wrong, disputed, retracted, duplicate, and unfound entries), then a verified entry for each flagged one. Also runs as a [Colab notebook](notebook/BibTeX_DOI_Verifier.ipynb) |
| "Do a literature review for main.tex and check whether my research gap is real" | `literature-review` | `literature_review.md` with a search log, verified source ledger, validated gaps, and a novelty assessment. The manuscript is left unchanged until you ask for integration |
| "Draft the response to reviewers" with the reviews and the revised `.tex` | `response-to-reviewer` | A point-by-point letter whose page, line, and number references are checked by script |
| "Audit the writing of my paper before I edit it" | `audit-paper` | `audit.md` with numbered issues, and the manuscript left unchanged |
| "Is my research gap real, and does my target journal fit?" | `research-auditor` | An evidence-tagged assessment of the claims, the gap, the closest prior work, and journal fit |
| "Write a cover letter for submitting main.tex to IEEE Access" | `journal-cover-letter` | A one-page `cover_letter.tex` and `cover_letter.pdf` grounded in the paper and the journal's current author instructions, checked by script |
| `/paper-format-converter IEEE Transactions on Smart Grid` | `paper-format-converter` | A `[Venue] Format` folder with the official template, the converted paper, and a conversion report |

## Skills that need material you supply

`asd-ste100` writes explanations to the ASD-STE100 Simplified Technical English rules. This repository does not
include the ASD-STE100 specification or any extract from it. Get an authorized copy from ASD through its official
website and point the skill at it. [skills/asd-ste100/REFERENCES.md](skills/asd-ste100/REFERENCES.md) explains how.

`paper-to-pptx` also needs Anthropic's `pptx` skill, which this repository does not include.

## Updating

```bash
npx skills check                      # report available updates without installing
npx skills update                     # Vercel Skills CLI installs
claude plugin marketplace update academic-agent-skills
claude plugin update academic-agent-skills@academic-agent-skills
```

## Uninstalling

```bash
npx skills remove aliakarma/academic-agent-skills --global --yes   # removes only this collection's skills
claude plugin uninstall academic-agent-skills@academic-agent-skills
claude plugin marketplace remove academic-agent-skills
```

Do not uninstall with `npx skills remove --skill '*'`. It removes every installed skill, including skills from other
sources.

## Contributing

Researchers and developers can contribute new skills, fixes, and compatibility reports. Read
[CONTRIBUTING.md](CONTRIBUTING.md), then run the checks locally:

```bash
pip install -r requirements-dev.txt
python scripts/validate_skills.py
python scripts/generate_catalog.py --check
python -m pytest tests
```

[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) explains how one `skills/` folder serves every distribution channel.

## Security

Skills run with the permissions of the agent that loads them. Read a skill's `SKILL.md` and its scripts before you
install it. Report vulnerabilities, leaked secrets, personal data, or content that may not be redistributed through
GitHub's private vulnerability reporting, as described in [SECURITY.md](SECURITY.md).

## License

This project is licensed under the [Creative Commons Attribution 4.0 International license](LICENSE) (CC BY 4.0).
You may share and adapt it, including commercially, if you credit **Academic Agent Skills**, link to this
repository, name the license, and say whether you made changes.

The license covers this project's own material. Third-party material keeps its own license, and the ASD-STE100
specification is not part of this repository. Creative Commons does not recommend its licenses for
software, so read [docs/LICENSE_AND_ATTRIBUTION.md](docs/LICENSE_AND_ATTRIBUTION.md) for how the license applies to
the bundled scripts, attribution examples, and the third-party material.

## Acknowledgments

- The [Agent Skills specification](https://agentskills.io/specification) defines the skill format used here.
- [Vercel Skills CLI](https://github.com/vercel-labs/skills) installs the skills across agents.
- [Claude Code plugins](https://code.claude.com/docs/en/plugins) provide the native plugin and marketplace format.
