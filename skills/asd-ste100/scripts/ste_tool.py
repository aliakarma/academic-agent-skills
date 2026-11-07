#!/usr/bin/env python3
"""Look up words in the ASD-STE100 Issue 9 dictionary and check text against its rules.

The word list is read on each run from the user's own authorized copy of the ASD-STE100 PDF.
No extracted copy is stored, and the PDF is not distributed with this skill (see REFERENCES.md).
PDF location, first match wins: --pdf PATH, the ASD_STE100_PDF environment variable,
references/ASD-STE100_ISSUE9.pdf inside the skill folder.

Usage:
  python ste_tool.py lookup WORD [WORD ...]
  python ste_tool.py check FILE [FILE ...]      (.html, .htm, .txt, .md)
  python ste_tool.py selftest

The check is a mechanical aid. It cannot confirm approved meanings (Rule 1.3) or the
part of speech in context (Rule 1.2), so its result never proves compliance alone.
"""
from __future__ import annotations

import argparse
import collections
import os
import re
import sys
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path

PDF = Path(os.environ.get("ASD_STE100_PDF") or Path(__file__).resolve().parent.parent / "references" / "ASD-STE100_ISSUE9.pdf")
WORD_LIST_START = 148  # 0-based index of PDF page 149, dictionary page 2-1-A1
VERB_LIST_PAGE = 146   # 0-based index of PDF page 147, "List of approved verbs"
POS = r"(?:n|v|adj|adv|pron|art|prep|conj|prefix)"
HEAD = re.compile(rf"^(?P<word>[A-Za-z][^()]*?(?:\s\([^()]*\))?)\s\((?P<pos>{POS})\)(?P<rest>.*)$")
LABEL = re.compile(r"^2-1-[A-Z]\d+$")


def _open(pdf=PDF):
    if not Path(pdf).is_file():
        sys.exit(f"ste_tool: PDF not found: {pdf}. Supply your own authorized copy with --pdf or ASD_STE100_PDF (see REFERENCES.md).")
    try:
        import pymupdf as fitz
    except ImportError:
        try:
            import fitz  # type: ignore[import-untyped]
        except ImportError:
            sys.exit("ste_tool: PyMuPDF is not installed (pip install pymupdf). Until then, read the dictionary "
                     "pages of the standard instead.")
    return fitz.open(str(pdf))


def _lines(words, tol=2.5):
    """Group (x, y, text) words into text lines, top to bottom."""
    out = []
    for x, y, t in sorted(words, key=lambda w: (w[1], w[0])):
        if out and abs(out[-1][0] - y) <= tol:
            out[-1][1].append((x, t))
        else:
            out.append([y, [(x, t)]])
    return [(y, " ".join(t for _, t in sorted(ws))) for y, ws in out]


@dataclass(eq=False)
class Entry:
    word: str             # as printed: "REMOVE", "chance (by chance)", "FOR EXAMPLE"
    pos: str              # "n", "v", "adj", ... or "" for the two phrase entries
    rest: str             # text after the part of speech (verb and adjective forms)
    label: str            # dictionary page, for example "2-1-R9"
    pdf: int              # PDF page number
    y: float
    cells: dict = field(default_factory=lambda: {2: [], 3: [], 4: []})

    @property
    def base(self):
        return self.word.split(" (")[0]

    @property
    def approved(self):
        return self.base.upper() == self.base

    @property
    def key(self):
        return self.base.lower()

    @property
    def phrase(self):
        """Text to search for: "chance (by chance)" -> "by chance", "so (that)" -> "so that"."""
        paren = self.word.partition(" (")[2].rstrip(")").strip().lower()
        if not paren or paren.startswith("or "):
            return self.key
        return paren if self.key in paren else f"{self.key} {paren}"

    @property
    def forms(self):
        found = {f.lower() for f in re.findall(r"[A-Z][A-Z'\-]+", self.rest)}
        alt = re.search(r"\(or ([A-Z]+)\)", self.word)          # MATT (or MATTE)
        return {self.key} | found | ({alt[1].lower()} if alt else set())

    def text(self, col):
        return " ".join(t for _, t in _lines(self.cells[col]))

    def ref(self):
        return f"dictionary page {self.label}, PDF page {self.pdf}"


