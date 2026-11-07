#!/usr/bin/env python3
"""Check an idea-to-paper LaTeX project against the skill's hard rules.

Usage:
  python check_paper.py main.tex [--bib references.bib] [--log main.log]
                        [--pdf main.pdf] [--pages 6-8] [--min-refs 25]
                        [--targets-out _build/target_register.md]
  python check_paper.py --selftest

Errors (exit 1):
  E01 skeleton marker left (<<FILL or a DEMO block)
  E02 placeholder text (TBD, TODO, ??, "will be added later", ...)
  E03 paragraph, item, or caption wrapped across lines
  E04 unescaped percent after a digit, or an inline comment inside prose
  E05 forced line break (\\ or \newline) inside prose
  E06 environment mismatch or unclosed environment
  E07 unbalanced braces
  E08 figure, table, or algorithm without caption or label, or label before caption
  E09 numbered equation without a label
  E10 duplicate label
  E11 reference to an undefined label
  E12 figure, table, equation, or algorithm label never referenced
  E13 package loaded twice
  E14 em dash in prose
  E15 semicolon in prose
  E16 targets used without the visible notice, or target macros neutralized
  E17 float with numeric data that is neither a marked target nor tagged
      % MEASURED: / % CONFIG: / % SOURCE:
  E18 F1 differs from 2PR/(P+R) in a table row (skipped for macro-averaged tables)
  E19 percentage-type metric above 100
  E20 cited key missing from the bib, or a cited entry without doi and url
  E21 fewer distinct cited references than --min-refs
  E22 build log error, undefined reference or citation, multiply defined label
  E23 page count outside --pages, or not checkable
Warnings: W01 caption placement, W03 decimal or percent number outside \\tgt{}
in a results-type paragraph, W04 external image, W06 overfull box wider than
5pt, W08 class is not IEEEtran conference, W12 section label never referenced.

Stock phrasing is not checked here: run universal-manuscript-polish's
scan_manuscript.py for that. Citation-key escaping and duplicates: run
Literature-Review's audit_citations.py. Standard library only. A clean run is
necessary, not sufficient: compile the paper and look at every page as well.
"""
import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

NONPROSE = {"tikzpicture", "axis", "semilogyaxis", "semilogxaxis", "loglogaxis", "groupplot", "scope",
            "tabular", "tabular*", "tabularx", "array", "equation", "equation*", "align", "align*",
            "gather", "gather*", "multline", "multline*", "split", "cases", "matrix", "pmatrix",
            "bmatrix", "algorithmic", "verbatim", "lstlisting", "IEEEeqnarray", "filecontents"}
FLOATS = {"figure", "figure*", "table", "table*", "algorithm"}
NUMBERED_EQ = {"equation", "align", "gather", "multline"}
STRUCT = re.compile(r"^\s*(\\(begin|end|section|subsection|subsubsection|paragraph|item|label|caption|"
                    r"centering|vspace|vfill|hspace|maketitle|bibliography|bibliographystyle|input|include|"
                    r"newpage|clearpage|balance|small|footnotesize|scriptsize|setlength|renewcommand|"
                    r"newcommand|resizebox|includegraphics|appendix|title|author|IEEEauthorblock[NA]|"
                    r"toprule|midrule|bottomrule|hline|cline|cmidrule|IEEEtriggeratref)\b|\\\[|\\\]|[{}]\s*$)")
OPENS_TEXT = re.compile(r"^\s*\\(item|paragraph|noindent)\b")  # structural start, but the line is prose
NEW_PARA = re.compile(r"^\s*\\(item|paragraph)\b")  # these start a new unit, so they never continue a line
PLACEHOLDER = re.compile(r"\bTBD\b|\bTODO\b|\bFIXME\b|\bXXX+\b|\?\?|lorem ipsum|to be added|will be added later|"
                         r"\[PASTE|results? will be (reported|added|provided)|future implementation", re.I)
