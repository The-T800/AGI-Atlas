"""确保公开成绩可以从原始快照复核，且导入没有悄悄遗漏来源表。"""

import hashlib
import importlib
import json

import yaml
from conftest import REPO

from agi_atlas.loader import load_data
from agi_atlas.models import BenchmarkScore


def test_scores_reference_intact_source_snapshots():
    root = REPO / "data/research/sources"
    manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
    sources = {}
    for entry in manifest:
        # 只提供 zip 的来源按二进制快照保存，文件名记录在 file 字段。
        content = (root / entry.get("file", f"{entry['id']}.txt")).read_bytes()
        assert hashlib.sha256(content).hexdigest() == entry["sha256"]
        sources[(entry["url"], entry["sha256"])] = entry
    for score in load_data(REPO / "data").scores:
        source = sources[(str(score.source_url), score.source_sha256)]
        assert score.observed_at.isoformat() == source["observed_at"]
        assert score.source_locator


def test_offline_import_reproduces_all_committed_scores(monkeypatch):
    monkeypatch.syspath_prepend(str(REPO / "scripts"))
    importer = importlib.import_module("import_public_scores")
    monkeypatch.setattr(importer, "SCORES", [])
    for name in (
        "import_qwen",
        "import_deepseek",
        "import_cl",
        "import_official",
        "import_mmsi",
        "import_audio_and_social",
        "import_robotics_safety_creation",
        "import_epoch",
    ):
        getattr(importer, name)()
    generated = {BenchmarkScore.model_validate(s).model_dump_json() for s in importer.SCORES}
    committed = {s.model_dump_json() for s in load_data(REPO / "data").scores}
    assert generated == committed
    assert {s["benchmark_id"] for s in importer.SCORES} >= {"libero", "wildguard", "gen-eval"}


def test_epoch_tables_reproducible_offline(monkeypatch):
    monkeypatch.syspath_prepend(str(REPO / "scripts"))
    importer = importlib.import_module("import_public_scores")
    for name, build in importer.EPOCH_TABLES.items():
        committed = yaml.safe_load((REPO / "data/research" / name).read_text(encoding="utf-8"))
        assert committed == build()
        assert committed["models"]
