#!/usr/bin/env python3
"""
gap_matrix.py - corpus analytics for the finding-gap skill.

Reads a coded extraction sheet (see assets/extraction_template.csv) and reports
descriptive patterns that help locate research gaps:

  * corpus overview (size, years, verification levels, preprints)
  * frequency profiles for categorical fields (cluster, method, country, ...)
  * cross-tabulations (e.g., cluster x method) with empty cells highlighted
  * variable inventory by role and a predictor x outcome co-occurrence matrix
    that exposes frequently studied variables whose link is rarely tested
  * sign conflicts on tested relations (candidate contradictions, M2)
  * recurring future-work / limitation tags across papers, groups, and years (M3)
  * data-age profile relative to an anchor year (M8)

Every number describes ONLY the coded papers in the sheet. A zero means
"not observed in this corpus", never "not studied anywhere".

Standard library only. Usage:
  python3 gap_matrix.py sheet.csv --out outdir --crosstab cluster:method \
      --anchor-year 2023 --top-k 8
"""

import argparse
import csv
import os
import re
import sys
from collections import Counter, defaultdict

MULTI_FIELDS = [
    "cluster", "study_type", "method", "data_source", "population", "country",
    "setting", "theory", "predictors", "mediators", "moderators", "outcomes",
    "limitations_tags", "future_work_tags",
]
PROFILE_FIELDS = [
    "cluster", "study_type", "method", "data_source", "population", "country",
    "setting", "theory",
]
REL_RE = re.compile(r"^\s*(.+?)\s*->\s*(.+?)\s*:\s*([+\-0~])\s*$")
SIGN_LABEL = {"+": "positive", "-": "negative", "0": "null", "~": "mixed/nonlinear"}
CAVEAT = ("All counts describe only the {n} coded papers in this sheet. "
          "A zero or low count means 'not observed in this corpus', not "
          "'unstudied in the literature'. Confirm every candidate gap with "
          "targeted searches.")


# ----------------------------------------------------------------- helpers
def norm(s):
    return re.sub(r"\s+", " ", (s or "").strip()).lower()


def split_multi(value):
    if value is None:
        return []
    out, seen = [], set()
    for part in value.split(";"):
        p = norm(part)
        if p and p not in seen:
            seen.add(p)
            out.append(p)
    return out


def to_int(value):
    try:
        return int(str(value).strip()[:4])
    except (TypeError, ValueError):
        return None


def first_author(authors):
    if not authors:
        return ""
    first = re.split(r";| and ", authors)[0].strip()
    if "," in first:
        return norm(first.split(",")[0])
    parts = first.split()
    return norm(parts[-1]) if parts else ""


def tex_escape(s):
    s = str(s).replace("->", "\x00")
    repl = {"\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "$": r"\$",
            "#": r"\#", "_": r"\_", "{": r"\{", "}": r"\}",
            "~": r"\textasciitilde{}", "^": r"\textasciicircum{}"}
    return "".join(repl.get(c, c) for c in s).replace("\x00", r"\textrightarrow{}")


def md_table(header, rows):
    lines = ["| " + " | ".join(map(str, header)) + " |",
             "|" + "|".join(["---"] * len(header)) + "|"]
    for r in rows:
        cells = [str(c).replace("|", "\\|") for c in r]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def tex_table(caption, label, header, rows, spec=None):
    spec = spec or ("l" + "r" * (len(header) - 1))
    out = [r"\begin{table}[htbp]", r"\centering", r"\small",
           r"\caption{" + tex_escape(caption) + "}",
           r"\label{" + label + "}",
           r"\resizebox{\ifdim\width>\linewidth\linewidth\else\width\fi}{!}{%",
           r"\begin{tabular}{" + spec + "}", r"\toprule",
           " & ".join(tex_escape(h) for h in header) + r" \\", r"\midrule"]
    for r in rows:
        out.append(" & ".join(tex_escape(c) for c in r) + r" \\")
    out += [r"\bottomrule", r"\end{tabular}}", r"\end{table}", ""]
    return "\n".join(out)


