#!/usr/bin/env python3
"""Build BibTeX entries from DOI registration records, never from memory.

Fetches the Crossref record (DataCite for arXiv and other DataCite DOIs),
maps it to a clean BibTeX entry, LaTeX-escapes special characters (an
unescaped % in a .bib field silently truncates the rendered reference),
protects acronyms with braces, and generates an author-year-word key.

  python doi2bib.py 10.1145/2939672.2939778
  python doi2bib.py --file dois.txt --bib references.bib --append
  python doi2bib.py 10.1038/s42256-019-0048-x --key rudin2019stop

With --bib, DOIs already present in that file are skipped and new keys are
made unique against it. --append writes to the --bib file (a .bak copy is
made first). Without --append the entries are printed for review.

Always read the generated entry before using it. Crossref metadata has
known defects (missing pages, all-caps titles, conference years that
differ from proceedings years). Record any correction in the ledger.
"""
import argparse
import html
import json
import os
import re
import shutil
import sys
import unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import litlib  # noqa: E402

TYPE_MAP = {
    "journal-article": "article", "proceedings-article": "inproceedings",
    "book-chapter": "incollection", "book-section": "incollection",
    "book-part": "incollection", "reference-entry": "incollection",
    "book": "book", "monograph": "book", "edited-book": "book",
    "reference-book": "book", "report": "techreport",
    "dissertation": "phdthesis", "posted-content": "misc",
    "standard": "misc", "dataset": "misc",
}
STOP = {"a", "an", "the", "on", "of", "for", "in", "to", "and", "with", "via",
        "towards", "toward", "from", "at", "by", "is", "are", "why", "how",
        "what", "do", "does"}
SPECIAL = {"\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "$": r"\$",
           "#": r"\#", "_": r"\_", "{": r"\{", "}": r"\}",
           "~": r"\textasciitilde{}", "^": r"\textasciicircum{}"}


SERIES = re.compile(r"^(lecture notes in|communications in computer|advances in "
                    r"intelligent systems|studies in |smart innovation|springer "
                    r"proceedings|ifip advances|lecture notes of the institute)", re.I)


def tex_escape(s):
    s = "".join(SPECIAL.get(ch, ch) for ch in s)
    return s.replace("—", "---").replace("–", "--")


def clean_markup(s):
    s = re.sub(r"<[^>]+>", "", s or "")       # JATS <i>, <sub>, <mml:...>
    return " ".join(html.unescape(s).split())


def protect(title):
    """Brace words whose capitalization must survive the bib style."""
    out = []
    for w in title.split(" "):
        core = re.sub(r"[^\w]", "", w)
        if len(core) > 1 and (core.isupper() or re.search(r"[a-z][A-Z]", core)
                              or re.search(r"[A-Z].*\d|\d.*[A-Z]", core)):
            lead = re.match(r"^[^\w\\]*", w).group(0)
            trail = re.search(r"[^\w}]*$", w).group(0)
            mid = w[len(lead):len(w) - len(trail)] if trail else w[len(lead):]
            out.append(f"{lead}{{{mid}}}{trail}")
        else:
            out.append(w)
    return " ".join(out)


def ascii_word(s):
    s = unicodedata.normalize("NFKD", s)
    return re.sub(r"[^a-z]", "", "".join(c for c in s if not unicodedata.combining(c)).lower())


def make_key(family, year, title, taken):
    words = [ascii_word(w) for w in clean_markup(title).split()]
    word = next((w for w in words if w and w not in STOP), "x")
    base = f"{ascii_word(family) or 'anon'}{year or ''}{word}"
    key, n = base, 0
    while key.lower() in taken:
        n += 1
        key = base + "abcdefghijklmnopqrstuvwxyz"[n - 1]
    taken.add(key.lower())
    return key


def year_of(msg):
    for k in ("published-print", "published-online", "issued", "published"):
        parts = (msg.get(k) or {}).get("date-parts") or [[None]]
        if parts and parts[0] and parts[0][0]:
            return str(parts[0][0])
    return ""


def from_crossref(msg):
    etype = TYPE_MAP.get(msg.get("type", ""), "misc")
    authors = []
    for a in msg.get("author") or []:
        if a.get("family"):
            authors.append(tex_escape(f"{a['family']}, {a.get('given', '')}".strip(", ")))
        elif a.get("name"):
            authors.append("{" + tex_escape(a["name"]) + "}")
    editors = [tex_escape(f"{a.get('family', '')}, {a.get('given', '')}".strip(", "))
               for a in msg.get("editor") or [] if a.get("family")]
    title = clean_markup(" ".join(msg.get("title") or []))
    sub = clean_markup(" ".join(msg.get("subtitle") or []))
    if sub and sub.lower() not in title.lower():
        title = f"{title}: {sub}"
    containers = [clean_markup(c) for c in msg.get("container-title") or []]
    # Crossref lists LNCS-style series and the volume title in either order.
    containers.sort(key=lambda c: bool(SERIES.match(c)))
    f = {"author": " and ".join(authors), "title": protect(tex_escape(title)),
         "year": year_of(msg)}
    if etype == "article":
        f["journal"] = tex_escape(containers[0]) if containers else ""
    elif etype in ("inproceedings", "incollection"):
        f["booktitle"] = tex_escape(containers[0]) if containers else ""
        if len(containers) > 1:
            f["series"] = tex_escape(containers[1])
        if editors:
            f["editor"] = " and ".join(editors)
    elif etype == "techreport":
        f["institution"] = tex_escape(msg.get("publisher", ""))
    elif etype == "phdthesis":
        inst = (msg.get("institution") or [{}])[0].get("name", "")
        f["school"] = tex_escape(inst)
    elif etype == "misc" and msg.get("type") == "posted-content":
        f["howpublished"] = "Preprint" + (f", {tex_escape(msg.get('publisher', ''))}"
                                          if msg.get("publisher") else "")
    f["volume"] = msg.get("volume", "")
    f["number"] = msg.get("issue", "")
    pages = msg.get("page", "") or msg.get("article-number", "")
    f["pages"] = re.sub(r"\s*[-–]\s*", "--", pages)
    if etype in ("book", "incollection", "inproceedings", "misc") and msg.get("publisher"):
        f["publisher"] = tex_escape(msg["publisher"])
    if msg.get("ISBN") and etype in ("book", "incollection"):
        f["isbn"] = msg["ISBN"][0]
    f["doi"] = msg.get("DOI", "")
    f["url"] = "https://doi.org/" + msg.get("DOI", "")
    first = (msg.get("author") or [{}])[0]
    return etype, f, first.get("family") or first.get("name") or "", title


