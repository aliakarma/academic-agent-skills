#!/usr/bin/env python3
"""Fetch registry metadata for one BibTeX entry and diff it field by field.

Evidence aid only. It never writes a corrected entry and never decides a status.
Sources: doi.org handle API (resolution without touching the publisher),
doi.org RA lookup, Crossref, DataCite, arXiv. Title search is Crossref only.

Usage:
  python fetch_metadata.py entry.bib          # first entry in the file
  python fetch_metadata.py - < entry.bib      # stdin
  python fetch_metadata.py --doi 10.1145/3292500.3330701
  python fetch_metadata.py --arxiv 1706.03762
  python fetch_metadata.py --selftest         # offline parser/diff tests
"""
import json
import re
import sys
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

UA = "reference-verify/1.0 (bibliographic verification script)"
TIMEOUT = 20

CROSSREF_TYPE = {
    "journal-article": "article", "proceedings-article": "inproceedings",
    "book-chapter": "incollection", "book": "book", "monograph": "book",
    "edited-book": "book", "reference-book": "book", "report": "techreport",
    "posted-content": "misc (preprint)", "dataset": "misc (dataset)",
    "dissertation": "phdthesis / mastersthesis", "standard": "misc / techreport (standard)",
    "proceedings": "proceedings", "book-section": "incollection",
}


# ---------- BibTeX parsing (single entry, enough for verification) ----------

def parse_bibtex(text):
    m = re.search(r"@(\w+)\s*([{(])\s*([^,\s]*)\s*,", text)
    if not m:
        raise ValueError("no BibTeX entry found")
    etype, key = m.group(1).lower(), m.group(3)
    close = "}" if m.group(2) == "{" else ")"
    i, n, fields = m.end(), len(text), {}
    while i < n:
        while i < n and text[i] in " \t\r\n,":
            i += 1
        if i >= n or text[i] == close:
            break
        fm = re.match(r"([\w\-:.]+)\s*=\s*", text[i:])
        if not fm:
            raise ValueError(f"cannot parse field near: {text[i:i+40]!r}")
        name, i = fm.group(1).lower(), i + fm.end()
        parts = []
        while True:
            if i >= n:
                raise ValueError(f"field {name} has no value")
            if text[i] == "{":
                depth, j = 0, i
                while j < n:
                    if text[j] == "{" and text[j - 1] != "\\":
                        depth += 1
                    elif text[j] == "}" and text[j - 1] != "\\":
                        depth -= 1
                        if depth == 0:
                            break
                    j += 1
                if depth:
                    raise ValueError(f"unbalanced braces in field {name}")
                parts.append(text[i + 1:j]); i = j + 1
            elif text[i] == '"':
                j = i + 1
                while j < n and not (text[j] == '"' and text[j - 1] != "\\"):
                    j += 1
                if j >= n:
                    raise ValueError(f"unterminated quote in field {name}")
                parts.append(text[i + 1:j]); i = j + 1
            else:
                vm = re.match(r"[^,#}\s)]+", text[i:])
                if not vm:
                    raise ValueError(f"field {name} has no value")
                parts.append(vm.group(0)); i += vm.end()
            k = i
            while k < n and text[k] in " \t\r\n":
                k += 1
            if k < n and text[k] == "#":
                i = k + 1
                while i < n and text[i] in " \t\r\n":
                    i += 1
                continue
            break
        fields[name] = "".join(parts)
    if i >= n or text[i] != close:
        raise ValueError("entry is not closed (a field brace or quote is probably unbalanced)")
    return etype, key, fields


# ---------- normalisation ----------

ACCENT = {'"': "\u0308", "'": "\u0301", "`": "\u0300", "^": "\u0302", "~": "\u0303",
          "c": "\u0327", "v": "\u030c", "u": "\u0306", "=": "\u0304", ".": "\u0307",
          "H": "\u030b", "k": "\u0328", "r": "\u030a"}
SPECIAL = {r"\ss": "ss", r"\o": "o", r"\O": "O", r"\l": "l", r"\L": "L",
           r"\ae": "ae", r"\AE": "AE", r"\oe": "oe", r"\i": "i", r"\&": "&"}


def delatex(s):
    s = s or ""
    s = re.sub(r"\\([\"'`^~=.Hcvukr])\s*\{?\\?([A-Za-z])\}?",
               lambda m: unicodedata.normalize("NFC", m.group(2) + ACCENT[m.group(1)]), s)
    for k, v in SPECIAL.items():
        s = re.sub(re.escape(k) + r"(?![A-Za-z])", v, s)
    s = re.sub(r"\\[A-Za-z]+\s*", " ", s)
    s = s.replace("{", "").replace("}", "").replace("~", " ")
    return re.sub(r"\s+", " ", s).strip()


