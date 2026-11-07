"""Release checks for the public collection: the published file set, exclusions, privacy rules, and counts."""
from __future__ import annotations

import importlib
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import generate_catalog  # noqa: E402
from validate_skills import PRIVATE_TERMS, user_supplied_files, validate_privacy, validate_repo  # noqa: E402

EXPECTED_SKILL_COUNT = 22                       # release 1.0.0; change together with the CATALOG table
EXCLUDED_SKILLS = ("remove-ai-marks",)          # not part of the public collection
LOCAL_ONLY = ("RELEASE_COMMIT_PLAN.md", "MANUAL_RELEASE_CHECKLIST.md", ".release-review/")
ASD_RESTRICTED = ("skills/asd-ste100/references/ASD-STE100_ISSUE9.pdf",
                  "skills/asd-ste100/references/STE-ISSUE9-REFERENCE-GUIDE.md")
GOOD_DESC = "Checks a thing in research manuscripts. Use when the user asks to check that thing."
GIT = shutil.which("git")
needs_git = pytest.mark.skipif(GIT is None, reason="git is not installed")


def _git_env() -> dict:
    # Ignore the user's global and system Git settings, so that only the repository's .gitignore counts.
    return {**os.environ, "GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_NOSYSTEM": "1"}


def public_files(root: Path, scratch: Path) -> list[str]:
    """Files that `git add -A` would take from `root` in a fresh repository. Uses a throwaway bare Git directory, so
    it never writes to `root` and never reads a repository that encloses it."""
    git_dir = scratch / "probe.git"
    subprocess.run([GIT, "init", "-q", "--bare", str(git_dir)], check=True, env=_git_env())
    out = subprocess.run([GIT, f"--git-dir={git_dir}", f"--work-tree={root}", "ls-files", "--others",
                          "--exclude-standard", "-z"], check=True, capture_output=True, env=_git_env()).stdout
    return sorted(p for p in out.decode("utf-8").split("\0") if p)


def skill_folders() -> list[str]:
    return sorted(p.name for p in (ROOT / "skills").iterdir() if (p / "SKILL.md").is_file())


# --- the public collection -----------------------------------------------------------------------------------------

def test_all_expected_public_skills_are_present():
    assert skill_folders() == sorted(generate_catalog.CATALOG)
    assert len(skill_folders()) == EXPECTED_SKILL_COUNT
    assert validate_repo(ROOT)[1] == skill_folders()


def test_excluded_skill_is_not_in_the_public_collection():
    public_docs = [ROOT / "README.md", ROOT / "CHANGELOG.md", ROOT / "SECURITY.md", ROOT / "CONTRIBUTING.md",
                   *sorted((ROOT / "docs").glob("*.md")), *sorted((ROOT / ".claude-plugin").glob("*.json")),
                   *sorted((ROOT / ".github").rglob("*.yml"))]
    for name in EXCLUDED_SKILLS:
        assert not (ROOT / "skills" / name).exists()
        assert name not in generate_catalog.CATALOG
        for doc in public_docs:
            assert name not in doc.read_text(encoding="utf-8"), f"{doc.relative_to(ROOT)} mentions {name}"
        for md in (ROOT / "skills").glob("*/SKILL.md"):
            assert name not in md.read_text(encoding="utf-8"), f"{md.relative_to(ROOT)} mentions {name}"


def test_catalog_readme_and_filesystem_counts_agree():
    n = len(skill_folders())
    catalog = (ROOT / "docs" / "SKILLS_CATALOG.md").read_text(encoding="utf-8")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert f"**{n} skills**" in catalog
    assert f"**{n} skills**" in readme
    table = readme.split(generate_catalog.README_START)[1].split(generate_catalog.README_END)[0]
    assert len(re.findall(r"^\| \[`", table, flags=re.M)) == n
    assert len(re.findall(r"^\| \[`", catalog, flags=re.M)) == n


def test_plugin_discovers_exactly_the_public_collection():
    plugin = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
    market = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))
    # Claude Code scans <plugin root>/skills/ unless plugin.json overrides it.
    assert plugin.get("skills") in (None, "./skills", "./skills/")
    assert [e["source"] for e in market["plugins"]] == ["./"]
    assert plugin.get("license") == "CC-BY-4.0"
    assert skill_folders() == sorted(generate_catalog.CATALOG)


def test_every_skill_resource_path_resolves():
    issues = validate_repo(ROOT)[0]
    assert [str(i) for i in issues if "does not exist" in i.message or "sibling skill" in i.message] == []


# --- local-only and restricted material ----------------------------------------------------------------------------

@needs_git
def test_local_only_release_files_are_git_ignored(tmp_path):
    work = tmp_path / "work"
    work.mkdir()
    shutil.copy(ROOT / ".gitignore", work / ".gitignore")
    paths = ["RELEASE_COMMIT_PLAN.md", "MANUAL_RELEASE_CHECKLIST.md", ".release-review/notes.md",
             ".release-review/excluded-skills/demo/SKILL.md", *ASD_RESTRICTED]
    for p in paths:
        (work / p).parent.mkdir(parents=True, exist_ok=True)
        (work / p).write_text("x\n", encoding="utf-8")
    subprocess.run([GIT, "init", "-q", str(work)], check=True, env=_git_env())
    for p in paths:
        r = subprocess.run([GIT, "-C", str(work), "check-ignore", "-q", p], env=_git_env())
        assert r.returncode == 0, f"{p} is not ignored by .gitignore"


