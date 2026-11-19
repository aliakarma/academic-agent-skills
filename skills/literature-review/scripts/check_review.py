#!/usr/bin/env python3
"""Check a literature_review.md against the skill's deliverable contract.

  python check_review.py literature_review.md
  python check_review.py literature_review.md --ledger literature/source_ledger.csv
  python check_review.py --selftest

ERROR (exit 1):
  E01 one of the 17 required sections is missing
  E02 gap matrix (Sec. 10) or novelty table (Sec. 11) lacks a required column
  E03 a gap record (### G<n> in Sec. 9) lacks a field A-K, a Category, or uses
      a value outside the allowed vocabulary
  E04 a cited [key] has no entry in Sec. 15 or Sec. 16
  E05 a Sec. 15 entry lacks a DOI/URL, a Status of VERIFIED or
      VERIFIED-QUALIFIED, a Peer review label, or an Access level
  E06 template placeholder text is left in the file
  E07 (--ledger) a Sec. 15 key is not VERIFIED/VERIFIED-QUALIFIED in the
      ledger, or its DOI differs from the ledger DOI
  E08 a key is listed in both Sec. 15 and Sec. 16
  E09 (--search-log) a gap's Examined line cites a Q-id not in the search log
WARN:
  W01 overclaim wording ("first to", "no prior work", ...) outside quotes
  W02 Sec. 15 entry never cited in the body
  W03 body cites a Sec. 16 (unverified) source
  W04 em dash or semicolon in prose (user style rule)
  W05 "systematic review" / "PRISMA" wording: confirm the protocol was run
  W06 the review says "fully verified" while Sec. 16 lists sources
  W08 (--ledger) closed-access venues outside 40-60% of Sec. 15, or sources
      with no venue_access
  W07 a gap has no Examined line with Q-ids, or (--search-log) none of its
      Q-ids was logged with a "counterevidence" purpose

The summary counts it prints (references by status, gaps by category and
confidence) are the numbers to use in the completion report.
"""
import argparse
import csv
import re
import sys

SECTIONS = [
    (1, "metadata"), (2, "executive summary"), (3, "original manuscript"),
    (4, "methodology"), (5, "background"), (6, "thematic"),
    (7, "critical comparison"), (8, "established knowledge"),
    (9, "research gaps"), (10, "evidence matrix"), (11, "novelty"),
    (12, "research directions"), (13, "implications"), (14, "limitations"),
    (15, "verified references"), (16, "unverified"), (17, "reproducibility"),
]
GAP_COLS = ["candidate gap", "supporting studies", "counterevidence",
            "remaining unresolved", "relevance", "confidence", "novelty risk"]
NOV_COLS = ["manuscript claim", "closest related work", "verified similarities",
            "distinctive", "evidence required", "current assessment"]
CATEGORIES = ["established research gap", "context-dependent gap",
              "emerging research gap", "potential or tentative gap",
              "unsupported or resolved gap"]
CONFIDENCE = ["strongly supported", "moderately supported", "tentative",
              "unsupported"]
RISK = ["low", "medium", "high"]
RELATION = ["partially addressed", "addressed", "unresolved"]
FIELDS = "ABCDEFGHIJK"
OVERCLAIM = re.compile(
    r"\b(first to|the first\b|no prior work|no previous work|no study has|"
    r"no studies have|never been (?:studied|addressed)|to the best of our "
    r"knowledge|unprecedented|fully verified)", re.I)
CITE = re.compile(r"\[([a-z][a-z0-9_:-]*\d[a-z0-9_:-]*(?:\s*[;,]\s*[a-z][a-z0-9_:-]*\d[a-z0-9_:-]*)*)\]")
ENTRY = re.compile(r"^\s*[-*]\s+\*\*\[([a-z][a-z0-9_:-]*)\]\*\*(.*)$", re.M)
PLACEHOLDER = re.compile(r"<(?:Review title|path|YYYY-MM-DD|short name|key|doi)>|"
                         r"\bTODO\b|\bTBD\b|lorem ipsum", re.I)


def split_sections(text):
    """Return {number: (heading, body)} for '## N. Name' headings."""
    out, cur, buf = {}, None, []
    for line in text.splitlines():
        m = re.match(r"^##\s+(\d+)\.\s+(.*)$", line)
        if m:
            if cur:
                out[cur[0]] = (cur[1], "\n".join(buf))
            cur, buf = (int(m.group(1)), m.group(2).strip()), []
        elif cur:
            buf.append(line)
    if cur:
        out[cur[0]] = (cur[1], "\n".join(buf))
    return out


