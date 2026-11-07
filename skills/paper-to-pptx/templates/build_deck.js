// Starter for a paper-to-pptx deck. Copy to <paper dir>/Presentation/src/build_deck.js,
// replace every FILL, choose the visual direction (THEME), then write the slides.
// Every data block on a slide carries a SOURCE comment naming the .tex line, table or figure
// it came from. Run from the Presentation folder:
//   python <skill>/scripts/render_equations.py src/equations.json assets/eq --preamble src/macros.tex
//   node src/build_deck.js
const path = require("path");
const fs = require("fs");
const os = require("os");
const pptxgen = require("pptxgenjs");

// The pptx skill's apply_theme.js writes THEME colors into the deck. Its synced folder name
// changes, so it is found by search unless PPTX_SKILL_DIR is set.
function pptxSkillDir() {
  if (process.env.PPTX_SKILL_DIR) return process.env.PPTX_SKILL_DIR;
  const synced = path.join(os.homedir(), ".claude", "skills", "synced");
  for (const d of fs.existsSync(synced) ? fs.readdirSync(synced) : []) {
    const p = path.join(synced, d, "pptx");
    if (fs.existsSync(path.join(p, "scripts", "apply_theme.js"))) return p;
  }
  throw new Error("pptx skill not found: set PPTX_SKILL_DIR");
}
const { applyTheme } = require(path.join(pptxSkillDir(), "scripts", "apply_theme.js"));

const ROOT = path.resolve(__dirname, "..");
const EQDIR = path.join(ROOT, "assets", "eq");
const EQ = fs.existsSync(path.join(EQDIR, "manifest.json"))
  ? JSON.parse(fs.readFileSync(path.join(EQDIR, "manifest.json"), "utf8")) : {};
const OUTFILE = path.join(ROOT, "Research_Presentation.pptx");

// ---------------------------------------------------------------- config
const CONFIG = {
  slides: 15,                       // the contract; change only if the user asked
  title: "FILL exact paper title",
  shortTitle: "FILL short title for the footer",
  footer: "FILL venue and status exactly as the source states it", // e.g. "ICLR 2027 submission, under review"
  author: "FILL as in the source, or Anonymous for a double-blind paper",
};

// ---------------------------------------------------------------- theme
// Replace with the direction chosen for this paper. Colors carry meaning (one accent per
// concept, used the same way on every slide). Six hex digits, never "#".
const HEX = {
  ink: "1B2430", dark: "141B24", white: "FFFFFF", panel: "F2F4F6",
  accentA: "B42318", accentB: "2456A6", accentC: "C26A12", gray: "7A8592",
  accentD: "2F7D4F", muted: "5B6573",
  onDarkMuted: "AEB7C2", onDarkSoft: "D7DDE4", grid: "E3E7EB",
};
const THEME = {
  name: "FILL theme name",
  headFontFace: "Cambria",   // widely installed serif for headings
  bodyFontFace: "Calibri",   // widely installed sans for body
  colors: {
    dk1: HEX.ink, lt1: HEX.white, dk2: HEX.dark, lt2: HEX.panel,
    accent1: HEX.accentA, accent2: HEX.accentB, accent3: HEX.accentC, accent4: HEX.gray,
    accent5: HEX.accentD, accent6: HEX.muted, hlink: HEX.accentB, folHlink: HEX.muted,
  },
};

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in, set before any slide
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
pres.title = CONFIG.title;
pres.author = CONFIG.author;
const C = pres.SchemeColor;
const HEAD = "+mj-lt";
const SH = pres.shapes;
const X0 = 0.6, XR = 12.733, CW = XR - X0; // alignment grid: 0.6 in side margins

// ---------------------------------------------------------------- layouts
pres.defineSlideMaster({
  title: "CONTENT",
  background: { color: C.background1 },
  margin: [0.5, 0.6, 0.5, 0.6],
  objects: [
    { placeholder: { options: { name: "kicker", type: "body", x: X0, y: 0.34, w: 8.9, h: 0.3,
        fontSize: 11, bold: true, color: C.accent6, charSpacing: 1.2, margin: 0, valign: "middle" }, text: "" } },
    { placeholder: { options: { name: "title", type: "title", x: X0, y: 0.66, w: CW, h: 0.66,
        fontSize: 28, bold: true, color: C.text1, margin: 0, valign: "top", align: "left" }, text: "" } },
    { text: { text: `${CONFIG.shortTitle}  ·  ${CONFIG.footer}`,
        options: { x: X0, y: 7.06, w: 9, h: 0.26, fontSize: 9, color: C.accent6, margin: 0, isTextBox: true } } },
  ],
  slideNumber: { x: 12.13, y: 7.06, w: 0.6, h: 0.26, fontSize: 9, color: C.accent6, align: "right", margin: 0 },
});
pres.defineSlideMaster({ title: "DARK", background: { color: C.text2 }, objects: [] });

