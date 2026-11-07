"""Shared helpers for the Literature-Review skill scripts (stdlib only).

BibTeX parsing, LaTeX citation extraction, text normalization, HTTP access
to scholarly metadata APIs, and the canonical column schemas for the
literature/ workspace files.
"""
import csv
import json
import os
import re
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
import sys
from difflib import SequenceMatcher

# Windows consoles default to cp1252, which mangles en dashes and accents.
for _stream in (sys.stdout, sys.stderr):
    _reconf = getattr(_stream, "reconfigure", None)
    if _reconf:
        try:
            _reconf(encoding="utf-8")
        except ValueError:
            pass

# ---------------------------------------------------------------- schemas
# Single source of truth for workspace file columns. init_workspace.py
# writes these headers and check_ledger.py validates against them.
SCHEMAS = {
    "search_log.csv": [
        "search_id", "date", "platform", "query", "filters",
        "results_reported", "results_screened", "discovery_method",
        "purpose", "notes",
    ],
    "source_ledger.csv": [
        "source_id", "title", "authors", "year", "venue", "pub_type",
        "doi", "url", "peer_review_status", "version_note",
        "verification_status", "verification_date", "verification_evidence",
        "access_level", "screening_decision", "exclusion_reason",
        "relevance", "themes", "cited_in_manuscript", "notes",
    ],
    "extraction_sheet.csv": [
        "source_id", "problem", "objectives", "theory", "method", "data",
        "metrics", "key_findings", "source_location", "author_limitations",
        "reviewer_limitations", "contributions", "relevance_to_manuscript",
        "evidence_strength", "conflicts", "uncertainty",
    ],
    "citation_map.csv": [
        "claim_id", "section", "location_hint", "claim_text", "claim_type",
        "source_ids", "support", "qualification", "priority", "status",
    ],
}

ENUMS = {
    "verification_status": {"VERIFIED", "VERIFIED-QUALIFIED", "UNRESOLVED",
                            "REJECTED", "PENDING"},
    "access_level": {"FULLTEXT", "ABSTRACT", "METADATA", ""},
    "screening_decision": {"candidate", "included", "excluded"},
    "peer_review_status": {"peer-reviewed", "preprint", "report", "standard",
                           "thesis", "book", "other", "unknown"},
    "relevance": {"essential", "useful", "optional", ""},
    "cited_in_manuscript": {"yes", "no"},
    "claim_type": {"definition", "fact", "method", "comparison", "result",
                   "limitation", "gap", "novelty"},
    "support": {"full", "partial"},
    "priority": {"essential", "useful", "optional"},
    "status": {"planned", "inserted", "dropped"},
}

CITABLE_STATUSES = {"VERIFIED", "VERIFIED-QUALIFIED"}


def read_csv(path):
    with open(path, newline="", encoding="utf-8-sig") as fh:
        return list(csv.DictReader(fh))


# ---------------------------------------------------------------- BibTeX
_FIELD_NAME = re.compile(r"\s*,?\s*([A-Za-z][\w:.+-]*)\s*=\s*")
_SKIP_TYPES = {"comment", "preamble", "string"}


def _parse_value(s, k):
    """Parse a field value starting at s[k]. Returns (raw_value, new_k)."""
    parts = []
    L = len(s)
    while k < L:
        while k < L and s[k].isspace():
            k += 1
        if k >= L:
            break
        c = s[k]
        if c == "{":
            depth, j = 0, k
            while j < L:
                if s[j] == "{":
                    depth += 1
                elif s[j] == "}":
                    depth -= 1
                    if depth == 0:
                        break
                j += 1
            parts.append(s[k + 1:j])
            k = j + 1
        elif c == '"':
            depth, j = 0, k + 1
            while j < L:
                if s[j] == "{":
                    depth += 1
                elif s[j] == "}":
                    depth -= 1
                elif s[j] == '"' and depth == 0:
                    break
                j += 1
            parts.append(s[k + 1:j])
            k = j + 1
        else:
            m = re.compile(r"[^,\s#}]+").match(s, k)
            if not m:
                break
            parts.append(m.group(0))
            k = m.end()
        while k < L and s[k].isspace():
            k += 1
        if k < L and s[k] == "#":
            k += 1
            continue
        break
    return "".join(parts), k


