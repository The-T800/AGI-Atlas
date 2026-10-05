"""AGI 差距：分母不能因缺测而缩小，未覆盖记 0，映射必须引用真实存在的节点。"""

import csv

import pytest
import yaml
from conftest import REPO

from agi_atlas.loader import load_data
from agi_atlas.site import build_payload
from agi_atlas.validator import DataValidationError


def _progress(data_dir=REPO / "data"):
    return build_payload(load_data(data_dir), data_dir)["progress"]


def test_denominators_are_complete_source_taxonomies():
    p = _progress()
    assert p["onet"]["summary"]["leaves"] == 2087
    assert p["onet"]["occupations"] == 923
    assert p["onet"]["tasks"] == 18838
    assert p["openalex"]["counts"] == {"domains": 4, "fields": 26, "subfields": 252, "topics": 4516}
    assert len(p["onet"]["groups"]) == 41
    assert len(p["onet"]["occupation_groups"]) == 22


def test_progress_never_exceeds_coverage():
    for key in ("onet",):
        s = _progress()[key]["summary"]
        assert 0 < s["progress"] <= s["scored_share"] <= s["mapped_share"] <= 100
        assert s["precise_share"] <= s["mapped_share"]
        assert s["scored"] <= s["mapped"] <= s["leaves"]


def test_removing_all_mappings_gives_zero_not_smaller_denominator(repo_data):
    for name in ("benchmark_onet_dwa.tsv",):
        path = repo_data / "mappings" / name
        lines = path.read_text(encoding="utf-8").splitlines()
        header = [line for line in lines if line.startswith(("#", "benchmark_id"))]
        path.write_text("\n".join(header) + "\n", encoding="utf-8")
    p = _progress(repo_data)
    for key in ("onet",):
        s = p[key]["summary"]
        assert s["progress"] == 0 and s["mapped"] == 0
        assert s["leaves"] == 2087
        assert s["depth"] is None


def test_partial_fit_is_discounted(repo_data):
    path = repo_data / "research/progress.yaml"
    base = _progress(repo_data)["onet"]["summary"]["progress"]
    plan = yaml.safe_load(path.read_text(encoding="utf-8"))
    plan["coverage_factor"]["partial"] = 1.0
    path.write_text(yaml.safe_dump(plan, allow_unicode=True), encoding="utf-8")
    assert _progress(repo_data)["onet"]["summary"]["progress"] > base


@pytest.mark.parametrize(
    ("name", "column", "value", "message"),
    [
        ("benchmark_onet_dwa.tsv", 1, "9.Z.9", "不存在的分母节点"),
        ("benchmark_onet_dwa.tsv", 0, "missing-bench", "不存在的基准"),
    ],
)
def test_invalid_mapping_is_rejected(repo_data, name, column, value, message):
    path = repo_data / "mappings" / name
    lines = path.read_text(encoding="utf-8").splitlines()
    i = next(
        i for i, line in enumerate(lines) if line and not line.startswith(("#", "benchmark_id"))
    )
    cells = lines[i].split("\t")
    cells[column] = value
    lines[i] = "\t".join(cells)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    with pytest.raises(DataValidationError, match=message):
        _progress(repo_data)


def test_occupation_weights_sum_to_one():
    with (REPO / "data/denominators/onet-dwa.tsv").open(encoding="utf-8") as f:
        total = sum(float(r["work_share"]) for r in csv.DictReader(f, delimiter="\t"))
    assert total == pytest.approx(1.0, abs=1e-3)
