# Public Release Privacy Audit

How this repository keeps personal data, unpublished research, and restricted material out of its public files.
Dated 2026-11-07, for release 1.0.0. This page describes the practices and the checks. It does not list the
private values that were removed.

## What was reviewed

Every file that the repository publishes: skill instructions, reference files, templates, examples, evaluation
records, scripts, tests, configuration, manifests, issue templates, workflows, and documentation. The review also
covered file names and paths, and looked for embedded document metadata. The public tree contains no PDF, Word,
PowerPoint, spreadsheet, archive, or image file, so there was no document metadata to scrub. The HTML preview pages
of the vendored `awesome-design` library are third-party demonstration material.

The review read each finding in context. It did not replace text blindly. Citations of published research and the
names of their authors are kept.

## What was changed

| Kind of material | Action |
|---|---|
| Names of private research projects used as test labels in evaluation records | Replaced with neutral labels (Evaluation Case A to D). The checker results that each record documents are unchanged |
| A worked example built from an unpublished manuscript (its title, manuscript ID, revised text, and reviewer-comment map) | Removed from the public tree, because it could not be anonymized without inventing replacement content. A synthetic example that runs end to end replaced it |
| Example names and file paths taken from private projects | Replaced with neutral names (`ExampleNet`, `Smith et al.`, `src/monitor.py`) |
| A fixed personal website that a skill fetched for every user | Replaced with "the URL the user gives you" |
| Personal machine paths in examples | Replaced with placeholders (`C:/Users/Jane Doe/...`, `C:\Users\<name>\...`) |
| One author's writing preferences applied to every user | Made optional (see [SKILLS_AUDIT.md](SKILLS_AUDIT.md), Section 4) |
| A skill that depends on an unpublished service | Not part of the public collection |
| The ASD-STE100 specification and a reference guide made from it | Not distributed. Users supply their own authorized copy ([skills/asd-ste100/REFERENCES.md](../skills/asd-ste100/REFERENCES.md)) |

Detailed findings, with their former locations, are kept outside the repository.

## What stays out of the repository

`.gitignore` excludes:

- Release planning files and a local review folder used to prepare releases.
- The user-supplied ASD-STE100 files at their default paths in `skills/asd-ste100/references/`.
- Caches and virtual environments (`__pycache__/`, `.mypy_cache/`, `.ruff_cache/`, `.pytest_cache/`, `.venv/`,
  `node_modules/`) and browser-test snapshots (`.playwright-cli/`).

## Automated checks

`python scripts/validate_skills.py` fails the build when a public file contains:

- a personal machine path (`C:\Users\<real name>\`, `/Users/<name>/`, `/home/<name>/`; placeholders are allowed),
- an e-mail address other than an `example.com` or GitHub `noreply` address (the vendored design previews are
  exempt, because they show placeholder sign-up forms),
- a PDF, Office document, or archive inside `skills/` that `.gitignore` does not declare as user-supplied,
- a term from a maintainer's private denylist. The denylist is a local file that is never published. When it is
  absent, for example in CI, this one check is skipped.

`tests/test_public_release.py` builds the exact list of files that Git would publish from a fresh clone, and checks
that no planning file, review file, excluded skill, restricted standard, or cache is on it.

## For contributors

- Use placeholders in examples: `C:/Users/<name>/`, `name@example.com`, `Example Author`.
- Do not add private manuscripts, unpublished results, reviewer comments, or project names to examples or test
  records. Build a small synthetic fixture instead, as `skills/highlighted-pdf-from-reviews/examples/demo/` does.
- Remove personal data from document properties before you add a PDF, Office file, or image.
- Report a privacy problem privately, as [SECURITY.md](../SECURITY.md) describes.
