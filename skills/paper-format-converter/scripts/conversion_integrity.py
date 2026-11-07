#!/usr/bin/env python3
"""Check that a format conversion kept the manuscript's content.

Usage:
  python -I conversion_integrity.py ORIGINAL CONVERTED [--template SAMPLE]
  python -I conversion_integrity.py --self-test

ORIGINAL and CONVERTED are root files: .tex (\\input, \\include, and \\subfile
are followed), .docx, .md, or .txt. For a PDF-only original, pass its
pdftotext output. SAMPLE is the official template's example manuscript.

Markup may change freely: class, packages, citation commands, starred floats,
"Figure" or "Fig.", caption position, and layout lengths. Content may not.

FAIL (exit 1): original content missing from the conversion (sentences,
numbers, math, citation keys, labels, reference targets, URLs, graphics,
section titles, or figure, table, algorithm, and caption counts), missing
input files, or template sample sentences left in the conversion.
WARN: content the conversion added. Explain each WARN in conversion-report.md.

universal-manuscript-polish/scripts/verify_edit.py checks wording-only edits
and fails by design when the template changes, so it does not fit this job.
"""
import argparse
import html
import re
import sys
import tempfile
import zipfile
from collections import Counter
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# shortcut: \import and \subimport are not followed. Inline those files before comparing.
INPUT = re.compile(r"\\(?:input|include|subfile)\s*\{([^}]+)\}")
UNCOMPILED = re.compile(r"\\begin\{comment\}.*?\\end\{comment\}|\\iffalse\b.*?\\fi\b", re.S)
MATH = re.compile(
    r"\\begin\{(equation|align|gather|multline|eqnarray|flalign|alignat|displaymath|math)(\*?)\}(.*?)\\end\{\1\2\}"
    r"|(?<!\\)\\\[(.*?)(?<!\\)\\\]|(?<!\\)\\\((.*?)(?<!\\)\\\)|(?<!\\)\$\$(.+?)(?<!\\)\$\$|(?<!\\)\$(.+?)(?<!\\)\$",
    re.S)
KEYCMD = re.compile(r"\\([A-Za-z]*(?:cite|ref)[A-Za-z]*|label|includegraphics|input|include|subfile|url|href)\*?"
                    r"\s*(?:\[[^\]]*\]\s*|\([^)]*\)\s*)*\{([^}]*)\}")
# Layout and definition commands, with the number of brace groups that carry no content.
DROP = [
    (r"\\(?:documentclass|usepackage|RequirePackage|bibliographystyle|bibliography|addbibresource|graphicspath"
     r"|pagestyle|thispagestyle|linespread|scalebox|raisebox|vspace|hspace|cline|cmidrule|captionsetup|setlist"
     r"|hypersetup|geometry|tikzset|pgfplotsset)\*?(?![A-Za-z])", 1),
    (r"\\(?:newcommand|renewcommand|providecommand|DeclareMathOperator|newtheorem|setlength|addtolength"
     r"|setcounter|addtocounter|fontsize|resizebox|rule)\*?(?![A-Za-z])", 2),
    (r"\\definecolor(?![A-Za-z])", 3),
    (r"\\begin\{(?:tabular|longtable|array|tblr)\}", 1),
    (r"\\begin\{(?:tabular\*|tabularx|tabulary|xltabular)\}", 2),
]
SECTION = re.compile(r"\\(?:part|chapter|section|subsection|subsubsection|paragraph)\*?\s*(?:\[[^\]]*\])?\s*(?=\{)")
URL = re.compile(r"https?://[^\s{}\\<>\"')\]]+")
NUM = re.compile(r"(?<!\w)\d+(?:[.,]\d+)*(?![\d.,]*\d)(?!(?:pt|bp|mm|cm|in|em|ex|pc|sp|dd|cc|mu|px)(?![A-Za-z])"
                 r"|\s*\\(?:linewidth|textwidth|columnwidth|textheight|hsize|vsize|paperwidth|paperheight"
                 r"|baselineskip|unitlength)(?![A-Za-z]))")
IMAGE_EXT = re.compile(r"\.(?:pdf|png|jpe?g|eps|ps|svg|tiff?|gif|bmp|pgf|tikz)$", re.I)
FOLD = [(r"\bfigs?\.|\bfigures?\b", "fig"), (r"\btabs?\.|\btables?\b", "table"),
        (r"\bsecs?\.|\bsects?\.|\bsections?\b", "sec"), (r"\beqs?\.|\bequations?\b", "eq"),
        (r"\balgs?\.|\balgorithms?\b", "alg"), (r"\bapps?\.|\bappendix\b|\bappendices\b", "app"),
        (r"\bet al\.", "et al"), (r"\be\.g\.", "eg"), (r"\bi\.e\.", "ie"), (r"\bcf\.", "cf"), (r"\bvs\.", "vs")]


