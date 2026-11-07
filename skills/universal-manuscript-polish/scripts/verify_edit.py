#!/usr/bin/env python3
"""Check that a universal-manuscript-polish edit changed wording only.

Usage: python verify_edit.py original.tex edited.tex [--allow-integrity-drop]

Exit code 0 when every check passes, 1 otherwise.
"""
import argparse
import re
import sys
from collections import Counter

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

INTEGRITY = re.compile(
    r"implementation[- ]targets?|\bprojected\b|pre-?registered|simulated (?:estimates?|targets?)"
    r"|illustrative (?:values?|numbers?|results?)|(?:yet|remains?) to be (?:measured|confirmed|validated|filled|run)"
    r"|not yet (?:measured|run|implemented|evaluated|validated)|pending (?:validation|evaluation|results?)"
    r"|\bunmeasured\b|placeholder|synthetic (?:targets?|values?|results?)|hypothetical results?"
    r"|\bX{2,}\b|\bX\.X+\b|\?\?|\bTBD\b|\bTODO\b|\bFIXME\b|citation needed", re.I)
EMDASH = re.compile(r"---|\\textemdash|\u2014|(?<=[A-Za-z])\s+--\s+(?=[A-Za-z])|(?<=[a-z])--(?=[a-z])")
MATH_ENVS = r"equation|align|gather|multline|eqnarray|displaymath|math|flalign|alignat|dmath"
FROZEN_ENVS = (r"tabular\*?|tabularx|longtable|algorithmic|lstlisting|verbatim|minted|tikzpicture|axis"
               r"|semilogyaxis|semilogxaxis|loglogaxis|groupplot")
KEY_CMD = re.compile(r"\\(cite[a-zA-Z]*|ref|eqref|autoref|cref|Cref|pageref|label|nameref|includegraphics|url|href"
                     r"|input|include)\*?(?:\[[^\]]*\])*\{([^}]*)\}")
KNOWN_MARKERS = {"tv", "target", "proj", "projected", "todo", "tbd", "placeholder", "hl", "missing", "tocheck"}
NEWCMD = re.compile(r"\\(?:re)?newcommand\*?\s*\{?\\([A-Za-z]+)\}?(?:\[\d\])?(?:\[[^\]]*\])?\s*\{(.*)")
# Prose that some templates (MDPI, plain article) keep in the preamble. It is checked like body text.
PREAMBLE_PROSE = ("title", "Title", "TitleCitation", "abstract", "keyword", "keywords")
# Back-matter statements that use semicolons by convention (CRediT author contributions and similar)
BACKMATTER = ("keywords", "keyword", "authorcontributions","funding", "institutionalreview", "informedconsent", "dataavailability",
              "acknowledgments", "conflictsofinterest", "abbreviations", "sampleavailability")


def pull_macro_args(text, names):
    """Replace the braced argument of each named macro with {} and return (text, full macro calls)."""
    out, args, i = [], [], 0
    pat = re.compile(r"\\(?:" + "|".join(names) + r")\s*\{")
    while True:
        m = pat.search(text, i)
        if not m:
            return "".join(out) + text[i:], args
        k, depth, p = m.end() - 1, 0, m.end() - 1
        for p in range(k, len(text)):
            if text[p - 1] != "\\":
                depth += {"{": 1, "}": -1}.get(text[p], 0)
            if depth == 0:
                break
        out.append(text[i:k] + "{}")
        args.append(text[m.start():p + 1])
        i = p + 1


def split_comments(text):
    code, comments = [], []
    for line in text.split("\n"):
        m = re.search(r"(?<!\\)%", line)
        code.append(line[:m.start()] if m else line)
        if m:
            comments.append(line[m.start():].rstrip())
    return "\n".join(code), comments


def parts(text):
    i = text.find("\\begin{document}")
    return (text[:i], text[i:]) if i >= 0 else ("", text)


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def strip_captions(s):
    out, i = [], 0
    while True:
        j = s.find("\\caption", i)
        if j < 0:
            return "".join(out) + s[i:]
        out.append(s[i:j])
        k = s.find("{", j)
        if k < 0:
            return "".join(out) + s[j:]
        depth = 0
        for p in range(k, len(s)):
            depth += {"{": 1, "}": -1}.get(s[p], 0) if s[p - 1] != "\\" else 0
            if depth == 0:
                break
        i = p + 1


