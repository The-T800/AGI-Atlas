"""从成绩记录生成模型注册表：合并同一模型的不同写法，发布日期只取有来源的精确匹配。"""

import hashlib
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
sys.path.insert(0, str(ROOT / "src"))

from agi_atlas.naming import model_key  # noqa: E402

HEADER = (
    "# 由 scripts/build_models.py 生成：name 为成绩中最常见的写法，aliases 为其他等价写法。\n"
    "# 发布日期只取 Epoch 模型元数据或 ECI 表中名称（或方括号内版本号）精确匹配的条目；\n"
    "# 匹配不上留空，不推测。\n"
)
VERSION = re.compile(r"\[([^\]]+)\]\s*$")


def load(path):
    return yaml.load(path.read_text(encoding="utf-8"), Loader=yaml.CSafeLoader)


def date_index():
    """返回（按模型名键索引，按版本号索引）两张表，值为（日期，来源 URL）。"""
    by_name, by_version = {}, {}
    for file in ("epoch-model-dates.yaml", "epoch-eci.yaml"):
        path = DATA / "research" / file
        if not path.exists():
            continue
        table = load(path)
        for m in table["models"]:
            if not m.get("release_date"):
                continue
            value = (m["release_date"], table["source_url"])
            by_name.setdefault(model_key(m["name"]), value)
            for version in m.get("model_versions") or []:
                by_version.setdefault(version, value)
    return by_name, by_version


def slug(key, used):
    base = re.sub(r"[^a-z0-9]+", "-", key).strip("-")[:60].strip("-") or "model"
    if base in used:
        base = f"{base}-{hashlib.sha256(key.encode()).hexdigest()[:6]}"
    used.add(base)
    return base


def build():
    scores = load(DATA / "scores/frontier_scores.yaml")
    spellings, providers = defaultdict(Counter), defaultdict(Counter)
    for s in scores:
        key = model_key(s["model"])
        spellings[key][s["model"]] += 1
        providers[key][s["model_provider"]] += 1
    by_name, by_version = date_index()
    used, entries = set(), []
    for key in sorted(spellings):
        names = sorted(spellings[key], key=lambda n: (-spellings[key][n], n))
        version = VERSION.search(names[0])
        found = by_version.get(version[1]) if version else by_name.get(key)
        entry = {
            "id": slug(key, used),
            "name": names[0],
            "provider": sorted(providers[key], key=lambda p: (-providers[key][p], p))[0],
        }
        if found:
            entry["release_date"], entry["release_source"] = found
        if names[1:]:
            entry["aliases"] = names[1:]
        entries.append(entry)
    path = DATA / "models/models.yaml"
    path.parent.mkdir(exist_ok=True)
    path.write_text(
        HEADER + yaml.safe_dump(entries, allow_unicode=True, sort_keys=False, width=120),
        encoding="utf-8",
    )
    dated = sum("release_date" in e for e in entries)
    print(
        f"模型 {len(entries)}；有发布日期 {dated}；合并写法 {sum('aliases' in e for e in entries)}"
    )


if __name__ == "__main__":
    build()
