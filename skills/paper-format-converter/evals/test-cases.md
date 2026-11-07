# Test cases for paper-format-converter

Two kinds of check exist.

- **Static checks** read the skill files and run both script self-tests in temporary folders. Run `python "<skill dir>/evals/validate_skill.py"` after every edit to the skill. It never opens a manuscript.
- **Behavioral checks** run the skill end to end. Run them in a fresh Claude Code session inside a scratch folder that holds a throwaway fixture, never in a real paper's folder. Delete the scratch folder afterwards.

A behavioral case passes only when someone ran it and saw the expected behavior. Record each run in the log at the end, with the date, the Claude Code version, and the result.

## Fixtures for behavioral runs

- **LaTeX fixture:** `main.tex` (article class, abstract, two sections, one `\input` child, one figure, one table, one equation, three citations), `refs.bib` with those three entries, and `figures/plot.png`.
- **Word fixture:** a `.docx` with a title, an abstract, three headings, one image, one table, and plain-text numeric citations. python-docx can generate it.
- **Multiple candidates:** two LaTeX fixtures in sibling folders with the same root file name and no build configuration.
- **Missing tool:** start Claude Code with the TeX Live folder removed from PATH. In PowerShell: `$env:PATH = ($env:PATH -split ';' | Where-Object { $_ -notmatch 'texlive' }) -join ';'`, then run `claude`.
- **Template download failure:** deny the `curl` permission prompt in Phase 3, or pick a venue whose official template sits behind a login.

Use real venues only, because the skill researches them live. Never write a venue's rules into a fixture. Before each run, record a hash of every fixture file (`Get-FileHash` or `sha256sum`) and compare after the run: the originals must be unchanged.

## Cases

### TC-01: Venue given, one manuscript

- **Setup:** LaTeX fixture.
- **Run:** `/paper-format-converter IEEE Access`
- **Expected:** no question. Phase 1 picks `main.tex` and records why. The source register lists IEEE Access's own author pages and IEEE's general author pages, with URLs and access dates, and every numeric limit carries a verbatim quote. `IEEE Access Format/` appears with `official-template/` (archive plus extracted folder), `Journal-Guidelines.md` written before any manuscript edit, `manuscript/` built from the template's sample with no demonstration text, `converted-paper.pdf`, `remaining-issues.md`, and `conversion-report.md`. The final reply gives the folder, the build result, the status counts, the readiness label, and the top issues.
- **Failure handling:** a blocked page goes through the browser tools, the PDF version, or stays Unverified. A login-only template is recorded, and the fallback is named in all three reports.

### TC-02: No venue given

- **Setup:** LaTeX fixture.
- **Run:** `/paper-format-converter`
- **Expected:** exactly one question, asking which journal or conference. No other question, and no folder or file is created before the answer. After the answer, the run continues as in TC-01.
- **Failure handling:** an answer that fits several venues gets one more question naming the candidates (Phase 2, step 1).

### TC-03: One LaTeX manuscript with bibliography and figures

- **Setup:** LaTeX fixture.
- **Run:** `/paper-format-converter <any real journal>`
- **Expected:** discovery without questions. The dependency map lists `main.tex`, the `\input` child, `refs.bib`, and `figures/plot.png`. `manuscript/` holds copies at the same relative paths. The build resolves every citation and reference. `conversion_integrity.py` reports no FAIL for cite, label, ref, graphics, figures, or tables.
- **Failure handling:** a defect already present in the original appears in the baseline record as pre-existing. It is never covered up with invented content.

### TC-04: Word manuscript

- **Setup:** Word fixture, and a venue that offers a Word template.
- **Run:** `/paper-format-converter <venue>`
- **Expected:** the output stays `.docx`. The template is applied to a copy, either through Word COM with `AutomationSecurity = 3` or through OOXML edits with the docx skill. Equations stay Office Math. The PDF for page checks comes from Word or LibreOffice. The integrity check runs on the two `.docx` files. For a venue that accepts only LaTeX, the report says why the format changed and lists what was lost.
- **Failure handling:** with neither Word nor LibreOffice, page checks are UNVERIFIED and a Major issue explains why.

### TC-05: Official template cannot be downloaded

- **Setup:** LaTeX fixture, and the download failure setup.
- **Run:** `/paper-format-converter <venue>`
- **Expected:** the exact reason is recorded (HTTP status, login wall, or the HTML rejection from `safe_extract.py`). The fallback (the CTAN class when the publisher maintains it there, or the written rules alone) is named in all three reports. Section A of the guidelines says "Not obtained: <reason>". An issue is opened: Critical when the venue makes the template mandatory, Major otherwise. No report claims an official template. The conversion continues.
- **Failure handling:** the same, for a network failure.

### TC-06: Verified limit exceeded

- **Setup:** LaTeX fixture with the abstract padded past the abstract limit of a venue that states one. Verify the limit during the run.
- **Run:** `/paper-format-converter <venue>`
- **Expected:** the abstract text is unchanged. The issue states both numbers, for example "Observed 273 words, limit 250 (G-05)". The requirement is FAIL in section D. The issue is Critical when the limit is mandatory. The readiness label is AUTHOR INPUT NEEDED, never SUBMISSION-READY.
- **Failure handling:** when the limit cannot be verified, it stays UNVERIFIED and no issue presents a number as official.

