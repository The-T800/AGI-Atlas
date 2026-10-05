# Contributing / 参与贡献

Thanks for helping! Keep one clear change per pull request and say what evidence backs it.
欢迎贡献！每个 PR 只做一件清楚的事，并写明证据。

## Publishing conventions

English is the default for commits, pull requests, documentation, UI, CLI messages,
and new code comments. Chinese is an explicit localization; keep both translations
and preserve cited source material. See [AGENTS.md](AGENTS.md) for project conventions.

Before your first commit, configure this checkout with **your GitHub username** and
the **noreply email shown in GitHub Settings → Emails**. Do not reuse a workstation's
personal or employer email. Enable the repository's checks:

```bash
git config --local user.name YOUR_GITHUB_USERNAME
git config --local user.email YOUR_GITHUB_NOREPLY_EMAIL
git config --local user.useConfigOnly true
git config --local core.hooksPath .githooks
uv run python scripts/check_public_metadata.py --identity-only
```

Commit messages must use English with ASCII characters, for example
`Fix benchmark protocol grouping`. Hooks check new commits; CI checks the published
history. GitHub's web merge identity is also supported.

GitHub displays a Markdown preview in the repository; the interactive app runs on
[GitHub Pages](https://the-t800.github.io/agi-atlas/). Repository administrators must
select **Settings → Pages → Source → GitHub Actions** when creating a new repository.
The Pages workflow deploys `docs/` on each push to `main` and supports manual reruns.

## What to change / 改哪里

| Goal / 目的 | Edit / 修改 | Then run / 然后运行 |
| --- | --- | --- |
| Add a benchmark / 新增基准 | `data/research/catalog.tsv` (`id\|name\|path\|url\|tasks[\|direction]`) | `scripts/build_catalog.py` |
| Add scores / 新增成绩 | Save the source in `data/research/source-urls.json`, run `scripts/collect_sources.py`, add a parser to `scripts/import_public_scores.py` | `scripts/import_public_scores.py`, `scripts/build_models.py` |
| Map a benchmark to jobs or disciplines / 映射到职业或学科 | `data/mappings/benchmark_onet_dwa.tsv`, `benchmark_gbt13745.tsv` (`direct` or `partial` + reason) | — |
| Change scoring factors / 改计分系数 | `data/research/progress.yaml` | — |
| Translations / 译文 | `data/i18n/*.tsv`, UI text in `src/agi_atlas/i18n.py` (both `zh` and `en`) | `scripts/build_denominators.py` for denominator names |

Generated files (`data/benchmarks/benchmarks.yaml`, `data/scores/frontier_scores.yaml`, `data/models/models.yaml`, `data/denominators/*.tsv`, `reports/`, `docs/index.html`) must not be edited by hand.
生成文件请勿手改。

## Rules / 规则

- Never type a score, human baseline, version or date from memory. Every score needs a saved source snapshot, its SHA-256 and a locator (table / row).
  不凭印象填写成绩、人类基线、版本或日期；每条成绩都要有来源快照、哈希和定位。
- Only compare scores with the same version, protocol, subset, metric and unit.
  只在相同版本、协议、子集、指标、单位下比较。
- Unknown dates stay `null`. Release date ≠ evaluation date ≠ collection date.
  未知日期留空；发布日、评测日、采集日分别记录。
- Map a benchmark only to activities or disciplines it actually tests. Knowledge-only multiple choice is at most `partial`.
  只把基准映射到它真正测量的活动或学科；纯知识选择题最多算 `partial`。

## Before you push / 提交前

```bash
uv sync --extra dev
uv run agi-atlas validate
uv run agi-atlas report
uv run agi-atlas site
uv run pytest
uv run ruff check . && uv run ruff format --check .
```

Commit the regenerated `reports/` and `docs/index.html` together with your change. CI rebuilds everything and fails if they differ.
请把重新生成的 `reports/` 与 `docs/index.html` 一并提交；CI 会重建并比对。

On Windows, set `PYTHONUTF8=1`. / Windows 下请设置 `PYTHONUTF8=1`。
