#!/usr/bin/env python3
"""Compile a journal cover letter and check it before submission.

Usage:
  python check_letter.py LETTER.tex [--require TEXT]... [--png OUT.png]
                         [--paper a4|letter] [--keep-build]
  python check_letter.py --selftest

Compiles with latexmk (pdflatex, or xelatex/lualatex when the source asks for
it), then checks the PDF: exactly one page, paper size, no [[...]] or TODO
placeholders, no missing glyphs, no overfull lines, no em dashes or semicolons,
every --require string present. Reports body word count and page fill, renders
a PNG for visual inspection, and deletes build files after a pass.

Exit codes: 0 all checks pass (WARN allowed), 1 a check failed, 2 no TeX tools.
"""
import argparse
import re
import shutil
import subprocess
import sys
import tempfile
import unicodedata
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PAPER = {"a4": (595.28, 841.89), "letter": (612.0, 792.0)}
PLACEHOLDER = re.compile(r"\[\[|\]\]|\bTODO\b|\bTBD\b|\bXXX\b|lorem ipsum|\?\?", re.I)
CLOSING = re.compile(r"^\s*(Sincerely|Yours sincerely|Yours faithfully|Yours truly|Kind regards|"
                     r"Best regards|Respectfully|With kind regards|Regards)\s*[,.]?\s*$", re.I | re.M)
BUILD_EXTS = (".aux", ".log", ".out", ".fls", ".fdb_latexmk", ".synctex.gz", ".xdv")
WORDS_ADVISORY = (250, 350)


def tool(name):
    """Prefer the copy next to pdflatex: Git Bash ships an xpdf pdftotext 4.00 without -bbox."""
    if shutil.which("pdflatex"):
        for cand in (Path(shutil.which("pdflatex")).parent / n for n in (name + ".exe", name)):
            if cand.exists():
                return str(cand)
    return shutil.which(name)


def run(cmd, cwd=None):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True,
                          encoding="utf-8", errors="replace", timeout=300)


def engine_for(src):
    m = re.search(r"%\s*!TEX\s+(?:TS-)?program\s*=\s*(\w+)", src, re.I)
    if m and m.group(1).lower() in ("xelatex", "lualatex"):
        return m.group(1).lower()
    return "xelatex" if re.search(r"\\usepackage(\[[^\]]*\])?\{fontspec\}", src) else "pdflatex"


def compile_tex(tex):
    """Return (ok, label). Runs in the letter's folder so spaces in parent paths never reach TeX."""
    eng = engine_for(tex.read_text(encoding="utf-8", errors="replace"))
    flags = ["-interaction=nonstopmode", "-halt-on-error", "-file-line-error"]
    if tool("latexmk"):  # -norc: never execute a project latexmkrc
        r = run([tool("latexmk"), {"pdflatex": "-pdf"}.get(eng, "-" + eng), "-norc", *flags, tex.name], tex.parent)
        return r.returncode == 0, f"latexmk ({eng})"
    if not tool(eng):
        return None, eng
    for _ in range(2):
        r = run([tool(eng), *flags, tex.name], tex.parent)
        if r.returncode:
            return False, eng
    return True, eng


def norm(s):
    s = unicodedata.normalize("NFKC", s)  # splits fi/fl ligatures
    return s.translate(str.maketrans({"\u2018": "'", "\u2019": "'", "\u201c": '"', "\u201d": '"',
                                      "\u00a0": " ", "\u2013": "-", "\u2010": "-", "\u2011": "-"}))


def key(s):
    # Drop whitespace and hyphens so line breaks and TeX hyphenation cannot hide a match.
    return re.sub(r"[\s\-]", "", norm(s).replace("``", '"').replace("''", '"')).lower()


