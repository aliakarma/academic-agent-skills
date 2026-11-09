# Platform Compatibility

Status as of 2026-11-07. Every skill uses the open [Agent Skills](https://agentskills.io/specification) layout
(`SKILL.md` with `name` and `description`, plus `scripts/`, `references/`, `templates/`). This page separates two
things that are easy to confuse:

- **Format compatibility.** The skill's files follow the standard, so an agent that supports Agent Skills can load it.
- **Runtime verification.** Someone ran the skill end to end in that agent and checked the result.

## What was actually tested

| Test | Result |
|---|---|
| `python scripts/validate_skills.py` (spec rules, repository rules, privacy rules) | 22 skills, 0 errors |
| Rules of the official `skills-ref` validator, compared by reading its source (not executed) | 19 skills pass. 3 fail its "unexpected fields" rule because they keep Claude Code fields (see below) |
| `claude plugin validate .` and `claude plugin validate .claude-plugin/plugin.json`, Claude Code 2.1.90 | Both passed |
| `claude --plugin-dir <public copy> -p ...`, Claude Code 2.1.90, one headless session | Plugin loaded. The model's skill list showed the 20 auto-invocable skills as `academic-agent-skills:<name>`. The 2 manual-only skills are hidden from that list by design. Their slash commands were not invoked |
| `npx skills@1.7.6 add <local path> --list`, on the working tree and on a copy of the published files | 22 skills discovered. No excluded or local-only material discovered |
| `npx skills@1.7.6 add <local path>` project install, `--agent codex --agent claude-code`: all skills, one skill, two selected skills | 22, 1, and 2 skills installed to `.agents/skills/` and `.claude/skills/` as requested |
| Same, `--global --agent antigravity --agent cursor`, throw-away home, with and without `--copy` and agent folders | Only `~/.agents/skills/` written. CLI 1.7.6 treats both agents as "universal" and skips their global directories (read from the CLI source). Whether the agents read `~/.agents/skills/` was not tested |
| `npx skills remove <source> --global`, with an unrelated skill installed | Removed this collection's 22 skills. The unrelated skill stayed |
| Any skill executed end to end in any agent | **Not done** |

No row in the matrix below is "Verified", because no skill's behaviour was integration-tested in any agent.

## Status labels

**Verified** = run end to end in that agent and checked (no skill has this status yet). **Format-compatible** =
format-compatible, not integration-tested. **Partial** = partially compatible: it loads, but a named feature depends
on one agent. **Adapt** = requires adaptation: it needs a component or setup this repository does not ship.
**Unsupported** = known not to work in that agent (no skill has this status). **Not assessed** = not reviewed for
that agent.

For Antigravity and Cursor, the statuses describe the skill files. A global install through the Vercel CLI needs the
extra step in [INSTALLATION.md](INSTALLATION.md#antigravity-and-cursor-global-installs).

## Matrix

| Skill | Claude Code | Codex | Antigravity | Cursor | Other agents | Known limitations |
|---|---|---|---|---|---|---|
| asd-ste100 | Adapt | Adapt | Adapt | Adapt | Not assessed | Needs the user's own authorized copy of the ASD-STE100 specification (not included, see `REFERENCES.md`) and PyMuPDF. Uses `$ARGUMENTS` and `disable-model-invocation`, which only Claude Code honours |
| audit-paper | Format-compatible | Format-compatible | Format-compatible | Format-compatible | Not assessed | Script path uses `${CLAUDE_SKILL_DIR}`. Applies punctuation rules only when the user supplies them |
| awesome-design | Format-compatible | Format-compatible | Format-compatible | Format-compatible | Not assessed | Ships `agents/openai.yaml` UI metadata for Codex. Not an academic skill |
| clean-user-facing-text | Format-compatible | Format-compatible | Format-compatible | Format-compatible | Not assessed | None found |
| figure-rebuild | Format-compatible | Format-compatible | Format-compatible | Format-compatible | Not assessed | Needs LaTeX, PyMuPDF, Pillow. Names the Claude "Write tool" in one tip |
| finding-gap | Partial | Partial | Partial | Partial | Not assessed | Prefers the Consensus and Scholar Gateway MCP connectors (`mcp__Consensus__search`). Without them it falls back to web search |
| highlighted-pdf-from-reviews | Format-compatible | Format-compatible | Format-compatible | Format-compatible | Not assessed | Needs LaTeX (`latexmk`) and Poppler |
| idea-to-paper | Format-compatible | Partial | Partial | Partial | Not assessed | Uses `$ARGUMENTS` and `argument-hint` (Claude Code only). Needs sibling skills `literature-review` and `universal-manuscript-polish`. Its checker reports em dashes and semicolons in generated papers as errors (E14, E15) |
| literature-review | Format-compatible | Format-compatible | Format-compatible | Format-compatible | Not assessed | Names Claude tools (WebFetch, WebSearch, Chrome). Needs web access |
| paper-format-converter | Format-compatible | Partial | Partial | Partial | Not assessed | Manual-only and `$ARGUMENTS` apply in Claude Code only. Needs web access and LaTeX |
| paper-to-pptx | Adapt | Adapt | Adapt | Adapt | Not assessed | Requires Anthropic's `pptx` skill (`PPTX_SKILL_DIR`), Node.js `pptxgenjs`, `python-pptx`, and Windows PowerPoint for PDF export |
| paper-to-project-report | Format-compatible | Format-compatible | Format-compatible | Format-compatible | Not assessed | Checker's punctuation check runs only with `--style` |
| peer-review | Format-compatible | Format-compatible | Format-compatible | Format-compatible | Not assessed | None found |
| project-report-to-github | Format-compatible | Format-compatible | Format-compatible | Format-compatible | Not assessed | Checker's punctuation check runs only with `--style` |
| readme-improvement | Format-compatible | Format-compatible | Format-compatible | Format-compatible | Not assessed | None found |
| reference-verify | Format-compatible | Format-compatible | Format-compatible | Format-compatible | Not assessed | Names Claude tools (WebFetch, WebSearch, Chrome). Needs web access |
| repair-paper | Format-compatible | Format-compatible | Format-compatible | Format-compatible | Not assessed | Needs sibling skill `universal-manuscript-polish` and an `audit.md` |
| repo-forensic-audit | Format-compatible | Format-compatible | Format-compatible | Format-compatible | Not assessed | None found |
| research-auditor | Format-compatible | Format-compatible | Format-compatible | Format-compatible | Not assessed | Needs web access for gap verification |
| response-to-reviewer | Format-compatible | Format-compatible | Format-compatible | Format-compatible | Not assessed | Needs PyMuPDF or Poppler for line indexes |
| text-humanizer | Format-compatible | Format-compatible | Format-compatible | Format-compatible | Not assessed | None found |
| universal-manuscript-polish | Format-compatible | Format-compatible | Format-compatible | Format-compatible | Not assessed | Word `.docx` manuscripts need a tool that can edit and render Word files |

## Claude Code features and how other agents treat them

| Feature | Used by | In Claude Code | In other agents |
|---|---|---|---|
| `${CLAUDE_SKILL_DIR}` | 10 skills | Replaced with the skill's folder | Seen literally. Each skill states that it means "the folder that holds this SKILL.md" |
| `disable-model-invocation: true` | asd-ste100, paper-format-converter | Skill runs only from its slash command | Ignored, so the agent may load it on a matching request. asd-ste100's own text asks before building when it was not called by name |
| `argument-hint`, `user-invocable` | asd-ste100, idea-to-paper, paper-format-converter | Autocomplete hint and `/` menu control | Ignored |
| `$ARGUMENTS` | asd-ste100, idea-to-paper, paper-format-converter | Replaced with the command's arguments | Seen literally. The agent uses the user's request instead |
| Sibling paths `${CLAUDE_SKILL_DIR}/../<skill>` | audit-paper, idea-to-paper, repair-paper | Works when the siblings are installed in the same skills folder | Same, once `${CLAUDE_SKILL_DIR}` is resolved |
| Skills outside this repository named as alternatives (`bibtex-validator`, `manuscript-revision`, `humanize-latex`, `MDPI-Format`, `anthropic-skills:pptx`) | several descriptions | Routing hints. Only `paper-to-pptx` depends on one | Same |

The three skills with Claude Code fields fail the official `skills-ref` rule that rejects unexpected frontmatter keys.
They keep those fields because removing `disable-model-invocation` would make two manual-only skills trigger
automatically in Claude Code. Agents that ignore unknown fields, including the Vercel CLI in the test above, load them
normally.

## Runtime dependencies

| Dependency | Needed by |
|---|---|
| Python 3.10+ standard library | All bundled Python scripts |
| PyMuPDF (`fitz`) | asd-ste100 (reads the user-supplied specification), figure-rebuild (`verify_selectable.py`), response-to-reviewer (`build_line_index.py`, or Poppler `pdftotext`) |
| Pillow | figure-rebuild (`extract_icons.py`), paper-to-pptx |
| python-pptx | paper-to-pptx (`qa_check.py`) |
| PyYAML | paper-format-converter (`evals/validate_skill.py`), this repository's validator |
| bibtexparser 1.x, requests | reference-verify (`verify_bib.py`, whole-file mode) |
| Node.js + `pptxgenjs` | paper-to-pptx |
| LaTeX (`latexmk`, `pdflatex`) | figure-rebuild, highlighted-pdf-from-reviews, idea-to-paper, paper-format-converter, paper-to-pptx, response-to-reviewer, universal-manuscript-polish |
| Poppler (`pdftoppm`, `pdftocairo`, `pdftotext`) | highlighted-pdf-from-reviews, idea-to-paper, paper-format-converter, paper-to-pptx, response-to-reviewer |
| Windows PowerShell + Microsoft PowerPoint | paper-to-pptx PDF export (`export_pdf.ps1`) |
