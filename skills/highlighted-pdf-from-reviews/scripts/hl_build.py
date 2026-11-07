"""Annotation engine for a highlighted revised manuscript (LaTeX).

A per-paper build script imports this module, calls start(), lists one
operation per revised element (each tied to reviewer-comment IDs), then calls
finish(). finish() writes <Paper>_Highlighted.tex and refuses to succeed unless
stripping the annotation layer gives back the clean manuscript byte for byte.

    import sys; sys.path.insert(0, r'<skill>/scripts'); from hl_build import *
    start('main.tex', 'Paper_Highlighted.tex')
    W(r'exact revised sentence.', 'R1.2', 'Sec. 3.1')       # inline highlight
    BOX('First words of a new paragraph', 'R2.1,R3.4', 'Sec. 4.2')
    FLOAT('tab:new', 'R2.3', 'Table 5')                      # box a table/figure
    finish(guide(title=..., rows=map_rows(COMMENTS), ...))

Every match must be unique in the current text; ambiguity aborts the build.
"""
import collections
import difflib
import os
import re

BS = chr(92)
_S = {}


def start(src, out):
    _S.update(src=src, out=out, text=open(src, encoding='utf-8').read(),
              where=collections.OrderedDict())


def _note(ids, where):
    for i in ids.split(','):
        lst = _S['where'].setdefault(i.strip(), [])
        if where not in lst:
            lst.append(where)


def _unique(s):
    n = _S['text'].count(s)
    if n != 1:
        raise SystemExit(f'expected 1 match, found {n}: {s[:90]!r}')


def W(s, ids, where):
    """Inline yellow highlight with an ID tag in front."""
    _unique(s); _note(ids, where)
    _S['text'] = _S['text'].replace(s, BS + 'rv{' + ids + '}{' + s + '}')


def H(s):
    """Highlight without a tag (further cells of a row already tagged)."""
    _unique(s)
    _S['text'] = _S['text'].replace(s, BS + 'rvhl{' + s + '}')


def T(before, ids, where):
    """ID tag alone, inserted before a unique string (row groups, row starts)."""
    _unique(before); _note(ids, where)
    _S['text'] = _S['text'].replace(before, BS + 'rvtag{' + ids + '}' + before)


def R(old, new, ids, where):
    """Explicit replacement; `new` may only add annotation macros to `old`
    (the strip check enforces this)."""
    _unique(old); _note(ids, where)
    _S['text'] = _S['text'].replace(old, new)


def _line(lines, prefix):
    hits = [k for k, l in enumerate(lines) if l.lstrip().startswith(prefix)]
    if len(hits) != 1:
        raise SystemExit(f'line prefix matched {len(hits)} times: {prefix[:80]!r}')
    return hits[0]


def BOX(first, ids, where, last=None):
    """Box whole source paragraphs, from the line starting with `first` to the
    line starting with `last` (default: the same line). Use only for
    paragraphs preceded by a blank line, never for text continuing after a
    display equation (that would add a paragraph break)."""
    lines = _S['text'].split('\n')
    i = _line(lines, first)
    j = _line(lines, last) if last else i
    assert j >= i, 'last paragraph precedes first'
    _note(ids, where)
    lines[j] += '\n' + BS + 'end{rvbox}'
    lines[i] = BS + 'begin{rvbox}{' + ids + '}\n' + lines[i]
    _S['text'] = '\n'.join(lines)


def FLOAT(label, ids, where):
    """Box a table or figure environment identified by its \\label. If the
    float opens with adjustwidth (wide floats), the box goes inside it; a
    caption placed after \\end{adjustwidth} then stays outside, so highlight it
    separately with W."""
    lines = _S['text'].split('\n')
    k = _line(lines, BS + 'label{' + label + '}')
    b = max(n for n in range(k) if re.match(r'\s*\\begin\{(table|figure)\*?\}', lines[n]))
    e = min(n for n in range(k, len(lines)) if re.match(r'\s*\\end\{(table|figure)\*?\}', lines[n]))
    _note(ids, where)
    if lines[b + 1].lstrip().startswith(BS + 'begin{adjustwidth}'):
        a = max(n for n in range(b, e) if lines[n].lstrip().startswith(BS + 'end{adjustwidth}'))
        lines[a] = BS + 'end{rvfloat}\n' + lines[a]
        lines[b + 1] += '\n' + BS + 'begin{rvfloat}{' + ids + '}'
    else:
        lines[e] = BS + 'end{rvfloat}\n' + lines[e]
        lines[b] += '\n' + BS + 'begin{rvfloat}{' + ids + '}'
    _S['text'] = '\n'.join(lines)


