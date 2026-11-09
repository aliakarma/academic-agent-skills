#!/usr/bin/env python3
"""Completion gate for a reviewer-driven revision: may the run stop yet?

Reads the comment table in revision_audit.md. The table is the one whose header row has an
"ID" and a "Status" column (column order does not matter; keep one such table):

    | ID | Reviewer | Request | Location | Action and evidence | Status | Blocker |
    |---|---|---|---|---|---|---|
    | R1-01 | Reviewer 1 | "Compare with X." | Sec. 5.2, Table 4 | Ran revision_experiments/R1-01/run.py | ADDRESSED | |
    | R2-03a | Reviewer 2 | "Use field data." | Sec. 6.3 | Limitation added | BLOCKED | needs: field data from the authors |

IDs: ED-01 / E-01 / AE-01 (editor), R1-00 (general assessment), R1-01, R2-03a (sub-request).
Status: OPEN, IN PROGRESS, ADDRESSED or BLOCKED.

The run may stop only when every ID is
  ADDRESSED, with a non-empty cell in the column whose header contains "evidence" (if there is one), or
  BLOCKED, with a non-empty Blocker cell that says what the authors must supply,
and, with --letter, every ID appears in the response letter.

Usage:
    python check_audit.py revision_audit.md
    python check_audit.py revision_audit.md --letter response_to_reviewers.tex
    python check_audit.py revision_audit.md --tsv inventory.tsv   # inventory for response-to-reviewer

Exit status: 0 done, 1 work remains (the IDs are listed), 2 the table is missing or malformed.
"""
from __future__ import annotations

import argparse
import re
import sys

ID = re.compile(r"^(?:ED|E|AE|R\d+)-\d{2,}[a-z]?$")
STATUSES = ("OPEN", "IN PROGRESS", "ADDRESSED", "BLOCKED")
EMPTY = {"", "-", "--", "—", "none", "n/a", "na", "tbd", "todo"}


def cells(line: str) -> list[str]:
    return [c.strip() for c in re.split(r"(?<!\\)\|", line.strip().strip("|"))]


def read_rows(text: str) -> tuple[list[str], list[list[str]]]:
    """Header and data rows of the first table whose header has ID and Status columns."""
    header, rows = None, []
    for line in text.splitlines():
        if not line.lstrip().startswith("|"):
            if header:
                break
            continue
        row = cells(line)
        if header is None:
            if {"id", "status"} <= {c.lower() for c in row}:
                header = [c.lower() for c in row]
            continue
        if not all(re.fullmatch(r":?-{3,}:?", c) for c in row if c):  # skip the |---| separator
            rows.append(row)
    return header or [], rows


def check(text: str, letter: str | None = None) -> tuple[int, list[str], list[tuple[str, str]]]:
    header, rows = read_rows(text)
    if not header:
        return 2, ["no table with an 'ID' and a 'Status' column"], []
    col = {name: header.index(name) for name in header}
    evidence = next((i for i, name in enumerate(header) if "evidence" in name), None)
    blocker = next((i for i, name in enumerate(header) if "blocker" in name), None)
    request = next((i for i, name in enumerate(header) if "request" in name or "issue" in name), None)

    malformed, remaining, items, seen = [], [], [], set()
    for row in rows:
        row += [""] * (len(header) - len(row))
        cid, status = row[col["id"]].strip("`*"), row[col["status"]].strip("`*").upper()
        if not ID.match(cid):
            malformed.append(f"row ID '{cid}' is not of the form ED-01, R1-01 or R2-03a")
            continue
        if cid in seen:
            malformed.append(f"{cid}: duplicate row")
            continue
        seen.add(cid)
        items.append((cid, row[request] if request is not None else ""))
        if status not in STATUSES:
            malformed.append(f"{cid}: unknown status '{row[col['status']]}' (use {', '.join(STATUSES)})")
        elif status in ("OPEN", "IN PROGRESS"):
            remaining.append(f"{cid}: {status}")
        elif status == "ADDRESSED" and evidence is not None and row[evidence].lower() in EMPTY:
            remaining.append(f"{cid}: ADDRESSED but the evidence cell is empty")
        elif status == "BLOCKED" and (blocker is None or row[blocker].lower() in EMPTY):
            remaining.append(f"{cid}: BLOCKED without a stated blocker (what must the authors supply?)")
    if not items and not malformed:
        malformed.append("the table has no comment rows")
    if malformed:
        return 2, malformed, items
    if letter is not None:
        body = re.sub(r"(?m)(?<!\\)%.*$", "", letter)  # an ID in a LaTeX comment does not count
        remaining += [f"{cid}: not found in the response letter" for cid, _ in items
                      if not re.search(r"(?<![\w-])" + re.escape(cid) + r"(?![\w-])", body)]
    return (1 if remaining else 0), remaining, items


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("audit")
    ap.add_argument("--letter", help="response letter (.tex) that must mention every ID")
    ap.add_argument("--tsv", help="write ID<TAB>request lines, in table order, for response-to-reviewer")
    a = ap.parse_args(argv)
    try:
        text = open(a.audit, encoding="utf-8").read()
        letter = open(a.letter, encoding="utf-8").read() if a.letter else None
    except OSError as exc:
        print(f"cannot read: {exc}")
        return 2
    code, problems, items = check(text, letter)
    if a.tsv and code != 2:
        with open(a.tsv, "w", encoding="utf-8") as fh:
            fh.writelines(f"{cid}\t{' '.join(req.split())[:100]}\n" for cid, req in items)
    for p in problems:
        print(("MALFORMED " if code == 2 else "REMAINING ") + p)
    if code == 0:
        print(f"DONE: all {len(items)} comment IDs are ADDRESSED or BLOCKED with a stated blocker.")
    elif code == 1:
        open_ids = {p.split(":")[0] for p in problems}
        print(f"NOT DONE: {len(open_ids)} of {len(items)} comment IDs need more work. Keep going.")
    return code


if __name__ == "__main__":
    sys.exit(main())
