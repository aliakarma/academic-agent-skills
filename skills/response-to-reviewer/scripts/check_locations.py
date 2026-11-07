#!/usr/bin/env python3
"""Validate every page/line citation in a response letter against the PDF index.

Finds citations such as
    p.~21, ll.~699--739      pp.~3--4, ll.~122--151      p.~16, l.~575
    p. 21, ll. 699–739       p.~1, ll.~4 and~17
in the letter (LaTeX comments are ignored) and checks that every cited line
number is printed as a body line on one of the cited pages of the revised
manuscript (index from build_line_index.py).

Usage:
    python check_locations.py main_idx.txt response_to_reviewers.tex [--show]

--show prints the text of the first cited line of each citation so quoted
passages and paragraph starts can be spot-checked by eye.

Exit status 0 means every citation matched.
"""
import argparse
import re
import sys

DASH = r"(?:--|–|-)"
SP = r"[~\s]*"
CITE = re.compile(
    rf"pp?\.{SP}(\d+)(?:{SP}{DASH}{SP}(\d+))?,{SP}ll?\.{SP}(\d+)(?:{SP}{DASH}{SP}(\d+))?"
    rf"((?:{SP}and{SP}\d+(?:{SP}{DASH}{SP}\d+)?)*)"
)
EXTRA = re.compile(rf"and{SP}(\d+)(?:{SP}{DASH}{SP}(\d+))?")
ROW = re.compile(r"^(\d+)\.(\d+): (.*)$")


def load_index(path):
    pages, text = {}, {}
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            m = ROW.match(line.rstrip("\n"))
            if m:
                p, n = int(m.group(1)), int(m.group(2))
                pages.setdefault(p, set()).add(n)
                text.setdefault(n, m.group(3))
    return pages, text


def pages_of(line, pages):
    """Pages on which `line` is a body line (it has a numbered neighbor there)."""
    return [p for p, s in pages.items() if line in s and (line - 1 in s or line + 1 in s)]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("index")
    ap.add_argument("letter")
    ap.add_argument("--show", action="store_true")
    a = ap.parse_args()

    pages, text = load_index(a.index)
    tex = open(a.letter, encoding="utf-8").read()
    tex = re.sub(r"(?m)(?<!\\)%.*$", "", tex)

    n_cites = n_lines = bad = 0
    for m in CITE.finditer(tex):
        n_cites += 1
        p1 = int(m.group(1))
        p2 = int(m.group(2) or p1)
        spans = [(int(m.group(3)), int(m.group(4) or m.group(3)))]
        spans += [(int(x), int(y or x)) for x, y in EXTRA.findall(m.group(5) or "")]
        for lo, hi in spans:
            if hi < lo:
                bad += 1
                print(f"BAD RANGE  {m.group(0)!r}: {lo} > {hi}")
            for L in sorted({lo, hi}):
                n_lines += 1
                found = pages_of(L, pages)
                if not any(p1 <= p <= p2 for p in found):
                    bad += 1
                    print(f"MISMATCH   {m.group(0)!r}: line {L} is on page(s) {found or 'none'}")
        if a.show:
            first = spans[0][0]
            print(f"  {m.group(0)!r} -> l.{first}: {text.get(first, '?')[:110]}")

    print(f"{n_cites} citations, {n_lines} line endpoints checked, {bad} problems")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
