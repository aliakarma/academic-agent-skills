#!/usr/bin/env python3
"""Audit LaTeX citations against the active bibliography (offline).

Follows \\input/\\include from the main .tex file, finds every cite-family
command (natbib and biblatex, including multicite), locates the active
.bib files, and reports:

  ERROR  cited key with no bib entry
  ERROR  duplicate bib key (BibTeX treats keys case-insensitively)
  ERROR  unescaped % in a non-URL field (silently truncates the .bbl line)
  ERROR  unescaped & outside url/doi (compile error)
  WARN   bib entry never cited (ignored when \\nocite{*} is present)
  WARN   duplicate DOI or near-identical title across entries
  WARN   missing required field for the entry type
  WARN   DOI field carrying a URL or "doi:" prefix
  WARN   field defined twice in one entry

Snapshots let you prove what changed during the review:
  python audit_citations.py paper.tex --snapshot literature/baseline_citations.json
  ... edit ...
  python audit_citations.py paper.tex --compare literature/baseline_citations.json

Exit status 1 when any ERROR is found.
"""
import argparse
import collections
import datetime
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import litlib  # noqa: E402

REQUIRED = {
    "article": [["author"], ["title"], ["journal", "journaltitle"],
                ["year", "date"]],
    "inproceedings": [["author"], ["title"], ["booktitle"], ["year", "date"]],
    "conference": [["author"], ["title"], ["booktitle"], ["year", "date"]],
    "incollection": [["author"], ["title"], ["booktitle"], ["year", "date"]],
    "book": [["author", "editor"], ["title"], ["publisher"], ["year", "date"]],
    "phdthesis": [["author"], ["title"], ["school", "institution"],
                  ["year", "date"]],
    "mastersthesis": [["author"], ["title"], ["school", "institution"],
                      ["year", "date"]],
    "techreport": [["author"], ["title"], ["institution"], ["year", "date"]],
    "online": [["title"], ["url"]],
    "misc": [["title"]],
}
URLISH = {"url", "doi", "eprint", "file", "howpublished", "note"}


