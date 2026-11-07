r"""Render deck equations to transparent high-dpi PNGs with pdflatex.

Input is a plain .tex file of named blocks, each body pasted verbatim from the
paper (math mode is added for you, so do not wrap bodies in $...$):

    %% loss
    \mathcal{L}(\theta)=\sum_i \ell_i(\theta)
    %% update
    \begin{aligned} a &= b \\ c &= d \end{aligned}

Output: <outdir>/<name>.png plus <outdir>/manifest.json with pixel sizes, so
the deck builder can place each image at true typographic scale.

    python render_equations.py equations.tex assets/eq [--preamble macros.tex]
        [--ink 1B2430] [--dpi 600] [--size 12pt]

--preamble takes the paper's \newcommand / \DeclareMathOperator lines so
bodies copied verbatim compile unchanged. Use one --ink per run: render a
second set with a light ink into another folder for dark slides.
"""
import argparse
import json
import shutil
import subprocess
import tempfile
from pathlib import Path

from PIL import Image

TEMPLATE = r"""\documentclass[%(size)s,border=1.5pt]{standalone}
\usepackage{amsmath,amssymb,amsfonts,bm}
\usepackage{xcolor}
\definecolor{ink}{HTML}{%(ink)s}
%(preamble)s
\begin{document}
\color{ink}$\displaystyle %(body)s$
\end{document}
"""


def render(name, body, work, out, args, preamble):
    tex = work / f"{name}.tex"
    tex.write_text(TEMPLATE % {"size": args.size, "ink": args.ink, "preamble": preamble, "body": body},
                   encoding="utf-8")
    r = subprocess.run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", tex.name],
                       cwd=work, capture_output=True, text=True, errors="replace")
    if r.returncode != 0:
        err = [l for l in r.stdout.splitlines() if l.startswith("!")]
        raise SystemExit(f"{name}: pdflatex failed: {err[:3] or r.stdout[-400:]}")
    subprocess.run(["pdftocairo", "-png", "-transp", "-r", str(args.dpi), "-singlefile",
                    f"{name}.pdf", str(out / name)], cwd=work, check=True)
    with Image.open(out / f"{name}.png") as im:
        return {"px_w": im.width, "px_h": im.height, "dpi": args.dpi, "latex": body}


def parse(text):
    """Split '%% name' blocks into {name: body}. Lines before the first header are ignored."""
    eqs, name = {}, None
    for line in text.splitlines():
        if line.startswith("%% "):
            name = line[3:].strip()
            if name in eqs:
                raise SystemExit(f"duplicate equation name '{name}'")
            eqs[name] = []
        elif name is not None:
            eqs[name].append(line)
    eqs = {k: "\n".join(v).strip() for k, v in eqs.items()}
    empty = [k for k, v in eqs.items() if not v]
    if empty or not eqs:
        raise SystemExit(f"no equations found or empty blocks: {empty}")
    return eqs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("equations", type=Path)
    ap.add_argument("outdir", type=Path)
    ap.add_argument("--preamble", type=Path)
    ap.add_argument("--ink", default="1B2430", help="six hex digits, no #")
    ap.add_argument("--dpi", type=int, default=600)
    ap.add_argument("--size", default="12pt")
    args = ap.parse_args()

    eqs = parse(args.equations.read_text(encoding="utf-8"))
    preamble = args.preamble.read_text(encoding="utf-8") if args.preamble else ""
    args.outdir.mkdir(parents=True, exist_ok=True)
    work = Path(tempfile.mkdtemp(prefix="eq_"))
    manifest = {}
    try:
        for name, body in eqs.items():
            manifest[name] = render(name, body, work, args.outdir.resolve(), args, preamble)
            print(f"{name}: {manifest[name]['px_w']}x{manifest[name]['px_h']}")
    finally:
        shutil.rmtree(work, ignore_errors=True)
    (args.outdir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
