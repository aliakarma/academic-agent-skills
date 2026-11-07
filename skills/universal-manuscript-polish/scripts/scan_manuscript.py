#!/usr/bin/env python3
"""Inventory editorial candidates in a LaTeX manuscript for the universal-manuscript-polish skill.

Usage: python scan_manuscript.py manuscript.tex [--max N]

The scanner reports candidates only. The editor decides what to change.
"""
import argparse
import re
import sys
from collections import Counter, defaultdict

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

INTEGRITY = re.compile(
    r"implementation[- ]targets?|\bprojected\b|pre-?registered|simulated (?:estimates?|targets?)"
    r"|illustrative (?:values?|numbers?|results?)|(?:yet|remains?) to be (?:measured|confirmed|validated|filled|run)"
    r"|not yet (?:measured|run|implemented|evaluated|validated)|pending (?:validation|evaluation|results?)"
    r"|\bunmeasured\b|placeholder|synthetic (?:targets?|values?|results?)|hypothetical results?",
    re.I)
PLACEHOLDER = re.compile(
    r"\bX{2,}\b|\bX\.X+\b|\?\?|\bTBD\b|\bTODO\b|\bFIXME\b|\\lipsum|citation needed|\\cite\{\s*\}")
SPECULATIVE = re.compile(
    r"\b(?:will|would|should|may|might|could|shall)\b|\b(?:is|are) expected\b|\bexpected to\b"
    r"|\banticipated?\b|\bintend(?:s|ed)? to\b|\baims? to\b|\bplans? to\b|\bplanned\b|\bpreliminary\b"
    r"|\bongoing\b|\bto be (?:evaluated|implemented|tested|validated|conducted|determined|explored|investigated|studied)\b"
    r"|\bfuture work\b|\bwe hope\b|\bhopefully\b|\bpotentially\b|\b(?:is|are) likely to\b", re.I)
SLOP = re.compile(
    r"plays? an? (?:crucial|pivotal|vital|key|critical) role|garnered (?:significant|considerable|growing) attention"
    r"|\bin recent years\b|paradigm shift|pav(?:e|es|ing) the way|\bto this end\b"
    r"|it is (?:worth noting|important to note|imperative)|\bdelv(?:e|es|ing)\b|\bleverag(?:e|es|ed|ing)\b"
    r"|\bharness(?:es|ed|ing)?\b|\blandscape\b|\btapestry\b|cutting-edge|groundbreaking|\bholistic\b"
    r"|\bseamless(?:ly)?\b|\bmoreover\b|\bfurthermore\b|\bin conclusion\b|\bin summary\b|\butiliz(?:e|es|ed|ing|ation)\b"
    r"|shed(?:s|ding)? light|a myriad of|\bmultifaceted\b|\bunderscor(?:e|es|ed|ing)\b|\bshowcas(?:e|es|ed|ing)\b"
    r"|ever-evolving|\brevolutioniz\w*|\bremarkabl[ey]\b|\bvery\b|\breally\b|\bbasically\b|\bactually\b|\bcertainly\b"
    r"|\bwe (?:attempt|attempted|try|tried) to\b|it is hoped|to some extent|\bsomewhat\b|\barguably\b|\bin some sense\b",
    re.I)
# En dashes stay in ranges (3--5) and paired names (Hazen--Williams). Lowercase word--word is a dash misuse.
EMDASH = re.compile(r"---|\\textemdash|\u2014|(?<=[A-Za-z])\s+--\s+(?=[A-Za-z])|(?<=[a-z])--(?=[a-z])")
# Back-matter statements that use semicolons by convention (CRediT author contributions and similar)
BACKMATTER = re.compile(r"\\(?:keywords?|authorcontributions|funding|institutionalreview|informedconsent|dataavailability"
                        r"|acknowledgments|conflictsofinterest|abbreviations|sampleavailability)\b")

IZE_STEMS = ("optimi|minimi|maximi|normali|initiali|generali|regulari|visuali|characteri|organi|recogni|reali"
             "|utili|summari|prioriti|categori|standardi|synchroni|speciali|parameteri|tokeni|vectori|discreti"
             "|randomi|stabili|locali|personali|customi|authori|emphasi|critici|digiti|anonymi|centrali|formali"
             "|hypothesi|memori|mobili|moderni|neutrali|operationali|penali|publici|quanti|rationali|symboli"
             "|theori|economi|harmoni|finali|contextuali|conceptuali|globali|lemmati|binari|capitali|democrati")
