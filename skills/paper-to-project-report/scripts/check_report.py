#!/usr/bin/env python3
"""Mechanical gate for a PROJECT_REPORT.md written by the paper-to-project-report skill.

Usage:
  python check_report.py PROJECT_REPORT.md [--aux paper.aux] [--style]
  python check_report.py --selftest

Checks (ERROR blocks the handoff, WARN must be fixed or justified in the reply):
  P01 section-36 hierarchy present and in order    P06 REQ entries without evidence
  P02 stable IDs exist (REQ mandatory)              P07 results carry provenance labels
  P03 every cited ID is defined                     P08 Table/Fig/Eq/Algorithm numbers exist in .aux
  P04 GSD Handoff has every required block          P09 optional house style (--style)            
  P05 REQ entries without A/B/C/D classification    P10 meta-commentary, unfilled template lines
  P11 no Mermaid diagram
Exit status 1 when any ERROR is found. Standard library only, Python 3.10+.
"""
from __future__ import annotations

import argparse
import re
import sys
import tempfile
from pathlib import Path

ERR, WARN = "ERROR", "WARN"
FAMILIES = ["REQ", "EXP", "METRIC", "DEC", "ASM", "DEP", "RISK"]
ID = r"\b(?:REQ|EXP|METRIC|DEC|ASM|DEP|RISK)-[A-Z]*\d+[A-Z]?\b"
DEFINE = re.compile(rf"^\s*(?:#{{1,6}}\s+|[-*\u2022]\s+|\|\s*|\d+\.\s+)?(?:\*\*|`)?({ID})(?:\*\*|`)?\s*(?:[.:|)]|\*\*|$|\s-\s)")
SECTIONS = [  # prompt section 36, in order: (name, heading regex)
    ("Executive Technical Summary", r"executive"),
    ("Research Objectives", r"objective"),
    ("Requirements Specification", r"requirement"),
    ("System Architecture", r"architecture"),
    ("System Boundary", r"boundar"),
    ("Mathematical Foundations", r"mathemat"),
    ("Algorithms and Methodology", r"algorithm|methodolog"),
    ("Dataset and Data Pipeline", r"data"),
    ("Model and Training Specification", r"model|training"),
    ("Experimental Specification", r"experiment(al)? (spec|design|protocol|setup)"),
    ("Experimental Results", r"result"),
    ("Reproducibility Audit", r"reproducibility audit"),
    ("Assumptions and Unknown Information", r"assumption"),
    ("Dependencies", r"dependenc"),
    ("Implementation Phase Candidates", r"phase candidate|implementation phase"),
    ("Phase Boundaries", r"phase boundar"),
    ("Verification Specification", r"verification"),
    ("Paper to Implementation Traceability", r"traceability"),
    ("Reproducibility and Implementation Gap Matrix", r"gap"),
    ("Risks", r"\brisks?\b"),
    ("Weaknesses and Limitations", r"weakness|limitation"),
    ("Improvement Recommendations", r"improvement|recommendation"),
    ("Engineering Implementation Guidance", r"guidance"),
    ("Proposed Repository Structure", r"repository|folder structure"),
    ("Documentation Requirements", r"documentation"),
    ("Final Technical Assessment", r"final (technical )?assessment"),
    ("GSD Handoff", r"handoff"),
]
HANDOFF_BLOCKS = ["project objective", "core requirements", "critical decisions", "critical assumptions",
                  "critical dependencies", "critical risks", "required experiments", "required metrics",
                  "proposed implementation phases", "major unknowns"]
CLASS = re.compile(r"(?i)paper-specified|engineering inference|approximation|not implementable|\[[ABCD]\]"
                   r"|\bclass(?:ification)?\b\s*[:=|]?\s*\**[ABCD]\b|^\|.*\|\s*\**[ABCD]\b")
EVIDENCE = re.compile(r"(?i)\u00a7|\bsec(?:tion)?\.?\s*[IVX\d]|\beqs?\.|\bequation|\btable\b|\bfig|\balg|\bL\d+"
                      r"|\bappendix|\bevidence\b|\babstract\b|\bcaption\b")
RESULT_LABELS = re.compile(r"(?i)reported in (the )?paper|not verified|locally reproduced|smoke-test demonstrated"
                           r"|reports no (measured )?results|no results")
META = re.compile(r"(?i)^\s*(here is|here's|below is|i have (written|produced|created))\b")
UNFILLED = re.compile(rf"^\s*[-*\u2022]?\s*{ID}:\s*(\.\.\.|\u2026|TBD)?\s*$|\[insert|<fill|\bFILL\b")


