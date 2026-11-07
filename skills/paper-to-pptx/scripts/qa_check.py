"""Post-build QA for a paper-to-pptx deck.

    python -I qa_check.py Research_Presentation.pptx --tex paper.tex [more.tex ...]
        [--pdf Research_Presentation.pdf] [--slides 15] [--min-font 9]
    python -I qa_check.py --selftest

ERROR codes (exit 1 if any):
  E01 slide count differs from --slides
  E02 slide has no speaker notes
  E03 em dash or semicolon in slide text or notes (house style)
  E04 shape extends past the slide edge
  E05 picture stretched (aspect ratio off by more than 2 percent)
  E06 picture covers 85 percent or more of the slide (full-slide image)
  E07 explicit font size below --min-font
  E08 template FILL placeholder left in slide text or notes
WARN codes (read every one, then fix or justify it in VERIFICATION.md):
  W01 banned style word
  W02 number on a slide or in notes not found verbatim in the --tex sources
  W03 two text boxes overlap
Overflow and contrast cannot be measured from XML: inspect the rendered PDF.
With --pdf, writes Slide_Montage.png next to the deck.
"""
import argparse
import re
import subprocess
import sys
import tempfile
from pathlib import Path

from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE
from pptx.util import Emu

BANNED = ["very", "really", "literally", "actually", "certainly", "probably", "basically",
          "could", "maybe", "delve", "embark", "utilize", "using", "moreover", "powerful",
          "harness", "groundbreaking", "cutting-edge", "remarkable", "in conclusion",
          "in summary", "not only", "revolutionize", "boost", "exciting", "crafting"]
NUM = re.compile(r"(?<![\w.])\d[\d,]*(?:\.\d+)?")
TOL = Emu(9144)  # 0.01 in


def walk(shapes):
    for sh in shapes:
        if sh.shape_type == MSO_SHAPE_TYPE.GROUP:
            yield from walk(sh.shapes)
        else:
            yield sh


def shape_text(sh):
    parts = []
    if sh.has_text_frame:
        parts.append(sh.text_frame.text)
    if getattr(sh, "has_table", False) and sh.has_table:
        parts += [c.text for row in sh.table.rows for c in row.cells]
    return "\n".join(parts)


def source_text(paths):
    txt = "\n".join(Path(p).read_text(encoding="utf-8", errors="replace") for p in paths)
    return txt.replace("{,}", "").replace(",", "")


def check(pptx, tex, expected, min_font):
    prs = Presentation(pptx)
    W, H = prs.slide_width, prs.slide_height
    src = source_text(tex) if tex else None
    out = []  # (code, slide_no, message)
    n = len(prs.slides)
    if n != expected:
        out.append(("E01", 0, f"{n} slides, expected {expected}"))
    for i, slide in enumerate(prs.slides, 1):
        notes = slide.notes_slide.notes_text_frame.text.strip() if slide.has_notes_slide else ""
        if not notes:
            out.append(("E02", i, "no speaker notes"))
        texts, boxes = [notes], []
        for sh in walk(slide.shapes):
            t = shape_text(sh)
            texts.append(t)
            if sh.left is None or sh.width is None:
                continue
            if sh.left < -TOL or sh.top < -TOL or sh.left + sh.width > W + TOL or sh.top + sh.height > H + TOL:
                out.append(("E04", i, f"'{sh.name}' extends past the slide edge"))
            if sh.shape_type == MSO_SHAPE_TYPE.PICTURE:
                pw, ph = sh.image.size
                cw = 1 - sh.crop_left - sh.crop_right
                chh = 1 - sh.crop_top - sh.crop_bottom
                if pw and ph and sh.height and cw > 0 and chh > 0:
                    native = (pw * cw) / (ph * chh)
                    placed = sh.width / sh.height
                    if abs(placed / native - 1) > 0.02:
                        out.append(("E05", i, f"'{sh.name}' aspect {placed:.3f} vs image {native:.3f}"))
                if sh.width * sh.height >= 0.85 * W * H:
                    out.append(("E06", i, f"'{sh.name}' covers most of the slide"))
            if sh.has_text_frame:
                for p in sh.text_frame.paragraphs:
                    for r in p.runs:
                        if r.font.size is not None and r.font.size.pt < min_font and r.text.strip():
                            out.append(("E07", i, f"{r.font.size.pt:g} pt text '{r.text[:30]}'"))
                if t.strip():
                    boxes.append(sh)
        for a in range(len(boxes)):
            for b in range(a + 1, len(boxes)):
                p, q = boxes[a], boxes[b]
                ix = min(p.left + p.width, q.left + q.width) - max(p.left, q.left)
                iy = min(p.top + p.height, q.top + q.height) - max(p.top, q.top)
                small = min(p.width * p.height, q.width * q.height) or 1
                if ix > 0 and iy > 0 and ix * iy > 0.15 * small:
                    out.append(("W03", i, f"'{p.name}' overlaps '{q.name}'"))
        blob = "\n".join(texts)
        if re.search(r"\bFILL\b", blob):
            out.append(("E08", i, "FILL placeholder left"))
        for ch, what in (("—", "em dash"), (";", "semicolon")):
            if ch in blob:
                out.append(("E03", i, what))
        for w in BANNED:
            if re.search(r"\b" + re.escape(w) + r"\b", blob, re.I):
                out.append(("W01", i, f"banned word '{w}'"))
        if src is not None:
            for m in sorted(set(NUM.findall(blob))):
                v = m.replace(",", "")
                if ("." in v or len(v) >= 2) and v not in src:
                    out.append(("W02", i, f"number {m} not found in source"))
    return n, out


