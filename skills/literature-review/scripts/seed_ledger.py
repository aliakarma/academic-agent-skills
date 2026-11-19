#!/usr/bin/env python3
"""Seed or update literature/source_ledger.csv from bib files and verify_refs output.

  python seed_ledger.py --bib references.bib literature/references_lit.bib \
      --verify literature/raw/verification/*.csv --notes literature/reading_notes.csv

For every bib entry it writes one ledger row with the bibliographic fields
from the bib and a verification_status derived from the machine check:
  MATCH -> VERIFIED, PARTIAL -> VERIFIED-QUALIFIED only if your notes say so
  (else PENDING), MISMATCH / DOI_NOT_FOUND -> PENDING with the issue in notes,
  no check -> PENDING.
Then it merges --notes (your reading judgments, one row per source_id, any
subset of ledger columns such as access_level, peer_review_status, themes,
verification_status, screening_decision, exclusion_reason, notes). Notes win.
Columns already filled in an existing ledger are kept unless notes override.

Never invents an access level: rows without one stay empty, and
check_review.py --ledger will refuse a Sec. 15 entry whose ledger status is
not VERIFIED or VERIFIED-QUALIFIED.
"""
import argparse
import csv
import datetime
import glob
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from litlib import SCHEMAS, get_json, load_bib  # noqa: E402

COLS = SCHEMAS["source_ledger.csv"]


def venue_access(dois):
    """{doi: 'open'|'closed'|'unknown'} from OpenAlex primary_location.source.

    open   = fully open-access venue (OpenAlex/DOAJ is_oa) or an open repository
             (arXiv, SSRN, Research Square, institutional server)
    closed = subscription or hybrid venue, even when one article is free to read
    """
    out = {d: "open" for d in dois if d.startswith("10.48550/")}  # arXiv
    rest = [d for d in dois if d not in out]
    for i in range(0, len(rest), 40):
        chunk = rest[i:i + 40]
        _, js, _ = get_json("https://api.openalex.org/works?per-page=50&select=doi,primary_location"
                            "&filter=doi:" + "|".join(chunk))
        for w in (js or {}).get("results", []):
            d = (w.get("doi") or "").replace("https://doi.org/", "").lower()
            src = (w.get("primary_location") or {}).get("source") or {}
            if not src:
                out[d] = "unknown"
            elif src.get("is_oa") or src.get("is_in_doaj") or src.get("type") == "repository":
                out[d] = "open"
            else:
                out[d] = "closed"
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--bib", nargs="+", required=True)
    ap.add_argument("--verify", nargs="*", default=[])
    ap.add_argument("--notes")
    ap.add_argument("--lit", default="literature")
    ap.add_argument("--fetch-venue-access", action="store_true",
                    help="fill empty venue_access (open/closed) for included rows from OpenAlex")
    a = ap.parse_args()

    path = os.path.join(a.lit, "source_ledger.csv")
    old = {}
    if os.path.exists(path) and os.path.getsize(path):
        with open(path, newline="", encoding="utf-8-sig") as fh:
            old = {r["source_id"]: r for r in csv.DictReader(fh)}
    ver = {}
    for pat in a.verify:
        for f in sorted(glob.glob(pat)):
            with open(f, newline="", encoding="utf-8") as fh:
                for r in csv.DictReader(fh):
                    if "key" in r and "machine_check" in r:
                        ver[r["key"]] = r  # later files win
    notes = {}
    if a.notes:
        with open(a.notes, newline="", encoding="utf-8-sig") as fh:
            notes = {r["source_id"]: r for r in csv.DictReader(fh)}
    unknown = set(notes) - {x["key"] for b in a.bib for x in load_bib(b)}
    today = datetime.date.today().isoformat()

    rows = {}
    for b in a.bib:
        for ent in load_bib(b):
            k, e = ent["key"], {**ent["fields"], "_type": ent["type"]}
            v = ver.get(k, {})
            mc = v.get("machine_check", "")
            status = {"MATCH": "VERIFIED"}.get(mc, "PENDING")
            r = dict.fromkeys(COLS, "")
            r.update(old.get(k, {}))
            r.update(source_id=k, title=e.get("title", ""), authors=e.get("author", ""), year=e.get("year", ""),
                     venue=e.get("journal") or e.get("booktitle") or e.get("institution") or e.get("howpublished") or e.get("publisher", ""),
                     pub_type=e.get("_type") or e.get("ENTRYTYPE", ""), doi=(e.get("doi") or "").lower())
            if mc:
                r["url"] = r["url"] or v.get("record_url", "")
                r["verification_date"] = (v.get("checked_at") or today)[:10]
                r["verification_evidence"] = f"{os.path.basename(b)} -> machine_check={mc}"
                if not r["verification_status"] or r["verification_status"] == "PENDING":
                    r["verification_status"] = status
                if mc != "MATCH" and v.get("issues") and "machine: " not in r["notes"]:  # idempotent on rerun
                    r["notes"] = (r["notes"] + ". " if r["notes"] else "") + "machine: " + v["issues"]
            r["verification_status"] = r["verification_status"] or "PENDING"
            r["cited_in_manuscript"] = r["cited_in_manuscript"] or "no"
            r["screening_decision"] = r["screening_decision"] or "candidate"
            for c, val in notes.get(k, {}).items():
                if c in COLS and c != "source_id" and val != "":
                    r[c] = val
            rows[k] = r
    rows.update({k: r for k, r in old.items() if k not in rows})
    if a.fetch_venue_access:
        todo = [r["doi"] for r in rows.values()
                if r["screening_decision"] == "included" and r["doi"] and not r.get("venue_access")]
        va = venue_access(todo)
        for r in rows.values():
            if r["doi"] in va and not r.get("venue_access"):
                r["venue_access"] = va[r["doi"]]

    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=COLS, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows.values())
    inc = [r for r in rows.values() if r["screening_decision"] == "included"]
    count = lambda col, vals: {x: sum(r[col] == x for r in inc) for x in vals}
    print(f"{path}: {len(rows)} rows, {len(inc)} included")
    print("included by status:", count("verification_status", ["VERIFIED", "VERIFIED-QUALIFIED", "UNRESOLVED", "REJECTED", "PENDING"]))
    print("included by access:", count("access_level", ["FULLTEXT", "ABSTRACT", "METADATA", ""]))
    vac = count("venue_access", ["open", "closed", "unknown", ""])
    known = vac["open"] + vac["closed"]
    print("included by venue:", vac, f"closed share {100 * vac['closed'] / known:.0f}%" if known else "")
    for r in inc:
        if r["verification_status"] not in ("VERIFIED", "VERIFIED-QUALIFIED") or not r["access_level"]:
            print(f"OPEN {r['source_id']}: status={r['verification_status']} access={r['access_level'] or '-'}")
    for k in sorted(unknown):
        print(f"WARN notes row {k} matches no bib entry")


if __name__ == "__main__":
    main()