# Same em-dash rule as universal-manuscript-polish/scan_manuscript.py: en dashes stay in ranges (3--5).
EMDASH = re.compile(r"---|\\textemdash|\u2014|(?<=[A-Za-z])\s+--\s+(?=[A-Za-z])|(?<=[a-z])--(?=[a-z])")
RESULTS_SEC = re.compile(r"result|evaluat|ablation|compar|performance|scalab|robust|discussion|"
                         r"analysis|conclusion|introduction", re.I)
REFCMD = re.compile(r"\\(?:ref|eqref|autoref|cref|Cref|pageref)\{([^}]*)\}")
CITECMD = re.compile(r"\\cite[a-zA-Z]*\*?(?:\[[^\]]*\])*\{([^}]*)\}")


def strip_comment(line):
    return re.split(r"(?<!\\)%", line, maxsplit=1)[0]


def demath(text):
    text = re.sub(r"\$[^$]*\$", " ", text)
    text = re.sub(r"\\\(.*?\\\)", " ", text)
    return re.sub(r"\\(cite[a-zA-Z]*|ref|eqref|label|url|autoref|cref|Cref)\{[^}]*\}", " ", text)


def first_number(cell):
    cell = re.split(r"\\pm|±", re.sub(r"\\cite[a-zA-Z]*\{[^}]*\}", "", cell))[0]
    m = re.search(r"-?\d+(?:\.(\d+))?", cell)
    return (float(m.group(0)), len(m.group(1) or "")) if m else (None, 0)


class Checker:
    def __init__(self):
        self.items = []

    def add(self, level, code, line, msg):
        self.items.append((level, code, line, msg))

    def errors(self):
        return [i for i in self.items if i[0] == "ERROR"]


