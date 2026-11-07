#!/usr/bin/env python3
"""Mechanical gate for a Github/ folder built by the project-report-to-github skill.

Usage:
  python check_repo.py <Github dir> [--report PATH] [--forbid "Name A,Name B"] [--style]
  python check_repo.py --selftest

Checks (ERROR blocks the handoff, WARN must be fixed or explained in IMPLEMENTATION_STATUS.md):
  R01 required files          R07 placeholder bodies, syntax  R13 forbidden identity strings
  R02 status sections         R08 doc commands resolve        R14 imports vs declared deps
  R03 smoke report statuses   R09 markdown links resolve      R15 README sections, provenance, overclaims
  R04 caches, venvs, junk     R10 report ID traceability      R16 smoke config, CI credentials
  R05 secrets and .env        R11 machine-specific paths
  R06 large files             R12 optional house style (--style)
Exit status 1 when any ERROR is found. Standard library only, Python 3.10+.
"""
from __future__ import annotations

import argparse
import ast
import re
import shutil
import sys
import tempfile
from pathlib import Path
from urllib.parse import unquote

ERR, WARN = "ERROR", "WARN"
REQUIRED = [
    "README.md", "LICENSE", ".gitignore", "IMPLEMENTATION_STATUS.md", "SMOKE_TEST_REPORT.md",
    "docs/paper_implementation_mapping.md", "docs/assumptions.md", "docs/architecture.md",
    "docs/setup.md", "docs/training.md", "docs/evaluation.md", "docs/inference.md",
    "docs/reproducibility.md", "docs/troubleshooting.md",
]
STATUS_SECTIONS = ["fully implemented", "partially implemented", "not implemented", "technical debt",
                   "recommended next steps", "research reproducibility", "production readiness"]
JUNK_DIRS = {"__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", ".ipynb_checkpoints",
             ".tox", "node_modules", ".idea", ".hypothesis", "htmlcov", ".eggs"}
JUNK_FILES = re.compile(r"(\.py[co]|\.DS_Store|Thumbs\.db|\.coverage|\.tmp|\.swp|~)$")
TEXT_EXT = {".py", ".md", ".txt", ".yml", ".yaml", ".toml", ".cfg", ".ini", ".json", ".sh", ".ps1",
            ".example", ".ipynb", ".csv", ".tsv", ".cff", ".r", ".jl", ".js", ".ts", ".html"}
TEXT_NAMES = {"Dockerfile", "Makefile", "LICENSE", ".gitignore", ".dockerignore"}
SECRETS = [
    ("API key (sk-...)", r"\bsk-(?:proj-|ant-)?[A-Za-z0-9_-]{20,}"),
    ("AWS access key", r"\bAKIA[0-9A-Z]{16}\b"),
    ("GitHub token", r"\bgh[pousr]_[A-Za-z0-9]{36,}"),
    ("Hugging Face token", r"\bhf_[A-Za-z0-9]{30,}"),
    ("Google API key", r"\bAIza[0-9A-Za-z_-]{35}"),
    ("Slack token", r"\bxox[baprs]-[A-Za-z0-9-]{10,}"),
    ("private key block", r"-----BEGIN (?:[A-Z ]+ )?PRIVATE KEY-----"),
]
HARDCODED_CRED = re.compile(r"(?i)\b(api_?key|password|passwd|secret|token)\b\s*[:=]\s*[\"'][^\"'\s]{12,}[\"']")
ABS_PATH = re.compile(r"[A-Za-z]:\\{1,2}Users\\{1,2}([^\\/\s\"'`]+)|/home/([A-Za-z_][\w.-]*)/|/Users/([A-Za-z][\w.-]*)/")
PLACEHOLDER_USERS = {"user", "username", "you", "runner", "name", "me", "public", "default"}
IMPORT_TO_DIST = {
    "sklearn": "scikit-learn", "yaml": "pyyaml", "PIL": "pillow", "cv2": "opencv", "bs4": "beautifulsoup4",
    "dotenv": "python-dotenv", "skimage": "scikit-image", "attr": "attrs", "jwt": "pyjwt",
    "dateutil": "python-dateutil", "torch_geometric": "torch-geometric", "Crypto": "pycryptodome",
    "serial": "pyserial", "docx": "python-docx", "pptx": "python-pptx", "fitz": "pymupdf", "zmq": "pyzmq",
    "multipart": "python-multipart", "jose": "python-jose", "OpenSSL": "pyopenssl", "magic": "python-magic",
    "win32api": "pywin32", "google": "google", "pkg_resources": "setuptools",
}
OVERCLAIMS = re.compile(r"(?i)\b(reproduces|replicates) (all |the )?(paper'?s? |published )?(results|findings)\b"
                        r"|\bstate[- ]of[- ]the[- ]art\b|\bproduction[- ]ready\b|\bsecurity[- ]certified\b")