def load_entries(pdf=PDF):
    doc = _open(pdf)
    entries = []
    for pno in range(WORD_LIST_START, doc.page_count):
        words = doc[pno].get_text("words")
        head = {w[4]: w for w in words if w[1] < 150}
        if "Approved" not in head:          # blank page at the end of the word list
            continue
        ste_x = min(w[0] for w in words if w[4] == "STE" and w[1] < 150)
        # Column text starts up to 5 pt left of its header. Text of the column before ends 13+ pt left of it.
        bounds = [head["Approved"][0] - 11, ste_x - 11, head["Non-STE"][0] - 11]
        top = max(head[k][3] for k in ("Approved", "ALTERNATIVES") if k in head)
        bottom = min((w[1] for w in words if w[4] == "Page" and w[1] > 600), default=800)
        label = next((w[4] for w in words if LABEL.match(w[4])), "?")
        cols = collections.defaultdict(list)
        for w in words:
            if top < w[1] < bottom - 1:
                cols[1 + sum(w[0] >= b for b in bounds)].append((w[0], w[1], w[4]))
        # Lines in one cell are 12 pt apart (16.5 pt before a note). A new row starts 18.5+ pt lower.
        cells = []
        for y, text in _lines(cols[1]):
            if cells and y - cells[-1][2] < 17.5:
                prev = cells[-1][1]
                cells[-1][1] = prev[:-1] + text if prev.endswith("-") else f"{prev} {text}"
                cells[-1][2] = y
            else:
                cells.append([y, text, y])
        page = []
        for y, text, _ in cells:
            m = HEAD.match(text)
            word, pos, rest = (m["word"].strip(), m["pos"], m["rest"].strip()) if m else (text, "", "")
            page.append(Entry(word, pos, rest, label, pno + 1, y))
        for col in (2, 3, 4):
            for x, y, t in cols[col]:
                owners = [e for e in page if e.y <= y + 3]
                # Text above the first row continues the last entry of the previous page.
                target = owners[-1] if owners else (entries[-1] if entries else None)
                if target:
                    target.cells[col].append((x, y if owners else y + 1000, t))
        entries.extend(page)
    return entries


class Dictionary:
    def __init__(self, entries):
        self.entries = entries
        self.approved = set()                              # approved single-word forms
        self.not_approved = collections.defaultdict(list)  # single word -> entries
        self.phrases = {}                                  # multi-word phrase -> entry
        self.verbs = set()
        # Approved multi-word entries (AWAY FROM, MAKE SURE, IN FRONT OF) are masked like declared terms.
        self.approved_phrases = [e.key for e in entries if e.approved and " " in e.key and "..." not in e.key]
        for e in entries:
            if e.approved:
                if " " not in e.key:
                    self.approved |= e.forms
                if e.pos == "n" and " " not in e.key:      # plurals of countable nouns are permitted
                    k = e.key
                    self.approved |= {k + "s", k + "es", k[:-1] + "ies" if k.endswith("y") else k + "s"}
                if e.pos == "v":
                    self.verbs.add(e.key)
            elif " " in e.phrase:
                self.phrases[e.phrase] = e
            else:
                self.not_approved[e.phrase].append(e)

    def find(self, word):
        w = word.lower().strip()
        hits = [e for e in self.entries if w in (e.key, e.phrase) or w in e.forms]
        if not hits:
            hits = [e for e in self.entries for c in _lemmas(w) if c in (e.key, e.phrase)]
        return list(dict.fromkeys(hits))


def _lemmas(t):
    out = [t]
    if t.endswith("ies") or t.endswith("ied"):
        out.append(t[:-3] + "y")
    if t.endswith("es"):
        out.append(t[:-2])
    if t.endswith("s") and not t.endswith("ss"):
        out.append(t[:-1])
    if t.endswith("ed"):
        out += [t[:-2], t[:-1]] + ([t[:-3]] if len(t) > 4 and t[-3] == t[-4] else [])
    if t.endswith("ing"):
        out += [t[:-3], t[:-3] + "e"] + ([t[:-4]] if len(t) > 5 and t[-4] == t[-5] else [])
    return out


# ---------------------------------------------------------------- lookup

def lookup(d, words):
    for word in words:
        hits = d.find(word)
        print(f"== {word}")
        if not hits:
            print("   Not in the STE dictionary. Use it only as a technical noun (Rule 1.5) or a technical")
            print("   verb (Rule 1.12) of your subject field, or find an approved synonym and look that up.")
            continue
        for e in hits:
            status = "APPROVED" if e.approved else "NOT APPROVED"
            forms = f"  forms: {e.rest}" if e.approved and e.rest else ""
            print(f"   {e.word} ({e.pos or 'phrase'}): {status}{forms}")
            print(f"     {'meaning' if e.approved else 'alternatives'}: {e.text(2)}")
            if e.text(3):
                print(f"     STE example: {e.text(3)}")
            if e.text(4):
                print(f"     non-STE example: {e.text(4)}")
            print(f"     source: {e.ref()}")


