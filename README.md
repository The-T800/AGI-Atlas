# AGI Atlas

**[Launch the live app on GitHub Pages](https://the-t800.github.io/agi-atlas/)**

**English** | [简体中文](README.zh-CN.md)

[![AGI Atlas](docs/preview.png)](https://the-t800.github.io/agi-atlas/)

**How far is AI from AGI?** We take *every* human job and *every* academic discipline as the denominator, score each item by the best published benchmark result, and count anything unmeasured as 0.

| Denominator | Size | AI reached |
| --- | --- | ---: |
| Jobs ([O*NET 31.0](https://www.onetcenter.org/database.html)) | 923 occupations · 18,838 tasks · 2,087 work activities | **0.91%** |
| Disciplines (GB/T 13745) | 2,656 fine-grained disciplines | **11.68%** |

- **Most of the gap is unmeasured, not failed.** 93% of human work has no benchmark at all; physical, care, repair and construction jobs score about 0.
- **Where AI is measured, it is strong.** On the 7% of work that has benchmarks, AI averages 42%. Writing code (96.6) and fixing software (80.0) score highest.
- **Computer & math occupations lead** at 7.6%.

👉 **[Open the interactive page](https://the-t800.github.io/agi-atlas/)** (also works offline: `docs/index.html`) · [Full report](reports/report.en.md)

## How it is computed

```
item score = coverage × benchmark SOTA        (best benchmark per item; none → 0)
coverage   = 1.0 direct · 0.5 partial          (× 0.3 / 0.1 if a discipline is only tested at level 2 / 1)
SOTA       = best score ÷ human baseline, or ÷ 100% when no baseline exists
AI reached = weighted average over all items in the denominator
```

Jobs are weighted by how much of each occupation's work an activity represents (O*NET task importance); every occupation counts equally. Disciplines count equally.

All factors live in [`data/research/progress.yaml`](data/research/progress.yaml); change them and rebuild.

## Data

| What | Where |
| --- | --- |
| 187 benchmarks | [`data/research/catalog.tsv`](data/research/catalog.tsv) |
| 3,706 scores with source, hash and locator | `data/scores/frontier_scores.yaml` (generated) |
| Denominators | [`data/denominators/`](data/denominators) |
| Benchmark → job activity / discipline | [`data/mappings/`](data/mappings) (each row has a reason) |
| Translations | [`data/i18n/`](data/i18n) |

Scores come from official leaderboards, independent evaluations (Epoch AI), papers and vendor model cards; each record keeps its source snapshot and SHA-256.

**Limitations.** Mappings are hand-labelled and not yet independently reviewed. Some scores are vendor-reported. O*NET reflects the US occupational system and is not employment-weighted. GB/T 13745 lists discipline names only.

## Quick start

Requires Python 3.12+ and [uv](https://docs.astral.sh/uv/).

```bash
uv sync --extra dev
uv run agi-atlas validate      # check data
uv run agi-atlas report        # reports/report.{zh,en}.md
uv run agi-atlas site          # docs/index.html
uv run pytest
```

Rebuild generated data (offline, from committed snapshots):

```bash
uv run python scripts/build_catalog.py
uv run python scripts/import_public_scores.py
uv run python scripts/build_models.py
uv run --extra build python scripts/build_denominators.py   # downloads O*NET / GB/T 13745 on first run
```

## Contributing

Add a benchmark, a score, or fix a mapping — see [CONTRIBUTING.md](CONTRIBUTING.md).

## License

Code: [MIT](LICENSE). Third-party data keeps its own license: O*NET (CC BY 4.0, U.S. Department of Labor), Epoch AI (CC BY 4.0), METR, papers and model cards as cited. Translations of O*NET and GB/T 13745 names are unofficial.