FENCE = re.compile(r"(?ms)^\s*(```|~~~).*?^\s*\1")


class Report:
    def __init__(self, root: Path):
        self.root = root
        self.items: list[tuple[str, str, str, str]] = []

    def add(self, level: str, code: str, path, msg: str, line: int | None = None) -> None:
        rel = path.relative_to(self.root).as_posix() if isinstance(path, Path) else str(path)
        self.items.append((level, code, rel + (f":{line}" if line else ""), msg))

    def errors(self) -> int:
        return sum(1 for i in self.items if i[0] == ERR)


def walk(root: Path):
    """Yield files under root, skipping .git, and junk dirs (reported separately)."""
    for p in sorted(root.rglob("*")):
        rel = p.relative_to(root).parts
        if ".git" in rel or any(part in JUNK_DIRS or part.endswith(".egg-info") for part in rel[:-1]):
            continue
        if p.is_file():
            yield p


def read(p: Path) -> str:
    if p.stat().st_size > 2_000_000:
        return ""
    return p.read_text(encoding="utf-8", errors="ignore")


def is_text(p: Path) -> bool:
    return p.suffix.lower() in TEXT_EXT or p.name in TEXT_NAMES


def is_env(p: Path) -> bool:
    return p.name == ".env" or (p.name.startswith(".env.") and p.name.split(".", 2)[2] not in
                                {"example", "sample", "template", "dist"})


def prose(text: str) -> list[tuple[int, str]]:
    """Markdown lines outside code fences, with inline code and HTML entities removed."""
    out, in_fence = [], False
    for n, line in enumerate(text.splitlines(), 1):
        if re.match(r"\s*(```|~~~)", line):
            in_fence = not in_fence
            continue
        if not in_fence:
            out.append((n, re.sub(r"&#?\w+;", "", re.sub(r"`[^`]*`", "", line))))
    return out


def headings(text: str) -> list[str]:
    return [line.lower() for _, line in prose(text) if line.lstrip().startswith("#")]


def check_files(root: Path, r: Report, docs: dict[str, str]) -> None:
    for rel in REQUIRED:
        if not (root / rel).is_file():
            r.add(ERR, "R01", rel, "required file is missing")
    if not (root / "tests").is_dir():
        r.add(ERR, "R01", "tests/", "no tests/ directory")
    status = docs.get("IMPLEMENTATION_STATUS.md")
    if status is not None:
        hs = headings(status)
        for sec in STATUS_SECTIONS:
            if not any(sec in h for h in hs):
                r.add(ERR, "R02", "IMPLEMENTATION_STATUS.md", f"no heading for section '{sec}'")
    smoke = docs.get("SMOKE_TEST_REPORT.md")
    if smoke is not None:
        check_smoke(smoke, r)


def check_smoke(text: str, r: Report) -> None:
    rows, col = 0, None
    for n, line in enumerate(text.splitlines(), 1):
        if not line.strip().startswith("|"):
            col = None
            continue
        cells = [c.strip().strip("*`").strip() for c in line.strip().strip("|").split("|")]
        if col is None:
            low = [c.lower() for c in cells]
            col = low.index("status") if "status" in low else None
            continue
        if set(line.replace("|", "").strip()) <= set("-: ") or col >= len(cells):
            continue
        val = re.sub(r"^[^A-Za-z]+", "", cells[col]).upper()
        rows += 1
        if not re.match(r"(PASS|FAIL|NOT RUN|BLOCKED)\b", val):
            r.add(ERR, "R03", "SMOKE_TEST_REPORT.md", f"status '{cells[col]}' is not PASS/FAIL/NOT RUN/BLOCKED", n)
    if rows == 0:
        r.add(ERR, "R03", "SMOKE_TEST_REPORT.md", "no table with a Status column")
    if not re.search(r"Python\s*3\.\d+", text):
        r.add(ERR, "R03", "SMOKE_TEST_REPORT.md", "Python version not recorded")


