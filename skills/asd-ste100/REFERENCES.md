# ASD-STE100 reference material

This skill applies the rules of ASD-STE100 Simplified Technical English, Issue 9. The specification is published by
ASD (the AeroSpace, Security and Defence Industries Association of Europe). **This skill does not include the
specification, extracts from it, or any reference guide made from it.**

## What you need

- Your own authorized copy of the ASD-STE100 Issue 9 specification (PDF). Get it from ASD through its official
  website, [www.asd-ste100.org](https://www.asd-ste100.org/). The terms of use are ASD's. Read them there, because
  they can change and this project does not restate them.
- [PyMuPDF](https://pypi.org/project/PyMuPDF/) (`pip install pymupdf`), so that `scripts/ste_tool.py` can read the
  dictionary pages of your copy.

## Tell the skill where your copy is

`scripts/ste_tool.py` uses the first of these that exists:

1. The `--pdf PATH` option: `python scripts/ste_tool.py lookup explain --pdf "/path/to/ASD-STE100_ISSUE9.pdf"`.
2. The `ASD_STE100_PDF` environment variable, set to the full path of the PDF.
3. `references/ASD-STE100_ISSUE9.pdf` inside this skill folder.

Run `python scripts/ste_tool.py selftest` to confirm that the tool can read your copy. The self-test expects the
Issue 9 page layout. Another issue of the standard needs changes to the page constants at the top of the script.

The tool reads the PDF each time it runs and stores no copy of the word list.

## Optional: your own rule index

The skill can also use a rule index that you write yourself from your copy, saved as
`references/STE-ISSUE9-REFERENCE-GUIDE.md`. When that file is absent, the skill reads the rule pages of the PDF
instead.

## Keep the material out of public repositories

If you work from a clone of this repository, the two paths above (`references/ASD-STE100_ISSUE9.pdf` and
`references/STE-ISSUE9-REFERENCE-GUIDE.md`) are listed in the repository's `.gitignore`, so Git does not pick them
up. Do not force-add them, and do not commit the PDF, extracts from it, or a guide made from it to any public
repository or shared folder. If you keep the PDF somewhere else, use `ASD_STE100_PDF` and leave the skill folder
unchanged.

Websites that this skill builds must not contain copies of the standard or long passages from it. Rule 9 in
[SKILL.md](SKILL.md) says so.
