"""生成离线双语页面：一份 HTML 内嵌全部数据，中英文可切换，不依赖网络与前端框架。"""

import json
import math
from datetime import date
from importlib.resources import files
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field, HttpUrl, model_validator

from agi_atlas.i18n import LANGS, REPORT, UI, term_table, translate
from agi_atlas.loader import read_model
from agi_atlas.models import AtlasData, Number, Record, Text
from agi_atlas.progress import build_progress
from agi_atlas.results import atlas_results
from agi_atlas.validator import DataValidationError

METR_FILE = "research/metr-horizon-v1.1-2026-10-04.yaml"


class HorizonInterval(Record):
    estimate: Number = Field(gt=0)
    ci_low: Number = Field(gt=0)
    ci_high: Number = Field(gt=0)

    @model_validator(mode="after")
    def ordered(self) -> "HorizonInterval":
        if not self.ci_low <= self.estimate <= self.ci_high:
            raise ValueError("时长估计必须位于来源区间之内")
        return self


class HorizonMetrics(BaseModel):
    """保留源文件的其他指标，但只读取两个时长指标。"""

    p50_horizon_length: HorizonInterval
    p80_horizon_length: HorizonInterval


class HorizonModel(BaseModel):
    benchmark_name: Text
    release_date: date
    metrics: HorizonMetrics

    @model_validator(mode="after")
    def reliability_order(self) -> "HorizonModel":
        if self.metrics.p80_horizon_length.estimate > self.metrics.p50_horizon_length.estimate:
            raise ValueError("80% 成功率的时长不得大于 50% 成功率的时长")
        return self


class HorizonDataset(BaseModel):
    results: dict[str, HorizonModel]


class HorizonSnapshot(BaseModel):
    source_url: HttpUrl
    methodology_url: HttpUrl
    observed_on: date
    unit: Literal["minutes"]
    data: HorizonDataset


class EciModel(BaseModel):
    name: Text
    organization: str | None
    release_date: date
    eci: Number
    eci_ci_low: Number | None
    eci_ci_high: Number | None
    accessibility_group: str | None = None


class EciSnapshot(BaseModel):
    source_url: HttpUrl
    observed_on: date
    method_source: HttpUrl
    license: Text
    models: list[EciModel]


def horizon_trend(models: list[dict], metric: str) -> dict | None:
    """取逐次刷新纪录的前沿点，对 log2(时长) 与发布日期做最小二乘，得到翻倍时间。"""
    frontier, best = [], 0.0
    for m in models:
        value = m["metrics"][metric]["estimate"]
        if value > best:
            best = value
            frontier.append(m)
    if len(frontier) < 3:
        return None
    xs = [date.fromisoformat(m["release_date"]).toordinal() for m in frontier]
    ys = [math.log2(m["metrics"][metric]["estimate"]) for m in frontier]
    mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
    sxx = sum((x - mx) ** 2 for x in xs)
    slope = sum((x - mx) * (y - my) for x, y in zip(xs, ys, strict=True)) / sxx
    if slope <= 0:
        return None
    intercept = my - slope * mx
    residual = sum((y - (intercept + slope * x)) ** 2 for x, y in zip(xs, ys, strict=True))
    total = sum((y - my) ** 2 for y in ys)
    return {
        "frontier_ids": [m["id"] for m in frontier],
        "doubling_days": round(1 / slope, 1),
        "slope_per_day": slope,
        "intercept": intercept,
        "r2": round(1 - residual / total, 3) if total else None,
    }


def _horizons(root: Path) -> dict:
    snapshot = read_model(root / METR_FILE, HorizonSnapshot)
    models = []
    for key, model in snapshot.data.results.items():
        # 源文件包含部分 v1.0 的历史数据，不能与 v1.1 当成同一量尺展示。
        if model.benchmark_name != "METR-Horizon-v1.1":
            continue
        if model.release_date > snapshot.observed_on:
            raise DataValidationError(f"模型 {key} 的发布日期晚于快照采集日期")
        models.append({"id": key, **model.model_dump(mode="json", exclude={"benchmark_name"})})
    if not models:
        raise DataValidationError("快照中没有 METR-Horizon-v1.1 记录")
    models.sort(key=lambda m: (m["release_date"], m["id"]))
    return {
        "source_url": str(snapshot.source_url),
        "methodology_url": str(snapshot.methodology_url),
        "observed_on": snapshot.observed_on.isoformat(),
        "models": models,
        "trend": {
            "p50": horizon_trend(models, "p50_horizon_length"),
            "p80": horizon_trend(models, "p80_horizon_length"),
        },
    }


