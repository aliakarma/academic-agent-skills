#!/usr/bin/env python3
"""Verify every field of every entry in a .bib file against public registries.

Whole-file triage for the reference-verify skill. Sources: CrossRef, DataCite,
OpenAlex, Europe PMC, DBLP, OpenLibrary, arXiv, DOI content negotiation, and
publisher pages that serve their own BibTeX (PMLR, ACL Anthology).

Two rules keep it from corrupting a good .bib:
  1. Only identity-confirmed records (matched by DOI, publisher page, ISBN, or a
     near-identical distinctive title) may donate a value.
  2. Disagreement is reported, never resolved: the field becomes REVIEW.

Report-only by default. --apply edits only the fields it corrects, in place,
keeps the original as <file>.orig.bak, and adds "% bibverify:" comments above
entries that still need a human.

Usage:
  python verify_bib.py refs.bib                       # report only
  python verify_bib.py refs.bib --email name@example.com --apply
  python verify_bib.py a.bib b.bib --no-urls --workers 8

Exit status: 0 = no entry needs attention, 1 = some entry is REVIEW, PROBLEM,
UNVERIFIED or ERROR, 2 = usage error. Requires bibtexparser 1.x and requests.
"""
CONTACT_EMAIL = ""   # polite-pool identifier sent to CrossRef/OpenAlex
BACKUP_SUFFIX = ".orig.bak"                # original preserved alongside the corrected file

APPLY_CORRECTIONS = False   # True = write corrections back to the .bib (CLI: --apply)
ANNOTATE_BIB      = True    # write "% bibverify:" provenance comments into the .bib
                            # so nothing unverified can leave without a visible flag
CHECK_URLS        = True    # live-fetch every url field
USE_CACHE         = True    # cache API responses between runs
CACHE_PATH        = ".bibverify_cache.json"
REPORT_PREFIX     = "verification_report"
WORKERS           = 6       # entries verified in parallel (per-host rate limits still apply)

ACCEPT_THRESHOLD = 0.90     # title similarity >= this -> confident match
REVIEW_THRESHOLD = 0.75     # between -> manual review; below -> reject
DONOR_THRESHOLD  = 0.97     # title similarity required to donate a field value
YEAR_TOLERANCE   = 1        # allowed |entry_year - registry_year| before flagging

MAX_RETRIES  = 3
HTTP_TIMEOUT = 30

# Corrected automatically when identity-confirmed and no trusted source disagrees.
AUTO_APPLY_FIELDS = {'doi', 'journal', 'volume', 'number', 'pages', 'author',
                     'year', 'title'}
# Proposed but never written: venue strings and URLs vary legitimately between a
# registry's form and the one your journal's style wants.
PROPOSE_ONLY_FIELDS = {'booktitle', 'series', 'url', 'howpublished', 'note',
                       'publisher', 'issn', 'isbn', 'edition', 'school',
                       'institution', 'address', 'editor'}

RETRACTION_TYPES = {'retraction', 'withdrawal', 'removal', 'expression_of_concern',
                    'expression-of-concern'}

DOI_OPTIONAL_TYPES = {'techreport', 'misc', 'manual', 'online', 'unpublished',
                      'booklet', 'dataset', 'software', 'patent', 'standard'}

# Optional: a JSON file of extra venue synonym groups, e.g.
#   [["my workshop on x", "mwx"], ["journal of foo", "j. foo"]]
VENUE_ALIAS_FILE = "venue_aliases.json"


import re, os, sys, json, time, difflib, unicodedata, shutil, threading, csv
from collections import Counter
from urllib.parse import quote, urlencode, urlparse

try:
    import requests
    import bibtexparser
    from bibtexparser.bparser import BibTexParser   # 1.x API; removed in 2.x
except ImportError:
    sys.exit('verify_bib.py needs bibtexparser 1.x and requests:\n'
             '  python -m pip install "bibtexparser>=1.4,<2" "requests>=2.28,<3"')


def user_agent():
    return 'reference-verify-bib/1.0' + (f' (mailto:{CONTACT_EMAIL})' if CONTACT_EMAIL else '')

# ---------- LaTeX <-> Unicode ----------
_ACCENT_CMDS = {'`': '\u0300', "'": '\u0301', '^': '\u0302', '"': '\u0308',
                '~': '\u0303', '=': '\u0304', '.': '\u0307', 'v': '\u030c',
                'u': '\u0306', 'H': '\u030b', 'c': '\u0327', 'k': '\u0328',
                'r': '\u030a', 'd': '\u0323', 'b': '\u0331', 't': '\u0361'}
_SPECIALS = {r'\ss': '\u00df', r'\i': 'i', r'\j': 'j', r'\o': '\u00f8',
             r'\O': '\u00d8', r'\l': '\u0142', r'\L': '\u0141',
             r'\ae': '\u00e6', r'\AE': '\u00c6', r'\aa': '\u00e5',
             r'\AA': '\u00c5', r'\oe': '\u0153', r'\OE': '\u0152',
             r'\th': '\u00fe', r'\TH': '\u00de', r'\dh': '\u00f0',
             r'\DH': '\u00d0', r'\ng': '\u014b',
             r'\&': '&', r'\%': '%', r'\_': '_', r'\#': '#', r'\$': '$',
             r'\{': '{', r'\}': '}', r'\textendash': '\u2013',
             r'\textemdash': '\u2014', r'\textquotesingle': "'"}


def latex_to_text(s):
    """Render a BibTeX field as plain Unicode text."""
    if not s:
        return ''
    s = str(s)
    for cmd, comb in _ACCENT_CMDS.items():
        c = re.escape(cmd)
        s = re.sub(r'\\' + c + r'\s*\{\\?([A-Za-z])\}',
                   lambda m, cb=comb: m.group(1) + cb, s)
        s = re.sub(r'\\' + c + r'\\?([A-Za-z])',
                   lambda m, cb=comb: m.group(1) + cb, s)
    for k in sorted(_SPECIALS, key=len, reverse=True):
        s = s.replace(k + '{}', _SPECIALS[k]).replace(k, _SPECIALS[k])
    s = re.sub(r'\\[A-Za-z]+\s*', ' ', s)
    s = s.replace('{', '').replace('}', '').replace('\\', ' ')
    s = unicodedata.normalize('NFC', s)
    return re.sub(r'\s+', ' ', s).strip()


_REV_ACCENT = {v: k for k, v in _ACCENT_CMDS.items()}
_REV_SPECIAL = {v: k for k, v in _SPECIALS.items()
                if len(v) == 1 and not v.isascii()}


def text_to_latex(s):
    """Encode Unicode as portable BibTeX (accents as \\'e, ampersand as \\&)."""
    if not s:
        return ''
    out = []
    for ch in unicodedata.normalize('NFD', str(s)):
        if unicodedata.combining(ch):
            cmd = _REV_ACCENT.get(ch)
            if cmd and out:
                out.append('{\\%s{%s}}' % (cmd, out.pop()))
            continue
        out.append(_REV_SPECIAL.get(ch, ch))
    s = ''.join(out)
    for a, b in (('&', r'\&'), ('%', r'\%'), ('#', r'\#'), ('_', r'\_')):
        s = re.sub(r'(?<!\\)' + re.escape(a), b, s)
    s = s.replace('\u2013', '--').replace('\u2014', '---')
    s = s.replace('\u2018', '`').replace('\u2019', "'")
    s = s.replace('\u201c', '``').replace('\u201d', "''")
    return s


def protect_caps(title_text):
    """Brace-protect acronyms and CamelCase so BibTeX styles keep their case."""
    def fix(tok):
        core = re.sub(r'[^A-Za-z0-9\-]', '', tok)
        if len(core) >= 2 and core.isupper():
            return tok.replace(core, '{%s}' % core, 1)
        if re.match(r'^[A-Z][a-z]*[A-Z][A-Za-z]*$', core):
            return tok.replace(core, '{%s}' % core, 1)
        return tok
    return ' '.join(fix(t) for t in title_text.split())


def strip_accents(s):
    return ''.join(c for c in unicodedata.normalize('NFD', str(s))
                   if not unicodedata.combining(c))


def normalize_title(t):
    t = strip_accents(latex_to_text(t)).lower()
    t = re.sub(r'[^a-z0-9 ]', ' ', t)
    return re.sub(r'\s+', ' ', t).strip()


def title_match_score(a_raw, b_raw):
    a, b = normalize_title(a_raw), normalize_title(b_raw)
    if not a or not b:
        return 0.0
    ratio = difflib.SequenceMatcher(None, a, b).ratio()
    # Containment counts only when the shorter string is substantial, which is
    # what a truncated registry title looks like. A short generic title inside a
    # long unrelated one must NOT score as a match.
    short, long_ = (a, b) if len(a) <= len(b) else (b, a)
    if len(short.split()) >= 5 and short in long_:
        ratio = max(ratio, 0.95)
    return ratio


def parse_year(y):
    m = re.search(r'(\d{4})', str(y) if y is not None else '')
    return int(m.group(1)) if m else None


# ---------- names ----------
def split_bib_authors(field):
    """Split a BibTeX name list on ' and ' at brace depth zero."""
    if not field:
        return []
    parts, depth, cur = [], 0, ''
    for tok in re.split(r'(\{|\}|\s+and\s+)', field):
        if tok is None:
            continue
        if tok == '{':
            depth += 1
            cur += tok
        elif tok == '}':
            depth -= 1
            cur += tok
        elif re.fullmatch(r'\s+and\s+', tok) and depth == 0:
            parts.append(cur)
            cur = ''
        else:
            cur += tok
    parts.append(cur)
    return [p.strip() for p in parts if p.strip()]


PARTICLES = {'van', 'von', 'de', 'del', 'della', 'da', 'di', 'du', 'la', 'le',
             'den', 'der', 'ten', 'ter', 'dos', 'das', 'y', 'bin', 'ibn',
             'al', 'el', 'abu', 'st', 'mac', 'mc', 'op', 'ten'}


def parse_name(raw):
    """-> (family, given) as plain text, handling 'Family, Given' and 'Given Family'."""
    t = latex_to_text(raw)
    if ',' in t:
        fam, _, giv = t.partition(',')
        return fam.strip(), giv.strip()
    toks = t.split()
    if not toks:
        return '', ''
    i = len(toks) - 1
    while i > 0 and toks[i - 1].lower().strip('.') in PARTICLES:
        i -= 1
    return ' '.join(toks[i:]).strip(), ' '.join(toks[:i]).strip()


def norm_family(fam):
    return re.sub(r'[^a-z]', '', strip_accents(fam).lower())


def initials(given):
    return ''.join(w[0].lower() for w in re.split(r'[\s\-.]+', strip_accents(given)) if w)


