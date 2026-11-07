#!/usr/bin/env python3
"""Machine-check BibTeX entries against authoritative metadata records.

For each entry:
  * DOI present: fetch the Crossref record (DataCite when the DOI belongs to
    that registration agency, e.g. arXiv 10.48550), compare title (with and
    without subtitle), first author, author count, year and venue, and ask
    Crossref whether a retraction, correction, withdrawal or expression of
    concern updates the work.
  * arXiv entry without DOI: fetch the arXiv record (Semantic Scholar as
    fallback) and report any published version the record links.
  * Other entries without DOI: title search in Crossref, then Semantic
    Scholar, then OpenAlex. A candidate DOI from an aggregator is re-fetched
    from Crossref and only reported as "confirmed" when that record matches.
    Aggregators carry wrong DOIs: never paste one in unconfirmed.

The output is a MACHINE CHECK of bibliographic identity. It never shows that
a source supports a sentence in the manuscript. The reviewer assigns the
final verification_status in the source ledger after reading the record.

machine_check values:
  MATCH             title, first author and year agree with the record
  PARTIAL           identifiable, one or more fields disagree (see issues)
  MISMATCH          the DOI/id resolves to a different work
  DOI_NOT_FOUND     no registration agency knows the DOI
  NO_DOI_CANDIDATE  no DOI in the entry, a close title match was found
  NO_DOI_NO_MATCH   no DOI and no close match found
  ERROR             network or parsing failure: the check did NOT happen

Usage:
  python verify_refs.py references.bib --out literature/raw/verification/verify.csv \\
      --raw-dir literature/raw/verification
  python verify_refs.py references.bib --keys smith2020a,lee2021b

Optional environment: CROSSREF_MAILTO (Crossref polite pool),
S2_API_KEY (Semantic Scholar), OPENALEX_API_KEY (OpenAlex daily budget).
Exit status 1 with --strict when any entry needs attention.
"""
import argparse
import csv
import datetime
import json
import os
import re
import sys
import time
import urllib.request
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import litlib  # noqa: E402

COLUMNS = ["key", "type", "doi", "record_source", "machine_check", "issues",
           "title_sim", "bib_title", "record_title", "bib_first_author",
           "record_first_author", "bib_year", "record_years", "bib_n_authors",
           "record_n_authors", "bib_venue", "record_venue", "updates",
           "candidate_doi", "candidate_status", "record_url", "checked_at"]
ATTENTION = {"PARTIAL", "MISMATCH", "DOI_NOT_FOUND", "NO_DOI_NO_MATCH", "ERROR"}
ARXIV_ID = re.compile(r"(\d{4}\.\d{4,5}|[a-z-]+(?:\.[A-Z]{2})?/\d{7})(v\d+)?", re.I)
PUBLISHED_TYPES = {"article", "inproceedings", "incollection", "conference"}


class Ctx:
    def __init__(self, mailto, raw_dir, pause):
        self.mailto, self.raw_dir, self.pause = mailto, raw_dir, pause
        self.s2_key = os.environ.get("S2_API_KEY")
        self.oa_key = os.environ.get("OPENALEX_API_KEY")

    def get(self, url, key, tag, accept="application/json", headers=None,
            timeout=30):
        time.sleep(self.pause)
        if headers:  # litlib.http_get has no custom headers, use urllib here
            req = urllib.request.Request(url, headers=dict(
                headers, **{"User-Agent": litlib.USER_AGENT, "Accept": accept}))
            try:
                with urllib.request.urlopen(req, timeout=timeout) as r:
                    status, text = r.status, r.read().decode("utf-8", "replace")
            except Exception as exc:
                status, text = getattr(exc, "code", 0), str(exc)
        else:
            status, text = litlib.http_get(url, accept=accept,
                                           mailto=self.mailto, timeout=timeout)
        if self.raw_dir and status == 200:
            safe = re.sub(r"[^\w.-]", "_", key)
            ext = "xml" if "xml" in accept else "json"
            with open(os.path.join(self.raw_dir, f"{safe}.{tag}.{ext}"), "w",
                      encoding="utf-8") as fh:
                fh.write(text)
        return status, text

    def crossref(self, path):
        sep = "&" if "?" in path else "?"
        return "https://api.crossref.org/" + path + (
            f"{sep}mailto={litlib.q(self.mailto)}" if self.mailto else "")


def jload(text):
    try:
        return json.loads(text)
    except (ValueError, TypeError):
        return None