def extract(body):
    """Return math blocks, frozen environments, and prose with both removed."""
    math, frozen = [], []

    def take(store):
        def repl(m):
            store.append(norm(m.group(0)))
            return " "
        return repl

    body = re.sub(r"\\begin\{(" + FROZEN_ENVS + r")\}.*?\\end\{\1\}", lambda m: (frozen.append(norm(strip_captions(m.group(0)))), " ")[1], body, flags=re.S)
    body = re.sub(r"\\begin\{(" + MATH_ENVS + r")(\*?)\}.*?\\end\{\1\2\}", take(math), body, flags=re.S)
    body = re.sub(r"(?<!\\)\\\[.*?(?<!\\)\\\]", take(math), body, flags=re.S)
    body = re.sub(r"(?<!\\)\\\(.*?(?<!\\)\\\)", take(math), body, flags=re.S)
    body = re.sub(r"(?<!\\)\$\$.+?(?<!\\)\$\$", take(math), body, flags=re.S)
    body = re.sub(r"(?<!\\)\$.+?(?<!\\)\$", take(math), body, flags=re.S)
    prose = KEY_CMD.sub(" ", body)
    return math, frozen, prose


def keys(body):
    c = Counter()
    for cmd, arg in KEY_CMD.findall(body):
        for k in (arg.split(",") if cmd.lower().startswith(("cite", "cref")) else [arg]):
            c[(cmd, k.strip())] += 1
    return c


def markers(preamble_raw):
    found, lines = set(), preamble_raw.split("\n")
    for i, l in enumerate(lines):
        m = NEWCMD.search(split_comments(l)[0])
        if m:
            ctx = " ".join(lines[max(0, i - 6): i + 1])
            if (m.group(1).lower() in KNOWN_MARKERS or INTEGRITY.search(ctx)
                    or re.search(r"\\(?:textcolor|color|colorbox|hl)\b", m.group(2))):
                found.add(m.group(1))
    return found | KNOWN_MARKERS


def marker_args(body, names):
    c = Counter()
    for name in names:
        for m in re.finditer(r"\\" + name + r"(?![A-Za-z])\*?\s*\{((?:[^{}]|\{[^{}]*\})*)\}", body):
            c[(name, norm(m.group(1)))] += 1
    return c