class Report:
    def __init__(self) -> None:
        self.items: list[tuple[str, str, int, str]] = []

    def add(self, level: str, code: str, msg: str, line: int = 0) -> None:
        self.items.append((level, code, line, msg))

    def errors(self) -> int:
        return sum(1 for i in self.items if i[0] == ERR)


def prose(lines: list[str]) -> list[tuple[int, str]]:
    """Lines outside code fences, without inline code, math, or blockquoted (quoted paper) text."""
    out, fence = [], False
    for n, line in enumerate(lines, 1):
        if re.match(r"\s*(```|~~~)", line):
            fence = not fence
            continue
        if fence or line.lstrip().startswith(">"):
            continue
        line = re.sub(r"\$\$.*?\$\$|\$[^$]*\$|`[^`]*`|&#?\w+;", "", line)
        out.append((n, line))
    return out


def headings(lines: list[str]) -> list[tuple[int, int, str]]:
    return [(n, len(m.group(1)), m.group(2).strip().lower()) for n, line in prose(lines)
            if (m := re.match(r"^(#{1,6})\s+(.*)", line))]


def section_text(lines: list[str], hs: list[tuple[int, int, str]], start: int, level: int) -> list[str]:
    end = next((n for n, lv, _ in hs if n > start and lv <= level), len(lines) + 1)
    return lines[start:end - 1]


def check_structure(lines: list[str], r: Report) -> dict[str, tuple[int, int]]:
    """P01. Returns {section name: (line, level)} for the sections found."""
    hs = headings(lines)
    first = next((line for line in lines if line.strip()), "")
    if not first.startswith("# "):
        r.add(ERR, "P10", "the document must open with the project title as a '# ' heading", 1)
    if META.search(first) or any(META.search(line) for line in lines[:3]):
        r.add(ERR, "P10", "meta-commentary before the report (prompt section 39 forbids it)", 1)
    anchor = next(((n, lv) for n, lv, t in hs if re.search(SECTIONS[0][1], t)), None)
    if anchor is None:
        r.add(ERR, "P01", "no 'Executive Technical Summary' heading, cannot locate the section-36 hierarchy")
        return {}
    level = anchor[1]
    top = [(n, t) for n, lv, t in hs if lv == level]
    found, pos = {}, 0
    for name, pat in SECTIONS:
        hit = next((i for i in range(pos, len(top)) if re.search(pat, top[i][1])), None)
        if hit is not None:
            found[name], pos = (top[hit][0], level), hit + 1
        elif any(re.search(pat, t) for _, t in top):
            r.add(WARN, "P01", f"section '{name}' is out of the section-36 order")
        else:
            r.add(ERR, "P01", f"section '{name}' is missing (expected a level-{level} heading)")
    return found


def check_ids(lines: list[str], r: Report, found: dict[str, tuple[int, int]]) -> None:
    text = "\n".join(lines)
    handoff = found.get("GSD Handoff")
    hs = headings(lines)
    hand_lines = section_text(lines, hs, handoff[0], handoff[1]) if handoff else []
    hand_start = handoff[0] if handoff else len(lines) + 1
    defined: dict[str, int] = {}
    in_handoff: set[str] = set()
    for n, line in enumerate(lines, 1):
        m = DEFINE.match(line)
        if not m:
            continue
        if hand_start <= n <= hand_start + len(hand_lines):
            in_handoff.add(m.group(1))  # the handoff summarizes IDs, the body should define them
        else:
            defined.setdefault(m.group(1), n)
    cited = set(re.findall(ID, text))
    for fam in FAMILIES:
        if not any(i.startswith(fam + "-") for i in defined | dict.fromkeys(in_handoff)):
            level = ERR if fam == "REQ" else WARN
            r.add(level, "P02", f"no {fam}- identifiers defined (prompt section 4 requires stable IDs)")
    undefined = sorted(cited - set(defined) - in_handoff)
    if undefined:
        r.add(ERR, "P03", f"{len(undefined)} IDs cited but never defined: " + ", ".join(undefined[:25]))
    only_handoff = sorted(in_handoff - set(defined))
    if only_handoff:
        r.add(WARN, "P03", f"{len(only_handoff)} IDs are defined only in the GSD Handoff, define them in the body: "
              + ", ".join(only_handoff[:25]))
    if handoff:
        body = "\n".join(hand_lines).lower()
        for block in HANDOFF_BLOCKS:
            if block not in body:
                r.add(ERR, "P04", f"GSD Handoff has no '{block}' block", handoff[0])
        if "completion evidence" not in body:
            r.add(WARN, "P04", "GSD Handoff phases give no 'Completion evidence'", handoff[0])
    no_class, no_evid = [], []
    starts = sorted(defined.items(), key=lambda kv: kv[1])
    for k, (ident, n) in enumerate(starts):
        if not ident.startswith("REQ-"):
            continue
        stop = min(starts[k + 1][1] - 1 if k + 1 < len(starts) else len(lines), n + 10)
        window = "\n".join(lines[n - 1:stop])
        if not CLASS.search(window):
            no_class.append(ident)
        if not EVIDENCE.search(window):
            no_evid.append(ident)
    if no_class:
        r.add(WARN, "P05", f"{len(no_class)} REQ entries show no A/B/C/D classification: " + ", ".join(no_class[:20]))
    if no_evid:
        r.add(WARN, "P06", f"{len(no_evid)} REQ entries cite no paper evidence: " + ", ".join(no_evid[:20]))


