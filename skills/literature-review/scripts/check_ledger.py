#!/usr/bin/env python3
"""Check traceability between the source ledger, bibliography, manuscript,
citation map, and per-source evidence records.

  python check_ledger.py --lit literature --tex paper.tex
  python check_ledger.py --lit literature --tex paper.tex \\
      --baseline literature/baseline_citations.json

ERROR conditions (exit status 1):
  * ledger is missing columns, has duplicate source_ids, or invalid enum values
  * a cited key has no ledger row, or its status is not VERIFIED /
    VERIFIED-QUALIFIED, or its access_level is empty
  * a ledger row says cited_in_manuscript=yes but the key is not cited
  * a ledger row is cited but its bib DOI differs from the ledger DOI
  * citation_map rows reference unknown source_ids, or an "inserted" claim
    cites a source that is not cited in the manuscript
WARN conditions:
  * a cited source has no raw/source_records/<id>.md or no extraction row
  * an included source is never cited (fine if deliberate: say why in notes)
  * with --baseline: citations that predate the review and are not in the
    ledger are listed as WARN instead of ERROR, so they can be verified
    without blocking the run
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import litlib  # noqa: E402


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawTextHelpFormatter)
    ap.add_argument("--lit", default="literature", help="workspace folder")
    ap.add_argument("--tex", required=True, help="main manuscript .tex")
    ap.add_argument("--bib", nargs="*", help="override detected .bib files")
    ap.add_argument("--baseline", help="snapshot JSON from audit_citations.py")
    a = ap.parse_args()

    errors, warns = [], []
    ledger_path = os.path.join(a.lit, "source_ledger.csv")
    if not os.path.exists(ledger_path):
        sys.exit(f"no ledger at {ledger_path} (run init_workspace.py)")
    rows = litlib.read_csv(ledger_path)
    header = list(rows[0].keys()) if rows else litlib.SCHEMAS["source_ledger.csv"]
    for c in litlib.SCHEMAS["source_ledger.csv"]:
        if c not in header:
            errors.append(f"ledger lacks column '{c}'")
    ledger = {}
    for i, r in enumerate(rows, 2):
        sid = (r.get("source_id") or "").strip()
        if not sid:
            errors.append(f"ledger line {i}: empty source_id")
            continue
        if sid in ledger:
            errors.append(f"ledger line {i}: duplicate source_id '{sid}'")
        ledger[sid] = r
        for col in ("verification_status", "access_level", "screening_decision",
                    "peer_review_status", "relevance", "cited_in_manuscript"):
            v = (r.get(col) or "").strip()
            if col in r and v not in litlib.ENUMS[col] and not (v == "" and col in
                                                               ("relevance", "access_level")):
                errors.append(f"ledger '{sid}': {col}='{v}' not in "
                              f"{sorted(x for x in litlib.ENUMS[col] if x)}")

    cites, bibs, _, _ = litlib.extract_citations(a.tex)
    if a.bib:
        bibs = a.bib
    cited = {k for k, *_ in cites}
    bib = {}
    for b in bibs:
        if os.path.exists(b):
            for e in litlib.load_bib(b):
                bib[e["key"]] = e
    baseline = set()
    if a.baseline:
        with open(a.baseline, encoding="utf-8") as fh:
            baseline = set(json.load(fh)["cited"])

    extraction = set()
    ex_path = os.path.join(a.lit, "extraction_sheet.csv")
    if os.path.exists(ex_path):
        extraction = {r["source_id"].strip() for r in litlib.read_csv(ex_path)}

    for key in sorted(cited):
        r = ledger.get(key)
        if r is None:
            (warns if key in baseline else errors).append(
                f"cited key '{key}' has no ledger row"
                + (" (pre-existing citation, still needs verification)" if key in baseline else ""))
            continue
        st = r.get("verification_status", "").strip()
        if st not in litlib.CITABLE_STATUSES:
            errors.append(f"'{key}' is cited but its status is {st or 'empty'}")
        if not r.get("access_level", "").strip():
            errors.append(f"'{key}' is cited but access_level is empty")
        if r.get("cited_in_manuscript", "").strip() != "yes":
            errors.append(f"'{key}' is cited but ledger says cited_in_manuscript="
                          f"{r.get('cited_in_manuscript', '')!r}")
        e = bib.get(key)
        if e is None:
            errors.append(f"'{key}' is cited and in the ledger but not in the bib")
        else:
            bd = litlib.clean_doi(e["fields"].get("doi", ""))
            ld = litlib.clean_doi(r.get("doi", ""))
            if bd and ld and bd != ld:
                errors.append(f"'{key}': bib DOI {bd} differs from ledger DOI {ld}")
        if not os.path.exists(os.path.join(a.lit, "raw", "source_records", f"{key}.md")):
            warns.append(f"'{key}' has no raw/source_records/{key}.md")
        if extraction and key not in extraction:
            warns.append(f"'{key}' has no extraction_sheet row")

    for sid, r in ledger.items():
        if r.get("cited_in_manuscript", "").strip() == "yes" and sid not in cited:
            errors.append(f"ledger says '{sid}' is cited, but the manuscript never cites it")
        if r.get("screening_decision", "").strip() == "included" and sid not in cited:
            warns.append(f"'{sid}' is included but not cited (record why in notes)")

    cm_path = os.path.join(a.lit, "citation_map.csv")
    if os.path.exists(cm_path):
        for r in litlib.read_csv(cm_path):
            cid = r.get("claim_id", "?")
            for col in ("claim_type", "support", "priority", "status"):
                v = (r.get(col) or "").strip()
                if v and v not in litlib.ENUMS[col]:
                    errors.append(f"citation_map {cid}: {col}='{v}' invalid")
            for sid in [s.strip() for s in (r.get("source_ids") or "").replace(";", ",").split(",") if s.strip()]:
                if sid not in ledger:
                    errors.append(f"citation_map {cid}: unknown source_id '{sid}'")
                elif r.get("status", "").strip() == "inserted" and sid not in cited:
                    errors.append(f"citation_map {cid}: marked inserted but '{sid}' is not cited")

    for m in errors:
        print(f"ERROR {m}")
    for m in warns:
        print(f"WARN  {m}")
    n_cited_ver = sum(1 for k in cited if ledger.get(k, {}).get("verification_status")
                      in litlib.CITABLE_STATUSES)
    print(f"Summary: {len(cited)} cited keys, {n_cited_ver} with a citable ledger status, "
          f"{len(ledger)} ledger rows, {len(errors)} error(s), {len(warns)} warning(s)")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