def name_key(fam, giv):
    """Order-free identity of a person: substantive name tokens, initials dropped.

    Makes 'McMahan, H. Brendan' == 'Brendan McMahan',
    'El Mhamdi, El Mahdi' == 'El Mahdi El Mhamdi', and
    'Aguera y Arcas, Blaise' == 'Blaise Aguera y Arcas' - immune to where a
    given registry puts the family/given boundary.
    """
    toks = re.split(r'[^A-Za-z]+', strip_accents(f'{fam} {giv}').lower())
    return frozenset(t for t in toks if len(t) > 1)


def same_person(a, b):
    ka, kb = name_key(*a), name_key(*b)
    if not ka or not kb:
        return False
    if ka == kb:
        return True
    return (ka <= kb or kb <= ka) and bool(ka & kb)


def fmt_author_field(authors):
    """[(family, given)] -> BibTeX 'Family, Given and ...'"""
    out = []
    for fam, giv in authors:
        fam_t, giv_t = text_to_latex(fam), text_to_latex(giv)
        out.append(f'{fam_t}, {giv_t}' if giv_t else '{%s}' % fam_t)
    return ' and '.join(out)


def norm_pages(p):
    if not p:
        return ''
    p = re.sub(r'\s', '', str(p)).replace('\u2013', '-')
    p = re.sub(r'-+', '-', p)
    m = re.match(r'^([\w.]+)-([\w.]+)$', p)
    return f'{m.group(1)}--{m.group(2)}' if m else p


def clean_doi(raw):
    if not raw:
        return None
    d = str(raw).strip()
    d = re.sub(r'^https?://(dx\.)?doi\.org/', '', d, flags=re.I)
    d = re.sub(r'^doi:\s*', '', d, flags=re.I)
    d = d.strip().rstrip('.').strip('{} ')
    return d if d.lower().startswith('10.') else None


def is_arxiv_doi(d):
    return bool(d) and d.lower().startswith('10.48550/')


def prefer_doi_case(doi, candidates):
    """DOIs are case-insensitive, but CrossRef/OpenAlex lowercase them while
    publishers register mixed case. Prefer the registered form."""
    if not doi:
        return doi
    same = [c for c in candidates if c and c.lower() == doi.lower()]
    mixed = [c for c in same if c != c.lower()]
    out = mixed[0] if mixed else doi
    return re.sub(r'^10\.48550/arxiv\.', '10.48550/arXiv.', out, flags=re.I)


# ---------- venue / container comparison ----------
STOPWORDS = {'of', 'on', 'the', 'and', 'in', 'for', 'a', 'an', 'at', 'to'}


def norm_container(c):
    c = strip_accents(latex_to_text(c)).lower()
    c = re.sub(r'\b(proceedings of the|proceedings of|proceedings|proc\.?|the|'
               r'conference on|conference|international|intl\.?|annual|'
               r'\d+(st|nd|rd|th))\b', ' ', c)
    c = re.sub(r'[^a-z0-9 ]', ' ', c)
    return re.sub(r'\s+', ' ', c).strip()


def _acronym(s):
    # Built from the unstripped words: norm_container drops "international" and
    # "conference", which would turn ICML's expansion into "ml".
    words = re.sub(r'[^a-z0-9 ]', ' ', strip_accents(latex_to_text(s)).lower()).split()
    return ''.join(w[0] for w in words
                   if w not in STOPWORDS and w not in ('proceedings', 'proc')
                   and not re.fullmatch(r'\d+(st|nd|rd|th)?', w))


def _load_venue_aliases():
    groups = []
    if VENUE_ALIAS_FILE and os.path.exists(VENUE_ALIAS_FILE):
        try:
            for g in json.load(open(VENUE_ALIAS_FILE, encoding='utf-8')):
                groups.append({norm_container(x) for x in g})
            print(f'Loaded {len(groups)} venue alias groups from {VENUE_ALIAS_FILE}')
        except Exception as e:
            print('Could not read', VENUE_ALIAS_FILE, '-', e)
    return groups


VENUE_ALIASES = _load_venue_aliases()


def container_equiv(a, b):
    """True when two venue/journal strings denote the same publication.

    Generic by construction - acronyms, abbreviations, and word-subset matching
    - so it needs no per-field venue table. VENUE_ALIAS_FILE only adds
    exceptions that no rule can derive (e.g. a venue that was renamed).
    """
    na, nb = norm_container(a), norm_container(b)
    if not na or not nb:
        return False
    if na == nb or na in nb or nb in na:
        return True
    for group in VENUE_ALIASES:
        if any(g in na or na in g for g in group) and \
           any(g in nb or nb in g for g in group):
            return True
    # acronym vs expansion: "ICML" == "International Conference on Machine Learning"
    if na.replace(' ', '') == _acronym(b) or nb.replace(' ', '') == _acronym(a):
        return True
    ta, tb = na.split(), nb.split()
    # abbreviation forms: "IEEE Commun. Mag." == "IEEE Communications Magazine"
    if len(ta) == len(tb) and all(x.startswith(y) or y.startswith(x)
                                  for x, y in zip(ta, tb)):
        return True
    sa = {t for t in ta if len(t) > 3 and t not in STOPWORDS}
    sb = {t for t in tb if len(t) > 3 and t not in STOPWORDS}
    if sa and sb and (sa <= sb or sb <= sa):
        return True
    # an acronym embedded in the long form: "... (NeurIPS)" vs "NeurIPS"
    short, long_ = (na, nb) if len(na) <= len(nb) else (nb, na)
    return len(short) >= 3 and ' ' not in short and short in long_.split()




_cache = {}
_cache_lock = threading.Lock()
_cache_dirty = False
CACHE_TTL_DAYS = 30         # registry records change (corrections, retractions)


def load_cache():
    """Called from main(), after the CLI has set CACHE_PATH and USE_CACHE."""
    global _cache
    _cache = {}
    if USE_CACHE and os.path.exists(CACHE_PATH):
        try:
            with open(CACHE_PATH, encoding='utf-8') as fh:
                _cache = json.load(fh)
        except (OSError, ValueError):
            _cache = {}

# Each service gets its own minimum spacing, so parallel workers stay polite to
# strict hosts (DBLP) without throttling permissive ones (CrossRef).
HOST_MIN_INTERVAL = {
    'dblp.org': 1.2, 'export.arxiv.org': 1.2, 'api.crossref.org': 0.12,
    'api.openalex.org': 0.12, 'api.datacite.org': 0.3, 'doi.org': 0.3,
    'www.ebi.ac.uk': 0.2, 'openlibrary.org': 0.4, 'aclanthology.org': 0.5,
    'proceedings.mlr.press': 0.5,
}
DEFAULT_INTERVAL = 0.4
_host_locks, _host_last, _host_guard = {}, {}, threading.Lock()


def _throttle(url):
    host = urlparse(url).netloc.lower()
    with _host_guard:
        lock = _host_locks.setdefault(host, threading.Lock())
    with lock:
        gap = HOST_MIN_INTERVAL.get(host, DEFAULT_INTERVAL)
        wait = gap - (time.time() - _host_last.get(host, 0.0))
        if wait > 0:
            time.sleep(wait)
        _host_last[host] = time.time()


def _cache_get(key):
    if not USE_CACHE:
        return None
    with _cache_lock:
        hit = _cache.get(key)
    # [state, payload, saved_at]; entries without a timestamp predate the TTL
    if not hit or len(hit) < 3 or time.time() - hit[2] > CACHE_TTL_DAYS * 86400:
        return None
    return hit


def _cache_put(key, value):
    global _cache_dirty
    if not USE_CACHE:
        return
    with _cache_lock:
        _cache[key] = [*value, time.time()]
        _cache_dirty = True


def save_cache():
    global _cache_dirty
    if not (USE_CACHE and _cache_dirty):
        return
    with _cache_lock:
        tmp = CACHE_PATH + '.tmp'
        try:
            with open(tmp, 'w', encoding='utf-8') as fh:
                json.dump(_cache, fh)
            os.replace(tmp, CACHE_PATH)      # a crash mid-write cannot corrupt the cache
            _cache_dirty = False
        except OSError as e:
            print(f'Could not save cache {CACHE_PATH}: {e}', file=sys.stderr)


def http_get(url, params=None, accept='application/json', as_text=False):
    """-> (state, payload); state in {'ok','not_found','error'}.

    'error' means the service was unreachable and is never collapsed into
    'not_found' - an unreachable registry must not be read as "does not exist".
    """
    key = f'{accept}|{url}?' + urlencode(sorted((params or {}).items()))
    hit = _cache_get(key)
    if hit and hit[0] != 'error':
        return hit[0], hit[1]

    headers = {'User-Agent': user_agent(), 'Accept': accept}
    state, payload = 'error', None
    for attempt in range(MAX_RETRIES):
        _throttle(url)
        try:
            r = requests.get(url, params=params, headers=headers,
                             timeout=HTTP_TIMEOUT)
            if r.status_code == 200:
                try:
                    payload = r.text if as_text else r.json()
                    state = 'ok'
                except ValueError:
                    state, payload = 'error', None
                break
            if r.status_code in (404, 400, 410):
                state, payload = 'not_found', None
                break
            if r.status_code in (429, 500, 502, 503, 504):
                time.sleep(2.0 * (attempt + 1))
                continue
        except requests.RequestException:
            pass
        time.sleep(1.0 * (attempt + 1))
    # Only successes are cached: a 'not_found' DOI may be registered tomorrow.
    if state == 'ok':
        _cache_put(key, (state, payload))
    return state, payload


def blank_record(source):
    return {'source': source, 'doi': None, 'title': '', 'authors': [],
            'year': None, 'container': '', 'type': '', 'volume': '', 'issue': '',
            'pages': '', 'publisher': '', 'issn': '', 'isbn': '', 'edition': '',
            'url': '', 'links': [], 'retracted': ''}




# ---------- CrossRef ----------
def _cr_record(msg):
    r = blank_record('CrossRef')
    r['doi'] = clean_doi(msg.get('DOI'))
    r['title'] = (msg.get('title') or [''])[0] or ''
    for k in ('issued', 'published-print', 'published-online', 'created'):
        try:
            y = (msg.get(k, {}).get('date-parts') or [[None]])[0][0]
        except Exception:
            y = None
        if y:
            r['year'] = y
            break
    r['type'] = (msg.get('type') or '').lower()
    r['container'] = (msg.get('container-title') or [''])[0] or ''
    r['volume'] = str(msg.get('volume') or '')
    r['issue'] = str(msg.get('issue') or '')
    r['pages'] = str(msg.get('page') or '')
    r['publisher'] = msg.get('publisher') or ''
    r['edition'] = str(msg.get('edition-number') or '')
    issn = msg.get('ISSN') or []
    isbn = msg.get('ISBN') or []
    r['issn'] = issn[0] if issn else ''
    r['isbn'] = isbn[0] if isbn else ''
    r['url'] = msg.get('URL') or ''
    r['links'] = [x.get('URL') for x in (msg.get('link') or []) if x.get('URL')]
    # CrossRef (with Retraction Watch data) lists later notices on the original work
    r['retracted'] = ', '.join(sorted({(u.get('type') or '').lower() for u in (msg.get('updated-by') or [])
                                       if (u.get('type') or '').lower() in RETRACTION_TYPES}))
    r['authors'] = [(a.get('family') or a.get('name') or '', a.get('given') or '')
                    for a in (msg.get('author') or [])]
    return r


