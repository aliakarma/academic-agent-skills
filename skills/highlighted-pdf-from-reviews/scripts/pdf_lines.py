"""Print the text of numbered lines of a compiled manuscript PDF (lineno margin
numbers), so "p. 8, ll. 281-292" citations in a response letter can be matched
to source sentences.

    python pdf_lines.py main.pdf 281-292 1371
    python pdf_lines.py main.pdf --left 40-55            # numbers in the left margin
    python pdf_lines.py main.pdf --after Introduction 4  # skip title-block superscripts

Requires pdftotext (poppler). Lines are printed as "<n> p<page>: <text>".
Table cells and floats carry no line numbers, and a number can be misread from a
table, so check the page shown against the letter.
"""
import argparse
import re
import subprocess

ap = argparse.ArgumentParser()
ap.add_argument('pdf')
ap.add_argument('ranges', nargs='+', help='N or A-B')
ap.add_argument('--left', action='store_true', help='line numbers are in the left margin')
ap.add_argument('--after', default='Abstract', help='ignore numbers before the first line starting with this word')
a = ap.parse_args()

txt = subprocess.run(['pdftotext', '-layout', a.pdf, '-'], capture_output=True, text=True,
                     encoding='utf-8', errors='replace', check=True).stdout
pat = re.compile(r'^\s*(\d{1,5})\s+(\S.*)$' if a.left else r'^(.*?\S)\s+(\d{1,5})\s*$')
cands, started = {}, False
for page, chunk in enumerate(txt.split('\f'), start=1):
    for raw in chunk.split('\n'):
        started = started or raw.strip().startswith(a.after)
        m = started and pat.match(raw)
        if m:
            num, body = (m.group(1), m.group(2)) if a.left else (m.group(2), m.group(1))
            cands.setdefault(int(num), []).append((page, body.strip()))
# table cells can end in numbers too: keep the candidate that fits the page order
lines, last_page = {}, 1
for n in sorted(k for k in cands if k > 0):   # lineno starts at 1; "0" is always a table cell
    fit = [c for c in cands[n] if c[0] >= last_page] or cands[n]
    lines[n] = min(fit)
    last_page = lines[n][0]

for r in a.ranges:
    lo, _, hi = r.partition('-')
    for n in range(int(lo), int(hi or lo) + 1):
        page, body = lines.get(n, ('?', '[no such line number found]'))
        print(f'{n} p{page}: {body}')
