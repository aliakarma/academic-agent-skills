#!/usr/bin/env python3
"""Prove that figure text in a compiled PDF is real text, not raster.

The whole point of the rebuild is selectable, searchable, body-font text. That
claim must be demonstrated, not asserted, so run this before reporting done.

Also renders the pages carrying each probe, because a figure that is correct in
isolation can still collide with a column or run off the page in context.
LOOK AT THOSE RENDERS.

Usage:
    python verify_selectable.py main.pdf "O-RU" "harmonised" "emulated"
"""
from __future__ import annotations

import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) < 3:
        print(__doc__)
        return 1
    try:
        import fitz  # PyMuPDF
    except ImportError:
        print("PyMuPDF is required:  pip install pymupdf")
        return 1

    pdf = Path(sys.argv[1])
    probes = sys.argv[2:]
    doc = fitz.open(pdf)

    pages_to_render, missing = set(), []
    for probe in probes:
        hits = [i for i, pg in enumerate(doc) if pg.search_for(probe)]
        if hits:
            print("  %-24s selectable on page(s) %s"
                  % (probe, ", ".join(str(h + 1) for h in hits)))
            pages_to_render.add(hits[0])
        else:
            print("  %-24s MISSING -- still rasterised, or the wording changed"
                  % probe)
            missing.append(probe)

    for i in sorted(pages_to_render):
        outp = pdf.with_name("_verify_page%d.png" % (i + 1))
        doc[i].get_pixmap(dpi=130).save(outp)
        print("  rendered %s" % outp.name)

    if missing:
        print("\nFAIL: %d probe(s) not found as text." % len(missing))
        return 1
    print("\nOK: every probe is selectable text. Now VIEW the rendered pages.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