# ---------------------------------------------------------------- check

SKIP_TAGS = {"script", "style", "code", "pre", "kbd", "samp", "var", "math", "blockquote", "q", "cite", "noscript"}
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
BLOCK = {"p", "li", "dt", "dd", "td", "th", "h1", "h2", "h3", "h4", "h5", "h6", "figcaption", "caption",
         "summary", "button", "label", "legend", "title", "desc", "text", "option", "div", "section", "nav"}
LABELS = {"h1", "h2", "h3", "h4", "h5", "h6", "th", "summary", "button", "label", "legend", "title", "text", "option"}
TERM_TAGS = {"dfn", "dt", "abbr"}
TEXT_ATTRS = ("alt", "aria-label", "title", "placeholder")


class _Text(HTMLParser):
    """Collect visible text units (kind, text, line) and the phrases declared as terms."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.units, self.terms, self.buf, self.kind, self.line = [], set(), [], "prose", 1
        self.skip, self.term_depth, self.term_buf = None, 0, []

    def _flush(self):
        text = re.sub(r"\s+", " ", "".join(self.buf)).strip()
        if text:
            self.units.append((self.kind, text, self.line))
        self.buf = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if self.skip:
            if tag == self.skip[0] and tag not in VOID:
                self.skip[1] += 1
            return
        if tag in SKIP_TAGS or a.get("data-ste") == "skip":
            if tag not in VOID:
                self.skip = [tag, 1]
            return
        for name in TEXT_ATTRS:
            if a.get(name):
                self.units.append(("label", a[name], self.getpos()[0]))
        if a.get("data-term"):
            self.terms |= _variants(a["data-term"])
        if tag in BLOCK:
            self._flush()
            self.kind, self.line = ("label" if tag in LABELS else "prose"), self.getpos()[0]
        if tag in TERM_TAGS:
            self.term_depth += 1

    def handle_startendtag(self, tag, attrs):
        if not self.skip:
            for name in TEXT_ATTRS:
                v = dict(attrs).get(name)
                if v:
                    self.units.append(("label", v, self.getpos()[0]))

    def handle_endtag(self, tag):
        if self.skip:
            if tag == self.skip[0]:
                self.skip[1] -= 1
                if self.skip[1] == 0:
                    self.skip = None
            return
        if tag in TERM_TAGS and self.term_depth:
            self.term_depth -= 1
            if not self.term_depth:
                self.terms |= _variants("".join(self.term_buf))
                self.term_buf = []
        if tag in BLOCK:
            self._flush()
            self.kind = "prose"

    def handle_data(self, data):
        if self.skip:
            return
        if self.term_depth:
            self.term_buf.append(data)
        if not self.buf:
            self.line = self.getpos()[0]
        self.buf.append(data)


def _variants(term):
    """A declared term, its form without a parenthetical, and the parenthetical itself:
    "Multi-Agent Reinforcement Learning (MARL)" -> the full text, "multi-agent reinforcement learning", "marl"."""
    t = " ".join(term.lower().split()).strip(" .,:;")
    out = {t, re.sub(r"\s*\([^)]*\)", "", t).strip()} | set(re.findall(r"\(([^)]*)\)", t))
    return {v.strip() for v in out if v.strip()}


def _term_forms(t):
    """A term and its irregular plurals: study/studies, hypothesis/hypotheses, criterion/criteria."""
    forms = {t}
    if t.endswith("y"):
        forms.add(t[:-1] + "ies")
    if t.endswith("is"):
        forms.add(t[:-2] + "es")
    if t.endswith("on"):
        forms.add(t[:-2] + "a")
    return forms


def _term_pattern(terms):
    if not terms:
        return None
    alts = "|".join(re.escape(f) for f in sorted({f for t in terms for f in _term_forms(t)}, key=len, reverse=True))
    # Plural and past participle forms are permitted for technical nouns and verbs (Rules 1.4, 1.13).
    return re.compile(rf"(?<![\w-])(?:{alts})(?:s|es|d|ed)?(?![\w-])", re.I)


def read_units(path):
    raw = Path(path).read_text(encoding="utf-8", errors="replace")
    if Path(path).suffix.lower() in (".html", ".htm"):
        p = _Text()
        p.feed(raw)
        p.close()
        p._flush()
        return p.units, p.terms
    units, line = [], 1
    for block in re.split(r"\n\s*\n", raw):
        text = " ".join(block.split())
        if text:
            units.append(("label" if text.startswith("#") else "prose", text.lstrip("# "), line))
        line += block.count("\n") + 2
    return units, set()


ABBREV = re.compile(r"\b(?:e\.g|i\.e|etc|vs|cf|viz|et al|Fig|Figs|Eq|Eqs|Sec|Ch|No|pp?|Ref|Dr|approx|a\.m|p\.m)\.", re.I)
UNITS = {"%", "ms", "s", "h", "min", "kg", "g", "mm", "cm", "m", "km", "hz", "khz", "mhz", "ghz", "w", "kw",
         "v", "a", "k", "b", "kb", "mb", "gb", "tb", "px", "db", "x", "°c", "°f"}


def sentences(text):
    protected = ABBREV.sub(lambda m: m.group(0).replace(".", "․"), text)
    parts = re.split(r"(?<=[.!?])\s+(?=[\"'“(\[]?[A-Z0-9])", protected)
    return [p.replace("․", ".").strip() for p in parts if p.strip()]


def word_count(sentence):
    """Count words with the conventions of Rules 8.5 to 8.7."""
    s = re.sub(r"\([^()]*\)", " W ", sentence)                    # text in parentheses: one word
    s = re.sub(r"[\"“][^\"”]*[\"”]", " W ", s)       # quoted text: one word
    toks = [t for t in s.split() if re.search(r"[A-Za-z0-9]", t)]  # hyphenated words stay one token
    n, i = 0, 0
    while i < len(toks):
        if re.fullmatch(r"[\d.,]+", toks[i]) and i + 1 < len(toks) and toks[i + 1].lower().strip(".,;:") in UNITS:
            i += 1                                                 # number with unit: one word
        n, i = n + 1, i + 1
    return n


RULES = [  # (rule, severity, pattern, message)
    ("8.1", "error", re.compile(r";"), "semicolon (not permitted)"),
    ("4.2", "error", re.compile(r"\b\w+(?:n't|'re|'ve|'ll|'m|'d)\b|\b(?:it|that|there|here|what|let|who)'s\b", re.I), "contraction"),
    ("3.6", "error", re.compile(r"\b(?:is|are|was|were|be|been|being)\s+\w+(?:ed|en|wn|ne|nt|ld|pt|de)\s+by\b", re.I),
     "passive voice with a known agent (use the agent as the subject)"),
    ("3.4", "error", re.compile(r"\b(?:has|have|had)\s+(?:been\s+)?\w+(?:ed|en|wn|ne)\b", re.I), "perfect tense (not approved)"),
    ("GR-6", "error", re.compile(r"\b(?:e\.g|i\.e|etc|viz|cf|vs)\.|\bet al\.", re.I), "Latin abbreviation"),
    ("GR-7", "error", re.compile(r"\b(?:he|she|him|his|hers|himself|herself)\b", re.I), "gender-specific pronoun"),
    ("house", "error", re.compile(r"—|\s–\s"), "em dash or spaced en dash (user house style, not an STE rule)"),
]


def read_register(path):
    """Terminology register: one term per line, tab, then TN or TV and its category. Lines with # are notes."""
    if not path or not Path(path).is_file():
        return set()
    lines = Path(path).read_text(encoding="utf-8").splitlines()
    return {v for ln in lines if ln.strip() and not ln.startswith("#") for v in _variants(ln.split("\t")[0])}


