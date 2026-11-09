# Installation

Three ways to install, from simplest to most manual. Every method uses the same files in `skills/`.

Test status. Commands marked *(tested)* were run on 2026-11-07 with Vercel Skills CLI 1.7.6 (the latest release on
that date) and Claude Code 2.1.90 on Windows 11, inside throw-away home and project directories. The source was a
copy of exactly the files this repository publishes, not the GitHub repository itself. Commands marked
*(documented)* follow the official documentation but cannot be tested until the GitHub repository is public.

## Prerequisites

| Need | For |
|---|---|
| Node.js 18 or later with `npx` | Vercel Skills CLI |
| Claude Code | The native plugin |
| Python 3.10 or later | Most skills run bundled Python scripts |
| A LaTeX distribution with `latexmk` and Poppler (`pdftoppm`, `pdftotext`) | Manuscript, figure, and highlighted-PDF skills |
| `PyMuPDF`, `Pillow`, `python-pptx`, `pptxgenjs` | Only the skills listed in [PLATFORM_COMPATIBILITY.md](PLATFORM_COMPATIBILITY.md#runtime-dependencies) |

## Method 1: Vercel Skills CLI (multi-agent)

The [Skills CLI](https://github.com/vercel-labs/skills) copies or links skills into each agent's skills directory.

```bash
# List the skills in the repository without installing anything (tested with a local path: 22 skills found)
npx skills add aliakarma/academic-agent-skills --list

# Install every skill for one agent, user-wide (tested with a local path)
npx skills add aliakarma/academic-agent-skills --skill '*' --agent claude-code --global --yes

# Install selected skills (tested with a local path)
npx skills add aliakarma/academic-agent-skills --skill literature-review --skill reference-verify --agent codex --global --yes

# Install for several agents at once
npx skills add aliakarma/academic-agent-skills --skill '*' --agent codex --agent antigravity --agent cursor --global --yes

# Install into the current project instead of user-wide: omit --global (tested with a local path)
npx skills add aliakarma/academic-agent-skills --skill '*' --agent codex --yes
```

Agent identifiers and the directories the CLI writes to, from the CLI's
[agent table](https://github.com/vercel-labs/skills/blob/main/docs/agents.md):

| Agent | `--agent` | Project directory | Global directory |
|---|---|---|---|
| Claude Code | `claude-code` | `.claude/skills/` | `~/.claude/skills/` |
| OpenAI Codex | `codex` | `.agents/skills/` | `~/.agents/skills/` |
| Google Antigravity | `antigravity` | `.agents/skills/` | `~/.gemini/config/skills/` |
| Cursor | `cursor` | `.agents/skills/` | `~/.cursor/skills/` |
| Gemini CLI | `gemini-cli` | `.agents/skills/` | `~/.gemini/skills/` |
| GitHub Copilot | `github-copilot` | `.agents/skills/` | `~/.copilot/skills/` |
| OpenCode | `opencode` | `.agents/skills/` | `~/.config/opencode/skills/` |

`--skill '*'` and `--agent '*'` mean "all". Quote the `*` so the shell does not expand it. Omit `--agent` to let the
CLI detect your agents or ask. Without `--yes` the CLI asks before it writes anything.

The CLI keeps one canonical copy and links it into each agent (symlink by default, `--copy` to copy instead). In the
local tests, project installs for Codex and Claude Code installed all 22 skills, one skill, and two selected skills
as requested.

### Antigravity and Cursor global installs

CLI 1.7.6 treats every agent whose project directory is `.agents/skills/` as a "universal" agent. Antigravity and
Cursor are two of them. For a global install of a universal agent, the CLI writes the canonical copy to
`~/.agents/skills/` and stops: it does not create a copy or link in the agent's own global directory. The tests
confirmed this with and without `--copy`, and with the agents' configuration folders present. It is how the CLI
works, not a problem with this repository, and `npx skills list --global` then shows the skills as "not linked".

The CLI's agent table names `~/.gemini/config/skills/` (Antigravity) and `~/.cursor/skills/` (Cursor) as global
directories, while the 1.7.6 source uses `~/.gemini/antigravity/skills/` for Antigravity. Whether either agent also
reads `~/.agents/skills/` was not tested. Until you have checked your agent:

- prefer a project install (omit `--global`), which writes `.agents/skills/` in the project for both agents, or
- copy the folders you need from `~/.agents/skills/` into the global skills directory that your agent's own
  documentation names.

Pin a release *(documented)*: `npx skills add aliakarma/academic-agent-skills@v1.0.0 --skill '*' --agent codex -g -y`.

### Update, inspect, and remove

```bash
npx skills list                    # project installs (tested)
npx skills list --global           # user-wide installs (tested)
npx skills check                   # report available updates; exits 1 when one exists (documented)
npx skills update --global --yes   # update user-wide installs (documented; local-path installs do not update)
npx skills remove aliakarma/academic-agent-skills --global --yes   # remove only this collection (tested with a local path: an unrelated skill stayed)
npx skills remove reference-verify --agent codex --yes             # remove one skill (tested)
```

Do not run `npx skills remove --skill '*' --global` to uninstall this collection. It removes every installed skill,
including skills from other sources.

## Method 2: Native Claude Code plugin

The repository root is both a plugin (`.claude-plugin/plugin.json`) and a marketplace that lists it
(`.claude-plugin/marketplace.json`). All skills install as one plugin named `academic-agent-skills`.

```bash
# Register the marketplace, then install the plugin for your user (documented)
claude plugin marketplace add aliakarma/academic-agent-skills
claude plugin install academic-agent-skills@academic-agent-skills --scope user
```

Inside a Claude Code session the same steps are `/plugin marketplace add aliakarma/academic-agent-skills` and
`/plugin install academic-agent-skills@academic-agent-skills`. Use `--scope project` to share the plugin with a
repository through `.claude/settings.json`, or `--scope local` for yourself in one project.

Plugin skills are namespaced: `/academic-agent-skills:reference-verify`. Claude also loads them automatically when a
request matches, except the manual-only skills (`asd-ste100`, `paper-format-converter`).

```bash
claude plugin list                                                 # installed plugins and status
claude plugin disable academic-agent-skills@academic-agent-skills
claude plugin enable academic-agent-skills@academic-agent-skills
claude plugin marketplace update academic-agent-skills             # fetch the latest catalog
claude plugin update academic-agent-skills@academic-agent-skills   # restart Claude Code to apply
claude plugin uninstall academic-agent-skills@academic-agent-skills
claude plugin marketplace remove academic-agent-skills             # also uninstalls its plugins
```

Try the plugin without installing it *(tested)*: clone the repository and start Claude Code with
`claude --plugin-dir ./academic-agent-skills`. The session changes no settings. In the test, the 20 skills that
Claude may load on its own were listed as `academic-agent-skills:<name>`. The two manual-only skills
(`asd-ste100`, `paper-format-converter`) are hidden from that list by design and run from their slash commands.

The plugin's `version` is pinned in `plugin.json`, so users receive a new release only after the version number
changes.

## Method 3: Manual installation

Copy the folders you want from `skills/` into the agent's skills directory (see the table in Method 1), for example:

```bash
git clone https://github.com/aliakarma/academic-agent-skills.git
cp -r academic-agent-skills/skills/reference-verify ~/.claude/skills/      # Claude Code
cp -r academic-agent-skills/skills/reference-verify ~/.agents/skills/      # Codex
```

Copy whole folders. Skills read their own `scripts/`, `references/`, and `templates/` folders.

## Skills that need other skills

Some skills call files in a sibling skill through `${CLAUDE_SKILL_DIR}/../<skill>/`. Install these together:

| Skill | Also install |
|---|---|
| `idea-to-paper` | `literature-review`, `universal-manuscript-polish` |
| `repair-paper` | `universal-manuscript-polish` (and an `audit.md` from `audit-paper`) |
| `manuscript-revision` | `response-to-reviewer`, `reference-verify`, `universal-manuscript-polish`, `text-humanizer` |
| `audit-paper` | `text-humanizer` (optional, for pattern IDs) |
| `paper-to-pptx` | Anthropic's `pptx` skill, which this repository does not include. Set `PPTX_SKILL_DIR` to its folder |
| `asd-ste100` | No other skill, but your own authorized copy of the ASD-STE100 specification ([REFERENCES.md](../skills/asd-ste100/REFERENCES.md)) |

## Troubleshooting

| Problem | Fix |
|---|---|
| `npx skills add` finds no skills | Check the repository name. Run `npx skills add aliakarma/academic-agent-skills --list` |
| A skill installed but the agent does not see it | Restart the agent. Check that the folder holds `SKILL.md` directly, for example `~/.agents/skills/reference-verify/SKILL.md` |
| Global install reports "Agents: not linked" | Expected for Antigravity and Cursor with CLI 1.7.6. See [Antigravity and Cursor global installs](#antigravity-and-cursor-global-installs) |
| Symlinks fail on Windows | Rerun with `--copy`, or enable Windows Developer Mode |
| `Plugin "academic-agent-skills" not found in marketplace` | Run `claude plugin marketplace update academic-agent-skills`, then install with the full id `academic-agent-skills@academic-agent-skills` |
| Each skill appears twice in Claude Code | You have both the plugin and a copy in `~/.claude/skills/`. Keep one |
| A script path fails with "No such file" | Outside Claude Code, replace `${CLAUDE_SKILL_DIR}` with the folder that holds the skill's `SKILL.md` |
| `asd-ste100` stops with "PDF not found" | Supply your own authorized copy of the ASD-STE100 specification: save it as the skill's `references/ASD-STE100_ISSUE9.pdf`, or set `ASD_STE100_PDF`. See [REFERENCES.md](../skills/asd-ste100/REFERENCES.md). This repository does not include it |