# ---------------------------------------------------------------- records
def rec(title, first, n, years, venue, url, alt_title=""):
    return {"title": title, "alt_title": alt_title, "first": first, "n": n,
            "years": {int(y) for y in years if str(y).isdigit()},
            "venue": venue or "", "url": url or ""}


def crossref_record(msg):
    years = []
    for k in ("issued", "published-print", "published-online", "published"):
        parts = (msg.get(k) or {}).get("date-parts") or [[None]]
        if parts and parts[0] and parts[0][0]:
            years.append(parts[0][0])
    authors = msg.get("author") or []
    first = (authors[0].get("family") or authors[0].get("name") or "") if authors else ""
    title = " ".join(msg.get("title") or [])
    sub = " ".join(msg.get("subtitle") or [])
    return rec(title, first, len(authors), years,
               " ".join((msg.get("container-title") or [])[:1]),
               "https://doi.org/" + msg.get("DOI", ""),
               alt_title=f"{title}: {sub}" if sub else "")


def datacite_record(data):
    at = (data or {}).get("attributes", {})
    cr = at.get("creators") or []
    first = (cr[0].get("familyName") or cr[0].get("name") or "") if cr else ""
    return rec(" ".join(t.get("title", "") for t in (at.get("titles") or [])[:1]),
               first, len(cr), [at.get("publicationYear") or ""],
               (at.get("container") or {}).get("title") or at.get("publisher") or "",
               "https://doi.org/" + at.get("doi", ""))


def s2_record(p):
    au = p.get("authors") or []
    first = au[0].get("name", "").split()[-1] if au and au[0].get("name") else ""
    return rec(p.get("title") or "", first, len(au), [p.get("year") or ""],
               p.get("venue") or "", p.get("url") or "")


def openalex_record(w):
    au = w.get("authorships") or []
    name = ((au[0].get("author") or {}).get("display_name") or "") if au else ""
    src = ((w.get("primary_location") or {}).get("source") or {})
    return rec(w.get("title") or "", name.split()[-1] if name else "", len(au),
               [w.get("publication_year") or ""], src.get("display_name") or "",
               w.get("doi") or w.get("id") or "")


def compare(entry, r):
    f = entry["fields"]
    authors = litlib.split_authors(f.get("author", ""))
    has_others = any(a.strip().lower() == "others" for a in authors)
    bib_first = litlib.family_name(authors[0]) if authors else ""
    m = re.search(r"\d{4}", f.get("year", "") or f.get("date", ""))
    bib_year = int(m.group(0)) if m else None
    bib_venue = f.get("journal") or f.get("journaltitle") or f.get("booktitle") or ""

    sim = max(litlib.similarity(f.get("title", ""), r["title"]),
              litlib.similarity(f.get("title", ""), r["alt_title"]) if r["alt_title"] else 0)
    issues = []
    first_ok = litlib.same_family(bib_first, r["first"]) if r["first"] and bib_first else None
    year_ok = (bib_year in r["years"]) if (bib_year and r["years"]) else None
    if sim < 0.95:
        issues.append(f"title similarity {sim:.2f}")
    if first_ok is False:
        issues.append(f"first author '{bib_first}' vs '{r['first']}'")
    if year_ok is False:
        near = any(abs(bib_year - y) == 1 for y in r["years"])
        issues.append("year off by one (online vs print, or preprint vs venue)"
                      if near else f"year {bib_year} vs {sorted(r['years'])}")
    n_bib = len([a for a in authors if a.strip().lower() != "others"])
    count_bad = bool(r["n"] and n_bib and not has_others and n_bib != r["n"])
    if count_bad:
        issues.append(f"author count {n_bib} vs {r['n']}")
    if bib_venue and r["venue"] and litlib.similarity(bib_venue, r["venue"]) < 0.5:
        issues.append(f"venue '{bib_venue[:40]}' vs '{r['venue'][:40]}'")

    if sim >= 0.95 and first_ok is not False and year_ok is not False and not count_bad:
        verdict = "MATCH" if not issues else "PARTIAL"
    elif sim >= 0.85 and (first_ok or year_ok):
        verdict = "PARTIAL"
    else:
        verdict = "MISMATCH"
    row = {"title_sim": f"{sim:.2f}", "record_title": r["title"],
           "bib_first_author": bib_first, "record_first_author": r["first"],
           "bib_year": bib_year or "",
           "record_years": ",".join(str(y) for y in sorted(r["years"])),
           "bib_n_authors": n_bib, "record_n_authors": r["n"],
           "bib_venue": bib_venue, "record_venue": r["venue"],
           "record_url": r["url"]}
    return verdict, issues, row


