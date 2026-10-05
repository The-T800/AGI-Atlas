"""测试夹具：仓库根目录、真实数据副本与最小虚构数据集。"""

import shutil
from datetime import date
from pathlib import Path

import pytest

from agi_atlas.models import AtlasData, Benchmark, BenchmarkScore

REPO = Path(__file__).resolve().parents[1]


@pytest.fixture
def repo_data(tmp_path: Path) -> Path:
    """真实数据的可修改副本，用于验证错误输入会被拒绝。"""
    target = tmp_path / "data"
    shutil.copytree(REPO / "data", target, ignore=shutil.ignore_patterns("sources"))
    return target


def score(**overrides) -> BenchmarkScore:
    """虚构成绩，仅用于测试。"""
    values = dict(
        benchmark_id="test",
        benchmark_version="v1",
        model="模型 A",
        model_provider="测试方",
        score=60.0,
        human_score=None,
        evaluation_date=date(2026, 1, 1),
        observed_at=date(2026, 2, 1),
        protocol="标准",
        metric="准确率",
        unit="%",
        source_locator="表 1",
        source_sha256="0" * 64,
        source_url="https://example.com/score",
        source_type="community",
        verified=True,
        notes=None,
    )
    return BenchmarkScore(**{**values, **overrides})


@pytest.fixture
def atlas() -> AtlasData:
    return AtlasData(
        benchmarks=[
            Benchmark(
                id="test", name="测试基准", path="测试/子类", url="https://example.com/benchmark"
            )
        ],
        scores=[score()],
    )