def diff(a, b, limit=12):
    removed, added = list((a - b).elements()), list((b - a).elements())
    return f"removed {removed[:limit]}{'...' if len(removed) > limit else ''} | added {added[:limit]}{'...' if len(added) > limit else ''}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("original")
    ap.add_argument("edited")
    ap.add_argument("--allow-integrity-drop", action="store_true",
                    help="downgrade removed integrity marks to WARN (only after per-item author confirmation)")
    args = ap.parse_args()
    raw_o = open(args.original, encoding="utf-8", errors="replace").read()
    raw_e = open(args.edited, encoding="utf-8", errors="replace").read()
    results = []

    def check(name, ok, detail="", warn=False):
        results.append(("PASS" if ok else ("WARN" if warn else "FAIL"), name, detail))

    pre_o, body_raw_o = parts(raw_o)
    pre_e, body_raw_e = parts(raw_e)
    pre_o, prose_pre_o = pull_macro_args(pre_o, PREAMBLE_PROSE)
    pre_e, prose_pre_e = pull_macro_args(pre_e, PREAMBLE_PROSE)
    check("preamble identical (title, abstract, and keywords are checked as body text)", norm(pre_o) == norm(pre_e))
    body_raw_o = "\n".join(prose_pre_o) + "\n" + body_raw_o
    body_raw_e = "\n".join(prose_pre_e) + "\n" + body_raw_e
    bib = r"\\begin\{thebibliography\}.*?\\end\{thebibliography\}|\\(?:bibliography|bibliographystyle|addbibresource)\{[^}]*\}|\\printbibliography"
    check("bibliography identical", [norm(x) for x in re.findall(bib, raw_o, re.S)] == [norm(x) for x in re.findall(bib, raw_e, re.S)])

    code_o, com_o = split_comments(body_raw_o)
    code_e, com_e = split_comments(body_raw_e)
    check("comments unchanged", Counter(com_o) == Counter(com_e), diff(Counter(com_o), Counter(com_e), 4))

    body_o = re.sub(r"\\begin\{thebibliography\}.*?\\end\{thebibliography\}", " ", code_o, flags=re.S)
    body_e = re.sub(r"\\begin\{thebibliography\}.*?\\end\{thebibliography\}", " ", code_e, flags=re.S)
    num = re.compile(r"\d+(?:[.,]\d+)*")
    n_o, n_e = Counter(num.findall(body_o)), Counter(num.findall(body_e))
    check("numbers unchanged", n_o == n_e, diff(n_o, n_e))
    k_o, k_e = keys(body_o), keys(body_e)
    check("citation, reference, label, and graphics keys unchanged", k_o == k_e, diff(k_o, k_e))

    math_o, frozen_o, prose_o = extract(body_o)
    math_e, frozen_e, prose_e = extract(body_e)
    check("math unchanged", Counter(math_o) == Counter(math_e), diff(Counter(math_o), Counter(math_e), 3))
    check("tables, algorithms, code, and plots unchanged", Counter(frozen_o) == Counter(frozen_e),
          diff(Counter(frozen_o), Counter(frozen_e), 2))

    names = markers(pre_o)
    m_o, m_e = marker_args(body_o, names), marker_args(body_e, names)
    check("marker macro uses unchanged", m_o == m_e, diff(m_o, m_e))

    i_o = Counter(x.lower() for x in INTEGRITY.findall(raw_o))
    i_e = Counter(x.lower() for x in INTEGRITY.findall(raw_e))
    dropped = i_o - i_e
    check("integrity and placeholder marks preserved", not dropped,
          f"dropped {dict(dropped)}" + (" (author-confirmed)" if args.allow_integrity_drop else ""),
          warn=args.allow_integrity_drop)

    env = re.compile(r"\\(begin|end)\{([^}]*)\}")
    e_o, e_e = Counter(env.findall(body_o)), Counter(env.findall(body_e))
    unbalanced = [name for (kind, name) in e_e if kind == "begin" and e_e[("begin", name)] != e_e[("end", name)]]
    check("environments unchanged and balanced", e_o == e_e and not unbalanced, diff(e_o, e_e) + f" | unbalanced {unbalanced}")
    brace = lambda s: s.replace("\\{", "").replace("\\}", "").count("{") - s.replace("\\{", "").replace("\\}", "").count("}")
    check("brace balance unchanged", brace(body_o) == brace(body_e), f"original {brace(body_o)}, edited {brace(body_e)}")
    sec = re.compile(r"\\(part|chapter|section|subsection|subsubsection|paragraph|appendix)\b")
    check("sectioning commands unchanged", Counter(sec.findall(body_o)) == Counter(sec.findall(body_e)))

    prose_o = pull_macro_args(prose_o, BACKMATTER)[0]
    prose_e = pull_macro_args(prose_e, BACKMATTER)[0]

    def ctx(s, pat):
        return [norm(s[max(0, m.start() - 40): m.end() + 40]) for m in re.finditer(pat, s)][:3]

    d_o, d_e = len(EMDASH.findall(prose_o)), len(EMDASH.findall(prose_e))
    check("no em dashes added", d_e <= d_o, f"original {d_o}, edited {d_e}")
    if d_e:
        check("em dashes remaining in prose", False, f"{d_e} left, e.g. {ctx(prose_e, EMDASH)}", warn=True)
    s_o, s_e = prose_o.count(";"), prose_e.count(";")
    check("no prose semicolons added", s_e <= s_o, f"original {s_o}, edited {s_e}")
    if s_e:
        check("semicolons remaining in prose", False, f"{s_e} left, e.g. {ctx(prose_e, ';')}", warn=True)

    for status, name, detail in results:
        print(f"{status}  {name}" + (f"  [{detail}]" if status != "PASS" and detail else ""))
    failed = any(s == "FAIL" for s, _, _ in results)
    print(f"\nRESULT: {'FAIL' if failed else 'PASS'}  (numbers {sum(n_o.values())}, citation keys "
          f"{sum(v for (c, _), v in k_o.items() if c.startswith('cite'))}, labels "
          f"{sum(v for (c, _), v in k_o.items() if c == 'label')}, math blocks {len(math_o)}, "
          f"frozen environments {len(frozen_o)}, marker uses {sum(m_o.values())})")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