def check_tree(root: Path, r: Report, forbid: list[str]) -> None:
    for p in sorted(root.rglob("*")):
        rel = p.relative_to(root).parts
        if ".git" in rel:
            continue
        if p.is_dir() and (p.name in JUNK_DIRS or p.name.endswith(".egg-info")):
            if not any(part in JUNK_DIRS for part in rel[:-1]):
                r.add(ERR, "R04", p, "generated cache or build directory")
        elif p.is_dir() and (p / "pyvenv.cfg").exists():
            r.add(ERR, "R04", p, "virtual environment inside the repository")
    for p in walk(root):
        if any((parent / "pyvenv.cfg").exists() for parent in p.parents if root in parent.parents):
            continue
        if JUNK_FILES.search(p.name):
            r.add(ERR, "R04", p, "generated or editor artifact")
        elif p.suffix == ".log":
            r.add(WARN, "R04", p, "log file left in the repository")
        size = p.stat().st_size
        if size > 50_000_000:
            r.add(ERR, "R06", p, f"{size / 1e6:.0f} MB file (GitHub rejects files over 100 MB, keep artifacts out)")
        elif size > 5_000_000:
            r.add(WARN, "R06", p, f"{size / 1e6:.1f} MB file, confirm it belongs in the repository")
        if is_env(p):
            r.add(ERR, "R05", p, "environment file with possible secrets, ship only .env.example")
            continue  # never read it
        if not is_text(p):
            continue
        text = read(p)
        for n, line in enumerate(text.splitlines(), 1):
            for name, pat in SECRETS:
                if re.search(pat, line):
                    r.add(ERR, "R05", p, f"looks like a {name}", n)
            if HARDCODED_CRED.search(line) and "example" not in line.lower():
                r.add(WARN, "R05", p, "hard-coded credential-like assignment", n)
            for m in ABS_PATH.finditer(line):
                user = next(g for g in m.groups() if g)
                if user.lower() not in PLACEHOLDER_USERS and user[0] not in "<%${":
                    r.add(ERR, "R11", p, f"machine-specific path '{m.group(0)}'", n)
        low = text.lower()
        for term in forbid:
            if term.lower() in low:
                r.add(ERR, "R13", p, f"contains forbidden identity string '{term}'")


def placeholder_kind(fn: ast.FunctionDef | ast.AsyncFunctionDef) -> str | None:
    body = list(fn.body)
    first = body[0] if body else None
    if isinstance(first, ast.Expr) and isinstance(first.value, ast.Constant) and isinstance(first.value.value, str):
        body = body[1:]
    if not body:
        return "docstring only"
    kinds = set()
    for st in body:
        if isinstance(st, ast.Pass):
            kinds.add("pass")
        elif isinstance(st, ast.Expr) and isinstance(st.value, ast.Constant) and st.value.value is Ellipsis:
            kinds.add("...")
        elif isinstance(st, ast.Raise) and "NotImplementedError" in ast.dump(st):
            kinds.add("raise NotImplementedError")
        else:
            return None
    return " / ".join(sorted(kinds))


def check_python(root: Path, r: Report, status_text: str) -> set[str]:
    imports: set[str] = set()
    todo = 0
    for p in walk(root):
        if p.suffix != ".py":
            continue
        src = read(p)
        todo += len(re.findall(r"#\s*(TODO|FIXME|XXX)\b", src))
        try:
            tree = ast.parse(src)
        except SyntaxError as e:
            r.add(ERR, "R07", p, f"syntax error: {e.msg}", e.lineno)
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.update(a.name.split(".")[0] for a in node.names)
            elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
                imports.add(node.module.split(".")[0])
        if p.relative_to(root).parts[0] == "tests":
            continue
        check_placeholders(tree, p, r, status_text, abstract=False)
    if todo:
        r.add(WARN, "R07", ".", f"{todo} TODO/FIXME/XXX markers in Python code")
    return imports


