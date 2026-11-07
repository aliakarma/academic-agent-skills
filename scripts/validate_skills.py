#!/usr/bin/env python3
"""Validate every skill in skills/ against the Agent Skills specification (https://agentskills.io/specification)
plus the repository's own portability rules, and check the plugin manifests, internal documentation links, and
privacy rules for public files (personal paths, e-mail addresses, private terms, undeclared document binaries).

Usage: python scripts/validate_skills.py [--root PATH]
Exit status: 0 when there are no errors (warnings are printed but allowed), 1 otherwise.
The validator only reads files. It never modifies a skill.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path

import yaml  # type: ignore[import-untyped]

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")  # spec: lowercase, digits, single hyphens, no edge hyphens
SPEC_FIELDS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
# Fields Claude Code documents for skills (code.claude.com/docs/en/skills). Other agents ignore them.
CLAUDE_FIELDS = {"argument-hint", "disable-model-invocation", "user-invocable", "when_to_use", "model",
                 "context", "agent", "hooks", "paths", "shell", "effort"}
RESOURCE_DIRS = ("scripts", "references", "assets", "templates", "examples", "evals", "agents", "tests")
HARDCODED_INSTALL = re.compile(r"(~|\$HOME|\$\{HOME\}|%USERPROFILE%|\$USERPROFILE)/\.claude/skills/")
CACHE_DIRS = {"__pycache__", ".mypy_cache", ".ruff_cache", ".pytest_cache", "node_modules", ".venv"}
MD_LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
CODE_PATH = re.compile(r"`(?:\$\{CLAUDE_SKILL_DIR\}/)?((?:\.\./[a-z0-9-]+/)?(?:%s)/[^`\s]*)`" % "|".join(RESOURCE_DIRS))
SKILL_DIR_PATH = re.compile(r"\$\{CLAUDE_SKILL_DIR\}/([^\s`\"')]+)")
# Privacy rules for public files. Placeholder names (<name>, Jane Doe, ...) are allowed.
PERSONAL_PATH = re.compile(r"(?:[A-Za-z]:[\\/]+Users|/Users|/home)[\\/]+(?!<|\.\.\.|Jane Doe|name\b|user\b|runner\b|alice\b|bob\b|\$)"
                           r"[A-Za-z][\w .-]*[\\/]")
EMAIL = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}\b")
EMAIL_OK = re.compile(r"@(?:example\.(?:com|org|net)|users\.noreply\.github\.com)$")
VENDORED = ("skills/awesome-design/design-md/", "skills/awesome-design/preview-library/")  # third-party demo pages
DOC_BINARIES = {".pdf", ".docx", ".doc", ".pptx", ".xlsx", ".zip", ".7z", ".tar", ".gz"}
TEXT_SUFFIXES = {".md", ".py", ".txt", ".json", ".yml", ".yaml", ".toml", ".cfg", ".ini", ".tex", ".bib", ".sty",
                 ".js", ".mjs", ".ts", ".html", ".css", ".tsv", ".csv", ".ps1", ".sh", ".aux", ""}
PRIVATE_TERMS = Path(".release-review") / "private-terms.txt"  # local-only denylist, never published


@dataclass(frozen=True)
class Issue:
    level: str  # "ERROR" or "WARN"
    path: str
    message: str

    def __str__(self) -> str:
        return f"{self.level:5} {self.path}: {self.message}"


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Return (frontmatter, body). Raise ValueError with a readable reason when the block is missing or invalid."""
    text = text.lstrip("﻿").replace("\r\n", "\n")
    if not text.startswith("---\n"):
        raise ValueError("file must start with a '---' YAML frontmatter line")
    end = text.find("\n---", 4)
    if end == -1:
        raise ValueError("frontmatter has no closing '---' line")
    try:
        data = yaml.safe_load(text[4:end])
    except yaml.YAMLError as exc:
        raise ValueError(f"frontmatter is not valid YAML: {exc}".replace("\n", " ")) from exc
    if not isinstance(data, dict):
        raise ValueError("frontmatter must be a YAML mapping")
    return data, text[end + 4:]


def _is_placeholder(target: str) -> bool:
    return any(c in target for c in "<>*{}$|") or target.endswith("...")