def check_results(lines: list[str], r: Report, found: dict[str, tuple[int, int]]) -> None:
    res = found.get("Experimental Results")
    if res and not RESULT_LABELS.search("\n".join(section_text(lines, headings(lines), res[0], res[1]))):
        r.add(ERR, "P07", "results section never labels numbers REPORTED IN PAPER / NOT VERIFIED "
                          "(or states the paper reports no results)", res[0])


def roman(s: str) -> str:
    vals = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100}
    if not s or any(c not in vals for c in s):
        return s
    total = sum(-vals[a] if vals[a] < vals[b] else vals[a] for a, b in zip(s, s[1:])) + vals[s[-1]]
    return str(total)


def check_aux(lines: list[str], r: Report, aux: Path) -> None:
    kinds = {"tab": "Table", "table": "Table", "tbl": "Table", "fig": "Figure", "figure": "Figure",
             "eq": "Equation", "eqn": "Equation", "equation": "Equation", "alg": "Algorithm", "algo": "Algorithm"}
    have: dict[str, set[str]] = {}
    for label, num in re.findall(r"\\newlabel\{([^}]*)\}\{\{([^}]*)\}", aux.read_text(encoding="utf-8", errors="ignore")):
        kind = kinds.get(re.split(r"[:_-]", label)[0].lower())
        if kind and not label.endswith("@cref"):
            have.setdefault(kind, set()).add(roman(re.sub(r"[^\dIVXLC]", "", num) or num))
    pats = {"Table": r"\bTables?\s+([IVXLC]+|\d+)\b", "Figure": r"\bFig(?:ure|s?\.)?\s*([IVXLC]+|\d+)\b",
            "Equation": r"\bEq(?:uation|s?\.)\s*\(?(\d+)\)?", "Algorithm": r"\bAlgorithm\s+(\d+)\b"}
    for n, line in prose(lines):
        for kind, pat in pats.items():
            if kind not in have or re.search(r"(?i)\bof \[|\[\d+\]'s|\bin \[\d", line):
                continue  # unknown label scheme, or a table/figure of a cited work
            for num in re.findall(pat, line):
                if roman(num) not in have[kind]:
                    r.add(WARN, "P08", f"{kind} {num} is cited but the compiled paper has no such {kind.lower()}", n)


def check_style(lines: list[str], r: Report, style: bool) -> None:
    if style:
        p = prose(lines)
        dashes = [n for n, line in p if "\u2014" in line]
        semis = [n for n, line in p if ";" in line]
        if dashes or semis:
            r.add(ERR, "P09", f"{len(dashes)} lines with em dashes, {len(semis)} with semicolons in prose "
                              f"(first at lines {(dashes + semis)[:6]})")
    for n, line in prose(lines):
        if UNFILLED.search(line):
            r.add(ERR, "P10", "unfilled template line", n)
    if not any(re.match(r"\s*```mermaid", line) for line in lines):
        r.add(WARN, "P11", "no Mermaid diagram (prompt section 37 asks for them)")


def run(path: Path, aux: Path | None, style: bool) -> Report:
    lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    r = Report()
    found = check_structure(lines, r)
    check_ids(lines, r, found)
    check_results(lines, r, found)
    if aux is not None:
        check_aux(lines, r, aux)
    check_style(lines, r, style)
    return r


# ----------------------------------------------------------------------------- selftest