def check_placeholders(node: ast.AST, p: Path, r: Report, status_text: str, abstract: bool, in_class=False):
    for child in ast.iter_child_nodes(node):
        if isinstance(child, ast.ClassDef):
            bases = {ast.unparse(b).split(".")[-1] for b in child.bases} | {
                ast.unparse(k.value).split(".")[-1] for k in child.keywords}
            check_placeholders(child, p, r, status_text, bool(bases & {"Protocol", "ABC", "ABCMeta"}), True)
        elif isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
            decos = {ast.unparse(d).split(".")[-1].split("(")[0] for d in child.decorator_list}
            kind = placeholder_kind(child)
            if kind and not abstract and not decos & {"abstractmethod", "overload", "abstractproperty"} \
                    and not re.search(rf"\b{re.escape(child.name)}\b", status_text):
                dunder = child.name.startswith("__") and child.name.endswith("__")
                level = WARN if dunder or (in_class and kind == "raise NotImplementedError") else ERR
                r.add(level, "R07", p, f"{child.name}() body is only {kind} and is not documented "
                                       f"in IMPLEMENTATION_STATUS.md", child.lineno)
            check_placeholders(child, p, r, status_text, False, False)


def check_deps(root: Path, r: Report, imports: set[str]) -> None:
    declared = set()
    for req in list(root.glob("requirements*.txt")) + list(root.glob("requirements/*.txt")):
        for line in read(req).splitlines():
            m = re.match(r"\s*([A-Za-z0-9][A-Za-z0-9_.-]*)", line.split("#")[0])
            if m and not line.lstrip().startswith("-"):
                declared.add(m.group(1))
    for cfg in ("pyproject.toml", "setup.cfg", "environment.yml"):
        if (root / cfg).is_file():
            # shortcut: any quoted or listed requirement-like token counts as declared, over-inclusive by design
            declared.update(re.findall(r"(?<=[\"'\s])([A-Za-z0-9][A-Za-z0-9_.-]*)\s*(?:\[[^\]]*\])?"
                                       r"\s*(?:[<>=!~;][^\"'\n]*)?(?=[\"'\n])", read(root / cfg)))
    norm = {re.sub(r"[-_.]+", "-", d.lower()) for d in declared}
    local = {p.stem for p in root.rglob("*.py")} | {p.name for p in root.rglob("*") if p.is_dir()}
    missing = []
    for mod in sorted(imports - set(sys.stdlib_module_names) - local - {"__future__"}):
        dist = re.sub(r"[-_.]+", "-", IMPORT_TO_DIST.get(mod, mod).lower())
        if not any(d == dist or d.startswith(dist + "-") or d.startswith(dist) for d in norm):
            missing.append(mod)
    if missing:
        r.add(WARN, "R14", ".", "imported but not declared in requirements/pyproject: " + ", ".join(missing))


def check_docs(root: Path, r: Report, docs: dict[str, str], style: bool) -> None:
    make = read(root / "Makefile") if (root / "Makefile").is_file() else None
    pkgs = {p.parent.name for p in root.rglob("__init__.py")}
    for md in sorted(root.rglob("*.md")):
        if any(part in JUNK_DIRS or part == ".git" for part in md.relative_to(root).parts):
            continue
        text = read(md)
        rel = md.relative_to(root).as_posix()
        if rel == "README.md" or rel.startswith("docs/"):
            for block in FENCE.finditer(text):
                check_commands(root, r, md, block.group(0), make, pkgs)
        for n, line in prose(text):
            for target in re.findall(r"\[[^\]]*\]\(\s*<?([^)\s>]+)>?(?:\s+\"[^\"]*\")?\s*\)", line):
                if re.match(r"(?i)(https?:|mailto:|#|data:|ftp:)", target):
                    continue
                dest = (md.parent / unquote(target.split("#")[0].split("?")[0])).resolve()
                if root.resolve() not in [dest, *dest.parents]:
                    r.add(ERR, "R09", md, f"link '{target}' points outside Github/ and breaks on GitHub", n)
                elif not dest.exists():
                    r.add(ERR, "R09", md, f"broken link '{target}'", n)
        if style and md.name not in {"CODE_OF_CONDUCT.md"}:
            dashes = sum(line.count("\u2014") for _, line in prose(text))
            semis = sum(line.count(";") for _, line in prose(text))
            if dashes or semis:
                r.add(ERR, "R12", md, f"{dashes} em dashes and {semis} semicolons in prose (house style forbids both)")
    readme = docs.get("README.md")
    if readme is None:
        return
    hs = " ".join(headings(readme))
    for keys in [("install",), ("quick start", "quickstart", "getting started"), ("smoke",), ("configur",),
                 ("data",), ("reproduc",), ("limitation",), ("citation", "cite"), ("license",)]:
        if not any(k in hs for k in keys):
            r.add(WARN, "R15", "README.md", f"no heading about '{keys[0]}'")
    if not re.search(r"(?i)reported in the paper|reports no (measured )?results", readme):
        r.add(WARN, "R15", "README.md", "no 'Reported in the paper' label separating paper numbers from local runs")
    for name, text in docs.items():
        for n, line in prose(text):
            m = OVERCLAIMS.search(line)
            if m and not re.search(r"(?i)\b(not|no|never|does not|cannot)\b", line):
                r.add(WARN, "R15", name, f"possible overclaim: '{m.group(0)}'", n)