def EQ(label, ids, where):
    """Box the formula of a single equation environment; numbering is kept."""
    lines = _S['text'].split('\n')
    k = _line(lines, BS + 'label{' + label + '}')
    b = max(n for n in range(k) if lines[n].lstrip().startswith(BS + 'begin{equation}'))
    first, last = b + 1, k - 1
    _note(ids, where)
    ind = re.match(r'\s*', lines[first]).group(0)
    lines[first] = ind + BS + 'rvmath[' + ids + ']{' + lines[first][len(ind):]
    lines[last] += '}'
    _S['text'] = '\n'.join(lines)


def BAR(begin_line, ids, where, msg):
    """Marker bar before an element that cannot be boxed (e.g. a longtable that
    runs across pages). `begin_line` is the start of its \\begin line."""
    lines = _S['text'].split('\n')
    k = _line(lines, begin_line)
    k -= 1 if lines[k - 1].strip() in (BS + 'small', BS + 'footnotesize') else 0
    _note(ids, where)
    lines[k] = BS + 'rvbar{' + ids + '}{' + msg + '}\n' + lines[k]
    _S['text'] = '\n'.join(lines)


def labels_from_aux(aux_path, prefix):
    """{name: page} for \\newlabel{<prefix><name>} entries of a compiled letter."""
    aux = open(aux_path, encoding='utf-8').read()
    return dict(re.findall(r'newlabel\{' + re.escape(prefix) + r'([^}]*)\}\{\{[^}]*\}\{([^}]*)\}', aux))


# ----------------------------------------------------------------- front guide
def map_rows(comments, extra_where=None, suppl=None, letter_pages=None, default_page='--'):
    """Rows of the reviewer comment map. comments: [(ID, reviewer, description)].
    'Highlighted in' is filled from the `where` labels of the operations."""
    extra_where, suppl, letter_pages = extra_where or {}, suppl or {}, letter_pages or {}
    stray = set(_S['where']) - {c[0] for c in comments}
    if stray:
        raise SystemExit(f'IDs used in operations but missing from comments: {sorted(stray)}')
    rows, prev = [], None
    for cid, rev, desc in comments:
        if rev != prev:
            rows.append(BS + r'multicolumn{5}{@{}l}{\rule{0pt}{2.6ex}\textbf{' + rev + r'}}\\')
            prev = rev
        where = '; '.join(_S['where'].get(cid, []))
        if cid in extra_where:
            where = extra_where[cid] + ('; ' + where if where else '')
        where += suppl.get(cid, '')
        rows.append(BS + 'leavevmode' + BS + 'hypertarget{rvmap.' + cid + '}{' + BS + 'textbf{' + cid + '}} & '
                    + desc + ' & ' + (where or '--') + r' & \rvpages{' + cid + '} & '
                    + letter_pages.get(cid, default_page) + r'\\')
    return '\n'.join(rows)


def _items(lst):
    return (BS + r'begin{itemize}[leftmargin=1.4em,itemsep=1pt,topsep=1pt]' + '\n'
            + '\n'.join(BS + 'item ' + x for x in lst) + '\n' + BS + 'end{itemize}')