def crossref_by_doi(doi):
    st, pl = http_get(f'https://api.crossref.org/works/{quote(doi)}',
                      {'mailto': CONTACT_EMAIL})
    return (st, _cr_record(pl.get('message', {}))) if st == 'ok' else (st, None)


def crossref_search(title, author=None, rows=5):
    params = {'query.bibliographic': latex_to_text(title), 'rows': rows,
              'mailto': CONTACT_EMAIL}
    if author:
        params['query.author'] = author
    st, pl = http_get('https://api.crossref.org/works', params)
    if st != 'ok':
        return None if st == 'error' else []    # None = could not look
    return [_cr_record(it) for it in (pl.get('message', {}).get('items') or [])]


# ---------- DOI content negotiation (works for ANY DOI registrar) ----------
def doi_negotiate(doi):
    """Ask doi.org itself for CSL-JSON. Covers registrars with no adapter here
    (mEDRA, JaLC, KISTI, OP Portal), so DOI coverage is not limited to the
    APIs implemented above."""
    st, pl = http_get(f'https://doi.org/{quote(doi)}',
                      accept='application/vnd.citationstyles.csl+json')
    if st != 'ok' or not isinstance(pl, dict):
        return st, None
    r = blank_record('doi.org')
    r['doi'] = clean_doi(pl.get('DOI') or doi)
    t = pl.get('title')
    r['title'] = (t[0] if isinstance(t, list) and t else t) or ''
    for k in ('issued', 'published', 'published-print', 'published-online'):
        try:
            y = (pl.get(k, {}).get('date-parts') or [[None]])[0][0]
        except Exception:
            y = None
        if y:
            r['year'] = y
            break
    r['type'] = (pl.get('type') or '').lower()
    ct = pl.get('container-title')
    r['container'] = (ct[0] if isinstance(ct, list) and ct else ct) or ''
    r['volume'] = str(pl.get('volume') or '')
    r['issue'] = str(pl.get('issue') or '')
    r['pages'] = str(pl.get('page') or '')
    r['publisher'] = pl.get('publisher') or ''
    r['issn'] = (pl.get('ISSN') or [''])[0] if isinstance(pl.get('ISSN'), list) \
        else (pl.get('ISSN') or '')
    r['authors'] = [(a.get('family') or a.get('literal') or '', a.get('given') or '')
                    for a in (pl.get('author') or [])]
    return 'ok', r


# ---------- DataCite ----------
def datacite_by_doi(doi):
    st, pl = http_get(f'https://api.datacite.org/dois/{quote(doi)}')
    if st != 'ok':
        return st, None
    a = (pl.get('data') or {}).get('attributes') or {}
    r = blank_record('DataCite')
    r['doi'] = clean_doi(a.get('doi'))
    r['title'] = ((a.get('titles') or [{}])[0]).get('title', '') or ''
    r['year'] = a.get('publicationYear')
    r['type'] = ((a.get('types') or {}).get('resourceTypeGeneral') or '').lower()
    pub = a.get('publisher')
    r['publisher'] = pub if isinstance(pub, str) else ((pub or {}).get('name', '') if pub else '')
    r['url'] = a.get('url') or ''
    r['container'] = ((a.get('container') or {}).get('title') or '')
    auths = []
    for c in (a.get('creators') or []):
        fam, giv = c.get('familyName') or '', c.get('givenName') or ''
        if not fam:
            fam, giv = parse_name(c.get('name') or '')
        auths.append((fam, giv))
    r['authors'] = auths
    return 'ok', r


# ---------- OpenAlex ----------
def _oa_record(w):
    r = blank_record('OpenAlex')
    r['doi'] = clean_doi(w.get('doi'))
    r['title'] = w.get('display_name') or w.get('title') or ''
    r['year'] = w.get('publication_year')
    r['type'] = (w.get('type') or '').lower()
    loc = w.get('primary_location') or {}
    src = loc.get('source') or {}
    r['container'] = src.get('display_name') or ''
    r['publisher'] = src.get('host_organization_name') or ''
    issn = src.get('issn') or []
    r['issn'] = issn[0] if issn else ''
    r['url'] = loc.get('landing_page_url') or ''
    b = w.get('biblio') or {}
    r['volume'] = str(b.get('volume') or '')
    r['issue'] = str(b.get('issue') or '')
    fp, lp = b.get('first_page'), b.get('last_page')
    r['pages'] = f'{fp}-{lp}' if fp and lp else str(fp or '')
    r['authors'] = [parse_name((a.get('author') or {}).get('display_name')
                               or a.get('raw_author_name') or '')
                    for a in (w.get('authorships') or [])]
    r['retracted'] = 'retraction' if w.get('is_retracted') else ''
    r['links'] = [x.get('landing_page_url') for x in (w.get('locations') or [])
                  if x.get('landing_page_url')]
    return r


def openalex_by_doi(doi):
    st, pl = http_get(f'https://api.openalex.org/works/doi:{quote(doi)}',
                      {'mailto': CONTACT_EMAIL})
    return (st, _oa_record(pl)) if st == 'ok' else (st, None)


def openalex_search(title, rows=5):
    q = re.sub(r'[^A-Za-z0-9 ]', ' ', latex_to_text(title))
    st, pl = http_get('https://api.openalex.org/works',
                      {'filter': f'title.search:{q}', 'per-page': rows,
                       'mailto': CONTACT_EMAIL})
    if st != 'ok':
        return None if st == 'error' else []    # None = could not look
    return [_oa_record(w) for w in (pl.get('results') or [])]


# ---------- Europe PMC (biomedicine / life sciences) ----------
def _epmc_record(w):
    r = blank_record('EuropePMC')
    r['doi'] = clean_doi(w.get('doi'))
    r['title'] = (w.get('title') or '').rstrip('.')
    r['year'] = w.get('pubYear')
    r['type'] = 'journal-article'
    ji = w.get('journalInfo') or {}
    j = ji.get('journal') or {}
    r['container'] = j.get('title') or ''
    r['issn'] = j.get('issn') or j.get('essn') or ''
    r['volume'] = str(ji.get('volume') or '')
    r['issue'] = str(ji.get('issue') or '')
    r['pages'] = str(w.get('pageInfo') or '')
    al = (w.get('authorList') or {}).get('author') or []
    auths = []
    for a in al:
        fam, giv = a.get('lastName') or '', a.get('firstName') or ''
        if not fam:
            fam, giv = parse_name(a.get('fullName') or '')
        auths.append((fam, giv))
    r['authors'] = auths
    return r


def europepmc_search(title, rows=5):
    q = re.sub(r'[^A-Za-z0-9 ]', ' ', latex_to_text(title))
    st, pl = http_get('https://www.ebi.ac.uk/europepmc/webservices/rest/search',
                      {'query': f'TITLE:"{q}"', 'format': 'json',
                       'resultType': 'core', 'pageSize': rows})
    if st != 'ok':
        return None if st == 'error' else []    # None = could not look
    return [_epmc_record(w) for w in
            ((pl.get('resultList') or {}).get('result') or [])]


# ---------- DBLP (computer science proceedings) ----------
DBLP_TYPE_MAP = {
    'conference and workshop papers': 'proceedings-article',
    'journal articles': 'journal-article',
    'informal and other publications': 'posted-content',
    'informal publications': 'posted-content',
    'parts in books or collections': 'book-chapter',
    'books and theses': 'book',
    'editorship': 'edited-book',
}


def _dblp_record(info):
    r = blank_record('DBLP')
    r['doi'] = clean_doi(info.get('doi'))
    r['title'] = (info.get('title') or '').rstrip('.')
    r['year'] = info.get('year')
    t = (info.get('type') or '').lower()
    r['type'] = DBLP_TYPE_MAP.get(t, t)
    ven = info.get('venue')
    r['container'] = ven if isinstance(ven, str) else ' / '.join(ven or [])
    r['volume'] = str(info.get('volume') or '')
    r['issue'] = str(info.get('number') or '')
    r['pages'] = str(info.get('pages') or '')
    ee = info.get('ee')
    r['url'] = ee or info.get('url') or ''
    r['links'] = [x for x in ([ee] if isinstance(ee, str) else (ee or [])) if x]
    a = (info.get('authors') or {}).get('author') or []
    if isinstance(a, dict):
        a = [a]
    auths = []
    for x in a:
        nm = x.get('text') if isinstance(x, dict) else str(x)
        nm = re.sub(r'\s+\d{4}$', '', nm or '')       # strip DBLP disambiguators
        auths.append(parse_name(nm))
    r['authors'] = auths
    return r


def dblp_search(title, rows=8):
    q = re.sub(r'[^A-Za-z0-9 ]', ' ', latex_to_text(title))
    st, pl = http_get('https://dblp.org/search/publ/api',
                      {'q': q, 'format': 'json', 'h': rows})
    if st != 'ok':
        return None if st == 'error' else []    # None = could not look
    hits = ((pl.get('result') or {}).get('hits') or {}).get('hit') or []
    if isinstance(hits, dict):
        hits = [hits]
    return [_dblp_record(h.get('info') or {}) for h in hits]


# ---------- OpenLibrary (books) ----------
def openlibrary_by_isbn(isbn):
    isbn = re.sub(r'[^0-9Xx]', '', str(isbn or ''))
    if len(isbn) not in (10, 13):
        return None
    st, pl = http_get('https://openlibrary.org/api/books',
                      {'bibkeys': f'ISBN:{isbn}', 'format': 'json', 'jscmd': 'data'})
    if st != 'ok' or not pl:
        return None
    d = pl.get(f'ISBN:{isbn}')
    if not d:
        return None
    r = blank_record('OpenLibrary')
    r['title'] = d.get('title') or ''
    if d.get('subtitle'):
        r['title'] += ': ' + d['subtitle']
    r['year'] = parse_year(d.get('publish_date'))
    r['type'] = 'book'
    r['isbn'] = isbn
    r['publisher'] = ', '.join(p.get('name', '') for p in (d.get('publishers') or []))
    r['url'] = d.get('url') or ''
    r['authors'] = [parse_name(a.get('name', '')) for a in (d.get('authors') or [])]
    return r


