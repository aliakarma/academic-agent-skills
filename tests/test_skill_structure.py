"""Tests for scripts/validate_skills.py and scripts/generate_catalog.py, on the real repository and on fixtures."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import generate_catalog  # noqa: E402
from validate_skills import parse_frontmatter, validate_repo  # noqa: E402

GOOD_DESC = "Checks a thing in research manuscripts. Use when the user asks to check that thing."


def make_skill(root: Path, folder: str, frontmatter: str | None, body: str = "# Title\n") -> Path:
    d = root / "skills" / folder
    d.mkdir(parents=True, exist_ok=True)
    text = body if frontmatter is None else f"---\n{frontmatter}\n---\n{body}"
    (d / "SKILL.md").write_text(text, encoding="utf-8")
    return d


def errors(root: Path) -> list[str]:
    return [f"{i.path}: {i.message}" for i in validate_repo(root)[0] if i.level == "ERROR"]


def warnings(root: Path) -> list[str]:
    return [i.message for i in validate_repo(root)[0] if i.level == "WARN"]


# --- the real repository -------------------------------------------------------------------------------------------

def test_repository_has_no_errors():
    assert errors(ROOT) == []


def test_every_skill_folder_is_discovered():
    folders = sorted(p.name for p in (ROOT / "skills").iterdir() if p.is_dir() and not p.name.startswith("."))
    assert validate_repo(ROOT)[1] == folders
    assert len(folders) >= 1


def test_catalog_and_readme_are_current():
    assert generate_catalog.main(["--check"]) == 0


def test_plugin_and_marketplace_names_agree():
    plugin = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
    market = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))
    assert [e["name"] for e in market["plugins"]] == [plugin["name"]]
    assert market["plugins"][0]["source"] == "./"


# --- expected-valid fixtures ---------------------------------------------------------------------------------------

def test_minimal_valid_skill(tmp_path):
    make_skill(tmp_path, "demo-skill", f"name: demo-skill\ndescription: {GOOD_DESC}")
    assert errors(tmp_path) == []


def test_claude_fields_and_existing_resources_are_allowed(tmp_path):
    d = make_skill(tmp_path, "demo-skill",
                   f"name: demo-skill\ndescription: {GOOD_DESC}\ndisable-model-invocation: true\n"
                   "license: MIT\nmetadata:\n  version: \"1.0\"",
                   body="Run `${CLAUDE_SKILL_DIR}/scripts/run.py` and read [guide](references/guide.md).\n")
    (d / "scripts").mkdir()
    (d / "scripts" / "run.py").write_text("print('ok')\n", encoding="utf-8")
    (d / "references").mkdir()
    (d / "references" / "guide.md").write_text("guide\n", encoding="utf-8")
    assert errors(tmp_path) == []
    assert any("Claude Code extension field" in w for w in warnings(tmp_path))


def test_folder_names_in_the_users_project_are_not_checked(tmp_path):
    # The skill has no templates/ folder, so `templates/out.tex` names a file the skill will create for the user.
    make_skill(tmp_path, "demo-skill", f"name: demo-skill\ndescription: {GOOD_DESC}", body="Write `templates/out.tex`.\n")
    assert errors(tmp_path) == []


def test_crlf_frontmatter_parses():
    fm, body = parse_frontmatter(f"---\r\nname: demo\r\ndescription: {GOOD_DESC}\r\n---\r\nbody\r\n")
    assert fm["name"] == "demo" and body.strip() == "body"


def test_gitignored_user_supplied_file_is_a_warning(tmp_path):
    make_skill(tmp_path, "demo-skill", f"name: demo-skill\ndescription: {GOOD_DESC}",
               body="Read `references/standard.pdf`.\n")
    (tmp_path / "skills" / "demo-skill" / "references").mkdir()
    (tmp_path / ".gitignore").write_text("skills/demo-skill/references/standard.pdf\n", encoding="utf-8")
    assert errors(tmp_path) == []
    assert any("user-supplied" in w for w in warnings(tmp_path))


# --- expected-invalid fixtures -------------------------------------------------------------------------------------

@pytest.mark.parametrize("folder, frontmatter, body, expected", [
    ("Bad", f"name: Bad\ndescription: {GOOD_DESC}", "", "must use lowercase"),
    ("a--b", f"name: a--b\ndescription: {GOOD_DESC}", "", "single hyphens"),
    ("-edge", f"name: -edge\ndescription: {GOOD_DESC}", "", "single hyphens"),
    ("other", f"name: demo\ndescription: {GOOD_DESC}", "", "must match its directory name"),
    ("demo", f"name: {'x' * 65}\ndescription: {GOOD_DESC}", "", "longer than 64"),
    ("demo", "name: demo", "", "missing required 'description'"),
    ("demo", f"description: {GOOD_DESC}", "", "missing required 'name'"),
    ("demo", f"name: demo\ndescription: {'x' * 1025}", "", "limit 1024"),
    ("demo", "name: demo\ndescription: [unclosed", "", "not valid YAML"),
    ("demo", f"name: demo\ndescription: {GOOD_DESC}\nmetadata:\n  sources:\n    - a", "", "'metadata' must map"),
    ("demo", f"name: demo\ndescription: {GOOD_DESC}\ncompatibility: {'x' * 501}", "", "'compatibility'"),
    ("demo", f"name: demo\ndescription: {GOOD_DESC}", "Run `python ~/.claude/skills/demo/x.py`.", "hard-coded install path"),
    ("demo", f"name: demo\ndescription: {GOOD_DESC}", "Use `${CLAUDE_SKILL_DIR}/../missing-skill/scripts/x.py`.", "sibling skill"),
])
def test_invalid_frontmatter_and_body(tmp_path, folder, frontmatter, body, expected):
    make_skill(tmp_path, folder, frontmatter, body=body)
    found = errors(tmp_path)
    assert any(expected in e for e in found), found
    assert all(e.startswith(f"skills/{folder}/") for e in found), "errors must name the affected skill and file"


def test_missing_frontmatter(tmp_path):
    make_skill(tmp_path, "demo", None, body="# No frontmatter\n")
    assert any("must start with a '---'" in e for e in errors(tmp_path))


def test_missing_referenced_script(tmp_path):
    d = make_skill(tmp_path, "demo", f"name: demo\ndescription: {GOOD_DESC}", body="Run `scripts/missing.py`.\n")
    (d / "scripts").mkdir()
    (d / "scripts" / "other.py").write_text("", encoding="utf-8")
    assert any("referenced file does not exist: scripts/missing.py" in e for e in errors(tmp_path))


def test_folder_without_skill_md(tmp_path):
    (tmp_path / "skills" / "empty-skill").mkdir(parents=True)
    assert any("has no SKILL.md" in e for e in errors(tmp_path))


def test_duplicate_names(tmp_path):
    make_skill(tmp_path, "demo", f"name: demo\ndescription: {GOOD_DESC}")
    make_skill(tmp_path, "demo-copy", f"name: demo\ndescription: {GOOD_DESC}")
    assert any("duplicate skill name 'demo'" in e for e in errors(tmp_path))


def test_broken_doc_link(tmp_path):
    make_skill(tmp_path, "demo", f"name: demo\ndescription: {GOOD_DESC}")
    (tmp_path / "README.md").write_text("See [the guide](docs/missing.md).\n", encoding="utf-8")
    assert any("broken link: docs/missing.md" in e for e in errors(tmp_path))


def _write_manifests(root: Path, plugin: dict, market: dict) -> None:
    (root / ".claude-plugin").mkdir(parents=True)
    (root / ".claude-plugin" / "plugin.json").write_text(json.dumps(plugin), encoding="utf-8")
    (root / ".claude-plugin" / "marketplace.json").write_text(json.dumps(market), encoding="utf-8")


@pytest.mark.parametrize("entry, expected", [
    ({"name": "demo-plugin", "source": "../elsewhere"}, "must start with './'"),
    ({"name": "demo-plugin", "source": "./nowhere"}, "does not exist"),
    ({"name": "another-name", "source": "./"}, "must match plugin.json"),
])
def test_invalid_manifests(tmp_path, entry, expected):
    make_skill(tmp_path, "demo", f"name: demo\ndescription: {GOOD_DESC}")
    _write_manifests(tmp_path, {"name": "demo-plugin", "version": "1.0.0"},
                     {"name": "demo-market", "owner": {"name": "someone"}, "plugins": [entry]})
    assert any(expected in e for e in errors(tmp_path))


def test_catalog_coverage_detects_missing_entry(tmp_path):
    skills = {"not-in-catalog": {"name": "not-in-catalog"}}
    assert any("has no CATALOG entry" in p for p in generate_catalog.check_coverage(skills))
