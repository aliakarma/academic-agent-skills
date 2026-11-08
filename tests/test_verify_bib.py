"""Offline tests for skills/reference-verify/scripts/verify_bib.py and its Colab notebook. No network access:
registry lookups are replaced by hand-built records."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "skills" / "reference-verify" / "scripts" / "verify_bib.py"
NOTEBOOK = ROOT / "notebook" / "BibTeX_DOI_Verifier.ipynb"


@pytest.fixture()
def vb(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)                       # reports and caches land in tmp_path
    spec = importlib.util.spec_from_file_location("verify_bib", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.USE_CACHE = False
    mod.CHECK_URLS = False
    monkeypatch.setattr(mod, "_throttle", lambda url: None)
    monkeypatch.setattr(mod.time, "sleep", lambda s: None)
    return mod


def record(vb, source, identity, score, **fields):
    r = vb.blank_record(source)
    r.update(fields, identity=identity, score=score)
    return r


ENTRY = {"ENTRYTYPE": "article", "ID": "he2016", "title": "Deep residual learning for image recognition",
         "author": "He, Kaiming and Zhang, Xiangyu", "journal": "Pattern Recognition Letters",
         "year": "2016", "volume": "12", "doi": "10.1000/abc"}
TITLE = ENTRY["title"]


def verdicts(rows, field):
    return [r["verdict"] for r in rows if r["field"] == field]


# --- text helpers --------------------------------------------------------------------------------------------------

def test_text_helpers(vb):
    assert vb.latex_to_text(r"M{\"u}ller \& Sons") == "Müller & Sons"
    assert vb.clean_doi("https://doi.org/10.1000/ABC.") == "10.1000/ABC"
    assert vb.clean_doi("not a doi") is None
    assert vb.norm_pages("12 – 15") == "12--15"
    assert vb.parse_name("Ludwig van Beethoven") == ("van Beethoven", "Ludwig")
    assert vb.same_person(("McMahan", "H. Brendan"), ("McMahan", "Brendan"))


@pytest.mark.parametrize("a, b, same", [
    ("ICML", "International Conference on Machine Learning", True),
    ("IEEE Commun. Mag.", "IEEE Communications Magazine", True),
    ("Nature", "Science", False),
])
def test_container_equiv(vb, a, b, same):
    assert vb.container_equiv(a, b) is same


# --- decision rules ------------------------------------------------------------------------------------------------

def test_one_record_never_replaces_a_whole_author_list(vb):
    doi_rec = record(vb, "CrossRef", "doi", 1.0, title=TITLE, doi="10.1000/abc", type="journal-article",
                     authors=[("Ren", "Shaoqing"), ("Sun", "Jian")], year=2016)
    rows = vb.compare(dict(ENTRY), [doi_rec], doi_rec)
    assert verdicts(rows, "author") == ["REVIEW"]


def test_disagreeing_registries_give_review_not_a_fix(vb):
    a = record(vb, "CrossRef", "doi", 1.0, title=TITLE, doi="10.1000/abc", type="journal-article", volume="13")
    b = record(vb, "OpenAlex", "doi", 1.0, title=TITLE, doi="10.1000/abc", type="journal-article", volume="14")
    rows = vb.compare(dict(ENTRY), [a, b], a)
    assert verdicts(rows, "volume") == ["REVIEW"]
    single = vb.compare(dict(ENTRY), [a], a)
    assert verdicts(single, "volume") == ["WRONG"]


def test_same_title_by_other_authors_never_donates(vb):
    # Found live: a 2025 book chapter titled "Attention Is All You Need" offered its DOI, year and pages for the
    # 2017 NeurIPS paper. A title match by different people is a different work.
    entry = {"ENTRYTYPE": "inproceedings", "ID": "vaswani2017", "title": "Attention is All you Need",
             "author": "Vaswani, Ashish and Shazeer, Noam", "year": "2017"}
    chapter = record(vb, "OpenAlex", "title", 1.0, title="Attention Is All You Need", type="book-chapter",
                     doi="10.1201/9781003561460-19", year=2025, pages="151-163",
                     authors=[("Bishop", "J. M."), ("Seiberth", "Gabriel")])
    authority, _ = vb.pick_authority(entry, [chapter])
    assert authority is None
    rows = vb.compare(entry, [chapter], authority)
    assert not [r for r in rows if r["verdict"] in ("ADD", "WRONG", "FIX") and r["suggested"]]


def test_search_outage_is_reported_not_read_as_no_match(vb, monkeypatch):
    monkeypatch.setattr(vb, "http_get", lambda url, *a, **k: ("error", None) if "dblp" in url else ("ok", {}))
    _, notes = vb.resolve({"title": "A long distinctive title for testing", "author": "Doe, Jane"})
    assert notes == ["dblp_search unreachable"]


def test_preprint_never_donates_venue_fields(vb):
    pre = record(vb, "DBLP", "title", 1.0, title=TITLE, type="posted-content", container="CoRR",
                 volume="abs/1512.03385")
    rows = vb.compare(dict(ENTRY), [pre], pre)
    assert verdicts(rows, "volume") == ["UNCHECKED"]


def test_retraction_is_flagged_only_for_identity_confirmed_records(vb):
    retracted = record(vb, "CrossRef", "doi", 1.0, title=TITLE, doi="10.1000/abc", type="journal-article",
                       retracted="retraction")
    rows = vb.compare(dict(ENTRY), [retracted], retracted)
    assert verdicts(rows, "_retraction") == ["RETRACTED"]
    other = record(vb, "OpenAlex", "title", 0.80, title=TITLE + " revisited", retracted="retraction")
    assert verdicts(vb.compare(dict(ENTRY), [other], other), "_retraction") == []


def test_crossref_updated_by_sets_retracted(vb):
    rec = vb._cr_record({"DOI": "10.1000/abc", "title": ["T"],
                         "updated-by": [{"type": "retraction", "DOI": "10.1000/r"}]})
    assert rec["retracted"] == "retraction"
    assert vb._cr_record({"DOI": "10.1000/abc", "title": ["T"]})["retracted"] == ""


def test_mark_duplicates(vb):
    results = [{"key": k, "entry": {"doi": d, "title": t}, "status": "CLEAN", "fields": []}
               for k, d, t in (("a", "10.1/X", "One"), ("b", "10.1/x", "Two"),
                               ("c", "", "A long distinctive title here"),
                               ("d", "", "A long distinctive title here!"), ("e", "", "Short"))]
    vb.mark_duplicates(results)
    flagged = {r["key"]: r["fields"][0]["evidence"] for r in results if r["fields"]}
    assert set(flagged) == {"a", "b", "c", "d"}
    assert "b (same DOI)" in flagged["a"] and "d (same title)" in flagged["c"]
    assert results[0]["status"] == "REVIEW"


# --- HTTP layer ----------------------------------------------------------------------------------------------------

class FakeResponse:
    def __init__(self, code, payload=None):
        self.status_code, self._payload, self.text = code, payload, ""

    def json(self):
        return self._payload

    def close(self):
        pass


@pytest.mark.parametrize("code, expected", [(200, "OK"), (202, "OK"), (418, "BLOCKED"), (403, "BLOCKED"),
                                            (404, "DEAD")])
def test_check_url_bot_blocks_are_not_dead_links(vb, monkeypatch, code, expected):
    monkeypatch.setattr(vb.requests, "get", lambda *a, **k: FakeResponse(code))
    assert vb.check_url("https://example.org/paper").startswith(expected)


def test_cache_keeps_successes_only_and_expires(vb, monkeypatch):
    vb.USE_CACHE = True
    calls = []

    def fake_get(url, **kw):
        calls.append(url)
        return FakeResponse(404) if "missing" in url else FakeResponse(200, {"ok": 1})

    monkeypatch.setattr(vb.requests, "get", fake_get)
    assert vb.http_get("https://example.org/found") == ("ok", {"ok": 1})
    assert vb.http_get("https://example.org/found") == ("ok", {"ok": 1})
    assert vb.http_get("https://example.org/missing")[0] == "not_found"
    assert vb.http_get("https://example.org/missing")[0] == "not_found"
    assert calls.count("https://example.org/found") == 1          # cached
    assert calls.count("https://example.org/missing") == 2        # a 404 is asked again
    for v in vb._cache.values():
        v[2] -= (vb.CACHE_TTL_DAYS + 1) * 86400
    vb.http_get("https://example.org/found")
    assert calls.count("https://example.org/found") == 2          # expired


# --- writing the .bib ----------------------------------------------------------------------------------------------

BIB = """@string{jmlr = "Journal of Machine Learning Research"}