# ---------- arXiv ----------
def arxiv_by_id(aid):
    st, xml = http_get('http://export.arxiv.org/api/query',
                       {'id_list': aid, 'max_results': 1},
                       accept='application/atom+xml', as_text=True)
    if st != 'ok' or not xml:
        return None
    def tag(name, blk):
        m = re.search(rf'<{name}>(.*?)</{name}>', blk, re.S)
        return re.sub(r'\s+', ' ', m.group(1)).strip() if m else ''
    m = re.search(r'<entry>(.*?)</entry>', xml, re.S)
    if not m:
        return None
    blk = m.group(1)
    r = blank_record('arXiv')
    r['title'] = tag('title', blk)
    if not r['title']:
        return None
    r['year'] = parse_year(tag('published', blk))
    r['type'] = 'posted-content'
    r['doi'] = clean_doi(tag('arxiv:doi', blk)) or f'10.48550/arXiv.{aid}'
    r['url'] = f'https://arxiv.org/abs/{aid}'
    r['container'] = 'arXiv'
    r['authors'] = [parse_name(n) for n in re.findall(r'<name>(.*?)</name>', blk, re.S)]
    return r


def extract_arxiv_id(entry):
    for key in ('eprint', 'arxiv', 'doi', 'howpublished', 'url', 'note', 'journal'):
        m = re.search(r'(\d{4}\.\d{4,5})(v\d+)?', str(entry.get(key, '')))
        if m:
            return m.group(1)
    return None




def _record_from_bibtex(text, source):
    """Parse a BibTeX string served by a publisher into our record shape."""
    if not text or '@' not in text:
        return None
    try:
        db = bibtexparser.loads(text, BibTexParser(common_strings=True))
    except Exception:
        return None
    if not db.entries:
        return None
    e = db.entries[0]
    r = blank_record(source)
    r['title'] = latex_to_text(e.get('title', ''))
    if not r['title']:
        return None
    r['year'] = parse_year(e.get('year'))
    r['doi'] = clean_doi(e.get('doi'))
    r['volume'] = e.get('volume', '')
    r['issue'] = e.get('number', '')
    r['pages'] = e.get('pages', '')
    r['publisher'] = latex_to_text(e.get('publisher', ''))
    r['container'] = latex_to_text(e.get('booktitle') or e.get('journal') or '')
    r['type'] = ('proceedings-article' if e.get('ENTRYTYPE') == 'inproceedings'
                 else 'journal-article' if e.get('ENTRYTYPE') == 'article'
                 else e.get('ENTRYTYPE', ''))
    r['authors'] = [parse_name(a) for a in split_bib_authors(e.get('author', ''))]
    return r


def resolve_pmlr(url):
    """PMLR embeds its BibTeX fields in the paper page."""
    st, html = http_get(url.replace('http://', 'https://'),
                        accept='text/html', as_text=True)
    if st != 'ok' or not html:
        return None

    def fld(name):
        m = re.search(name + r'\s*=\s*\{(.*?)\}[,\n]', html, re.S)
        return re.sub(r'\s+', ' ', m.group(1)).strip() if m else ''

    r = blank_record('PMLR')
    r['title'] = latex_to_text(fld('title'))
    if not r['title']:
        return None
    r['year'] = parse_year(fld('year'))
    r['pages'] = fld('pages')
    r['volume'] = fld('volume')
    r['container'] = latex_to_text(fld('booktitle'))
    r['publisher'] = 'PMLR'
    r['type'] = 'proceedings-article'
    r['url'] = url
    au = fld('author')
    if au:
        r['authors'] = [parse_name(a) for a in re.split(r'\s+and\s+', au)]
    return r


def resolve_bibtex_suffix(url, source):
    """Sites that serve '<landing page>.bib' (ACL Anthology and friends)."""
    st, text = http_get(url.rstrip('/') + '.bib', accept='text/plain', as_text=True)
    return _record_from_bibtex(text, source) if st == 'ok' else None


PUBLISHER_RESOLVERS = [
    (re.compile(r'proceedings\.mlr\.press', re.I), resolve_pmlr),
    (re.compile(r'aclanthology\.org', re.I),
     lambda u: resolve_bibtex_suffix(u, 'ACL Anthology')),
]


def publisher_record(links):
    """First publisher-of-record hit among a record's outbound links."""
    for url in links:
        if not url:
            continue
        for pattern, fn in PUBLISHER_RESOLVERS:
            if pattern.search(url):
                try:
                    rec = fn(url)
                except Exception:
                    rec = None
                if rec:
                    return rec
    return None


# ---------- URL liveness ----------
def check_url(u):
    """A single dropped connection is not evidence a link is dead, so retry
    before condemning it - otherwise a live URL is flagged on a network blip."""
    if not u:
        return ''
    last = ''
    headers = {'User-Agent': user_agent()}
    for attempt in range(3):
        try:
            _throttle(u)
            r = requests.get(u, headers=headers, timeout=HTTP_TIMEOUT + 15 * attempt,
                             allow_redirects=True, stream=True)
            code = r.status_code
            r.close()
            # 202 is what ScienceDirect/ACM serve to bots; it is not a dead link
            if 200 <= code < 300:
                return f'OK {code}'
            if code in (401, 403, 405, 418, 429):
                return f'BLOCKED {code} (paywall/bot-guard; probably fine)'
            last = f'DEAD {code}'
            if code < 500:
                return last
        except requests.RequestException as e:
            last = f'DEAD ({type(e).__name__} after {attempt + 1} attempts)'
        time.sleep(1.5 * (attempt + 1))
    return last




REGISTRY_TYPES = {
    'article':       {'journal-article', 'article', 'review', 'text',
                      'journal', 'article-journal'},
    'inproceedings': {'proceedings-article', 'conference-paper', 'article',
                      'posted-content', 'preprint', 'book-chapter',
                      'inproceedings', 'conference', 'text', 'paper-conference'},
    'conference':    {'proceedings-article', 'conference-paper', 'article',
                      'paper-conference'},
    'incollection':  {'book-chapter', 'book-part', 'reference-entry',
                      'incollection', 'chapter'},
    'inbook':        {'book-chapter', 'book-part', 'chapter'},
    'book':          {'book', 'monograph', 'reference-book', 'edited-book'},
    'proceedings':   {'proceedings', 'book', 'edited-book'},
    'phdthesis':     {'dissertation', 'thesis'},
    'mastersthesis': {'dissertation', 'thesis'},
    'techreport':    {'report', 'report-component', 'text'},
    'dataset':       {'dataset'},
    'software':      {'software', 'computational notebook'},
    'patent':        {'patent'},
    'standard':      {'standard'},
    'misc':          None,          # None = accept any registry type
    'online':        None,
    'unpublished':   None,
}

# container bib-field, plus soft fields worth reporting for this type
TYPE_PROFILES = {
    'article':       ('journal',   [('publisher', 'publisher'), ('issn', 'issn')]),
    'inproceedings': ('booktitle', [('publisher', 'publisher')]),
    'conference':    ('booktitle', [('publisher', 'publisher')]),
    'incollection':  ('booktitle', [('publisher', 'publisher'), ('isbn', 'isbn')]),
    'inbook':        ('booktitle', [('publisher', 'publisher'), ('isbn', 'isbn')]),
    'book':          (None,        [('publisher', 'publisher'), ('isbn', 'isbn'),
                                    ('edition', 'edition')]),
    'proceedings':   (None,        [('publisher', 'publisher'), ('isbn', 'isbn')]),
    # A registry's 'publisher' is NOT a thesis's school or a report's issuing
    # institution (CrossRef says "Wiley" for a thesis reprinted in a journal),
    # so those fields are left to the author.
    'phdthesis':     (None,        []),
    'mastersthesis': (None,        []),
    'techreport':    (None,        []),
    'misc':          (None,        [('publisher', 'publisher')]),
}
DEFAULT_PROFILE = (None, [('publisher', 'publisher')])


def profile_for(etype):
    return TYPE_PROFILES.get(etype, DEFAULT_PROFILE)


def type_compatible(bibtype, regtype):
    if bibtype not in REGISTRY_TYPES:
        return None                       # unknown bib type: do not judge
    allowed = REGISTRY_TYPES[bibtype]
    if allowed is None or not regtype:
        return None
    return regtype.lower() in allowed




def load_bib(path):
    with open(path, encoding='utf-8') as fh:
        content = fh.read()
    p = BibTexParser(common_strings=True)
    p.ignore_nonstandard_types = False
    p.homogenize_fields = False
    return bibtexparser.loads(content, p)


def resolve(entry):
    """Gather every registry record that plausibly describes this entry."""
    title = entry.get('title', '')
    doi = clean_doi(entry.get('doi'))
    recs, notes = [], []

    if doi:
        resolved = False
        for fn in (crossref_by_doi, datacite_by_doi, openalex_by_doi, doi_negotiate):
            st, r = fn(doi)
            if st == 'ok' and r:
                # Some deposits (ACL Anthology, several society publishers) carry
                # no title. The DOI still resolves, so keep the record as proof of
                # existence; the empty title scores 0 and bars it from donating.
                r['identity'] = 'doi'
                recs.append(r)
                resolved = True
            elif st == 'error':
                notes.append(f'{fn.__name__} unreachable')
        if not resolved and not notes:
            notes.append('DOI did not resolve on any registry')

    if not title:
        for r in recs:
            r['score'] = 0.0
        return recs, notes + ['entry has no title; only DOI lookup possible']

    first_author = None
    if entry.get('author'):
        names = split_bib_authors(entry['author'])
        if names:
            first_author = parse_name(names[0])[0]

    # Title-based lookups always run: they validate venue/pages/authors and find
    # a DOI when the entry has none.
    hits = []
    for fn, args in ((dblp_search, (title,)), (openalex_search, (title,)),
                     (crossref_search, (title, first_author)), (europepmc_search, (title,))):
        got = fn(*args)
        if got is None:     # a search that could not run is an outage, not "no match"
            notes.append(f'{fn.__name__} unreachable')
        else:
            hits += got
    for cand in hits:
        if title_match_score(title, cand['title']) >= REVIEW_THRESHOLD:
            cand['identity'] = 'title'
            recs.append(cand)

    # Follow outbound links to a publisher of record, if any source offers one.
    for r in sorted(recs, key=lambda x: -title_match_score(title, x['title'])):
        if title_match_score(title, r['title']) < ACCEPT_THRESHOLD:
            break
        pub = publisher_record((r.get('links') or []) + [r.get('url') or ''])
        if pub and title_match_score(title, pub['title']) >= ACCEPT_THRESHOLD:
            pub['identity'] = 'publisher'
            recs.append(pub)
            break

    aid = extract_arxiv_id(entry)
    if aid:
        ar = arxiv_by_id(aid)
        if ar and title_match_score(title, ar['title']) >= REVIEW_THRESHOLD:
            ar['identity'] = 'arxiv-id'
            recs.append(ar)

    if entry.get('isbn'):
        ol = openlibrary_by_isbn(entry['isbn'])
        if ol and title_match_score(title, ol['title']) >= REVIEW_THRESHOLD:
            ol['identity'] = 'isbn'
            recs.append(ol)

    for r in recs:
        r['score'] = title_match_score(title, r['title'])
    return recs, notes