def check_commands(root: Path, r: Report, md: Path, block: str, make: str | None, pkgs: set[str]) -> None:
    dirs = "scripts|configs|src|tests|docs|notebooks|deployment|examples|tools"
    for tok in re.findall(rf"(?<![\w/.$-])((?:{dirs})/[^\s\"'`|]+)", block):
        tok = tok.rstrip(".,:;)")
        if re.search(r"[*?{}<>$\[\]%]", tok):  # glob, shell variable or placeholder, not a literal path
            continue
        if not (root / tok).exists():
            r.add(ERR, "R08", md, f"command references '{tok}', which does not exist")
    for target in re.findall(r"(?m)^\s*(?:\$\s*)?make\s+([\w.-]+)", block):
        if make is None:
            r.add(ERR, "R08", md, f"'make {target}' but there is no Makefile")
        elif not re.search(rf"(?m)^{re.escape(target)}\s*:", make):
            r.add(ERR, "R08", md, f"'make {target}' but the Makefile has no such target")
    for mod in re.findall(r"python3?\s+-m\s+([\w.]+)", block):
        parts = mod.split(".")
        if parts[0] in pkgs and not any((base.joinpath(*parts).with_suffix(".py")).exists()
                                        or (base.joinpath(*parts) / "__init__.py").exists()
                                        or (base.joinpath(*parts) / "__main__.py").exists()
                                        for base in (root, root / "src")):
            r.add(ERR, "R08", md, f"'python -m {mod}' but that module does not exist")


def check_trace(root: Path, r: Report, docs: dict[str, str], report: Path | None) -> None:
    if report is None:
        cands = [p for p in root.resolve().parent.iterdir() if p.name.lower() == "project_report.md"]
        report = cands[0] if cands else None
    if report is None or not report.is_file():
        r.add(WARN, "R10", ".", "no PROJECT_REPORT.md found beside Github/, ID traceability not checked")
        return
    ids = set(re.findall(r"\b(?:REQ|EXP|METRIC|DEC|ASM)-[0-9A-Z]*\d+\b", read(report)))
    mapping = docs.get("docs/paper_implementation_mapping.md", "")
    elsewhere = " ".join(docs.values())
    must = sorted(i for i in ids if i.split("-")[0] in {"REQ", "EXP", "METRIC"} and not re.search(rf"\b{i}\b", mapping))
    should = sorted(i for i in ids if i.split("-")[0] in {"DEC", "ASM"} and not re.search(rf"\b{i}\b", elsewhere))
    if must:
        r.add(ERR, "R10", "docs/paper_implementation_mapping.md",
              f"{len(must)} REQ/EXP/METRIC IDs from the report are not mapped: " + ", ".join(must))
    if should:
        r.add(WARN, "R10", "docs/assumptions.md", f"{len(should)} DEC/ASM IDs from the report are never mentioned: "
              + ", ".join(should))


