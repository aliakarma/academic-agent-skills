#!/usr/bin/env python3
"""Render literature/gap_matrix.csv as a booktabs LaTeX table.

CSV layout: first column source_id (a bib key, or THIS_WORK for the
manuscript's own row), then one column per comparison dimension. Cell
values yes / partial / no / n.r. (not reported) become symbols, anything
else is printed as escaped text.

  python gap_table.py literature/gap_matrix.csv \\
      --out literature/gap_matrix_out/tables.tex \\
      --caption "Comparison of representative studies" --label tab:gap

Needs \\usepackage{booktabs,amssymb} in the preamble. A legend line is
written under the table. Every cell must trace to an extraction_sheet row:
the script cannot check that, the reviewer must.
"""
import argparse
import csv
import os
import sys

SYMBOL = {"yes": r"\checkmark", "y": r"\checkmark", "partial": r"$\sim$",
          "p": r"$\sim$", "no": r"--", "n": r"--", "n.r.": r"n.r.", "nr": r"n.r."}


def esc(s):
    for a, b in (("\\", r"\textbackslash{}"), ("&", r"\&"), ("%", r"\%"),
                 ("#", r"\#"), ("_", r"\_"), ("$", r"\$")):
        s = s.replace(a, b)
    return s


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawTextHelpFormatter)
    ap.add_argument("csv")
    ap.add_argument("--out")
    ap.add_argument("--caption", default="Comparison of representative prior work.")
    ap.add_argument("--label", default="tab:gap-matrix")
    ap.add_argument("--cite", default="citet", help="cite command (default citet)")
    a = ap.parse_args()

    with open(a.csv, newline="", encoding="utf-8-sig") as fh:
        rows = list(csv.reader(fh))
    if len(rows) < 2:
        sys.exit("gap matrix needs a header and at least one row")
    header, body = rows[0], rows[1:]
    ncol = len(header)
    lines = [
        r"\begin{table*}[t]", r"\centering", r"\small",
        f"\\caption{{{a.caption}}}", f"\\label{{{a.label}}}",
        r"\begin{tabular}{l" + "c" * (ncol - 1) + "}", r"\toprule",
        "Study & " + " & ".join(esc(h) for h in header[1:]) + r" \\", r"\midrule",
    ]
    this_work = []
    for r in body:
        r = (r + [""] * ncol)[:ncol]
        sid = r[0].strip()
        cells = [SYMBOL.get(c.strip().lower(), esc(c.strip())) for c in r[1:]]
        if sid.upper() == "THIS_WORK":
            this_work = ["This work"] + cells
            continue
        lines.append(f"\\{a.cite}{{{sid}}} & " + " & ".join(cells) + r" \\")
    if this_work:
        lines += [r"\midrule", r"\textbf{" + this_work[0] + "} & "
                  + " & ".join(this_work[1:]) + r" \\"]
    lines += [r"\bottomrule", r"\end{tabular}",
              r"\\[2pt]{\footnotesize \checkmark\ addressed; $\sim$ partially "
              r"addressed; -- not addressed; n.r.\ not reported.}",
              r"\end{table*}"]
    text = "\n".join(lines) + "\n"
    if a.out:
        os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
        with open(a.out, "w", encoding="utf-8") as fh:
            fh.write(text)
        print(f"wrote {a.out}")
    else:
        print(text)


if __name__ == "__main__":
    main()