def check(tex, required=(), png=None, paper="a4", keep_build=False):
    """Return (exit_code, results) where results is a list of (status, name, detail)."""
    tex = Path(tex).resolve()
    res = []
    add = lambda status, name, detail="": res.append((status, name, detail))
    if not tex.exists():
        add("FAIL", "source", f"{tex} not found")
        return 1, res

    ok, label = compile_tex(tex)
    pdf, log_path = tex.with_suffix(".pdf"), tex.with_suffix(".log")
    if ok is None:
        add("BLOCKED", "compile", "no LaTeX compiler found, deliver the .tex and say the PDF is blocked")
        return 2, res
    log = log_path.read_text(encoding="utf-8", errors="replace") if log_path.exists() else ""
    if not ok or not pdf.exists():
        err = re.findall(r"^(?:.*:\d+: .*|! .*)$", log, re.M)[:3]
        add("FAIL", "compile", f"{label} failed: {' | '.join(err) or 'see ' + log_path.name}")
        return 1, res
    add("PASS", "compile", label)

    # Log checks
    over = [float(x) for x in re.findall(r"Overfull \\hbox \(([\d.]+)pt too wide\)", log)]
    if any(x > 1.0 for x in over):
        add("FAIL", "overfull lines", f"{len(over)} line(s) run into the margin, worst {max(over):.1f}pt")
    elif over:
        add("WARN", "overfull lines", f"{len(over)} line(s) under 1pt too wide")
    else:
        add("PASS", "overfull lines", "none")
    missing = re.findall(r"Missing character: There is no (.+?) in font", log)
    add("FAIL" if missing else "PASS", "glyphs", f"missing: {sorted(set(missing))}" if missing else "all present")
    undef = re.findall(r"LaTeX Warning: (?:Reference|Citation) `([^']+)' .*undefined", log)
    if undef:
        add("FAIL", "references", f"undefined: {sorted(set(undef))}")
    fonts = sorted(set(re.findall(r"LaTeX Font Warning: (.+)", log)))
    if fonts:
        add("WARN", "fonts", " | ".join(fonts)[:200])

    # PDF checks
    info = run([tool("pdfinfo"), str(pdf)]).stdout if tool("pdfinfo") else ""
    m = re.search(r"^Pages:\s+(\d+)", info, re.M)
    pages = int(m.group(1)) if m else None
    if pages is None:
        add("FAIL", "pages", "pdfinfo could not read the PDF (corrupt or tool missing)")
    else:
        add("PASS" if pages == 1 else "FAIL", "pages", f"{pages} (must be exactly 1)")
    m = re.search(r"^Page size:\s+([\d.]+) x ([\d.]+) pts", info, re.M)
    if m:
        w, h = float(m.group(1)), float(m.group(2))
        ew, eh = PAPER[paper]
        same = abs(w - ew) < 2 and abs(h - eh) < 2
        add("PASS" if same else "FAIL", "paper", f"{w:.0f} x {h:.0f} pt, expected {paper}")

    if not tool("pdftotext"):
        add("FAIL", "text", "pdftotext not found, text checks impossible")
        return 1, res
    raw = run([tool("pdftotext"), "-enc", "UTF-8", str(pdf), "-"]).stdout
    text = norm(raw)
    if len(text.split()) < 50:
        add("FAIL", "text", f"only {len(text.split())} words extracted, PDF text may be missing or garbled")

    ph = sorted({mm.group(0) for mm in PLACEHOLDER.finditer(text)})
    add("FAIL" if ph else "PASS", "placeholders", f"found {ph}" if ph else "none")

    missing_req = [r for r in required if key(r) not in key(text)]
    if required:
        add("FAIL" if missing_req else "PASS", "required text",
            f"missing: {missing_req}" if missing_req else f"{len(required)} string(s) present")

    # Style: required strings (a title may legitimately contain a semicolon) are exempt.
    style_text = raw
    for r in required:
        style_text = style_text.replace(r, " ")
    em = [ln.strip() for ln in style_text.splitlines() if "\u2014" in ln or "\u2015" in ln]
    add("FAIL" if em else "PASS", "em dashes", f"{len(em)} line(s): {em[:2]}" if em else "none")
    semi = [ln.strip() for ln in style_text.splitlines() if ";" in ln]
    add("FAIL" if semi else "PASS", "semicolons", f"{len(semi)} line(s): {semi[:2]}" if semi else "none")

    # Body word count: from the salutation to the closing line.
    start = re.search(r"^\s*Dear\b.*$", text, re.M)
    end = CLOSING.search(text, start.end()) if start else None
    if start and end:
        n = len(re.findall(r"[A-Za-z0-9][\w'-]*", text[start.end():end.start()]))
        lo, hi = WORDS_ADVISORY
        add("PASS" if lo <= n <= hi else "WARN", "body words", f"{n} (advisory {lo} to {hi}, one page wins)")
    else:
        add("WARN", "body words", "salutation ('Dear ...') or closing ('Sincerely,') not found")

    # Page fill: lowest text baseline as a share of page height.
    bbox = run([tool("pdftotext"), "-bbox", "-f", "1", "-l", "1", str(pdf), "-"]).stdout
    hm = re.search(r'<page width="[\d.]+" height="([\d.]+)"', bbox)
    ys = [float(y) for y in re.findall(r'yMax="([\d.]+)"', bbox)]
    if hm and ys:
        fill = max(ys) / float(hm.group(1))
        add("WARN" if fill < 0.55 else "INFO", "page fill",
            f"text ends at {fill:.0%} of page height" + (", page looks sparse" if fill < 0.55 else ""))

    if png:
        png = Path(png).resolve()
        png.parent.mkdir(parents=True, exist_ok=True)
        if tool("pdftoppm"):
            run([tool("pdftoppm"), "-png", "-r", "110", "-singlefile", str(pdf), str(png.with_suffix(""))])
        add("INFO" if png.exists() else "WARN", "render", str(png) if png.exists() else "PNG not produced")

    code = 1 if any(s == "FAIL" for s, _, _ in res) else 0
    if code == 0 and not keep_build:
        for ext in BUILD_EXTS:
            tex.with_suffix(ext).unlink(missing_ok=True)
    return code, res


