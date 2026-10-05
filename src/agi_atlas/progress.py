"""O*NET work proxy scores and a separate OpenAlex task-evidence map."""

import csv
from collections import defaultdict
from pathlib import Path
from typing import Literal

from pydantic import HttpUrl

from agi_atlas.loader import read_model, read_yaml
from agi_atlas.models import Record, Text
from agi_atlas.subjects import build_subjects
from agi_atlas.validator import DataValidationError

Fit = Literal["direct", "partial"]


class Bilingual(Record):
    zh: Text
    en: Text


class Denominator(Record):
    name: Bilingual
    source_url: HttpUrl
    limitation: Bilingual


class ProgressPlan(Record):
    reviewed_on: Text
    coverage_factor: dict[Fit, float]
    denominators: dict[Literal["onet", "openalex"], Denominator]


def read_tsv(path: Path) -> list[dict]:
    with path.open(encoding="utf-8", newline="") as f:
        lines = [line for line in f if not line.startswith("#")]
    return list(csv.DictReader(lines, delimiter="\t"))


def _mapping(path: Path, key: str, valid_targets: set, benchmarks: set) -> list[dict]:
    rows = read_tsv(path)
    seen = set()
    for r in rows:
        pair = (r["benchmark_id"], r[key])
        if r["benchmark_id"] not in benchmarks:
            raise DataValidationError(f"{path.name} 引用了不存在的基准：{r['benchmark_id']}")
        if r[key] not in valid_targets:
            raise DataValidationError(f"{path.name} 引用了不存在的分母节点：{r[key]}")
        if r["fit"] not in ("direct", "partial"):
            raise DataValidationError(f"{path.name} 的 fit 只能是 direct 或 partial：{pair}")
        if pair in seen:
            raise DataValidationError(f"{path.name} 重复映射：{pair}")
        seen.add(pair)
    return rows


def benchmark_values(saturation: dict) -> dict[str, float]:
    """每个基准取代表比较组相对上限的比例（0–1）；无法换算的基准不给分。"""
    return {bid: min(1.0, s["ratio"]) for bid, s in saturation.items() if s["ratio"] is not None}


def _leaf_points(links: list[dict], values: dict, factors: dict) -> tuple[float, dict | None]:
    best, best_link = 0.0, None
    for link in links:
        if link["benchmark_id"] not in values:
            continue
        value = factors[link["fit"]] * link["breadth"] * values[link["benchmark_id"]]
        if value > best:
            best, best_link = value, link
    return best, best_link


def _share(items: list[dict], total: float) -> float:
    return round(sum(x["weight"] for x in items) / total * 100, 2)


def _summary(leaves: list[dict]) -> dict:
    total = sum(x["weight"] for x in leaves) or 1.0
    mapped = [x for x in leaves if x["links"]]
    # 精确覆盖：直接挂在该叶子上的映射（不含从上级学科摊下来的粗覆盖）。
    precise = [x for x in leaves if any(link["breadth"] == 1.0 for link in x["links"])]
    scored = [x for x in leaves if x["points"] > 0]
    earned = sum(x["weight"] * x["points"] for x in leaves)
    scored_weight = sum(x["weight"] for x in scored)
    return {
        "leaves": len(leaves),
        "mapped": len(mapped),
        "precise": len(precise),
        "scored": len(scored),
        "mapped_share": _share(mapped, total),
        "precise_share": _share(precise, total),
        "scored_share": _share(scored, total),
        "progress": round(earned / total * 100, 2),
        "depth": round(earned / scored_weight * 100, 1) if scored_weight else None,
    }


def _top(leaves: list[dict], n: int = 15) -> list[dict]:
    ranked = sorted(leaves, key=lambda x: (-x["points"], -x["weight"], x["id"]))[:n]
    return [
        {
            "id": x["id"],
            "name": x["name"],
            "points": round(x["points"] * 100, 1),
            "benchmark_id": x["best"]["benchmark_id"],
            "fit": x["best"]["fit"],
        }
        for x in ranked
        if x["points"] > 0
    ]