def parse_bib(text):
    """Return a list of entries: dict(type, key, fields, line, dup_fields)."""
    entries = []
    i, n = 0, len(text)
    head = re.compile(r"@\s*([A-Za-z]+)\s*([{(])")
    while True:
        at = text.find("@", i)
        if at < 0:
            break
        m = head.match(text, at)
        if not m:
            i = at + 1
            continue
        etype, open_ch = m.group(1).lower(), m.group(2)
        start, depth, j = m.end(), 0, m.end()
        while j < n:
            c = text[j]
            if c == "{":
                depth += 1
            elif c == "}":
                if depth == 0 and open_ch == "{":
                    break
                depth -= 1
            elif c == ")" and open_ch == "(" and depth == 0:
                break
            j += 1
        body = text[start:j]
        i = j + 1
        if etype in _SKIP_TYPES:
            continue
        comma = body.find(",")
        key = (body if comma < 0 else body[:comma]).strip()
        fields, dups = {}, []
        rest = "" if comma < 0 else body[comma:]
        k = 0
        while k < len(rest):
            fm = _FIELD_NAME.match(rest, k)
            if not fm:
                break
            name = fm.group(1).lower()
            val, k = _parse_value(rest, fm.end())
            if name in fields:
                dups.append(name)
            fields[name] = val
        entries.append({"type": etype, "key": key, "fields": fields,
                        "line": text.count("\n", 0, at) + 1,
                        "dup_fields": dups})
    return entries


def load_bib(path):
    with open(path, encoding="utf-8", errors="replace") as fh:
        return parse_bib(fh.read())


def split_authors(raw):
    """Split a BibTeX author string on top-level ' and '."""
    out, depth, cur = [], 0, []
    toks = re.split(r"(\{|\}|\s+and\s+)", raw or "")
    for t in toks:
        if t == "{":
            depth += 1
        elif t == "}":
            depth -= 1
        if depth == 0 and t and re.fullmatch(r"\s+and\s+", t):
            out.append("".join(cur).strip())
            cur = []
        else:
            cur.append(t)
    if "".join(cur).strip():
        out.append("".join(cur).strip())
    return out


def family_name(author):
    a = author.strip()
    if a.startswith("{") and a.endswith("}"):
        return a[1:-1]
    if "," in a:
        return a.split(",", 1)[0]
    parts = a.split()
    return parts[-1] if parts else a


# ---------------------------------------------------------------- text
_LATEX_ACCENT = re.compile(r"\\[`'^\"~=.uvHtcdbk]\s*\{?([A-Za-z])\}?")
_LATEX_CMD = re.compile(r"\\[A-Za-z]+\*?")


def norm(s):
    """Lowercase ASCII alphanumerics and single spaces, for comparison."""
    if not s:
        return ""
    s = re.sub(r"<[^>]+>", " ", s)            # JATS/HTML tags from Crossref
    s = _LATEX_ACCENT.sub(r"\1", s)
    s = _LATEX_CMD.sub(" ", s)
    s = unicodedata.normalize("NFKD", s)
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    s = re.sub(r"[^A-Za-z0-9]+", " ", s).lower()
    return re.sub(r"\s+", " ", s).strip()


def similarity(a, b):
    a, b = norm(a), norm(b)
    if not a or not b:
        return 0.0
    return SequenceMatcher(None, a, b).ratio()


def same_family(a, b):
    a, b = norm(a), norm(b)
    if not a or not b:
        return False
    return a == b or a in b or b in a


def clean_doi(doi):
    if not doi:
        return ""
    d = doi.strip()
    d = re.sub(r"^(https?://(dx\.)?doi\.org/|doi:\s*)", "", d, flags=re.I)
    return d.strip().strip("{}").lower()


# ---------------------------------------------------------------- LaTeX
_INCLUDE = re.compile(r"\\(?:input|include|subfile)\s*\{([^}]+)\}")
_BIBLIO = re.compile(r"\\bibliography\s*\{([^}]+)\}")
_ADDBIB = re.compile(r"\\addbibresource\s*(?:\[[^\]]*\])?\s*\{([^}]+)\}")
_CITE_CMD = re.compile(r"\\([A-Za-z]*cite[A-Za-z]*|nocite)\*?")