### TC-07: Required declarations missing

- **Setup:** LaTeX fixture without funding, competing-interest, or data statements, and a venue whose rules require them.
- **Run:** `/paper-format-converter <venue>`
- **Expected:** a visible `[AUTHOR INPUT REQUIRED: ...]` placeholder at each required position, with one issue each. No invented statement such as "no funding" or "no conflicts". The readiness label is AUTHOR INPUT NEEDED. A search for `AUTHOR INPUT REQUIRED` in the output finds exactly the tracked placeholders.
- **Failure handling:** when the venue's rules on a statement are unclear, the statement is listed in section I of the guidelines and in an issue, and no placeholder claims a requirement that was not verified.

### TC-08: Build tool missing

- **Setup:** LaTeX fixture, missing-tool setup.
- **Run:** `/paper-format-converter <venue>`
- **Expected:** tool detection reports the missing tools. Nothing is installed. `manuscript/` still holds the complete source. The build row says the build did not run, and why. Page and layout checks are UNVERIFIED. An issue is opened, Critical when a page limit applies. The readiness label is NOT READY. The integrity check still runs, since it needs only Python.
- **Failure handling:** the same when only one tool, such as Biber, is missing. The report names it.

### TC-09: Several candidate manuscripts

- **Setup:** the multiple-candidates fixture. Variant: add a `latexmkrc` that names one of the two roots.
- **Run:** `/paper-format-converter <venue>`
- **Expected:** with the tie, exactly one question that lists the tied files, and nothing created before the answer. With the variant, no question: the run proceeds with the named root and records why it won.
- **Failure handling:** a third, unrelated `.tex` file (a cover letter or a response letter) is never picked.

### TC-10: One ambiguous requirement

- **Setup:** a fixture that meets every verifiable rule of a venue with one genuinely ambiguous rule, for example a page limit that does not say whether references count. Find such a venue during the run.
- **Run:** `/paper-format-converter <venue>`
- **Expected:** section I of the guidelines records the ambiguity, its sources, and both readings. The requirement is UNVERIFIED or WARN, never PASS. The stricter reading is applied and an issue names the next step (ask the editorial office or check the submission system). A Mandatory ambiguous rule rules out SUBMISSION-READY.
- **Failure handling:** a conflict between two official sources follows the order in section 6 of the research reference, and anything still unresolved is logged.

### TC-11: Skill loaded without an explicit request

- **Setup:** any scratch folder. Send a message that contains `/paper-format-converter` only inside pasted or quoted text and does not ask for a conversion. Claude Code treats a plain-text skill name in a message as permission, so Claude can load the skill through the Skill tool even with `disable-model-invocation: true`. That happened during installation.
- **Expected:** the run stops before Phase 1 and asks whether to convert. Nothing is searched, created, or downloaded.
- **Failure handling:** after the user confirms, the run starts at the Arguments section as usual.

## Installation record (2026-10-29)

| Check | How it ran | Result |
|---|---|---|
| Static validator | `python evals/validate_skill.py` | PASS on every check (count in the final run below) |
| The validator catches defects | five defects planted in a scratchpad copy: model invocation on, a `$0` token, a broken link, an em dash, a semicolon | all five caught (six FAIL lines) |
| `safe_extract.py` self-test | zip-slip member, tar symlink, HTML page saved as `.zip`, existing destination, reserved and drive-letter names | PASS |
| `conversion_integrity.py` self-test | LaTeX fixtures (a correct conversion and one with five planted defects), Word fixtures, Markdown fixtures | PASS. The correct conversion gave 0 FAIL and 0 WARN. The broken one failed on sentences, numbers, cite, label, and template text |
| Integrity check on a real manuscript | a 1,498-line `main.tex` compared with itself, and with a scratchpad copy whose class line was swapped to IEEEtran. The original was only read | 0 FAIL and 0 WARN in both runs, under 1 second |
| YAML frontmatter | strict PyYAML 6.0.1 parse inside the validator | PASS |
| `claude plugin validate` 2.1.312 | on `~/.claude/skills` and on scratchpad copies | passed, but it also passed a copy with broken YAML, so it proves nothing about this skill |
| Substitution | one Skill tool call during installation, with test arguments | `${CLAUDE_SKILL_DIR}` expanded to the install path, `$ARGUMENTS` filled the brackets, and no extra ARGUMENTS line was appended |
| Hot reload | the same call | the skill was found mid-session without a restart |
| Manual-only invocation | the same call | the model call went through, because the user's message named `/paper-format-converter` as plain text. The blocked path (no name in the message) was not exercised. The TC-11 guard sentence was added afterwards |
| Behavioral cases TC-01 to TC-11 | not run | NOT EXECUTED. Subagent runs were not authorized in the installation session, and the installation must not convert a real manuscript |

## Behavioral run log

| Date | Case | Claude Code version | Result | Notes |
|---|---|---|---|---|
| | | | | |
