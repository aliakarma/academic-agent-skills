#!/usr/bin/env python3
"""Check a reference-verify response against the skill's required structure.

Usage:
  python check_response.py response.md [--key originalKey]
  python check_response.py --selftest
Exit 0 = no errors (warnings may print), 1 = errors found.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from fetch_metadata import parse_bibtex  # noqa: E402

HEADS = ["Verification status:", "Source(s) checked:", "Corrections made:",
         "Final verified BibTeX:", "Notes:"]
STATUSES = ("Verified", "Partially verified", "Not verified")
PLACEHOLDER = re.compile(r"^\s*(unverified|unknown|todo|tbd|xxx+|\?+|n/?a|none|-+|\.\.\.)?\s*$|"
                         r"\b(unverified|todo|tbd|placeholder)\b", re.I)


def blocks(text):
    """Split into one chunk per reference (each starts at a status heading)."""
    idx = [m.start() for m in re.finditer(r"\*\*Verification status:\*\*", text)]
    return [text[a:b] for a, b in zip(idx, idx[1:] + [len(text)])]


def check_block(b, n, key=None):
    errs, warns = [], []
    pos = [b.find(f"**{h}**") for h in HEADS]
    for h, p in zip(HEADS, pos):
        if p < 0:
            errs.append(f"ref {n}: missing heading **{h}**")
    found = [p for p in pos if p >= 0]
    if found != sorted(found):
        errs.append(f"ref {n}: headings out of order")
    if errs:
        return errs, warns

    def section(i):
        end = pos[i + 1] if i + 1 < len(pos) else len(b)
        return b[pos[i] + len(HEADS[i]) + 4:end].strip()

    status = section(0).splitlines()[0].strip().strip("*").strip() if section(0) else ""
    if status not in STATUSES:
        errs.append(f"ref {n}: status must be exactly one of {STATUSES}, got {status!r}")
    if not re.search(r"https?://\S+", section(1)):
        errs.append(f"ref {n}: Source(s) checked lists no link")
    if not section(2):
        errs.append(f"ref {n}: Corrections made is empty (write None if nothing changed)")

    code = re.findall(r"```bibtex\s*\n(.*?)```", section(3), re.S)
    if status == "Not verified":
        if code:
            errs.append(f"ref {n}: Not verified must not carry a BibTeX block")
        elif not section(3):
            errs.append(f"ref {n}: Not verified needs a statement under the BibTeX heading")
    elif status in STATUSES:
        if len(code) != 1:
            errs.append(f"ref {n}: expected exactly one ```bibtex block, found {len(code)}")
        else:
            try:
                etype, k, fields = parse_bibtex(code[0])
                if not k:
                    errs.append(f"ref {n}: BibTeX entry has no citation key")
                if key and k != key:
                    errs.append(f"ref {n}: citation key changed ({key} -> {k})")
                for f, v in fields.items():
                    if PLACEHOLDER.search(v):
                        errs.append(f"ref {n}: field {f} holds a placeholder or empty value: {v!r}")
                if code[0].count("@") > 1 and re.search(r"^\s*@\w+\s*\{", code[0].split("\n", 1)[1], re.M):
                    errs.append(f"ref {n}: more than one entry in the BibTeX block")
                if "year" not in fields and "note" not in fields and "urldate" not in fields:
                    warns.append(f"ref {n}: no year and no access date (note/urldate)")
            except ValueError as e:
                errs.append(f"ref {n}: BibTeX does not parse: {e}")

    notes = section(4)
    if not notes:
        errs.append(f"ref {n}: Notes is empty")
    if status == "Partially verified" and not re.search(r"unverif|conflict|could not|not (be )?confirm",
                                                          notes, re.I):
        warns.append(f"ref {n}: Partially verified but Notes names no unverified or conflicting field")
    if status == "Verified" and re.search(r"\*\*unverified\*\*|could not be (independently )?verified",
                                          notes, re.I):
        warns.append(f"ref {n}: Verified but Notes reports unverified fields (should it be Partially verified?)")
    return errs, warns


def check(text, key=None):
    bs = blocks(text)
    if not bs:
        return ["no **Verification status:** heading found"], []
    errs, warns = [], []
    for i, b in enumerate(bs, 1):
        e, w = check_block(b, i, key if len(bs) == 1 else None)
        errs += e; warns += w
    return errs, warns


GOOD = """**Verification status:** Verified

**Source(s) checked:** Crossref record https://api.crossref.org/works/10.1/x

**Corrections made:** None

**Final verified BibTeX:**

```bibtex
@article{doe2020,
  author = {Doe, Jane},
  title = {A Title},
  journal = {J. Test},
  year = {2020},
  doi = {10.1/x}
}
```

**Notes:** Crossref and the publisher page agree on every field.
"""


def selftest():
    assert check(GOOD, "doe2020") == ([], []), check(GOOD, "doe2020")
    e, _ = check(GOOD, "other")
    assert any("key changed" in x for x in e), e
    e, _ = check(GOOD.replace("{2020}", "{unverified}"))
    assert any("placeholder" in x for x in e), e
    e, _ = check(GOOD.replace("Verified\n", "Not verified\n", 1))
    assert any("must not carry" in x for x in e), e
    e, _ = check(GOOD.replace("**Notes:**", "**Note:**"))
    assert any("missing heading" in x for x in e), e
    e, _ = check(GOOD.replace("https://api.crossref.org/works/10.1/x", "Crossref"))
    assert any("no link" in x for x in e), e
    e, _ = check(GOOD.replace("{A Title}", "{A Title"))
    assert any("does not parse" in x for x in e), e
    _, w = check(GOOD.replace("Verified\n", "Partially verified\n", 1))
    assert any("names no unverified" in x for x in w), w
    two = GOOD + "\n" + GOOD.replace("doe2020", "roe2021")
    assert check(two) == ([], []), check(two)
    print("selftest: all checks passed")
    return 0


def main(argv):
    if "--selftest" in argv:
        return selftest()
    if len(argv) < 2:
        print(__doc__); return 2
    key = argv[argv.index("--key") + 1] if "--key" in argv else None
    errs, warns = check(Path(argv[1]).read_text(encoding="utf-8"), key)
    for w in warns:
        print("WARN ", w)
    for e in errs:
        print("ERROR", e)
    print(f"{len(errs)} error(s), {len(warns)} warning(s)")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
