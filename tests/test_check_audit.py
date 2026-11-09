"""Tests for skills/manuscript-revision/scripts/check_audit.py, the completion gate of a revision."""
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "skills" / "manuscript-revision" / "scripts" / "check_audit.py"
spec = importlib.util.spec_from_file_location("check_audit", SCRIPT)
ca = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ca)

HEAD = ("# Revision audit\n\n| ID | Reviewer | Request | Location | Action and evidence | Status | Blocker |\n"
        "|---|---|---|---|---|---|---|\n")


def audit(*rows: str) -> str:
    return HEAD + "".join(r + "\n" for r in rows) + "\n## Plan\n\n| ID | Step |\n|---|---|\n| R9-99 | ignored |\n"


DONE = audit("| ED-01 | Editor | Shorten abstract | Abstract | Cut to 200 words | ADDRESSED | |",
             "| R1-01 | Reviewer 1 | Add baseline | Table 4 | Ran revision_experiments/R1-01/run.py | addressed | |",
             "| R2-03a | Reviewer 2 | Field data | Sec. 6.3 | Limitation added | BLOCKED | needs: field data |")


def test_all_addressed_or_justified_blocked_is_done():
    code, problems, items = ca.check(DONE)
    assert code == 0 and problems == []
    assert [i for i, _ in items] == ["ED-01", "R1-01", "R2-03a"]   # the second table is not read


def test_open_in_progress_and_unsupported_statuses_keep_the_run_going():
    code, problems, _ = ca.check(audit(
        "| R1-01 | Reviewer 1 | a | b | c | OPEN | |",
        "| R1-02 | Reviewer 1 | a | b | c | IN PROGRESS | |",
        "| R1-03 | Reviewer 1 | a | b | - | ADDRESSED | |",
        "| R1-04 | Reviewer 1 | a | b | c | BLOCKED | n/a |",
        "| R1-05 | Reviewer 1 | a | b | c | ADDRESSED | |"))
    assert code == 1
    assert [p.split(":")[0] for p in problems] == ["R1-01", "R1-02", "R1-03", "R1-04"]


def test_malformed_tables():
    assert ca.check("no table here")[0] == 2
    assert ca.check(audit("| R1-01 | x | a | b | c | DONE | |"))[0] == 2              # unknown status
    assert ca.check(audit("| R1-01 | x | a | b | c | ADDRESSED | |",
                          "| R1-01 | x | a | b | c | ADDRESSED | |"))[0] == 2        # duplicate
    assert ca.check(audit("| Reviewer 1 | x | a | b | c | ADDRESSED | |"))[0] == 2     # not an ID
    assert ca.check(audit())[0] == 2                                                 # no rows


def test_letter_must_mention_every_id_as_a_whole_token():
    letter = "\\begin{reviewercomment}{ED-01}\n\\begin{reviewercomment}{R1-01a}\n% R2-03a\nR2-03a-bis\n"
    code, problems, _ = ca.check(DONE, letter)
    assert code == 1
    assert sorted(p.split(":")[0] for p in problems) == ["R1-01", "R2-03a"]   # R1-01a, comment, suffix do not count
    assert ca.check(DONE, letter + "R1-01 and R2-03a\n")[0] == 0


def test_cli_writes_inventory_for_response_to_reviewer(tmp_path, capsys):
    (tmp_path / "revision_audit.md").write_text(DONE, encoding="utf-8")
    tsv = tmp_path / "inventory.tsv"
    assert ca.main([str(tmp_path / "revision_audit.md"), "--tsv", str(tsv)]) == 0
    assert tsv.read_text(encoding="utf-8").splitlines() == [
        "ED-01\tShorten abstract", "R1-01\tAdd baseline", "R2-03a\tField data"]
    assert "DONE" in capsys.readouterr().out
    assert ca.main([str(tmp_path / "missing.md")]) == 2
