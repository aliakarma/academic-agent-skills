#!/usr/bin/env python3
"""Check a generated explanation website for structure, links, offline use, and accessibility basics.

Usage:
  python validate_html.py PATH/index.html [MORE.html ...]
  python validate_html.py --self-test

ERROR items fail the check (exit code 1). WARN items need a decision but do not fail it.
Standard library only. Local .js files get a syntax check when Node.js is installed.
"""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
import tempfile
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
OPTIONAL_END = {"p", "li", "dt", "dd", "tr", "td", "th", "thead", "tbody", "tfoot", "option", "colgroup"}
ID_REFS = ("aria-labelledby", "aria-describedby", "aria-controls", "aria-owns", "for", "headers", "list")
PLACEHOLDER = re.compile(r"\{\{[^{}]*\}\}|lorem ipsum|\bTODO\b|\bTBD\b|\bFIXME\b|\[INSERT", re.I)
RAW_TEXT = {"code", "pre", "script", "style", "math", "annotation", "kbd", "samp", "textarea"}  # LaTeX and code can contain {{ }}
FETCHING = {("script", "src"), ("link", "href"), ("img", "src"), ("source", "src"), ("iframe", "src"),
            ("video", "src"), ("audio", "src"), ("embed", "src"), ("object", "data")}