def report(code, res):
    for status, name, detail in res:
        print(f"[{status}] {name}: {detail}")
    warns = sum(s == "WARN" for s, _, _ in res)
    print(f"RESULT: {['PASS', 'FAIL', 'BLOCKED'][code]}" + (f" ({warns} warning(s))" if warns else ""))


# ---------------------------------------------------------------- self-test
SYNTH = {  # synthetic values, used only by the self-test
    "LetterDate": "November 14, 2026", "RecipientName": "Editorial Office", "JournalName": "Journal of Test Studies",
    "Publisher": "Example Press", "Salutation": "Dear Editor", "ArticleType": "Research Article",
    "ManuscriptTitle": "Synthetic Evidence for a Test Manuscript", "AuthorName": "Test Author",
    "AuthorDept": "Department of Testing", "AuthorInstitution": "Example University, Testville, Nowhere",
    "AuthorEmail": "author@example.com",
}
PARA = ("This synthetic paragraph exists only to exercise the checker. It reports that the test study compared "
        "two designs across forty trials and found a difference in completion time that the manuscript reports "
        "with confidence intervals. ")


def fill(template, body):
    out = template
    for k, v in SYNTH.items():
        out = re.sub(r"(\\newcommand\{\\%s\})\{\[\[[^\]]*\]\]\}" % k, lambda m: m.group(1) + "{" + v + "}", out)
    return re.sub(r"(% ---- BODY START ----\n).*?(% ---- BODY END ----)",
                  lambda m: m.group(1) + body + "\n" + m.group(2), out, flags=re.S)


def selftest():
    tpl = Path(__file__).resolve().parent.parent / "templates" / "cover-letter-template.tex"
    src = tpl.read_text(encoding="utf-8")
    good = "\n\n".join([PARA * 2] * 3)
    cases = [  # (name, body or None for the raw template, expected exit code, check that must FAIL)
        ("raw template is rejected", None, 1, "placeholders"),
        ("filled letter passes", good, 0, None),
        ("two-page letter is rejected", "\n\n".join([PARA * 3] * 9), 1, "pages"),
        ("em dash is rejected", good + "\n\nA clause\\textemdash another clause.", 1, "em dashes"),
        ("semicolon is rejected", good + "\n\nOne clause; another clause.", 1, "semicolons"),
        ("missing title is rejected", good, 1, "required text"),
    ]
    failures = 0
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as d:
        for i, (name, body, want, must_fail) in enumerate(cases):
            tex = Path(d) / f"case{i}.tex"
            tex.write_text(src if body is None else fill(src, body), encoding="utf-8")
            req = [SYNTH["ManuscriptTitle"], SYNTH["JournalName"], SYNTH["AuthorName"], SYNTH["AuthorEmail"]]
            if must_fail == "required text":
                req.append("A Title That Is Not In The Letter")
            code, res = check(tex, req if body is not None else [], png=Path(d) / f"case{i}.png")
            if code == 2:
                print("BLOCKED: no LaTeX compiler, self-test cannot run")
                return 2
            failed = {n for s, n, _ in res if s == "FAIL"}
            ok = code == want and (must_fail is None or must_fail in failed)
            if code == 0 and any(tex.with_suffix(e).exists() for e in (".aux", ".log")):
                ok = False  # build files must be cleaned after a pass
            failures += not ok
            print(f"{'ok  ' if ok else 'FAIL'} {name}: exit {code}, failed checks {sorted(failed) or 'none'}")
    print("SELFTEST:", "PASS" if not failures else f"{failures} case(s) failed")
    return 1 if failures else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("tex", nargs="?")
    ap.add_argument("--require", action="append", default=[], help="text that must appear in the PDF")
    ap.add_argument("--png", help="write a page render here for visual inspection")
    ap.add_argument("--paper", choices=sorted(PAPER), default="a4")
    ap.add_argument("--keep-build", action="store_true", help="keep .aux/.log after a pass")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not a.tex:
        ap.error("LETTER.tex is required")
    code, res = check(a.tex, a.require, a.png, a.paper, a.keep_build)
    report(code, res)
    return code


if __name__ == "__main__":
    sys.exit(main())
