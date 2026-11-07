#!/usr/bin/env python3
"""Build a page.line index of a line-numbered manuscript PDF.

Journals in review mode (MDPI `submit`, Elsevier `review`, `lineno`, IEEE
draft) print continuous line numbers in the margin. This script extracts the
PDF text and writes one row per text line:

    <page>.<line>: <text>     body line carrying a margin line number
    <page>.-: <text>          anything else (tables, captions, headers)

The index is what check_locations.py validates "p. X, ll. Y-Z" against, and
it is the fastest way to read the whole revised manuscript with its real
page and line positions.

Usage:
    python build_line_index.py main.pdf [--out main_idx.txt] [--side auto|left|right]

Notes:
- Prefers `pdftotext -layout` (poppler). Falls back to PyMuPDF if poppler is
  missing; the fallback is less reliable for margin numbers.
- Text extraction drops many Greek letters and subscripts and scrambles table
  columns. Read equation and table content from the .tex source, not from
  this index.
"""
import argparse
import re
import shutil
import subprocess
import sys

RIGHT = re.compile(r"^(.*?\S)\s+(\d{1,5})\s*$")
LEFT = re.compile(r"^\s*(\d{1,5})\s+(\S.*)$")


def extract_pages(pdf):
    if shutil.which("pdftotext"):
        res = subprocess.run(["pdftotext", "-layout", pdf, "-"], capture_output=True)
        if res.returncode == 0:
            return res.stdout.decode("utf-8", "replace").split("\f")
        sys.stderr.write(res.stderr.decode("utf-8", "replace"))
    try:
        import pymupdf  # PyMuPDF >= 1.24
    except ImportError:
        try:
            import fitz as pymupdf
        except ImportError:
            sys.exit("Neither pdftotext nor PyMuPDF is available.")
    sys.stderr.write("warning: pdftotext not found, using PyMuPDF (margin numbers less reliable)\n")
    return [page.get_text() for page in pymupdf.open(pdf)]


def squeeze(s):
    return re.sub(r"\s{2,}", " ", s.strip())


def parse(pages, side):
    """Return (page, line_number_or_None, text) rows for one margin side."""
    rows = []
    for pno, text in enumerate(pages, 1):
        for raw in text.splitlines():
            if not raw.strip():
                continue
            if side == "right":
                m = RIGHT.match(raw)
                # short lines ending in a number are usually table cells or headers
                if m and len(raw.rstrip()) > 60:
                    rows.append((pno, int(m.group(2)), squeeze(m.group(1))))
                    continue
            else:
                m = LEFT.match(raw)
                if m:
                    rows.append((pno, int(m.group(1)), squeeze(m.group(2))))
                    continue
            rows.append((pno, None, squeeze(raw)))
    return rows


def score(rows):
    """Count numbered lines whose successor number appears on the same page."""
    seen = {}
    for p, n, _ in rows:
        if n is not None:
            seen.setdefault(p, set()).add(n)
    return sum(1 for s in seen.values() for n in s if n + 1 in s)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pdf")
    ap.add_argument("--out", default=None, help="output file (default: <pdf stem>_idx.txt)")
    ap.add_argument("--side", choices=["auto", "left", "right"], default="auto",
                    help="margin that carries the line numbers (auto tries both)")
    a = ap.parse_args()

    pages = extract_pages(a.pdf)
    if a.side == "auto":
        r, l = parse(pages, "right"), parse(pages, "left")
        rows, side = (r, "right") if score(r) >= score(l) else (l, "left")
    else:
        rows, side = parse(pages, a.side), a.side

    out = a.out or re.sub(r"\.pdf$", "", a.pdf, flags=re.I) + "_idx.txt"
    with open(out, "w", encoding="utf-8") as fh:
        for p, n, t in rows:
            fh.write(f"{p}.{n if n is not None else '-'}: {t}\n")

    numbered = sum(1 for _, n, _ in rows if n is not None)
    print(f"{out}: {len(pages)} pages, {len(rows)} rows, {numbered} numbered lines "
          f"({side} margin), consecutive-pair score {score(rows)}")
    if score(rows) < 20:
        print("warning: few consecutive line numbers found. The PDF may lack line numbers; "
              "cite sections, paragraphs, tables and figures instead of lines.")


if __name__ == "__main__":
    main()