class Checker(HTMLParser):
    def __init__(self, path: Path):
        super().__init__(convert_charrefs=True)
        self.path = path
        self.issues: list[tuple[str, int, str]] = []
        self.stack: list[tuple[str, int]] = []
        self.ids: dict[str, int] = {}
        self.refs: list[tuple[int, str, str]] = []
        self.files: list[tuple[int, str, str]] = []
        self.doctype = self.charset = self.viewport = self.main = False
        self.title, self.in_title, self.h1, self.last_h = "", False, 0, 0
        self.named: list[list] = []          # open buttons and links: [tag, line, accessible-name text]
        self.label_depth = 0
        self.label_fors: set[str] = set()
        self.inputs: list[tuple[int, str, str | None, bool]] = []
        self.figures: list[list] = []
        self.tables: list[list] = []
        self.svgs: list[list] = []
        self.raw_depth = 0

    def add(self, level, msg, line=None):
        self.issues.append((level, line or self.getpos()[0], msg))

    def handle_decl(self, decl):
        self.doctype |= decl.lower().startswith("doctype html")

    def handle_starttag(self, tag, attrs):
        self._open(tag, dict(attrs))
        if tag not in VOID:
            self.stack.append((tag, self.getpos()[0]))
        self.raw_depth += tag in RAW_TEXT

    def handle_startendtag(self, tag, attrs):
        self._open(tag, dict(attrs))

    def _open(self, tag, a):
        line = self.getpos()[0]
        for k, v in a.items():
            if v and PLACEHOLDER.search(v):
                self.add("ERROR", f"template placeholder left in {tag}[{k}]: {v[:60]}")
        if "id" in a:
            if a["id"] in self.ids:
                self.add("ERROR", f'duplicate id "{a["id"]}" (first on line {self.ids[a["id"]]})')
            self.ids.setdefault(a["id"], line)
        for k in ID_REFS:
            for ref in (a.get(k) or "").split():
                self.refs.append((line, f"{tag}[{k}]", ref))
        href = a.get("href") or ""
        if href.startswith("#") and len(href) > 1:
            self.refs.append((line, f"{tag}[href]", unquote(href[1:])))
        for t, k in FETCHING:
            if tag == t and a.get(k):
                self._resource(line, tag, a[k], a)
        if tag == "a" and href and not href.startswith(("#", "mailto:", "tel:", "javascript:")):
            u = urlparse(href)
            if not u.scheme and not u.netloc:
                self.files.append((line, "a[href]", href))
        if tag == "html" and not a.get("lang"):
            self.add("ERROR", "<html> has no lang attribute")
        if tag == "meta":
            self.charset |= "charset" in a
            self.viewport |= a.get("name") == "viewport"
        if tag == "title":
            self.in_title = True
        if tag == "main":
            self.main = True
        if re.fullmatch(r"h[1-6]", tag):
            level = int(tag[1])
            self.h1 += level == 1
            if self.last_h and level > self.last_h + 1:
                self.add("WARN", f"heading level jumps from h{self.last_h} to h{level}")
            self.last_h = level
        if tag == "img" and "alt" not in a:
            self.add("ERROR", f'<img src="{a.get("src", "")}"> has no alt attribute (use alt="" for decoration)')
        if tag == "svg":
            ok = a.get("aria-hidden") == "true" or a.get("aria-label") or a.get("aria-labelledby")
            self.svgs.append([line, bool(ok), a.get("role")])
        if tag == "title" and self.svgs and any(t == "svg" for t, _ in self.stack):
            self.svgs[-1][1] = True
        if tag in ("button", "a"):
            name = a.get("aria-label") or a.get("aria-labelledby") or a.get("title") or ""
            self.named.append([tag, line, name])
        if tag == "img" and self.named and a.get("alt"):
            self.named[-1][2] += a["alt"]
        if tag == "label":
            self.label_depth += 1
            if a.get("for"):
                self.label_fors.add(a["for"])
        if tag in ("input", "select", "textarea") and a.get("type") not in ("hidden", "submit", "button", "reset"):
            labelled = self.label_depth or a.get("aria-label") or a.get("aria-labelledby") or a.get("title")
            self.inputs.append((line, tag, a.get("id"), bool(labelled)))
        if tag == "figure":
            self.figures.append([line, False])
        if tag == "figcaption" and self.figures:
            self.figures[-1][1] = True
        if tag == "table":
            self.tables.append([line, False, False])
        if tag == "caption" and self.tables:
            self.tables[-1][1] = True
        if tag == "th" and self.tables:
            self.tables[-1][2] = True

    def _resource(self, line, tag, url, a):
        u = urlparse(url)
        if u.scheme in ("http", "https") or url.startswith("//"):
            self.add("WARN", f"{tag} loads {url} from the network (pages must work offline unless the user agreed)", line)
        elif u.scheme in ("", "file") and not url.startswith("data:"):
            if tag == "link" and "stylesheet" not in (a.get("rel") or "") and "icon" not in (a.get("rel") or ""):
                return
            self.files.append((line, f"{tag}", url))

    def handle_endtag(self, tag):
        if tag in RAW_TEXT and self.raw_depth:
            self.raw_depth -= 1
        if tag == "title":
            self.in_title = False
        if tag == "label":
            self.label_depth = max(0, self.label_depth - 1)
        if tag in ("button", "a") and self.named and self.named[-1][0] == tag:
            t, line, name = self.named.pop()
            if not name.strip():
                self.add("ERROR", f"<{t}> has no accessible name (no text, aria-label, or title)", line)
        if not any(t == tag for t, _ in self.stack):
            self.add("ERROR", f"closing </{tag}> has no matching open tag")
            return
        while self.stack:
            t, line = self.stack.pop()
            if t == tag:
                break
            if t not in OPTIONAL_END:
                self.add("ERROR", f"<{t}> opened on line {line} is not closed before </{tag}>")

    def handle_data(self, data):
        if self.in_title and not any(t == "svg" for t, _ in self.stack):
            self.title += data
        for item in self.named:
            item[2] += data
        if not self.raw_depth and PLACEHOLDER.search(data):
            self.add("ERROR", f"template placeholder left in text: {data.strip()[:60]}")

    def finish(self):
        for t, line in self.stack:
            if t not in OPTIONAL_END | {"html", "body", "head"}:
                self.add("ERROR", f"<{t}> opened on line {line} is never closed", line)
        if not self.doctype:
            self.add("ERROR", "missing <!doctype html>", 1)
        if not self.charset:
            self.add("ERROR", "missing <meta charset>", 1)
        if not self.viewport:
            self.add("ERROR", 'missing <meta name="viewport"> (needed for phone layouts)', 1)
        if not self.title.strip():
            self.add("ERROR", "missing or empty <title>", 1)
        if self.h1 != 1:
            self.add("ERROR", f"page has {self.h1} <h1> elements (use exactly one)", 1)
        if not self.main:
            self.add("ERROR", "missing <main> landmark", 1)
        for line, where, ref in self.refs:
            if ref not in self.ids:
                self.add("ERROR", f'{where} points to id "{ref}", which does not exist', line)
        for line, tag, id_, labelled in self.inputs:
            if not labelled and id_ not in self.label_fors:
                self.add("ERROR", f"<{tag}> has no label", line)
        for line, ok, role in self.svgs:
            if not ok:
                self.add("ERROR", "<svg> needs <title> or aria-label (or aria-hidden=\"true\" if decorative)", line)
        for line, has_caption in self.figures:
            if not has_caption:
                self.add("WARN", "<figure> has no <figcaption>", line)
        for line, has_caption, has_th in self.tables:
            if not has_th:
                self.add("WARN", "<table> has no <th> header cells", line)
            if not has_caption:
                self.add("WARN", "<table> has no <caption>", line)
        base = self.path.parent
        for line, where, url in self.files:
            target = base / unquote(urlparse(url).path)
            if not target.exists():
                self.add("ERROR", f'{where} file not found: "{url}"', line)
            elif target.suffix == ".js":
                self._js_syntax(target, line)

    def _js_syntax(self, target, line):
        node = shutil.which("node")
        if not node:
            self.add("WARN", f"Node.js not found, JavaScript syntax of {target.name} not checked", line)
            return
        r = subprocess.run([node, "--check", str(target)], capture_output=True, text=True)
        if r.returncode:
            self.add("ERROR", f"JavaScript syntax error in {target.name}: {r.stderr.strip().splitlines()[-1]}", line)