def user_supplied_files(root: Path) -> set[str]:
    """Exact skills/... paths listed in the root .gitignore: files users supply themselves (not redistributable)."""
    gi = root / ".gitignore"
    lines = gi.read_text(encoding="utf-8").splitlines() if gi.is_file() else []
    return {ln.strip() for ln in lines if ln.strip().startswith("skills/") and not any(c in ln for c in "*?[!")}


def _check_reference(skill_dir: Path, rel: str, where: str, issues: list[Issue],
                     user_supplied: set[str] | frozenset[str]) -> None:
    rel = rel.split("#")[0].rstrip(".,:;")
    if not rel or _is_placeholder(rel):
        return
    repo_rel = f"skills/{skill_dir.name}/{rel}"
    if repo_rel in user_supplied:
        issues.append(Issue("WARN", where, f"{rel} is user-supplied (git-ignored); it is not shipped with the skill"))
        return
    target = (skill_dir / rel).resolve()
    first = Path(rel).parts[0]
    if first == "..":  # sibling skill: only check when it names one of this collection's skills
        parts = Path(rel).parts
        if len(parts) < 2 or not (skill_dir.parent / parts[1]).is_dir():
            issues.append(Issue("ERROR", where, f"references sibling skill path '{rel}', but that skill is not in skills/"))
            return
    elif first in RESOURCE_DIRS and not (skill_dir / first).is_dir():
        return  # names a folder in the user's project, not in the skill
    if not target.exists():
        issues.append(Issue("ERROR", where, f"referenced file does not exist: {rel}"))


def validate_skill(skill_dir: Path, repo_root: Path,
                   user_supplied: set[str] | frozenset[str] = frozenset()) -> tuple[list[Issue], str | None]:
    """Validate one skill directory. Return (issues, declared name or None)."""
    issues: list[Issue] = []
    md = skill_dir / "SKILL.md"
    where = md.relative_to(repo_root).as_posix()
    if not md.is_file():
        return [Issue("ERROR", skill_dir.relative_to(repo_root).as_posix(), "directory in skills/ has no SKILL.md")], None
    try:
        fm, body = parse_frontmatter(md.read_text(encoding="utf-8"))
    except UnicodeDecodeError:
        return [Issue("ERROR", where, "SKILL.md is not valid UTF-8")], None
    except ValueError as exc:
        return [Issue("ERROR", where, str(exc))], None

    name = fm.get("name")
    if not isinstance(name, str) or not name:
        issues.append(Issue("ERROR", where, "missing required 'name'"))
        name = None
    else:
        if len(name) > 64:
            issues.append(Issue("ERROR", where, f"name '{name}' is longer than 64 characters"))
        if not NAME_RE.match(name):
            issues.append(Issue("ERROR", where, f"name '{name}' must use lowercase letters, digits and single hyphens"))
        if name != skill_dir.name:
            issues.append(Issue("ERROR", where, f"name '{name}' must match its directory name '{skill_dir.name}'"))

    desc = fm.get("description")
    if not isinstance(desc, str) or not desc.strip():
        issues.append(Issue("ERROR", where, "missing required 'description'"))
    else:
        if len(desc) > 1024:
            issues.append(Issue("ERROR", where, f"description is {len(desc)} characters (limit 1024)"))
        elif len(desc.strip()) < 40:
            issues.append(Issue("WARN", where, "description is under 40 characters; say what the skill does and when to use it"))

    for key in ("license", "allowed-tools"):
        if key in fm and not isinstance(fm[key], str):
            issues.append(Issue("ERROR", where, f"'{key}' must be a string"))
    if "compatibility" in fm and (not isinstance(fm["compatibility"], str) or not 1 <= len(fm["compatibility"]) <= 500):
        issues.append(Issue("ERROR", where, "'compatibility' must be a string of 1-500 characters"))
    if "metadata" in fm:
        meta = fm["metadata"]
        if not isinstance(meta, dict) or not all(isinstance(k, str) and isinstance(v, str) for k, v in meta.items()):
            issues.append(Issue("ERROR", where, "'metadata' must map string keys to string values"))
    for key in fm:
        if key in CLAUDE_FIELDS:
            issues.append(Issue("WARN", where, f"'{key}' is a Claude Code extension field; other agents ignore it"))
        elif key not in SPEC_FIELDS:
            issues.append(Issue("WARN", where, f"'{key}' is not an Agent Skills field"))

    if HARDCODED_INSTALL.search(body):
        issues.append(Issue("ERROR", where, "hard-coded install path (~/.claude/skills/...); use ${CLAUDE_SKILL_DIR}/ instead"))
    refs = {m.group(1) for m in MD_LINK.finditer(body)
            if not re.match(r"^(https?:|mailto:|#)", m.group(1))}
    refs |= {m.group(1) for m in CODE_PATH.finditer(body)}
    refs |= {m.group(1) for m in SKILL_DIR_PATH.finditer(body)}
    for rel in sorted(refs):
        _check_reference(skill_dir, rel, where, issues, user_supplied)

    if body.count("\n") > 500:
        issues.append(Issue("WARN", where, "SKILL.md body is over 500 lines; the spec recommends moving detail to references/"))
    for p in sorted(skill_dir.rglob("*")):
        if any(part in CACHE_DIRS for part in p.relative_to(skill_dir).parts):
            continue
        rel = p.relative_to(repo_root).as_posix()
        if p.is_dir() and not any(p.iterdir()):
            issues.append(Issue("WARN", rel, "empty directory"))
        elif p.is_file() and p.stat().st_size == 0:
            issues.append(Issue("WARN", rel, "empty file"))
    return issues, name