def from_datacite(data):
    at = data.get("attributes", {})
    rtype = (at.get("types") or {}).get("resourceTypeGeneral", "")
    authors = []
    for c in at.get("creators") or []:
        if c.get("familyName"):
            authors.append(tex_escape(f"{c['familyName']}, {c.get('givenName', '')}".strip(", ")))
        elif c.get("name"):
            authors.append("{" + tex_escape(c["name"]) + "}")
    title = clean_markup((at.get("titles") or [{}])[0].get("title", ""))
    doi = at.get("doi", "")
    f = {"author": " and ".join(authors), "title": protect(tex_escape(title)),
         "year": str(at.get("publicationYear") or ""), "doi": doi,
         "url": "https://doi.org/" + doi}
    m = re.match(r"10\.48550/arxiv\.(.+)", doi, re.I)
    if m:
        f["howpublished"] = f"arXiv preprint arXiv:{m.group(1)}"
        f["eprint"], f["archiveprefix"] = m.group(1), "arXiv"
    else:
        f["publisher"] = tex_escape(at.get("publisher") or "")
        if rtype:
            f["note"] = tex_escape(rtype)
    first = (at.get("creators") or [{}])[0]
    return "misc", f, first.get("familyName") or first.get("name") or "", title


def fetch(doi, mailto):
    url = f"https://api.crossref.org/works/{litlib.q(doi)}" + (
        f"?mailto={litlib.q(mailto)}" if mailto else "")
    status, data, text = litlib.get_json(url, mailto=mailto)
    if status == 200 and data:
        return ("crossref",) + from_crossref(data["message"])
    status2, data2, _ = litlib.get_json(f"https://api.datacite.org/dois/{litlib.q(doi)}")
    if status2 == 200 and data2:
        return ("datacite",) + from_datacite(data2["data"])
    raise LookupError(f"DOI {doi}: Crossref HTTP {status}, DataCite HTTP {status2}")


ORDER = ["author", "editor", "title", "journal", "booktitle", "series",
         "howpublished", "school", "institution", "volume", "number", "pages",
         "year", "publisher", "isbn", "eprint", "archiveprefix", "note",
         "doi", "url"]


def render(etype, key, f):
    lines = [f"@{etype}{{{key},"]
    for name in ORDER:
        if f.get(name):
            lines.append(f"  {name} = {{{f[name]}}},")
    lines[-1] = lines[-1].rstrip(",")
    lines.append("}")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawTextHelpFormatter)
    ap.add_argument("dois", nargs="*")
    ap.add_argument("--file", help="text file with one DOI per line")
    ap.add_argument("--bib", help="existing .bib for duplicate/key checks")
    ap.add_argument("--append", action="store_true", help="append to --bib")
    ap.add_argument("--key", help="explicit key (single DOI only)")
    ap.add_argument("--mailto", default=os.environ.get("CROSSREF_MAILTO"))
    a = ap.parse_args()

    dois = [litlib.clean_doi(d) for d in a.dois]
    if a.file:
        with open(a.file, encoding="utf-8") as fh:
            dois += [litlib.clean_doi(l) for l in fh if l.strip() and not l.startswith("#")]
    if not dois:
        ap.error("no DOIs given")
    if a.key and len(dois) != 1:
        ap.error("--key needs exactly one DOI")
    if a.append and not a.bib:
        ap.error("--append needs --bib")

    taken, have = set(), {}
    if a.bib and os.path.exists(a.bib):
        for e in litlib.load_bib(a.bib):
            taken.add(e["key"].lower())
            d = litlib.clean_doi(e["fields"].get("doi", ""))
            if d:
                have[d] = e["key"]

    out, failures = [], 0
    for doi in dois:
        if doi in have:
            print(f"% skip {doi}: already in bib as {have[doi]}", file=sys.stderr)
            continue
        try:
            src, etype, f, family, title = fetch(doi, a.mailto)
        except LookupError as exc:
            failures += 1
            print(f"% FAILED {exc}", file=sys.stderr)
            continue
        key = a.key or make_key(family, f.get("year"), title, taken)
        have[doi] = key
        out.append(f"% source: {src} record for doi:{doi}\n" + render(etype, key, f))

    text = "\n\n".join(out)
    if a.append and out:
        shutil.copyfile(a.bib, a.bib + ".bak")
        with open(a.bib, "a", encoding="utf-8") as fh:
            fh.write("\n\n" + text + "\n")
        print(f"Appended {len(out)} entries to {a.bib} (backup: {a.bib}.bak)",
              file=sys.stderr)
    else:
        print(text)
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
