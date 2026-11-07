#!/usr/bin/env python3
"""Compare an original and a revised text for changes that can alter meaning.

Usage: python fidelity_check.py ORIGINAL REVISED

Works on plain text, Markdown, and LaTeX prose.

Hard checks (exit code 1 if any differ):
  numbers      every numeric token, with sign and percent, compared as a multiset
  math         $...$, $$...$$, \\(...\\), \\[...\\], and equation-like environments
  citations    LaTeX \\cite/\\ref/\\label commands, bracketed numeric citations,
               and parenthetical author-year citations

Review items (reported, never fail the run):
  negation, hedge, causal, and strength/universal word counts. A change here is
  acceptable only when it is a reported substantive correction, such as
  withdrawing "proves" from an unsupported claim.

Exit code 0 when all hard checks pass.
"""
import re
import sys
from collections import Counter
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

MATH = re.compile(
    r"\$\$.+?\$\$|\$[^$\n]+\$|\\\(.+?\\\)|\\\[.+?\\\]"
    r"|\\begin\{(equation|align|gather|multline|eqnarray|displaymath)\*?\}.+?\\end\{\1\*?\}",
    re.S,
)
LATEX_CITE = re.compile(
    r"\\(?:cite[a-zA-Z]*|ref|eqref|autoref|cref|Cref|pageref|label)\*?(?:\[[^\]]*\])*\{[^}]*\}"
)
BRACKET_CITE = re.compile(r"\[\d+(?:\s*[-\u2013,]\s*\d+)*\]")
AUTHOR_YEAR = re.compile(
    r"\((?:[A-Z][\w'\-]+(?: et al\.)?(?: (?:and|&) [A-Z][\w'\-]+)?,? \d{4}[a-z]?(?:; )?)+\)"
)
NUMBER = re.compile(r"[\u2212\-]?\d+(?:[.,]\d+)*%?")

WORD_CLASSES = {
    "negation": r"\b(?:not|no|never|none|neither|nor|without|cannot)\b|n't\b",
    "hedge": r"\b(?:may|might|could|can|would|possibly|perhaps|potentially|likely|unlikely"
             r"|suggests?|suggested|appears?|appeared|seems?|seemed|approximately|roughly)\b",
    "causal": r"\b(?:caus(?:e|es|ed|ing)|because|therefore|thus|hence|consequently|due to"
              r"|leads? to|led to|results? in|resulted in|drives?|owing to)\b",
    "strength": r"\b(?:all|every|always|only|ensures?|ensured|guarantees?|guaranteed"
                r"|proves?|proved|proven|proving|establish(?:es|ed)?|demonstrates?|demonstrated)\b",
}


def normalize(text: str) -> str:
    # LaTeX thousands separator 1{,}000 and non-breaking spaces should not count as changes.
    return text.replace("{,}", ",").replace("\u00a0", " ").replace("~", " ")


def extract(text: str) -> dict:
    text = normalize(text)
    math = [m.group(0) for m in MATH.finditer(text)]
    prose = MATH.sub(" ", text)
    citations = (
        LATEX_CITE.findall(prose) + BRACKET_CITE.findall(prose) + AUTHOR_YEAR.findall(prose)
    )
    prose_no_cites = LATEX_CITE.sub(" ", prose)
    return {
        "numbers": Counter(NUMBER.findall(text)),
        "math": Counter(" ".join(m.split()) for m in math),
        "citations": Counter(" ".join(c.split()) for c in citations),
        "words": {
            name: Counter(w.lower() for w in re.findall(pattern, prose_no_cites, re.I))
            for name, pattern in WORD_CLASSES.items()
        },
    }


def diff(before: Counter, after: Counter) -> tuple:
    return before - after, after - before


def show(counter: Counter) -> str:
    return ", ".join(f"{k!r}" + (f" x{v}" if v > 1 else "") for k, v in sorted(counter.items()))


def main(argv: list) -> int:
    if len(argv) != 3:
        print(__doc__)
        return 2
    original = extract(Path(argv[1]).read_text(encoding="utf-8"))
    revised = extract(Path(argv[2]).read_text(encoding="utf-8"))

    failed = False
    for key in ("numbers", "math", "citations"):
        missing, added = diff(original[key], revised[key])
        if missing or added:
            failed = True
            print(f"FAIL {key}")
            if missing:
                print(f"  in original only: {show(missing)}")
            if added:
                print(f"  in revision only: {show(added)}")
        else:
            print(f"PASS {key} ({sum(original[key].values())} items)")

    for name in WORD_CLASSES:
        missing, added = diff(original["words"][name], revised["words"][name])
        if missing or added:
            print(f"REVIEW {name} words")
            if missing:
                print(f"  removed: {show(missing)}")
            if added:
                print(f"  added: {show(added)}")

    print("RESULT:", "FAIL" if failed else "PASS (hard checks)")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