def _cells(leaves: list[dict], order: list[str]) -> list[list]:
    """马赛克图数据：每个分母叶子一格，按分组顺序、组内按得分排列。

    每格 [得分 0–100，-1 有基准无成绩，-2 无基准；分组下标；英文名；中文名]。
    """
    index = {g: i for i, g in enumerate(order)}
    ranked = sorted(
        leaves, key=lambda x: (index[x["group"]], -x["points"], not x["links"], x["id"])
    )
    return [
        [
            round(x["points"] * 100) if x["points"] > 0 else (-1 if x["links"] else -2),
            index[x["group"]],
            x["name"]["en"],
            x["name"]["zh"],
        ]
        for x in ranked
    ]


def _onet(root: Path, plan: ProgressPlan, values: dict, benchmarks: set) -> dict:
    dwas = read_tsv(root / "denominators/onet-dwa.tsv")
    occupations = read_tsv(root / "denominators/onet-occupations.tsv")
    labels = read_yaml(root / "denominators/labels.yaml")
    rows = _mapping(
        root / "mappings/benchmark_onet_dwa.tsv", "dwa_id", {d["dwa_id"] for d in dwas}, benchmarks
    )
    links = defaultdict(list)
    for r in rows:
        links[r["dwa_id"]].append({**r, "breadth": 1.0})
    leaves = []
    for d in dwas:
        points, best = _leaf_points(links[d["dwa_id"]], values, plan.coverage_factor)
        leaves.append(
            {
                "id": d["dwa_id"],
                "name": {"en": d["dwa"], "zh": d["dwa_zh"]},
                "group": d["gwa_id"],
                "weight": float(d["work_share"]),
                "links": links[d["dwa_id"]],
                "points": points,
                "best": best,
            }
        )
    gwa_en = {d["gwa_id"]: d["gwa"] for d in dwas}
    groups = [
        {
            "id": gid,
            "name": {"zh": zh, "en": gwa_en[gid]},
            **_summary([x for x in leaves if x["group"] == gid]),
        }
        for gid, zh in labels["gwa"].items()
    ]
    by_id = {x["id"]: x for x in leaves}
    majors = defaultdict(list)
    for occ in occupations:
        weights = {
            pair.split(":")[0]: float(pair.split(":")[1]) for pair in occ["dwa_weights"].split(";")
        }
        points = sum(w * by_id[d]["points"] for d, w in weights.items())
        covered = sum(w for d, w in weights.items() if by_id[d]["links"])
        majors[occ["soc"][:2]].append((occ, points, covered))
    occupation_groups = [
        {
            "id": code,
            "name": labels["soc_major"][code],
            "occupations": len(items),
            "progress": round(sum(p for _, p, _ in items) / len(items) * 100, 2),
            "mapped_share": round(sum(c for _, _, c in items) / len(items) * 100, 2),
        }
        for code, items in sorted(majors.items())
    ]
    ranked = sorted(
        (item for items in majors.values() for item in items), key=lambda t: (-t[1], t[0]["soc"])
    )
    return {
        **plan.denominators["onet"].model_dump(mode="json"),
        "occupations": len(occupations),
        "tasks": sum(int(o["tasks"]) for o in occupations),
        "summary": _summary(leaves),
        "groups": sorted(groups, key=lambda g: (-g["progress"], g["id"])),
        "occupation_groups": sorted(occupation_groups, key=lambda g: (-g["progress"], g["id"])),
        "top_occupations": [
            {
                "soc": o["soc"],
                "name": {"en": o["title"], "zh": o["title_zh"]},
                "progress": round(p * 100, 1),
            }
            for o, p, _ in ranked[:10]
        ],
        "top_leaves": _top(leaves),
        "cell_groups": [{"zh": zh, "en": gwa_en[gid]} for gid, zh in labels["gwa"].items()],
        "cells": _cells(leaves, list(labels["gwa"])),
    }


def build_progress(data_dir: Path | str, saturation: dict, benchmarks: set) -> dict:
    root = Path(data_dir)
    plan = read_model(root / "research/progress.yaml", ProgressPlan)
    values = benchmark_values(saturation)
    return {
        "reviewed_on": plan.reviewed_on,
        "coverage_factor": plan.coverage_factor,
        "scored_benchmarks": len(values),
        "onet": _onet(root, plan, values, benchmarks),
        "openalex": build_subjects(root, benchmarks),
    }