BRITISH_PATTERNS = [
    (re.compile(r"\b((?:de|re|un|over|under)?(?:" + IZE_STEMS + r"))s(e|ed|es|ing|ation|ations|er|ers|able)\b", re.I),
     lambda m: m.group(1) + "z" + m.group(2)),
    (re.compile(r"\b(analy|cataly|paraly|dialy)s(e|ed|ing|er|ers)\b", re.I), lambda m: m.group(1) + "z" + m.group(2)),
    (re.compile(r"\b(behavio|colo|favo|hono|labo|neighbo|rumo|vapo|harbo|flavo|endeavo|humo|armo|savo|tumo)ur"
                r"(s|ed|ing|ite|ites|able|hood|al)?\b", re.I), lambda m: m.group(1) + "r" + (m.group(2) or "")),
    (re.compile(r"\b(cent|fib|lit|theat|calib|spect|kilomet|centimet|millimet)re(s|d)?\b", re.I),
     lambda m: m.group(1) + "er" + (m.group(2) or "")),
    (re.compile(r"\b(model|label|travel|cancel|signal|fuel|level|channel|tunnel|marshal|total|dial|equal|counsel)l"
                r"(ed|ing|er|ers)\b", re.I), lambda m: m.group(1) + m.group(2)),
]
BRITISH_WORDS = {
    "defence": "defense", "offence": "offense", "licence": "license", "programme": "program",
    "programmes": "programs", "ageing": "aging", "grey": "gray", "artefact": "artifact", "artefacts": "artifacts",
    "catalogue": "catalog", "analogue": "analog", "whilst": "while", "amongst": "among", "towards": "toward",
    "afterwards": "afterward", "fulfil": "fulfill", "fulfilment": "fulfillment", "enrolment": "enrollment",
    "judgement": "judgment", "acknowledgement": "acknowledgment", "aluminium": "aluminum", "sceptical": "skeptical",
    "manoeuvre": "maneuver", "focussed": "focused", "focussing": "focusing", "learnt": "learned", "spelt": "spelled",
    "tyre": "tire", "tyres": "tires", "mould": "mold", "sulphur": "sulfur", "orientated": "oriented",
    "per cent": "percent", "practise": "practice", "paediatric": "pediatric", "oesophageal": "esophageal",
}
BRITISH_WORD_RE = re.compile(r"\b(" + "|".join(re.escape(w) for w in BRITISH_WORDS) + r")\b", re.I)

FROZEN_ENVS = ("tabular", "tabular*", "tabularx", "longtable", "algorithmic", "lstlisting", "verbatim", "minted",
               "tikzpicture", "axis", "semilogyaxis", "semilogxaxis", "loglogaxis", "groupplot")
MATH_ENVS = ("equation", "align", "gather", "multline", "eqnarray", "displaymath", "flalign", "alignat")
KNOWN_MARKERS = {"tv", "target", "proj", "projected", "todo", "tbd", "placeholder", "hl", "missing", "tocheck"}
NEWCMD = re.compile(r"\\(?:re)?newcommand\*?\s*\{?\\([A-Za-z]+)\}?(?:\[\d\])?(?:\[[^\]]*\])?\s*\{(.*)")


def strip_comment(line):
    m = re.search(r"(?<!\\)%", line)
    return (line[:m.start()], line[m.start():]) if m else (line, "")


