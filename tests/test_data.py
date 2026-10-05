"""数据契约、校验与成绩分组：重复、悬空引用和不可比口径都必须被拦住。"""

from datetime import date

import pytest
from conftest import REPO, score

from agi_atlas.loader import load_data
from agi_atlas.results import result_groups, saturation
from agi_atlas.validator import DataValidationError, validate_data


def test_repository_data_is_valid_and_traceable():
    data = load_data(REPO / "data")
    assert len(data.benchmarks) >= 180
    assert len(data.scores) > 3000
    assert all(s.source_sha256 and s.source_locator for s in data.scores)


@pytest.mark.parametrize("kind", ["benchmarks", "scores"])
def test_duplicates_are_rejected(atlas, kind):
    records = getattr(atlas, kind)
    records.append(records[0])
    with pytest.raises(DataValidationError, match="重复"):
        validate_data(atlas)


def test_unknown_benchmark_is_rejected(atlas):
    atlas.scores[0].benchmark_id = "missing"
    with pytest.raises(DataValidationError, match="不存在"):
        validate_data(atlas)


def test_dates_cannot_follow_observation(atlas):
    atlas.scores[0].published_at = date(2026, 3, 1)
    with pytest.raises(DataValidationError, match="晚于采集日期"):
        validate_data(atlas)


def test_duplicate_yaml_keys_are_rejected(repo_data):
    path = repo_data / "benchmarks/benchmarks.yaml"
    path.write_text("- id: a\n  id: b\n", encoding="utf-8")
    with pytest.raises(DataValidationError, match="重复键"):
        load_data(repo_data)


@pytest.mark.parametrize(
    ("field", "value"),
    [("protocol", "允许工具"), ("subset", "几何"), ("benchmark_version", "v2"), ("unit", "分")],
)
def test_incompatible_settings_are_not_merged(atlas, field, value):
    atlas.scores.append(score(**{field: value, "model": "模型 B", "score": 99.0}))
    assert len(result_groups(atlas)) == 2


def test_lower_is_better_ranks_lowest_first(atlas):
    atlas.benchmarks[0].metric_direction = "lower_is_better"
    atlas.scores.append(score(model="低错误率模型", score=1.2))
    assert result_groups(atlas)[0]["winner"]["model"] == "低错误率模型"


@pytest.mark.parametrize(
    ("value", "human", "unit", "stage"),
    [
        (95, None, "%", "near"),
        (60, None, "%", "progress"),
        (30, None, "%", "gap"),
        (80, 75, "%", "reached"),
        (1500, None, "Elo", "unknown"),
    ],
)
def test_stage_rules(atlas, value, human, unit, stage):
    atlas.scores = [score(score=float(value), human_score=human, unit=unit)]
    status = saturation(atlas, result_groups(atlas))["benchmarks"]["test"]
    assert status["status"] == stage


def test_benchmark_without_scores_has_no_stage(atlas):
    atlas.scores = []
    assert saturation(atlas, [])["benchmarks"]["test"]["status"] == "none"
