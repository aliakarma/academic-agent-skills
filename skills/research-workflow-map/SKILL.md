---
name: research-workflow-map
description: Use when a research or paper task spans more than one academic skill, when it is unclear which skill to run next, or when planning work from an idea (title and abstract) through gap finding, drafting, literature, code, review, figures, auditing, polishing, reference checks, and the cover letter. Also use when the user asks how the academic skills connect, what order to run them in, or what a skill needs before it starts.
---

# Research Workflow Map

This skill routes work across the 24 academic skills in this collection. It holds the run order, what each skill needs as input, and what it hands on. It does no research or writing itself. Pick the entry point, then invoke the named skills with the Skill tool and follow their own workflows.

**Rule:** every skill's own `## Related skills` section agrees with this map. When a needed skill is not installed, say so and continue with what the current skill can do alone. Never fake its output.

## The paper cycle: from an idea to a submitted paper

The user brings an idea as a title and abstract, and optionally research questions, methodology, datasets, or results. Fourteen steps take it to a submission-ready paper with a cover letter. `→` runs in sequence, `+` runs together.

| Step | Skills | Input it needs | Output it hands on |
|---|---|---|---|
| Step 1. Find the gap | `finding-gap` | Title and abstract, plus any research questions, methodology, datasets, or results | Validated gap in that domain, research questions, source ledger |
| Step 2. Draft | `idea-to-paper` | The title, abstract, and other inputs, plus the step 1 gap | Initial draft built on that gap: LaTeX project, `references.bib`, PDF, `PAPER_REPORT.md` |
| Step 3. Literature | `literature-review` (with its integration stage) | The draft and the gap | Verified literature cited in the paper, `literature_review.md` |
| Step 4. Project report | `paper-to-project-report` | The paper with its literature | `PROJECT_REPORT.md`, the engineering spec for the repository |
| Step 5. Code repository | `project-report-to-github` | `PROJECT_REPORT.md` and the paper | Runnable, tested repository |
| Step 6. Simulated review | `peer-review` | The paper and its repository | Three reviewer reports, meta-review, revision roadmap |
| Step 7. Revision | `manuscript-revision` | The paper and the step 6 reports | Revised paper, every comment addressed |
| Step 8. Figures | `nanobanana-prompt-generator` → Google Flow (by the user) → `figure-rebuild` | TikZ diagrams in the revised paper | Final vector figures with selectable text |
| Step 9. Deep audit | `audit-paper` + `research-auditor` | The paper with its final figures, and the project folder | `audit.md` (I-001...) and `MASTER_PAPER_ASSESSMENT.md` (R-001...) |
| Step 10. Repair | `repair-paper` | Both step 9 reports | Repaired paper, `REPAIR_REPORT.md` that accounts for every I- and R- ID |
| Step 11. Polish | `universal-manuscript-polish` | The repaired paper | Polished paper |
| Step 12. Remove AI patterns | `text-humanizer` + `clean-user-facing-text` | The polished paper | Natural, clean prose |
| Step 13. Verify references | `reference-verify` | The final `.bib` | Every entry checked one by one against its publisher or registry record |
| Step 14. Cover letter | `journal-cover-letter` | The final paper and the target journal | One-page cover letter that follows the journal's policy |

The cycle ends at step 14. A user who already has material can enter at a later step: a finished draft starts at step 6 or step 9, and a `.bib` to check starts at step 13.

## Other-purpose skills

These skills sit outside the paper cycle. Run them when the task calls for them.

| Skill | When to run it |
|---|---|
| `repo-forensic-audit` | Review a whole GitHub repository: right after step 5, or on any research repository |
| `response-to-reviewer` | Write the response letter for real comments from a journal or conference |
| `highlighted-pdf-from-reviews` | After every real review comment is fixed and the response letter exists: highlight the revised parts of the paper |
| `paper-to-pptx` | Make a PowerPoint deck from a paper, report, or similar document |
| `paper-format-converter` | Move a paper from one journal or conference format to another |
| `readme-improvement` | Improve a repository README so it is professional and matches the project |
| `asd-ste100` | Make an easy-to-read HTML explainer of a paper, project, or codebase in Simplified Technical English. The user must first download the ASD-STE100 PDF from the official ASD website and supply it |

## Who calls whom