def check_file(d, path, register=None):
    units, terms = read_units(path)
    terms |= read_register(register or Path(path).parent / "_qa" / "ste-terms.tsv")
    declared = _term_pattern(terms | set(d.approved_phrases))  # masked before the vocabulary check
    words = {f for t in terms if not re.search(r"[\s-]", t) for f in _term_forms(t)}  # parts of hyphenated words
    errors, review = collections.defaultdict(list), collections.defaultdict(collections.Counter)
    stats = collections.Counter()
    for kind, text, line in units:
        sents = sentences(text) if kind == "prose" else [text]
        if kind == "prose" and len(sents) > 6 and len(text) > 200:
            errors[("6.6", "paragraph has more than six sentences")].append((line, f"{len(sents)} sentences: {text[:90]}..."))
        for s in sents:
            for rule, _, pat, msg in RULES:
                m = pat.search(s)
                if m:
                    errors[(rule, msg)].append((line, s))
            if kind == "prose":
                stats["sentences"] += 1
                n = word_count(s)
                first = (re.findall(r"[A-Za-z]+", s) or [""])[0].lower()
                limit = 20 if first in d.verbs and not s.endswith("?") else 25
                stats["longest"] = max(stats["longest"], n)
                if n > limit:
                    errors[("5.1/6.3", f"sentence longer than its limit")].append((line, f"{n} words, limit {limit}: {s}"))
                for inner in re.findall(r"\(([^()]*)\)", s):         # Rule 8.5: text in parentheses is its own sentence
                    if word_count(inner) > 25:
                        errors[("8.5", "text in parentheses longer than 25 words")].append((line, inner))
            masked = declared.sub(" TERM ", s) if declared else s
            low = masked.lower()
            for phrase, e in d.phrases.items():
                if re.search(rf"(?<![\w-]){re.escape(phrase)}(?![\w-])", low):
                    errors[("1.1", "not approved")].append((line, f'"{phrase}" -> {e.text(2)} ({e.ref()})'))
            for i, tok in enumerate(re.findall(r"[A-Za-z][A-Za-z'\-]*", masked)):
                if tok == "TERM" or (tok.isupper() and len(tok) > 1):
                    continue                                       # declared term, or abbreviation (Rule 8.6)
                for part in tok.split("-"):
                    _classify(d, part, tok, i, errors, review, line, words)
    return errors, review, stats


