"""原始成绩按同版本、协议、子集与量纲分组比较；每个基准取一个代表组判定阶段。"""

from collections import defaultdict

from agi_atlas.models import AtlasData, Benchmark, BenchmarkScore
from agi_atlas.naming import resolver

# 来源可信度排序：选代表比较组时优先官方榜单与独立复测，其次论文，最后厂商自报。
SOURCE_PRIORITY = {
    "official_benchmark": 0,
    "independent_evaluation": 1,
    "paper": 2,
    "model_provider": 3,
    "community": 4,
}

# 阶段阈值：达到上限的 90% 以上为接近上限，50%–90% 为进行中，低于 50% 为差距明显。
NEAR = 0.9
HALF = 0.5
STATUSES = ("reached", "near", "progress", "gap", "unknown", "none")


def comparison_key(score: BenchmarkScore) -> tuple:
    return (
        score.benchmark_id,
        score.benchmark_version,
        score.protocol,
        score.subset,
        score.metric,
        score.unit,
    )


def metric_direction(data: AtlasData, benchmark: Benchmark, metric: str | None) -> str:
    """指标级规则优先；未登记的指标沿用基准级方向。"""
    for rule in data.metric_rules:
        if rule.metric == metric:
            return rule.direction
    return benchmark.metric_direction


def group_status(group: dict) -> tuple[str, float | None]:
    """返回（阶段，相对上限的比例）。

    有同源人类值时与之比较，否则只对“越高越好的 %”以 100 为上限。
    """
    winner = group["winner"]
    higher = group["direction"] == "higher_is_better"
    human = winner["human_score"]
    if human is None:
        human = next(
            (
                r["human_score"]
                for r in group["records"]
                if r["human_score"] is not None and r["source_url"] == winner["source_url"]
            ),
            None,
        )
    score = winner["score"]
    if human is not None and human > 0:
        if (score >= human) if higher else (score <= human):
            return "reached", 1.0
        ratio = score / human if higher else (human / score if score > 0 else None)
    elif higher and group["unit"] == "%":
        ratio = score / 100
    else:
        return "unknown", None
    if ratio is None:
        return "unknown", None
    if ratio >= NEAR:
        return "near", ratio
    return ("progress" if ratio >= HALF else "gap"), ratio


def result_groups(data: AtlasData) -> list[dict]:
    benchmarks = {b.id: b for b in data.benchmarks}
    models = resolver(data)
    groups = defaultdict(list)
    for score in data.scores:
        if score.verified:
            groups[comparison_key(score)].append(score)
    result = []
    for key, records in sorted(groups.items(), key=lambda item: tuple(str(x) for x in item[0])):
        direction = metric_direction(data, benchmarks[key[0]], key[4])
        descending = direction == "higher_is_better"
        ordered = sorted(records, key=lambda s: (s.score, s.model), reverse=descending)
        group = {
            "benchmark_id": key[0],
            "version": key[1],
            "protocol": key[2],
            "subset": key[3],
            "metric": key[4],
            "unit": key[5],
            "count": len(records),
            "direction": direction,
            "source_type": min(
                (s.source_type for s in records), key=lambda kind: SOURCE_PRIORITY[kind]
            ),
            "winner": ordered[0].model_dump(mode="json"),
            "records": [
                {**s.model_dump(mode="json"), "model_id": models.model_id(s)} for s in ordered
            ],
        }
        group["status"], group["ratio"] = group_status(group)
        result.append(group)
    return result


def representative(groups: list[dict]) -> dict | None:
    """同一基准的代表比较组：总体子集优先，其次来源可信度，再次成绩条数。"""
    if not groups:
        return None
    return min(
        groups,
        key=lambda g: (g["subset"] != "overall", SOURCE_PRIORITY[g["source_type"]], -g["count"]),
    )


def saturation(data: AtlasData, groups: list[dict]) -> dict:
    """每个基准一个阶段，并按一级能力域计数。"""
    by_benchmark = defaultdict(list)
    for g in groups:
        by_benchmark[g["benchmark_id"]].append(g)
    benchmarks = {}
    grid: dict[str, dict[str, int]] = {}
    for b in data.benchmarks:
        rep = representative(by_benchmark[b.id])
        status = rep["status"] if rep else "none"
        benchmarks[b.id] = {
            "status": status,
            "ratio": rep["ratio"] if rep else None,
            "group": (
                {k: rep[k] for k in ("version", "protocol", "subset", "metric", "unit")}
                if rep
                else None
            ),
        }
        row = grid.setdefault(b.domain, dict.fromkeys(STATUSES, 0))
        row[status] += 1
    return {"benchmarks": benchmarks, "grid": grid}


def atlas_results(data: AtlasData) -> dict:
    groups = result_groups(data)
    return {
        "groups": groups,
        "saturation": saturation(data, groups),
        "measured_benchmarks": len({s.benchmark_id for s in data.scores if s.verified}),
        "source_counts": {
            kind: sum(s.source_type == kind for s in data.scores)
            for kind in sorted({s.source_type for s in data.scores})
        },
    }