def check_misc(root: Path, r: Report) -> None:
    configs = root / "configs"
    if not configs.is_dir():
        r.add(WARN, "R16", "configs/", "no configs/ directory (research-critical settings should live in config files)")
    elif not any("smoke" in p.as_posix().lower() for p in configs.rglob("*")):
        r.add(WARN, "R16", "configs/", "no smoke configuration next to the full research configuration")
    flows = list((root / ".github" / "workflows").glob("*.y*ml"))
    if not flows:
        r.add(WARN, "R16", ".github/workflows/", "no CI workflow")
    for f in flows:
        if "secrets." in read(f):
            r.add(WARN, "R16", f, "CI references repository secrets, confirm the default jobs run without them")


def run(root: Path, report: Path | None, forbid: list[str], style: bool) -> Report:
    r = Report(root)
    docs = {p.relative_to(root).as_posix(): read(p) for p in walk(root) if p.suffix == ".md"}
    check_files(root, r, docs)
    check_tree(root, r, forbid)
    imports = check_python(root, r, docs.get("IMPLEMENTATION_STATUS.md", ""))
    check_deps(root, r, imports)
    check_docs(root, r, docs, style)
    check_trace(root, r, docs, report)
    check_misc(root, r)
    return r


# ----------------------------------------------------------------------------- selftest

CLEAN = {
    "README.md": "# Demo\n\n## Installation\n\n```bash\npip install -e .\npython scripts/train.py --config "
                 "configs/smoke.yaml\nmake test\npython -m demo.cli\nfor e in a b; do run configs/pilot_$e.yaml; done\n```\n\n## Quick start\n\nSee [setup](docs/setup.md)."
                 "\n\n## Smoke test\n\nRun it.\n\n## Configuration\n\nYAML.\n\n## Datasets\n\nNone.\n\n## Results\n\n"
                 "Reported in the paper: accuracy 0.91. Not reproduced locally.\n\n## Reproducibility\n\nSeeds.\n\n"
                 "## Limitations\n\nMany.\n\n## Citation\n\nTBD.\n\n## License\n\nMIT.\n",
    "LICENSE": "MIT License\n", ".gitignore": "__pycache__/\n.env\n", ".env.example": "OPENAI_API_KEY=\n",
    "IMPLEMENTATION_STATUS.md": "# Status\n## Fully Implemented\n## Partially Implemented\n## Not Implemented\n"
                                "## Technical Debt\n## Recommended Next Steps\n## Research Reproducibility\n"
                                "## Production Readiness Assessment\n",
    "SMOKE_TEST_REPORT.md": "# Smoke\n\nPython 3.10.11\n\n| Test | Status | Command |\n|---|---|---|\n"
                            "| unit | PASS | pytest |\n| api | NOT RUN | none |\n",
    "docs/paper_implementation_mapping.md": "# Map\n\n| ID | Module |\n|---|---|\n| REQ-001 | demo.model |\n"
                                            "| EXP-001 | scripts/train.py |\n",
    "docs/assumptions.md": "# Assumptions\n\nASM-001 kept.\n",
    **{f"docs/{n}.md": f"# {n}\n" for n in ["architecture", "setup", "training", "evaluation", "inference",
                                              "reproducibility", "troubleshooting"]},
    "Makefile": "test:\n\tpytest\n",
    "pyproject.toml": "[project]\nname = \"demo\"\ndependencies = [\"numpy>=1.26\", \"pyyaml\"]\n",
    "configs/smoke.yaml": "seed: 0\n", "configs/full.yaml": "seed: 0\n",
    ".github/workflows/ci.yml": "on: push\njobs: {}\n",
    "src/demo/__init__.py": "", "src/demo/cli.py": "import numpy\nimport yaml\n\n\ndef main() -> int:\n    return 0\n",
    "src/demo/base.py": "from abc import ABC, abstractmethod\n\n\nclass Base(ABC):\n    @abstractmethod\n"
                        "    def step(self):\n        ...\n",
    "scripts/train.py": "from demo.cli import main\n\nmain()\n",
    "tests/test_cli.py": "from demo.cli import main\n\n\ndef test_main():\n    assert main() == 0\n",
}
REPORT = "# Report\n\nREQ-001 x\nEXP-001 y\nASM-001 z\n"
FAULTS: dict[str, tuple[str, dict]] = {  # code -> (expected level, file overrides; None deletes)
    "R01": (ERR, {"docs/assumptions.md": None}),
    "R02": (ERR, {"IMPLEMENTATION_STATUS.md": "# Status\n## Fully Implemented\n"}),
    "R03": (ERR, {"SMOKE_TEST_REPORT.md": "Python 3.10\n\n| Test | Status |\n|---|---|\n| unit | OK |\n"}),
    "R04": (ERR, {"src/demo/__pycache__/cli.cpython-310.pyc": "x"}),
    "R05": (ERR, {".env": "KEY=1\n"}),
    "R06": (WARN, {"data/big.bin": "0" * 5_100_000}),
    "R07": (ERR, {"src/demo/train.py": "def train():\n    pass\n"}),
    "R08": (ERR, {"docs/training.md": "# T\n\n```bash\npython scripts/missing.py\nmake bench\n```\n"}),
    "R09": (ERR, {"docs/setup.md": "# S\n\nSee [paper](../../paper.tex) and [x](nothere.md).\n"}),
    "R10": (ERR, {"__report__": REPORT + "REQ-099 new\n"}),
    "R11": (ERR, {"docs/setup.md": "# S\n\nRun from C:\\Users\\alice\\proj.\n"}),
    "R12": (ERR, {"docs/architecture.md": "# A\n\nFast \u2014 and simple; really.\n"}),
    "R13": (ERR, {"CITATION.cff": "authors:\n  - name: Jane Roe\n"}),
    "R14": (WARN, {"src/demo/net.py": "import requests\n"}),
    "R15": (WARN, {"docs/evaluation.md": "# E\n\nThis code reproduces the paper's results.\n"}),
    "R16": (WARN, {"configs/smoke.yaml": None}),
}


