# Subject classification and freshness

## Official reference set

AGI Atlas uses the complete [OpenAlex topic hierarchy](https://help.openalex.org/data/topics):
4 domains, 26 fields, 252 subfields and 4,516 topics. These are research-literature
clusters, not an exhaustive inventory of human knowledge or capability. The topic
names and descriptions are source-authored, including their machine-generated labels.
Domain and field Chinese labels are unofficial translations; deeper names remain English.

The latest complete public release found on 2026-10-05 was **2026-09-23**, downloaded
on 2026-10-05 from the [official S3 snapshot](https://help.openalex.org/access/snapshot).
The live anonymous API ran out of shared IP budget after 3,200 topics; those incomplete
pages are excluded from the published dataset. The complete public snapshot is used
consistently across all four levels. It is not described as a complete same-day API snapshot.

`data/research/sources/openalex/manifest.json` retains every original file URL, retrieval
time, release date and SHA-256. The original release manifests and compressed JSONL
records are committed. The builder rejects duplicate IDs, missing pages, broken lineage,
count changes and tampered source files. It derives counts from the source, not constants.

## Independent axes and mapping scope

`data/taxonomy/capabilities.json` defines 12 project capability annotations. All 187
benchmarks have capability links in `data/mappings/benchmark_openalex.tsv`. Subject
links target a field, subfield or topic based on tested task content; general tasks can
remain academically unassigned. A benchmark paper about machine learning does not imply
that its questions test machine-learning knowledge.

Each mapping records a reason, source URL, partial fit and `benchmark_only` score scope.
The matrix counts distinct benchmarks per field and capability. Parents can summarize
child evidence for navigation; a parent mapping does not establish evidence in any child.
Only two topics currently have explicit links (software testing/debugging and financial
analysis). The remaining detailed mapping work is visible as unknown, not fabricated coverage.

Benchmark results remain in their original comparable version/protocol/subset/metric/unit
groups. A combined exam score is never used as a score for every named discipline.
No subject mastery percentage or overall AGI completion percentage is computed. The former
Nature index has been retired and is not numerically comparable with this evidence map.
The O*NET work proxy remains a separate existing metric with its own zero-contribution rule.

## Score dates

Benchmark sources were refreshed on 2026-10-05. This updates retrieval provenance only.
The page retains evaluation date, publication date and retrieval date separately.
Current subject evidence highlights scores dated within 365 days before taxonomy retrieval:
evaluation date takes precedence; publication date is used only if evaluation is unknown.
Undated, historical and future-dated records do not qualify. They remain in score details.
A benchmark's age does not invalidate a recent result on it; a recent download does not
validate an old result. The window is a display convention, not a scientific freshness threshold.

## Rebuild and refresh

```bash
uv run python scripts/build_openalex.py            # deterministic offline rebuild
uv run python scripts/build_openalex.py --snapshot # latest complete public release
uv run python scripts/build_openalex.py --refresh  # live API; optional OPENALEX_API_KEY
uv run python scripts/collect_sources.py --refresh
uv run python scripts/import_public_scores.py
uv run python scripts/build_models.py
uv run agi-atlas report
uv run agi-atlas site
```

Keys are sent in an Authorization header and never saved in source URLs. The optional
`.work/openalex-api-key.txt` local file is ignored by Git. OpenAlex data is CC0.