def authors_agree(entry, r):
    """A record found by title alone must share at least one author surname with
    the entry. A same-titled work by other people (a 2025 book chapter called
    "Attention Is All You Need") is a different work, however exact the title."""
    if r.get('identity') != 'title' or not r.get('authors'):
        return True
    mine = {norm_family(parse_name(a)[0]) for a in split_bib_authors(entry.get('author', ''))}
    mine.discard('')
    return not mine or bool(mine & {norm_family(f) for f, _ in r['authors']})


def pick_authority(entry, recs):
    etype = entry.get('ENTRYTYPE', '')
    strong = [r for r in recs if r['score'] >= ACCEPT_THRESHOLD and authors_agree(entry, r)]
    pool = list(strong) or [r for r in recs if r['score'] >= REVIEW_THRESHOLD
                            and authors_agree(entry, r)]
    if not pool:
        return None, strong
    pref = (['PMLR', 'ACL Anthology', 'CrossRef', 'EuropePMC', 'OpenAlex', 'DBLP',
             'doi.org', 'DataCite', 'OpenLibrary', 'arXiv'] if etype == 'article'
            else ['PMLR', 'ACL Anthology', 'DBLP', 'CrossRef', 'EuropePMC',
                  'OpenAlex', 'doi.org', 'DataCite', 'OpenLibrary', 'arXiv'])

    def rank(r):
        base = pref.index(r['source']) if r['source'] in pref else 20
        if r.get('identity') == 'publisher':
            base -= 10
        if r['type'] in ('posted-content', 'preprint') or r['container'] == 'arXiv':
            base += 15          # a preprint never outranks a published record
        return (base, -r['score'])

    pool.sort(key=rank)
    return pool[0], strong


def field_of(entry, name):
    return (entry.get(name) or '').strip()


def compare(entry, recs, authority):
    """-> [{field, current, suggested, verdict, evidence}]"""
    etype = entry.get('ENTRYTYPE', '')
    container_field, soft_fields = profile_for(etype)
    out = []

    def add(field, cur, sug, verdict, ev):
        out.append({'field': field, 'current': cur, 'suggested': sug,
                    'verdict': verdict, 'evidence': ev})

    trusted = [r for r in recs
               if r.get('identity') in ('doi', 'publisher', 'isbn')
               or r['score'] >= DONOR_THRESHOLD]
    all_dois = [r['doi'] for r in recs if r['doi']]

    def is_preprint(r):
        return (r['type'] in ('posted-content', 'preprint')
                or r['container'] in ('arXiv', 'CoRR')
                or is_arxiv_doi(r['doi'])
                or str(r['volume']).startswith('abs/'))

    def donor_rank(r):
        ident = {'publisher': 0, 'doi': 1, 'isbn': 1}.get(r.get('identity'), 2)
        return (ident, -r['score'])

    # A donor must additionally (a) match this entry's title - a DOI that
    # resolves to a DIFFERENT work must never lend its authors or pages - and
    # (b) be type-compatible, so a journal *review of* a book cannot supply
    # metadata for the book itself.
    # A short title is not evidence of identity: "Biopython" matches a different
    # work titled "Biopython" at 1.000. When the title is not distinctive, only
    # a hard identifier (DOI, publisher page, ISBN) may donate a value.
    distinctive = len(normalize_title(field_of(entry, 'title')).split()) >= 4

    donors = sorted([r for r in trusted
                     if not is_preprint(r)
                     and r['score'] >= ACCEPT_THRESHOLD
                     and type_compatible(etype, r['type']) is not False
                     and (distinctive or r.get('identity') != 'title')
                     and authors_agree(entry, r)],
                    key=donor_rank)

    if not distinctive and field_of(entry, 'title'):
        cands = sorted([r for r in recs if r.get('identity') == 'title'
                        and r['score'] >= ACCEPT_THRESHOLD],
                       key=lambda r: -r['score'])[:2]
        add('_title', field_of(entry, 'title'), None, 'REVIEW',
            'title is too short to identify this work by title alone; verified by '
            'identifier only'
            + ('. Same-title candidates found: '
               + '; '.join(f"{c['source']}: {c.get('doi') or c['container'] or '?'} "
                           f"({c['year']})" for c in cands) if cands else ''))

    def donate(recf):
        """-> (value, source, conflicts). Never guesses between disagreeing
        registries: a conflict is reported, not silently resolved."""
        vals = [(str(r[recf]), r['source']) for r in donors if str(r.get(recf) or '')]
        if not vals:
            return '', '', []
        top_val, top_src = vals[0]

        def same(a, b):
            if recf == 'pages':
                return norm_pages(a) == norm_pages(b)
            if recf in ('container', 'publisher'):
                return container_equiv(a, b)
            return re.sub(r'\W', '', a).lower() == re.sub(r'\W', '', b).lower()

        conflicts = [f'{s}:{v}' for v, s in vals[1:] if not same(v, top_val)]
        return top_val, top_src, conflicts

    # ---- DOI ----
    cur_doi_raw = field_of(entry, 'doi')
    cur_doi = clean_doi(cur_doi_raw)
    doi_conf = [r for r in recs if r.get('identity') == 'doi']
    doi_titled = [r for r in doi_conf if r['title']]
    if cur_doi:
        if not doi_titled and doi_conf:
            add('doi', cur_doi, None, 'REVIEW',
                'DOI resolves on ' + '+'.join(sorted({r['source'] for r in doi_conf}))
                + ' but that record carries no title, so it could not be cross-checked')
        elif doi_titled:
            best = max(doi_titled, key=lambda r: r['score'])
            srcs = '+'.join(sorted({r['source'] for r in doi_titled}))
            if best['score'] >= ACCEPT_THRESHOLD:
                if cur_doi_raw != cur_doi:
                    add('doi', cur_doi_raw, cur_doi, 'FIX', f'normalize; resolves on {srcs}')
                else:
                    add('doi', cur_doi, None, 'OK', f'resolves on {srcs}')
            elif best['score'] >= REVIEW_THRESHOLD:
                add('doi', cur_doi, None, 'REVIEW',
                    f"resolves but registry title differs (sim={best['score']:.2f}): "
                    f"{best['title'][:80]}")
            else:
                repl = next((r['doi'] for r in donors if r['doi']), None)
                add('doi', cur_doi, prefer_doi_case(repl, all_dois), 'WRONG',
                    f"DOI resolves to a different work: {best['title'][:80]}")
        else:
            repl = next((r['doi'] for r in donors if r['doi']), None)
            add('doi', cur_doi, prefer_doi_case(repl, all_dois), 'WRONG',
                'DOI does not resolve on any registry')
        if is_arxiv_doi(cur_doi):
            pub = next((r['doi'] for r in donors
                        if r['doi'] and not is_arxiv_doi(r['doi'])), None)
            if pub:
                pub = prefer_doi_case(pub, all_dois)
                add('doi', cur_doi, pub, 'REVIEW',
                    f'entry cites the preprint DOI although a publisher DOI exists ({pub})')
    else:
        cand = next((r['doi'] for r in donors
                     if r['doi'] and not is_arxiv_doi(r['doi'])), None) \
            or next((r['doi'] for r in donors if r['doi']), None)
        if cand:
            src = next(r['source'] for r in donors if r['doi'] == cand)
            add('doi', '', prefer_doi_case(cand, all_dois), 'ADD', f'found via {src}')
        elif etype not in DOI_OPTIONAL_TYPES:
            add('doi', '', None, 'REVIEW',
                'no DOI in entry and none found (this venue may genuinely have none)')

    # ---- retraction: only records proven to be THIS work may raise it ----
    confirmed = donors + [r for r in recs if r.get('identity') == 'doi'
                          and r['score'] >= ACCEPT_THRESHOLD]
    flagged = sorted({f"{r['source']}: {r['retracted']}" for r in confirmed if r.get('retracted')})
    if flagged:
        add('_retraction', field_of(entry, 'doi'), None, 'RETRACTED',
            'registry marks this work as ' + '; '.join(flagged)
            + '. Check the notice and decide whether to cite it.')

    if not authority:
        add('_record', '', None, 'NOT_FOUND', 'no registry record matched this entry')
        return out

    A = authority

    # ---- title ----
    cur_t = field_of(entry, 'title')
    s = title_match_score(cur_t, A['title'])
    if s >= ACCEPT_THRESHOLD:
        add('title', latex_to_text(cur_t), None, 'OK', f"{A['source']} sim={s:.3f}")
    elif s >= REVIEW_THRESHOLD:
        add('title', latex_to_text(cur_t), protect_caps(text_to_latex(A['title'])),
            'REVIEW', f"{A['source']}: {A['title'][:90]} (sim={s:.2f})")
    else:
        add('title', latex_to_text(cur_t), protect_caps(text_to_latex(A['title'])),
            'WRONG', f"{A['source']}: {A['title'][:90]} (sim={s:.2f})")

    # ---- authors ----
    cur_authors = [parse_name(a) for a in split_bib_authors(field_of(entry, 'author'))]
    ref, ref_src = [], A['source']
    for r in donors:
        if r['authors']:
            ref, ref_src = r['authors'], r['source']
            break
    if not ref:
        add('author', f'{len(cur_authors)} authors', None, 'UNCHECKED',
            'no author list in any identity-confirmed record')
    elif not cur_authors:
        add('author', '', fmt_author_field(ref), 'ADD', ref_src)
    else:
        n = min(len(cur_authors), len(ref))
        aligned = all(same_person(cur_authors[i], ref[i]) for i in range(n))
        if aligned and len(cur_authors) == len(ref):
            # same_person already proved identity from substantive tokens, so only
            # flag initials sharing nothing ("J. Smith" vs "R. Smith"); "H. Brendan"
            # vs "Brendan" is a completeness difference, not an error.
            bad = [i for i, ((_, cg), (_, rg)) in enumerate(zip(cur_authors, ref))
                   if initials(cg) and initials(rg)
                   and set(initials(cg)).isdisjoint(set(initials(rg)))]
            if bad:
                add('author', field_of(entry, 'author'), fmt_author_field(ref), 'REVIEW',
                    f'{ref_src}: given-name mismatch at position(s) '
                    f'{[i + 1 for i in bad]} -> '
                    + '; '.join(f'{ref[i][1]} {ref[i][0]}' for i in bad))
            else:
                add('author', f'{len(cur_authors)} authors', None, 'OK',
                    f'{ref_src}: all {len(ref)} authors match in order')
        elif aligned and len(cur_authors) < len(ref):
            # keep the authors as the user wrote them; append only the missing ones
            add('author', field_of(entry, 'author'),
                field_of(entry, 'author') + ' and ' + fmt_author_field(ref[len(cur_authors):]), 'FIX',
                f'{ref_src}: entry is missing {len(ref) - len(cur_authors)} author(s): '
                + ', '.join(f'{g} {f}'.strip() for f, g in ref[len(cur_authors):]))
        elif aligned and len(cur_authors) > len(ref):
            add('author', field_of(entry, 'author'), None, 'REVIEW',
                f'{ref_src} lists only {len(ref)} of your {len(cur_authors)} authors '
                '(registry record may be truncated - do not delete authors blindly)')
        else:
            cfam = [norm_family(f) for f, _ in cur_authors]
            rfam = [norm_family(f) for f, _ in ref]
            ck = [name_key(*a) for a in cur_authors]
            rk = [name_key(*a) for a in ref]
            if cfam == rfam:
                # Same surnames, same order: a given-name variant ("Sanmi" vs
                # "Oluwasanmi"), not a different author list. Never auto-applied.
                diff = [f'{cg or "-"} -> {rg or "-"} ({rf})'
                        for (_, cg), (rf, rg) in zip(cur_authors, ref)
                        if name_key('', cg) != name_key('', rg)]
                add('author', field_of(entry, 'author'), fmt_author_field(ref), 'REVIEW',
                    f'{ref_src}: surnames all match; given-name variant(s): '
                    + '; '.join(diff[:4]))
            elif sorted(map(sorted, ck)) == sorted(map(sorted, rk)):
                add('author', field_of(entry, 'author'), fmt_author_field(ref), 'REVIEW',
                    f'{ref_src}: same people, different order')
            else:
                missing = [f'{g} {f}'.strip() for f, g in ref if name_key(f, g) not in ck]
                extra = [f'{g} {f}'.strip() for f, g in cur_authors
                         if name_key(f, g) not in rk]
                # REVIEW, not WRONG: one record never replaces a whole author list
                # (collaboration names and truncated deposits look exactly like this).
                add('author', field_of(entry, 'author'), fmt_author_field(ref), 'REVIEW',
                    f'{ref_src}: author lists differ; missing={missing or "-"} '
                    f'not-in-registry={extra or "-"}')

    # ---- author surname split: cross-check across donors ----------------
    # Publisher BibTeX is often auto-generated and reverses names: PMLR writes
    # "Kannan, Ramchandran" for Kannan Ramchandran, which renders as "Kannan, R."
    # Because the publisher of record outranks everything, a reversed name there
    # would silently confirm the same mistake in the entry. Registries that
    # disagree about which token is the surname must therefore be surfaced.
    if cur_authors and ref:
        base = [norm_family(f) for f, _ in ref]
        conflicts = {}
        for r in donors:
            if r['source'] == ref_src or not r['authors']:
                continue
            if len(r['authors']) != len(ref):
                continue
            other = [norm_family(f) for f, _ in r['authors']]
            if other != base and sorted(map(sorted, [name_key(*a) for a in r['authors']])) \
                    == sorted(map(sorted, [name_key(*a) for a in ref])):
                conflicts[r['source']] = r['authors']
        if conflicts:
            spots = []
            for i, (fam, giv) in enumerate(ref):
                alts = {src: a[i]
                        for src, a in conflicts.items()
                        if norm_family(a[i][0]) != norm_family(fam)}
                if alts:
                    others = '; '.join(f'{src} says surname "{a[0]}"'
                                       for src, a in alts.items())
                    spots.append(f'position {i + 1}: {ref_src} says surname '
                                 f'"{fam}" but {others}')
            if spots:
                add('author', field_of(entry, 'author'), None, 'REVIEW',
                    'registries disagree on which name is the surname - check how '
                    'this renders in your bibliography. ' + ' | '.join(spots[:3]))

    # ---- year ----
    yv, ysrc, yconf = donate('year')
    ry, ey = parse_year(yv), parse_year(field_of(entry, 'year'))
    if ry is None:
        add('year', str(ey or ''), None, 'UNCHECKED', 'no year in any trusted record')
    elif ey is None:
        add('year', '', str(ry), 'ADD', ysrc)
    elif ey == ry:
        add('year', str(ey), None, 'OK', ysrc)
    elif abs(ey - ry) <= YEAR_TOLERANCE or yconf:
        add('year', str(ey), str(ry), 'REVIEW',
            f'{ysrc} says {ry}'
            + (f'; other sources: {", ".join(yconf)}' if yconf
               else ' (online-first vs issue year, or preprint vs published)'))
    else:
        add('year', str(ey), str(ry), 'WRONG', f'{ysrc} says {ry}')

    # ---- container: journal / booktitle ----
    if container_field:
        cur_c = field_of(entry, container_field)
        ref_c, csrc, cconf = donate('container')
        if not ref_c:
            add(container_field, latex_to_text(cur_c), None, 'UNCHECKED',
                'no container title in any trusted record')
        elif not cur_c:
            add(container_field, '', text_to_latex(ref_c),
                'ADD' if not cconf else 'REVIEW', csrc)
        elif container_equiv(cur_c, ref_c):
            add(container_field, latex_to_text(cur_c), None, 'OK',
                f'{csrc}: "{ref_c}"')
        elif container_field == 'journal' and not cconf:
            add('journal', latex_to_text(cur_c), text_to_latex(ref_c), 'WRONG',
                f'{csrc}: "{ref_c}"')
        else:
            add(container_field, latex_to_text(cur_c), text_to_latex(ref_c), 'REVIEW',
                f'registry venue differs: "{ref_c}" per {csrc}'
                + (f'; other sources: {", ".join(cconf)}' if cconf else ''))

    # ---- volume / number / pages ----
    for bibf, recf in (('volume', 'volume'), ('number', 'issue'), ('pages', 'pages')):
        cur = field_of(entry, bibf)
        ref, rsrc, conflicts = donate(recf)
        if bibf == 'pages':
            cur_n, ref_n = norm_pages(cur), norm_pages(ref)
        else:
            cur_n, ref_n = re.sub(r'\D', '', cur), re.sub(r'\D', '', ref)
        if not ref:
            if cur:
                add(bibf, cur, None, 'UNCHECKED',
                    'no trusted record carries this field')
            continue
        sug = norm_pages(ref) if bibf == 'pages' else ref
        if not cur:
            add(bibf, '', sug, 'ADD' if not conflicts else 'REVIEW',
                rsrc if not conflicts else
                f'{rsrc}:{ref} but sources disagree: ' + ', '.join(conflicts))
        elif cur_n == ref_n:
            add(bibf, cur, None, 'OK', rsrc
                + (f' (others differ: {", ".join(conflicts)})' if conflicts else ''))
        elif conflicts:
            add(bibf, cur, sug, 'REVIEW',
                f'sources disagree - {rsrc}:{ref}, ' + ', '.join(conflicts))
        else:
            add(bibf, cur, sug, 'WRONG', f'{rsrc} says {ref}')

    # ---- soft fields (publisher, issn, isbn, school, ...) ----
    for bibf, recf in soft_fields:
        cur = field_of(entry, bibf)
        ref, rsrc, conflicts = donate(recf)
        if not ref:
            continue
        if not cur:
            add(bibf, '', text_to_latex(ref), 'OPTIONAL',
                f'{rsrc} has this; most styles do not require it')
        elif container_equiv(cur, ref) or \
                re.sub(r'\W', '', cur).lower() == re.sub(r'\W', '', ref).lower():
            add(bibf, latex_to_text(cur), None, 'OK', rsrc)
        else:
            add(bibf, latex_to_text(cur), text_to_latex(ref), 'REVIEW',
                f'{rsrc}: "{ref}"')

    # ---- entry type ----
    if type_compatible(etype, A['type']) is False:
        add('ENTRYTYPE', etype, None, 'REVIEW',
            f'{A["source"]} classifies this as "{A["type"]}"')

    # ---- structural check: BibTeX requires a container for these types ----
    if container_field and not field_of(entry, container_field):
        add(container_field, '', None, 'WRONG',
            f'BibTeX requires {container_field} for an {etype} entry; '
            f'it has none (bibtex will warn "empty {container_field}")')

    # ---- url ----
    cur_u = field_of(entry, 'url')
    if cur_u and CHECK_URLS:
        st = check_url(cur_u)
        add('url', cur_u, None, 'OK' if st.startswith(('OK', 'BLOCKED')) else 'WRONG', st)
    elif cur_u:
        add('url', cur_u, None, 'UNCHECKED', 'CHECK_URLS is off')
    return out