# Rule 1.5 lists these as technical nouns: numbers, units, and time (category 9) and colors (category 17).
CATEGORY_WORDS = set("zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen "
                     "sixteen seventeen eighteen nineteen twenty thirty forty fifty sixty seventy eighty ninety hundred "
                     "thousand million billion first second third fourth fifth sixth seventh eighth ninth tenth half "
                     "quarter twice minute hour month year percent "
                     "red green blue yellow orange black white gray grey brown purple pink cyan magenta beige".split())
ROMAN = re.compile(r"^m{0,3}(cm|cd|d?c{0,3})(xc|xl|l?x{0,3})(ix|iv|v?i{0,3})$")


def _classify(d, part, tok, index, errors, review, line, declared_words=frozenset()):
    w = re.sub(r"'s?$", "", part).lower()
    if len(w) < 2 or w in CATEGORY_WORDS or w[:-1] in CATEGORY_WORDS and w.endswith("s") or ROMAN.match(w):
        return
    if w in declared_words or any(c in declared_words for c in _lemmas(w)):
        return
    if re.search(r"[a-z][A-Z]", part):
        return                                                     # CamelCase name: ExampleNet, RiskAcceptable
    if index > 0 and part[:1].isupper() and not tok.isupper():
        return                                                     # proper noun or named item
    if w in d.approved:
        if w in d.not_approved:
            e = d.not_approved[w][0]
            review[("1.2", "approved only as another part of speech")][f"{w}: {e.word} ({e.pos}) is not approved, alternatives {e.text(2)}"] += 1
        return
    na = next((c for c in _lemmas(w) if c in d.not_approved), None)
    if na:
        e = d.not_approved[na][0]
        errors[("1.1", "not approved")].append((line, f'"{w}" -> {e.text(2)} ({e.ref()})'))
    elif any(c in d.approved for c in _lemmas(w)[1:]):
        review[("1.4/3.1", "form not given in the dictionary for this approved word")][w] += 1
    elif w.endswith("ing"):
        review[("3.5", '"-ing" word: permitted only as a technical noun or part of one')][w] += 1
    else:
        review[("1.1", "not in the dictionary: declare it as a technical noun or verb (glossary <dt>, <dfn>, data-term) or replace it")][w] += 1


def report(path, errors, review, stats):
    print(f"STE check: {path}")
    print(f"  {stats['sentences']} sentences checked, longest {stats['longest']} words "
          f"(limits: 25 descriptive, 20 procedural)")
    n_err = sum(len(v) for v in errors.values())
    if errors:
        print("ERRORS (fix these)")
        for (rule, msg), items in sorted(errors.items()):
            print(f"  [{rule}] {msg}: {len(items)}")
            for line, s in items[:8]:
                print(f"     line {line}: {s[:160]}")
            if len(items) > 8:
                print(f"     ... {len(items) - 8} more")
    if review:
        print("REVIEW (decide by hand)")
        for (rule, msg), counts in sorted(review.items()):
            words = ", ".join(f"{w} ({c})" for w, c in counts.most_common(40))
            print(f"  [{rule}] {msg}: {words}")
    print(f"Result: {n_err} errors, {sum(sum(c.values()) for c in review.values())} review items. "
          "Approved meanings (Rule 1.3) still need a manual check.")
    return n_err