def group_end(s, i):
    """s[i] is '{'. Return the index just past its matching '}'."""
    depth, j = 0, i
    while j < len(s):
        if s[j] == "\\":
            j += 2
            continue
        depth += (s[j] == "{") - (s[j] == "}")
        if depth == 0:
            return j + 1
        j += 1
    return len(s)


def drop(s, pattern, nargs):
    """Delete each match of pattern with its [..] or (..) options and its first nargs brace groups."""
    rx, out, i = re.compile(pattern), [], 0
    while m := rx.search(s, i):
        out.append(s[i:m.start()])
        j, taken = m.end(), 0
        while taken < nargs:
            t = j
            while t < len(s) and s[t].isspace():
                t += 1
            if t < len(s) and s[t] in "[(":
                close = s.find("]" if s[t] == "[" else ")", t)
                if close < 0:
                    break
                j = close + 1
            elif t < len(s) and s[t] == "{":
                j, taken = group_end(s, t), taken + 1
            else:
                break
        i = j
    return "".join(out) + s[i:]


def read_tex(path, root, seen):
    path = path.resolve()
    if path in seen or not path.is_file():
        return ""
    seen.add(path)
    text = re.sub(r"(?<!\\)%.*", "", path.read_text(encoding="utf-8", errors="replace"))

    def child(m):
        name = m.group(1).strip()
        for base in (root, path.parent):
            for candidate in (base / name, base / f"{name}.tex"):
                if candidate.is_file():
                    return read_tex(candidate, root, seen)
        return m.group(0)

    return INPUT.sub(child, text)


def words_of(text):
    return " ".join(re.findall(r"\w+", re.sub(r"\\[A-Za-z@]+\*?", " ", text).lower()))


def prose_stats(text):
    low = text.lower()
    for pattern, short in FOLD:
        low = re.sub(pattern, short, low)
    sentences, words = Counter(), 0
    for chunk in re.split(r"[.!?]+(?:\s+|$)", low):
        tokens = re.findall(r"\w+", chunk)
        words += len(tokens)
        if len(tokens) >= 6:
            sentences[" ".join(tokens)] += 1
    return sentences, words


def take_math(text):
    found = Counter()

    def repl(m):
        inner = next(g for g in m.groups()[2:] if g is not None)
        found[re.sub(r"\\label\{[^}]*\}|\\nonumber|\\notag|\s+", "", inner)] += 1
        return " MATH "

    return MATH.sub(repl, text), found


def tex_inventory(path):
    path = Path(path)
    t = UNCOMPILED.sub(" ", read_tex(path, path.resolve().parent, set()))
    inv = {"kind": "tex", "urls": Counter(u.rstrip(".,;:") for u in URL.findall(t)), "unresolved": []}
    envs = Counter(re.findall(r"\\begin\{([A-Za-z]+)\*?\}", t))
    inv["figures"] = envs["figure"] + envs["sidewaysfigure"] + envs["wrapfigure"]
    inv["subfigures"] = envs["subfigure"] + len(re.findall(r"\\sub(?:float|captionbox)(?![A-Za-z])", t))
    inv["tables"] = envs["table"] + envs["sidewaystable"] + envs["wraptable"] + envs["longtable"]
    inv["algorithms"] = envs["algorithm"]
    inv["captions"] = len(re.findall(r"\\caption(?:of)?\*?\s*[\[{]", t))
    t = re.sub(r"(\\begin\{[^}]*\})\s*\[[^\]]*\]", r"\1", t)
    for pattern, nargs in DROP:
        t = drop(t, pattern, nargs)
    for k in ("cite", "ref", "label", "graphics"):
        inv[k] = Counter()

    def key(m):
        cmd, arg = m.group(1).lower(), m.group(2)
        if cmd in ("url", "href") or cmd.endswith("name"):
            pass
        elif "cite" in cmd or "ref" in cmd:
            inv["cite" if "cite" in cmd else "ref"].update(k.strip() for k in arg.split(",") if k.strip())
        elif cmd == "label":
            inv["label"][arg.strip()] += 1
        elif cmd == "includegraphics":
            inv["graphics"][IMAGE_EXT.sub("", arg.strip().replace("\\", "/").rsplit("/", 1)[-1]).lower()] += 1
        else:
            inv["unresolved"].append(arg.strip())
        return " "

    t = KEYCMD.sub(key, t)
    t, inv["math"] = take_math(t)
    inv["sections"], parts, i = Counter(), [], 0
    while m := SECTION.search(t, i):
        end = group_end(t, m.end())
        title = t[m.end() + 1:end - 1]
        inv["sections"][words_of(title)] += 1
        parts.append(f"{t[i:m.start()]} . {title} . ")
        i = end
    t = "".join(parts) + t[i:]
    inv["numbers"] = Counter(NUM.findall(URL.sub(" ", t).replace("{,}", ",")))
    prose = re.sub(r"\\(?:item|par|maketitle|and|newline|linebreak)(?![A-Za-z])|\\\\|\\(?:begin|end)\s*\{[^}]*\}"
                   r"|\n\s*\n", " . ", t)
    inv["sentences"], inv["words"] = prose_stats(re.sub(r"\\[A-Za-z@]+\*?|\\.|[{}&~$]", " ", prose))
    return inv


