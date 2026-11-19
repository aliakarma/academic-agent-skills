// ---------------------------------------------------------------------------
//  TEMPLATE: editable PowerPoint twin of a TikZ figure (figure-rebuild skill).
//
//  Copy to figures/<name>_pptx.js, then edit only the CONFIG block and the
//  FIGURE CONTENT block. Every coordinate is the TikZ one, in cm, read off
//  figures/<name>.tex: same centres, widths, heights, lane ordinates. The
//  helpers flip y, fit the figure to the slide and scale the type with it.
//
//  Run from figures/ (icons resolve to icons/<name>.png):
//      node <name>_pptx.js                 -> <name>.pptx
//      zip -dq <name>.pptx '*/'            # drop ZIP folder entries
//  then validate and render (see SKILL.md, Phase 8).
//
//  Needs pptxgenjs (preinstalled with the pptx skill; else npm i pptxgenjs).
// ---------------------------------------------------------------------------
const fs = require("fs");
const path = require("path");
const pptxgen = require("pptxgenjs");

// =============================== CONFIG ====================================
const OUT = "figure.pptx";                       // -> "<name>.pptx"
const TITLE = "Figure N: <caption head>";        // document title (not drawn)
const NOTES = "<full figure caption, pasted from the manuscript>";
// TikZ bounding box in cm (xmin, xmax, ymin, ymax): take it from the
// extreme node edges in <name>.tex; add ~0.1 cm of slack each side.
const EXTENT = { xmin: -0.2, xmax: 8.2, ymin: -1.6, ymax: 1.6 };
const FONT = "Calibri";                          // safe in PowerPoint and QA
// TikZ type sizes in pt (\scriptsize = 8, \tiny = 6 in a 12pt class;
// 7 and 5 in a 10pt class). They are scaled with the drawing below.
const TIKZ_PT = { title: 8, detail: 6, panel: 10 };
// Palette: paste the hex values from figures/figstyle.tex. Each fill
// colour is [fill, stroke].
const COL = {
  ink: "2B2B2B", mute: "6E6E6E", line: "9E9E9E", panel: "F3F3F3",
  box: ["F2F2F2", "C4C4C4"], accent: ["C2DDFB", "7FA9DA"],
  good: ["C9E7CD", "86BF8E"], bad: ["F4C9A7", "DE9A66"],
};
// ===========================================================================

// ---- fit: 13.33 x 7.5 in slide, 0.4 in margins ----------------------------
const SW = 13.333, SH = 7.5, M = 0.4;
const K = Math.min((SW - 2 * M) / (EXTENT.xmax - EXTENT.xmin),
                   (SH - 2 * M) / (EXTENT.ymax - EXTENT.ymin));   // in per cm
const X0 = (SW - K * (EXTENT.xmax - EXTENT.xmin)) / 2;
const Y0 = (SH - K * (EXTENT.ymax - EXTENT.ymin)) / 2;
const X = (x) => X0 + (x - EXTENT.xmin) * K;
const Y = (y) => Y0 + (EXTENT.ymax - y) * K;
const PT = (tikzPt) => Math.round(tikzPt * K * 2.54);   // keep type in proportion
const T = PT(TIKZ_PT.title), D = PT(TIKZ_PT.detail), P = PT(TIKZ_PT.panel);

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
pres.title = TITLE;
const s = pres.addSlide();
s.background = { color: "FFFFFF" };

// ---- rich text: "{k}" italic, "_{L}" subscript, "^{2}" superscript --------
function runs(str, size, color = COL.ink, extra = {}) {
  const out = [], re = /\{([^}]*)\}|_\{([^}]*)\}|\^\{([^}]*)\}|([^{_^]+|[_^])/g;
  let m;
  while ((m = re.exec(str))) {
    const o = { fontSize: size, color, fontFace: FONT, ...extra };
    if (m[1] !== undefined) out.push({ text: m[1], options: { ...o, italic: true } });
    else if (m[2] !== undefined) out.push({ text: m[2], options: { ...o, subscript: true } });
    else if (m[3] !== undefined) out.push({ text: m[3], options: { ...o, superscript: true } });
    else out.push({ text: m[4], options: o });
  }
  return out;
}
// lines: [[text, size, color?, {italic|bold}?], ...] -> one paragraph per line
function para(lines) {
  const all = [];
  lines.forEach(([t, sz, c, extra], i) => {
    const r = runs(t, sz, c || COL.ink, extra || {});
    if (i < lines.length - 1) r[r.length - 1].options.breakLine = true;
    all.push(...r);
  });
  return all;
}