VERDICT_RANK = {'RETRACTED': 3, 'WRONG': 3, 'NOT_FOUND': 3, 'ADD': 2, 'REVIEW': 2, 'FIX': 1,
                'OK': 0, 'UNCHECKED': 0, 'OPTIONAL': 0}
# Verdicts that do not demand human attention: the value is right, absent from
# every registry, or merely an optional style field the entry could carry.
QUIET = ('OK', 'UNCHECKED', 'OPTIONAL')


def verify_entry(entry):
    key = entry.get('ID', '?')
    try:
        recs, notes = resolve(entry)
        authority, strong = pick_authority(entry, recs)
        fields = compare(entry, recs, authority)
    except Exception as e:                       # one bad entry must not kill the run
        return {'key': key, 'entry': entry, 'status': 'ERROR', 'fields': [],
                'sources': [], 'notes': [f'{type(e).__name__}: {e}'],
                'degraded': True, 'doi_confirmed': False}

    # If any registry was unreachable we did not hear from every source, so the
    # "sources disagree" safeguard could not run. Downgrade every WRONG to
    # REVIEW: nothing is auto-corrected on incomplete evidence.
    outages = [x for x in notes if 'unreachable' in x]
    if outages:
        # "Not found" and "could not look" are different claims. When a registry
        # was down, absence of evidence must never be reported as evidence of
        # absence, and nothing may be auto-corrected on partial evidence.
        honest = [
            ('DOI does not resolve on any registry',
             'DOI could NOT be checked - registry unreachable'),
            ('no registry record matched this entry',
             'entry could NOT be checked - registries unreachable'),
            ('no DOI in entry and none found',
             'no DOI in entry, and the search could NOT run'),
            ('no registry has this record',
             'the registries could not be reached'),
        ]
        for f in fields:
            for a, b in honest:
                f['evidence'] = f['evidence'].replace(a, b)
            if f['verdict'] == 'WRONG':
                f['verdict'] = 'REVIEW'
                f['evidence'] += (' | NOT auto-applied: a registry was unreachable '
                                  'during this run, so sources could not be '
                                  'cross-checked. Re-run when online.')

    worst = max((VERDICT_RANK.get(f['verdict'], 0) for f in fields), default=0)
    status = {0: 'CLEAN', 1: 'NORMALIZED', 2: 'REVIEW', 3: 'PROBLEM'}[worst]
    if not recs:
        status = 'UNVERIFIED'
    elif outages and status in ('CLEAN', 'NORMALIZED'):
        status = 'REVIEW'          # never report a clean bill on partial evidence
    return {'key': key, 'entry': entry, 'status': status, 'fields': fields,
            'sources': sorted({r['source'] for r in strong}), 'notes': notes,
            'degraded': bool(outages),
            'doi_confirmed': any(r.get('identity') == 'doi'
                                 and r['score'] >= ACCEPT_THRESHOLD for r in recs)}


def _progress(done, total, res):
    nbad = len([f for f in res['fields'] if f['verdict'] not in QUIET])
    print(f'[{done:>3}/{total}] {res["key"][:30]:<30} {res["status"]:<11} '
          f'sources={",".join(res["sources"]) or "-":<34} issues={nbad}', flush=True)