# ---------------------------------------------------------------- lookups
def crossref_updates(ctx, key, doi):
    status, text = ctx.get(ctx.crossref(f"works?filter=updates:{litlib.q(doi)}&rows=20"),
                           key, "crossref-updates")
    data = jload(text) if status == 200 else None
    if data is None:
        return f"update check failed (HTTP {status})"
    found = set()
    for item in data.get("message", {}).get("items", []):
        for u in item.get("update-to") or []:
            if litlib.clean_doi(u.get("DOI")) == doi:
                found.add(f"{u.get('type', 'update')}:{item.get('DOI', '')}")
    return "; ".join(sorted(found))


def fetch_doi(ctx, key, doi):
    """Return (record, source, error_row)."""
    status, text = ctx.get(ctx.crossref(f"works/{litlib.q(doi)}"), key, "crossref")
    if status == 200 and jload(text):
        return crossref_record(jload(text)["message"]), "crossref", None
    if status != 404:
        return None, "", {"machine_check": "ERROR",
                          "issues": f"Crossref HTTP {status}: {text[:100]}"}
    st, t = ctx.get(f"https://doi.org/doiRA/{doi}", key, "doiRA")
    d = jload(t)
    ra = (d[0].get("RA") or d[0].get("status") or "") if isinstance(d, list) and d else ""
    if ra.lower() == "datacite":
        st3, t3 = ctx.get(f"https://api.datacite.org/dois/{litlib.q(doi)}", key, "datacite")
        if st3 == 200 and jload(t3):
            return datacite_record(jload(t3).get("data")), "datacite", None
        return None, "", {"machine_check": "ERROR", "issues": f"DataCite HTTP {st3}"}
    if not ra or "not exist" in ra.lower() or "invalid" in ra.lower():
        return None, "", {"machine_check": "DOI_NOT_FOUND",
                          "issues": f"no registration agency knows this DOI ({ra or st})"}
    return None, "", {"machine_check": "ERROR",
                      "issues": f"DOI registered with {ra}: no API wired, verify at https://doi.org/{doi}"}


def check_doi(ctx, entry, doi):
    r, source, err = fetch_doi(ctx, entry["key"], doi)
    if err:
        return err
    verdict, issues, row = compare(entry, r)
    if doi.startswith("10.48550/") and entry["type"] in PUBLISHED_TYPES:
        issues.append("DOI is the arXiv preprint but the entry cites a published "
                      "venue (version mismatch: use the venue DOI/URL or cite the preprint)")
        issues = [i for i in issues if not i.startswith("venue")]
        if verdict == "MATCH":
            verdict = "PARTIAL"
    row.update({"record_source": source, "machine_check": verdict,
                "issues": "; ".join(issues)})
    if source == "crossref":
        row["updates"] = crossref_updates(ctx, entry["key"], doi)
    return row


def confirm_candidate(ctx, entry, doi):
    """Re-fetch an aggregator-supplied DOI from its agency and compare."""
    r, _, err = fetch_doi(ctx, entry["key"] + ".candidate", litlib.clean_doi(doi))
    if err:
        return f"unconfirmed ({err['machine_check']})"
    verdict, _, row = compare(entry, r)
    if verdict == "MISMATCH":
        return f"REJECTED: DOI resolves to '{row['record_title'][:60]}'"
    return f"confirmed at registration agency ({verdict})"


def s2_get(ctx, key, path, tag):
    hdr = {"x-api-key": ctx.s2_key} if ctx.s2_key else None
    url = "https://api.semanticscholar.org/graph/v1/" + path
    status, text = ctx.get(url, key, tag, headers=hdr)
    if status == 429:
        time.sleep(3)
        status, text = ctx.get(url, key, tag, headers=hdr)
    return status, jload(text) if status == 200 else None


S2_FIELDS = "title,authors,year,venue,externalIds,url,publicationTypes"


