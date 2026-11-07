#!/usr/bin/env python3
"""Comment-by-comment completeness and structure check for a response letter.

Inputs
  inventory.tsv   one reviewer item per line, in report order:
                      R1-00<TAB>General assessment
                      R1-01<TAB>Operating conditions and the UF/RO choice
                      R2-03a<TAB>Sub-comment (a) of comment 3
                  Lines starting with # are ignored. Build it from the
                  reviewer file BEFORE drafting (SKILL.md step 1).
  letter.tex      written with templates/response_template.tex

Checks
  1. every inventory ID has exactly one reviewercomment box, in the same order,
     and the letter has no IDs that are not in the inventory;
  2. each box is followed by \\response, \\actiontaken and a location box
     before the next box;
  3. the completeness index links every ID (\\rref{ID} ... \\pageref{c:ID});
  4. author prose outside verbatim boxes, quotations and lists has no
     semicolons or em dashes (STRICT house style) and no common British
     spellings. These are reported for review, not failed.

Usage:
    python check_completeness.py inventory.tsv response_to_reviewers.tex

Exit status 0 means checks 1-3 passed.
"""
import argparse
import re
import sys

BS = "\\"
# "analyses" (plural noun), "optimistic", "characteristics" are American English and must not match
BRITISH = re.compile(
    r"\b(modell(?:ed|ing|er)s?|behaviour\w*|colour\w*|analys(?:e|ed|ing)|"
    r"(?:optimi|utili|organi|characteri|summari|normali|minimi|maximi|recogni|emphasi)s(?:e|ed|es|ing|ation|ations)|"
    r"centre[sd]?|metre[s]?|litre[s]?|fibre[s]?|programme[s]?|labelled|travelled|whilst|amongst|ageing)\b",
    re.I,
)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("inventory")
    ap.add_argument("letter")
    a = ap.parse_args()

    inv = []
    for line in open(a.inventory, encoding="utf-8"):
        line = line.strip()
        if line and not line.startswith("#"):
            inv.append(line.split("\t")[0].strip())

    raw = open(a.letter, encoding="utf-8").read()
    tex = re.sub(r"(?m)(?<!\\)%.*$", "", raw)
    body = tex[tex.find(BS + "begin{document}"):]

    box = re.compile(re.escape(BS + "begin{reviewercomment}") + r"\{([^}]*)\}")
    found = [(m.group(1), m.start()) for m in box.finditer(body)]
    ids = [i for i, _ in found]
    problems = 0

    # 1. coverage and order
    missing = [i for i in inv if i not in ids]
    extra = [i for i in ids if i not in inv]
    dups = sorted({i for i in ids if ids.count(i) > 1})
    for label, items in (("MISSING from letter", missing), ("NOT in inventory", extra), ("DUPLICATE", dups)):
        if items:
            problems += len(items)
            print(f"{label}: {', '.join(items)}")
    common = [i for i in ids if i in inv]
    if common != [i for i in inv if i in ids]:
        problems += 1
        print("ORDER differs from the inventory:\n  letter:    " + " ".join(common))

    # 2. per-item structure
    ends = [pos for _, pos in found[1:]] + [len(body)]
    for (cid, start), end in zip(found, ends):
        chunk = body[start:end]
        for need, what in ((BS + "response", "Response"), (BS + "actiontaken", "Action taken"),
                           (BS + "begin{location}", "Location box")):
            if need not in chunk:
                problems += 1
                print(f"{cid}: no {what}")

    # 3. completeness index
    for cid in inv:
        linked = any((BS + cmd + "{" + cid + "}") in body for cmd in ("rref", "cref"))  # cref: older letters
        if not linked or (BS + "pageref{c:" + cid + "}") not in body:
            problems += 1
            print(f"{cid}: missing from the completeness index")

    # 4. prose style (report only)
    prose = body
    for env in ("reviewercomment", "location", "longtable", "tabularx"):
        prose = re.sub(re.escape(BS + "begin{" + env + "}") + r".*?" + re.escape(BS + "end{" + env + "}"),
                       " ", prose, flags=re.S)
    prose = re.sub(r"``.*?''", " ", prose, flags=re.S)        # quotations stay verbatim
    prose = re.sub(r"\$[^$]*\$", " ", prose)                  # math
    style = []
    for line in prose.splitlines():
        s = line.strip()
        if s.startswith(BS + "item") or "Location:" in s:
            continue                                          # list and location separators are allowed
        if ";" in s or re.search(r"(?<!-)---(?!-)|—", s):
            style.append(f"  punctuation: {s[:110]}")
        for m in BRITISH.finditer(s):
            style.append(f"  spelling '{m.group(0)}': {s[:90]}")
    print(f"{len(inv)} inventory items, {len(ids)} comment boxes, {problems} structural problems")
    if style:
        print(f"{len(style)} prose style notes (review each; verbatim quotes are exempt):")
        print("\n".join(style))
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