def strip_comments(line):
    return re.sub(r"(?<!\\)%.*", "", line)


def tex_files(main):
    """Main .tex plus every \\input/\\include reachable from it."""
    seen, order, missing = set(), [], []
    base = os.path.dirname(os.path.abspath(main))

    def visit(path):
        p = os.path.abspath(path)
        if p in seen:
            return
        if not os.path.exists(p):
            missing.append(path)
            return
        seen.add(p)
        order.append(p)
        with open(p, encoding="utf-8", errors="replace") as fh:
            for line in fh:
                for inc in _INCLUDE.findall(strip_comments(line)):
                    inc = inc.strip()
                    cand = os.path.join(base, inc)
                    if not os.path.splitext(cand)[1]:
                        cand += ".tex"
                    visit(cand)

    visit(main)
    return order, missing


def _skip_args(s, k):
    """Skip optional [..] and (..) groups. Returns new index."""
    while True:
        while k < len(s) and s[k].isspace():
            k += 1
        if k < len(s) and s[k] in "[(":
            close = "]" if s[k] == "[" else ")"
            j = s.find(close, k)
            if j < 0:
                return k
            k = j + 1
        else:
            return k


def extract_citations(main):
    """Return (citations, bib_files, nocite_all, missing_inputs).

    citations is a list of (key, file, line, command).
    """
    files, missing = tex_files(main)
    cites, bibs, nocite_all = [], [], False
    base = os.path.dirname(os.path.abspath(main))
    for f in files:
        with open(f, encoding="utf-8", errors="replace") as fh:
            lines = [strip_comments(l) for l in fh]
        for ln, line in enumerate(lines, 1):
            for b in _BIBLIO.findall(line):
                for name in b.split(","):
                    name = name.strip()
                    if name:
                        p = os.path.join(base, name)
                        bibs.append(p if p.endswith(".bib") else p + ".bib")
            for b in _ADDBIB.findall(line):
                bibs.append(os.path.join(base, b.strip()))
            for m in _CITE_CMD.finditer(line):
                cmd = m.group(1)
                multi = cmd.endswith("cites")
                k = m.end()
                while True:
                    k = _skip_args(line, k)
                    if k < len(line) and line[k] == "{":
                        j = line.find("}", k)
                        if j < 0:
                            break
                        for key in line[k + 1:j].split(","):
                            key = key.strip()
                            if key == "*" and cmd == "nocite":
                                nocite_all = True
                            elif key:
                                cites.append((key, f, ln, cmd))
                        k = j + 1
                        if not multi:
                            break
                    else:
                        break
    seen, uniq = set(), []
    for b in bibs:
        if os.path.abspath(b) not in seen:
            seen.add(os.path.abspath(b))
            uniq.append(b)
    return cites, uniq, nocite_all, missing


# ---------------------------------------------------------------- HTTP
USER_AGENT = "LiteratureReviewSkill/1.0"


def http_get(url, accept="application/json", mailto=None, retries=3,
             timeout=30):
    """GET a URL. Returns (status, text). Retries on 429/5xx with backoff."""
    ua = USER_AGENT + (f" (mailto:{mailto})" if mailto else "")
    req = urllib.request.Request(url, headers={"User-Agent": ua,
                                               "Accept": accept})
    delay = 2.0
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.status, r.read().decode("utf-8", errors="replace")
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504) and attempt < retries:
                time.sleep(delay)
                delay *= 2
                continue
            body = ""
            try:
                body = e.read().decode("utf-8", errors="replace")
            except Exception:
                pass
            return e.code, body
        except (urllib.error.URLError, TimeoutError, OSError) as e:
            if attempt < retries:
                time.sleep(delay)
                delay *= 2
                continue
            return 0, f"network error: {e}"
    return 0, "network error"


def get_json(url, **kw):
    status, text = http_get(url, **kw)
    if status != 200:
        return status, None, text
    try:
        return status, json.loads(text), text
    except ValueError:
        return status, None, text


def q(s):
    return urllib.parse.quote(s, safe="")
