#!/usr/bin/env python3
"""Render review Sec. 15 and Sec. 16 reference lines from the ledger and bib records.

  python render_references.py --ledger literature/source_ledger.csv \
      --bib literature/references_corrected.bib literature/references_lit.bib references.bib \
      > literature/refs_rendered.md

Earlier --bib files win when a key appears in several, so put corrected
records first and the manuscript's own bib last. Typing reference lines by
hand is how metadata drifts from the verified record: paste these instead.

Sec. 15 gets every included source whose ledger status is VERIFIED or
VERIFIED-QUALIFIED (qualified ones carry the ledger note). Sec. 16 gets
included sources with any other status and excluded sources whose status is
REJECTED or UNRESOLVED. Lines follow the review-template.md format that
check_review.py parses.
"""
import argparse
import csv
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from litlib import load_bib, split_authors  # noqa: E402


def clean(s):
    s = re.sub(r"\\[`'^\"~=.uvHtcdbk]\s*\{?([A-Za-z])\}?", r"\1", s or "")
    s = s.replace("\\&", "&").replace("\\%", "%").replace("\\_", "_").replace("---", "-").replace("--", "-")
    return " ".join(re.sub(r"[{}]", "", s).split())


def authors(raw):
    names = [clean(a) for a in split_authors(raw or "")]
    names = [n.split(",")[0].strip() if "," in n else (n.split()[-1] if n.split() else n) for n in names]
    if not names:
        return "Anonymous"
    if names[-1].lower() == "others":
        names = names[:-1] + ["et al."]
    return names[0] + " et al." if len(names) > 3 else ", ".join(names)


def line(k, e, r):
    f = e["fields"]
    venue = clean(f.get("journal") or f.get("booktitle") or f.get("institution") or f.get("howpublished") or f.get("publisher") or "")
    vol = clean(f.get("volume", ""))
    num = clean(f.get("number", ""))
    pages = clean(f.get("pages", "") or f.get("eid", "")).replace("--", "-")
    loc = ", ".join(x for x in [vol + (f"({num})" if num and vol and e["type"] == "article" else ""), pages] if x)
    if e["type"] == "techreport" and num:
        loc = num
    doi = (f.get("doi") or r.get("doi") or "").strip()
    link = f"https://doi.org/{doi}" if doi else (f.get("url") or r.get("url") or "")
    st = r["verification_status"]
    note = f" Note: {r['notes']}." if st == "VERIFIED-QUALIFIED" and r.get("notes") else ""
    return (f"- **[{k}]** {authors(f.get('author'))} ({clean(f.get('year', 'n.d.'))}). {clean(f.get('title'))}. "
            f"*{venue}*{', ' + loc if loc else ''}. {link}. Status: {st} | Peer review: {r.get('peer_review_status') or 'unknown'} "
            f"| Access: {r.get('access_level') or 'METADATA'} | Venue: {r.get('venue_access') or 'unknown'}.{note}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ledger", required=True)
    ap.add_argument("--bib", nargs="+", required=True)
    a = ap.parse_args()
    bib = {}
    for b in reversed(a.bib):  # earlier files win
        bib.update({x["key"]: x for x in load_bib(b)})
    with open(a.ledger, newline="", encoding="utf-8-sig") as fh:
        rows = list(csv.DictReader(fh))
    ok = ("VERIFIED", "VERIFIED-QUALIFIED")
    s15 = sorted((r for r in rows if r["screening_decision"] == "included" and r["verification_status"] in ok),
                 key=lambda r: r["source_id"])
    s16 = sorted((r for r in rows if (r["screening_decision"] == "included" and r["verification_status"] not in ok)
                  or r["verification_status"] in ("REJECTED", "UNRESOLVED")), key=lambda r: r["source_id"])
    print("<!-- Sec. 15 lines -->")
    for r in s15:
        e = bib.get(r["source_id"])
        print(line(r["source_id"], e, r) if e else f"- **[{r['source_id']}]** MISSING BIB ENTRY")
    print("\n<!-- Sec. 16 lines -->")
    for r in s16:
        e = bib.get(r["source_id"])
        title = clean(e["fields"].get("title")) if e else "(no bib entry)"
        print(f"- **[{r['source_id']}]** {title}. Status: {r['verification_status']}. "
              f"Problem: {r.get('exclusion_reason') or r.get('notes') or 'not recorded'}.")
    print(f"\n<!-- {len(s15)} verified lines, {len(s16)} unverified or rejected lines -->", file=sys.stderr)


if __name__ == "__main__":
    main()
