#!/usr/bin/env python3
"""Static checks for the paper-format-converter skill.

Usage: python validate_skill.py [SKILL_DIR]

Reads the skill files and runs both script self-tests in temporary folders.
It never opens or converts a manuscript. Exit code 1 when any check fails.
"""
import re
import subprocess
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# Frontmatter fields documented at https://code.claude.com/docs/en/skills (checked 2026-10-29).
KNOWN_FIELDS = {"name", "description", "when_to_use", "argument-hint", "arguments", "disable-model-invocation",
                "user-invocable", "allowed-tools", "disallowed-tools", "model", "effort", "context", "agent",
                "background", "hooks", "paths", "shell", "metadata", "license", "compatibility"}
FILES = ["SKILL.md", "references/research-and-source-verification.md", "references/manuscript-conversion-workflow.md",
         "references/compliance-and-quality-assurance.md", "scripts/safe_extract.py",
         "scripts/conversion_integrity.py", "evals/test-cases.md", "evals/validate_skill.py"]
# Mandatory instructions, by file.
REQUIRED = {
    "SKILL.md": ["Journal-Guidelines.md", "remaining-issues.md", "conversion-report.md", " Format/",
                 "Never edit, move, rename, or build inside the original manuscript", "never the whole disk",
                 "Unverified", "-shell-escape", "Never install software", "safe_extract.py", "conversion_integrity.py",
                 "AUTHOR INPUT REQUIRED", "submission-ready", "latexmk -norc", "read this file again",
                 "Anonymize only when the venue requires it", "Write `Journal-Guidelines.md` now",
                 "stop before Phase 1 and ask"],
    "references/research-and-source-verification.md": [
        "Source hierarchy", "verbatim", "Official source register", "Compliance requirements", "Quantitative limits",
        "Uncertainties and conflicts", "Access date", "Never claim an official template you did not obtain"],
    "references/manuscript-conversion-workflow.md": [
        "Baseline the original", "Never add, drop, or substitute an entry", "keep every image file unchanged",
        "AutomationSecurity = 3", "Silence is not a statement", "Anonymization", "PDF-only source"],
    "references/compliance-and-quality-assurance.md": [
        "PASS", "FAIL", "WARN", "UNVERIFIED", "NOT APPLICABLE", "Critical", "Major", "Minor", "R-001",
        "latexmk -norc", "texcount", "pdfinfo", "pdftoppm", "SUBMISSION-READY", "AUTHOR INPUT NEEDED", "NOT READY",
        "Never present an estimate as a measurement"],
}
# The governing instruction for each test case in evals/test-cases.md, searched across SKILL.md and references.
COVERAGE = {
    "TC-01": ["Raw arguments: [$ARGUMENTS]", "Phase 8: Final reply", "Official source register"],
    "TC-02": ["If the venue name is missing, ask one question"],
    "TC-03": ["Map every dependency", "relative paths intact", "cite, label, ref, urls, or graphics missing"],
    "TC-04": ["Keep the source format", "Word route", "AutomationSecurity = 3"],
    "TC-05": ["If the template cannot be obtained", "Never claim an official template you did not obtain"],
    "TC-06": ["keep the content and log the issue", "both the observed count and the limit"],
    "TC-07": ["AUTHOR INPUT REQUIRED", "Silence is not a statement"],
    "TC-08": ["A missing tool is a finding", "Never install software"],
    "TC-09": ["A genuine tie: ask one question that lists the tied files"],
    "TC-10": ["record it as unresolved, apply the stricter reading", "UNVERIFIED"],
    "TC-11": ["stop before Phase 1 and ask"],
}


def frontmatter(text):
    m = re.match(r"---\r?\n(.*?)\r?\n---\r?\n", text, re.S)
    if not m:
        return None, text, "no frontmatter block"
    try:
        import yaml  # type: ignore[import-untyped]
    except ImportError:  # minimal fallback: one "key: value" per line
        data = {}
        for line in m.group(1).splitlines():
            key, _, value = line.partition(":")
            value = value.strip().strip('"')
            data[key.strip()] = {"true": True, "false": False}.get(value.lower(), value)
        return data, text[m.end():], ""
    try:
        return yaml.safe_load(m.group(1)), text[m.end():], ""
    except yaml.YAMLError as error:
        return None, text[m.end():], str(error)


def report(results):
    for ok, name, detail in results:
        print(("PASS  " if ok else "FAIL  ") + name + ("" if ok or not detail else f"  [{detail}]"))
    failed = sum(not ok for ok, _, _ in results)
    print(f"\nRESULT: {'FAIL' if failed else 'PASS'} ({len(results) - failed} of {len(results)} checks passed)")
    return 1 if failed else 0


