#!/usr/bin/env python3
"""Create the literature/ research workspace without touching existing files.

  python init_workspace.py                 # creates ./literature
  python init_workspace.py --root path/to/project

Creates folders, CSV files with their canonical headers, and PROGRESS.md.
Anything that already exists is reported and left exactly as it is. If an
existing CSV has different columns, the script says so instead of fixing it.
"""
import argparse
import csv
import datetime
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import litlib  # noqa: E402

DIRS = ["raw/source_records", "raw/evidence_notes", "raw/verification",
        "gap_matrix_out"]

PROGRESS = """# Literature Review Progress

Manuscript: <path>
Active bibliography: <path>
Genre: <original research | survey | systematic review | theory | framework | other>
Started: {date}

Update this file at the end of every phase. After a context reset, read it
first and resume from the first phase whose gate is not met.

| Phase | Gate (exit condition) | Status | Notes |
|---|---|---|---|
| 0 Workspace | manuscript, bib, genre identified; baseline snapshot saved | open | |
| 1 Baseline diagnosis | existing citations machine-checked; baseline_diagnosis.md written | open | |
| 2 Scope and strategy | concept table and query plan in search_strategy.md | open | |
| 3 Search | stopping criteria met or limits documented | open | |
| 4 Screen | every candidate has a screening_decision | open | |
| 5 Verify | every included source VERIFIED or VERIFIED-QUALIFIED | open | |
| 6 Extract | extraction row + source record for every included source | open | |
| 7 Gap matrix | gaps.md with evidence per gap and calibrated wording | open | |
| 8 Citation map | citation_map.csv covers every planned insertion | open | |
| 9-10 Write and integrate | manuscript edited, original preserved | open | |
| 12 QA | all four audits pass or failures documented | open | |

## Open questions for the author

## Access limitations encountered
"""


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawTextHelpFormatter)
    ap.add_argument("--root", default=".", help="project folder (default: cwd)")
    a = ap.parse_args()
    base = os.path.join(os.path.abspath(a.root), "literature")
    created, kept = [], []

    for d in DIRS:
        p = os.path.normpath(os.path.join(base, d))
        (kept if os.path.isdir(p) else created).append(p + os.sep)
        os.makedirs(p, exist_ok=True)

    for name, cols in litlib.SCHEMAS.items():
        p = os.path.join(base, name)
        if os.path.exists(p):
            with open(p, newline="", encoding="utf-8-sig") as fh:
                header = next(csv.reader(fh), [])
            missing = [c for c in cols if c not in header]
            kept.append(p + (f"  (missing columns: {', '.join(missing)})" if missing else ""))
            continue
        with open(p, "w", newline="", encoding="utf-8") as fh:
            csv.writer(fh).writerow(cols)
        created.append(p)

    p = os.path.join(base, "PROGRESS.md")
    if os.path.exists(p):
        kept.append(p)
    else:
        with open(p, "w", encoding="utf-8") as fh:
            fh.write(PROGRESS.format(date=datetime.date.today().isoformat()))
        created.append(p)

    for p in created:
        print(f"created  {p}")
    for p in kept:
        print(f"kept     {p}")


if __name__ == "__main__":
    main()
