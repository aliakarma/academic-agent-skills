# Architecture

## One canonical copy

```text
academic-agent-skills/          repository root = Claude Code plugin root = marketplace root
├── .claude-plugin/
│   ├── plugin.json             plugin "academic-agent-skills", version 1.0.0
│   └── marketplace.json        marketplace "academic-agent-skills", one entry with source "./"
├── skills/<name>/SKILL.md      the only copy of each skill (22), the single source of truth
├── scripts/                    repository tooling: validator and catalog generator
├── tests/                      pytest suite for the tooling and the release rules
├── docs/                       installation, catalog, compatibility, audits, license notes, this file
├── .github/                    CI workflow and issue templates
└── LICENSE                     CC BY 4.0 legal code
```

Each distribution channel reads `skills/` directly. Nothing is copied or generated per platform, so a skill is
added, changed, or removed in one place.

| Channel | How it finds the skills |
|---|---|
| Vercel Skills CLI | Searches the `skills/` container directory (and reads `.claude-plugin/` manifests) |
| Claude Code plugin | Scans the default `skills/` directory under the plugin root. `plugin.json` needs no `skills` key |
| Claude Code marketplace | `marketplace.json` lists one plugin whose `source` is `./`, the repository root |
| Manual install | The user copies `skills/<name>/` into an agent's skills directory |

The other parts have these roles:

| Part | Role |
|---|---|
| Vercel Skills CLI | Installs the skills into Claude Code, Codex, Antigravity, Cursor, and other agents from the GitHub repository. Discovery reads `skills/`, so only the folders there are installable |
| Claude Code plugin (`plugin.json`) | Names and versions the collection for Claude Code. Its skills are the folders in `skills/` |
| Claude Code marketplace (`marketplace.json`) | Lets users add the repository as a marketplace and install the plugin from it |
| Documentation (`README.md`, `docs/`) | The README catalog table and `docs/SKILLS_CATALOG.md` are generated from `skills/` and the `CATALOG` table in `scripts/generate_catalog.py` |
| Validation scripts (`scripts/`) | `validate_skills.py` checks the skills, manifests, links, and privacy rules. `generate_catalog.py` keeps the catalog in step |
| Tests (`tests/`) | Check the tooling, the expected public skill set, exclusions, ignored files, and privacy rules |
| CI (`.github/workflows/validate.yml`) | Runs the validator, the catalog check, the tests, and a Skills CLI discovery count on every push and pull request |

Files that must not be published (release planning notes, a local review folder, and the user-supplied ASD-STE100
files) are excluded by `.gitignore`. A skill leaves the public collection only by leaving `skills/` and its `CATALOG`
entry. Hiding it in the documentation is not enough.

## Why one plugin

The collection ships as one plugin with every skill. It is the simplest thing to install, and the skills depend on
each other (`idea-to-paper` calls `literature-review` and `universal-manuscript-polish` scripts, `repair-paper` calls
`universal-manuscript-polish`), so category plugins would break those links unless users installed several.

The cost is context: Claude Code lists every auto-invocable skill's description, about 13,800 characters (roughly
3,400 tokens) for the 20 auto-invocable skills. If that becomes a problem, split the marketplace into category plugins
with `git-subdir` or relative sources and keep `skills/` as the single source.

## Portability rules

- Skill names are lowercase, hyphenated, and equal to the folder name (Agent Skills specification).
- A skill refers to its own files as `${CLAUDE_SKILL_DIR}/...` and to a sibling skill as
  `${CLAUDE_SKILL_DIR}/../<skill>/...`. Claude Code substitutes the variable. Each such skill tells other agents
  to use the folder that holds its `SKILL.md`. No skill hard-codes `~/.claude/skills/`; the validator rejects it.
- Claude Code extension fields (`disable-model-invocation`, `argument-hint`, `user-invocable`) stay in the
  frontmatter. Other agents ignore them. The validator reports them as warnings.

## Versioning

`plugin.json` carries the release version, and Claude Code users receive a new release only when it changes.
Releases follow [Semantic Versioning](https://semver.org/): a major release for a removed or renamed skill or a broken
install path, a minor release for a new skill, a patch release for fixes. Record every release in `CHANGELOG.md` and
tag it `vX.Y.Z`, which also lets Skills CLI users pin `aliakarma/academic-agent-skills@vX.Y.Z`.

## Quality gates

`scripts/validate_skills.py` checks the skills, manifests, and documentation links. `scripts/generate_catalog.py
--check` keeps the catalog in step with `skills/`. `tests/` covers both scripts and the release rules. `.github/workflows/validate.yml`
runs all three on every push and pull request, plus a Vercel Skills CLI discovery count.
