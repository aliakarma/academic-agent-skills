#!/usr/bin/env python3
"""Compare surface-pattern counts between the pre-repair and repaired manuscript.

Usage: python -I count_patterns.py <before.tex> <after.tex>

Counts running prose only: `%` comment lines, table rows (lines with `&`), and
everything from \\begin{thebibliography} or \\bibliography on are skipped.
A repair must not raise a guarded count. Exit code 1 if one rose.
"""
import re
import sys

# name -> (regex, guarded: a repair must not raise it)
PATTERNS = {
    # one group: swapping "thus" for "therefore" is not inflation
    "therefore/thus/hence": (r"\b(therefore|thus|hence)\b", True),
    "however": (r"\bhowever\b", True),
    "moreover/furthermore": (r"\b(moreover|furthermore)\b", True),
    "notably/importantly/crucially": (r"\b(notably|importantly|crucially)\b", True),
    "consequently/nevertheless": (r"\b(consequently|nevertheless)\b", True),
    "it is important to note": (r"it is (important|worth) (to note|noting)", True),
    "highlights/underscores": (r"\b(highlights?|underscores?)\b", True),
    "valuable/crucial/robust": (r"\b(valuable|crucial|robust(ly)?)\b", True),
    "contractions": (r"\b\w+n't\b|\b(it|that|there)'s\b", True),
    "unicode quotes": (r"[\u201c\u201d\u2018\u2019]", True),
    "straight double quotes": (r'"', True),
    "em dashes": (r"\u2014|---", True),
    "prose semicolons": (r";", True),
    "sentence-initial This/These": (r"(?:^|[.!?]\s+)(This|These)\s", False),
    "demonstrate/prove/guarantee": (r"\b(demonstrat\w*|prov(e|es|ed|en)|guarantee\w*)\b", False),
}


def prose(path):
    out = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            if re.search(r"\\begin\{thebibliography\}|\\bibliography\{", line):
                break
            s = line.strip()
            if s.startswith("%") or "&" in s:
                continue
            out.append(re.sub(r"(?<!\\)%.*", "", line))
    return "".join(out)


def counts(text):
    return {k: len(re.findall(p, text, re.I | re.M)) for k, (p, _) in PATTERNS.items()}


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    a, b = counts(prose(sys.argv[1])), counts(prose(sys.argv[2]))
    rose = []
    print(f"{'pattern':34} {'before':>7} {'after':>7}")
    for k, (_, guard) in PATTERNS.items():
        flag = ""
        if guard and b[k] > a[k]:
            flag = "  ROSE"
            rose.append(k)
        print(f"{k:34} {a[k]:>7} {b[k]:>7}{flag}")
    print(f"{len(rose)} guarded patterns rose" + (f": {', '.join(rose)}" if rose else ""))
    sys.exit(1 if rose else 0)


if __name__ == "__main__":
    main()