def run_verification(entries, workers=None):
    workers = workers or WORKERS
    total = len(entries)
    results = [None] * total
    if workers > 1:
        from concurrent.futures import ThreadPoolExecutor, as_completed
        with ThreadPoolExecutor(max_workers=workers) as pool:
            futures = {pool.submit(verify_entry, e): i for i, e in enumerate(entries)}
            # Report as each entry lands rather than after the whole batch, so a
            # large bibliography shows progress instead of sitting silent.
            for done, fut in enumerate(as_completed(futures), 1):
                results[futures[fut]] = fut.result()
                _progress(done, total, results[futures[fut]])
    else:
        for i, e in enumerate(entries):
            results[i] = verify_entry(e)
            _progress(i + 1, total, results[i])
    save_cache()
    return results


def build_reports(results, bib_filename, prefix=None):
    prefix = prefix or REPORT_PREFIX
    rows = []
    for res in results:
        for f in res['fields']:
            rows.append({'key': res['key'], 'entry_status': res['status'],
                         'field': f['field'], 'verdict': f['verdict'],
                         'current': f['current'], 'suggested': f['suggested'] or '',
                         'evidence': f['evidence'], 'sources': ','.join(res['sources'])})
    write_csv(f'{prefix}.csv', rows, ['key', 'entry_status', 'field', 'verdict', 'current',
                                      'suggested', 'evidence', 'sources'])

    summary = Counter(r['status'] for r in results)
    print('\nEntry status:')
    for k, v in summary.most_common():
        print(f'  {k:<11} {v}')
    if rows:
        print('\nField verdicts:')
        for k, v in Counter(r['verdict'] for r in rows).most_common():
            print(f'  {k:<11} {v}')

    md = ['# BibTeX verification report', '',
          f'File: `{bib_filename}` - {len(results)} entries', '',
          '## Summary', '', '| Status | Entries |', '|---|---|']
    md += [f'| {k} | {v} |' for k, v in summary.most_common()]
    md += ['', '## Entries needing attention', '']
    for res in results:
        bad = [f for f in res['fields'] if f['verdict'] not in QUIET]
        if not bad and not res['notes']:
            continue
        md += [f"### `{res['key']}` - {res['status']}", '',
               f"Sources: {', '.join(res['sources']) or 'none'}", '']
        if res['notes']:
            md += [f"Notes: {'; '.join(res['notes'])}", '']
        if bad:
            md += ['| Field | Verdict | Current | Suggested | Evidence |',
                   '|---|---|---|---|---|']
            for f in bad:
                cur = str(f['current']).replace('|', r'\|')[:110]
                sug = str(f['suggested'] or '').replace('|', r'\|')[:110]
                ev = str(f['evidence']).replace('|', r'\|')[:170]
                md.append(f"| {f['field']} | {f['verdict']} | {cur} | {sug} | {ev} |")
        md.append('')
    with open(f'{prefix}.md', 'w', encoding='utf-8') as fh:
        fh.write('\n'.join(md))
    print(f'\nWrote {prefix}.csv and {prefix}.md')
    return rows


def write_csv(path, rows, columns):
    with open(path, 'w', newline='', encoding='utf-8') as fh:
        w = csv.DictWriter(fh, fieldnames=columns)
        w.writeheader()
        w.writerows(rows)


def mark_duplicates(results):
    """Flag entries that share a DOI or a distinctive title under different keys:
    BibTeX prints both, and reviewers notice."""
    groups = {}
    for res in results:
        e = res['entry']
        doi = (clean_doi(e.get('doi')) or '').lower()
        title = normalize_title(e.get('title', ''))
        if doi:
            groups.setdefault(('DOI', doi), []).append(res)
        if len(title.split()) >= 4:          # short titles collide legitimately
            groups.setdefault(('title', title), []).append(res)
    dupes = {}
    for (kind, _), group in groups.items():
        if len(group) < 2:
            continue
        for res in group:
            others = dupes.setdefault(id(res), (res, {}))[1]
            others.update({r['key']: kind for r in group if r is not res})
    for res, others in dupes.values():
        res['fields'].append({'field': '_duplicate', 'current': res['key'], 'suggested': None,
                              'verdict': 'REVIEW',
                              'evidence': 'possible duplicate of ' + ', '.join(
                                  f'{k} (same {kind})' for k, kind in sorted(others.items()))})
        if res['status'] in ('CLEAN', 'NORMALIZED'):
            res['status'] = 'REVIEW'


ANNOT = '% bibverify:'      # every generated line starts with this


def _safe(line):
    """BibTeX does NOT treat '%' as a comment: it scans for '@' anywhere in the
    file and starts reading an entry there. A generated comment mentioning
    '@inproceedings' therefore silently destroys the bibliography. Neutralise
    every '@' before it reaches the file."""
    return str(line).replace('@', '(at)')


def _wrap(prefix, text, width=96):
    """Emit possibly-long evidence across continuation lines: a truncated
    explanation is not actionable for the person who has to fix it."""
    import textwrap
    text = re.sub(r'\s+', ' ', str(text or '')).strip().replace('@', '(at)')
    if not text:
        return []
    body = textwrap.wrap(text, width=width) or ['']
    pad = ' ' * (len(prefix) - len(prefix.lstrip()))
    out = [f'{ANNOT} {prefix}{body[0]}']
    out += [f'{ANNOT} {pad}{" " * 4}{ln}' for ln in body[1:]]
    return out


def _clip(v, n=64):
    v = re.sub(r'\s+', ' ', str(v or '')).strip()
    v = v.replace('@', '(at)')
    return v if len(v) <= n else v[:n - 3] + '...'


def entry_annotation(res, changes):
    """Comment block placed above one entry.

    Only entries that still need a human get a comment: CLEAN and NORMALIZED
    entries - status values that mean every field checked out, or was fixed by
    a plain formatting normalization with nothing left to review - carry NO
    comment at all, so the file stays readable and the flags that remain are
    the ones that matter. REVIEW, PROBLEM, UNVERIFIED and ERROR always get one:
    those are exactly the entries where something could not be confirmed, so
    nothing unverified is ever allowed to leave without a visible flag.
    """
    if res['status'] in ('CLEAN', 'NORMALIZED'):
        return []

    key, srcs = res['key'], ', '.join(res['sources'])
    fields = res.get('fields') or []
    unchecked = [f['field'] for f in fields if f['verdict'] == 'UNCHECKED']
    optional = [f['field'] for f in fields if f['verdict'] == 'OPTIONAL']
    # A field that was corrected is reported under CHANGED; listing it again as
    # "not auto-applied" would contradict that.
    written = {c['field'] for c in changes}
    todo = [f for f in fields
            if f['verdict'] in ('REVIEW', 'ADD', 'FIX', 'WRONG', 'NOT_FOUND', 'RETRACTED')
            and f['field'] not in written]

    L = [f'{ANNOT} {"=" * 68}',
         f'{ANNOT} [CHECK] {key}  -  status: {res["status"]}',
         f'{ANNOT}   confirmed against: {srcs or "NOTHING - no registry matched"}']

    if res.get('degraded'):
        L.append(f'{ANNOT}   !! A REGISTRY WAS UNREACHABLE DURING THIS RUN:')
        for x in res.get('notes', []):
            L.append(f'{ANNOT}        {x}')
        L.append(f'{ANNOT}      No registry value was written here. This result is '
                 f'INCOMPLETE, not clean.')
        L.append(f'{ANNOT}      Re-run the verifier when the services are back.')

    if not res['sources'] and res['status'] != 'ERROR':
        why = ('the registries could not be reached' if res.get('degraded')
               else 'no registry has this record')
        L.append(f'{ANNOT}   !! NOT VERIFIED AT ALL - {why}.')
        L.append(f'{ANNOT}      The entry below is exactly as you wrote it and was '
                 f'NOT confirmed.')
        L.append(f'{ANNOT}      Check every field by hand before submitting.')

    if res['status'] == 'ERROR':
        L.append(f'{ANNOT}   !! The verifier errored on this entry: '
                 f'{"; ".join(res.get("notes", []))}')
        L.append(f'{ANNOT}      Entry left untouched. Verify by hand.')

    if changes:
        L.append(f'{ANNOT}   CHANGED by the verifier (old value shown):')
        for c in changes:
            L.append(f'{ANNOT}     - {c["field"]}: {_clip(c["before"])!r} -> '
                     f'{_clip(c["after"])!r}')
            L += _wrap('      reason: ', c['why'])

    if todo:
        L.append(f'{ANNOT}   VERIFY BY HAND (not auto-applied):')
        for f in todo:
            L += _wrap(f'    - [{f["verdict"]}] {f["field"]}: ', f['evidence'])
            if f['suggested']:
                L += _wrap('        registry value (NOT written): ',
                           repr(_clip(f['suggested'], 200)))

    if unchecked:
        L.append(f'{ANNOT}   KEPT AS YOU WROTE IT, no registry carries these '
                 f'fields: ' + ', '.join(unchecked))
    if optional:
        L.append(f'{ANNOT}   optional fields available if your style wants them: '
                 + ', '.join(optional))

    L.append(f'{ANNOT} {"=" * 68}')
    return L


def strip_annotations(text):
    """Drop our own generated lines so re-runs do not accumulate them, while
    preserving every comment the author wrote."""
    return ''.join(ln for ln in text.splitlines(keepends=True)
                   if not ln.lstrip().startswith(ANNOT))


# ---------- in-place editing of the original .bib text ----------
# Re-serializing through bibtexparser would reorder fields, expand @string macros
# and reformat every entry. Instead only the values that change are rewritten.
_ENTRY_HEAD = re.compile(r'@\s*(\w+)\s*([{(])\s*([^,\s]+)\s*,')
_FIELD_HEAD = re.compile(r'\s*,?\s*([A-Za-z][\w\-:.+]*)\s*=\s*')


def _scan_to(text, i, stop):
    """Index of the ',' that ends a field value starting at i, or of the entry's
    closing delimiter. Tracks braces and double quotes, so '#' concatenation,
    macros and nested braces all stay inside one value."""
    depth, quoted = 0, False
    while i < stop:
        ch = text[i]
        if ch == '\\':
            i += 2
            continue
        if ch == '{':
            depth += 1
        elif ch == '}':
            if depth == 0:
                return i
            depth -= 1
        elif ch == '"' and depth == 0:
            quoted = not quoted
        elif ch in ',)' and depth == 0 and not quoted:
            return i
        i += 1
    return stop