def audit(main, bib_override=None):
    cites, bibs, nocite_all, missing_inputs = litlib.extract_citations(main)
    if bib_override:
        bibs = bib_override
    findings = []

    def add(level, msg):
        findings.append((level, msg))

    for m in missing_inputs:
        add("WARN", f"\\input target not found: {m}")
    entries = []
    for b in bibs:
        if not os.path.exists(b):
            add("ERROR", f"bibliography file not found: {b}")
            continue
        for e in litlib.load_bib(b):
            e["file"] = b
            entries.append(e)

    by_lower = collections.defaultdict(list)
    for e in entries:
        by_lower[e["key"].lower()].append(e)
    for k, group in by_lower.items():
        if len(group) > 1:
            locs = ", ".join(f"{os.path.basename(g['file'])}:{g['line']}"
                             for g in group)
            add("ERROR", f"duplicate bib key '{group[0]['key']}' at {locs}")

    cited = collections.OrderedDict()
    for key, f, ln, cmd in cites:
        cited.setdefault(key, []).append(f"{os.path.basename(f)}:{ln}")
    keys_exact = {e["key"] for e in entries}
    cited_lower = {k.lower() for k in cited}
    for key, locs in cited.items():
        if key in keys_exact:
            continue
        where = ", ".join(locs[:3])
        if key.lower() in by_lower:
            add("WARN", f"cited key '{key}' matches bib key "
                        f"'{by_lower[key.lower()][0]['key']}' only by case "
                        f"(BibTeX accepts this, biber fails); cited at {where}")
        else:
            add("ERROR", f"cited key '{key}' has no bib entry; cited at {where}")
    if not nocite_all:
        for e in entries:
            if e["key"].lower() not in cited_lower:
                add("WARN", f"bib entry '{e['key']}' is never cited "
                            f"({os.path.basename(e['file'])}:{e['line']})")

    dois = collections.defaultdict(list)
    titles = collections.defaultdict(list)
    for e in entries:
        f = e["fields"]
        loc = f"{os.path.basename(e['file'])}:{e['line']}"
        for name in e["dup_fields"]:
            add("WARN", f"'{e['key']}' defines field '{name}' twice ({loc})")
        for alts in REQUIRED.get(e["type"], []):
            if not any(f.get(a, "").strip() for a in alts):
                add("WARN", f"'{e['key']}' (@{e['type']}) lacks "
                            f"{'/'.join(alts)} ({loc})")
        for name, val in f.items():
            if name in URLISH:
                continue
            if re.search(r"(?<!\\)%", val):
                add("ERROR", f"'{e['key']}' field '{name}' has an unescaped "
                             f"% (truncates text in the .bbl) ({loc})")
            if re.search(r"(?<!\\)&", val):
                add("ERROR", f"'{e['key']}' field '{name}' has an unescaped "
                             f"& ({loc})")
        raw_doi = f.get("doi", "")
        if raw_doi and re.match(r"\s*(https?://|doi:)", raw_doi, re.I):
            add("WARN", f"'{e['key']}' doi field has a URL/doi: prefix ({loc})")
        d = litlib.clean_doi(raw_doi)
        if d:
            dois[d].append(e["key"])
        t = litlib.norm(f.get("title", ""))
        if len(t) > 20:
            titles[t].append(e["key"])
    for d, ks in dois.items():
        if len(ks) > 1:
            add("WARN", f"DOI {d} shared by {', '.join(ks)}")
    for t, ks in titles.items():
        if len(ks) > 1:
            add("WARN", f"identical title in {', '.join(ks)}")

    return {
        "main": os.path.abspath(main),
        "bib_files": [os.path.abspath(b) for b in bibs],
        "nocite_all": nocite_all,
        "cited": cited,
        "bib_keys": sorted(keys_exact),
        "findings": findings,
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawTextHelpFormatter)
    ap.add_argument("tex", help="main .tex file")
    ap.add_argument("--bib", nargs="*", help="override detected .bib files")
    ap.add_argument("--snapshot", help="write cited/bib key snapshot JSON")
    ap.add_argument("--compare", help="compare against a snapshot JSON")
    ap.add_argument("--quiet-uncited", action="store_true",
                    help="hide 'never cited' warnings")
    a = ap.parse_args()

    r = audit(a.tex, a.bib)
    print(f"Main file : {r['main']}")
    print(f"Bib files : {', '.join(r['bib_files']) or 'NONE FOUND'}")
    print(f"Cited keys: {len(r['cited'])} unique | Bib entries: "
          f"{len(r['bib_keys'])} | nocite{{*}}: {r['nocite_all']}")
    errs = [m for lvl, m in r["findings"] if lvl == "ERROR"]
    warns = [m for lvl, m in r["findings"] if lvl == "WARN"
             and not (a.quiet_uncited and "never cited" in m)]
    for m in errs:
        print(f"ERROR {m}")
    for m in warns:
        print(f"WARN  {m}")
    print(f"Summary: {len(errs)} error(s), {len(warns)} warning(s)")

    if a.compare:
        with open(a.compare, encoding="utf-8") as fh:
            snap = json.load(fh)
        old_c, new_c = set(snap["cited"]), set(r["cited"])
        old_b, new_b = set(snap["bib_keys"]), set(r["bib_keys"])
        print(f"\nCompared with snapshot of {snap.get('date', '?')}:")
        print(f"  newly cited keys   ({len(new_c - old_c)}): "
              f"{', '.join(sorted(new_c - old_c))}")
        print(f"  no longer cited    ({len(old_c - new_c)}): "
              f"{', '.join(sorted(old_c - new_c))}")
        print(f"  new bib entries    ({len(new_b - old_b)}): "
              f"{', '.join(sorted(new_b - old_b))}")
        print(f"  removed bib entries({len(old_b - new_b)}): "
              f"{', '.join(sorted(old_b - new_b))}")
    if a.snapshot:
        if os.path.exists(a.snapshot):
            sys.exit(f"refusing to overwrite existing snapshot {a.snapshot}")
        with open(a.snapshot, "w", encoding="utf-8") as fh:
            json.dump({"date": datetime.date.today().isoformat(),
                       "main": r["main"], "bib_files": r["bib_files"],
                       "cited": list(r["cited"]), "bib_keys": r["bib_keys"]},
                      fh, indent=1)
        print(f"Snapshot written to {a.snapshot}")
    sys.exit(1 if errs else 0)


if __name__ == "__main__":
    main()