def check(path):
    path = Path(path)
    c = Checker(path)
    c.feed(path.read_text(encoding="utf-8"))
    c.close()
    c.finish()
    return sorted(set(c.issues), key=lambda i: (i[1], i[0]))


def main(paths):
    failed = False
    for p in paths:
        issues = check(p)
        errors = [i for i in issues if i[0] == "ERROR"]
        print(f"{p}: {len(errors)} errors, {len(issues) - len(errors)} warnings")
        for level, line, msg in issues:
            print(f"  {level} line {line}: {msg}")
        failed |= bool(errors)
    return 1 if failed else 0


def self_test():
    good = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>T</title>
<link rel="stylesheet" href="styles.css"></head><body><a href="#main">Go to the content</a>
<main id="main"><h1>Title</h1><h2 id="s1">Part</h2><p>Text.</p>
<figure><svg role="img" aria-labelledby="t1"><title id="t1">Flow</title></svg><figcaption>Flow</figcaption></figure>
<label for="f">Filter</label><input id="f" type="search"><button type="button">Copy</button>
<table><caption>Values</caption><tr><th>A</th></tr><tr><td>1</td></tr></table>
<math><semantics><mi>x</mi><annotation encoding="application/x-tex">\\mathcal{S}_{\\mathrm{safe}}</annotation></semantics></math>
<pre><code>&lt;p&gt;{{ message }}&lt;/p&gt; // TODO in code is not a slot</code></pre>
<a href="https://doi.org/10.1000/1">Source</a></main><script src="app.js"></script></body></html>"""
    bad = """<html><head><title></title><script src="https://cdn.example.com/x.js"></script></head>
<body><h1>One</h1><h1>Two</h1><h4 id="d">Jump</h4><p id="d">{{OVERVIEW}}</p>
<a href="#nowhere">Link</a><img src="missing.png"><button></button><input type="text">
<svg><rect/></svg><div><span></div></body></html>"""
    with tempfile.TemporaryDirectory() as tmp:
        t = Path(tmp)
        (t / "styles.css").write_text("body{}", encoding="utf-8")
        (t / "app.js").write_text("document.title = 'ok';", encoding="utf-8")
        (t / "good.html").write_text(good, encoding="utf-8")
        (t / "bad.html").write_text(bad, encoding="utf-8")
        g = [i for i in check(t / "good.html") if i[0] == "ERROR"]
        assert not g, g
        msgs = " | ".join(m for _, _, m in check(t / "bad.html"))
        for expected in ("no lang", "doctype", "viewport", "empty <title>", "2 <h1>", "duplicate id", "placeholder",
                         '"nowhere"', "no alt", "no accessible name", "no label", "<svg> needs", "not closed",
                         "from the network", "<main>", "jumps from h1 to h4"):
            assert expected in msgs, f"missing check: {expected}\n{msgs}"
    print("self-test passed: a clean page has 0 errors and a broken page triggers all 16 checks")
    return 0


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if sys.argv[1:] == ["--self-test"]:
        sys.exit(self_test())
    if not sys.argv[1:]:
        sys.exit(__doc__)
    sys.exit(main(sys.argv[1:]))
