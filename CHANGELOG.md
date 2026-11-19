# Changelog

All notable changes to this project are recorded here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project uses
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Removed

- `awesome-design`: the vendored third-party DESIGN.md library (VoltAgent, MIT) and its "General-Purpose
  Utilities" catalog category. The collection now holds only this project's own skills.

### Added

- `research-workflow-map`: one routing skill that holds the run order of all skills (a 14-step paper cycle from a
  title and abstract to the cover letter, plus seven other-purpose skills), what each skill needs first, and which
  skill to run next. Every skill now ends with a `Related skills` section that names its step in the cycle, the
  skills it needs first, uses during the run, and hands on to, and points back to the map. `tests/test_skill_links.py`
  checks that every named skill exists and that the map covers every skill.
- `journal-cover-letter`: writes a one-page submission cover letter for a named journal. It researches the
  journal's current author instructions and scope on official pages, grounds every claim and declaration in the
  manuscript or the user, runs the letter through `text-humanizer`, and fills a LaTeX template.
  `scripts/check_letter.py` compiles the letter and fails it on more than one page, leftover placeholders, missing
  glyphs, em dashes, semicolons, or missing required text. `--selftest` proves the checks fire.
- `nanobanana-prompt-generator`: writes a NanoBanana prompt for every TikZ diagram in `figures/tikz/` or the
  manuscript and a step-by-step `GUIDE.md` for generating reference images in Google Gemini or Google Flow for
  `figure-rebuild`. Results figures never get a prompt: `scripts/find_tikz.py` excludes plot code outright and
  flags results captions and values for review. Tested by `tests/test_find_tikz.py`.
- `manuscript-revision`: revises a manuscript against every editor and reviewer comment, runs the experiments
  the reviewers request, and hands the letter to `response-to-reviewer`. `scripts/check_audit.py` keeps the run going
  until each comment in `revision_audit.md` is ADDRESSED with evidence, or BLOCKED with a stated need from the
  authors. Tested by `tests/test_check_audit.py`.
- `reference-verify` whole-file mode: `scripts/verify_bib.py` checks every field of every entry in a `.bib`
  against CrossRef, DataCite, OpenAlex, Europe PMC, DBLP, OpenLibrary, arXiv, DOI content negotiation, and
  publisher BibTeX pages (PMLR, ACL Anthology). It flags retracted works and duplicate entries, writes Markdown
  and CSV reports, and exits 1 when an entry needs attention. It is report-only unless `--apply` is given.
  `--apply` edits only the corrected values in place and keeps a `.orig.bak` backup. A record found by title
  alone must share an author surname with the entry before it can supply values. When any registry or search
  service is unreachable, the entry gets formatting fixes only.
- `notebook/BibTeX_DOI_Verifier.ipynb`: a Colab and Jupyter front end for `verify_bib.py`.
- `tests/test_verify_bib.py`: offline tests for the verifier's decision rules, write-back, and command line, and a
  check that the notebook is committed without outputs.

### Changed

- License: the project moves from CC BY 4.0 to the MIT License (`LICENSE`, plugin manifest, README, contributing
  guide, and `docs/LICENSE_AND_ATTRIBUTION.md`). Copies obtained under release 1.0.0 keep CC BY 4.0.
- `literature-review` is now a read-only discovery and validation phase. It writes `literature_review.md` (17
  sections from the bundled brief, `references/prompt.md`) and leaves the manuscript, bib, code, and data
  untouched. Integration into the paper is a separate step on explicit request. New scripts: `search.py` (logged
  OpenAlex, Crossref, and arXiv queries and snowballing), `seed_ledger.py` (builds `source_ledger.csv` and measures
  the open-access and closed-access venue split), `render_references.py` (generates the reference sections), and
  `check_review.py` (validates the review against the ledger and search log). New `references/review-template.md`.
- Run order: the skills follow one 14-step paper cycle. `finding-gap` is the entry point and takes a title and
  abstract; `idea-to-paper` writes the paper inside the validated gap; `literature-review` (with its integration
  stage) cites the verified literature. Seven skills sit outside the cycle for other purposes.
- `research-auditor` numbers every weakness finding `R-001` onward. `repair-paper` takes its
  `MASTER_PAPER_ASSESSMENT.md` beside `audit.md` and accounts for every I- and R- ID. `check_report.py` accepts the
  assessment as an optional third argument, and its `--selftest` covers it.