def table_headers(body):
    return [ln.lower() for ln in body.splitlines()
            if ln.strip().startswith("|") and not re.match(r"^\s*\|[\s|:-]+\|\s*$", ln)]


def has_table_with(body, cols):
    for hdr in table_headers(body):
        if all(c in hdr for c in cols):
            return []
    best = max(table_headers(body) or [""], key=lambda h: sum(c in h for c in cols))
    return [c for c in cols if c not in best]


def prose_lines(text):
    """Lines outside code fences and tables, with inline code removed."""
    fence = False
    for i, ln in enumerate(text.splitlines(), 1):
        if ln.strip().startswith("```"):
            fence = not fence
            continue
        if fence or ln.strip().startswith("|"):
            continue
        yield i, re.sub(r"`[^`]*`", "", ln)


def check(text, ledger=None, search_log=None):
    """search_log: {search_id: purpose} or None."""
    errs, warns = [], []
    secs = split_sections(text)
    for num, kw in SECTIONS:
        if num not in secs or kw not in secs[num][0].lower():
            errs.append(f"E01 missing section '## {num}. ...' containing '{kw}'")

    body = lambda n: secs.get(n, ("", ""))[1]
    miss = has_table_with(body(10), GAP_COLS)
    if miss:
        errs.append(f"E02 Sec. 10 gap matrix lacks columns: {', '.join(miss)}")
    miss = has_table_with(body(11), NOV_COLS)
    if miss:
        errs.append(f"E02 Sec. 11 novelty table lacks columns: {', '.join(miss)}")

    gaps = re.split(r"^###\s+(G\d+)\b", body(9), flags=re.M)
    cat_count, conf_count = {}, {}
    if len(gaps) < 3:
        errs.append("E03 Sec. 9 has no gap records ('### G1: ...')")
    for gid, rec in zip(gaps[1::2], gaps[2::2]):
        low = rec.lower()
        ex = re.search(r"\*\*examined:\*\*\s*(.+)", low)
        qids = {q.upper() for q in re.findall(r"\bq\d{3}\b", ex.group(1))} if ex else set()
        if not qids:
            warns.append(f"W07 {gid} has no **Examined:** line with search ids (Q###)")
        elif search_log is not None:
            unknown = sorted(qids - set(search_log))
            if unknown:
                errs.append(f"E09 {gid} cites search ids not in the search log: {', '.join(unknown)}")
            if not any("counterevidence" in search_log.get(q, "").lower() for q in qids):
                warns.append(f"W07 {gid}: none of {', '.join(sorted(qids))} was logged with a 'counterevidence' purpose")
        for f in FIELDS:
            if not re.search(rf"\*\*{f}\.\s", rec):
                errs.append(f"E03 {gid} lacks field **{f}. ...**")
        cat = re.search(r"\*\*category:\*\*\s*(.+)", low)
        val = next((c for c in CATEGORIES if cat and c in cat.group(1)), None)
        if not val:
            errs.append(f"E03 {gid} Category missing or not one of the five categories")
        cat_count[val] = cat_count.get(val, 0) + 1
        h = re.search(r"\*\*h\.[^*]*\*\*\s*(.+)", low)
        conf = next((c for c in CONFIDENCE if h and h.group(1).lstrip(" *").startswith(c)), None)
        if not conf:
            errs.append(f"E03 {gid} H. confidence must start with one of: {', '.join(CONFIDENCE)}")
        conf_count[conf] = conf_count.get(conf, 0) + 1
        i = re.search(r"\*\*i\.[^*]*\*\*\s*(.+)", low)
        if not (i and any(i.group(1).lstrip(" *").startswith(r) for r in RISK)):
            errs.append(f"E03 {gid} I. novelty risk must start with Low, Medium, or High")
        j = re.search(r"\*\*j\.[^*]*\*\*\s*(.+)", low)
        if not (j and any(j.group(1).lstrip(" *").startswith(r) for r in RELATION)):
            errs.append(f"E03 {gid} J. must start with Addressed, Partially addressed, or Unresolved")

    verified = {m.group(1): m.group(2) for m in ENTRY.finditer(body(15))}
    unverified = {m.group(1) for m in ENTRY.finditer(body(16))}
    for k in sorted(set(verified) & unverified):
        errs.append(f"E08 [{k}] listed in both Sec. 15 and Sec. 16")
    status_count = {}
    for k, rest in verified.items():
        st = re.search(r"Status:\s*(VERIFIED-QUALIFIED|VERIFIED)\b", rest)
        if not st:
            errs.append(f"E05 [{k}] Sec. 15 entry lacks 'Status: VERIFIED' or 'VERIFIED-QUALIFIED'")
        else:
            status_count[st.group(1)] = status_count.get(st.group(1), 0) + 1
        if not re.search(r"https?://\S+", rest):
            errs.append(f"E05 [{k}] Sec. 15 entry lacks a DOI link or stable URL")
        if not re.search(r"Peer review:\s*\w", rest):
            errs.append(f"E05 [{k}] Sec. 15 entry lacks 'Peer review: <label>'")
        if not re.search(r"Access:\s*(FULLTEXT|ABSTRACT|METADATA)", rest):
            errs.append(f"E05 [{k}] Sec. 15 entry lacks 'Access: FULLTEXT|ABSTRACT|METADATA'")

    cited = {}
    for n, (_, b) in secs.items():
        if n in (15, 16):
            continue
        for m in CITE.finditer(b):
            for k in re.split(r"\s*[;,]\s*", m.group(1)):
                cited.setdefault(k, n)
    for k, n in sorted(cited.items()):
        if k not in verified and k not in unverified:
            errs.append(f"E04 [{k}] cited (first in Sec. {n}) but has no Sec. 15 or 16 entry")
        elif k in unverified:
            warns.append(f"W03 [{k}] cited in Sec. {n} but only listed as unverified")
    for k in sorted(set(verified) - set(cited)):
        warns.append(f"W02 [{k}] in Sec. 15 but never cited in the body")

    for i, ln in prose_lines(text):
        if PLACEHOLDER.search(ln):
            errs.append(f"E06 line {i}: placeholder left: {ln.strip()[:70]}")
        noquote = re.sub(r'"[^"]*"', "", ln)
        for m in OVERCLAIM.finditer(noquote):
            warns.append(f"W01 line {i}: overclaim wording '{m.group(0)}'")
        if "—" in ln or ";" in re.sub(r"\[[^\]]*\]", "", ln):
            warns.append(f"W04 line {i}: em dash or semicolon in prose")
        if re.search(r"systematic review|prisma", ln, re.I):
            warns.append(f"W05 line {i}: systematic-review wording, confirm it is a disclaimer")
    if re.search(r"fully verified", text, re.I) and unverified:
        warns.append("W06 'fully verified' appears while Sec. 16 lists unverified sources")

    if ledger:
        with open(ledger, newline="", encoding="utf-8-sig") as fh:
            rows = {r["source_id"]: r for r in csv.DictReader(fh)}
        for k, rest in verified.items():
            r = rows.get(k)
            if not r or r.get("verification_status") not in ("VERIFIED", "VERIFIED-QUALIFIED"):
                errs.append(f"E07 [{k}] not VERIFIED/VERIFIED-QUALIFIED in the ledger")
                continue
            doi = (r.get("doi") or "").lower().strip()
            if doi and doi not in rest.lower():
                errs.append(f"E07 [{k}] ledger DOI {doi} not in its Sec. 15 entry")
        venue = {"open": 0, "closed": 0, "unknown": 0}
        for k in verified:
            v = (rows.get(k, {}).get("venue_access") or "unknown").strip() or "unknown"
            venue[v if v in venue else "unknown"] += 1
        known = venue["open"] + venue["closed"]
        share = round(100 * venue["closed"] / known) if known else None
        if share is not None and not 40 <= share <= 60:
            warns.append(f"W08 closed-access venues are {share}% of Sec. 15 (target about 50%, band 40-60%)")
        if venue["unknown"]:
            warns.append(f"W08 {venue['unknown']} Sec. 15 sources have no venue_access in the ledger")

    summary = {
        "verified_refs": status_count.get("VERIFIED", 0),
        "qualified_refs": status_count.get("VERIFIED-QUALIFIED", 0),
        "unverified_refs": len(unverified),
        "gaps_by_category": {k: v for k, v in cat_count.items() if k},
        "gaps_by_confidence": {k: v for k, v in conf_count.items() if k},
        "cited_keys": len(cited),
    }
    if ledger:
        summary["venue_split"] = {**venue, "closed_share_pct": share}
    return errs, warns, summary