def check_arxiv(ctx, entry):
    f = entry["fields"]
    blob = " ".join(f.get(k, "") for k in ("eprint", "journal", "url", "howpublished",
                                            "note", "archiveprefix", "booktitle"))
    if "arxiv" not in blob.lower() and not f.get("eprint"):
        return None
    m = ARXIV_ID.search(f.get("eprint", "") or blob)
    if not m:
        return None
    aid = m.group(1)
    status, text = ctx.get(f"https://export.arxiv.org/api/query?id_list={aid}",
                           entry["key"], "arxiv", accept="application/atom+xml",
                           timeout=60)
    ns = {"a": "http://www.w3.org/2005/Atom", "x": "http://arxiv.org/schemas/atom"}
    r, pub_doi, jref, source = None, "", "", "arxiv"
    if status == 200:
        try:
            e = ET.fromstring(text).find("a:entry", ns)
        except ET.ParseError:
            e = None
        if e is not None and e.find("a:title", ns) is not None:
            names = [n.text for n in e.findall("a:author/a:name", ns)]
            r = rec(" ".join(e.find("a:title", ns).text.split()),
                    names[0].split()[-1] if names else "", len(names),
                    [(e.findtext("a:published", "", ns) or "")[:4]], "arXiv",
                    f"https://arxiv.org/abs/{aid}")
            pub_doi = e.findtext("x:doi", "", ns)
            jref = e.findtext("x:journal_ref", "", ns)
    if r is None:  # arXiv API slow or down: fall back to Semantic Scholar
        st, p = s2_get(ctx, entry["key"], f"paper/arXiv:{aid}?fields={S2_FIELDS}", "s2-arxiv")
        if not p:
            return {"machine_check": "ERROR",
                    "issues": f"arXiv HTTP {status} and Semantic Scholar HTTP {st}"}
        r, source = s2_record(p), "semanticscholar"
        r["venue"] = "arXiv"
        pub_doi = (p.get("externalIds") or {}).get("DOI", "")
    verdict, issues, row = compare(entry, r)
    issues = [i for i in issues if not i.startswith("venue")]
    if verdict == "PARTIAL" and not issues:
        verdict = "MATCH"
    if pub_doi or jref:
        status_txt = confirm_candidate(ctx, entry, pub_doi) if pub_doi else ""
        row["candidate_doi"], row["candidate_status"] = pub_doi, status_txt
        if not status_txt.startswith("REJECTED"):
            issues.append(f"record links a published version: {pub_doi} {jref}".strip())
    row.update({"record_source": source, "machine_check": verdict,
                "issues": "; ".join(issues)})
    return row


def search_title(ctx, entry):
    f = entry["fields"]
    title = f.get("title", "")
    if not litlib.norm(title):
        return {"machine_check": "NO_DOI_NO_MATCH", "issues": "entry has no title"}
    authors = litlib.split_authors(f.get("author", ""))
    first = litlib.family_name(authors[0]) if authors else ""
    qt = litlib.q(litlib.norm(title))
    best, statuses = (0.0, None, "", ""), []

    def consider(r, doi, source):
        nonlocal best
        s = max(litlib.similarity(title, r["title"]),
                litlib.similarity(title, r["alt_title"]) if r["alt_title"] else 0)
        if s > best[0]:
            best = (s, r, doi or "", source)

    st, text = ctx.get(ctx.crossref(
        f"works?query.bibliographic={litlib.q(litlib.norm(title) + ' ' + litlib.norm(first))}"
        "&rows=5&select=DOI,title,subtitle,author,issued,container-title,type"),
        entry["key"], "crossref-search")
    statuses.append(f"Crossref {st}")
    for it in ((jload(text) or {}).get("message") or {}).get("items", []) if st == 200 else []:
        consider(crossref_record(it), it.get("DOI"), "crossref")
    if best[0] < 0.95:
        st, data = s2_get(ctx, entry["key"],
                          f"paper/search?query={qt}&limit=5&fields={S2_FIELDS}", "s2-search")
        statuses.append(f"SemanticScholar {st}")
        for p in (data or {}).get("data", []):
            consider(s2_record(p), (p.get("externalIds") or {}).get("DOI"), "semanticscholar")
    if best[0] < 0.95:
        url = (f"https://api.openalex.org/works?search={qt}&per-page=5"
               "&select=id,doi,title,publication_year,authorships,primary_location"
               + (f"&api_key={litlib.q(ctx.oa_key)}" if ctx.oa_key else ""))
        st, text = ctx.get(url, entry["key"], "openalex-search")
        statuses.append(f"OpenAlex {st}")
        for w in (jload(text) or {}).get("results", []) if st == 200 else []:
            consider(openalex_record(w), litlib.clean_doi(w.get("doi") or ""), "openalex")
    s, r, cdoi, source = best
    if r is None:
        if all(not x.endswith(" 200") for x in statuses):
            return {"machine_check": "ERROR", "issues": "search failed: " + ", ".join(statuses)}
        return {"machine_check": "NO_DOI_NO_MATCH", "issues": "no hits: " + ", ".join(statuses)}
    verdict, issues, row = compare(entry, r)
    row["record_source"] = source
    row["issues"] = "; ".join(issues)
    if s >= 0.90 and verdict != "MISMATCH":
        row["machine_check"] = "NO_DOI_CANDIDATE"
        row["candidate_doi"] = cdoi
        if cdoi:
            row["candidate_status"] = ("from Crossref record" if source == "crossref"
                                       else confirm_candidate(ctx, entry, cdoi))
    else:
        # Best hit is a different work. Keep its title for the reviewer, but
        # never surface its DOI where it could be pasted into the entry.
        row["machine_check"] = "NO_DOI_NO_MATCH"
        row["record_url"] = ""
        row["issues"] = f"closest hit is a different work ({row['issues']})"
    return row