- `figure-rebuild` ships every rebuilt figure with an editable one-slide PowerPoint twin (Phase 8):
  `assets/figure_pptx_template.js` transcribes the TikZ figure into native shapes and real text with pptxgenjs, and
  `scripts/render_pptx.py` renders the slide for viewing (PowerPoint over COM on Windows, LibreOffice elsewhere).
- `README.md` rewritten for beginners around the paper cycle: what a skill is, the 14 steps with what each takes
  and returns, the seven other-purpose skills, a quick start, a glossary, and the repository layout. Four diagrams
  in `docs/images/` illustrate the cycle, step 8, the other-purpose skills, and how to read a skill. All install,
  update, and uninstall commands are unchanged.
- `scripts/validate_skills.py` includes `.ipynb` files in the privacy scan and skips the local, git-ignored
  `presentation/` folder.
- `requirements-dev.txt` adds `bibtexparser` 1.x and `requests` for the new tests.

## [1.0.0] - 2026-11-07

First public release.

### Added

- 22 skills for academic research and publishing in one canonical `skills/` directory, installable with the Vercel
  Skills CLI (Claude Code, Codex, Antigravity, Cursor, and other agents) and as a Claude Code plugin.
- Claude Code plugin manifest (`.claude-plugin/plugin.json`) and marketplace (`.claude-plugin/marketplace.json`)
  that ship every skill as one plugin, `academic-agent-skills`.
- License: Creative Commons Attribution 4.0 International (`LICENSE`), with
  `docs/LICENSE_AND_ATTRIBUTION.md` on scope, attribution, the bundled scripts, and third-party material.
- `scripts/validate_skills.py`: Agent Skills specification checks, portability rules, manifest checks,
  documentation link checks, and privacy rules for public files (personal paths, e-mail addresses, undeclared
  document binaries, and an optional local denylist).
- `scripts/generate_catalog.py`: generates `docs/SKILLS_CATALOG.md` and the README catalog table, with a `--check`
  mode for CI.
- `tests/test_skill_structure.py`, `tests/test_public_release.py`, and the `Validate` GitHub Actions workflow.
- Documentation: README, installation guide, skills catalog, platform compatibility matrix, architecture, skills
  audit, public release privacy audit, license and attribution notes, contributing guide, and security policy.
- `asd-ste100/REFERENCES.md`: how to supply an authorized copy of the ASD-STE100 specification.
- `highlighted-pdf-from-reviews/examples/example_build.py` with a synthetic `examples/demo/` project.

### Changed

- Moved every skill from the repository root to `skills/<name>/`.
- `literature-review`: `name` changed from `Literature-Review` to `literature-review` to meet the specification and
  match its folder. In Claude Code the skill is now invoked as `/literature-review`.
- `figure-rebuild`: description shortened to fit the 1,024-character limit. The full trigger list moved to a
  "Trigger phrases" section.
- `awesome-design`: `metadata.sources` (a list) became `metadata.source` (a string), and the specification count is
  stated as 54.
- Ten skills now call their scripts through `${CLAUDE_SKILL_DIR}` instead of `~/.claude/skills/<name>`, so they work
  from a plugin, a project install, or another agent's skills directory.
- `idea-to-paper` now finds the `literature-review` scripts on case-sensitive file systems.
- `finding-gap` asks for the user's own portfolio URL instead of fetching a fixed one.
- `asd-ste100` uses the user's own copy of the ASD-STE100 specification, found through `references/`, the
  `ASD_STE100_PDF` environment variable, or `--pdf`. Its optional reference guide has fallbacks.
- Punctuation rules (no em dashes, no semicolons) are now applied only when the user supplies them.
  `universal-manuscript-polish` defaults to the STANDARD punctuation policy, and the `paper-to-project-report` and
  `project-report-to-github` checkers run their punctuation check only with the new `--style` option.
- `audit-paper` and `research-auditor` descriptions now separate writing audits from research-substance audits.
- Personal file paths, project names, and names taken from private work were replaced with placeholders and
  neutral labels in examples, evaluation records, and self-tests.

### Not included

- The ASD-STE100 specification and any reference guide made from it. Users supply an authorized copy.
