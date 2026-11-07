"""Worked example: highlighted revised manuscript for the synthetic project in examples/demo/.

The demo manuscript and letter labels are placeholders, not research. Every operation below ties one
revised element of main.tex to the reviewer-comment IDs of the letter, using each kind of operation once.
Run it on a copy, never inside the skill folder:
    python example_build.py <project_dir>      # <project_dir> holds main.tex and response_to_reviewers.aux
then copy scripts/rvhighlight.sty next to <project_dir>/Example_Highlighted.tex and compile it twice with latexmk.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'scripts'))
from hl_build import *  # noqa: E402,F401,F403

P = sys.argv[1]
start(os.path.join(P, 'main.tex'), os.path.join(P, 'Example_Highlighted.tex'))

# Sentence-level highlight (W) for an edit inside an existing paragraph.
W(r'It shows how a revised sentence is tagged with the reviewer comment that it answers.', 'R1.1', 'Abstract')
# A new paragraph preceded by a blank line (BOX).
BOX('This paragraph was added in the revision', 'R1.2', 'Sec. 1')
# A corrected display equation (EQ), identified by its label.
EQ('eq:score', 'R2.1', 'Eq. (1)')
# A revised table (FLOAT), plus a row tag (T) and a further cell of that row (H).
FLOAT('tab:values', 'R2.2', 'Table 1')
T('Revised & 1.5', 'R2.2', 'Table 1')
H('2.5')
# A revised sentence that answers two comments.
W('The revised conclusion now states the limits of the demonstration explicitly.', 'R1.1,R2.1', 'Sec. 3')

COMMENTS = [
    ('R1.1', 'Reviewer 1', 'Clarity of the abstract and the conclusion'),
    ('R1.2', 'Reviewer 1', 'Statement of scope'),
    ('R2.1', 'Reviewer 2', 'Correction of the score equation'),
    ('R2.2', 'Reviewer 2', 'Revised values in Table 1'),
]

letter = labels_from_aux(os.path.join(P, 'response_to_reviewers.aux'), 'c:')
further = labels_from_aux(os.path.join(P, 'response_to_reviewers.aux'), 'sec:')['further']
rows = map_rows(COMMENTS, letter_pages=letter, default_page=further)
finish(guide(
    title='A Synthetic Manuscript for the Highlighting Example',
    venue_line='Demonstration build. Replace this line with the manuscript ID, revision number and venue.',
    header_label='Highlighted revised manuscript, demonstration',
    intro=("This version of the revised manuscript identifies the changes made in response to the reviewers' "
           "comments. Reviewer-comment IDs (for example R2.1) are those of the Response to Reviewers."),
    rows=rows,
    pdfmeta=r'\hypersetup{pdftitle={A Synthetic Manuscript for the Highlighting Example}}',
    cannot_show=['Deletions leave no visible text. List each deleted passage here with its comment ID.']))