def build(base: Path, overrides: dict) -> tuple[Path, Path]:
    root = base / "Github"
    files = {**CLEAN, **{k: v for k, v in overrides.items() if k != "__report__"}}
    for rel, content in files.items():
        if content is not None:
            (root / rel).parent.mkdir(parents=True, exist_ok=True)
            (root / rel).write_text(content, encoding="utf-8")
    report = base / "PROJECT_REPORT.md"
    report.write_text(overrides.get("__report__", REPORT), encoding="utf-8")
    return root, report


def selftest() -> int:
    failures = 0
    with tempfile.TemporaryDirectory() as tmp:
        root, report = build(Path(tmp) / "clean", {})
        clean = run(root, report, ["Jane Roe"], True)
        if clean.items:
            failures += 1
            print("FAIL clean repo produced findings:", *clean.items, sep="\n  ")
        for code, (level, overrides) in FAULTS.items():
            root, report = build(Path(tmp) / code, overrides)
            got = [i for i in run(root, report, ["Jane Roe"], True).items if i[1] == code and i[0] == level]
            print(("ok  " if got else "FAIL") + f" {code} {level} " + (got[0][3] if got else "not detected"))
            failures += not got
            shutil.rmtree(root.parent)
    print(f"selftest: {len(FAULTS) + 1 - failures}/{len(FAULTS) + 1} passed")
    return 1 if failures else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("repo", nargs="?", default="Github")
    ap.add_argument("--report", type=Path, help="PROJECT_REPORT.md (default: found beside the repo)")
    ap.add_argument("--forbid", default="", help="comma-separated strings that must not appear (anonymous review)")
    ap.add_argument("--style", action="store_true", help="opt in to the em-dash and semicolon prose check")
    ap.add_argument("--no-style", action="store_true", help="skip the prose style check (the default; kept for old commands)")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    root = Path(a.repo)
    if not root.is_dir():
        print(f"check_repo: {root} is not a directory")
        return 2
    rep = run(root, a.report, [t.strip() for t in a.forbid.split(",") if t.strip()], a.style and not a.no_style)
    for level, code, where, msg in sorted(rep.items, key=lambda i: (i[0] != ERR, i[1], i[2])):
        print(f"{level:5} {code} {where}: {msg}")
    print(f"check_repo: {rep.errors()} errors, {len(rep.items) - rep.errors()} warnings")
    return 1 if rep.errors() else 0


if __name__ == "__main__":
    sys.exit(main())