def entry_spans(text):
    """key -> (at, body_start, close): '@' position, first char after 'key,', and
    the closing delimiter. @string/@preamble/@comment blocks are skipped."""
    spans, pos = {}, 0
    while True:
        m = _ENTRY_HEAD.search(text, pos)
        if not m:
            return spans
        opener = m.group(2)
        closer = '}' if opener == '{' else ')'
        i, depth = m.end(), 0
        while i < len(text):
            ch = text[i]
            if ch == '{':
                depth += 1
            elif ch == '}' and depth > 0:
                depth -= 1
            elif ch == closer and depth == 0:
                break
            i += 1
        if m.group(1).lower() not in ('comment', 'string', 'preamble'):
            spans.setdefault(m.group(3), (m.start(), m.end(), i))
        pos = i + 1


def _set_field(body, field, value):
    """Replace one field's value inside an entry body, or append the field."""
    pos = 0
    while True:
        m = _FIELD_HEAD.match(body, pos)
        if not m or m.end() >= len(body):
            break
        end = _scan_to(body, m.end(), len(body))
        if m.group(1).lower() == field:
            vend = len(body[:end].rstrip())
            return body[:m.end()] + '{' + value + '}' + body[vend:]
        pos = end
    core = body.rstrip()
    tail = body[len(core):] or '\n'
    ind = re.search(r'\n([ \t]+)\S', body)
    sep = '' if not core.strip() or core.endswith(',') else ','
    return f'{core}{sep}\n{ind.group(1) if ind else "  "}{field} = {{{value}}}{tail}'


def patch_bib_text(text, changes):
    """changes: [{'key', 'field', 'after'}] -> text with only those values touched."""
    by_key = {}
    for c in changes:
        by_key.setdefault(c['key'], {})[c['field']] = c['after']
    spans = entry_spans(text)
    # right to left, so earlier offsets stay valid
    for key in sorted((k for k in by_key if k in spans), key=lambda k: -spans[k][1]):
        _, start, close = spans[key]
        body = text[start:close]
        for field, value in by_key[key].items():
            body = _set_field(body, field, value)
        text = text[:start] + body + text[close:]
    return text


def annotate_bib(text, results, applied, outages):
    by_key = {}
    for a in applied:
        by_key.setdefault(a['key'], []).append(a)

    verified = sum(1 for r in results
                   if r['status'] in ('CLEAN', 'NORMALIZED') and r['sources']
                   and not r.get('degraded'))
    header = [f'{ANNOT} {"=" * 68}',
              f'{ANNOT} Verified with the BibTeX Reference Verifier on '
              f'{time.strftime("%Y-%m-%d %H:%M:%S")}.',
              f'{ANNOT} {len(results)} entries: {verified} fully confirmed, '
              f'{len(results) - verified} need a human look.',
              f'{ANNOT} Lines starting "{ANNOT}" are generated and rewritten on '
              f'every run; BibTeX ignores them.']
    if outages:
        header += [f'{ANNOT}',
                   f'{ANNOT} !! REGISTRY OUTAGES DURING THIS RUN - results are '
                   f'INCOMPLETE:',
                   *[f'{ANNOT}      {o}' for o in sorted(outages)],
                   f'{ANNOT}    Entries touched by an outage got formatting fixes only, no registry values.',
                   f'{ANNOT}    Re-run when those services are reachable.']
    header.append(f'{ANNOT} {"=" * 68}')

    ann = {r['key']: [_safe(x) for x in entry_annotation(r, by_key.get(r['key'], []))]
           for r in results}
    out, pos = [], 0
    for key, (at, _, _) in sorted(entry_spans(text).items(), key=lambda kv: kv[1][0]):
        out.append(text[pos:at])
        if ann.get(key):
            out.append('\n'.join(ann[key]) + '\n')
        pos = at
    out.append(text[pos:])
    header = [_safe(h) for h in header]
    return '\n'.join(header) + '\n\n' + ''.join(out).lstrip('\n')


def apply_corrections(results, bib_db, bib_filename):
    applied = []
    for res in results:
        if res.get('degraded'):
            continue        # a registry was down: no value is written on partial evidence
        entry = res['entry']
        for f in res['fields']:
            fld, verdict, sug = f['field'], f['verdict'], f['suggested']
            if fld.startswith('_') or fld == 'ENTRYTYPE':
                continue
            if verdict not in ('FIX', 'ADD', 'WRONG') or not sug:
                continue
            if fld in PROPOSE_ONLY_FIELDS or fld not in AUTO_APPLY_FIELDS:
                continue
            if str(entry.get(fld, '')).strip() == str(sug).strip():
                continue                        # already correct; not a change
            applied.append({'key': res['key'], 'field': fld,
                            'before': entry.get(fld, ''), 'after': sug,
                            'why': f['evidence']})
    touched = {(a['key'], a['field']) for a in applied}
    for entry in bib_db.entries:                         # dash normalization
        if entry.get('pages') and (entry.get('ID'), 'pages') not in touched:
            np_ = norm_pages(entry['pages'])
            if np_ != entry['pages']:
                applied.append({'key': entry.get('ID'), 'field': 'pages',
                                'before': entry['pages'], 'after': np_,
                                'why': 'page-range dash normalization'})

    with open(bib_filename, encoding='utf-8') as fh:
        original = fh.read()
    new_text = patch_bib_text(strip_annotations(original), applied)
    if ANNOTATE_BIB:
        outages = sorted({x for r in results for x in r.get('notes', [])
                          if 'unreachable' in x})
        new_text = annotate_bib(new_text, results, applied, outages)
    else:
        new_text = new_text.lstrip('\n')

    # Never trust our own output. BibTeX ignores '%' but NOT '@': a stray '@' in
    # a generated comment starts a phantom entry and silently destroys the
    # bibliography. Re-read what we are about to write and refuse it unless every
    # entry survived and every correction landed exactly as intended.
    check = BibTexParser(common_strings=True)
    check.ignore_nonstandard_types = False
    try:
        reparsed = {e.get('ID'): e for e in bibtexparser.loads(new_text, check).entries}
    except Exception as e:
        raise RuntimeError(f'refusing to write {bib_filename}: generated file does '
                           f'not parse ({type(e).__name__}: {e}); '
                           f'your original is untouched')
    lost = {e.get('ID') for e in bib_db.entries} - set(reparsed)
    stray = [ln for ln in new_text.split('\n')
             if ln.lstrip().startswith(ANNOT) and '@' in ln]
    squash = lambda v: re.sub(r'\s+', ' ', str(v)).strip()  # noqa: E731
    missed = [f"{a['key']}.{a['field']}" for a in applied
              if squash(reparsed.get(a['key'], {}).get(a['field'], '')) != squash(a['after'])]
    if lost or stray or missed:
        raise RuntimeError(
            f'refusing to write {bib_filename}: '
            + (f'{len(lost)} entries would be lost ({sorted(lost)[:5]}); ' if lost else '')
            + (f'{len(stray)} comment line(s) contain "@", which BibTeX reads as an '
               f'entry start; ' if stray else '')
            + (f'corrections did not land: {missed[:5]}; ' if missed else '')
            + 'your original is untouched')

    backup = bib_filename + BACKUP_SUFFIX
    if not os.path.exists(backup):          # the first run's input is the true original
        shutil.copyfile(bib_filename, backup)
    with open(bib_filename, 'w', encoding='utf-8', newline='') as fh:
        fh.write(new_text)
    print(f'\nApplied {len(applied)} field corrections; wrote {bib_filename} '
          f'(original kept at {backup})')
    if applied:
        write_csv(os.path.splitext(bib_filename)[0] + '_applied_corrections.csv', applied,
                  ['key', 'field', 'before', 'after', 'why'])
        for a in applied:
            print(f"  {a['key'][:26]:<26} {a['field']:<9} "
                  f"{str(a['before'])[:42]!r} -> {str(a['after'])[:42]!r}")
    return applied


def _parse_cli(argv=None):
    global CONTACT_EMAIL, APPLY_CORRECTIONS, CHECK_URLS, USE_CACHE
    global CACHE_PATH, REPORT_PREFIX, WORKERS, ANNOTATE_BIB
    import argparse
    p = argparse.ArgumentParser(
        description='Verify every field of every entry in a .bib against public '
                    'bibliographic registries. Report-only unless --apply is given.')
    p.add_argument('bib', nargs='+', help='one or more .bib files')
    p.add_argument('--email', default=CONTACT_EMAIL,
                   help='contact address for API polite pools')
    g = p.add_mutually_exclusive_group()
    g.add_argument('--apply', dest='apply', action='store_true', default=None,
                   help='write corrections back to the .bib')
    g.add_argument('--dry-run', dest='apply', action='store_false',
                   help='report only; never modify the .bib')
    p.add_argument('--no-urls', action='store_true', help='skip live URL checks')
    p.add_argument('--no-cache', action='store_true', help='ignore the response cache')
    p.add_argument('--cache', default=CACHE_PATH, help='cache file path')
    p.add_argument('--report', default=REPORT_PREFIX, help='report filename prefix')
    p.add_argument('--workers', type=int, default=WORKERS,
                   help='entries verified in parallel (default: %(default)s)')
    p.add_argument('--no-annotate', action='store_true',
                   help='with --apply, do not write "%% bibverify:" comments')
    a = p.parse_args(argv)
    CONTACT_EMAIL = a.email
    APPLY_CORRECTIONS = APPLY_CORRECTIONS if a.apply is None else a.apply
    CHECK_URLS = not a.no_urls
    USE_CACHE = not a.no_cache
    ANNOTATE_BIB = not a.no_annotate
    CACHE_PATH, REPORT_PREFIX, WORKERS = a.cache, a.report, max(1, a.workers)
    return a.bib


NEEDS_ATTENTION = ('REVIEW', 'PROBLEM', 'UNVERIFIED', 'ERROR')


def main(paths):
    """-> [(path, results, report_rows)]. A missing file is an error, never a
    silent fallback to some other .bib."""
    missing = [p for p in paths if not os.path.isfile(p)]
    if missing:
        raise FileNotFoundError(f'no such .bib file: {", ".join(missing)}')
    load_cache()
    all_results = []
    for path in paths:
        db = load_bib(path)
        print(f'\nLoaded {len(db.entries)} entries from {path}')
        results = run_verification(db.entries)
        mark_duplicates(results)
        prefix = REPORT_PREFIX if len(paths) == 1 else \
            f'{REPORT_PREFIX}_{os.path.splitext(os.path.basename(path))[0]}'
        rows = build_reports(results, path, prefix)
        if APPLY_CORRECTIONS:
            apply_corrections(results, db, path)
        else:
            print('\nReport only - the .bib was not modified (use --apply to write corrections).')
        attention = [r for r in rows if r['verdict'] not in QUIET]
        if attention:
            print(f'\n{len(attention)} field-level items need review across '
                  f'{len({r["key"] for r in attention})} entries - see {prefix}.md')
        all_results.append((path, results, rows))
    save_cache()
    return all_results


if __name__ == '__main__':
    try:
        out = main(_parse_cli())
    except FileNotFoundError as e:
        print(f'error: {e}', file=sys.stderr)
        sys.exit(2)
    sys.exit(1 if any(r['status'] in NEEDS_ATTENTION for _, res, _ in out for r in res) else 0)
