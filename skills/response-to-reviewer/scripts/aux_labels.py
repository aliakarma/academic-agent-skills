#!/usr/bin/env python3
"""Print every LaTeX label of the compiled revised manuscript with its number
and page, from the .aux file. Use it to cite section, equation, figure, table
and appendix numbers and float pages exactly as they appear in the PDF.

Usage:
    python aux_labels.py main.aux [--grep tab:]

Output columns: label, printed number, page. cleveref (@cref) duplicates are
skipped. Recompile the manuscript first if main.aux is older than main.tex.
"""
import argparse
import re

LABEL = re.compile(r"\\newlabel\{([^}]+)\}\{\{([^}]*)\}\{([^}]*)\}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("aux")
    ap.add_argument("--grep", default="", help="only labels containing this text")
    a = ap.parse_args()
    for m in LABEL.finditer(open(a.aux, encoding="utf-8", errors="replace").read()):
        key, num, page = m.groups()
        if key.endswith("@cref") or a.grep not in key:
            continue
        print(f"{key:<32} {num:<8} p.{page}")


if __name__ == "__main__":
    main()
