"""Protect taxonomy provenance, mapping scope and date semantics."""

import importlib
import json
import shutil
from datetime import date

import pytest
from conftest import REPO

from agi_atlas.loader import load_data
from agi_atlas.subjects import build_subjects, score_freshness
from agi_atlas.validator import DataValidationError


def subjects(root=REPO / "data"):
    return build_subjects(root, {b.id for b in load_data(root).benchmarks})


def test_full_taxonomy_has_valid_unique_lineage():
    data = subjects()
    all_nodes = data["nodes"] + data["subjects"]
    keys = {(n["level"], n["id"]) for n in all_nodes}
    assert len(keys) == len(all_nodes) == 4 + 26 + 252 + 4516
    for topic in data["subjects"]:
        for level in ("domain", "field", "subfield"):
            assert (level, topic[level]) in keys
    assert len(data["cells"]) == 4516
    assert data["release_date"] == "2026-09-23"
    assert data["retrieved_at"][:10] >= data["release_date"]


def test_broad_exam_scores_do_not_propagate_into_topics():
    data = subjects()
    assert any(m["benchmark_id"] == "mmlu" for m in data["mappings"])
    assert all("mmlu" not in n["benchmark_ids"] for n in data["subjects"])
    assert all(n["points"] is None for n in data["subjects"])
    assert data["summary"]["progress"] is None
    software = next(n for n in data["subjects"] if n["id"] == "T10743")
    assert "swe-bench" in software["benchmark_ids"]
    assert data["summary"]["mapped"] == sum(bool(n["mapping_ids"]) for n in data["subjects"])


def test_matrix_deduplicates_multiple_task_links():
    data = subjects()
    for cell in data["matrix"]:
        assert len(cell["benchmark_ids"]) == len(set(cell["benchmark_ids"]))
    assert {m["benchmark_id"] for m in data["mappings"]} == {
        b.id for b in load_data(REPO / "data").benchmarks
    }


def test_invalid_subject_link_fails_closed(repo_data):
    path = repo_data / "mappings/benchmark_openalex.tsv"
    content = path.read_text(encoding="utf-8").replace("\tfield\t11\t", "\tfield\t99999\t", 1)
    path.write_text(content, encoding="utf-8")
    with pytest.raises(DataValidationError, match="Unknown OpenAlex"):
        subjects(repo_data)


def test_missing_evidence_leaves_topics_unknown(repo_data):
    path = repo_data / "mappings/benchmark_openalex.tsv"
    path.write_text(path.read_text(encoding="utf-8").splitlines()[0] + "\n", encoding="utf-8")
    data = subjects(repo_data)
    assert data["summary"]["leaves"] == 4516
    assert data["summary"]["mapped"] == 0
    assert data["summary"]["progress"] is None
    assert all(n["points"] is None for n in data["subjects"])


@pytest.mark.parametrize(
    ("record", "expected"),
    [
        ({"evaluation_date": "2026-10-05"}, "recent"),
        ({"evaluation_date": "2025-10-05"}, "recent"),
        ({"evaluation_date": "2024-01-01", "published_at": "2026-10-05"}, "historical"),
        ({"published_at": "2026-09-01"}, "recent"),
        ({"observed_at": "2026-10-05"}, "undated"),
        ({"evaluation_date": "2027-01-01"}, "future"),
    ],
)
def test_recent_retrieval_never_relabels_old_results(record, expected):
    assert score_freshness(record, date(2026, 10, 5)) == expected


def test_pinned_snapshot_rebuild_and_tamper_detection(repo_data, monkeypatch):
    monkeypatch.syspath_prepend(str(REPO / "scripts"))
    module = importlib.import_module("build_openalex")
    before = (repo_data / "denominators/openalex.json").read_bytes()
    shutil.copytree(
        REPO / "data/research/sources/openalex", repo_data / "research/sources/openalex"
    )
    module.build(repo_data)
    assert before == (repo_data / "denominators/openalex.json").read_bytes()
    source = repo_data / "research/sources/openalex"
    manifest = json.loads((source / "manifest.json").read_text())
    (source / manifest[0]["file"]).write_bytes(b"tampered")
    with pytest.raises(ValueError, match="hash mismatch"):
        module.build(repo_data)