@needs_git
def test_public_tree_has_no_private_restricted_or_generated_files(tmp_path):
    files = public_files(ROOT, tmp_path)
    assert "LICENSE" in files and "skills/asd-ste100/REFERENCES.md" in files
    bad = [f for f in files if f in LOCAL_ONLY or f.startswith(".release-review/") or f in ASD_RESTRICTED
           or any(f"skills/{s}/" in f for s in EXCLUDED_SKILLS)
           or re.search(r"(^|/)(__pycache__|\.mypy_cache|\.ruff_cache|\.pytest_cache|node_modules|\.venv)/", f)]
    assert bad == []
    assert sorted({f.split("/")[1] for f in files if f.startswith("skills/")}) == skill_folders()


def test_asd_reference_material_is_user_supplied(monkeypatch, tmp_path):
    assert set(ASD_RESTRICTED) <= user_supplied_files(ROOT)
    skill = (ROOT / "skills" / "asd-ste100" / "SKILL.md").read_text(encoding="utf-8")
    assert "ASD_STE100_PDF" in skill and "REFERENCES.md" in skill
    assert (ROOT / "skills" / "asd-ste100" / "REFERENCES.md").is_file()
    # The script takes its PDF location from ASD_STE100_PDF when the variable is set.
    monkeypatch.syspath_prepend(str(ROOT / "skills" / "asd-ste100" / "scripts"))
    monkeypatch.setenv("ASD_STE100_PDF", str(tmp_path / "user-copy.pdf"))
    ste_tool = importlib.reload(importlib.import_module("ste_tool"))
    assert ste_tool.PDF == tmp_path / "user-copy.pdf"
    with pytest.raises(SystemExit, match="Supply your own authorized copy"):
        ste_tool._open()


def test_private_denylist_terms_are_absent_from_public_files():
    if not (ROOT / PRIVATE_TERMS).is_file() and not os.environ.get("PRIVATE_TERMS_FILE"):
        pytest.skip("no private denylist on this machine (it is never published)")
    assert [str(i) for i in validate_repo(ROOT)[0] if "private denylist" in i.message] == []


# --- the privacy rules of the validator, on fixtures ---------------------------------------------------------------

def _privacy_fixture(tmp_path: Path, body: str, extra: dict[str, bytes] | None = None) -> list[str]:
    d = tmp_path / "skills" / "demo"
    d.mkdir(parents=True)
    (d / "SKILL.md").write_text(f"---\nname: demo\ndescription: {GOOD_DESC}\n---\n{body}\n", encoding="utf-8")
    for rel, data in (extra or {}).items():
        (tmp_path / rel).parent.mkdir(parents=True, exist_ok=True)
        (tmp_path / rel).write_bytes(data)
    return [f"{i.path}: {i.message}" for i in validate_privacy(tmp_path, user_supplied_files(tmp_path))]


# The fixtures are assembled at run time so that this file itself passes the privacy rules it tests.
@pytest.mark.parametrize("body, expected", [
    ("Run C:" + "\\Users\\Bob Smith\\proj\\x.py.", "personal machine path"),
    ("See /ho" + "me/bobsmith/work/x.", "personal machine path"),
    ("Mail a.person" + "@" + "university.edu for access.", "e-mail address"),
])
def test_privacy_rules_flag_personal_data(tmp_path, body, expected):
    assert any(expected in e for e in _privacy_fixture(tmp_path, body))


@pytest.mark.parametrize("body", [
    "Quote paths such as C:/Users/<name>/proj or C:/Users/Jane Doe/proj.",
    "Write to name@example.com. CI runs in /home/runner/work.",
])
def test_privacy_rules_allow_placeholders(tmp_path, body):
    assert _privacy_fixture(tmp_path, body) == []


def test_privacy_rules_flag_undeclared_documents(tmp_path):
    found = _privacy_fixture(tmp_path, "Body.", {"skills/demo/references/standard.pdf": b"%PDF-1.4"})
    assert any("document or archive" in e for e in found)
    (tmp_path / ".gitignore").write_text("skills/demo/references/standard.pdf\n", encoding="utf-8")
    assert [i for i in validate_privacy(tmp_path, user_supplied_files(tmp_path)) if "document" in i.message] == []


def test_privacy_denylist_matches_whole_words_and_never_prints_the_term(tmp_path, monkeypatch):
    terms = tmp_path / ".release-review" / "terms.txt"   # local-only folder, as in the real repository
    terms.parent.mkdir()
    terms.write_text("# comment\nzorbaproject\n", encoding="utf-8")
    monkeypatch.setenv("PRIVATE_TERMS_FILE", str(terms))
    found = _privacy_fixture(tmp_path, "Results of the ZorbaProject pilot.")
    assert any("private denylist" in e for e in found)
    assert not any("zorbaproject" in e.lower() for e in found)
    (tmp_path / "skills" / "demo" / "SKILL.md").write_text(
        f"---\nname: demo\ndescription: {GOOD_DESC}\n---\nThe zorbaprojects word is longer.\n", encoding="utf-8")
    assert [i for i in validate_privacy(tmp_path) if "denylist" in i.message] == []


# --- the synthetic highlighting example ----------------------------------------------------------------------------

def test_highlighted_pdf_example_builds_and_passes_its_strip_check(tmp_path):
    skill = ROOT / "skills" / "highlighted-pdf-from-reviews"
    shutil.copytree(skill / "examples" / "demo", tmp_path / "demo")
    r = subprocess.run([sys.executable, "-B", str(skill / "examples" / "example_build.py"), str(tmp_path / "demo")],
                       capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr
    assert "strip check passed" in r.stdout
    assert (tmp_path / "demo" / "Example_Highlighted.tex").is_file()
    assert not (skill / "examples" / "demo" / "Example_Highlighted.tex").exists()