| Skill | Needs first | Uses during the run | Hands on to |
|---|---|---|---|
| finding-gap | a title and abstract, or a topic (step 1, the entry point) | reference-verify | idea-to-paper |
| idea-to-paper | the title and abstract plus the finding-gap gap | literature-review scripts (required), reference-verify, nanobanana-prompt-generator, figure-rebuild, universal-manuscript-polish (required), text-humanizer | literature-review |
| literature-review | the draft and the gap | reference-verify, universal-manuscript-polish and text-humanizer (integration stage) | paper-to-project-report |
| paper-to-project-report | the paper with its literature | none | project-report-to-github |
| project-report-to-github | `PROJECT_REPORT.md` and the paper | none | peer-review, repo-forensic-audit (optional) |
| peer-review | the paper and its repository | none | manuscript-revision |
| manuscript-revision | peer-review reports, or a real decision letter | response-to-reviewer, reference-verify, universal-manuscript-polish, text-humanizer (all required), literature-review, figure-rebuild | nanobanana-prompt-generator; after a real review, highlighted-pdf-from-reviews |
| nanobanana-prompt-generator | the revised paper's TikZ diagrams | none | Google Flow (by the user), then figure-rebuild |
| figure-rebuild | reference images from Google Flow | none | audit-paper, research-auditor, paper-to-pptx |
| audit-paper | the paper with final figures | text-humanizer (optional) | repair-paper |
| research-auditor | the paper and its project folder | literature-review, repo-forensic-audit | repair-paper |
| repair-paper | `audit.md` from audit-paper and `MASTER_PAPER_ASSESSMENT.md` from research-auditor | universal-manuscript-polish (required), text-humanizer | universal-manuscript-polish |
| universal-manuscript-polish | the repaired paper | text-humanizer, reference-verify, figure-rebuild, clean-user-facing-text | text-humanizer, clean-user-facing-text |
| text-humanizer | the polished paper, or any prose | none | clean-user-facing-text, reference-verify |
| clean-user-facing-text | text from text-humanizer | text-humanizer | reference-verify |
| reference-verify | the final `.bib` | none | journal-cover-letter, literature-review (replacements) |
| journal-cover-letter | the final paper and a journal | text-humanizer (required) | submission |
| repo-forensic-audit | a code repository | none | research-auditor, manuscript-revision, readme-improvement |
| response-to-reviewer | real reviews and the revised manuscript | text-humanizer | highlighted-pdf-from-reviews |
| highlighted-pdf-from-reviews | revised LaTeX and the response letter | none | resubmission |
| paper-to-pptx | a paper or report | figure-rebuild, Anthropic `pptx` skill (required, not in this collection) | none |
| paper-format-converter | a paper and a target venue | figure-rebuild | universal-manuscript-polish, journal-cover-letter |
| readme-improvement | a repository README | none | none |
| asd-ste100 | a paper, project, or codebase, plus your own ASD-STE100 PDF | none | none |

"Required" means the skill runs files from the other skill's folder, so install both. All other links are hand-offs: run or offer them when the task calls for them.

## Routing common requests

| The user says | Start with | Then |
|---|---|---|
| "Here is my title and abstract, write the paper" | finding-gap | idea-to-paper, then the rest of the paper cycle, steps 3 to 14 |
| "Is my gap real / is this novel?" | finding-gap | literature-review |
| "I have a draft, get it ready to submit" | peer-review | steps 7 to 14 |
| "Check my references" | reference-verify | literature-review for replacements |
| "Make my figures publication quality" | nanobanana-prompt-generator (TikZ) or figure-rebuild (raster) | audit-paper |
| "We got reviews from the journal" | manuscript-revision | response-to-reviewer, highlighted-pdf-from-reviews |
| "Rejected, send it to another journal" | paper-format-converter | universal-manuscript-polish, journal-cover-letter |
| "Build the code for this paper" | paper-to-project-report | project-report-to-github, repo-forensic-audit, readme-improvement |
| "Make slides from this paper" | paper-to-pptx | none |

## Common mistakes

| Mistake | Fix |
|---|---|
| Drafting before the gap is found | Run finding-gap first, so idea-to-paper writes the paper inside a validated gap |
| Polishing before auditing | Run steps 9 and 10 first, so polish does not hide substance problems |
| Running literature-review without its integration stage in the paper cycle | Ask it to cite the verified works in the paper, so the literature actually enters the manuscript |
| Repairing only the audit.md issues | repair-paper accounts for every R- finding in `MASTER_PAPER_ASSESSMENT.md` too |
| Converting the template after polishing | Convert first, then polish in the new template |
| Writing a response letter before the revision | manuscript-revision first, response-to-reviewer second |
| Writing a submission cover letter with response-to-reviewer | Use journal-cover-letter. response-to-reviewer is for revision letters only |
| Running a hand-off silently | Tell the user which skill runs next and why |