DEFAULT_KEY = [
    r'\rvsampletag{R1.1}\,\hl{Yellow highlight}: a revised or new sentence, clause, table cell or caption '
    r'passage, preceded by the ID of the reviewer comment it answers. Several IDs separated by a dot '
    r'(\rvsampletag{R1.1\,\textperiodcentered\,R2.3}) mean that the passage answers each of them.',
    r'A pale yellow box with an ID tab at its top left: a new or substantially rewritten paragraph, or a '
    r'new or revised equation, table or figure. Inside a boxed table, tags on row groups name the comment '
    r'that each group of rows answers.',
    r'A yellow bar with an ID tab: placed before a new element that runs across pages and therefore cannot '
    r'be boxed.',
    r'Every tag is a link to its row in the map below, and every page number in the map is a link to the '
    r'highlighted passage on that page.']
DEFAULT_NOTES = [
    r'Page numbers in the map are those printed on the pages of this document. Section, equation, table and '
    r'figure numbers are identical to those of the clean manuscript.',
    r'Page and line numbers quoted in the Response to Reviewers refer to the clean revised manuscript. The '
    r'annotation adds a little space, so pages and line numbers shift slightly here, and lines inside boxes '
    r'carry no line numbers.']


def guide(*, title, venue_line, header_label, intro, rows, pdfmeta,
          key=DEFAULT_KEY, reading_notes=DEFAULT_NOTES, supplementary='', cannot_show=(),
          wide_open='', wide_close='', lt_left='0pt', map_width=r'\textwidth', page_style=None):
    """Return the annotation layer: package load, front guide and a \\maketitle
    wrapper that prints the guide before the journal title page.

    pdfmeta      \\hypersetup{...} with the journal's PDF metadata. The guide ships the
                 first page, so metadata a class sets inside \\maketitle is otherwise lost.
    wide_open/   e.g. \\begin{adjustwidth}{-\\extralength}{0cm} / \\end{adjustwidth} for
    wide_close   classes with a margin column (MDPI); lt_left the matching \\LTleft and
                 map_width the full width, e.g. \\textwidth+\\extralength.
    page_style   style restored after the guide; default: fancy if defined, else plain.
    """
    restore = (BS + 'pagestyle{' + page_style + '}') if page_style else \
        r'\@ifundefined{ps@fancy}{\pagestyle{plain}}{\pagestyle{fancy}}'
    return r"""% >>> highlighting layer (not part of the clean revised manuscript)
\usepackage{rvhighlight}
% guide page style built without fancyhdr, so the journal's own headers stay untouched
\makeatletter
\def\ps@rvguide{\def\@oddhead{\footnotesize """ + header_label + r"""\hfil Revision guide, page \thepage}%
  \let\@evenhead\@oddhead\def\@oddfoot{}\let\@evenfoot\@oddfoot}
\makeatother
\newcommand{\rvguide}{%
\pagenumbering{roman}\pagestyle{rvguide}\thispagestyle{rvguide}%
\pdfbookmark[1]{Revision highlighting guide and reviewer comment map}{rvguide}%
""" + wide_open + r"""
\setlength{\parindent}{0pt}\setlength{\parskip}{4pt}
{\Large\bfseries Highlighted Revised Manuscript}\par\smallskip
{\large """ + title + r"""}\par\smallskip
{\small """ + venue_line + r"""}\par
\medskip{\color{rvframe}\hrule height 0.6pt}\medskip

{\large\bfseries Revision Highlighting Guide and Reviewer Comment Map}\par\smallskip
""" + intro + r"""

\textbf{Annotation key}
""" + _items(key) + r"""

\textbf{Reading notes}
""" + _items(reading_notes) + r"""

\textbf{Reviewer comment map}\par
% longtable ignores adjustwidth, so shift it explicitly
\setlength{\LTleft}{""" + lt_left + r"""}\setlength{\LTright}{0pt plus 1fill}\setlength{\LTpre}{2pt}
% longtable always steps the table counter; keep manuscript table numbers unchanged
\addtocounter{table}{-1}
\newlength{\rvmapw}\setlength{\rvmapw}{\dimexpr """ + map_width + r"""-8\tabcolsep\relax}
{\footnotesize\renewcommand{\arraystretch}{1.12}
\begin{longtable}{@{}>{\raggedright\arraybackslash}p{0.1\rvmapw}>{\raggedright\arraybackslash}p{0.25\rvmapw}>{\raggedright\arraybackslash}p{0.385\rvmapw}>{\raggedright\arraybackslash}p{0.175\rvmapw}>{\raggedleft\arraybackslash}p{0.09\rvmapw}@{}}
\toprule
\textbf{ID} & \textbf{Comment / issue} & \textbf{Highlighted in} & \textbf{Highlighted pages} & \textbf{Letter page}\\\midrule
\endfirsthead
\toprule
\textbf{ID} & \textbf{Comment / issue} & \textbf{Highlighted in} & \textbf{Highlighted pages} & \textbf{Letter page}\\\midrule
\endhead
\bottomrule
\endfoot
""" + rows + r"""
\end{longtable}}
""" + (('\n' + supplementary + '\n') if supplementary else '') + (
        ('\n' + r'\textbf{Revisions that cannot be shown by highlighting}' + '\n' + _items(cannot_show) + '\n')
        if cannot_show else '') + wide_close + r"""
\clearpage}
\makeatletter
\let\rv@origmaketitle\maketitle
% the guide ships the first page, so set the journal's PDF metadata before it
\def\rv@meta{""" + pdfmeta + r"""}
\def\maketitle{\rv@meta\rvguide\pagenumbering{arabic}""" + restore + r"""\rv@origmaketitle}
\makeatother
% <<< highlighting layer
"""