def main():
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent
    results = []

    def check(name, ok, detail=""):
        results.append((bool(ok), name, detail))

    missing = [f for f in FILES if not (root / f).is_file()]
    check("required files present", not missing, f"missing {missing}")
    if missing:
        return report(results)

    skill = (root / "SKILL.md").read_text(encoding="utf-8")
    fm, body, error = frontmatter(skill)
    check("frontmatter parses as YAML", fm is not None, error)
    fm = fm or {}
    check("name is paper-format-converter and matches the folder",
          fm.get("name") == root.name == "paper-format-converter", f"name {fm.get('name')!r}, folder {root.name!r}")
    desc = str(fm.get("description") or "")
    check("description has 1 to 1536 characters and no angle brackets",
          0 < len(desc) <= 1536 and not re.search(r"[<>]", desc), f"{len(desc)} characters")
    check("argument-hint names the venue argument", "conference name" in str(fm.get("argument-hint", "")))
    check("manual invocation only (disable-model-invocation: true)", fm.get("disable-model-invocation") is True)
    unknown = sorted(set(fm) - KNOWN_FIELDS)
    check("only documented frontmatter fields", not unknown, f"unknown {unknown}")
    check("$ARGUMENTS appears exactly once in the body", body.count("$ARGUMENTS") == 1,
          f"{body.count('$ARGUMENTS')} found")
    stray = re.findall(r"\$\d|\$ARGUMENTS\[", body)
    check("no positional placeholders that Claude Code would substitute", not stray, f"found {stray}")
    check("scripts are called through ${CLAUDE_SKILL_DIR}", "${CLAUDE_SKILL_DIR}/scripts/" in body)
    lines = len(skill.splitlines())
    check("SKILL.md stays under 500 lines", lines < 500, f"{lines} lines")

    broken = []
    for md in sorted(root.rglob("*.md")):
        text = md.read_text(encoding="utf-8")
        for target in re.findall(r"\]\(([^)\s#]+)\)", text):
            if not target.startswith(("http://", "https://")) and not (md.parent / target).exists():
                broken.append(f"{md.relative_to(root).as_posix()} -> {target}")
        for target in re.findall(r"`((?:references|scripts|evals)/[^`\s]+)`", text):
            if not (root / target).exists():
                broken.append(f"{md.relative_to(root).as_posix()} -> {target}")
    check("every linked or named skill file exists", not broken, f"broken {broken}")
    unlinked = [p.relative_to(root).as_posix() for p in sorted((root / "references").glob("*.md"))
                if f"]({p.relative_to(root).as_posix()})" not in skill]
    check("SKILL.md links every reference file", not unlinked, f"unlinked {unlinked}")

    for rel, phrases in REQUIRED.items():
        text = (root / rel).read_text(encoding="utf-8")
        absent = [p for p in phrases if p not in text]
        check(f"mandatory instructions present in {rel}", not absent, f"absent {absent}")
    corpus = skill + "".join(p.read_text(encoding="utf-8") for p in sorted((root / "references").glob("*.md")))
    cases = (root / "evals/test-cases.md").read_text(encoding="utf-8")
    for case, phrases in COVERAGE.items():
        absent = [p for p in phrases if p not in corpus]
        check(f"{case} is defined and its governing instructions exist",
              f"### {case}" in cases and not absent, f"absent {absent}" if absent else "not defined in test-cases.md")

    dashes, semicolons = [], []
    for f in sorted(root.rglob("*")):
        if f.suffix not in (".md", ".py") or not f.is_file():
            continue
        text = f.read_text(encoding="utf-8")
        rel = f.relative_to(root).as_posix()
        if chr(0x2014) in text:  # em dash, written as a code point so this file stays ASCII
            dashes.append(rel)
        if f.suffix == ".md":
            fenced = False
            for n, line in enumerate(text.splitlines(), 1):
                if line.lstrip().startswith("```"):
                    fenced = not fenced
                elif not fenced and ";" in re.sub(r"`[^`]*`", "", line):
                    semicolons.append(f"{rel}:{n}")
    check("no em dashes in skill files", not dashes, f"found in {dashes}")
    check("no semicolons in Markdown prose", not semicolons, f"found at {semicolons[:10]}")

    for script in ("safe_extract.py", "conversion_integrity.py"):
        run = subprocess.run([sys.executable, "-I", str(root / "scripts" / script), "--self-test"],
                             capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=300)
        check(f"{script} self-test", run.returncode == 0 and "SELF-TEST PASS" in run.stdout,
              (run.stdout + run.stderr).strip()[-400:])
    return report(results)


if __name__ == "__main__":
    sys.exit(main())