def montage(pdf, dest):
    from PIL import Image, ImageDraw
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(["pdftoppm", "-png", "-r", "40", str(pdf), str(Path(tmp) / "s")], check=True)
        thumbs = [Image.open(p).convert("RGB") for p in sorted(Path(tmp).glob("s-*.png"))]
        w, h = thumbs[0].size
        cols, pad = 3, 14
        rows = (len(thumbs) + cols - 1) // cols
        sheet = Image.new("RGB", (cols * (w + pad) + pad, rows * (h + pad + 18) + pad), "white")
        draw = ImageDraw.Draw(sheet)
        for i, im in enumerate(thumbs):
            x, y = pad + (i % cols) * (w + pad), pad + (i // cols) * (h + pad + 18)
            sheet.paste(im, (x, y + 18))
            draw.rectangle([x - 1, y + 17, x + w, y + 18 + h], outline="#C3CAD2")
            draw.text((x, y + 2), f"Slide {i + 1}", fill="#1B2430")
        sheet.save(dest)
    return len(thumbs)


def selftest():
    from PIL import Image
    from pptx.util import Inches, Pt
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        Image.new("RGB", (400, 200), "gray").save(tmp / "img.png")
        (tmp / "paper.tex").write_text("We report a gain of 12.5\\% on 1{,}000 samples.", encoding="utf-8")
        prs = Presentation()
        prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
        s1 = prs.slides.add_slide(prs.slide_layouts[6])
        tb = s1.shapes.add_textbox(Inches(1), Inches(1), Inches(5), Inches(1))
        tb.text_frame.text = "Gain of 12.5% on 1,000 samples, really 99.7 — fine; ok"
        s1.shapes.add_textbox(Inches(1.2), Inches(1.1), Inches(5), Inches(1)).text_frame.text = "overlap"
        s1.notes_slide.notes_text_frame.text = "Notes."
        s2 = prs.slides.add_slide(prs.slide_layouts[6])
        s2.shapes.add_textbox(Inches(12), Inches(1), Inches(3), Inches(1)).text_frame.text = "off"
        s2.shapes.add_picture(str(tmp / "img.png"), Inches(1), Inches(3), Inches(2), Inches(2))
        r = s2.shapes.add_textbox(Inches(1), Inches(6), Inches(3), Inches(0.5)).text_frame.paragraphs[0].add_run()
        r.text, r.font.size = "tiny", Pt(7)
        s3 = prs.slides.add_slide(prs.slide_layouts[6])
        s3.shapes.add_picture(str(tmp / "img.png"), 0, 0, prs.slide_width, Inches(6.67))
        s3.notes_slide.notes_text_frame.text = "FILL from the abstract."
        prs.save(tmp / "t.pptx")
        _, out = check(tmp / "t.pptx", [tmp / "paper.tex"], 15, 9)
    got = {c for c, _, _ in out}
    want = {"E01", "E02", "E03", "E04", "E05", "E06", "E07", "E08", "W01", "W02", "W03"}
    nums = {m for c, _, m in out if c == "W02"}
    assert got == want, f"codes {sorted(got)} != {sorted(want)}"
    assert nums == {"number 99.7 not found in source"}, nums  # 12.5 and 1,000 must match the source
    print("selftest passed: all 11 checks fire, source numbers match")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pptx", nargs="?", type=Path)
    ap.add_argument("--tex", nargs="+", default=[])
    ap.add_argument("--pdf", type=Path)
    ap.add_argument("--slides", type=int, default=15)
    ap.add_argument("--min-font", type=float, default=9)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not a.pptx:
        ap.error("pptx path required")
    n, out = check(a.pptx, a.tex, a.slides, a.min_font)
    for code, i, msg in sorted(out, key=lambda r: (r[0][0] != "E", r[1], r[0])):
        print(f"{code} slide {i}: {msg}")
    errs = sum(c.startswith("E") for c, _, _ in out)
    print(f"slides: {n}, errors: {errs}, warnings: {len(out) - errs}")
    if not a.tex:
        print("no --tex given: number audit W02 skipped")
    if a.pdf:
        k = montage(a.pdf, a.pptx.with_name("Slide_Montage.png"))
        print(f"montage: {a.pptx.with_name('Slide_Montage.png')} ({k} slides)")
    sys.exit(1 if errs else 0)


if __name__ == "__main__":
    main()
