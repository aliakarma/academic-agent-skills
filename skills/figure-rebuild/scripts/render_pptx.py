#!/usr/bin/env python3
"""Render slide 1 of a .pptx to PNG so the PowerPoint twin can be viewed.

Windows: drives installed PowerPoint over COM (the pptx skill's soffice.py
wrapper fails there with AttributeError: socket.AF_UNIX).
Elsewhere: LibreOffice -> PDF -> pdftoppm.

Usage:  python render_pptx.py figures/<name>.pptx OUT.png
"""
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__)
        return 1
    src, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    if sys.platform == "win32":
        ps = (f"$a = New-Object -ComObject PowerPoint.Application; "
              f"$p = $a.Presentations.Open('{src}', $true, $false, $false); "
              f"$p.Slides(1).Export('{out}', 'PNG', 1600, 900); $p.Close(); $a.Quit()")
        subprocess.run(["powershell", "-NoProfile", "-Command", ps], check=True)
    else:
        soffice = shutil.which("soffice") or shutil.which("libreoffice")
        if not soffice:
            print("no PowerPoint and no LibreOffice: cannot render")
            return 1
        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run([soffice, "--headless", "--convert-to", "pdf", "--outdir", tmp, str(src)],
                           check=True, capture_output=True)
            pdf = Path(tmp) / (src.stem + ".pdf")
            subprocess.run(["pdftoppm", "-png", "-r", "120", "-singlefile", str(pdf), str(out.with_suffix(""))],
                           check=True)
    if not out.exists():
        print(f"render failed: {out} not written")
        return 1
    print(f"wrote {out}; NOW VIEW IT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
