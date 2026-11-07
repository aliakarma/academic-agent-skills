#!/usr/bin/env python3
"""Extract a downloaded template archive without trusting it.

Usage:
  python -I safe_extract.py ARCHIVE DEST_DIR
  python -I safe_extract.py --self-test

DEST_DIR must not exist yet. The whole archive is rejected (exit 2, nothing
written) when any member has an absolute or drive-letter path, a '..' part,
a Windows reserved name, or a trailing dot or space, when any member is a link
or device, or when the unpacked size exceeds 500 MB. After extraction the
script lists every file, flags files that must never be run, and prints the
version line of each .cls, .sty, and .bst file.
"""
import contextlib
import io
import re
import stat
import sys
import tarfile
import tempfile
import zipfile
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

LIMIT = 500 * 2**20
RESERVED = {"con", "prn", "aux", "nul"} | {f"{p}{i}" for p in ("com", "lpt") for i in range(1, 10)}
NEVER_RUN_SUFFIXES = {".exe", ".msi", ".bat", ".cmd", ".com", ".scr", ".ps1", ".vbs", ".js", ".jar", ".sh", ".bash",
                      ".zsh", ".py", ".pl", ".rb", ".lua", ".dll", ".so", ".dylib", ".app", ".command", ".docm", ".dotm"}
NEVER_RUN_NAMES = {"latexmkrc", ".latexmkrc", "makefile", "gnumakefile"}


def unsafe_name(name):
    if "\x00" in name:
        return True
    parts = [p for p in name.replace("\\", "/").split("/") if p not in ("", ".")]
    return bool(parts) and (name.startswith(("/", "\\")) or re.match(r"[A-Za-z]:", name) is not None or any(
        p == ".." or p.split(".")[0].lower() in RESERVED or p != p.rstrip(". ") for p in parts))


def read_members(path):
    """Return (handle, [(name, size, is_link_or_device)]), or (None, None) when path is not an archive."""
    if zipfile.is_zipfile(path):
        z = zipfile.ZipFile(path)
        return z, [(i.filename, i.file_size, stat.S_ISLNK(i.external_attr >> 16)) for i in z.infolist()]
    if tarfile.is_tarfile(path):
        t = tarfile.open(path)
        return t, [(m.name, m.size, not (m.isfile() or m.isdir())) for m in t.getmembers()]
    return None, None


def version_line(path):
    text = path.read_text(encoding="latin-1")
    if path.suffix.lower() == ".bst":
        m = re.search(r"^%.*\bversion\b.*$", text, re.M | re.I)
        return m.group(0).lstrip("% ").strip() if m else ""
    m = re.search(r"\\Provides(?:Class|Package|File)\s*\{[^}]*\}\s*\[([^\]]*)\]", text)
    return m.group(1).strip() if m else ""


def extract(archive, dest):
    archive, dest = Path(archive), Path(dest)
    if dest.exists():
        print(f"REJECT: {dest} already exists. Pick a new, empty destination.")
        return 2
    handle, members = read_members(archive)
    if handle is None:
        head = archive.read_bytes()[:512].lower()
        hint = (" It looks like an HTML page, so the download probably hit a login or error page."
                if b"<html" in head or b"<!doctype" in head else "")
        print(f"REJECT: {archive} is not a zip or tar archive.{hint}")
        return 2
    with handle:
        bad = [name for name, _, special in members if special or unsafe_name(name)]
        total = sum(size for _, size, _ in members)
        if bad or total > LIMIT:
            print("REJECT: " + (f"{len(bad)} unsafe member(s), for example {bad[:5]}" if bad
                                else f"unpacked size {total} bytes is over the {LIMIT} byte limit"))
            return 2
        dest.mkdir(parents=True)
        if isinstance(handle, tarfile.TarFile) and hasattr(tarfile, "data_filter"):
            handle.extractall(dest, filter="data")
        else:
            handle.extractall(dest)  # every member passed the checks above
    root = dest.resolve()
    files = sorted(p for p in dest.rglob("*") if p.is_file())
    for p in files:
        if root not in p.resolve().parents:
            print(f"ERROR: {p} resolves outside {root}. Delete {dest} and do not use this archive.")
            return 3
        flag = "[DO NOT RUN] " if p.suffix.lower() in NEVER_RUN_SUFFIXES or p.name.lower() in NEVER_RUN_NAMES else ""
        version = version_line(p) if p.suffix.lower() in (".cls", ".sty", ".bst") else ""
        print(f"{flag}{p.relative_to(dest).as_posix()} ({p.stat().st_size} bytes)"
              + (f"  version: {version}" if version else ""))
    print(f"OK: extracted {len(files)} file(s) into {dest}")
    return 0


def self_test():
    with tempfile.TemporaryDirectory() as tmp, contextlib.redirect_stdout(io.StringIO()):
        d = Path(tmp)
        good = d / "good.zip"
        with zipfile.ZipFile(good, "w") as z:
            z.writestr("tmpl/sample.tex", "\\documentclass{demo}")
            z.writestr("tmpl/demo.cls", "\\ProvidesClass{demo}[2026/01/01 v1.0 demo class]")
            z.writestr("tmpl/latexmkrc", "$pdf_mode = 1;")
        assert extract(good, d / "out") == 0 and (d / "out/tmpl/sample.tex").is_file()
        assert extract(good, d / "out") == 2, "an existing destination must be refused"
        evil = d / "evil.zip"
        with zipfile.ZipFile(evil, "w") as z:
            z.writestr("ok.tex", "x")
            z.writestr("../escape.txt", "x")
        assert extract(evil, d / "evil") == 2 and not (d / "evil").exists() and not (d / "escape.txt").exists()
        link = d / "link.tar"
        with tarfile.open(link, "w") as t:
            info = tarfile.TarInfo("template/passwd")
            info.type, info.linkname = tarfile.SYMTYPE, "/etc/passwd"
            t.addfile(info)
        assert extract(link, d / "link") == 2 and not (d / "link").exists()
        page = d / "template.zip"
        page.write_text("<!DOCTYPE html><html><body>Sign in</body></html>")
        assert extract(page, d / "page") == 2 and not (d / "page").exists()
        for name in ("/etc/x", "C:/x.tex", "a/../../b", "con.tex", "dir/name. ", "x\x00y"):
            assert unsafe_name(name), name
        for name in ("./tmpl/main.tex", "tmpl/", "a/b/c.cls", "./"):
            assert not unsafe_name(name), name
    print("SELF-TEST PASS")
    return 0


def main(argv):
    if argv[1:] == ["--self-test"]:
        return self_test()
    if len(argv) != 3:
        print(__doc__)
        return 2
    return extract(argv[1], argv[2])


if __name__ == "__main__":
    sys.exit(main(sys.argv))
