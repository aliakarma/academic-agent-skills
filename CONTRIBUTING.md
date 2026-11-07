# Contributing

Contributions are welcome: new skills, fixes to existing skills, compatibility reports for other agents, and
documentation corrections.

## Ground rules

- **One canonical copy.** Every skill lives only in `skills/<name>/`. Do not add per-agent copies.
- **Honest skills.** A skill must not fabricate citations, data, results, or test outcomes, and must say what it did not
  verify. Describe only what the skill actually does.
- **Redistributable content only.** Add only files you have the right to publish. Copyrighted standards, publisher
  templates, and paywalled papers stay out. Reference them and let users download them.
- **No secrets or personal data.** No API keys, tokens, personal paths, e-mail addresses, private manuscripts, or
  unpublished project names, including in examples and test records. Use placeholders and synthetic fixtures. See
  [docs/PUBLIC_RELEASE_PRIVACY_AUDIT.md](docs/PUBLIC_RELEASE_PRIVACY_AUDIT.md).
- **License.** Contributions are licensed under CC BY 4.0, the project license. Keep the license notice of any
  third-party material you add, and list it in [docs/LICENSE_AND_ATTRIBUTION.md](docs/LICENSE_AND_ATTRIBUTION.md).

## Add or change a skill

1. Create `skills/<name>/SKILL.md`. The folder name and the `name` field must match and use lowercase letters, digits,
   and single hyphens. Write a `description` of at most 1,024 characters that says what the skill does and when to
   use it. See the [Agent Skills specification](https://agentskills.io/specification).
2. Put scripts in `scripts/`, long documentation in `references/`, and templates or static files in `templates/` or
   `assets/`. Keep `SKILL.md` under 500 lines.
3. Refer to the skill's own files as `${CLAUDE_SKILL_DIR}/scripts/...`, never `~/.claude/skills/...`, and add the
   "Paths" note that other skills use so that agents other than Claude Code know how to read it. Refer to a sibling
   skill as `${CLAUDE_SKILL_DIR}/../<skill>/...` and list the dependency in `docs/INSTALLATION.md`.
4. Python scripts use the standard library where possible. List any third-party package or system tool in
   `docs/PLATFORM_COMPATIBILITY.md` under Runtime dependencies.
5. Add a `CATALOG` entry (category and a one-line summary) in `scripts/generate_catalog.py`, then run it.
6. Add a row to the matrix in `docs/PLATFORM_COMPATIBILITY.md`. Use "Verified" only for an agent in which you ran the
   skill end to end.
7. Note the change under "Unreleased" in `CHANGELOG.md`.

Claude Code fields such as `disable-model-invocation` and `argument-hint` are allowed. The validator reports them as
warnings because other agents ignore them.

## Run the checks

```bash
pip install -r requirements-dev.txt
python scripts/validate_skills.py          # skills, manifests, documentation links, privacy rules
python scripts/generate_catalog.py --check # catalog and README table are current
python -m pytest tests                     # tests for the scripts and the release rules
claude plugin validate .                   # optional, needs Claude Code
npx skills add . --list                    # optional, needs Node.js: every skill must be listed
```

CI runs the first three on every push and pull request.

## Pull requests

Keep one skill or one topic per pull request. Describe what changed, why, and how you tested it, including which
agent you used. For a change to an existing skill's instructions, quote the old and new text of each substantive
change.

## Report a compatibility result

Open an issue with the "Compatibility report" template: the agent and version, the skill, what you asked, and what
happened.
