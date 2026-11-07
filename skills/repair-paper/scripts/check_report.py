#!/usr/bin/env python3
"""Check a repair report against the audit it answers.

Usage: python -I check_report.py <audit.md> <REPAIR_REPORT.md>
       python -I check_report.py --selftest

Checks: sections A-F present and in order, every audit ID appears exactly once
in the Section B matrix with a valid status, no matrix ID missing from the audit,
MERGED rows name an existing target, and the Section A counts match the matrix.
Prints one line per problem and "N problems". Exit code 1 if any problem.
"""
import re
import sys

ID = re.compile(r"\bI-\d{3,}\b")
SECTIONS = ["A", "B", "C", "D", "E", "F"]


def audit_ids(text):
    # Issue headings and master-index rows are the two forms audit-paper writes.
    heads = re.findall(r"\*\*Issue (I-\d{3,})\*\*", text)
    rows = re.findall(r"^\|\s*(I-\d{3,})\s*\|", text, re.M)
    return set(heads) | set(rows)


def status_of(cell):
    c = cell.upper()
    if "MERGED" in c:
        return "MERGED"
    if "NOT APPLICABLE" in c:
        return "NOT APPLICABLE"
    if "UNSUPPORTED" in c:
        return "UNSUPPORTED"
    if "AUTHOR INPUT" in c:
        return "AUTHOR INPUT"
    if "FIXED" in c and "NOT FIXED" not in c:
        return "FIXED"
    return None


def split_sections(text):
    marks = [(m.start(), m.group(1)) for m in
             re.finditer(r"^#{1,4}\s*([A-F])\.\s", text, re.M)]
    found = [s for _, s in marks]
    body = {}
    for i, (pos, s) in enumerate(marks):
        end = marks[i + 1][0] if i + 1 < len(marks) else len(text)
        body.setdefault(s, text[pos:end])
    return found, body


def check(audit_text, report_text):
    problems = []
    found, body = split_sections(report_text)
    if [s for s in found if s in SECTIONS] != SECTIONS:
        problems.append(f"sections A-F missing or out of order: found {found}")

    expected = audit_ids(audit_text)
    if not expected:
        problems.append("no audit IDs found in the audit file")

    rows = {}
    for line in body.get("B", "").splitlines():
        m = re.match(r"^\|\s*(I-\d{3,})\s*\|([^|]*)\|", line)
        if not m:
            continue
        iid, cell = m.group(1), m.group(2)
        if iid in rows:
            problems.append(f"{iid} appears twice in the matrix")
        st = status_of(cell)
        if st is None:
            problems.append(f"{iid} has no valid status: '{cell.strip()}'")
        if st == "MERGED":
            target = ID.search(cell)
            if not target or target.group(0) not in expected:
                problems.append(f"{iid} is MERGED but names no existing target")
        rows[iid] = st

    for iid in sorted(expected - set(rows)):
        problems.append(f"{iid} is in the audit but missing from the matrix")
    for iid in sorted(set(rows) - expected):
        problems.append(f"{iid} is in the matrix but not in the audit")

    # Section A counts, checked only when the report states them as numbers.
    a = body.get("A", "")
    tally = {}
    for st in rows.values():
        tally[st] = tally.get(st, 0) + 1
    claims = {
        "identified": (r"identified\D{0,20}?(\d+)", len(expected)),
        "fixed": (r"\|\s*Fixed\s*\|\s*(\d+)|\bFixed\b\D{0,10}?(\d+)", tally.get("FIXED", 0)),
        "merged": (r"\bMerged\b[^|\n]*\|\s*(\d+)|\bMerged\b\D{0,10}?(\d+)", tally.get("MERGED", 0)),
    }
    for name, (pat, actual) in claims.items():
        m = re.search(pat, a, re.I)
        if m:
            stated = int(next(g for g in m.groups() if g))
            if stated != actual:
                problems.append(f"Section A says {stated} {name}, matrix has {actual}")
    return problems


def _selftest():
    audit = "**Issue I-001**\n**Issue I-002**\n| I-001 | x |\n| I-002 | x |\n| I-003 | x |\n"
    good = ("## A. Repair\n| Audit issues identified | 3 |\n| Fixed | 2 |\n| Merged into another fix | 1 |\n"
            "## B. Matrix\n| ID | Status |\n|---|---|\n| I-001 | FIXED | s | x |\n"
            "| I-002 | MERGED (I-001) | s | x |\n| I-003 | FIXED | s | x |\n"
            "## C. x\n## D. x\n## E. x\n## F. x\n")
    assert check(audit, good) == [], check(audit, good)
    bad = good.replace("| I-003 | FIXED | s | x |\n", "| I-002 | maybe | s | x |\n").replace("## E. x\n", "")
    msgs = check(audit, bad)
    for needle in ("out of order", "twice", "no valid status", "I-003 is in the audit", "says 2 fixed"):
        assert any(needle in m for m in msgs), (needle, msgs)
    print("selftest ok")


if __name__ == "__main__":
    if sys.argv[1:] == ["--selftest"]:
        _selftest()
        sys.exit(0)
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    with open(sys.argv[1], encoding="utf-8") as f:
        audit_text = f.read()
    with open(sys.argv[2], encoding="utf-8") as f:
        report_text = f.read()
    probs = check(audit_text, report_text)
    for p in probs:
        print(p)
    print(f"{len(probs)} problems")
    sys.exit(1 if probs else 0)