def validate_manifests(root: Path) -> list[Issue]:
    """Static checks for .claude-plugin/. `claude plugin validate .` remains the authoritative check."""
    issues: list[Issue] = []
    files = {}
    for fname in ("plugin.json", "marketplace.json"):
        p = root / ".claude-plugin" / fname
        rel = p.relative_to(root).as_posix()
        if not p.is_file():
            issues.append(Issue("ERROR", rel, "file is missing"))
            continue
        try:
            files[fname] = json.loads(p.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            issues.append(Issue("ERROR", rel, f"invalid JSON: {exc}"))
    plugin, market = files.get("plugin.json"), files.get("marketplace.json")
    if plugin is not None:
        if not isinstance(plugin.get("name"), str) or not NAME_RE.match(plugin["name"]):
            issues.append(Issue("ERROR", ".claude-plugin/plugin.json", "'name' must be kebab-case"))
        if not re.match(r"^\d+\.\d+\.\d+$", str(plugin.get("version", ""))):
            issues.append(Issue("ERROR", ".claude-plugin/plugin.json", "'version' must be MAJOR.MINOR.PATCH"))
    if market is not None:
        mrel = ".claude-plugin/marketplace.json"
        for key in ("name", "owner", "plugins"):
            if key not in market:
                issues.append(Issue("ERROR", mrel, f"missing required '{key}'"))
        if not isinstance(market.get("owner", {}).get("name"), str):
            issues.append(Issue("ERROR", mrel, "'owner.name' is required"))
        for i, entry in enumerate(market.get("plugins", [])):
            src = entry.get("source")
            if isinstance(src, str) and (not (src == "." or src.startswith("./")) or ".." in src):
                issues.append(Issue("ERROR", mrel, f"plugins[{i}].source must start with './' and stay inside the repo"))
            elif isinstance(src, str) and not (root / src).is_dir():
                issues.append(Issue("ERROR", mrel, f"plugins[{i}].source '{src}' does not exist"))
            if plugin is not None and entry.get("name") == plugin.get("name") and "version" in entry:
                issues.append(Issue("WARN", mrel, f"plugins[{i}] sets 'version'; plugin.json wins, keep it there only"))
        if plugin is not None and plugin.get("name") not in {e.get("name") for e in market.get("plugins", [])}:
            issues.append(Issue("ERROR", mrel, f"no plugin entry is named '{plugin.get('name')}' (must match plugin.json)"))
    return issues


def validate_doc_links(root: Path) -> list[Issue]:
    """Relative links in repository Markdown (outside skills/) must point at files that exist."""
    issues: list[Issue] = []
    docs = [p for p in root.glob("*.md")] + list((root / "docs").glob("*.md")) + list((root / ".github").rglob("*.md"))
    for doc in sorted(docs):
        text = re.sub(r"```.*?```", "", doc.read_text(encoding="utf-8"), flags=re.S)
        for m in MD_LINK.finditer(text):
            target = m.group(1)
            if re.match(r"^(https?:|mailto:|#)", target) or _is_placeholder(target):
                continue
            if not (doc.parent / target.split("#")[0]).exists():
                issues.append(Issue("ERROR", doc.relative_to(root).as_posix(), f"broken link: {target}"))
    return issues


def _public_text_files(root: Path, user_supplied: set[str]) -> list[Path]:
    """Text files that would be published: everything except local-only, git-ignored and cache paths."""
    local_only = {".release-review", "RELEASE_COMMIT_PLAN.md", "MANUAL_RELEASE_CHECKLIST.md", ".git"} | CACHE_DIRS
    out = []
    for p in sorted(root.rglob("*")):
        rel = p.relative_to(root)
        if (p.is_file() and not set(rel.parts) & local_only and rel.as_posix() not in user_supplied
                and p.suffix.lower() in TEXT_SUFFIXES and p.name != "LICENSE"):
            out.append(p)
    return out


def validate_privacy(root: Path, user_supplied: set[str] | frozenset[str] = frozenset()) -> list[Issue]:
    """Personal machine paths, real e-mail addresses, private terms, and document binaries in public files."""
    issues: list[Issue] = []
    terms_file = Path(os.environ.get("PRIVATE_TERMS_FILE") or root / PRIVATE_TERMS)
    terms = [ln.strip().lower() for ln in terms_file.read_text(encoding="utf-8").splitlines()
             if ln.strip() and not ln.startswith("#")] if terms_file.is_file() else []
    for p in _public_text_files(root, user_supplied):
        rel = p.relative_to(root).as_posix()
        try:
            text = p.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if PERSONAL_PATH.search(text):
            issues.append(Issue("ERROR", rel, "personal machine path (use a placeholder such as C:/Users/<name>/)"))
        if not rel.startswith(VENDORED):
            for m in EMAIL.finditer(text):
                if not EMAIL_OK.search(m.group(0)):
                    issues.append(Issue("ERROR", rel, "e-mail address in a public file (use name@example.com)"))
                    break
        low = text.lower() + "\n" + rel.lower()
        if any(re.search(r"(?<![a-z0-9])" + re.escape(t) + r"(?![a-z0-9])", low) for t in terms):  # never printed
            issues.append(Issue("ERROR", rel, f"contains a term from the private denylist ({terms_file.name})"))
    for p in sorted((root / "skills").rglob("*")):
        rel = p.relative_to(root).as_posix()
        if p.is_file() and p.suffix.lower() in DOC_BINARIES and rel not in user_supplied:
            issues.append(Issue("ERROR", rel, "document or archive in skills/; publish only files you may redistribute, "
                                "or list a user-supplied file in .gitignore"))
    return issues


def validate_repo(root: Path) -> tuple[list[Issue], list[str]]:
    """Validate the whole repository. Return (issues, sorted skill names)."""
    skills_dir = root / "skills"
    if not skills_dir.is_dir():
        return [Issue("ERROR", "skills", "skills/ directory is missing")], []
    issues: list[Issue] = []
    seen: dict[str, str] = {}
    user_supplied = user_supplied_files(root)
    for d in sorted(p for p in skills_dir.iterdir() if p.is_dir() and not p.name.startswith(".")):
        found, name = validate_skill(d, root, user_supplied)
        issues += found
        if name:
            if name in seen:
                issues.append(Issue("ERROR", f"skills/{d.name}/SKILL.md", f"duplicate skill name '{name}' (also in skills/{seen[name]})"))
            seen[name] = d.name
    for stray in sorted(p for p in skills_dir.iterdir() if p.is_file()):
        issues.append(Issue("WARN", stray.relative_to(root).as_posix(), "loose file in skills/; skills are directories"))
    if (root / ".claude-plugin").exists():
        issues += validate_manifests(root)
    issues += validate_doc_links(root)
    issues += validate_privacy(root, user_supplied)
    return issues, sorted(seen)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent, help="repository root")
    ap.add_argument("--quiet", action="store_true", help="print errors only")
    args = ap.parse_args(argv)
    issues, names = validate_repo(args.root.resolve())
    errors = [i for i in issues if i.level == "ERROR"]
    for issue in issues:
        if issue.level == "ERROR" or not args.quiet:
            print(issue)
    print(f"\n{len(names)} skills, {len(errors)} errors, {len(issues) - len(errors)} warnings")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