def norm(s):
    s = unicodedata.normalize("NFKD", delatex(s))
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r"<[^>]+>", " ", s)  # Crossref JATS tags such as <i>
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def bib_families(author_field):
    out = []
    for a in re.split(r"\s+and\s+", delatex(author_field or "")):
        a = a.strip()
        if not a:
            continue
        if a.lower() == "others":
            out.append("others")
        elif "," in a:
            out.append(a.split(",")[0].strip())
        else:
            toks = a.split()
            # keep lowercase particles with the surname (van der Berg, de la Cruz)
            k = len(toks) - 1
            while k > 0 and toks[k - 1][:1].islower():
                k -= 1
            out.append(" ".join(toks[k:]))
    return out


def norm_pages(p):
    return re.sub(r"\s*[-\u2013\u2014]+\s*", "-", (p or "").strip())


# ---------- network ----------

def get(url, accept="application/json"):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": accept})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            return r.status, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, ""
    except Exception as e:  # network down, DNS, timeout
        return None, str(e)


def doi_resolution(doi):
    q = urllib.parse.quote(doi, safe="/")
    st, body = get(f"https://doi.org/api/handles/{q}")
    info = {"handle_status": st, "registered_url": None, "agency": None}
    if st == 200:
        for v in json.loads(body).get("values", []):
            if v.get("type") == "URL":
                info["registered_url"] = v["data"]["value"]
    st2, body2 = get(f"https://doi.org/ra/{q}")
    if st2 == 200:
        try:
            info["agency"] = json.loads(body2)[0].get("RA")
        except Exception:
            pass
    return info


def crossref(doi):
    st, body = get("https://api.crossref.org/works/" + urllib.parse.quote(doi, safe="/"))
    return json.loads(body)["message"] if st == 200 else None


def datacite(doi):
    st, body = get("https://api.datacite.org/dois/" + urllib.parse.quote(doi, safe=""))
    return json.loads(body)["data"]["attributes"] if st == 200 else None


def arxiv(aid):
    st, body = get("https://export.arxiv.org/api/query?id_list=" + urllib.parse.quote(aid),
                   accept="application/atom+xml")
    if st != 200:
        return None
    ns = {"a": "http://www.w3.org/2005/Atom", "x": "http://arxiv.org/schemas/atom"}
    e = ET.fromstring(body).find("a:entry", ns)
    if e is None or e.find("a:title", ns) is None:
        return None
    return {
        "title": " ".join(e.find("a:title", ns).text.split()),
        "authors": [a.find("a:name", ns).text for a in e.findall("a:author", ns)],
        "published": e.find("a:published", ns).text,
        "updated": e.find("a:updated", ns).text,
        "id": e.find("a:id", ns).text,
        "journal_ref": getattr(e.find("x:journal_ref", ns), "text", None),
        "doi": getattr(e.find("x:doi", ns), "text", None),
    }


def crossref_search(title, author=""):
    q = urllib.parse.urlencode({"query.bibliographic": f"{title} {author}".strip(), "rows": 5})
    st, body = get("https://api.crossref.org/works?" + q)
    return json.loads(body)["message"]["items"] if st == 200 else []


# ---------- registry -> comparable record ----------

def from_crossref(m):
    yr = None
    for k in ("published-print", "published-online", "issued", "published"):
        dp = (m.get(k) or {}).get("date-parts") or [[None]]
        if dp[0] and dp[0][0]:
            yr = yr or str(dp[0][0])
    title = " ".join(m.get("title") or [])
    if m.get("subtitle"):
        title += ": " + " ".join(m["subtitle"])
    return {
        "source": "Crossref",
        "type": f'{m.get("type")} -> @{CROSSREF_TYPE.get(m.get("type"), "?")}',
        "authors": [a.get("family") or a.get("name") or "" for a in m.get("author") or []],
        "authors_full": [", ".join(x for x in (a.get("family") or a.get("name"), a.get("given")) if x)
                         for a in m.get("author") or []],
        "editors": [a.get("family", "") for a in m.get("editor") or []],
        "title": title,
        "container": " | ".join(m.get("container-title") or []),
        "year": yr,
        "dates": {k: (m.get(k) or {}).get("date-parts") for k in
                  ("published-print", "published-online", "issued") if m.get(k)},
        "volume": m.get("volume"), "issue": m.get("issue"),
        "pages": m.get("page"), "article_number": m.get("article-number"),
        "publisher": m.get("publisher"), "doi": m.get("DOI"),
        "isbn": m.get("ISBN"), "issn": m.get("ISSN"),
        "event": (m.get("event") or {}).get("name"),
        "url": (m.get("resource") or {}).get("primary", {}).get("URL"),
        "relations": list((m.get("relation") or {}).keys()),
        "update_to": [u.get("type") for u in m.get("update-to") or []],
    }


