# Editorial guidelines (Stages 4 to 6)

The editor reads the letter during initial assessment and asks four things: is this in scope, is it new, is it sound enough to send to reviewers, and is anything about the submission unusual. Answer those four quickly and accurately. A letter cannot rescue a weak paper, and inflated language makes the desk decision harder.

## Structure

Body of three to five paragraphs, between the salutation and "Sincerely,". The template supplies the sender block, date, recipient, subject line, and signature.

| Paragraph | Content | Size |
|---|---|---|
| 1. Opening | Ask the editor to consider the enclosed manuscript as the journal's article type, then state in one sentence what the study does. The subject line already carries the exact title, so do not repeat it here. | 2 sentences |
| 2. Problem and gap | The problem, why it matters to practice or theory, and the specific limitation of current work that the study addresses. Name the gap concretely ("existing intrusion detectors assume IID client data"), never "a gap remains in the literature". | 2 to 3 sentences |
| 3. Contribution and evidence | What the study contributes, how the approach differs from prior work, and the main results with the manuscript's own numbers and conditions. Explain why each component matters scientifically rather than listing components. | 3 to 5 sentences |
| 4. Journal fit | Connect the work to named topics in the journal's aims and scope and to its readership. Say which readers will use the result and how. | 2 to 3 sentences |
| 5. Declarations and close | Only the declarations the journal requires in the letter or that the editor must know (see below), then one sentence of thanks. | 1 to 4 sentences |

Paragraphs 2 and 3, or 4 and 5, may merge when the content is short. Do not add a paragraph about the authors.

## Length

- One page after compilation, always. This outranks every other target.
- Body of about 250 to 350 words. Go below that when the journal needs little, and above it only when the journal requires in-letter declarations and the page still fits.
- When the page overflows, cut in this order: (1) repetition between paragraphs, (2) background in paragraph 2, (3) methodological detail in paragraph 3, (4) declarations the journal collects elsewhere, (5) wordy sentences. Only then adjust layout, within the limits in `latex-production.md`.

## Language

- Formal academic English. American spelling unless the journal specifies British. Active voice by default ("We show", "The study tests").
- No em dashes and no semicolons (the check script fails both). Use commas, colons, parentheses, or two sentences.
- Concrete nouns and numbers over adjectives. One idea per sentence.
- Name the journal in italics (the template does this) and the manuscript title in quotation marks.
- Avoid: "prestigious", "esteemed", "renowned", "high-impact", "groundbreaking", "cutting-edge", "revolutionary", "game-changing", "paradigm shift", "novel" as decoration, "comprehensive" unless coverage is documented, "state-of-the-art" unless the paper benchmarks against it, "robust" without a robustness test, "seamless", "leverage", "utilize", "harness", "delve", "pave the way", "shed light", "fill a critical gap", "in today's world", "we believe our manuscript is suitable", "to the best of our knowledge, this is the first" unless the manuscript supports it.
- No flattery of the journal, no claims about its impact or reputation, no author biographies.

## Claim calibration

Use the verb the evidence supports.

| Evidence in the manuscript | Verbs | Example |
|---|---|---|
| Controlled experiment or formal proof | shows, demonstrates, proves (proofs only) | "The method reduces false alarms by 18% on three public benchmarks." |
| Observational, correlational, or a single dataset | indicates, suggests, is associated with | "Longer sleep was associated with higher grades in this cohort." |
| Method or framework with limited evaluation | proposes, introduces, describes | "We propose a scheduling policy and evaluate it in simulation." |
| Conceptual or position argument | argues, outlines, identifies | "The paper argues that audit logs must bind to execution." |
| Review or survey | synthesizes, maps, classifies, identifies gaps | "We synthesize 64 studies published from 2015 to 2025." |

Carry the manuscript's own qualifiers (dataset, setting, sample) with every number. A limitation the manuscript states may appear in the letter when it shows the scope honestly. It is never required.

## Article-type adaptations

- **Original research.** Paragraph 3 carries the main finding, the design that supports it (sample, setting, comparison), and one implication.
- **Systematic review or meta-analysis.** State the question, databases, period, number of included studies, reporting standard (PRISMA) and registration (PROSPERO or OSF) when the manuscript reports them, and what the synthesis adds beyond earlier reviews by name or year.
- **Survey or narrative review.** State the coverage, the organizing taxonomy or framework, why the review is needed now (new methods, earlier reviews outdated by a named development), and the open problems identified.
- **Technical AI or engineering paper.** State the engineering problem in the reader's terms, what the method does differently and why that matters, the evaluation setting (datasets, baselines, metrics), the headline result against the strongest baseline with numbers, and code or data availability when the manuscript states it. Keep architecture detail to one clause.
- **Extended conference paper.** Name the earlier paper (venue, year) and state concretely what is new. Follow the journal's rule on the required share of new material.
- **Short communication or letter.** Two or three paragraphs. Explain why rapid publication is warranted.
- **Special issue.** Name the issue title exactly. Name guest editors only if verified.
- **Resubmission after rejection at another journal.** Do not mention the earlier rejection unless the journal asks or the manuscript is a formal transfer.

## Declarations

Include a declaration when both conditions hold:

1. The journal asks for it in the letter, or it discloses something the editor must know: a related or overlapping publication, a conference version, a preprint when the journal requires disclosure, an earlier submission to this journal, a transfer, or a special-issue target.
2. Its truth is verified from the manuscript, the project files, or the user.

When the journal is silent, the standard originality and exclusive-submission sentence may appear if the user confirmed it. Leave funding, competing interests, ethics approval, consent, and data availability to the manuscript and submission system unless the journal requests them in the letter.

| Declaration | Verified only by |
|---|---|
| Original and not published elsewhere | The user, or a signed statement in the project |
| Not under consideration elsewhere | The user. Cross-check the project for parallel submissions |
| All authors approved the submission | The user, or an author agreement in the project |
| Competing interests | The manuscript's declaration section, or the user |
| Funding | The manuscript's funding or acknowledgment section |
| Ethics approval and consent | The manuscript (committee name and approval number) |
| Related publications or preprints | The manuscript's references or notes, or the user |
| Permissions for reproduced material | The figure captions, or the user |

Never write a declaration you cannot trace to that table. When the journal requires one and it cannot be verified, ask.

## Salutation and close

- "Dear Dr. Surname" or "Dear Professor Surname" only for a verified editor with the title as listed. Otherwise "Dear Editor". Never "Dear Sir/Madam" or "To whom it may concern".
- End the body with one sentence of thanks ("Thank you for considering our manuscript."). No promises of quick revisions and no requests for fast decisions.
- The signature block lists the corresponding author's full name, the designation "Corresponding author", the affiliation, and the institutional email, all taken from the manuscript.

## One example: the fit paragraph

Generic and unusable for any real journal:

> We believe our manuscript is well suited to your prestigious journal, as it addresses an important topic of broad interest to your readers.

Specific to the journal and the paper (illustrative journal and scope):

> The study falls within the journal's stated focus on "data-driven decision support for public health". Program managers who allocate screening resources can use the reported calibration curves directly, and methodologists will find the comparison of three missing-data strategies relevant to their own cohort studies.