GOOD = """# R
## 1. Title and Review Metadata
x
## 2. Executive Summary
Agents help [wang2026epanet].
## 3. Understanding the Original Manuscript
x
## 4. Review Scope and Methodology
x
## 5. Background and Conceptual Foundations
x
## 6. Comprehensive Thematic Literature Review
Leak work [mu2026leakagent; wang2026epanet].
## 7. Critical Comparison of Existing Approaches
x
## 8. Established Knowledge and Solved Problems
x
## 9. Evidence-Based Research Gaps
### G1: trust
- **Category:** Context-dependent gap
- **A. Gap statement:** a
- **B. Supporting evidence:** b
- **C. Counterevidence:** c
- **D. Existing solutions:** d
- **E. Residual uncertainty:** e
- **F. Research significance:** f
- **G. Potential research direction:** g
- **H. Verification confidence:** Moderately supported because h
- **I. Novelty risk:** Medium because i
- **J. Relationship to the manuscript:** Partially addressed
- **K. Appropriate claim boundary:** k
- **Examined:** wang2026epanet. Searches Q001, Q002.
## 10. Research-Gap Evidence Matrix
| Candidate gap | Supporting studies | Counterevidence or existing solutions | Remaining unresolved issue | Relevance to manuscript | Confidence | Novelty risk |
|---|---|---|---|---|---|---|
## 11. Novelty and Contribution Assessment
| Manuscript claim | Closest related work | Verified similarities | Potentially distinctive aspect | Evidence required | Current assessment |
|---|---|---|---|---|---|
## 12. Recommended Research Directions
x
## 13. Implications for the Existing Manuscript
x
## 14. Limitations of This Literature Review
x
## 15. Complete Verified References
- **[wang2026epanet]** W. (2026). T. *V*. https://doi.org/10.1/x. Status: VERIFIED | Peer review: peer-reviewed | Access: FULLTEXT
## 16. Unverified Sources and Open Questions
- **[mu2026leakagent]** M. Problem: no record.
## 17. Reproducibility Appendix
x
"""