def docx_inventory(path):
    with zipfile.ZipFile(path) as z:
        names = set(z.namelist())
        xml = " ".join(z.read(n).decode("utf-8", "replace") for n in
                       ("word/document.xml", "word/footnotes.xml", "word/endnotes.xml") if n in names)
    inv = {"kind": "docx", "math": Counter(), "sections": Counter(), "captions": 0}
    for block in re.findall(r"<m:oMath(?:\s[^>]*)?>(.*?)</m:oMath>", xml, re.S):
        inv["math"]["".join(re.findall(r"<m:t(?:\s[^>]*)?>([^<]*)</m:t>", block)).replace(" ", "")] += 1
    xml = re.sub(r"<m:oMath(?:\s[^>]*)?>.*?</m:oMath>", "<w:t> MATH </w:t>", xml, flags=re.S)
    inv["tables"] = xml.count("<w:tbl>")
    inv["figures"] = len(re.findall(r"<w:drawing>|<w:pict>", xml))
    paragraphs = []
    for p in re.findall(r"<w:p[ >].*?</w:p>", xml, re.S):
        text = html.unescape("".join(re.findall(r"<w:t(?:\s[^>]*)?>([^<]*)</w:t>",
                                                p.replace("<w:tab/>", "<w:t> </w:t>"))))
        style = re.search(r'<w:pStyle w:val="([^"]+)"', p)
        style = style.group(1).lower() if style else ""
        if "heading" in style and text.strip():
            inv["sections"][words_of(text)] += 1
        inv["captions"] += "caption" in style
        paragraphs.append(text)
    body = " . ".join(paragraphs)
    inv["urls"] = Counter(u.rstrip(".,;:") for u in URL.findall(body))
    inv["numbers"] = Counter(NUM.findall(URL.sub(" ", body)))
    inv["sentences"], inv["words"] = prose_stats(body)
    return inv


def md_inventory(path):
    t = Path(path).read_text(encoding="utf-8", errors="replace")
    if Path(path).suffix.lower() == ".txt":  # pdftotext output: rejoin hyphenated words, treat pages as breaks
        t = re.sub(r"(\w)-\r?\n(\w)", r"\1\2", t).replace("\f", "\n\n")
    t = re.sub(r"<!--.*?-->|```.*?```", " ", t, flags=re.S)
    inv = {"kind": "md", "urls": Counter(u.rstrip(".,;:") for u in URL.findall(t))}
    images = re.findall(r"!\[[^\]]*\]\(\s*<?([^)\s>]+)", t)
    inv["graphics"] = Counter(IMAGE_EXT.sub("", g.replace("\\", "/").rsplit("/", 1)[-1]).lower() for g in images)
    inv["figures"] = len(images)
    inv["tables"] = len(re.findall(r"^\s*\|?\s*:?-{3,}:?\s*(?:\|\s*:?-{3,}:?\s*)+\|?\s*$", t, re.M))
    inv["cite"] = Counter(re.findall(r"(?<![\w@])@([\w:-]+(?:[./][\w:-]+)*)", t))
    inv["sections"] = Counter(words_of(h) for h in re.findall(r"^#{1,6}\s+(.+?)\s*#*\s*$", t, re.M))
    t, inv["math"] = take_math(t)
    t = re.sub(r"!\[[^\]]*\]\([^)]*\)|\[@[^\]]*\]|(?<![\w@])@[\w:./-]+|`[^`]*`", " ", URL.sub(" ", t))
    t = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", t)
    t = re.sub(r"^#{1,6}\s+(.+?)\s*#*\s*$", r" . \1 . ", t, flags=re.M)
    t = re.sub(r"\n\s*\n|^\s*(?:[-*+]|\d+\.)\s+", " . ", t, flags=re.M)
    inv["numbers"] = Counter(NUM.findall(t))
    inv["sentences"], inv["words"] = prose_stats(re.sub(r"[*_|<>#]", " ", t))
    return inv