# ---------------------------------------------------------------- self-test

def selftest(d):
    approved = sum(e.approved for e in d.entries)
    assert (approved, len(d.entries) - approved) == (879, 1319), (approved, len(d.entries) - approved)
    doc = _open()
    listed = {v.lower() for v in re.findall(r"\b[A-Z][A-Z\-]+(?: (?:ON|OFF|SURE))?\b",
                                            doc[VERB_LIST_PAGE].get_text().split("find the approved verbs.")[1])}
    assert listed == d.verbs, sorted(listed ^ d.verbs)
    acc = d.find("acceptable")
    assert acc and not acc[0].approved and "PERMITTED" in acc[0].text(2), acc
    rem = d.find("removes")
    assert rem and rem[0].approved and "removed" in rem[0].forms, rem
    assert d.find("by chance") and d.find("such as")
    assert word_count("Make sure that the EMER pushbutton switch is released (the EMER legend is off).") == 10
    assert word_count("The unit weighs 20 kg.") == 4
    assert sentences("See Fig. 2 for the flow. It has two parts.") == ["See Fig. 2 for the flow.", "It has two parts."]
    import tempfile
    sample = ("<html><body><h1>Test page</h1><p>The data is processed by the server; it's fast. "
              "The operator has adjusted the linkage. Utilize the tool, e.g. the probe.</p>"
              "<p>This long sentence has many words in it so that it goes past the limit of twenty five words "
              "for a descriptive sentence in this text.</p>"
              "<pre><code>utilize(); // skipped</code></pre><dl><dt>Gradient</dt><dd>A gradient shows a slope.</dd></dl>"
              "<details><summary data-term=\"technical explanation\">Technical explanation</summary>"
              "<p>This explanation is short.</p></details><p>The paper gives four checks in step (ii).</p>"
              "<p>ExampleNet extends the green phase by 20 seconds.</p>"
              "<p>The studies keep the gate away from the signal-phase data and the predicted criteria.</p>"
              "<p data-ste=\"skip\">Utilize this quoted source text.</p></body></html>")
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as f:
        f.write(sample)
    with tempfile.NamedTemporaryFile("w", suffix=".tsv", delete=False, encoding="utf-8") as r:
        r.write("# term\ttype and category\nlinkage\tTN 1\nstudy\tTN 15\nsignal\tTN 6\nphase\tTN 6\n"
                "gate\tTN 19\npredict\tTV 3a\ncriterion\tTN 7\n")
    errors, review, _ = check_file(d, f.name, r.name)
    Path(f.name).unlink()
    Path(r.name).unlink()
    assert not any(w == "linkage" for c in review.values() for w in c), review   # declared in the register
    rules = {r for r, _ in errors}
    assert {"8.1", "4.2", "3.6", "3.4", "GR-6", "1.1", "5.1/6.3"} <= rules, rules
    flagged = " ".join(s for (r, _), v in errors.items() for _, s in v)
    assert flagged.count('"utilize"') == 1, flagged                   # code and data-ste="skip" were skipped
    unknown = {w for (r, _), c in review.items() if r == "1.1" for w in c}
    assert "gradient" not in unknown, unknown                         # declared in <dt>
    assert "explanation" in unknown, unknown                          # only the declared phrase is exempt
    assert "technical" not in unknown, unknown
    assert not {"four", "ii", "green", "seconds", "examplenet"} & unknown, unknown   # Rule 1.5, names
    assert not {"studies", "away", "signal", "phase", "predicted", "criteria"} & unknown, unknown  # forms, AWAY FROM
    print("selftest passed: 879 approved and 1319 not-approved entries, 208 approved verbs match page 2-0-19")


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("command", choices=["lookup", "check", "selftest"])
    ap.add_argument("args", nargs="*")
    ap.add_argument("--pdf", default=str(PDF), help="path to ASD-STE100_ISSUE9.pdf")
    ap.add_argument("--terms", help="terminology register (default: _qa/ste-terms.tsv next to the checked file)")
    a = ap.parse_args()
    d = Dictionary(load_entries(a.pdf))
    if a.command == "lookup":
        lookup(d, a.args)
    elif a.command == "check":
        total = 0
        for path in a.args:
            total += report(path, *check_file(d, path, a.terms))
        sys.exit(1 if total else 0)
    else:
        selftest(d)


if __name__ == "__main__":
    main()