// ---- icons: the same PNGs the TikZ figure uses ----------------------------
function pngSize(p) { const b = fs.readFileSync(p); return [b.readUInt32BE(16), b.readUInt32BE(20)]; }
function icon(name, cxIn, topIn, hIn) {
  const p = path.join("icons", `${name}.png`);
  if (!fs.existsSync(p)) throw new Error(`missing icon ${p}: run extract_icons.py first`);
  const [w, h] = pngSize(p), wIn = (hIn * w) / h;
  s.addImage({ path: p, x: cxIn - wIn / 2, y: topIn, w: wIn, h: hIn, altText: name });
}

// ---- shapes (all arguments in TikZ cm) ------------------------------------
// box: rounded node centred at (cx,cy), size w x h, optional icon on top
function box(name, cx, cy, w, h, col, lines, { ic = null, icCm = 0.55 } = {}) {
  const x = X(cx - w / 2), y = Y(cy + h / 2), wi = w * K, hi = h * K, icH = icCm * K;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w: wi, h: hi, rectRadius: 0.08,
    fill: { color: col[0] }, line: { color: col[1], width: 0.75 }, objectName: name });
  if (ic) icon(ic, x + wi / 2, y + 0.1, icH);
  const ty = ic ? y + 0.12 + icH : y;
  s.addText(para(lines), { x, y: ty, w: wi, h: y + hi - ty - 0.04, margin: 0.02,
    align: "center", valign: "middle", isTextBox: true, objectName: `${name} text` });
}
// enclosure: dashed group outline from (x1,y1) top-left to (x2,y2) bottom-right
function enclosure(name, x1, y1, x2, y2, fill = COL.panel) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: X(x1), y: Y(y1), w: (x2 - x1) * K, h: (y1 - y2) * K,
    rectRadius: 0.1, fill: { color: fill }, line: { color: COL.line, width: 0.75, dashType: "dash" },
    objectName: name });
}
// poly: orthogonal connector through [[x,y],...]; head on the last segment.
// dash: "solid" data flow, "dash" comparison/control (match the TikZ legend)
function poly(pts, { dash = "solid", head = true, color = COL.line, width = 1.25 } = {}) {
  for (let i = 0; i < pts.length - 1; i++) {
    const [x1, y1] = pts[i], [x2, y2] = pts[i + 1];
    if (x1 !== x2 && y1 !== y2) throw new Error(`poly segment ${i} is diagonal; add a corner point`);
    const ax = X(x1), ay = Y(y1), bx = X(x2), by = Y(y2);
    const o = { x: Math.min(ax, bx), y: Math.min(ay, by), w: Math.abs(bx - ax), h: Math.abs(by - ay),
      flipH: bx < ax, flipV: by < ay, line: { color, width, dashType: dash } };
    if (head && i === pts.length - 2) o.line.endArrowType = "triangle";
    s.addShape(pres.shapes.LINE, o);
  }
}
// label: text centred at (cx,cy), w cm wide; knock=true paints white behind it
// (the TikZ fill=white callout). Size the width to the text, or it blanks the line.
function label(str, cx, cy, w, { size = D, color = COL.ink, knock = false, align = "center" } = {}) {
  const o = { x: X(cx - w / 2), y: Y(cy) - 0.13, w: w * K, h: 0.26, margin: 0, align,
    valign: "middle", isTextBox: true };
  if (knock) o.fill = { color: "FFFFFF" };
  s.addText(runs(str, size, color), o);
}

// ============================ FIGURE CONTENT ===============================
// Transcribe <name>.tex in this order: panel tags, enclosures (they are
// behind everything), boxes, connectors, labels. Example below: replace it.
label("(a) Panel tag", 0.9, 1.4, 2.2, { size: P, align: "left" });
enclosure("group", 2.6, 1.15, 5.4, -1.15);
box("Source", 1.0, 0, 2.0, 1.4, COL.box, [["Source", T], ["rate {λ}_{0}", D]]);
box("Stage", 4.0, 0, 2.0, 1.4, COL.accent, [["Stage", T], ["G/G/{k}", D]]);   // add { ic: "llm" } for an icon
box("Done", 7.0, 0.55, 2.0, 0.9, COL.good, [["Done", T]]);
box("Failed", 7.0, -0.85, 2.0, 0.9, COL.bad, [["Failed", T]]);
poly([[2.0, 0], [3.0, 0]]);
poly([[5.0, 0], [5.6, 0], [5.6, 0.55], [6.0, 0.55]]);
poly([[5.0, 0], [5.6, 0], [5.6, -0.85], [6.0, -0.85]], { dash: "dash" });
label("retry", 5.6, -1.35, 0.8);
// ===========================================================================

s.addNotes(NOTES);
pres.writeFile({ fileName: OUT }).then((f) => console.log(`wrote ${f} (K=${K.toFixed(3)} in/cm, title ${T}pt, detail ${D}pt)`));