def from_datacite(a):
    pub = a.get("publisher")
    return {
        "source": "DataCite",
        "type": (a.get("types") or {}).get("resourceTypeGeneral"),
        "authors": [c.get("familyName") or c.get("name") or "" for c in a.get("creators") or []],
        "authors_full": [c.get("name", "") for c in a.get("creators") or []],
        "title": " ".join(t.get("title", "") for t in (a.get("titles") or [])[:1]),
        "container": (a.get("container") or {}).get("title"),
        "year": str(a.get("publicationYear") or ""),
        "publisher": pub if isinstance(pub, str) else (pub or {}).get("name"),
        "version": a.get("version"), "doi": a.get("doi"), "url": a.get("url"),
    }


def from_arxiv(x):
    return {
        "source": "arXiv",
        "type": "preprint -> @misc (or @article with journal = {arXiv preprint})",
        "authors": [n.split()[-1] for n in x["authors"]],
        "authors_full": x["authors"],
        "title": x["title"], "year": x["published"][:4],
        "dates": {"v1_submitted": x["published"], "last_updated": x["updated"]},
        "url": x["id"], "journal_ref": x["journal_ref"], "doi": x["doi"],
    }


# ---------- diff ----------

def verdict(a, b, cmp=norm):
    if not a and not b:
        return None
    if not a:
        return "REGISTRY-ONLY"
    if not b:
        return "BIB-ONLY"
    return "match" if cmp(a) == cmp(b) else "DIFF"


def diff(fields, rec):
    rows = []
    fam_b = [norm(x) for x in bib_families(fields.get("author"))]
    fam_r = [norm(x) for x in rec.get("authors") or []]
    if fam_b or fam_r:
        if fam_b == fam_r:
            v = "match"
        elif fam_b and fam_b[-1] == "others" and fam_b[:-1] == fam_r[:len(fam_b) - 1]:
            v = "TRUNCATED (and others)"
        elif sorted(fam_b) == sorted(fam_r):
            v = "DIFF (order)"
        elif not fam_r:
            v = "BIB-ONLY"
        else:
            v = f"DIFF (bib {len(fam_b)} vs registry {len(fam_r)})" if fam_b else "REGISTRY-ONLY"
        rows.append(("author", fields.get("author"), "; ".join(rec.get("authors_full") or []), v))
    rows.append(("title", fields.get("title"), rec.get("title"),
                 verdict(fields.get("title"), rec.get("title"))))
    cont = fields.get("journal") or fields.get("booktitle")
    if cont or rec.get("container"):
        v = verdict(cont, rec.get("container"))
        if v == "DIFF" and any(norm(cont) == norm(c) for c in rec["container"].split(" | ")):
            v = "match"
        rows.append(("journal/booktitle", cont, rec.get("container"), v))
    rows.append(("year", fields.get("year"), rec.get("year"), verdict(fields.get("year"), rec.get("year"))))
    rows.append(("volume", fields.get("volume"), rec.get("volume"),
                 verdict(fields.get("volume"), rec.get("volume"))))
    rows.append(("number", fields.get("number"), rec.get("issue"),
                 verdict(fields.get("number"), rec.get("issue"))))
    rows.append(("publisher", fields.get("publisher"), rec.get("publisher"),
                 verdict(fields.get("publisher"), rec.get("publisher"))))
    bdoi = re.sub(r"^(https?://)?(dx\.)?doi\.org/", "", fields.get("doi") or "", flags=re.I)
    rows.append(("doi", fields.get("doi"), rec.get("doi"),
                 verdict(bdoi, rec.get("doi"), lambda s: s.lower().strip())))
    pg_r = rec.get("pages") or rec.get("article_number")
    rows.append(("pages", fields.get("pages"), pg_r, verdict(fields.get("pages"), pg_r, norm_pages)))
    return [r for r in rows if r[3]]


def show(title, obj):
    print(f"\n== {title} ==")
    for k, v in obj.items():
        if v not in (None, "", [], {}):
            print(f"  {k:15} {v}")