def check_tex(tex_path, ck):
    raw_lines = Path(tex_path).read_text(encoding="utf-8", errors="replace").splitlines()
    body_start = next((i for i, l in enumerate(raw_lines) if "\\begin{document}" in strip_comment(l)), 0)
    full = "\n".join(raw_lines)
    uses_tgt = bool(re.search(r"\\tgt\{|\\tgtcap\b", re.sub(r"\\newcommand\{\\tgt(cap)?\}.*", "", full)))
    stack, labels, refs, floats, eqs, packages = [], {}, [], [], [], {}
    section, prev, prev_comment, skip_group, depth = "", None, "", 0, 0
    for n, raw in enumerate(raw_lines, 1):
        code = strip_comment(raw)
        is_comment_only = raw.strip().startswith("%")
        if "<<FILL" in raw or ">>> DEMO" in raw:
            ck.add("ERROR", "E01", n, "skeleton marker left: " + raw.strip()[:70])
        for ch in re.sub(r"\\[{}]", "", code):
            depth += (ch == "{") - (ch == "}")
            if depth < 0:
                ck.add("ERROR", "E07", n, "closing brace without an opening brace")
                depth = 0
        for m in re.finditer(r"\\usepackage(?:\[[^\]]*\])?\{([^}]*)\}", code):
            for p in (x.strip() for x in m.group(1).split(",")):
                if p in packages:
                    ck.add("ERROR", "E13", n, f"package '{p}' already loaded on line {packages[p]}")
                packages.setdefault(p, n)
        ctx = list(stack)  # environments open at line start decide the context
        for m in re.finditer(r"\\(begin|end)\{([^}]+)\}", code):
            kind, env = m.groups()
            if kind == "begin":
                stack.append((env, n))
                if env in FLOATS:
                    floats.append({"env": env, "start": n, "lines": [], "section": section, "end": None})
                if env in NUMBERED_EQ:
                    eqs.append({"env": env, "start": n, "lines": [], "end": None})
            elif stack and stack[-1][0] == env:
                stack.pop()
            else:
                ck.add("ERROR", "E06", n, f"\\end{{{env}}} closes {stack[-1][0] if stack else 'nothing'}")
                if any(e == env for e, _ in stack):
                    while stack[-1][0] != env:
                        stack.pop()
                    stack.pop()
        for blk in floats + eqs:
            if blk["end"] is None:
                blk["lines"].append((n, raw))
                if (blk["env"], blk["start"]) not in stack:
                    blk["end"] = n
        for m in re.finditer(r"\\label\{([^}]*)\}", code):
            inner = [e for e, _ in reversed(ctx + stack) if e in FLOATS or e in NUMBERED_EQ]
            if m.group(1) in labels:
                ck.add("ERROR", "E10", n, f"duplicate label '{m.group(1)}' (first on line {labels[m.group(1)][0]})")
            else:
                labels[m.group(1)] = (n, inner[0] if inner else "section")
        refs += [(k.strip(), n) for m in REFCMD.finditer(code) for k in m.group(1).split(",")]
        sec = re.search(r"\\section\*?\{([^}]*)\}", code)
        if sec:
            section = sec.group(1)
        if n - 1 <= body_start or is_comment_only:
            prev_comment = raw if is_comment_only else prev_comment
            continue
        if skip_group or re.match(r"^\s*\\(author|title)\b", code):  # author block may legally use \\
            skip_group = max(skip_group + code.count("{") - code.count("}"), 0)
            prev = None
            continue
        if PLACEHOLDER.search(code):
            ck.add("ERROR", "E02", n, "placeholder text: " + PLACEHOLDER.search(code).group(0))
        if re.search(r"\d%", raw):
            ck.add("ERROR", "E04", n, "unescaped % after a number comments out the rest of the line (use \\%)")
        if not code.strip():
            prev, prev_comment = None, ""
            continue
        open_envs = {e for e, _ in ctx}
        prose = not ((open_envs | set(re.findall(r"\\begin\{([^}]+)\}", code))) & NONPROSE)
        if prose:
            structural = bool(STRUCT.match(code)) and not OPENS_TEXT.match(code)
            if not structural and re.search(r"\S\s*(?<!\\)%", raw) and not re.search(r"\d%", raw):
                ck.add("ERROR", "E04", n, "inline comment inside prose drops the text after the % sign")
            if not structural and re.search(r"\\\\|\\newline\b", code):
                ck.add("ERROR", "E05", n, "forced line break inside a paragraph")
            text = demath(code)
            if EMDASH.search(text):
                ck.add("ERROR", "E14", n, "em dash in prose")
            if ";" in text:
                ck.add("ERROR", "E15", n, "semicolon in prose")
            if prev and prev[2]:
                p_struct = bool(STRUCT.match(prev[1])) and not OPENS_TEXT.match(prev[1])
                p_open = prev[1].count("{") > prev[1].count("}")
                cont = not NEW_PARA.match(code) and (not STRUCT.match(code) or OPENS_TEXT.match(code))
                if cont and (not p_struct or p_open):
                    ck.add("ERROR", "E03", n, f"line continues the paragraph from line {prev[0]} (one paragraph per line)")
            if uses_tgt and (RESULTS_SEC.search(section) or "abstract" in open_envs) and not structural \
                    and "MEASURED:" not in prev_comment:
                for sent in re.split(r"(?<=\.)\s+", code):
                    if "\\cite" in sent:
                        continue
                    nums = re.findall(r"\d+\.\d+|\d+(?:\.\d+)?\\%", demath(re.sub(r"\\tgt\{[^{}]*\}", " ", sent)))
                    if nums:
                        ck.add("WARN", "W03", n, f"number(s) outside \\tgt{{}}: {', '.join(nums[:4])} "
                                                 "(mark as target, or put a '% MEASURED: <source>' line above)")
        if "\\includegraphics" in code:
            ck.add("WARN", "W04", n, "external image: TikZ is required unless the author supplied this file")
        prev, prev_comment = (n, code, prose), ""
    if depth:
        ck.add("ERROR", "E07", len(raw_lines), f"{depth} unclosed brace(s) at end of file")
    for env, start in stack:
        ck.add("ERROR", "E06", start, f"\\begin{{{env}}} never closed")
    for f in floats:
        check_float(f, ck)
    for q in eqs:
        code = "\n".join(strip_comment(r) for _, r in q["lines"])
        rows = [r for r in re.split(r"\\\\(?!\[)", code) if r.strip() and not r.strip().startswith("\\end")] \
            if q["env"] in ("align", "gather") else [code]
        numbered = sum(1 for r in rows if not re.search(r"\\(nonumber|notag)\b", r))
        if len(re.findall(r"\\label\{", code)) < numbered:
            ck.add("ERROR", "E09", q["start"], f"{q['env']} has {numbered} numbered line(s) but fewer labels")
    referenced = {k for k, _ in refs}
    for key, line in refs:
        if key not in labels:
            ck.add("ERROR", "E11", line, f"reference to undefined label '{key}'")
    for key, (line, kind) in labels.items():
        if key not in referenced:
            if kind != "section" or re.match(r"(fig|tab|eq|alg):", key):
                ck.add("ERROR", "E12", line, f"label '{key}' is never referenced in the text")
            else:
                ck.add("WARN", "W12", line, f"section label '{key}' is never referenced")
    if uses_tgt:
        if len(re.findall(r"\\tgtnotice\b", full)) - len(re.findall(r"\\newcommand\{\\tgtnotice\}", full)) < 1:
            ck.add("ERROR", "E16", 1, "implementation targets are used but \\tgtnotice is not shown in the paper")
        if not re.search(r"\\newcommand\{\\tgt\}\[1\]\{\\textcolor\{", full) or \
                re.search(r"\\(renewcommand|def)\s*\{?\\(tgt|tgtcap|tgtnotice)\b", full):
            ck.add("ERROR", "E16", 1, "\\tgt must stay defined as \\textcolor{...}{#1} and must not be redefined")
    if not re.search(r"\\documentclass\[[^\]]*conference[^\]]*\]\{IEEEtran\}", full):
        ck.add("WARN", "W08", 1, "document class is not IEEEtran conference: confirm the venue")
    cited = [k.strip() for m in CITECMD.finditer("\n".join(strip_comment(l) for l in raw_lines))
             for k in m.group(1).split(",") if k.strip()]
    return list(dict.fromkeys(cited)), full


