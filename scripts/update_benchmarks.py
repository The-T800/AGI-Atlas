"""Refresh retained benchmark evidence and rebuild outputs before replacing project data."""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from agi_atlas.loader import load_data
from agi_atlas.site import build_payload

ROOT = Path(__file__).resolve().parents[1]
START = "<!-- benchmark-refresh:start -->"
END = "<!-- benchmark-refresh:end -->"


def update_readmes(root: Path) -> None:
    """Keep bilingual freshness summaries reproducible from the same data as the site."""
    data = load_data(root / "data")
    payload = build_payload(data, root / "data")
    summary = payload["summary"]
    subjects = payload["progress"]["openalex"]["summary"]
    manifest = json.loads((root / "data/research/sources/manifest.json").read_text("utf-8"))
    days = sorted({r["observed_at"] for r in manifest})
    retrieved = days[0] if len(days) == 1 else f"{days[0]} – {days[-1]}"
    blocks = {
        "README.md": (
            f"Benchmark sources: **{len(manifest)}**; retrieval dates: **{retrieved}**. "
            f"Catalog: **{summary['benchmarks']} benchmarks**, "
            f"**{summary['scores']:,} score records**, **{summary['models']} models**; "
            f"**{summary['scored_benchmarks']} benchmarks** have verified score transcriptions.\n\n"
            f"Subject links: **{subjects['linked_benchmarks']} benchmarks**; "
            f"**{subjects['scored_benchmarks']}** have results and "
            f"**{subjects['recent_benchmarks']}** have dated results within the last year. "
            "The evidence window follows the latest score retrieval, independently of taxonomy "
            "retrieval. Evaluation, publication, model release and retrieval dates stay separate. "
            "Downloading an old result does not make its evaluation recent."
        ),
        "README.zh-CN.md": (
            f"Benchmark 来源：**{len(manifest)} 个**；抓取日期：**{retrieved}**。"
            f"目录共 **{summary['benchmarks']} 个基准**、**{summary['scores']:,} 条成绩**、"
            f"**{summary['models']} 个模型**；"
            f"**{summary['scored_benchmarks']} 个基准**有核验转录成绩。\n\n"
            f"学科挂靠：**{subjects['linked_benchmarks']} 个基准**；其中 "
            f"**{subjects['scored_benchmarks']} 个**有成绩，**{subjects['recent_benchmarks']} 个**"
            "有近一年日期明确的成绩。证据时间窗口按最新成绩抓取日期推进，与分类抓取日期独立。"
            "评测日期、发布日期、模型发布日期和抓取日期分别保留；重新下载不会把旧评测变成新评测。"
        ),
    }
    for name, block in blocks.items():
        path = root / name
        text = path.read_text("utf-8")
        pattern = re.escape(START) + r".*?" + re.escape(END)
        text, count = re.subn(
            pattern, lambda _, block=block: f"{START}\n{block}\n{END}", text, flags=re.S
        )
        if count != 1:
            raise ValueError(f"Expected one benchmark freshness block in {name}")
        path.write_text(text, encoding="utf-8")


def rebuild(stage: Path, *, offline: bool) -> None:
    env = dict(os.environ, PYTHONIOENCODING="utf-8")

    def run(*args: str) -> None:
        subprocess.run([sys.executable, *args], cwd=stage, env=env, check=True)

    if not offline:
        run("scripts/collect_sources.py", "--refresh")
    for script in ("build_catalog", "import_public_scores", "build_models", "build_openalex"):
        run(f"scripts/{script}.py")
    run("-m", "agi_atlas", "validate")
    run("-m", "agi_atlas", "report")
    run("-m", "agi_atlas", "site")
    update_readmes(stage)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--offline", action="store_true", help="Rebuild retained snapshots only")
    args = parser.parse_args()
    with tempfile.TemporaryDirectory(prefix="agi-atlas-refresh-") as directory:
        stage = Path(directory)
        shutil.copytree(ROOT / "data", stage / "data")
        shutil.copytree(
            ROOT / "scripts", stage / "scripts", ignore=shutil.ignore_patterns("__pycache__")
        )
        for name in ("README.md", "README.zh-CN.md"):
            shutil.copy2(ROOT / name, stage / name)
        rebuild(stage, offline=args.offline)
        # Fetch or parser failures leave the current project data and outputs intact.
        for name in ("data", "reports", "docs"):
            shutil.copytree(stage / name, ROOT / name, dirs_exist_ok=True)
        for name in ("README.md", "README.zh-CN.md"):
            shutil.copy2(stage / name, ROOT / name)
    print("Benchmark evidence, model registry, bilingual reports and site updated.")


if __name__ == "__main__":
    main()
