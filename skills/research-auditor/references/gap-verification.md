# Research-Gap Verification Protocol

The manuscript's gap claim is a hypothesis. This file is how you test it.

## Per-Gap Procedure

Run all seven steps for **every** gap the paper targets, including gaps that are implied rather than stated.

1. **State the gap exactly.** Quote or closely paraphrase, and record where it appears (section, page, line). Vague gaps get sharpened into a testable statement first — write both the paper's version and your testable version.
2. **Locate the claim's support.** Where does the manuscript claim or imply this gap exists? Which citations does it lean on? Read those citations — a gap propped up by papers that do not say what the manuscript implies is a finding in itself.
3. **Search independently.** Query the gap's concepts, not the paper's phrasing. Use the field's own vocabulary and known synonyms, since a gap often exists only in one terminology. Search at least three phrasings before concluding anything is absent.
4. **Cover the right time window.** Prioritize the last 5-10 years; add seminal older work where the problem's formulation originates. A gap claim about a fast-moving subfield needs the last 24 months checked specifically.
5. **Assign a verdict** from the five below.
6. **Name the challengers.** List papers that challenge, reduce, or contradict the gap. Even a surviving gap is usually narrower than claimed — say how much narrower.
7. **State the residue.** After the existing literature is accounted for, what remains genuinely unresolved? That residue, not the paper's original claim, is the real gap the paper can defend.

## The Five Verdicts

| Verdict | Criteria | Consequence for the paper |
|---|---|---|
| **Real and insufficiently studied** | Repeated searches surface no work addressing it; adjacent work stops short | Gap stands; strengthen the citation trail supporting it |
| **Partially real but overstated** | Some prior work addresses part of it; the paper's framing exceeds what is unaddressed | Narrow the claim to the residue; cite the near-misses explicitly |
| **Already addressed** | Existing literature covers it, possibly under different terminology | Gap must be reframed or replaced; the paper's motivation is at risk |
| **Too narrow or weak to justify the paper** | Genuinely unaddressed but of low consequence to the field | Reposition around a consequence the field cares about |
| **Unclear — insufficient evidence** | Searches inconclusive, literature fragmented or paywalled | Report what is missing and what search would resolve it |

A verdict without citations is not a verdict. Record the searches you ran.

## Gap Taxonomy

Classify each gap. Different types carry very different weight with reviewers, and conflating them is a common way papers overclaim.

| Type | What it is | Typical strength |
|---|---|---|
| **Research gap** | A question the field has not answered | Strongest, if genuinely open |
| **Methodological limitation in prior work** | Existing work answers the question, but with a flaw | Strong if the flaw materially changes conclusions |
| **Deployment / practical gap** | Known in theory, unvalidated in real conditions | Strong in applied venues, weak in theoretical ones |
| **Dataset / geographic gap** | Approach untested on this data, region, or population | Weak alone; strong if the setting changes the conclusion |
| **Theoretical gap** | No formal framework, proof, or model exists | Strong, but demands theoretical contribution to match |
| **Validation gap** | Claims exist but are unverified or unreproduced | Moderate; needs rigorous validation design to pay off |
| **Merely unexplored idea** | Nobody has done it, and there may be a reason | Weakest. Not automatically a research gap. |

For each gap, say which type it actually is versus which type the paper implies it is. That mismatch is one of the most common sources of reviewer rejection.

## Trigger-Phrase Audit

Find every occurrence of these in the manuscript and verify each one individually:

- "no studies", "no existing work", "has not been studied"
- "few studies", "limited attention", "little attention", "scarce"
- "first", "the first to", "for the first time"
- "novel", "new approach", "unprecedented"
- "state-of-the-art", "outperforms existing methods"
- "existing approaches fail", "current methods cannot"
- "remains unexplored", "open problem"
- "to the best of our knowledge"

Report each as a row: phrase, location, what it asserts, verdict, evidence. "To the best of our knowledge" is not a defense against a paper that already did it — flag those specifically, since reviewers who know the field will find them.

## Checks That Catch Missed Prior Work

- Search the method name **and** its generic description; the same technique travels under different names across communities
- Check the closest papers' own related-work sections and their forward citations
- Check adjacent fields that solve a structurally identical problem
- Check for preprints and recent conference versions, which often precede the claim
- Check whether a survey or review already catalogues what the paper calls unexplored

## Recording Format

For each gap, the report carries: gap statement, manuscript location, gap type (claimed vs. actual), verdict, evidence with citations, challenging papers, remaining residue, and the searches performed. Incomplete rows are marked incomplete rather than quietly dropped.