def check_entry(ctx, entry, search):
    f = entry["fields"]
    doi = litlib.clean_doi(f.get("doi", ""))
    row = {"key": entry["key"], "type": entry["type"], "doi": doi,
           "bib_title": " ".join(f.get("title", "").split())}
    try:
        if doi:
            row.update(check_doi(ctx, entry, doi))
        else:
            ax = check_arxiv(ctx, entry)
            if ax:
                row.update(ax)
            elif search:
                row.update(search_title(ctx, entry))
            else:
                row.update({"machine_check": "NO_DOI_NO_MATCH",
                            "issues": "no DOI, search disabled"})
    except Exception as exc:  # report a failed check, never hide it
        row.update({"machine_check": "ERROR", "issues": f"{type(exc).__name__}: {exc}"})
    row["checked_at"] = datetime.datetime.now().isoformat(timespec="seconds")
    return row


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawTextHelpFormatter)
    ap.add_argument("bib")
    ap.add_argument("--out", help="CSV report path")
    ap.add_argument("--raw-dir", help="save every API response here (audit trail)")
    ap.add_argument("--keys", help="comma-separated subset of keys to check")
    ap.add_argument("--mailto", default=os.environ.get("CROSSREF_MAILTO"))
    ap.add_argument("--pause", type=float, default=0.3,
                    help="seconds between requests (default 0.3)")
    ap.add_argument("--no-search", action="store_true",
                    help="do not title-search entries without a DOI")
    ap.add_argument("--strict", action="store_true",
                    help="exit 1 when any entry needs attention")
    a = ap.parse_args()

    entries = litlib.load_bib(a.bib)
    if a.keys:
        wanted = {k.strip() for k in a.keys.split(",")}
        entries = [e for e in entries if e["key"] in wanted]
        missing = wanted - {e["key"] for e in entries}
        if missing:
            print(f"keys not in bib: {', '.join(sorted(missing))}", file=sys.stderr)
    if a.raw_dir:
        os.makedirs(a.raw_dir, exist_ok=True)
    ctx = Ctx(a.mailto, a.raw_dir, a.pause)

    rows = []
    for i, e in enumerate(entries, 1):
        r = check_entry(ctx, e, not a.no_search)
        rows.append(r)
        upd = r.get("updates", "")
        serious = any(t in upd for t in ("retraction", "withdrawal", "removal",
                                         "expression_of_concern"))
        flag = "  " if r["machine_check"] in ("MATCH", "NO_DOI_CANDIDATE") \
            and not serious else "!!"
        upd = f" | UPDATES: {upd}" if upd and "failed" not in upd else ""
        cand = f" | candidate {r['candidate_doi']}: {r.get('candidate_status', '')}" \
            if r.get("candidate_doi") else ""
        print(f"{flag} [{i}/{len(entries)}] {r['key']}: {r['machine_check']}"
              f"{' | ' + r['issues'] if r.get('issues') else ''}{upd}{cand}", flush=True)

    if a.out:
        if os.path.dirname(a.out):
            os.makedirs(os.path.dirname(a.out), exist_ok=True)
        with open(a.out, "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=COLUMNS, extrasaction="ignore")
            w.writeheader()
            for r in rows:
                w.writerow({c: r.get(c, "") for c in COLUMNS})
        print(f"Report: {a.out}")
    counts = {}
    for r in rows:
        counts[r["machine_check"]] = counts.get(r["machine_check"], 0) + 1
    updated = [r["key"] for r in rows if r.get("updates") and "failed" not in r["updates"]]
    print("Summary: " + ", ".join(f"{k}={v}" for k, v in sorted(counts.items())))
    if updated:
        print(f"Entries with retraction/correction notices: {', '.join(updated)}")
    if a.strict and (any(r["machine_check"] in ATTENTION for r in rows) or updated):
        sys.exit(1)


if __name__ == "__main__":
    main()
