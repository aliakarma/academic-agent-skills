# License and Attribution

## The license

Academic Agent Skills is released under the **MIT License**. The full text is in [LICENSE](../LICENSE). It is the
standard MIT text as published by the [Open Source Initiative](https://opensource.org/license/mit).

This page explains how the project applies the license. It is not legal advice.

Releases up to and including 1.0.0 were published under the Creative Commons Attribution 4.0 International license
(CC BY 4.0). Copies obtained under that license keep it. Everything published after 1.0.0 is under MIT.

## What the license covers

The MIT License applies to the original material of this project that its authors have the right to license:

- The skill instructions (`skills/*/SKILL.md`) and their reference documents, templates, examples, and evaluation
  records.
- The scripts and tests written for this project, inside `skills/*/scripts/` and in the repository's own `scripts/`
  and `tests/` folders.
- The project documentation (`README.md`, `docs/`, `CONTRIBUTING.md`, `SECURITY.md`, `CHANGELOG.md`) and the images
  in `docs/images/`.

It does not cover the material listed under "Third-party material", and it does not cover any trademark.

## What you may do

- Use, copy, change, merge, publish, distribute, sublicense, and sell the material, in open or closed projects.
- Ship a single skill, or an adapted skill, on its own.

The one condition: every copy or substantial portion must include the copyright notice and the license text from
[LICENSE](../LICENSE). The material comes with no warranty.

## How to give credit

The MIT License requires the copyright notice and license text, nothing more. A visible credit is appreciated, for
example:

> `reference-verify` from [Academic Agent Skills](https://github.com/aliakarma/academic-agent-skills) (MIT License).

For an adapted skill, say what you changed:

> Adapted from `literature-review` in [Academic Agent Skills](https://github.com/aliakarma/academic-agent-skills)
> (MIT License). Changes: shortened the search protocol and added a Zotero export step.

A credit must not suggest that the project endorses you or your adaptation.

## Third-party material

Some material in this repository belongs to others. It keeps its own license, and the MIT License of this project
does not apply to it or grant any permission for it.

| Material | Location | Owner and terms |
|---|---|---|
| Rewrite-pattern and word-replacement lists that the skill says it adapted from the public `blader/humanizer` and `conorbronsdon/avoid-ai-writing` catalogs (described there as MIT-licensed) | `skills/clean-user-facing-text/` (`scripts/score_stylometry.py`, `references/detectors.md`) | Their authors. The upstream license notices are not yet included. This is an open item for the maintainer |
| Cited publications, standards, and web pages | Bibliographies and reference files in several skills | Their publishers and authors. The skills cite and summarize them. They do not reproduce them |

Software that the skills call but that this repository does not include (Python packages, LaTeX, Poppler, Node.js
packages, Microsoft PowerPoint, LibreOffice, Google Flow, Anthropic's `pptx` skill) stays under its own license.
Using it with this project does not change its license, and the MIT License of this project does not extend to it.

## Material that is not distributed

The `asd-ste100` skill applies the ASD-STE100 Simplified Technical English specification, which is published by ASD.
This project does not distribute the specification, extracts from it, or a reference guide made from it. ASD
controls the specification and its terms, and this project cannot license it. Users get an authorized copy from
ASD and point the skill at it. See [skills/asd-ste100/REFERENCES.md](../skills/asd-ste100/REFERENCES.md).

## For contributors

- By contributing, you agree that your contribution is licensed under the MIT License as part of this project.
- Contribute only material that you wrote or that you have the right to license under the MIT License.
- For third-party material that has a compatible license and may be redistributed, keep its license file and notice
  next to it, and add a row to the table above in the same pull request.
- Do not add copyrighted standards, publisher templates, paywalled papers, or other material that may not be
  redistributed. Link to the official source instead.
- When a skill adapts ideas or text from a published source, cite it in the skill's reference files.