def inventory(path):
    if not Path(path).is_file():
        sys.exit(f"Not found: {path}")
    suffix = Path(path).suffix.lower()
    if suffix == ".tex":
        return tex_inventory(path)
    if suffix in (".docx", ".dotx"):
        return docx_inventory(path)
    if suffix in (".md", ".markdown", ".txt"):
        return md_inventory(path)
    sys.exit(f"Unsupported file type: {path}. Pass .tex, .docx, .md, or .txt (pdftotext output for a PDF).")


def show(counter, limit=5):
    items = [f'"{k[:90]}"' + (f" x{n}" if n > 1 else "") for k, n in list(counter.items())[:limit]]
    return ", ".join(items) + (f", and {len(counter) - limit} more" if len(counter) > limit else "")


def compare(a, b, template=None):
    results, same = [], a["kind"] == b["kind"]
    for k in ("sentences", "numbers", "math", "cite", "label", "ref", "urls", "graphics", "sections"):
        if k not in a or k not in b:
            continue
        if k == "math" and not same:
            na, nb = sum(a[k].values()), sum(b[k].values())
            results.append(("PASS" if na == nb else "WARN", k, f"{na} vs {nb} expressions, compared by count across formats"))
            continue
        missing, added = a[k] - b[k], b[k] - a[k]
        if missing:
            results.append(("FAIL", k, f"{sum(missing.values())} missing: {show(missing)}"))
        if added:
            results.append(("WARN", k, f"{sum(added.values())} added: {show(added)}"))
        if not missing and not added:
            results.append(("PASS", k, f"{sum(a[k].values())} matched"))
    for k in ("figures", "subfigures", "tables", "algorithms", "captions"):
        if k in a and k in b:
            status = "PASS" if a[k] == b[k] else ("FAIL" if b[k] < a[k] and same else "WARN")
            results.append((status, k, f"original {a[k]}, converted {b[k]}"))
    if b.get("unresolved"):
        results.append(("FAIL", "inputs", f"the conversion pulls in missing files: {b['unresolved']}"))
    if a.get("unresolved"):
        results.append(("WARN", "inputs", f"the original pulls in missing files: {a['unresolved']}"))
    if template is not None:
        left = (b["sentences"] & template["sentences"]) - a["sentences"]
        results.append(("FAIL", "template text", f"{sum(left.values())} sample sentence(s) left: {show(left)}") if left
                       else ("PASS", "template text", "no sentence from the template sample remains"))
    results.append(("INFO", "words", f"original {a['words']}, converted {b['words']}"))
    return results