def selftest():
    e, w, s = check(GOOD)
    assert e == [], e
    assert any(x.startswith("W03 [mu2026leakagent]") for x in w), w
    assert s["verified_refs"] == 1 and s["unverified_refs"] == 1, s
    assert s["gaps_by_category"] == {"context-dependent gap": 1}, s
    bad = (GOOD.replace("## 11. Novelty", "## 11. Nov")
               .replace("- **K. Appropriate claim boundary:** k\n", "")
               .replace("Status: VERIFIED", "Status: PENDING")
               .replace("Agents help", "We are the first to show agents help [smith2020x]"))
    e, w, _ = check(bad)
    for code in ("E01", "E03", "E04", "E05"):
        assert any(x.startswith(code) for x in e), (code, e)
    assert any(x.startswith("W01") for x in w), w
    e, w, _ = check(GOOD, search_log={"Q001": "counterevidence G1"})
    assert any(x.startswith("E09") for x in e), e
    e, w, _ = check(GOOD, search_log={"Q001": "competitors", "Q002": "x"})
    assert not e and any(x.startswith("W07") for x in w), (e, w)
    print("selftest passed")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("review", nargs="?")
    ap.add_argument("--ledger")
    ap.add_argument("--search-log")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not a.review:
        ap.error("review path required")
    with open(a.review, encoding="utf-8") as fh:
        text = fh.read()
    log = None
    if a.search_log:
        with open(a.search_log, newline="", encoding="utf-8-sig") as fh:
            log = {r["search_id"]: r.get("purpose", "") for r in csv.DictReader(fh)}
    errs, warns, summary = check(text, a.ledger, log)
    for x in errs:
        print("ERROR", x)
    for x in warns:
        print("WARN ", x)
    print("SUMMARY", summary)
    print(f"{len(errs)} errors, {len(warns)} warnings")
    sys.exit(1 if errs else 0)


if __name__ == "__main__":
    main()
