#!/usr/bin/env python3
"""List numbers in the author-written parts of a response letter that do not
occur in the revised manuscript or its supplementary sources.

Every quantitative claim in a response must be traceable to the revised
files. This script extracts decimals (0.981, 12.4) and integers with four or
more digits (1440, 726000) from the letter, skipping the preamble, LaTeX
comments, the verbatim reviewer-comment boxes and the location boxes, and
looks each one up in the source files given (thousands separators and
LaTeX `{,}` are normalized away).

Usage:
    python check_numbers.py response_to_reviewers.tex main.tex main_idx.txt [results.json ...]
        [--skip-env reviewercomment --skip-env location]

Each reported number must then be checked by hand. Legitimate misses are
rounded values (0.43 for a reported 0.426), values from the ORIGINAL
submission (which must carry a "% AUTHOR CHECK" comment), and layout
constants. Anything else is an unsupported number: fix or remove it.
"""
import argparse
import re

BS = "\\"


def strip_env(tex, env):
    pat = re.escape(BS + "begin{" + env + "}") + r".*?" + re.escape(BS + "end{" + env + "}")
    return re.sub(pat, " ", tex, flags=re.S)


def normalize(s):
    return s.replace("{,}", "").replace(",", "")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("letter")
    ap.add_argument("sources", nargs="+", help="manuscript .tex, PDF index, supplementary/results files")
    ap.add_argument("--skip-env", action="append", default=None,
                    help="environment to ignore (default: reviewercomment, location)")
    a = ap.parse_args()
    envs = a.skip_env or ["reviewercomment", "location"]

    tex = open(a.letter, encoding="utf-8").read()
    start = tex.find(BS + "begin{document}")
    tex = tex[start:] if start >= 0 else tex
    tex = re.sub(r"(?m)(?<!\\)%.*$", "", tex)
    for env in envs:
        tex = strip_env(tex, env)
    tex = re.sub(r"\d*\.\d+" + re.escape(BS) + r"(?:text|line|column)width", " ", tex)
    tex = normalize(tex)

    corpus = ""
    for path in a.sources:
        with open(path, encoding="utf-8", errors="replace") as fh:
            corpus += normalize(fh.read()) + "\n"

    def present(x):
        # whole-number match: 0.592 must not hit 0.5923, 1440 must not hit 14400
        return re.search(r"(?<![\d.])" + re.escape(x) + r"(?![\d])", corpus) is not None

    nums = set(re.findall(r"(?<![\d.])\d+\.\d+(?!\d)|(?<![\d.])\d{4,}(?![\d.])", tex))
    missing, scaled = [], []
    for x in sorted(nums, key=float):
        if present(x):
            continue
        # 556000 USD in the letter vs 556 kUSD in a table
        if "." not in x and x.endswith("000") and present(x[:-3]):
            scaled.append(x)
        else:
            missing.append(x)

    def show(x):
        ctx = re.search(r".{0,60}" + re.escape(x) + r".{0,40}", tex)
        print(f"  {x:>10}   ...{ctx.group(0).strip() if ctx else ''}...")

    print(f"{len(nums)} distinct numbers in author text; {len(missing)} not found in sources:")
    for x in missing:
        show(x)
    if scaled:
        print(f"{len(scaled)} found only as thousands (confirm the unit, e.g. kUSD):")
        for x in scaled:
            show(x)


if __name__ == "__main__":
    main()