def check_float(f, ck):
    text = "\n".join(r for _, r in f["lines"])
    code = "\n".join(strip_comment(r) for _, r in f["lines"])
    cap, lab = code.find("\\caption"), code.find("\\label")
    if cap < 0 or lab < 0:
        ck.add("ERROR", "E08", f["start"], f"{f['env']} needs both \\caption and \\label")
    elif lab < cap:
        ck.add("ERROR", "E08", f["start"], f"{f['env']}: \\label must come after \\caption")
    is_table = f["env"].startswith("table")
    body = code.find("\\begin{tabular") if is_table else max(code.rfind("\\end{tikzpicture}"), code.rfind("\\includegraphics"))
    if cap >= 0 and body >= 0 and (is_table and cap > body or f["env"].startswith("figure") and cap < body):
        ck.add("WARN", "W01", f["start"], "IEEE places table captions above tables and figure captions below figures")
    tab = re.search(r"\\begin\{tabular\*?\}.*?\\end\{tabular\*?\}", code, re.S)
    cells = tab and re.sub(r"\\(cite|ref|label)[a-zA-Z]*\{[^}]*\}|\\begin\{tabular\*?\}(\{[^}]*\})+|"
                           r"\\cmidrule(\([^)]*\))?\{[^}]*\}", "", tab.group(0))
    has_data = "\\addplot" in code or bool(cells and re.search(r"\d", cells))
    tagged = re.search(r"%\s*(MEASURED|CONFIG|SOURCE):", text)
    marked = re.search(r"\\caption\{\s*\\tgtcap", code)
    if f["env"] != "algorithm" and has_data and not tagged and not marked:
        ck.add("ERROR", "E17", f["start"], f"{f['env']} holds numbers but is neither a marked target "
                                           "(caption starts with \\tgtcap) nor tagged % MEASURED:/CONFIG:/SOURCE:")
    if tab:
        check_metric_table(tab.group(0), code, f["start"], ck)