def _eci(root: Path) -> dict | None:
    path = root / "research/epoch-eci.yaml"
    if not path.exists():
        return None
    eci = read_model(path, EciSnapshot)
    return {
        "source_url": str(eci.source_url),
        "method_url": str(eci.method_source),
        "observed_on": eci.observed_on.isoformat(),
        "license": eci.license,
        "models": [
            m.model_dump(mode="json")
            for m in sorted(eci.models, key=lambda m: (m.release_date, m.name))
        ],
    }


def _compact_groups(groups: list[dict], table: dict, status: dict) -> tuple[list[dict], list[str]]:
    """页面载荷瘦身：成绩记录去掉与比较组重复的字段，来源改为索引，并附英文口径。"""
    sources: dict[str, int] = {}
    shared = {"benchmark_id", "benchmark_version", "protocol", "subset", "metric", "unit"}
    drop = {"verified", "notes", "source_sha256", "source_locator", "observed_at"}
    compact = []
    for g in groups:
        records = []
        for r in g["records"]:
            row = {k: v for k, v in r.items() if k not in shared | drop and v is not None}
            row["source_url"] = sources.setdefault(r["source_url"], len(sources))
            records.append(row)
        en = {
            k: translate(g[k], table) for k in ("version", "protocol", "subset", "metric", "unit")
        }
        rep = status[g["benchmark_id"]]["group"] or {}
        representative = all(rep.get(k) == g[k] for k in en)
        compact.append(
            {k: v for k, v in g.items() if k not in ("winner", "ratio")}
            | {"records": records, "en": en, "representative": representative}
        )
    return compact, list(sources)


def build_payload(data: AtlasData, data_dir: Path | str) -> dict:
    root = Path(data_dir)
    table = term_table(root)
    results = atlas_results(data)
    status = results["saturation"]["benchmarks"]
    groups, sources = _compact_groups(results["groups"], table, status)

    def path_en(path: str) -> str:
        return "/".join(table.get(part, part) for part in path.split("/"))

    benchmarks = [
        {
            **b.model_dump(mode="json"),
            "path_en": path_en(b.path),
            "tasks_en": [table.get(t, t) for t in b.tasks],
            "status": status[b.id]["status"],
        }
        for b in data.benchmarks
    ]
    domains = list(dict.fromkeys(b.domain for b in data.benchmarks))
    return {
        "snapshot": max(s.observed_at for s in data.scores).isoformat(),
        "i18n": {lang: {k: v[lang] for k, v in {**UI, **REPORT}.items()} for lang in LANGS},
        "summary": {
            "benchmarks": len(data.benchmarks),
            "scored_benchmarks": results["measured_benchmarks"],
            "scores": len(data.scores),
            "models": len(data.models),
        },
        "domains": [{"zh": d, "en": table.get(d, d)} for d in domains],
        "benchmarks": benchmarks,
        "grid": results["saturation"]["grid"],
        "groups": groups,
        "sources": sources,
        "models": {
            m.id: {
                "name": m.name,
                "provider": m.provider,
                "provider_en": table.get(m.provider, m.provider),
                **({"release_date": m.release_date.isoformat()} if m.release_date else {}),
            }
            for m in data.models
        },
        "progress": build_progress(root, status, {b.id for b in data.benchmarks}),
        "horizons": _horizons(root),
        "eci": _eci(root),
    }


def render_site(data: AtlasData, data_dir: Path | str = "data") -> str:
    payload = build_payload(data, data_dir)
    serialized = json.dumps(payload, ensure_ascii=False, allow_nan=False, separators=(",", ":"))
    # 防止来源文本中的 HTML 结束标签打断内嵌 JSON。
    serialized = serialized.replace("&", "\\u0026").replace("<", "\\u003c").replace(">", "\\u003e")
    template = files("agi_atlas").joinpath("templates/index.html").read_text(encoding="utf-8")
    return template.replace("__ATLAS_PAYLOAD__", serialized)


def write_site(
    data: AtlasData, data_dir: Path | str = "data", output: Path | str = "docs/index.html"
) -> Path:
    path = Path(output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_site(data, data_dir), encoding="utf-8")
    return path
