# License and Attribution

## The license

Academic Agent Skills is licensed under the **Creative Commons Attribution 4.0 International** license
(CC BY 4.0). The full legal code is in [LICENSE](../LICENSE), copied unchanged from
[creativecommons.org/licenses/by/4.0/legalcode](https://creativecommons.org/licenses/by/4.0/legalcode). The
human-readable summary is at [creativecommons.org/licenses/by/4.0](https://creativecommons.org/licenses/by/4.0/).
The summary is not a substitute for the legal code.

This page explains how the project applies the license. It is not legal advice.

## What the license covers

CC BY 4.0 applies to the original material of this project that its authors have the right to license:

- The skill instructions (`skills/*/SKILL.md`) and their reference documents, templates, examples, and evaluation
  records.
- The project documentation (`README.md`, `docs/`, `CONTRIBUTING.md`, `SECURITY.md`, `CHANGELOG.md`).
- The scripts and tests written for this project, inside `skills/*/scripts/` and in the repository's own `scripts/`
  and `tests/` folders (see "Software components" below).

It does not cover the material listed under "Third-party material", and it does not cover any trademark.

## Software components

Creative Commons [recommends against](https://creativecommons.org/faq/#can-i-apply-a-creative-commons-license-to-software)
using its licenses for software, because they say nothing about source code, patents, or software distribution. This
project has chosen CC BY 4.0 for the whole collection, including its scripts, because the scripts are small helpers
that the skill instructions run. In practice:

- You may use, copy, change, and redistribute the scripts, including commercially, if you give attribution as
  described below.
- CC BY 4.0 grants no express patent license and contains no software-specific terms.
- If you need a software license (for example, MIT or Apache-2.0) for a script, open an issue. This project has not
  dual-licensed any file.

## How to give attribution

When you share this project, a skill from it, or a work adapted from it, Section 3(a) of the license requires you to:

1. Credit the project: **Academic Agent Skills**.
2. Link to the source: <https://github.com/aliakarma/academic-agent-skills>.
3. Name the license and link to it: CC BY 4.0, <https://creativecommons.org/licenses/by/4.0/>.
4. Say whether you changed the material.

The license also lets you give these details in any reasonable manner for your medium, for example a link to a page
that contains them.

Example for an unchanged skill:

> `reference-verify` from [Academic Agent Skills](https://github.com/aliakarma/academic-agent-skills), licensed
> under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

Example for an adapted skill:

> Adapted from `literature-review` in [Academic Agent Skills](https://github.com/aliakarma/academic-agent-skills),
> licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Changes: shortened the search protocol
> and added a Zotero export step.

The attribution must not suggest that the project endorses you or your adaptation (Section 2(a)(6)).

## Third-party material

Some material in this repository belongs to others. It keeps its own license, and CC BY 4.0 from this project does
not apply to it or grant any permission for it.

| Material | Location | Owner and terms |
|---|---|---|
| DESIGN.md design-system specifications, preview pages, and upstream repository files | `skills/awesome-design/` | VoltAgent, MIT license in [`skills/awesome-design/LICENSE`](../skills/awesome-design/LICENSE). Keep that notice with any copy. The specifications describe the visual styles of third-party websites. The names, logos, and trademarks of those companies belong to their owners |
| Rewrite-pattern and word-replacement lists that the skill says it adapted from the public `blader/humanizer` and `conorbronsdon/avoid-ai-writing` catalogs (described there as MIT-licensed) | `skills/clean-user-facing-text/` (`scripts/score_stylometry.py`, `references/detectors.md`) | Their authors. The upstream license notices are not yet included. This is an open item for the maintainer |
| Cited publications, standards, and web pages | Bibliographies and reference files in several skills | Their publishers and authors. The skills cite and summarize them. They do not reproduce them |

Software that the skills call but that this repository does not include (Python packages, LaTeX, Poppler, Node.js
packages, Microsoft PowerPoint, Anthropic's `pptx` skill) stays under its own license. Using it with this project
does not change its license, and the CC BY 4.0 license of this project does not extend to it.

## Material that is not distributed

The `asd-ste100` skill applies the ASD-STE100 Simplified Technical English specification, which is published by ASD.
This project does not distribute the specification, extracts from it, or a reference guide made from it. ASD
controls the specification and its terms, and this project cannot license it. Users get an authorized copy from
ASD and point the skill at it. See [skills/asd-ste100/REFERENCES.md](../skills/asd-ste100/REFERENCES.md).

## For contributors

- By contributing, you agree that your contribution is licensed under CC BY 4.0 as part of this project.
- Contribute only material that you wrote or that you have the right to license under CC BY 4.0.
- For third-party material that has a compatible license and may be redistributed, keep its license file and notice
  next to it, and add a row to the table above in the same pull request.
- Do not add copyrighted standards, publisher templates, paywalled papers, or other material that may not be
  redistributed. Link to the official source instead.
- When a skill adapts ideas or text from a published source, cite it in the skill's reference files.