def check_metric_table(tab, float_code, start, ck):
    rows = [r for r in re.split(r"\\\\", re.sub(r"\\(toprule|midrule|bottomrule|hline)", "", tab)) if r.strip()]
    header, cols, pct_cols = None, {}, []
    for i, row in enumerate(rows):
        cells = [re.sub(r"\\[a-zA-Z]+|[{}]", " ", c).lower() for c in re.split(r"(?<!\\)&", row)]
        pct_cols = [j for j, c in enumerate(cells) if re.search(r"%|acc|prec|rec|\bf1\b|auc", c)]
        if pct_cols:
            header = i
            for j, c in enumerate(cells):
                key = "p" if "prec" in c else "r" if "rec" in c else "f" if re.search(r"\bf1\b|f-score|f-measure", c) else None
                if key:
                    cols.setdefault(key, j)
            break
    if header is None:
        return
    macro = "macro" in float_code.lower()
    for row in rows[header + 1:]:
        cells = re.split(r"(?<!\\)&", row)
        vals = {j: first_number(c) for j, c in enumerate(cells)}
        for j in pct_cols:
            v = vals.get(j, (None, 0))[0]
            if v is not None and v > 100:
                ck.add("ERROR", "E19", start, f"metric value {v} above 100")
        if not macro and {"p", "r", "f"} <= cols.keys():
            (p, dp), (r, dr), (f, df) = (vals.get(cols[k], (None, 0)) for k in "prf")
            if None in (p, r, f) or p + r == 0:
                continue
            expect = 2 * p * r / (p + r)
            if abs(expect - f) > 1.1 * 10 ** -max(dp, dr, df):
                ck.add("ERROR", "E18", start, f"F1 {f} but 2PR/(P+R) = {expect:.3f} for P={p}, R={r} "
                                              "(write 'macro-averaged' in the caption if it is)")


def check_bib(bib_path, cited, min_refs, ck):
    if len(cited) < min_refs:
        ck.add("ERROR", "E21", 0, f"{len(cited)} distinct references cited, minimum is {min_refs}")
    if not bib_path or not Path(bib_path).exists():
        ck.add("ERROR", "E20", 0, f"bibliography file not found: {bib_path}")
        return
    text = Path(bib_path).read_text(encoding="utf-8", errors="replace")
    entries = {m.group(1).lower(): m.group(2)
               for m in re.finditer(r"@\w+\s*\{\s*([^,\s]+)\s*,(.*?)(?=\n\s*@|\Z)", text, re.S)}
    for key in cited:
        body = entries.get(key.lower())
        if body is None:
            ck.add("ERROR", "E20", 0, f"cited key '{key}' has no bib entry")
        elif not re.search(r"^\s*(doi|url)\s*=", body, re.M | re.I):
            ck.add("ERROR", "E20", 0, f"bib entry '{key}' has neither doi nor url")


def check_log(log_path, ck):
    text = Path(log_path).read_text(encoding="utf-8", errors="replace")
    for m in re.finditer(r"^! .*", text, re.M):
        ck.add("ERROR", "E22", 0, "LaTeX error: " + m.group(0)[:90])
    for pat in (r"(Reference|Citation) `[^']*' on page \d+ undefined", r"Label `[^']*' multiply defined",
                r"There were undefined (references|citations)"):
        for m in re.finditer(pat, text):
            ck.add("ERROR", "E22", 0, m.group(0))
    for m in re.finditer(r"Overfull \\[hv]box \(([\d.]+)pt too (?:wide|high)\)[^\n]*?lines? (\d+)", text):
        if float(m.group(1)) > 5:
            ck.add("WARN", "W06", int(m.group(2)), f"overfull box {m.group(1)}pt")


