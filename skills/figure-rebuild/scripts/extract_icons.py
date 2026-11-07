#!/usr/bin/env python3
"""Extract pictograms from a raster figure, trimmed and free of neighbouring text.

Starting point for Phase 3 of the figure-rebuild skill. Edit BOXES for the
figure at hand; the coordinates are in ORIGINAL image pixels.

Method, and the order matters:

 1. View a zoomed crop of each region first, at 1:1, to read exact coordinates.
    Estimating from a downscaled preview reliably puts a neighbouring word
    inside the crop.
 2. Crop generously, then auto-trim the near-white margin.
 3. Upscale 2x so the icon stays crisp at print size.
 4. Build a contact sheet and LOOK AT IT. Fix any icon carrying a stray glyph
    or a neighbour's arrowhead, and re-run. Two passes is normal.

Usage:
    python extract_icons.py SOURCE.jpeg OUTDIR
"""
from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw

# name -> (left, top, right, bottom) in ORIGINAL image pixels
BOXES: dict[str, tuple[int, int, int, int]] = {
    # "camera": (70, 552, 165, 628),
}


def trim(im: Image.Image, thresh: int = 246, pad: int = 3) -> Image.Image:
    """Drop uniform near-white margin so each icon sits tight in its box."""
    g = im.convert("L").point(lambda v: 0 if v < thresh else 255)
    bbox = ImageChops.invert(g).getbbox()
    if bbox is None:
        return im
    l, t, r, b = bbox
    return im.crop((max(0, l - pad), max(0, t - pad),
                    min(im.width, r + pad), min(im.height, b + pad)))


def main() -> int:
    if len(sys.argv) < 3:
        print(__doc__)
        return 1
    src = Image.open(sys.argv[1]).convert("RGB")
    out = Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)

    if not BOXES:
        print("BOXES is empty. Crop and view the regions first, then fill it in.")
        print("source size: %dx%d" % src.size)
        return 1

    tiles = []
    for name, box in BOXES.items():
        ic = trim(src.crop(box))
        ic = ic.resize((ic.width * 2, ic.height * 2), Image.LANCZOS)
        ic.save(out / ("%s.png" % name))
        tiles.append((name, ic))

    cols = 7
    tw = max(c.width for _, c in tiles)
    th = max(c.height for _, c in tiles)
    rows = (len(tiles) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * (tw + 14), rows * (th + 30)), "white")
    d = ImageDraw.Draw(sheet)
    for i, (name, c) in enumerate(tiles):
        r, col = divmod(i, cols)
        x = col * (tw + 14) + 7 + (tw - c.width) // 2
        y = r * (th + 30) + 4 + (th - c.height) // 2
        sheet.paste(c, (x, y))
        d.text((col * (tw + 14) + 7, r * (th + 30) + th + 8), name, fill="black")
    sheet.save(out / "_contact.png")
    print("extracted %d icons; NOW VIEW %s" % (len(tiles), out / "_contact.png"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
