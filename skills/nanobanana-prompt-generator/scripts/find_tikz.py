#!/usr/bin/env python3
"""List a paper's TikZ figures and flag results figures, which must never get a NanoBanana prompt.

Sources, in this order:
  1. every .tex / .tikz file in the TikZ folder (default figures/tikz/), named by its file stem;
  2. every tikzpicture inside a figure environment of the manuscript's .tex files outside figures/,
     named by its \\label (fig:arch -> arch) or <file>_tikz<N>.
Captions come from the figure environment that inputs the file (or holds the inline picture).

Status of each figure:
  EXCLUDE    plot code (pgfplots axis, \\addplot, plot coordinates/file/table, pie or bar charts, error bars).
             A results figure. Never write a prompt for it. Not overridable.
  REVIEW     a results hint in the caption, label or labels (accuracy, comparison, ablation, 94\\%, \\pm ...).
             Read the code and caption; exclude it if it shows any measured or computed result, or if in doubt.
  CANDIDATE  no results signal. Still read it before writing a prompt.

Usage:
    python find_tikz.py [project_root] [--tikz-dir figures/tikz]
Exit status: 0 figures listed, 2 no TikZ figure found.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

HARD = [
    (r"\\begin\{(?:axis|semilogxaxis|semilogyaxis|loglogaxis|polaraxis|ternaryaxis|smithchart|groupplot)\}",
     "pgfplots axis"),
    (r"\\(?:addplot3?|nextgroupplot|pgfplotstable\w*|datavisualization|pie|wheelchart)\b", "plot command"),
    (r"\\usepackage(?:\[[^\]]*\])?\{[^}]*\bpgfplots\b|\\usepgfplotslibrary", "pgfplots package"),
    (r"\bplot\s*(?:\[[^\]]*\]\s*)?(?:coordinates|file|table)\b", "plotted data"),
    (r"\b(?:ybar|xbar|error bars|colorbar)\b", "chart option"),
]
SOFT_WORDS = re.compile(
    r"\b(?:results?|accuracy|precision|recall|f1|auc|roc|confusion matrix|error rates?|rmse|mae|mse|"
    r"benchmark\w*|ablation\w*|performance|evaluation|comparisons?|compared|speed-?ups?|latency|throughput|"
    r"convergence|sensitivity|histograms?|scatter|heat ?maps?|box ?plots?|trade-?offs?|measured|"
    r"experiments?|experimental|outperform\w*|p-values?|significan\w*|loss curves?|learning curves?)\b",
    re.I)
SOFT_NUMBERS = [(r"\d\s*\\%", "percentage"), (r"\\pm\s*\d", "plus-minus value")]
SKIP_DIRS = {".git", "figures", "node_modules", "__pycache__"}


def strip_comments(tex: str) -> str:
    return re.sub(r"(?m)(?<!\\)%.*$", "", tex)


def braced(tex: str, start: int) -> str:
    """Contents of the {...} group that opens at or after `start`, with nested braces."""
    i = tex.find("{", start)
    if i < 0:
        return ""
    depth = 0
    for j in range(i, len(tex)):
        depth += {"{": 1, "}": -1}.get(tex[j], 0)
        if depth == 0:
            return tex[i + 1:j]
    return tex[i + 1:]


def caption_of(env: str) -> str:
    m = re.search(r"\\caption(?:\[[^\]]*\])?", env)
    return " ".join(braced(env, m.end()).split()) if m else ""


def classify(code: str, caption: str) -> tuple[str, list[str]]:
    hard = [why for pat, why in HARD if re.search(pat, code)]
    if hard:
        return "EXCLUDE", sorted(set(hard))
    soft = sorted({m.group(0).lower() for m in SOFT_WORDS.finditer(code + "\n" + caption)})
    soft += [why for pat, why in SOFT_NUMBERS if re.search(pat, code + caption)]
    return ("REVIEW", soft) if soft else ("CANDIDATE", [])


def scan(root: Path, tikz_dir: str = "figures/tikz") -> list[dict]:
    root = root.resolve()
    tdir = root / tikz_dir
    manuscript = [p for p in sorted(root.rglob("*.tex"))
                  if not SKIP_DIRS & set(p.relative_to(root).parts[:-1])]
    envs = []  # (file, figure environment text)
    for p in manuscript:
        text = strip_comments(p.read_text(encoding="utf-8", errors="replace"))
        envs += [(p, m.group(0)) for m in re.finditer(r"\\begin\{figure\*?\}.*?\\end\{figure\*?\}", text, re.S)]

    items, seen = [], set()
    files = sorted(f for f in tdir.rglob("*") if f.suffix in (".tex", ".tikz")) if tdir.is_dir() else []
    for f in files:
        code = strip_comments(f.read_text(encoding="utf-8", errors="replace"))
        ref = re.compile(r"[{/]" + re.escape(f.stem) + r"(?:\.tex|\.tikz)?\}")
        env = next((e for _, e in envs if ref.search(e)), "")
        items.append({"name": f.stem, "source": f.relative_to(root).as_posix(), "code": code,
                      "caption": caption_of(code) or caption_of(env), "wide": "figure*" in env})
        seen.add(f.stem)
    for p, env in envs:
        for n, m in enumerate(re.finditer(r"\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}", env, re.S), 1):
            label = re.search(r"\\label\{(?:fig:)?([^}]*)\}", env)
            name = re.sub(r"[^A-Za-z0-9_-]+", "_", label.group(1)) if label else f"{p.stem}_tikz{n}"
            if label and n > 1:
                name += f"_{n}"
            if name in seen:
                continue
            seen.add(name)
            items.append({"name": name, "source": p.relative_to(root).as_posix() + " (inline)",
                          "code": m.group(0), "caption": caption_of(env), "wide": "figure*" in env})
    for it in items:
        it["status"], it["signals"] = classify(it["code"], it["caption"])
    return items


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("root", nargs="?", default=".")
    ap.add_argument("--tikz-dir", default="figures/tikz")
    a = ap.parse_args(argv)
    items = scan(Path(a.root), a.tikz_dir)
    if not items:
        print(f"no TikZ figure found in {a.tikz_dir}/ or in figure environments of the manuscript")
        return 2
    for it in items:
        signals = ", ".join(it["signals"]) or "-"
        width = "wide" if it["wide"] else "column"
        print(f"{it['status']:<9}  {it['name']}  [{it['source']}, {width}]\n"
              f"           caption: {it['caption'][:120] or '-'}\n           signals: {signals}")
    counts = {s: sum(it["status"] == s for it in items) for s in ("CANDIDATE", "REVIEW", "EXCLUDE")}
    print(f"\n{len(items)} figures: {counts['CANDIDATE']} candidate, {counts['REVIEW']} to review, "
          f"{counts['EXCLUDE']} excluded as results figures")
    return 0


if __name__ == "__main__":
    sys.exit(main())
