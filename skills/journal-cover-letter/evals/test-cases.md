# Test cases for journal-cover-letter

Re-run these after editing the skill. Use synthetic manuscripts in the session scratchpad, never a real project folder, and never send a test letter anywhere. Journal research is real and must be redone on every run, since policies change.

Static check first: `python scripts/check_letter.py --selftest` must print `SELFTEST: PASS`.

## Scenarios

| ID | Manuscript (input format) | Target journal | Trap | Expected behavior |
|---|---|---|---|---|
| S1 | Observational cohort study (.md) | PLOS ONE | Intro claims "the first study" while citing two earlier studies. PLOS requires Academic Editor suggestions in the letter, and the notes say "not chosen yet". | No novelty claim. "Associated with", not causal verbs. The fit paragraph argues rigor, because PLOS ONE judges validity, not significance. Letter states article type, prior interactions, opposed reviewers. The missing editor suggestion is asked, not invented. The check script fails while it stays `[[...]]`. COI, funding, and ethics stay out (submission system and Methods). |
| S2 | Systematic review (.docx), with an old `cover_letter.tex` and `.pdf` from another journal in the folder | Sensors (MDPI) | The old letter has `\documentclass` and must not be taken as the manuscript. The paper was declined earlier by another MDPI journal. | Discovery picks the .docx. The old pair is renamed `cover_letter_v1.*`, never overwritten. Article type "Review" with PRISMA and registration stated. MDPI's two mandatory statements appear verbatim (pass them to `--require`). The prior MDPI submission and its ID are acknowledged. No reviewer names in the letter. |
| S3 | AI/engineering paper extending a conference paper (.tex) | Engineering Applications of Artificial Intelligence (Elsevier) | Abstract says "state-of-the-art" and "generalizes across topologies", but the method wins on 2 of 3 feeders and was tested only on reconfigurations of one feeder. The manuscript cites "Sections 5 to 7" but has 5 sections. No bibliography confirms the conference paper is cited. | Measured statements replace the overclaims (wins on two feeders, on par on the third). The letter details how the journal version differs from the conference paper, as the guide requires. No originality or exclusivity sentence, because Elsevier treats it as implied by submission. The section mismatch and the missing citation are flagged to the user, not repeated. |

## Edge cases

| ID | Situation | Expected behavior |
|---|---|---|
| E1 | No journal named anywhere | One question: which journal. Nothing created first. |
| E2 | No TeX compiler (rename PATH in a sandbox) | `check_letter.py` exits 2 with BLOCKED. The `.tex` is delivered and the reply says the PDF is blocked. |
| E3 | Text overflows to two pages | Script fails on `pages`. Text is cut in the documented order before any layout change. |
| E4 | The official page returns 403 to WebFetch | The browser route is used, and the source is recorded as read in the browser. |
| E5 | The journal requires a declaration that no file confirms | The user is asked. The letter is not delivered with an assumed statement. |

## Last run: 2026-11-14

- Self-test 6 of 6 passed. S1, S2, and S3 each ended at `RESULT: PASS`, one A4 page, 292, 310, and 313 body words. Each render was read.
- WebFetch reached PLOS. MDPI and Elsevier returned 403 and were read through the browser (E4 confirmed).
- S1 with the open editor placeholder failed on `placeholders` as intended (E5 path).
- S3 first compiled to two pages (376 words) and passed after text cuts only (E3 confirmed).
- Fixes from this run: the title no longer repeats in paragraph 1, the subject line never hyphenates, `\hyphenation{}` keeps journal names whole, and `\emergencystretch` stops the overfull line that the hyphenation fix caused.
- Not run: E1, E2, and fresh-context subagent runs of the full skill. These tests were executed by the session that wrote the skill.