% my own note, kept as written
@article{smith2020,
  author    = {Smith, John and Doe, Jane},
  title     = {A {Study} of Things, Part {II}},
  journal   = jmlr,
  year      = 2020,
  pages     = "1-10",
}

@inproceedings(lee2019,
  title = {Nested {B}races},
  booktitle = {Proc. X}
)
"""


def test_patch_touches_only_the_changed_values(vb):
    out = vb.patch_bib_text(BIB, [
        {"key": "smith2020", "field": "year", "after": "2021"},
        {"key": "smith2020", "field": "pages", "after": "1--10"},
        {"key": "smith2020", "field": "doi", "after": "10.1000/xyz"},
        {"key": "lee2019", "field": "year", "after": "2019"},
    ])
    assert out.startswith('@string{jmlr = "Journal of Machine Learning Research"}\n\n% my own note, kept as written')
    assert "  journal   = jmlr,\n  year      = {2021},\n  pages     = {1--10},\n  doi = {10.1000/xyz}\n}" in out
    assert "  booktitle = {Proc. X},\n  year = {2019}\n)" in out
    assert vb.patch_bib_text(BIB, []) == BIB


def write_results(vb, path):
    db = vb.load_bib(str(path))
    entries = {e["ID"]: e for e in db.entries}
    results = [
        {"key": "smith2020", "entry": entries["smith2020"], "status": "REVIEW", "sources": ["CrossRef"],
         "notes": [], "degraded": False,
         "fields": [{"field": "year", "verdict": "WRONG", "current": "2020", "suggested": "2021",
                     "evidence": "CrossRef says 2021"},
                    {"field": "author", "verdict": "REVIEW", "current": "x", "suggested": "y",
                     "evidence": "CrossRef: given-name variant"}]},
        {"key": "lee2019", "entry": entries["lee2019"], "status": "CLEAN", "sources": ["DBLP"],
         "notes": [], "degraded": False, "fields": []},
    ]
    return db, results


def test_apply_writes_backup_annotations_and_is_idempotent(vb, tmp_path):
    bib = tmp_path / "refs.bib"
    bib.write_text(BIB, encoding="utf-8")
    vb.ANNOTATE_BIB = True
    db, results = write_results(vb, bib)
    vb.apply_corrections(results, db, str(bib))
    first = bib.read_text(encoding="utf-8")
    assert (tmp_path / "refs.bib.orig.bak").read_text(encoding="utf-8") == BIB
    assert "  year      = {2021},\n  pages     = {1--10},\n" in first      # correction + dash normalization
    assert "% bibverify: [CHECK] smith2020" in first
    assert "[CHECK] lee2019" not in first                                  # CLEAN entries get no comment
    assert "journal   = jmlr," in first and "% my own note, kept as written" in first
    assert (tmp_path / "refs_applied_corrections.csv").is_file()

    db, results = write_results(vb, bib)                                   # second run: no pile-up
    assert vb.apply_corrections(results, db, str(bib)) == []               # 2021 is already there
    second = bib.read_text(encoding="utf-8")
    assert second.count("[CHECK] smith2020") == 1 and second.count("Verified with") == 1
    assert vb.strip_annotations(second) == vb.strip_annotations(first)
    assert (tmp_path / "refs.bib.orig.bak").read_text(encoding="utf-8") == BIB


def test_outage_writes_formatting_fixes_only(vb, tmp_path):
    bib = tmp_path / "refs.bib"
    bib.write_text(BIB, encoding="utf-8")
    db, results = write_results(vb, bib)
    results[0]["degraded"], results[0]["notes"] = True, ["dblp_search unreachable"]
    applied = vb.apply_corrections(results, db, str(bib))
    assert [(a["field"], a["after"]) for a in applied] == [("pages", "1--10")]
    text = bib.read_text(encoding="utf-8")
    assert "year      = 2020," in text and "[REVIEW] author" in text


def test_missing_authors_are_appended_not_rewritten(vb):
    entry = dict(ENTRY, author="Wakefield, A. J. and Murch, S. H.")
    rec = record(vb, "CrossRef", "doi", 1.0, title=TITLE, doi="10.1000/abc", type="journal-article",
                 authors=[("Wakefield", "AJ"), ("Murch", "SH"), ("Anthony", "A")])
    fix = [r for r in vb.compare(entry, [rec], rec) if r["field"] == "author"][0]
    assert fix["verdict"] == "FIX"
    assert fix["suggested"] == "Wakefield, A. J. and Murch, S. H. and Anthony, A"


# --- command line --------------------------------------------------------------------------------------------------

def test_missing_file_is_an_error_not_a_fallback(vb, tmp_path):
    (tmp_path / "references.bib").write_text(BIB, encoding="utf-8")
    with pytest.raises(FileNotFoundError):
        vb.main(["typo.bib"])


def test_report_only_by_default(vb, tmp_path, monkeypatch):
    bib = tmp_path / "refs.bib"
    bib.write_text(BIB, encoding="utf-8")
    monkeypatch.setattr(vb, "resolve", lambda entry: ([], []))
    out = vb.main(vb._parse_cli([str(bib), "--no-urls"]))
    assert bib.read_text(encoding="utf-8") == BIB
    assert not (tmp_path / "refs.bib.orig.bak").exists()
    assert {r["status"] for r in out[0][1]} == {"UNVERIFIED"}
    assert (tmp_path / "verification_report.md").is_file()


# --- notebook ------------------------------------------------------------------------------------------------------

def test_notebook_is_committed_without_outputs():
    nb = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
    for cell in nb["cells"]:
        if cell["cell_type"] == "code":
            assert cell.get("outputs") == [] and cell.get("execution_count") is None
    code = "\n".join("".join(c["source"]) for c in nb["cells"] if c["cell_type"] == "code")
    assert "verify_bib.py" in code and "def compare(" not in code       # thin wrapper, one copy of the logic
