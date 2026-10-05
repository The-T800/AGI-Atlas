"""从 data/research/catalog.tsv 生成基准目录 data/benchmarks/benchmarks.yaml。"""

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "data/research/catalog.tsv"
OUTPUT = ROOT / "data/benchmarks/benchmarks.yaml"
HEADER = "# 由 scripts/build_catalog.py 从 data/research/catalog.tsv 生成，请勿手改。\n"


def build() -> list[dict]:
    benchmarks = []
    for row in CATALOG.read_text(encoding="utf-8").splitlines():
        if not row or row.startswith("#"):
            continue
        key, name, path, url, tasks, *rest = row.split("|")
        benchmarks.append(
            {
                "id": key,
                "name": name,
                "path": path,
                "url": url,
                "tasks": tasks.split(";"),
                "metric_direction": rest[0] if rest else "higher_is_better",
            }
        )
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        HEADER + yaml.safe_dump(benchmarks, allow_unicode=True, sort_keys=False, width=120),
        encoding="utf-8",
    )
    print(f"基准 {len(benchmarks)}")
    return benchmarks


if __name__ == "__main__":
    build()
