# Skills Audit

Audit of the skill collection prepared for release 1.0.0, dated 2026-11-07. It records what was checked, what was
changed to make the skills portable and publishable, and what is still open.

Method: a full file inventory, YAML parsing of every `SKILL.md`, a reading of each `SKILL.md` and of the reference
files relevant to each finding, pattern scans of every public file (paths, secrets, personal data, tool names,
imports, risky calls), `scripts/validate_skills.py`, `claude plugin validate`, and discovery and install tests with
the Vercel Skills CLI. The specifications were checked against their official pages on the same date:
[Agent Skills](https://agentskills.io/specification), [Vercel Skills CLI](https://github.com/vercel-labs/skills),
and [Claude Code plugins](https://code.claude.com/docs/en/plugins).

Depth: every `SKILL.md` frontmatter was parsed and every body was scanned. Long reference prompts (for example
`audit-paper/references/prompt.md`, 40 KB) were scanned for the patterns above, not proofread line by line.

## 1. Inventory

**22 skills** and 363 published files under `skills/`. Generated cache folders (`__pycache__`, `.mypy_cache`,
`.ruff_cache`) are excluded by `.gitignore`.

| Skill | Purpose | Files | Scripts | SKILL.md lines | Frontmatter beyond name and description |
|---|---|---|---|---|---|
| asd-ste100 | Offline HTML explainer in ASD-STE100 Simplified Technical English | 10 | 2 | 167 | argument-hint, disable-model-invocation, user-invocable |
| audit-paper | Line-by-line forensic writing audit to `audit.md` | 3 | 1 | 71 | none |
| awesome-design | 54 DESIGN.md design-system specs and a preview library (from VoltAgent, MIT) | 227 | 1 | 140 | license, metadata |
| clean-user-facing-text | Invisible-Unicode audit and prose finalization | 10 | 5 | 191 | none |
| figure-rebuild | Raster figure to LaTeX/TikZ with selectable text and claim audit | 5 | 2 | 260 | none |
| finding-gap | Evidence-grounded research-gap discovery with a source ledger | 7 | 1 | 139 | none |
| highlighted-pdf-from-reviews | Highlighted revised manuscript keyed to reviewer-comment IDs | 8 | 2 | 71 | none |
| idea-to-paper | Full LaTeX paper project from an idea or abstract | 10 | 1 | 148 | argument-hint |
| literature-review | Literature base built, extended, or repaired and integrated | 14 | 7 | 193 | none |
| paper-format-converter | Manuscript converted to a venue's official template | 8 | 2 | 137 | argument-hint, disable-model-invocation |
| paper-to-pptx | Paper-faithful 15-slide PowerPoint deck | 7 | 3 | 90 | none |
| paper-to-project-report | Paper to engineering spec `PROJECT_REPORT.md` | 5 | 1 | 53 | none |
| peer-review | Simulated three-reviewer journal review with meta-review | 3 | 0 | 340 | none |
| project-report-to-github | Tested research repository built from a project report | 4 | 1 | 61 | none |
| readme-improvement | README.md upgraded without changing technical meaning | 1 | 0 | 304 | none |
| reference-verify | One reference verified and returned as corrected BibTeX | 4 | 2 | 92 | none |
| repair-paper | Manuscript revised against an existing `audit.md` | 4 | 2 | 59 | none |
| repo-forensic-audit | Research-repository integrity and reproducibility audit | 5 | 0 | 212 | none |
| research-auditor | Pre-submission diagnosis of claims, gap, prior work, journal fit | 5 | 0 | 140 | none |
| response-to-reviewer | Point-by-point response letter with checking scripts | 8 | 5 | 89 | none |
| text-humanizer | Academic and professional prose revision and critique | 12 | 1 | 164 | none |
| universal-manuscript-polish | Staged, verified manuscript polishing | 3 | 2 | 451 | none |

"Scripts" counts `.py`, `.js`, `.ps1`, and `.sh` files in a skill's `scripts/` folder.

## 2. Original structure

All skills first sat directly in the repository root (`<skill>/SKILL.md`). There was no README, license, manifest,
test, or CI file. Each skill folder followed the Agent Skills layout (`SKILL.md` plus `scripts/`, `references/`,
`templates/`, `assets/`, `examples/`, `evals/`, `tests/`). `awesome-design` also keeps the files of its upstream
repository (`README.md`, `LICENSE`, `CONTRIBUTING.md`, `.gitignore`, `.github/`, `agents/openai.yaml`). They are
inert inside a skill folder and were kept.

## 3. Metadata validation

| Skill | Finding | Rule | Status |
|---|---|---|---|
| literature-review | `name: Literature-Review` was not lowercase and did not match the folder | name format, name = folder | Fixed |
| figure-rebuild | Description was 1,248 characters | description at most 1,024 | Fixed. Trigger list moved to the body |
| awesome-design | `metadata.sources` was a list | metadata maps strings to strings | Fixed. Now `metadata.source` |
| 10 skills | Hard-coded `~/.claude/skills/...` paths | repository portability rule | Fixed (Section 4) |
| asd-ste100, idea-to-paper, paper-format-converter | Claude Code fields `argument-hint`, `disable-model-invocation`, `user-invocable` | `skills-ref` rejects unexpected fields | Kept on purpose. Reported as warnings |

Other checks passed: every skill folder has a `SKILL.md`, all frontmatter parses as YAML, all 22 names are unique and
match their folders, every description is between 40 and 1,024 characters, no `SKILL.md` exceeds 500 lines, no file
or folder is empty, and every resource that a `SKILL.md` names exists.

## 4. Portability findings

1. **Hard-coded install paths (fixed).** Ten skills called their scripts through `~/.claude/skills/<name>/scripts/`,
   which is wrong for a plugin install, for Codex, and for every project install. They now use
   `${CLAUDE_SKILL_DIR}/scripts/` and say how other agents should read it.
2. **Wrong-case sibling path (fixed).** `idea-to-paper` pointed at `Literature-Review/scripts`. The folder is
   `literature-review`.
3. **Cross-skill dependencies.** `idea-to-paper` needs `literature-review` and `universal-manuscript-polish`.
   `repair-paper` needs `universal-manuscript-polish`. `audit-paper` optionally reads `text-humanizer`. Documented in
   INSTALLATION.md.
4. **External skill dependency.** `paper-to-pptx` requires Anthropic's `pptx` skill (`PPTX_SKILL_DIR`), which is not
   part of this repository.
5. **Claude connector tools.** `finding-gap` prefers the Consensus and Scholar Gateway MCP connectors and falls back
   to web search.
6. **Windows-only step.** `paper-to-pptx` exports PDF through PowerPoint (`export_pdf.ps1`). It needs adaptation on
   macOS and Linux.
7. **Claude-only substitutions.** `$ARGUMENTS` in asd-ste100, idea-to-paper, and paper-format-converter.
8. **User-supplied standard.** `asd-ste100` reads the ASD-STE100 specification from a copy the user supplies (a
   path in the skill folder, `ASD_STE100_PDF`, or `--pdf`). See [skills/asd-ste100/REFERENCES.md](../skills/asd-ste100/REFERENCES.md).
9. **Style defaults (fixed).** Several skills applied one author's punctuation rules (no em dashes, no semicolons)
   to every user. They now apply such rules only when the user supplies them. `universal-manuscript-polish` defaults
   to the STANDARD punctuation policy. The `paper-to-project-report` and `project-report-to-github` checkers run the
   punctuation check only with `--style`. `idea-to-paper`'s checker still reports em dashes and semicolons in
   generated papers (E14, E15) as its own house style.
10. **Line endings.** Two `SKILL.md` files use CRLF (awesome-design, clean-user-facing-text). Both loaders accept
    them. Kept as found.

Per-agent status is in [PLATFORM_COMPATIBILITY.md](PLATFORM_COMPATIBILITY.md).

## 5. Overlapping triggers

| Request | Skills | Status |
|---|---|---|
| "audit my paper" | audit-paper, research-auditor | Fixed. `audit-paper` covers the writing, `research-auditor` the research substance (claims, gap, prior work, journal fit). Each description names the other as the alternative, and neither lists the bare phrase as its own trigger |
| Rebuttal or reviewer response letter | peer-review, response-to-reviewer | Open. peer-review's description includes "help preparing a rebuttal or reviewer response letter" |
| Research gap analysis, gap matrix | finding-gap, literature-review | Open. Both build gap matrices |
| Prose humanizing | text-humanizer, clean-user-facing-text | Open. Overlapping rewrite scope |

**Skills named but not included.** Descriptions route to `bibtex-validator`, `manuscript-revision`, `humanize-latex`,
`MDPI-Format`, and `anthropic-skills:pptx`, which are not in this repository. Only `paper-to-pptx` depends on one.
The others are "use X instead" hints.

**Content claims.** `awesome-design/SKILL.md` claimed "55+" specifications. The folder holds 54, and the text now
says 54.

## 6. Changes made to skill content

None of these changes alters what a skill does, except where the Reason column says so.

| File | Change | Reason |
|---|---|---|
| all skill folders | Moved from the root to `skills/<name>/` | Canonical layout for both installers |
| literature-review/SKILL.md | `name: Literature-Review` → `literature-review` | Spec name rule |
| figure-rebuild/SKILL.md | Description shortened. The full trigger list moved, unchanged, to a `## Trigger phrases` section | Spec 1,024-character limit |
| awesome-design/SKILL.md | `metadata.sources: [url]` → `metadata.source: "url"`. "55+" → "54" | Spec metadata type, accurate count |
| ten SKILL.md files and one reference file | `~/.claude/skills/...` → `${CLAUDE_SKILL_DIR}/...`, plus a short "Paths" note | Portability |
| asd-ste100/SKILL.md, scripts/ste_tool.py, new REFERENCES.md | The specification is user-supplied, with a configurable location (`ASD_STE100_PDF`, `--pdf`). The optional reference guide has fallbacks. The example names in the text and the self-test are neutral | Licensing, portability |
| finding-gap/SKILL.md, references/search-protocol.md | A fixed personal portfolio URL → "the portfolio or profile URL they give you" | Correctness: the skill fetched one person's site for every user |
| response-to-reviewer, text-humanizer | Personal file paths → placeholders | Privacy |
| audit-paper, paper-to-project-report, project-report-to-github, reference-verify, repair-paper, response-to-reviewer, universal-manuscript-polish | One author's punctuation rules → rules the user supplies, STANDARD by default. The two report checkers gained `--style` | Not imposing one person's style |
| audit-paper, research-auditor descriptions | Triggers separated (Section 5) | Fewer accidental double activations |
| highlighted-pdf-from-reviews/examples | The worked example from a real manuscript was replaced by `example_build.py` and a synthetic `examples/demo/` project | Privacy (see [PUBLIC_RELEASE_PRIVACY_AUDIT.md](PUBLIC_RELEASE_PRIVACY_AUDIT.md)) |
| paper-to-project-report/evals, project-report-to-github/evals | Private project names → Evaluation Case A to D | Privacy |
| clean-user-facing-text/scripts/common.py | Docstring names its own skill | Stale reference |

## 7. Security, privacy, and licensing

| Finding | Location | Status |
|---|---|---|
| Secret scan (API keys, tokens, private keys, passwords) | all public files | None found. One pattern hit in `text-humanizer/references/bibliography.md` is a URL slug, not a credential |
| ASD-STE100 specification and a reference guide made from it | `skills/asd-ste100/references/` | Not distributed. Both paths are in `.gitignore`. Users supply an authorized copy |
| Vendored third-party content: MIT license, VoltAgent | `skills/awesome-design/` | Kept with its license notice. Credited in README and [LICENSE_AND_ATTRIBUTION.md](LICENSE_AND_ATTRIBUTION.md) |
| Pattern lists described as adapted from two MIT-licensed catalogs, without the upstream notices | `skills/clean-user-facing-text/` | Open. Listed in LICENSE_AND_ATTRIBUTION.md |
| `-ExecutionPolicy Bypass` in a usage line | `paper-to-pptx` | Documented. It runs the bundled script only |
| No `shell=True`, `os.system`, `eval`, `exec`, or unpickling in any bundled script | all scripts | None |
| Downloaded archives are extracted only through `scripts/safe_extract.py` | paper-format-converter | Good practice |
| Project license | root | CC BY 4.0 in [LICENSE](../LICENSE) |

## 8. Recommendations

1. Disambiguate the remaining trigger overlaps in Section 5.
2. Decide whether to drop the Claude Code fields from the three affected skills for strict `skills-ref` compliance,
   accepting that the manual-only skills would then trigger automatically in Claude Code.
3. Run each skill once end to end in Codex, Antigravity, and Cursor, and record the results in
   PLATFORM_COMPATIBILITY.md.