def self_test():
    original = r"""\documentclass[11pt]{article}
\usepackage[numbers]{natbib}
\renewcommand{\arraystretch}{1.2}
\title{A Test Paper on Conversion Integrity}
\begin{document}
\maketitle
\begin{abstract}
We study how a format conversion can silently drop content from a manuscript.
\end{abstract}
\input{intro}
\section{Results}
As shown in Figure~\ref{fig:a}, the method reaches 92.4\% accuracy on 3 datasets \citep{smith2020,lee2021}.
\begin{figure}[t]
\centering
\includegraphics[width=0.8\linewidth]{figs/plot.png}
\caption{Accuracy of the proposed method across all three benchmark datasets.}
\label{fig:a}
\end{figure}
\begin{table}[h]
\begin{tabular}{p{2cm}cc}
Model & Acc & F1 \\
Ours & 92.4 & 0.871 \\
\end{tabular}
\caption{Main results of the comparison against the strongest baseline.}
\label{tab:main}
\end{table}
\begin{equation}
E = mc^2 \label{eq:e}
\end{equation}
Code and data are available at \url{https://example.org/code} for all readers.
\bibliographystyle{plainnat}
\bibliography{refs}
\end{document}
"""
    intro = r"""\section{Introduction}
Deep learning models need careful evaluation before anyone deploys them in practice.
See Table~\ref{tab:main} and Eq.~\eqref{eq:e}.
"""
    caption = "\\caption{Main results of the comparison against the strongest baseline.}\n\\label{tab:main}\n"
    converted = (original.replace(r"\documentclass[11pt]{article}", r"\documentclass[journal]{IEEEtran}")
                 .replace(r"\usepackage[numbers]{natbib}", r"\usepackage{cite}")
                 .replace(r"\renewcommand{\arraystretch}{1.2}", "")
                 .replace(r"\input{intro}", intro)
                 .replace("Figure~", "Fig.~").replace(r"\citep", r"\cite")
                 .replace(r"\begin{figure}[t]", r"\begin{figure*}[!t]").replace(r"\end{figure}", r"\end{figure*}")
                 .replace(r"[width=0.8\linewidth]{figs/plot.png}", r"[width=\textwidth]{figures/plot.pdf}")
                 .replace("\\end{tabular}\n" + caption, "\\end{tabular}\n")
                 .replace("\\begin{table}[h]\n\\begin{tabular}{p{2cm}cc}", "\\begin{table}[!t]\n" + caption
                          + "\\begin{tabular}{lcc}")
                 .replace(r"E = mc^2 \label{eq:e}", "E = m c^2\n\\label{eq:e}")
                 .replace("plainnat", "IEEEtran"))
    sample = "This sample paragraph shows authors where the body text of the paper begins."
    broken = (converted.replace("Deep learning models need careful evaluation before anyone deploys them in practice.", "")
              .replace("0.871", "0.817").replace("smith2020,lee2021", "smith2020")
              .replace("\\label{tab:main}\n", "").replace("\\section{Results}", "\\section{Results}\n" + sample))
    assert converted != original and "\\label{tab:main}" not in broken and caption in converted

    def docx(path, paragraphs, tables):
        body = "".join(f"<w:p><w:r><w:t>{p}</w:t></w:r></w:p>" for p in paragraphs) + "<w:tbl></w:tbl>" * tables
        with zipfile.ZipFile(path, "w") as z:
            z.writestr("word/document.xml", f'<w:document xmlns:w="w"><w:body>{body}</w:body></w:document>')

    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        files = {"orig/main.tex": original, "orig/intro.tex": intro, "ok/main.tex": converted, "bad/main.tex": broken,
                 "tmpl/sample.tex": f"\\documentclass{{IEEEtran}}\n\\begin{{document}}\n{sample}\n\\end{{document}}\n",
                 "a.md": "# Intro\n\nThe method improves recall on every dataset we tested.\n\n![Plot](figs/a.png)\n\n"
                         "As reported before [@smith2020], recall matters most here.\n",
                 "b.md": "# Intro\n\nThe method improves recall on every dataset we tested.\n"}
        for name, text in files.items():
            (d / name).parent.mkdir(parents=True, exist_ok=True)
            (d / name).write_text(text, encoding="utf-8")
        template = inventory(d / "tmpl/sample.tex")
        original_inv = inventory(d / "orig/main.tex")
        ok = compare(original_inv, inventory(d / "ok/main.tex"), template)
        assert not [r for r in ok if r[0] in ("FAIL", "WARN")], ok
        bad = compare(original_inv, inventory(d / "bad/main.tex"), template)
        failed = {name for status, name, _ in bad if status == "FAIL"}
        assert {"sentences", "numbers", "cite", "label", "template text"} <= failed, bad
        assert "ref" not in failed and "graphics" not in failed, bad
        p1 = "The first paragraph of the test document has enough words to count."
        p2 = "The second paragraph also has enough words to count as a sentence."
        docx(d / "a.docx", [p1, p2], 1)
        docx(d / "b.docx", [p1], 0)
        failed = {name for status, name, _ in compare(inventory(d / "a.docx"), inventory(d / "b.docx")) if status == "FAIL"}
        assert {"sentences", "tables"} <= failed, failed
        failed = {name for status, name, _ in compare(inventory(d / "a.md"), inventory(d / "b.md")) if status == "FAIL"}
        assert {"sentences", "cite", "graphics", "figures"} <= failed, failed
    print("SELF-TEST PASS")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("original", nargs="?")
    ap.add_argument("converted", nargs="?")
    ap.add_argument("--template", help="the official template's sample manuscript")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    if not (args.original and args.converted):
        ap.print_help()
        return 2
    results = compare(inventory(args.original), inventory(args.converted),
                      inventory(args.template) if args.template else None)
    for status, name, detail in results:
        print(f"{status:<5} {name}: {detail}")
    fails = sum(s == "FAIL" for s, _, _ in results)
    warns = sum(s == "WARN" for s, _, _ in results)
    print(f"\nRESULT: {'FAIL' if fails else 'PASS'} ({fails} failed, {warns} warnings). "
          "Fix or justify every FAIL in conversion-report.md.")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