# ----------------------------------------------------------------- loading
def load(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        rows = [r for r in reader if any((v or "").strip() for v in r.values())]
        fields = reader.fieldnames or []
    papers, warnings = [], []
    for i, r in enumerate(rows, start=2):
        p = {k: (v or "").strip() for k, v in r.items() if k}
        p["_row"] = i
        p["_label"] = p.get("citation_key") or p.get("id") or f"row{i}"
        p["_year"] = to_int(p.get("year"))
        p["_data_end"] = to_int(p.get("data_end_year"))
        p["_group"] = first_author(p.get("authors", "")) or p["_label"]
        for fld in MULTI_FIELDS:
            p["_" + fld] = split_multi(p.get(fld, ""))
        rels = []
        for raw in (p.get("relations") or "").split(";"):
            if not raw.strip():
                continue
            m = REL_RE.match(raw)
            if not m:
                warnings.append(f"line {i}: could not parse relation '{raw.strip()}' "
                                f"(expected 'X->Y:+|-|0|~')")
                continue
            rels.append((norm(m.group(1)), norm(m.group(2)), m.group(3)))
        p["_relations"] = rels
        if p["_year"] is None:
            warnings.append(f"line {i}: missing or invalid year")
        papers.append(p)
    return papers, fields, warnings


# ----------------------------------------------------------------- analyses
def overview(papers):
    years = [p["_year"] for p in papers if p["_year"]]
    per_year = Counter(years)
    ver = Counter(p.get("verification_level", "") or "unrecorded" for p in papers)
    pre = Counter(norm(p.get("preprint", "")) or "unrecorded" for p in papers)
    return {
        "n": len(papers),
        "year_min": min(years) if years else None,
        "year_max": max(years) if years else None,
        "per_year": sorted(per_year.items()),
        "verification": sorted(ver.items()),
        "preprint": sorted(pre.items()),
    }


def profile(papers, field):
    c = Counter()
    for p in papers:
        c.update(p["_" + field])
    uncoded = sum(1 for p in papers if not p["_" + field])
    return c.most_common(), uncoded


def crosstab(papers, a, b):
    rows_c, cols_c = Counter(), Counter()
    cell = Counter()
    for p in papers:
        for x in p["_" + a]:
            rows_c[x] += 1
            for y in p["_" + b]:
                cell[(x, y)] += 1
        for y in p["_" + b]:
            cols_c[y] += 1
    rows = [r for r, _ in rows_c.most_common()]
    cols = [c for c, _ in cols_c.most_common()]
    return rows, cols, cell


def variable_analysis(papers, top_k):
    roles = {}
    for role in ("predictors", "mediators", "moderators", "outcomes"):
        c = Counter()
        for p in papers:
            c.update(p["_" + role])
        roles[role] = c
    # tested predictor->outcome links (from relations; fall back to co-listing)
    tested = Counter()
    colisted = Counter()
    for p in papers:
        seen = set()
        for x, y, _ in p["_relations"]:
            if (x, y) not in seen:
                tested[(x, y)] += 1
                seen.add((x, y))
        for x in p["_predictors"]:
            for y in p["_outcomes"]:
                colisted[(x, y)] += 1
    top_pred = [v for v, _ in roles["predictors"].most_common(top_k)]
    top_out = [v for v, _ in roles["outcomes"].most_common(top_k)]
    holes = []
    for x in top_pred:
        for y in top_out:
            if x == y:
                continue
            t = tested.get((x, y), 0)
            if t == 0:
                holes.append((x, roles["predictors"][x], y, roles["outcomes"][y],
                              colisted.get((x, y), 0)))
    holes.sort(key=lambda h: -(h[1] * h[3]))
    return roles, tested, top_pred, top_out, holes


def sign_conflicts(papers):
    by_rel = defaultdict(lambda: defaultdict(list))
    for p in papers:
        for x, y, s in p["_relations"]:
            by_rel[(x, y)][s].append(p["_label"])
    conflicts = []
    for rel, signs in by_rel.items():
        directional = {s for s in signs if s in "+-"}
        distinct = set(signs)
        if len(directional) == 2 or (len(distinct) >= 2 and len(directional) >= 1):
            n = sum(len(v) for v in signs.values())
            conflicts.append((rel, {s: sorted(set(v)) for s, v in signs.items()}, n))
    conflicts.sort(key=lambda c: -c[2])
    return conflicts


def recurring_tags(papers, field, min_papers, min_groups, min_years):
    info = defaultdict(lambda: {"papers": set(), "groups": set(), "years": set()})
    for p in papers:
        for t in p["_" + field]:
            info[t]["papers"].add(p["_label"])
            info[t]["groups"].add(p["_group"])
            if p["_year"]:
                info[t]["years"].add(p["_year"])
    rows = []
    for t, d in info.items():
        yrs = sorted(d["years"])
        span = f"{yrs[0]}-{yrs[-1]}" if yrs else "n/a"
        recurring = (len(d["papers"]) >= min_papers and len(d["groups"]) >= min_groups
                     and len(d["years"]) >= min_years)
        rows.append((t, len(d["papers"]), len(d["groups"]), len(d["years"]), span,
                     "yes" if recurring else "no"))
    rows.sort(key=lambda r: (r[5] != "yes", -r[1], -r[2]))
    return rows


def data_age(papers, anchor):
    per_cluster = defaultdict(lambda: {"known": 0, "pre": 0, "unknown": 0})
    for p in papers:
        clusters = p["_cluster"] or ["(no cluster)"]
        for c in clusters:
            if p["_data_end"] is None:
                per_cluster[c]["unknown"] += 1
            else:
                per_cluster[c]["known"] += 1
                if anchor is not None and p["_data_end"] < anchor:
                    per_cluster[c]["pre"] += 1
    rows = []
    for c, d in sorted(per_cluster.items(), key=lambda kv: kv[0]):
        share = f"{100 * d['pre'] / d['known']:.0f}%" if d["known"] else "n/a"
        rows.append((c, d["known"], d["pre"], share, d["unknown"]))
    return rows


# ----------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("sheet", help="coded extraction sheet (CSV)")
    ap.add_argument("--out", default="gap_matrix_out", help="output directory")
    ap.add_argument("--crosstab", action="append", default=[],
                    help="field pair as a:b (repeatable), e.g. cluster:method")
    ap.add_argument("--anchor-year", type=int, default=None,
                    help="flag papers whose data ends before this year (M8)")
    ap.add_argument("--top-k", type=int, default=8,
                    help="top predictors/outcomes for the co-occurrence check")
    ap.add_argument("--recur-min-papers", type=int, default=3)
    ap.add_argument("--recur-min-groups", type=int, default=2)
    ap.add_argument("--recur-min-years", type=int, default=2)
    args = ap.parse_args()

    if not os.path.exists(args.sheet):
        sys.exit(f"error: file not found: {args.sheet}")
    papers, fields, warnings = load(args.sheet)
    if not papers:
        sys.exit("error: the sheet has no data rows")
    missing = [f for f in ["id", "title", "year"] if f not in fields]
    if missing:
        warnings.append(f"missing expected columns: {', '.join(missing)}")

    os.makedirs(args.out, exist_ok=True)
    md, tex = [], []
    n = len(papers)
    caveat = CAVEAT.format(n=n)

    md.append("# Gap matrix summary\n")
    md.append(f"> {caveat}\n")
    tex.append("% Generated by gap_matrix.py. " + caveat)
    tex.append("% Requires: booktabs, graphicx. Use \\input{tables.tex} in the report.\n")
    if warnings:
        md.append("## Data warnings\n")
        md.extend(f"- {w}" for w in warnings)
        md.append("")

    # overview
    ov = overview(papers)
    md.append("## Corpus overview\n")
    md.append(f"- Papers coded: {ov['n']}")
    md.append(f"- Publication years: {ov['year_min']} to {ov['year_max']}")
    md.append("- Verification levels: " +
              ", ".join(f"{k}: {v}" for k, v in ov["verification"]))
    md.append("- Preprint flag: " + ", ".join(f"{k}: {v}" for k, v in ov["preprint"]))
    md.append("")
    if ov["per_year"]:
        md.append(md_table(["Year", "Papers"], ov["per_year"]) + "\n")
        tex.append(tex_table("Coded papers per publication year.", "tab:gm-years",
                             ["Year", "Papers"], ov["per_year"]))

    # profiles
    md.append("## Field profiles\n")
    for fld in PROFILE_FIELDS:
        counts, uncoded = profile(papers, fld)
        if not counts:
            continue
        rows = [(k, v, f"{100 * v / n:.0f}%") for k, v in counts]
        md.append(f"### {fld} (uncoded rows: {uncoded})\n")
        md.append(md_table([fld, "Papers", "Share of corpus"], rows) + "\n")
        tex.append(tex_table(f"Distribution of {fld} in the coded corpus "
                             f"(n={n}; papers can have several values).",
                             f"tab:gm-{fld}", [fld, "Papers", "Share"], rows))

    # crosstabs
    for spec in args.crosstab:
        if ":" not in spec:
            warnings.append(f"ignored crosstab '{spec}' (use a:b)")
            continue
        a, b = [s.strip() for s in spec.split(":", 1)]
        if a not in MULTI_FIELDS or b not in MULTI_FIELDS:
            md.append(f"_Skipped crosstab {spec}: fields must be among "
                      f"{', '.join(MULTI_FIELDS)}_\n")
            continue
        rows, cols, cell = crosstab(papers, a, b)
        if not rows or not cols:
            continue
        table_rows = [[r] + [cell.get((r, c), 0) for c in cols] for r in rows]
        empties = [(r, c) for r in rows for c in cols if cell.get((r, c), 0) == 0]
        md.append(f"## Cross-tabulation: {a} x {b}\n")
        md.append(md_table([f"{a} \\ {b}"] + cols, table_rows) + "\n")
        if empties:
            md.append(f"Empty cells ({len(empties)}), leads only, confirm by search:\n")
            md.extend(f"- {r} x {c}" for r, c in empties[:40])
            md.append("")
        tex.append(tex_table(f"Cross-tabulation of {a} by {b} (paper counts).",
                             f"tab:gm-{a}-{b}", [f"{a} / {b}"] + cols, table_rows))

    # variables
    roles, tested, top_pred, top_out, holes = variable_analysis(papers, args.top_k)
    if any(roles.values()):
        md.append("## Variable inventory\n")
        for role, c in roles.items():
            if c:
                md.append(f"### {role}\n")
                md.append(md_table([role[:-1] if role.endswith('s') else role, "Papers"],
                                   c.most_common()) + "\n")
        if top_pred and top_out:
            md.append(f"## Frequently studied predictors x outcomes with no tested "
                      f"relation in this corpus (top {args.top_k} of each)\n")
            if holes:
                md.append(md_table(["Predictor", "Pred. papers", "Outcome",
                                    "Outc. papers", "Co-listed (untested)"],
                                   holes[:30]) + "\n")
                md.append("Leads for M7. 'Co-listed' means both variables appear in the "
                          "same paper without a coded relation between them.\n")
                tex.append(tex_table("Frequently studied predictor--outcome pairs with "
                                     "no tested relation in the coded corpus.",
                                     "tab:gm-holes",
                                     ["Predictor", "n", "Outcome", "n", "Co-listed"],
                                     holes[:20], spec="lrlrr"))
            else:
                md.append("No untested pairs among the top variables.\n")

    # contradictions
    conflicts = sign_conflicts(papers)
    md.append("## Sign conflicts on tested relations (M2 leads)\n")
    if conflicts:
        rows = []
        for (x, y), signs, total in conflicts:
            detail = "; ".join(f"{SIGN_LABEL[s]}: {', '.join(v)}"
                               for s, v in sorted(signs.items()))
            rows.append((f"{x} -> {y}", total, detail))
        md.append(md_table(["Relation", "Findings", "By sign (papers)"], rows) + "\n")
        md.append("Check that conflicting papers measure comparable constructs before "
                  "calling this a genuine contradiction.\n")
        tex.append(tex_table("Relations with conflicting reported directions.",
                             "tab:gm-conflicts", ["Relation", "Findings", "By sign"],
                             rows, spec="lrp{7cm}"))
    else:
        md.append("No sign conflicts found (or no relations coded).\n")

    # recurring tags
    for fld, title in (("future_work_tags", "Recurring future-work recommendations (M3)"),
                       ("limitations_tags", "Recurring limitations")):
        rows = recurring_tags(papers, fld, args.recur_min_papers,
                              args.recur_min_groups, args.recur_min_years)
        if not rows:
            continue
        md.append(f"## {title}\n")
        md.append(f"Recurring = at least {args.recur_min_papers} papers, "
                  f"{args.recur_min_groups} first-author groups, "
                  f"{args.recur_min_years} distinct years.\n")
        md.append(md_table(["Tag", "Papers", "Groups", "Years", "Span", "Recurring"],
                           rows) + "\n")
        tex.append(tex_table(title + ".", f"tab:gm-{fld}",
                             ["Tag", "Papers", "Groups", "Years", "Span", "Recurring"],
                             rows, spec="lrrrll"))

    # data age
    if args.anchor_year is not None or any(p["_data_end"] for p in papers):
        rows = data_age(papers, args.anchor_year)
        anchor_txt = str(args.anchor_year) if args.anchor_year else "n/a"
        md.append(f"## Data age by cluster (anchor year: {anchor_txt}) (M8)\n")
        md.append(md_table(["Cluster", "Data year known", f"Data ends before {anchor_txt}",
                            "Share pre-anchor", "Data year unknown"], rows) + "\n")
        tex.append(tex_table(f"Data recency by cluster relative to {anchor_txt}.",
                             "tab:gm-dataage",
                             ["Cluster", "Known", "Pre-anchor", "Share", "Unknown"], rows))

    with open(os.path.join(args.out, "summary.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(md))
    with open(os.path.join(args.out, "tables.tex"), "w", encoding="utf-8") as f:
        f.write("\n".join(tex))
    print(f"Analyzed {n} papers -> {args.out}/summary.md, {args.out}/tables.tex")
    if warnings:
        print(f"{len(warnings)} warning(s); see summary.md", file=sys.stderr)


if __name__ == "__main__":
    main()