// ---------------------------------------------------------------- helpers
// Mini markup inside strings: **bold**, _{sub}, ^{sup}, ~{italic}
function runs(str, base = {}) {
  str = str.replace(/(\S) = (\S)/g, "$1 = $2"); // keep "a = b" on one line
  const out = [];
  let buf = "", bold = false;
  const flush = () => { if (buf) { out.push({ text: buf, options: { ...base, ...(bold ? { bold: true } : {}) } }); buf = ""; } };
  for (let i = 0; i < str.length; i++) {
    const two = str.slice(i, i + 2);
    if (two === "**") { flush(); bold = !bold; i++; continue; }
    if (two === "_{" || two === "^{" || two === "~{") {
      flush();
      const end = str.indexOf("}", i + 2);
      const o = { ...base, ...(bold ? { bold: true } : {}) };
      if (two === "_{") o.subscript = true;
      if (two === "^{") o.superscript = true;
      if (two === "~{") o.italic = true;
      out.push({ text: str.slice(i + 2, end), options: o });
      i = end;
      continue;
    }
    buf += str[i];
  }
  flush();
  return out;
}

// items: string or {t, bullet, size, color, bold, italic, space, font}
function paras(items, base = {}) {
  const all = [];
  items.forEach((it, idx) => {
    const o = typeof it === "string" ? { t: it } : it;
    const rb = { ...base };
    delete rb._bullet; delete rb._space;
    if (o.size) rb.fontSize = o.size;
    if (o.color) rb.color = o.color;
    if (o.bold) rb.bold = true;
    if (o.italic) rb.italic = true;
    if (o.font) rb.fontFace = o.font;
    const rs = runs(o.t, rb);
    const bullet = o.bullet === undefined ? base._bullet : o.bullet;
    if (bullet) rs[0].options.bullet = { indent: 14 };
    rs[0].options.paraSpaceAfter = o.space !== undefined ? o.space : (base._space !== undefined ? base._space : 6);
    if (idx < items.length - 1) rs[rs.length - 1].options.breakLine = true;
    all.push(...rs);
  });
  return all;
}

function text(slide, content, opts) {
  const o = { isTextBox: true, margin: 0, valign: "top", fontSize: 14, color: C.text1, ...opts };
  slide.addText(typeof content === "string" ? runs(content, {}) : content, o);
}

// Equation image at true scale: scale 1 = the 12pt render size. Alt text keeps the LaTeX.
function eq(slide, name, x, y, scale = 1.6) {
  const m = EQ[name];
  if (!m) throw new Error(`equation '${name}' missing from assets/eq/manifest.json`);
  const w = (m.px_w / m.dpi) * scale, h = (m.px_h / m.dpi) * scale;
  slide.addImage({ path: path.join(EQDIR, `${name}.png`), x, y, w, h, altText: m.latex || name });
  return { w, h };
}

// Figure from the paper at its native aspect ratio, fitted into a w x h box.
function figure(slide, file, x, y, w, h, alt) {
  const { execFileSync } = require("child_process");
  const [pw, ph] = execFileSync("python", ["-c",
    "import sys;from PIL import Image;im=Image.open(sys.argv[1]);print(*im.size)", file]).toString().trim().split(" ").map(Number);
  const s = Math.min(w / pw, h / ph);
  const fw = pw * s, fh = ph * s;
  slide.addImage({ path: file, x: x + (w - fw) / 2, y: y + (h - fh) / 2, w: fw, h: fh, altText: alt });
  return { w: fw, h: fh };
}

function line(slide, x1, y1, x2, y2, o = {}) {
  slide.addShape(SH.LINE, {
    x: Math.min(x1, x2), y: Math.min(y1, y2), w: Math.abs(x2 - x1), h: Math.abs(y2 - y1),
    flipH: x2 < x1, flipV: y2 < y1,
    line: { color: o.color || C.text1, width: o.width || 1.25, dashType: o.dash || "solid",
      endArrowType: o.arrow ? "triangle" : undefined, beginArrowType: o.beginArrow ? "triangle" : undefined,
      transparency: o.transparency },
  });
}

function box(slide, x, y, w, h, content, o = {}) {
  slide.addText(typeof content === "string" ? runs(content, {}) : content, {
    shape: o.shape || SH.RECTANGLE, x, y, w, h,
    fill: o.fill === null ? undefined : (o.fill || { color: C.background1 }),
    line: o.line === null ? undefined : (o.line || { color: C.text1, width: 1 }),
    align: o.align || "center", valign: o.valign || "middle",
    fontSize: o.fontSize || 13, color: o.color || C.text1, margin: o.margin !== undefined ? o.margin : 4,
    rectRadius: o.rectRadius, objectName: o.name,
  });
}