def check_pdf(pdf_path, page_range, ck):
    tool = shutil.which("pdfinfo")
    if not tool:
        ck.add("ERROR", "E23", 0, "pdfinfo not found: page count NOT checked")
        return None
    m = re.search(r"Pages:\s+(\d+)", subprocess.run([tool, str(pdf_path)], capture_output=True, text=True).stdout)
    pages = int(m.group(1)) if m else None
    lo, hi = (int(x) for x in page_range.split("-"))
    if pages is None or not lo <= pages <= hi:
        ck.add("ERROR", "E23", 0, f"PDF has {pages} pages, required {page_range}")
    return pages


def target_register(tex_path, out_path):
    rows, section = [], ""
    for n, raw in enumerate(Path(tex_path).read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        code = strip_comment(raw)
        sec = re.search(r"\\(?:sub)?section\*?\{([^}]*)\}", code)
        section = sec.group(1) if sec else section
        if "\\newcommand" in code:
            continue
        if "\\tgtcap" in code:
            cap = re.sub(r"\s+", " ", code.strip())[:90].replace("|", "/")
            rows.append(f"| {n} | {section} | whole float | `{cap}` |")
        for m in re.finditer(r"\\tgt\{([^{}]*)\}", code):
            ctx = re.sub(r"\s+", " ", code[max(0, m.start() - 50):m.start()]).replace("|", "/")
            rows.append(f"| {n} | {section} | {m.group(1)} | ...{ctx} |")
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    Path(out_path).write_text(
        "# Implementation target register\n\nEvery value below is planned, not measured. Replace it with the measured "
        "value, remove its \\tgt wrapper, and tag its float `% MEASURED: <log or file>`.\n\n"
        "| Line | Section | Value | Context |\n|---|---|---|---|\n" + "\n".join(rows) + "\n", encoding="utf-8")


def run(args):
    ck = Checker()
    tex = Path(args.tex)
    cited, full = check_tex(tex, ck)
    bib = args.bib
    if not bib:
        m = re.search(r"\\bibliography\{([^}]*)\}", full)
        bib = str(tex.parent / (m.group(1).split(",")[0].strip() + ".bib")) if m else None
    check_bib(bib, cited, args.min_refs, ck)
    if args.log:
        check_log(args.log, ck)
    pages = check_pdf(args.pdf, args.pages, ck) if args.pdf else None
    ntgt = len(re.findall(r"\\tgt\{", full)) - len(re.findall(r"\\newcommand\{\\tgt\}", full))
    ncap = len(re.findall(r"\\caption\{\s*\\tgtcap", full))
    if args.targets_out:
        target_register(tex, args.targets_out)
    for level, code, line, msg in sorted(ck.items, key=lambda i: (i[0] != "ERROR", i[2], i[1])):
        print(f"{level:5} {code} line {line}: {msg}")
    ne = len(ck.errors())
    print(f"\nSummary: {ne} error(s), {len(ck.items) - ne} warning(s). Distinct citations: {len(cited)}. "
          f"Pages: {pages if pages is not None else 'not checked'}. "
          f"Implementation targets: {ntgt} value(s), {ncap} marked float(s).")
    if ntgt or ncap:
        print("Status: BLUEPRINT WITH IMPLEMENTATION TARGETS. Not submission-ready until every target is measured.")
    return ck


BAD = r"""\documentclass[conference]{IEEEtran}
\usepackage{amsmath}
\usepackage{amsmath}
\newcommand{\tgt}[1]{\textcolor{blue}{#1}}
\newcommand{\tgtcap}{[T]}
\newcommand{\tgtnotice}{notice}
\begin{document}
\section{Results}\label{sec:res}
Our method reaches 92.4% accuracy.
This line wraps the paragraph, which is TBD \cite{a}.
We note one thing; and another --- here. See Fig.~\ref{fig:nope}.
The gain is 3.15 points over \tgt{90.0}.\\ Forced break.
\begin{table}[t]
\centering
\label{tab:x}
\caption{Results.}
\begin{tabular}{lccc}
Method & Precision & Recall & F1 \\
A & 90.0 & 80.0 & 88.0 \\
\end{tabular}
\end{table}
\begin{figure}[t]
\centering
\begin{tikzpicture}\draw (0,0) -- (1,1);\end{tikzpicture}
\end{figure}
\begin{equation}
a = b
\end{equation}
\begin{itemize}
\item open item
\end{enumerate}
\end{document}
"""

GOOD = r"""\documentclass[conference]{IEEEtran}
\usepackage{xcolor}
\newcommand{\tgt}[1]{\textcolor{blue}{#1}}
\newcommand{\tgtcap}{\textcolor{blue}{[Implementation target]}~}
\newcommand{\tgtnotice}{Blue values are targets.}
\title{T\thanks{\tgtnotice}}
\begin{document}
\maketitle
\section{Results}\label{sec:res}
The method reaches an F1-score of \tgt{92.1}\% in Table~\ref{tab:m}, as defined in Equation~\eqref{eq:f1} and drawn in Fig.~\ref{fig:d}, following \cite{a}.

% MEASURED: author log run_07.csv
The measured latency is 41.2 ms on the reference host.
\begin{itemize}
\item First item on one line.
\item Second item on one line.
\end{itemize}
\begin{table}[t]
\centering
\caption{\tgtcap Results.}
\label{tab:m}
\begin{tabular}{lccc}
Method & Precision (\%) & Recall (\%) & F1 (\%) \\
A & \tgt{92.7} & \tgt{91.5} & \tgt{92.1} \\
\end{tabular}
\end{table}
\begin{equation}
F_1 = \frac{2PR}{P+R}
\label{eq:f1}
\end{equation}
\begin{figure}[t]
\centering
\begin{tikzpicture}\draw (0,0) -- (1,1);\end{tikzpicture}
\caption{A diagram.}
\label{fig:d}
\end{figure}
\bibliographystyle{IEEEtran}
\bibliography{refs}
\end{document}
"""


def selftest():
    with tempfile.TemporaryDirectory() as d:
        Path(d, "refs.bib").write_text("@article{a,\n  title={X},\n  doi={10.1/x}\n}\n", encoding="utf-8")
        ns = argparse.Namespace(bib=str(Path(d, "refs.bib")), log=None, pdf=None, pages="6-8", min_refs=1, targets_out=None)
        for name, src in (("bad.tex", BAD), ("good.tex", GOOD)):
            Path(d, name).write_text(src, encoding="utf-8")
        ns.tex = str(Path(d, "bad.tex"))
        bad = {c for _, c, _, _ in run(ns).items}
        want = {"E02", "E03", "E04", "E05", "E06", "E08", "E09", "E11", "E12", "E13", "E14", "E15", "E16", "E17", "E18"}
        assert want <= bad, f"bad sample missed {sorted(want - bad)}"
        ns.tex = str(Path(d, "good.tex"))
        good = run(ns)
        assert not good.errors(), f"good sample raised {good.errors()}"
        assert not [i for i in good.items if i[1] == "W03"], "measured line wrongly flagged"
    print("\nSELFTEST PASSED")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("tex", nargs="?")
    ap.add_argument("--bib")
    ap.add_argument("--log")
    ap.add_argument("--pdf")
    ap.add_argument("--pages", default="6-8")
    ap.add_argument("--min-refs", type=int, default=25)
    ap.add_argument("--targets-out")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        selftest()
        return 0
    if not args.tex:
        ap.error("main .tex file required")
    return 1 if run(args).errors() else 0


if __name__ == "__main__":
    sys.exit(main())
