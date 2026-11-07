"""Structural checks for an audit.md produced by the audit-paper skill.

Usage: python check_audit.py path/to/audit.md
Exit 0 when every check passes, 1 otherwise. Prints one line per problem.
"""
import re
import sys

SECTIONS = [
    "Executive Diagnostic", "Coverage Verification", "Critical Issues",
    "High-Priority Issues", "Medium-Priority Issues", "Low-Priority Issues",
    "Recurring Manuscript-Wide Patterns", "AI-Rewrite Signature Analysis",
    "Authorial Voice Loss", "Scientific Reasoning Loss",
    "Section-by-Section Diagnosis", "Highest-Leverage Repair Plan",
    "Global Editing Rules", "Master Issue Index", "Completeness Check",
]
# issue-list section number -> severity it must hold
SEVERITY_OF_SECTION = {3: "Critical", 4: "High", 5: "Medium", 6: "Low"}
FIELDS = ["Location:", "Section:", "Severity:", "Priority:", "Category:", "Original passage:",
          "Problem:", "Why it matters:", "Underlying pattern:", "What to restore/check:", "Related issues:"]


def check(text):
    errors = []
    heads = [(m.start(), int(m.group(1)), m.group(2)) for m in
             re.finditer(r"^##\s+(\d+)\.\s+(.+)$", text, re.M)]
    # 1. required sections in order
    nums = [n for _, n, _ in heads]
    if nums != list(range(1, 16)):
        errors.append(f"section numbers are {nums}, expected 1..15 in order")
    for _, n, title in heads:
        if 1 <= n <= 15 and SECTIONS[n - 1].lower() not in title.lower():
            errors.append(f"section {n} titled '{title}', expected '{SECTIONS[n - 1]}'")

    def section_of(pos):
        cur = None
        for start, n, _ in heads:
            if start <= pos:
                cur = n
        return cur

    # 2. issue blocks: fields, severity, placement
    blocks = list(re.finditer(r"^\*\*Issue (I-\d+)\*\*$", text, re.M))
    body = {}
    for i, m in enumerate(blocks):
        iid = m.group(1)
        end = blocks[i + 1].start() if i + 1 < len(blocks) else len(text)
        chunk = text[m.start():end]
        if iid in body:
            errors.append(f"{iid} defined twice")
        sev = re.search(r"Severity:\s*(Critical|High|Medium|Low)", chunk)
        body[iid] = sev.group(1) if sev else None
        if not sev:
            errors.append(f"{iid} has no Severity")
        for f in FIELDS:
            if f not in chunk:
                errors.append(f"{iid} missing field '{f}'")
        want = SEVERITY_OF_SECTION.get(section_of(m.start()))
        if sev and want and sev.group(1) != want:
            errors.append(f"{iid} is {sev.group(1)} but sits in the {want} section")

    # 3. master index agrees with the body
    index = {}
    for m in re.finditer(r"^\|\s*(I-\d+)\s*\|(.+)\|\s*$", text, re.M):
        cells = [c.strip() for c in m.group(2).split("|")]
        sev = next((c for c in cells if c in ("Critical", "High", "Medium", "Low")), None)
        index[m.group(1)] = sev
    for iid in sorted(set(body) - set(index)):
        errors.append(f"{iid} defined but missing from the master index")
    for iid in sorted(set(index) - set(body)):
        errors.append(f"{iid} in the master index but never defined")
    for iid in sorted(set(body) & set(index)):
        if body[iid] != index[iid]:
            errors.append(f"{iid} severity {body[iid]} in body, {index[iid]} in index")

    # 4. every referenced ID exists
    for ref in sorted(set(re.findall(r"\bI-\d{3}\b", text)) - set(body)):
        errors.append(f"{ref} referenced but never defined")
    patterns = set(re.findall(r"^\*\*(P-\d+)\.", text, re.M))
    for ref in sorted(set(re.findall(r"\bP-\d{2}\b", text)) - patterns):
        errors.append(f"pattern {ref} referenced but never defined")

    # 5. stated totals match
    tot = re.search(r"Totals:\s*(\d+)\s*Critical,\s*(\d+)\s*High,\s*(\d+)\s*Medium,\s*(\d+)\s*Low", text)
    if tot:
        actual = [sum(1 for s in body.values() if s == k) for k in ("Critical", "High", "Medium", "Low")]
        if [int(x) for x in tot.groups()] != actual:
            errors.append(f"stated totals {list(map(int, tot.groups()))} but counted {actual}")
    return errors, body, patterns


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    text = open(sys.argv[1], encoding="utf-8").read().replace("\r\n", "\n")
    errors, body, patterns = check(text)
    for e in errors:
        print("FAIL:", e)
    counts = {k: sum(1 for s in body.values() if s == k) for k in ("Critical", "High", "Medium", "Low")}
    print(f"{len(body)} issues {counts}, {len(patterns)} patterns, {len(errors)} problems")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