# ----------------------------------------------------------------- output + check
def strip(t):
    """Remove the annotation layer; the result must equal the clean source."""
    t = re.sub(r'% >>> highlighting layer.*?% <<< highlighting layer\n', '', t, flags=re.S)
    t = re.sub(r'^\\(begin\{rv(box|float)\}\{[^}]*\}|end\{rv(box|float)\}|rvbar\{[^}]*\}\{[^}]*\})\n', '', t, flags=re.M)
    t = re.sub(r'\\rvtag\{[^}]*\}', '', t)
    out, k = [], 0
    pat = re.compile(r'\\rv\{[^}]*\}\{|\\rvhl\{|\\rvmath\[[^\]]*\]\{')
    while True:
        m = pat.search(t, k)
        if not m:
            out.append(t[k:])
            return ''.join(out)
        out.append(t[k:m.start()])
        depth, j = 1, m.end()
        while depth:
            if t[j] == BS:
                j += 2
                continue
            depth += (t[j] == '{') - (t[j] == '}')
            j += 1
        out.append(t[m.end():j - 1])
        k = j


def finish(layer, anchor=BS + 'begin{document}'):
    """Insert the layer before `anchor`, write the output and run the strip check."""
    if os.path.abspath(_S['out']) == os.path.abspath(_S['src']):
        raise SystemExit('refusing to overwrite the clean manuscript')
    text = _S['text']
    n = text.count(anchor)
    if n != 1:
        raise SystemExit(f'layer anchor matched {n} times: {anchor!r}')
    text = text.replace(anchor, layer + anchor)
    open(_S['out'], 'w', encoding='utf-8', newline='\n').write(text)
    orig = open(_S['src'], encoding='utf-8').read()
    s = text
    while True:   # nested annotations (a tag inside a highlighted cell) need repeated passes
        s2 = strip(s)
        if s2 == s:
            break
        s = s2
    if s != orig:
        print('\n'.join(list(difflib.unified_diff(orig.splitlines(), s.splitlines(), lineterm='', n=0))[:40]))
        raise SystemExit('STRIP CHECK FAILED: the annotation layer changed manuscript content')
    print(f'wrote {_S["out"]}; strip check passed (annotation removed == clean source)')
    print('IDs annotated:', ', '.join(_S['where']))


def report(aux_path, comments):
    """After compiling twice: highlighted pages per ID, read from the .aux."""
    pages = collections.defaultdict(set)
    for ids, _n, pg in re.findall(r'\\rvrecord\{([^}]*)\}\{(\d+)\}\{([^}]*)\}', open(aux_path, encoding='utf-8').read()):
        for i in ids.split(','):
            pages[i].add(pg)
    for cid, _rev, _desc in comments:
        print(f'{cid:8s} pages: {", ".join(sorted(pages[cid], key=lambda p: (len(p), p))) or "NONE"}')