def main(argv):
    if "--selftest" in argv:
        return selftest()
    fields = {}
    if "--doi" in argv:
        fields["doi"] = argv[argv.index("--doi") + 1]
    elif "--arxiv" in argv:
        fields["eprint"] = argv[argv.index("--arxiv") + 1]
    else:
        src = argv[1] if len(argv) > 1 else "-"
        text = sys.stdin.read() if src == "-" else open(src, encoding="utf-8").read()
        etype, key, fields = parse_bibtex(text)
        print(f"Entry: @{etype}{{{key}}}  fields: {', '.join(fields)}")

    doi = re.sub(r"^(https?://)?(dx\.)?doi\.org/", "", (fields.get("doi") or "").strip(), flags=re.I)
    if not doi:
        m = re.search(r"doi\.org/(10\.\S+)", fields.get("url", ""))
        doi = m.group(1) if m else ""
    aid = fields.get("eprint") or ""
    if not aid:
        m = re.search(r"arxiv\.org/(?:abs|pdf)/([\w.\-/]+?)(?:\.pdf)?$", fields.get("url", ""))
        aid = m.group(1) if m else ""
    if not aid and doi.lower().startswith("10.48550/arxiv."):
        aid = doi.split(".", 2)[2]

    records = []
    if doi:
        res = doi_resolution(doi)
        show(f"DOI resolution for {doi}", res)
        if res["handle_status"] == 404:
            print("  -> DOI is NOT registered at doi.org.")
        elif res["handle_status"] is None:
            print("  -> network failure, resolution not checked.")
        cr = crossref(doi)
        if cr:
            records.append(from_crossref(cr))
        else:
            dc = datacite(doi)
            if dc:
                records.append(from_datacite(dc))
    if aid:
        ax = arxiv(aid)
        if ax:
            records.append(from_arxiv(ax))
        else:
            print(f"\n arXiv id {aid}: no record returned")
    if not records and fields.get("title"):
        fam = bib_families(fields.get("author"))
        print("\nNo DOI/arXiv record. Crossref title search candidates (identity NOT established):")
        for it in crossref_search(delatex(fields["title"]), fam[0] if fam else ""):
            r = from_crossref(it)
            print(f"  - {r['doi']} | {r['year']} | {r['title'][:90]} | {r['container'][:50]} | "
                  f"{', '.join(r['authors'][:3])}")
        print("Re-run with --doi <DOI> only after confirming the candidate is the same work.")

    for rec in records:
        show(f"{rec['source']} record", {k: v for k, v in rec.items() if k != "source"})
        if fields.get("title") or fields.get("author"):
            print(f"\n-- field diff: bib vs {rec['source']} --")
            for f, b, r, v in diff(fields, rec):
                print(f"  [{v}] {f}\n      bib:      {b}\n      registry: {r}")
    if not records and not fields.get("title"):
        print("\nNothing to look up: no DOI, arXiv id, or title.")
    print("\nReminder: registry data is strong evidence, not the final word. Confirm on the "
          "publisher/venue page or the document itself before assigning a status.")
    return 0


def selftest():
    bib = r"""@inproceedings{k1,
      author = {M{\"u}ller, Hans and van der Berg, Anna and Li, Wei and others},
      title = "{Deep} Learning " # {for X},
      booktitle = {Proc. IEEE CVPR}, year = 2020, pages = {1--10},
      doi = {https://doi.org/10.1/ABC},
    }"""
    t, k, f = parse_bibtex(bib)
    assert (t, k) == ("inproceedings", "k1"), (t, k)
    assert f["year"] == "2020" and f["title"] == "{Deep} Learning for X", f
    assert bib_families(f["author"]) == ["Müller", "van der Berg", "Li", "others"], bib_families(f["author"])
    assert bib_families("Anna van der Berg and Juan de la Cruz") == ["van der Berg", "de la Cruz"]
    assert norm(r"G{\"o}del") == norm("Gödel") == "godel"
    assert norm_pages("1 -- 10") == norm_pages("1–10") == "1-10"
    rec = {"authors": ["Müller", "van der Berg", "Li", "Zhao"], "authors_full": [],
           "title": "Deep learning for <i>X</i>", "container": "CVPR", "year": "2021",
           "pages": "1-10", "doi": "10.1/abc"}
    d = {r[0]: r[3] for r in diff(f, rec)}
    assert d["author"] == "TRUNCATED (and others)", d
    assert d["title"] == "match" and d["year"] == "DIFF" and d["pages"] == "match", d
    assert d["doi"] == "match" and d["journal/booktitle"] == "DIFF", d
    for bad in ("@article{x, title = {open", '@article{x, title = "open', "no entry here"):
        try:
            parse_bibtex(bad)
            raise AssertionError(f"bad input accepted: {bad!r}")
        except ValueError:
            pass
    print("selftest: all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
