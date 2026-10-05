# Subject classification

The academic reference set now uses the [Nature public subject directory](https://www.nature.com/subjects),
captured on 2026-10-05: **8 categories, 95 unique subject IDs, and 105 category memberships**.
The directory covers biological sciences, business and commerce, Earth and environmental
sciences, health sciences, humanities, physical sciences, scientific community and society,
and social science.

This replaces the previous national discipline classification. The old reference table,
translation table and mappings have been retired from the active dataset. The new index
has a different denominator and different mappings; its value must not be compared
directly with the former percentage.

## Scope and counting

- This is Nature's public two-level browsing directory, not its entire ontology or an
  exhaustive inventory of human knowledge. Names and memberships follow the source.
- A subject such as ecology can appear in multiple categories. It counts once in the
  overall denominator; category subtotals overlap and must not be summed.
- The mosaic places a cross-listed subject under its first directory occurrence for
  layout only. All memberships remain visible in the full directory.
- Deeper links labelled "Related Subjects" are not assumed to be parent-child links.
- Chinese labels are unofficial project translations. No Nature endorsement is implied.

## Benchmark mappings

Mappings are independently curated project data in `data/mappings/benchmark_nature.tsv`,
with a reason and task-definition URL for every link. Nature provides topic names, not
the benchmark mappings or progress scores.

All current academic links are **partial**. A coding task samples computing, a medical
conversation samples care knowledge, and an exam category samples a field. None proves
mastery of the complete subject. Some imported results are aggregate benchmark scores,
so mapped values are task proxies, not measured subject-specific scores.

Subjects with no task mapping remain in the denominator at zero under the project's
existing convention. The resulting index depends on this directory, the mappings and
the scoring factors; it is not a calibrated percentage of AGI achieved.

## Reproducibility

The original directory HTML, retrieval date and SHA-256 are retained in
`data/research/sources/`. Rebuild the topic tables offline with:

```bash
uv run python scripts/build_nature.py
uv run agi-atlas report
uv run agi-atlas site
```

Tests verify source labels, cross-listings, unique counting and the lack of score
inflation from overlapping categories. CI checks that regenerated files match the
committed snapshot.