// Claim-status tag on the kicker row. It tells the audience what kind of support a slide
// has, the same way the paper does. "target" marks numbers the paper itself labels as
// unmeasured, projected or implementation targets.
function tag(slide, label, kind = "evidence") {
  const w = 0.3 + label.length * 0.082;
  const st = {
    theory: { fill: { color: C.text1 }, line: { color: C.text1, width: 0.75 }, color: C.background1 },
    evidence: { fill: { color: C.background1 }, line: { color: C.text1, width: 0.75 }, color: C.text1 },
    method: { fill: { color: C.accent2 }, line: { color: C.accent2, width: 0.75 }, color: C.background1 },
    target: { fill: { color: C.background1 }, line: { color: C.accent2, width: 1, dashType: "dash" }, color: C.accent2 },
  }[kind];
  slide.addText(label, {
    shape: SH.ROUNDED_RECTANGLE, rectRadius: 0.13, x: XR - w, y: 0.33, w, h: 0.28,
    fill: st.fill, line: st.line, color: st.color, fontSize: 9.5, bold: true,
    charSpacing: 1, align: "center", valign: "middle", margin: 0, objectName: "Claim tag",
  });
}

function contentSlide(section, kicker, title, tagSpec) {
  const s = pres.addSlide({ masterName: "CONTENT", sectionTitle: section });
  s.addText(kicker, { placeholder: "kicker" });
  s.addText(title, { placeholder: "title" }); // a sentence stating the slide's point
  if (tagSpec) tag(s, tagSpec[0], tagSpec[1]);
  return s;
}

const chartFont = { catAxisLabelFontFace: "+mn-lt", valAxisLabelFontFace: "+mn-lt",
  dataLabelFontFace: "+mn-lt", legendFontFace: "+mn-lt", titleFontFace: "+mn-lt",
  valAxisTitleFontFace: "+mn-lt", catAxisTitleFontFace: "+mn-lt" };

// ================================================================ SLIDE 1 · Title
pres.addSection({ title: "Opening" });
{
  // SOURCE: \title, \author, venue line of paper.tex (FILL line numbers)
  const s = pres.addSlide({ masterName: "DARK", sectionTitle: "Opening" });
  text(s, CONFIG.title, { x: 0.7, y: 1.7, w: 7.4, h: 2.3, fontSize: 36, bold: true, color: C.background1, fontFace: HEAD });
  text(s, CONFIG.author, { x: 0.7, y: 4.2, w: 7, h: 0.4, fontSize: 18, color: C.background1 });
  // FILL: a research-specific visual on the right (the paper's headline result or framework),
  // never a stock image.
  s.addNotes("FILL from the abstract.");
}

// ================================================================ SLIDES 2-14
// FILL: one block per slide, following the plan in VERIFICATION.md. Example frame:
//   pres.addSection({ title: "Motivation" });
//   { // SOURCE: paper.tex L40-L58 (Introduction, para 2)
//     const s = contentSlide("Motivation", "PROBLEM", "FILL sentence that states the point", ["EVIDENCE", "evidence"]);
//     text(s, paras(["FILL", "FILL"], { _bullet: true }), { x: X0, y: 1.6, w: 6, h: 4.8, fontSize: 18 });
//     s.addNotes("FILL from the paper text.");
//   }

// ================================================================ SLIDE 15 · Closing
pres.addSection({ title: "Closing" });
{
  // SOURCE: Conclusion section (FILL line numbers)
  const s = pres.addSlide({ masterName: "DARK", sectionTitle: "Closing" });
  text(s, "FILL one-line takeaway grounded in the conclusion", { x: 0.7, y: 1.3, w: 7.2, h: 1.5, fontSize: 36, bold: true, color: C.background1, fontFace: HEAD });
  text(s, "Questions and discussion", { x: 0.7, y: 5.75, w: 8, h: 0.55, fontSize: 28, bold: true, color: C.background1, fontFace: HEAD });
  s.addNotes("FILL from the conclusion.");
}

// ---------------------------------------------------------------- write
(async () => {
  const n = pres.slides.length;
  if (n !== CONFIG.slides) console.warn(`WARNING: ${n} slides built, contract is ${CONFIG.slides}`);
  await pres.writeFile({ fileName: OUTFILE });
  await applyTheme(OUTFILE, THEME);
  console.log("wrote", OUTFILE, `(${n} slides)`);
})();
