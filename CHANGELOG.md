# Changelog

All notable changes to this project are recorded here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project uses
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

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

- `scripts/validate_skills.py` includes `.ipynb` files in the privacy scan.
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