def clean_report() -> str:
    body = {
        "Requirements Specification": "**REQ-001. Gate.** Classification: [A]. Evidence: Section III, Eq. (1).\n\n"
                                      "| ID | Requirement | Class | Evidence |\n|---|---|---|---|\n"
                                      "| REQ-002 | Log decisions | [B] | Table 1 |\n",
        "Experimental Specification": "**EXP-001. Main run.** See REQ-001.\n\n**METRIC-001. Violation rate.**\n",
        "Experimental Results": "Accuracy 0.91 (REPORTED IN PAPER, NOT VERIFIED).\n",
        "Assumptions and Unknown Information": "| ID | Assumption |\n|---|---|\n| ASM-001 | Twin is a simulator |\n\n"
                                               "**DEC-001.** Pick the twin model.\n",
        "Dependencies": "- DEP-001: SUMO 1.20\n",
        "Risks": "- RISK-001: calibration drift\n",
        "System Architecture": "```mermaid\ngraph LR\nA-->B\n```\n",
        "GSD Handoff": "Project Objective\nBuild it.\n\nCore Requirements\n- REQ-001: gate\n\nCritical Decisions\n- DEC-001: twin\n\n"
                       "Critical Assumptions\n- ASM-001: sim\n\nCritical Dependencies\n- DEP-001: SUMO\n\n"
                       "Critical Risks\n- RISK-001: drift\n\nRequired Experiments\n- EXP-001: main\n\n"
                       "Required Metrics\n- METRIC-001: rate\n\nProposed Implementation Phases\nPhase 1\n"
                       "Completion evidence: tests pass.\n\nMajor Unknowns\n- twin model\n",
    }
    out = ["# Demo Project", ""]
    for name, _ in SECTIONS:
        out += [f"# {name}", "", body.get(name, "Text."), ""]
    return "\n".join(out)


AUX = "\\newlabel{tab:main}{{1}{3}}\n\\newlabel{eq:gate}{{1}{2}}\n\\newlabel{fig:arch}{{1}{1}}\n"
FAULTS: dict[str, tuple[str, list[tuple[str, str]]]] = {  # code -> (level, [(old, new)] edits to the clean report)
    "P01": (ERR, [("# Phase Boundaries", "# Phase Plan")]),
    "P02": (ERR, [("REQ-001", "R1"), ("REQ-002", "R2")]),
    "P03": (ERR, [("See REQ-001.", "See REQ-077.")]),
    "P03w": (WARN, [("**METRIC-001. Violation rate.**", "Metric: violation rate.")]),
    "P04": (ERR, [("Major Unknowns\n", "Open items\n")]),
    "P05": (WARN, [("| REQ-002 | Log decisions | [B] |", "| REQ-002 | Log decisions | |")]),
    "P06": (WARN, [("| REQ-002 | Log decisions | [B] | Table 1 |", "| REQ-002 | Log decisions | [B] | |")]),
    "P07": (ERR, [("(REPORTED IN PAPER, NOT VERIFIED)", "(measured)")]),
    "P08": (WARN, [("Table 1 |", "Table 4 |")]),
    "P09": (ERR, [("Build it.", "Build it \u2014 fast; now.")]),
    "P10": (ERR, [("# Demo Project", "Here is the report.\n\n# Demo Project")]),
    "P11": (WARN, [("```mermaid\ngraph LR\nA-->B\n```\n", "")]),
}


def selftest() -> int:
    fails = 0
    with tempfile.TemporaryDirectory() as tmp:
        aux = Path(tmp) / "paper.aux"
        aux.write_text(AUX, encoding="utf-8")
        rep = Path(tmp) / "PROJECT_REPORT.md"
        rep.write_text(clean_report(), encoding="utf-8")
        clean = run(rep, aux, True)
        if clean.items:
            fails += 1
            print("FAIL clean report produced findings:", *clean.items, sep="\n  ")
        for code, (level, edits) in FAULTS.items():
            text = clean_report()
            for old, new in edits:
                assert old in text, (code, old)
                text = text.replace(old, new)
            rep.write_text(text, encoding="utf-8")
            got = [i for i in run(rep, aux, True).items if i[1] == code[:3] and i[0] == level]
            print(("ok  " if got else "FAIL") + f" {code} {level} " + (got[0][3] if got else "not detected"))
            fails += not got
    print(f"selftest: {len(FAULTS) + 1 - fails}/{len(FAULTS) + 1} passed")
    return 1 if fails else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("report", nargs="?", default="PROJECT_REPORT.md")
    ap.add_argument("--aux", type=Path, help="compiled .aux of the paper, enables the P08 number check")
    ap.add_argument("--style", action="store_true", help="opt in to the em-dash and semicolon prose check")
    ap.add_argument("--no-style", action="store_true", help="skip the prose style check (the default; kept for old commands)")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    path = Path(a.report)
    if not path.is_file():
        print(f"check_report: {path} not found")
        return 2
    rep = run(path, a.aux, a.style and not a.no_style)
    for level, code, line, msg in sorted(rep.items, key=lambda i: (i[0] != ERR, i[1], i[2])):
        print(f"{level:5} {code}{f' L{line}' if line else ''}: {msg}")
    print(f"check_report: {rep.errors()} errors, {len(rep.items) - rep.errors()} warnings")
    return 1 if rep.errors() else 0


if __name__ == "__main__":
    sys.exit(main())