def snippet(text, m=None, width=80):
    text = re.sub(r"\s+", " ", text).strip()
    if m is None or len(text) <= 2 * width:
        return text[: 2 * width]
    s = max(0, m.start() - width)
    return ("..." if s else "") + text[s: m.end() + width] + ("..." if m.end() + width < len(text) else "")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("tex")
    ap.add_argument("--max", type=int, default=300, help="max hits printed per category")
    args = ap.parse_args()
    lines = open(args.tex, encoding="utf-8", errors="replace").read().split("\n")

    doc_start = next((i for i, l in enumerate(lines) if "\\begin{document}" in strip_comment(l)[0]), -1)
    hits = defaultdict(list)
    section, env_depth, math_depth, in_bib = "(preamble)" if doc_start >= 0 else "(body)", 0, 0, False
    prose_words = Counter()

    # Marker macros from the preamble
    markers = {}
    for i, l in enumerate(lines[: max(doc_start, 0)]):
        code, _ = strip_comment(l)
        m = NEWCMD.search(code)
        if not m:
            continue
        name, body = m.group(1), m.group(2)
        context = " ".join(lines[max(0, i - 6): i + 1])
        strong = name.lower() in KNOWN_MARKERS or bool(INTEGRITY.search(context)) or "todo" in body.lower()
        if strong or re.search(r"\\(?:textcolor|color|colorbox|hl)\b", body):
            markers[name] = (i + 1, strong)
    for name, (defline, strong) in markers.items():
        uses = [i + 1 for i, l in enumerate(lines) if re.search(r"\\" + name + r"(?![A-Za-z])", strip_comment(l)[0])
                and i + 1 != defline]
        label = "marker macro" if strong else "possible marker macro (colors text)"
        if uses:
            hits["INTEGRITY"].append((defline, f"{label} \\{name}: {len(uses)} uses, first at L{uses[0]}"))

    # Title, abstract, and keywords that templates such as MDPI place in the preamble are scanned as body text
    preamble_prose = set()
    if doc_start > 0:
        pre = "\n".join(lines[:doc_start])
        for m in re.finditer(r"\\(?:title|Title|TitleCitation|abstract|keywords?)\s*\{", pre):
            depth, p = 0, m.end() - 1
            for p in range(m.end() - 1, len(pre)):
                if pre[p - 1] != "\\":
                    depth += {"{": 1, "}": -1}.get(pre[p], 0)
                if depth == 0:
                    break
            preamble_prose.update(range(pre.count("\n", 0, m.start()), pre.count("\n", 0, p) + 1))

    for idx, raw in enumerate(lines):
        n = idx + 1
        code, comment = strip_comment(raw)
        for m in INTEGRITY.finditer(raw):
            hits["INTEGRITY"].append((n, ("[comment] " if comment and m.start() >= len(code) else "") + snippet(raw, m)))
            break
        for m in PLACEHOLDER.finditer(raw):
            hits["PLACEHOLDER"].append((n, snippet(raw, m)))
            break
        if doc_start >= 0 and idx <= doc_start and idx not in preamble_prose:
            continue
        if "\\begin{thebibliography}" in code:
            in_bib = True
        if in_bib:
            in_bib = "\\end{thebibliography}" not in code
            continue
        sec = re.search(r"\\(?:sub)*section\*?\{([^}]*)\}", code)
        if sec:
            section = sec.group(1)
        for e in FROZEN_ENVS:
            env_depth += code.count("\\begin{" + e + "}") - code.count("\\end{" + e + "}")
        for e in MATH_ENVS:
            math_depth += code.count("\\begin{" + e) - code.count("\\end{" + e)
        if env_depth > 0 or math_depth > 0 or not code.strip():
            continue
        prose = re.sub(r"(?<!\\)\$[^$]*(?<!\\)\$", " ", code)
        prose = re.sub(r"\\(?:cite\w*|ref|eqref|label|url|href|includegraphics)\*?(?:\[[^\]]*\])*\{[^}]*\}", " ", prose)
        tag = " [future-work section]" if "future" in section.lower() else (
            " [limitations section]" if "limitation" in section.lower() else "")
        for m in SPECULATIVE.finditer(prose):
            hits["SPECULATIVE"].append((n, f"'{m.group(0)}'{tag}: " + snippet(prose, m)))
        for pat, fix in BRITISH_PATTERNS:
            for m in pat.finditer(prose):
                hits["BRITISH"].append((n, f"{m.group(0)} -> {fix(m)}"))
        for m in BRITISH_WORD_RE.finditer(prose):
            hits["BRITISH"].append((n, f"{m.group(0)} -> {BRITISH_WORDS[m.group(0).lower()]}"))
        for m in EMDASH.finditer(prose):
            hits["EMDASH"].append((n, snippet(prose, m)))
        if ";" in prose and not BACKMATTER.search(code):
            hits["SEMICOLON"].append((n, snippet(prose, re.search(";", prose))))
        for m in SLOP.finditer(prose):
            hits["SLOP"].append((n, f"'{m.group(0)}': " + snippet(prose, m)))
        prose_words.update(w.lower() for w in re.findall(r"[A-Za-z]+(?:-[A-Za-z]+)+|[A-Za-z]+", prose))
        for m in re.finditer(r"(?<=[A-Za-z.])[ \t]+\\(cite[pt]?|ref|eqref)\{", code):
            hits["CONSISTENCY"].append((n, f"missing '~' before \\{m.group(1)}: " + snippet(code, m)))

    body = "\n".join(strip_comment(l)[0] for l in lines[doc_start + 1:])
    for w in sorted(k for k in prose_words if "-" in k):
        joined = w.replace("-", "")
        if prose_words[joined]:
            hits["CONSISTENCY"].append((0, f"hyphenation variants: '{w}' x{prose_words[w]} vs '{joined}' x{prose_words[joined]}"))
    styles = {"Figure~\\ref": r"Figure~?\\ref", "Fig.~\\ref": r"Fig\.~?\\ref", "Table~\\ref": r"Table~?\\ref",
              "Tab.~\\ref": r"Tab\.~?\\ref", "Eq.~\\eqref": r"Eq\.~?\\(?:eq)?ref", "Equation~\\eqref": r"Equation~?\\(?:eq)?ref",
              "Section~\\ref": r"Section~?\\ref", "Sec.~\\ref": r"Sect?\.~?\\ref"}
    counts = {k: len(re.findall(v, body)) for k, v in styles.items()}
    for a, b in (("Figure~\\ref", "Fig.~\\ref"), ("Table~\\ref", "Tab.~\\ref"),
                 ("Eq.~\\eqref", "Equation~\\eqref"), ("Section~\\ref", "Sec.~\\ref")):
        if counts[a] and counts[b]:
            hits["CONSISTENCY"].append((0, f"mixed reference style: {a} x{counts[a]} vs {b} x{counts[b]}"))
    defs = defaultdict(list)
    for i, l in enumerate(lines[doc_start + 1:], start=doc_start + 2):
        for m in re.finditer(r"\(([A-Z][A-Za-z0-9-]*[A-Z0-9]s?)\)", strip_comment(l)[0]):
            defs[m.group(1)].append(i)
    for abbr, where in sorted(defs.items()):
        if len(where) > 1:
            hits["CONSISTENCY"].append((where[0], f"abbreviation ({abbr}) defined {len(where)} times: L{where}"))
        first_use = next((i for i, l in enumerate(lines[doc_start + 1:], start=doc_start + 2)
                          if re.search(r"\b" + re.escape(abbr) + r"\b", strip_comment(l)[0])), None)
        if first_use and first_use < where[0]:
            hits["CONSISTENCY"].append((first_use, f"abbreviation {abbr} used at L{first_use} before definition at L{where[0]}"))

    order = ["INTEGRITY", "PLACEHOLDER", "SPECULATIVE", "BRITISH", "EMDASH", "SEMICOLON", "SLOP", "CONSISTENCY"]
    notes = {"INTEGRITY": "never reword on assumption, report as blockers",
             "PLACEHOLDER": "never fill, report", "SPECULATIVE": "classify each with the SKILL.md table",
             "BRITISH": "skip keys, URLs, names, cited titles", "EMDASH": "remove all in prose under STRICT, reduce under STANDARD, keep numeric ranges",
             "SEMICOLON": "split in prose", "SLOP": "cut or replace, never strengthen claims",
             "CONSISTENCY": "use the dominant form"}
    print(f"confirm-results scan: {args.tex}")
    print(f"preamble ends at L{doc_start + 1}" if doc_start >= 0 else "no \\begin{document}: whole file scanned as body")
    print("summary: " + " | ".join(f"{c} {len(hits[c])}" for c in order))
    for c in order:
        print(f"\n== {c} ({notes[c]}) ==")
        if not hits[c]:
            print("  none")
        for n, text in hits[c][: args.max]:
            print(f"  {'L' + str(n) if n else '--'}: {text}")
        if len(hits[c]) > args.max:
            print(f"  ... {len(hits[c]) - args.max} more (raise --max)")


if __name__ == "__main__":
    main()
