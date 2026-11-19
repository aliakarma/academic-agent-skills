#!/usr/bin/env python3
"""Run one literature query and log it, so search counts are never typed by hand.

  python search.py "zero trust" "multi-agent" --purpose "comparators G2"
  python search.py "digital twin water distribution" --from-year 2024 --sort date
  python search.py --platform crossref "EPANET agent" --rows 10
  python search.py --platform arxiv 'abs:"prompt injection" AND abs:agent'
  python search.py --cites W4392 --purpose "forward snowball wang2026epanet"
  python search.py --refs 10.1016/j.watres.2026.125433 --purpose "backward snowball"
  python search.py --lookup 10.1016/j.watres.2026.125433,10.3390/rs18050685 --abstract

--lookup fetches OpenAlex records for known DOIs (max 50) and is not logged,
because it is not a search. Use it to read abstracts of screened sources.

Each run appends one row to literature/search_log.csv (search_id, date,
platform, exact query, filters, results_reported as the platform returned
it) and saves the raw response to literature/raw/searches/<search_id>.json.
It prints the hits with DOI, OpenAlex id, venue, and citation count.
--abstract also prints the abstract when the platform has one: that is
ABSTRACT access, not FULLTEXT.

Platforms: openalex (default, no key, small daily budget per IP), crossref,
arxiv (slow, allow 60 s). results_screened records the titles displayed. Quote
phrases in your shell as usual. Raise it by hand only if you screened more
(for example a second page).
"""
import argparse
import csv
import datetime
import json
import os
import re
import sys
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from litlib import SCHEMAS, get_json, http_get, q  # noqa: E402


def abstract_from_index(inv):
    if not inv:
        return ""
    pos = sorted((p, w) for w, ps in inv.items() for p in ps)
    return " ".join(w for _, w in pos)


def openalex(a, query, extra=None):
    filt = [extra] if extra else []
    if a.from_year:
        filt.append(f"from_publication_date:{a.from_year}-01-01")
    if a.to_year:
        filt.append(f"to_publication_date:{a.to_year}-12-31")
    if a.type:
        filt.append(f"type:{a.type}")
    if a.cites:
        filt.append(f"cites:{a.cites}")
    url = f"https://api.openalex.org/works?per-page={a.rows}"
    if query:
        url += f"&search={q(query)}"
    if filt:
        url += "&filter=" + ",".join(filt)
    if a.sort == "date":
        url += "&sort=publication_date:desc"
    elif a.sort == "cited":
        url += "&sort=cited_by_count:desc"
    st, js, txt = get_json(url)
    if not js:
        return url, None, [], f"HTTP {st}: {txt[:120]}"
    hits = [dict(year=w.get("publication_year"), title=w.get("title") or "",
                 venue=((w.get("primary_location") or {}).get("source") or {}).get("display_name") or "",
                 doi=(w.get("doi") or "").replace("https://doi.org/", ""),
                 oid=(w.get("id") or "").rsplit("/", 1)[-1],
                 cited=w.get("cited_by_count"), type=w.get("type"),
                 abstract=abstract_from_index(w.get("abstract_inverted_index")))
            for w in js.get("results", [])]
    return url, js.get("meta", {}).get("count"), hits, js


def openalex_refs(a):
    doi = a.refs.replace("https://doi.org/", "")
    st, js, txt = get_json(f"https://api.openalex.org/works/doi:{q(doi)}?select=id,referenced_works")
    if not js:
        return f"refs {doi}", None, [], f"HTTP {st}"
    ids = [r.rsplit("/", 1)[-1] for r in js.get("referenced_works", [])]
    hits = []
    for i in range(0, len(ids), 50):
        chunk = "|".join(ids[i:i + 50])
        _, page, _ = get_json(f"https://api.openalex.org/works?filter=openalex:{chunk}&per-page=50")
        for w in (page or {}).get("results", []):
            hits.append(dict(year=w.get("publication_year"), title=w.get("title") or "",
                             venue=((w.get("primary_location") or {}).get("source") or {}).get("display_name") or "",
                             doi=(w.get("doi") or "").replace("https://doi.org/", ""),
                             oid=w["id"].rsplit("/", 1)[-1], cited=w.get("cited_by_count"),
                             type=w.get("type"), abstract=""))
    return f"referenced_works of doi:{doi}", len(ids), hits, js


