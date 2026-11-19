"""Cross-skill links: every 'Related skills' section names real skills, and research-workflow-map covers them all."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = {p.parent.name: p.read_text(encoding="utf-8") for p in (ROOT / "skills").glob("*/SKILL.md")}
MAP = "research-workflow-map"
# Named on purpose but not part of this collection (see each section's own wording).
EXTERNAL = {"pptx", "bibtex-validator", "sop-skill"}


def related_section(text: str) -> str:
    m = re.search(r"^## Related skills\s*$(.*?)(?=^## |\Z)", text, re.M | re.S)
    return m.group(1) if m else ""


def named(text: str) -> set[str]:
    return set(re.findall(r"`([a-z0-9]+(?:-[a-z0-9]+)+|pptx)`", text))


def test_every_skill_links_to_the_map():
    missing = [n for n, t in SKILLS.items() if n != MAP and MAP not in related_section(t)]
    assert missing == []


def test_related_sections_name_only_real_skills():
    bad = {n: sorted(named(related_section(t)) - set(SKILLS) - EXTERNAL) for n, t in SKILLS.items() if n != MAP}
    assert {n: b for n, b in bad.items() if b} == {}


def test_map_covers_every_skill_and_names_no_unknown_one():
    text = SKILLS[MAP]
    rows = set(re.findall(r"^\| ([a-z0-9-]+) \|", text, re.M))
    assert rows == set(SKILLS) - {MAP}
    assert named(text) - set(SKILLS) - EXTERNAL == set()


def test_required_links_in_the_map_appear_in_the_skill():
    # A dependency the map marks "(required)" must also be named in that skill's own Related skills section.
    for name, uses in re.findall(r"^\| ([a-z0-9-]+) \| [^|]* \| ([^|]*) \|", SKILLS[MAP], re.M):
        for dep in re.findall(r"([a-z0-9-]+)(?: scripts)? \(required", uses):
            assert dep in related_section(SKILLS[name]), f"{name} should name required {dep}"
