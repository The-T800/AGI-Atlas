"""Protect scheduled refreshes from stale cutoffs and broken upstream snapshots."""

import importlib
import json
from pathlib import Path

import pytest
from conftest import REPO


def test_deepseek_readme_preamble_does_not_change_imported_scores(tmp_path, monkeypatch):
    monkeypatch.syspath_prepend(str(REPO / "scripts"))
    importer = importlib.import_module("import_public_scores")
    monkeypatch.setattr(importer, "SCORES", [])
    importer.import_deepseek()
    expected = list(importer.SCORES)
    for name in ("deepseek-r1", "deepseek-v3"):
        text = (importer.SOURCES / f"{name}.txt").read_text("utf-8")
        (tmp_path / f"{name}.txt").write_text("New upstream notice\n\n" + text, encoding="utf-8")
    monkeypatch.setattr(importer, "SOURCES", tmp_path)
    monkeypatch.setattr(importer, "SCORES", [])
    importer.import_deepseek()
    assert importer.SCORES == expected
    assert expected


def test_swe_bench_uses_retrieval_date_not_a_fixed_cutoff(tmp_path, monkeypatch):
    monkeypatch.syspath_prepend(str(REPO / "scripts"))
    importer = importlib.import_module("import_public_scores")
    monkeypatch.setattr(importer, "SOURCES", tmp_path)
    monkeypatch.setattr(importer, "SCORES", [])
    manifest = {k: dict(v) for k, v in importer.MANIFEST.items()}
    manifest["swe-board"]["observed_at"] = "2026-10-08"
    monkeypatch.setattr(importer, "MANIFEST", manifest)
    for i in (1, 2, 3):
        (tmp_path / f"arc-v{i}.txt").write_text('{"evaluations": []}', encoding="utf-8")
    rows = [
        dict(name="Current agent", date="2026-10-07", checked=True, warning=None),
        dict(name="Future agent", date="2026-10-09", checked=True, warning=None),
        dict(name="Unchecked agent", date="2026-10-07", checked=False, warning=None),
        dict(name="Warned agent", date="2026-10-07", checked=True, warning="Invalid run"),
    ]
    for r in rows:
        r.update(resolved=80, folder=r["name"])
    payload = json.dumps([dict(name="Verified", results=rows)])
    (tmp_path / "swe-board.txt").write_text(
        f'<script type="application/json" id="leaderboard-data">{payload}</script>',
        encoding="utf-8",
    )
    (tmp_path / "abstention-scores.txt").write_text("model_name_formatted,f1_score\n")
    importer.import_official()
    assert [s["model"] for s in importer.SCORES] == ["Current agent"]
    assert importer.SCORES[0]["published_at"] == "2026-10-07"
    assert importer.SCORES[0]["evaluation_date"] is None


def test_failed_refresh_does_not_replace_project_files(tmp_path, monkeypatch):
    monkeypatch.syspath_prepend(str(REPO / "scripts"))
    updater = importlib.import_module("update_benchmarks")
    monkeypatch.setattr(updater, "ROOT", tmp_path)
    monkeypatch.setattr("sys.argv", ["update_benchmarks.py"])
    (tmp_path / "data").mkdir()
    (tmp_path / "scripts").mkdir()
    for name in ("data/snapshot.txt", "README.md", "README.zh-CN.md"):
        (tmp_path / name).write_text("Retained evidence", encoding="utf-8")

    def failed_build(stage: Path, *, offline: bool) -> None:
        (stage / "data/snapshot.txt").write_text("Broken upstream", encoding="utf-8")
        raise ValueError("Upstream schema changed")

    monkeypatch.setattr(updater, "rebuild", failed_build)
    with pytest.raises(ValueError, match="Upstream schema changed"):
        updater.main()
    assert (tmp_path / "data/snapshot.txt").read_text() == "Retained evidence"
    assert (tmp_path / "README.md").read_text() == "Retained evidence"
    assert not (tmp_path / "docs").exists()
