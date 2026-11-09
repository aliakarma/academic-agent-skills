"""Tests for skills/nanobanana-prompt-generator/scripts/find_tikz.py: results figures must never be eligible."""
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "skills" / "nanobanana-prompt-generator" / "scripts" / "find_tikz.py"
spec = importlib.util.spec_from_file_location("find_tikz", SCRIPT)
ft = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ft)

ARCH = r"""\begin{tikzpicture}
\node[box] (enc) {Encoder}; \node[box, right=of enc] (dec) {Decoder}; % 94\% accuracy (comment, ignored)
\draw[->] (enc) -- (dec);
\end{tikzpicture}"""
PLOT = r"""\begin{tikzpicture}\begin{axis}[ybar]\addplot coordinates {(1,0.9) (2,0.8)};\end{axis}\end{tikzpicture}"""
LINE = r"""\begin{tikzpicture}\draw plot coordinates {(0,0) (1,2) (2,3)};\end{tikzpicture}"""
NUMBERS = r"""\begin{tikzpicture}\node {Classifier}; \node {Acc. 94.2\%};\end{tikzpicture}"""


def project(tmp_path: Path, tikz: dict[str, str], main: str = "") -> Path:
    (tmp_path / "figures" / "tikz").mkdir(parents=True)
    for name, code in tikz.items():
        (tmp_path / "figures" / "tikz" / name).write_text(code, encoding="utf-8")
    (tmp_path / "main.tex").write_text(main, encoding="utf-8")
    return tmp_path


def by_name(root: Path) -> dict[str, dict]:
    return {it["name"]: it for it in ft.scan(root)}


def test_plots_are_excluded_and_diagrams_are_candidates(tmp_path):
    items = by_name(project(tmp_path, {"arch.tex": ARCH, "bars.tex": PLOT, "curve.tikz": LINE}))
    assert items["arch"]["status"] == "CANDIDATE"          # the commented-out percentage is ignored
    assert items["bars"]["status"] == "EXCLUDE"
    assert items["curve"]["status"] == "EXCLUDE"


def test_result_values_or_results_caption_need_review(tmp_path):
    main = r"""\begin{figure*}\input{figures/tikz/arch}\caption{Accuracy comparison of the {two} models.}\end{figure*}"""
    items = by_name(project(tmp_path, {"arch.tex": ARCH, "clf.tex": NUMBERS}, main))
    assert items["arch"]["status"] == "REVIEW" and items["arch"]["wide"]
    assert items["arch"]["caption"] == "Accuracy comparison of the {two} models."
    assert set(items["arch"]["signals"]) == {"accuracy", "comparison"}
    assert items["clf"]["status"] == "REVIEW" and "percentage" in items["clf"]["signals"]


def test_inline_tikz_in_the_manuscript_is_found_and_named_by_label(tmp_path):
    main = ("\\begin{figure}" + ARCH + "\\caption{System overview.}\\label{fig:sys-overview}\\end{figure}\n"
            "\\begin{figure}" + PLOT + "\\caption{Scores.}\\end{figure}\n")
    items = by_name(project(tmp_path, {}, main))
    assert items["sys-overview"]["status"] == "CANDIDATE"
    assert items["sys-overview"]["source"] == "main.tex (inline)"
    assert items["main_tikz1"]["status"] == "EXCLUDE"


def test_cli_reports_no_figures(tmp_path, capsys):
    assert ft.main([str(tmp_path)]) == 2
    assert ft.main([str(project(tmp_path, {"arch.tex": ARCH}))]) == 0
    assert "1 candidate, 0 to review, 0 excluded" in capsys.readouterr().out