def crossref(a, query):
    url = f"https://api.crossref.org/works?query.bibliographic={q(query)}&rows={a.rows}"
    filt = []
    if a.from_year:
        filt.append(f"from-pub-date:{a.from_year}-01-01")
    if a.to_year:
        filt.append(f"until-pub-date:{a.to_year}-12-31")
    if filt:
        url += "&filter=" + ",".join(filt)
    st, js, txt = get_json(url, mailto=os.environ.get("CROSSREF_MAILTO"))
    if not js:
        return url, None, [], f"HTTP {st}: {txt[:120]}"
    m = js["message"]
    hits = [dict(year=(i.get("issued", {}).get("date-parts") or [[None]])[0][0],
                 title=" ".join(i.get("title") or []), venue=" ".join(i.get("container-title") or []),
                 doi=i.get("DOI", ""), oid="", cited=i.get("is-referenced-by-count"),
                 type=i.get("type"), abstract=re.sub(r"<[^>]+>", "", i.get("abstract", "")))
            for i in m.get("items", [])]
    return url, m.get("total-results"), hits, js


def arxiv(a, query):
    url = (f"https://export.arxiv.org/api/query?search_query={q(query)}"
           f"&max_results={a.rows}&sortBy={'submittedDate' if a.sort == 'date' else 'relevance'}")
    st, txt = http_get(url, accept="application/atom+xml", timeout=60)
    if st != 200:
        return url, None, [], f"HTTP {st}"
    ns = {"a": "http://www.w3.org/2005/Atom", "o": "http://a9.com/-/spec/opensearch/1.1/"}
    root = ET.fromstring(txt)
    total = root.findtext("o:totalResults", namespaces=ns)
    hits = []
    for e in root.findall("a:entry", ns):
        hits.append(dict(year=(e.findtext("a:published", "", ns) or "")[:4],
                         title=" ".join((e.findtext("a:title", "", ns) or "").split()),
                         venue="arXiv", doi="", oid=(e.findtext("a:id", "", ns) or "").rsplit("/", 1)[-1],
                         cited="", type="preprint",
                         abstract=" ".join((e.findtext("a:summary", "", ns) or "").split())))
    return url, int(total) if total else None, hits, {"raw_atom": txt}


