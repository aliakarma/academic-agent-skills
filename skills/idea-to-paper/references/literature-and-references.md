# Literature Grounding and References

Every reference in `references.bib` is a real publication, generated from its registration record, machine-verified, and cited only for what you saw it say. The scripts come from the Literature-Review skill (`$LIT` is the `scripts/` folder of the sibling `literature-review` skill, as defined in SKILL.md). Run any of them with `--help`.

## 1. Plan the queries

From the Input Map, write four to six concept families into `PAPER_REPORT.md`:

- the core method (for example "trust-weighted federated aggregation")
- the application domain ("industrial IoT intrusion detection")
- each technical component the method combines
- the baselines and the datasets you intend to use
- evaluation methods and metrics specific to the topic
- known limitations, attacks, or competing approaches

Search each family in the vocabulary of every community that works on it (security, ML, systems, HCI). Aim for 40 to 60 candidates so that 25 to 40 survive.

## 2. Discover

Use what the session has, and log what failed:

| Source | Call |
|---|---|
| WebSearch | Topic queries, then follow publisher, arXiv, and proceedings links |
| Semantic Scholar | `curl -s "https://api.semanticscholar.org/graph/v1/paper/search?query=<q>&fields=title,year,venue,externalIds,abstract&limit=20"` |
| OpenAlex | `curl -s "https://api.openalex.org/works?search=<q>&filter=from_publication_date:2021-01-01&per-page=25&select=doi,title,publication_year,primary_location"` |
| Crossref | `curl -s "https://api.crossref.org/works?query.bibliographic=<q>&rows=10"` |
| Proceedings without DOIs | proceedings.neurips.cc, proceedings.mlr.press, openreview.net, aclanthology.org, usenix.org |

URL-encode queries. Never send the user's email address to any service.

Selection rules:

- At least 60% from 2021 to 2026. Foundational papers (the original method, the dataset paper, the baseline papers) are welcome at any age.
- Prefer the peer-reviewed version over the arXiv version when both exist.
- Include the paper that introduced each dataset and each baseline you use.
- Prefer primary studies for empirical claims. Use surveys to map a field.
- A retracted paper is excluded unless the paper discusses the retraction.

## 3. Generate BibTeX from records

Put one DOI per line in `_build/dois.txt`, then:

```bash
python -I "$LIT/doi2bib.py" --file _build/dois.txt --bib references.bib --append
```

The first run on an empty file needs `references.bib` to exist (create it empty). For a venue without DOIs, build the entry from the official proceedings page you opened, with a `url` field pointing at that page. Never type author lists, titles, or years from memory.

## 4. Verify

```bash
python -I "$LIT/verify_refs.py" references.bib --out _build/verify.csv --raw-dir _build/raw --strict
```

| `machine_check` | Action |
|---|---|
| MATCH | Keep |
| PARTIAL | Correct the field from the record in `_build/raw/`, rerun, keep when it matches |
| NO_DOI_CANDIDATE | Fetch the candidate DOI's record, confirm title, authors, and year, then regenerate with doi2bib |
| MISMATCH, DOI_NOT_FOUND, NO_DOI_NO_MATCH | Remove the entry and every citation of it |
| ERROR | The check did not run. Retry later. The entry stays out until it passes |

Also run `python -I "$LIT/audit_citations.py" main.tex --quiet-uncited` once the paper cites the entries. It catches missing keys, duplicate keys, and unescaped `%` or `&` in the bib.

If verification cannot reach the minimum count, report the shortfall in `PAPER_REPORT.md` and the final reply. `check_paper.py` fails with E21 until it is met. Never fill the gap from memory.

## 5. Read before you cite

| What you reached | What you may cite it for |
|---|---|
| Full text | Specific results with numbers and conditions, method details, limitations |
| Abstract | Only what the abstract states |
| Metadata only | That the work exists and its general topic |
| A search snippet or an AI summary | Nothing. Retrieve the source or drop it |

Keep `_build/sources.csv` while drafting, one row per entry:

```text
key,doi_or_url,machine_check,access,supports
he2016deep,10.1109/cvpr.2016.90,MATCH,ABSTRACT,"II-A: residual connections ease training of deep networks"
```

## 6. Place citations

- Put each citation at the clause it supports, not in a cluster at the end of a paragraph.
- Every baseline, dataset, metric definition taken from prior work, and number quoted from prior work carries its citation.
- Related work compares the cited approaches on the paper's design dimensions. The comparison table lists only verified works.
- Spread citations across the paper: introduction (motivation), related work, method (design choices), setup (datasets, baselines, metrics), and discussion (where results agree or disagree with prior findings).

## 7. Datasets

Take dataset statistics (size, classes, features, collection period, license) from the dataset's official page or its paper, opened in this run, and cite it. Tag the dataset table `% SOURCE: <keys>`. A statistic you could not confirm is omitted, not estimated.
