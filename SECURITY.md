# Security Policy

## What to report

- A skill that instructs an agent to run unsafe commands, exfiltrate data, or ignore the user's instructions.
- A bundled script with a vulnerability, such as unsafe archive extraction, shell injection, or credential exposure.
- A secret, credential, or personal data committed to the repository.
- Content that may not be redistributed (copyright or license problems), such as a copy of the ASD-STE100
  specification.
- Personal data or unpublished research details in an example, test record, or document.

## How to report

Use GitHub's private vulnerability reporting for this repository (Security tab, "Report a vulnerability"). Do not
open a public issue for a security problem, and do not include a live secret in any report. Say where it is and what
kind it is.

Expect an acknowledgment within 7 days. Supported versions: the latest release only.

## What skills can do

Skills are instructions plus scripts, and they run with the permissions of the agent that loads them. Before you
install a skill:

- Read its `SKILL.md` and any script it tells the agent to run.
- Note the skills that use the network (`literature-review`, `reference-verify`, `finding-gap`, `research-auditor`,
  `paper-format-converter`).
- `paper-format-converter` downloads publisher templates. It extracts archives only through its
  `scripts/safe_extract.py` and never runs downloaded scripts.
- `paper-to-pptx` runs a bundled PowerShell script with `-ExecutionPolicy Bypass` to export slides through PowerPoint.

The repository's own scripts (`scripts/validate_skills.py`, `scripts/generate_catalog.py`) read files only, except that
`generate_catalog.py` without `--check` rewrites `docs/SKILLS_CATALOG.md` and the catalog table in `README.md`.