def log_row(path, row):
    new = not os.path.exists(path) or os.path.getsize(path) == 0
    ids = []
    if not new:
        with open(path, newline="", encoding="utf-8") as fh:
            ids = [r["search_id"] for r in csv.DictReader(fh)]
    n = max([int(m.group(1)) for i in ids if (m := re.match(r"Q(\d+)", i))] or [0]) + 1
    row["search_id"] = f"Q{n:03d}"
    with open(path, "a", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=SCHEMAS["search_log.csv"])
        if new:
            w.writeheader()
        w.writerow(row)
    return row["search_id"]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("terms", nargs="*")
    ap.add_argument("--platform", default="openalex", choices=["openalex", "crossref", "arxiv"])
    ap.add_argument("--from-year", type=int)
    ap.add_argument("--to-year", type=int)
    ap.add_argument("--type", help="OpenAlex work type, e.g. article, review")
    ap.add_argument("--sort", choices=["relevance", "date", "cited"], default="relevance")
    ap.add_argument("--rows", type=int, default=15)
    ap.add_argument("--cites", help="OpenAlex W-id: forward snowball")
    ap.add_argument("--refs", help="DOI: backward snowball via OpenAlex")
    ap.add_argument("--purpose", default="")
    ap.add_argument("--abstract", action="store_true")
    ap.add_argument("--lit", default="literature")
    ap.add_argument("--no-log", action="store_true")
    ap.add_argument("--lookup", help="comma-separated DOIs: fetch records, no log")
    a = ap.parse_args()
    query = " ".join(a.terms)
    if a.lookup:
        src = a.lookup
        if src.startswith("@"):  # file of ids: avoids shell/batch-shim breakage on DOIs with ( ) or ;
            with open(src[1:], encoding="utf-8") as fh:
                src = ",".join(fh.read().split())
        ids = [d.strip().replace("https://doi.org/", "") for d in src.split(",") if d.strip()]
        # arXiv ids (2506.08837) and arXiv DOIs go to the arXiv API, which has abstracts OpenAlex lacks
        ax = [re.sub(r"(?i)^10\.48550/arxiv\.", "", i) for i in ids
              if re.match(r"(?i)^(10\.48550/arxiv\.)?\d{4}\.\d{4,5}(v\d+)?$", i)]
        dois = [i for i in ids if not re.match(r"(?i)^(10\.48550/arxiv\.)?\d{4}\.\d{4,5}(v\d+)?$", i)]
        hits = []
        a.rows, a.cites = 50, None
        if dois:
            _, total, h1, raw = openalex(a, "", extra="doi:" + "|".join(dois))
            print(f"OpenAlex lookup found={total}" + (f" FAILED {raw}" if isinstance(raw, str) else ""))
            if a.abstract:  # Crossref carries abstracts for MDPI, ACS, IEEE and others that OpenAlex lacks
                for h in h1:
                    if not h["abstract"] and h["doi"]:
                        _, cr, _ = get_json(f"https://api.crossref.org/works/{q(h['doi'])}",
                                            mailto=os.environ.get("CROSSREF_MAILTO"))
                        ab = re.sub(r"<[^>]+>", " ", ((cr or {}).get("message") or {}).get("abstract", ""))
                        if ab.strip():
                            h["abstract"] = "[Crossref] " + " ".join(ab.split())
            hits += h1
        if ax:
            st, txt = http_get("https://export.arxiv.org/api/query?id_list=" + ",".join(ax)
                               + f"&max_results={len(ax)}", accept="application/atom+xml", timeout=90)
            ns = {"a": "http://www.w3.org/2005/Atom", "x": "http://arxiv.org/schemas/atom"}
            entries = ET.fromstring(txt).findall("a:entry", ns) if st == 200 else []
            print(f"arXiv lookup found={len(entries)}" + ("" if st == 200 else f" FAILED HTTP {st}"))
            for e in entries:
                hits.append(dict(year=(e.findtext("a:published", "", ns) or "")[:10],
                                 title=" ".join((e.findtext("a:title", "", ns) or "").split()),
                                 venue="arXiv; journal_ref: " + (e.findtext("x:journal_ref", "", ns) or "none")
                                       + "; published DOI: " + (e.findtext("x:doi", "", ns) or "none"),
                                 doi="10.48550/arXiv." + re.sub(r"v\d+$", "", (e.findtext("a:id", "", ns) or "").rsplit("/", 1)[-1]),
                                 oid=(e.findtext("a:id", "", ns) or "").rsplit("/", 1)[-1],
                                 type="preprint; authors: " + ", ".join(x.findtext("a:name", "", ns) for x in e.findall("a:author", ns)),
                                 abstract=" ".join((e.findtext("a:summary", "", ns) or "").split())))
        for h in hits:
            print(f"- {h['year']} | {h['title']} | {h['venue']} | doi:{h['doi']} | {h['oid']} | {h['type']}")
            if a.abstract:
                print(f"  ABSTRACT: {h['abstract'] or '(none in OpenAlex)'}")
        return
    if not (query or a.cites or a.refs):
        ap.error("give search terms, --cites, or --refs")

    if a.refs:
        url, total, hits, raw = openalex_refs(a)
        platform, method = "OpenAlex API", "backward"
    elif a.platform == "openalex":
        url, total, hits, raw = openalex(a, query)
        platform, method = "OpenAlex API", "forward" if a.cites else "database"
    elif a.platform == "crossref":
        url, total, hits, raw = crossref(a, query)
        platform, method = "Crossref API", "database"
    else:
        url, total, hits, raw = arxiv(a, query)
        platform, method = "arXiv API", "database"

    failed = isinstance(raw, str)
    filters = " ".join(x for x in [f"from {a.from_year}" if a.from_year else "",
                                   f"to {a.to_year}" if a.to_year else "",
                                   f"type {a.type}" if a.type else "",
                                   f"cites {a.cites}" if a.cites else "",
                                   f"sort {a.sort}"] if x)
    sid = "-"
    if not a.no_log:
        sid = log_row(os.path.join(a.lit, "search_log.csv"), dict(
            date=datetime.date.today().isoformat(), platform=platform,
            query=a.refs or query, filters=filters,
            results_reported="" if total is None else total, results_screened=len(hits),
            discovery_method=method, purpose=a.purpose,
            notes=("FAILED: " + raw) if failed else url))
        os.makedirs(os.path.join(a.lit, "raw", "searches"), exist_ok=True)
        with open(os.path.join(a.lit, "raw", "searches", f"{sid}.json"), "w", encoding="utf-8") as fh:
            json.dump(raw if not failed else {"error": raw, "url": url}, fh)
    print(f"{sid} {platform} reported={total} shown={len(hits)}" + (f" FAILED {raw}" if failed else ""))
    for i, h in enumerate(hits, 1):
        print(f"{i:2d}. {h['year']} | {h['title'][:110]} | {h['venue'][:40]} | doi:{h['doi'] or '-'} | {h['oid']} | cites:{h['cited']}")
        if a.abstract and h["abstract"]:
            print(f"    ABSTRACT: {h['abstract'][:900]}")


if __name__ == "__main__":
    main()
