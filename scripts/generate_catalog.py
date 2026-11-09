#!/usr/bin/env python3
"""Generate docs/SKILLS_CATALOG.md and the catalog table in README.md from skills/ and the CATALOG table below.

Usage:
  python scripts/generate_catalog.py          # rewrite both files
  python scripts/generate_catalog.py --check  # exit 1 if either file is out of date (used by CI)

Adding a skill: add one CATALOG entry (category, one-line summary based on what the skill actually does), then run
this script. The script fails if a skill in skills/ has no entry or an entry has no skill.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_skills import parse_frontmatter  # noqa: E402

CATEGORIES = [
    "Research Discovery and Literature",
    "Manuscript Development",
    "Academic Writing Quality",
    "Peer Review and Revision",
    "Research Quality Assurance",
    "Figures, Slides and Explainers",
    "Research Engineering and Repositories",
]

CATALOG = {
    "finding-gap": ("Research Discovery and Literature",
                    "Evidence-grounded research-gap discovery with logged searches and a verified source ledger. "
                    "Stress-tests a proposed gap and drafts research questions, hypotheses, and methods."),
    "literature-review": ("Research Discovery and Literature",
                          "Builds, extends, or repairs a manuscript's literature base: search log, source ledger, gap "
                          "matrix, verified BibTeX, and citations placed into the paper."),
    "idea-to-paper": ("Manuscript Development",
                      "Generates a complete LaTeX paper project (IEEE conference by default) from an idea, abstract, or "
                      "brief, with TikZ figures, a verified references.bib, and unmeasured results marked as targets."),
    "universal-manuscript-polish": ("Manuscript Development",
                                    "Staged, verified polishing of a LaTeX or Word manuscript for submission, "
                                    "resubmission, or camera-ready, with scan and edit-verification scripts."),
    "paper-format-converter": ("Manuscript Development",
                               "Converts a manuscript to a named journal's or conference's current official template "
                               "and guidelines, with a conversion report and a remaining-issues list. Manual only."),
    "text-humanizer": ("Academic Writing Quality",
                       "Drafts, revises, and critiques academic and professional prose for clarity, specificity, and "
                       "author voice. Also interprets AI-detection and similarity reports."),
    "audit-paper": ("Academic Writing Quality",
                    "Line-by-line forensic writing audit of a manuscript, written to audit.md without editing the "
                    "paper, and checked by a bundled script."),
    "repair-paper": ("Academic Writing Quality",
                     "Revises a manuscript against an existing audit.md so that every numbered audit issue is repaired "
                     "or accounted for."),
    "clean-user-facing-text": ("Academic Writing Quality",
                               "Audits suspicious invisible Unicode and revises reader-facing prose while keeping "
                               "facts, meaning, voice, code, citations, and quotations unchanged."),
    "peer-review": ("Peer Review and Revision",
                    "Simulates a three-reviewer Q1 journal peer review with an area-chair meta-review, for whole "
                    "manuscripts or single sections."),
    "manuscript-revision": ("Peer Review and Revision",
                            "Revises a manuscript against every editor and reviewer comment, runs the experiments "
                            "reviewers request, and writes a matching response letter, with a script that keeps the "
                            "run going until each comment is addressed or its blocker is stated."),
    "response-to-reviewer": ("Peer Review and Revision",
                             "Drafts, updates, or verifies a point-by-point response-to-reviewers letter, with scripts "
                             "that check completeness, page and line references, and numbers."),
    "highlighted-pdf-from-reviews": ("Peer Review and Revision",
                                     "Builds a highlighted revised-manuscript PDF from a LaTeX paper and its response "
                                     "letter, with each change tagged by reviewer-comment ID and mapped to pages."),
    "research-auditor": ("Research Quality Assurance",
                         "Independent pre-submission diagnosis of a research project: its real claims, the research gap "
                         "checked against the literature, closest prior work, journal fit, and acceptance blockers."),
    "repo-forensic-audit": ("Research Quality Assurance",
                            "Forensic audit of a research code repository for reproducibility, hard-coded metrics, "
                            "disconnected evaluation pipelines, and other fabrication fingerprints."),
    "reference-verify": ("Research Quality Assurance",
                         "Checks one reference against publisher, DOI, Crossref, arXiv, or issuing-body sources and "
                         "returns a corrected, paste-ready BibTeX entry. Triages a whole .bib file by script "
                         "first, with a Colab notebook front end."),
    "nanobanana-prompt-generator": ("Figures, Slides and Explainers",
                                    "Writes a NanoBanana prompt for every TikZ diagram in a paper, never for results "
                                    "figures, and a step-by-step guide for making reference images in Google Gemini "
                                    "or Flow that figure-rebuild then turns into vector figures."),
    "figure-rebuild": ("Figures, Slides and Explainers",
                       "Rebuilds a raster or AI-generated research figure as LaTeX/TikZ with selectable text and a "
                       "matched style, and audits the figure's claims against measured results."),
    "paper-to-pptx": ("Figures, Slides and Explainers",
                      "Turns a LaTeX paper into an editable 15-slide PowerPoint talk deck that stays faithful to the "
                      "paper, with rendered equations and a number-fidelity check."),
    "asd-ste100": ("Figures, Slides and Explainers",
                   "Builds an interactive offline HTML explainer of a paper, method, or codebase, with visible text "
                   "written to ASD-STE100 Issue 9 Simplified Technical English rules. Needs your own authorized copy "
                   "of the specification, which is not included. Manual only."),
    "paper-to-project-report": ("Research Engineering and Repositories",
                                "Converts a paper into an implementation-oriented PROJECT_REPORT.md (engineering spec, "
                                "reproducibility audit, roadmap phases), checked by a bundled script."),
    "project-report-to-github": ("Research Engineering and Repositories",
                                 "Builds a runnable, tested, GitHub-ready research code repository from a "
                                 "PROJECT_REPORT.md and the paper's .tex, checked by a bundled script."),
    "readme-improvement": ("Research Engineering and Repositories",
                           "Refactors a repository README.md to publication quality without changing the project's "
                           "technical meaning."),
}

README_START, README_END = "<!-- catalog:start -->", "<!-- catalog:end -->"


def load_skills(root: Path) -> dict[str, dict]:
    skills = {}
    for md in sorted((root / "skills").glob("*/SKILL.md")):
        fm, _ = parse_frontmatter(md.read_text(encoding="utf-8"))
        skills[md.parent.name] = fm
    return skills


def check_coverage(skills: dict) -> list[str]:
    problems = [f"skills/{n} has no CATALOG entry in scripts/generate_catalog.py" for n in skills if n not in CATALOG]
    problems += [f"CATALOG entry '{n}' has no skills/{n}/SKILL.md" for n in CATALOG if n not in skills]
    problems += [f"CATALOG entry '{n}' uses unknown category '{c}'" for n, (c, _) in CATALOG.items() if c not in CATEGORIES]
    return problems


def render_catalog(skills: dict) -> str:
    out = ["# Skills Catalog", "",
           "<!-- Generated by scripts/generate_catalog.py. Edit the CATALOG table there, then rerun the script. -->", "",
           f"The collection has **{len(skills)} skills** in {len(CATEGORIES)} categories. \"Manual only\" skills set "
           "`disable-model-invocation: true`, so Claude Code runs them only when you type their slash command. Other "
           "agents ignore that field. See [PLATFORM_COMPATIBILITY.md](PLATFORM_COMPATIBILITY.md) for per-agent status.", ""]
    for cat in CATEGORIES:
        names = [n for n, (c, _) in CATALOG.items() if c == cat and n in skills]
        if not names:
            continue
        out += [f"## {cat}", "", "| Skill | What it does | Invocation |", "|---|---|---|"]
        for n in sorted(names):
            mode = "Manual only" if skills[n].get("disable-model-invocation") else "Automatic or by name"
            out.append(f"| [`{n}`](../skills/{n}/SKILL.md) | {CATALOG[n][1]} | {mode} |")
        out.append("")
    return "\n".join(out)


def render_readme_table(skills: dict) -> str:
    rows = ["| Skill | Description | Category |", "|---|---|---|"]
    for cat in CATEGORIES:
        for n in sorted(n for n, (c, _) in CATALOG.items() if c == cat and n in skills):
            rows.append(f"| [`{n}`](skills/{n}/SKILL.md) | {CATALOG[n][1]} | {cat} |")
    return "\n".join(rows)


def splice_readme(readme: str, table: str) -> str:
    start, end = readme.find(README_START), readme.find(README_END)
    if start == -1 or end == -1:
        raise SystemExit(f"README.md must contain {README_START} and {README_END}")
    return readme[:start + len(README_START)] + "\n" + table + "\n" + readme[end:]


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Generate the skills catalog.")
    ap.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    ap.add_argument("--check", action="store_true", help="fail if generated files are out of date; write nothing")
    args = ap.parse_args(argv)
    root = args.root.resolve()
    skills = load_skills(root)
    problems = check_coverage(skills)
    if problems:
        print("\n".join(problems))
        return 1
    targets = {root / "docs" / "SKILLS_CATALOG.md": render_catalog(skills) + "\n"}
    readme = root / "README.md"
    targets[readme] = splice_readme(readme.read_text(encoding="utf-8"), render_readme_table(skills))
    stale = [p for p, text in targets.items() if not p.exists() or p.read_text(encoding="utf-8") != text]
    if args.check:
        for p in stale:
            print(f"out of date: {p.relative_to(root).as_posix()} (run python scripts/generate_catalog.py)")
        return 1 if stale else 0
    for p in stale:
        p.write_text(targets[p], encoding="utf-8", newline="\n")
        print(f"wrote {p.relative_to(root).as_posix()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
