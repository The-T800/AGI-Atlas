"""OpenAlex subject navigation and independently annotated benchmark capabilities."""

import csv
import json
from collections import defaultdict
from datetime import date
from pathlib import Path

from agi_atlas.validator import DataValidationError


def score_freshness(record: dict, as_of: date) -> str:
    """Retrieval is not evidence that an evaluation happened recently."""
    recorded = record.get("evaluation_date") or record.get("published_at")
    if not recorded:
        return "undated"
    age = (as_of - date.fromisoformat(str(recorded))).days
    if age < 0:
        return "future"
    return "recent" if age <= 365 else "historical"


def build_subjects(root: Path, benchmarks: set[str]) -> dict:
    taxonomy = json.loads((root / "denominators/openalex.json").read_text(encoding="utf-8"))
    capabilities = json.loads((root / "taxonomy/capabilities.json").read_text(encoding="utf-8"))
    translations = json.loads((root / "i18n/openalex.json").read_text(encoding="utf-8"))
    cap_ids = {c["id"] for c in capabilities}
    nodes = {}
    for level in ("domain", "field", "subfield", "topic"):
        for item in taxonomy[level + "s"]:
            name = item["name"]
            node = {
                **item,
                "level": level,
                "name": {"en": name, "zh": translations.get(level + ":" + item["id"], name)},
                "mapping_ids": [],
                "benchmark_ids": [],
                "points": None,
            }
            nodes[level + ":" + item["id"]] = node
    with (root / "mappings/benchmark_openalex.tsv").open(encoding="utf-8") as stream:
        mappings = list(csv.DictReader(stream, delimiter="\t"))
    seen = set()
    matrix = defaultdict(set)
    for index, link in enumerate(mappings):
        key = (link["benchmark_id"], link["target_level"], link["target_id"], link["capability_id"])
        if key in seen:
            raise DataValidationError("Duplicate subject/capability mapping")
        seen.add(key)
        if link["benchmark_id"] not in benchmarks or link["capability_id"] not in cap_ids:
            raise DataValidationError("Unknown benchmark or capability in subject mapping")
        if link["fit"] != "partial" or link["score_scope"] != "benchmark_only":
            raise DataValidationError("Subject links must preserve benchmark-only score scope")
        if not link["reason"] or not link["evidence_url"].startswith("https://"):
            raise DataValidationError("Subject mappings require task evidence")
        if link["target_level"] == "unassigned":
            if link["target_id"]:
                raise DataValidationError("Unassigned subject must have an empty target ID")
            continue
        node = nodes.get(link["target_level"] + ":" + link["target_id"])
        if node is None:
            raise DataValidationError("Unknown OpenAlex mapping target")
        node["mapping_ids"].append(index)
        ancestors = [node]
        for level in ("domain", "field", "subfield"):
            if level in node:
                ancestors.append(nodes[level + ":" + node[level]])
        for ancestor in ancestors:
            ancestor["benchmark_ids"].append(link["benchmark_id"])
        field = node["id"] if node["level"] == "field" else node.get("field")
        if field:
            matrix[field, link["capability_id"]].add(link["benchmark_id"])
    for node in nodes.values():
        node["benchmark_ids"] = sorted(set(node["benchmark_ids"]))
    topics = [n for n in nodes.values() if n["level"] == "topic"]
    fields = [n for n in nodes.values() if n["level"] == "field"]
    mapped = sum(bool(t["mapping_ids"]) for t in topics)
    dates = [t["updated_at"] for t in topics if t["updated_at"]]
    order = {f["id"]: i for i, f in enumerate(fields)}
    return {
        "name": {"en": "Subjects: OpenAlex research topics", "zh": "学科：OpenAlex 科研主题"},
        "source_url": taxonomy["source_url"],
        "retrieved_at": taxonomy["retrieved_at"],
        "release_date": taxonomy["release_date"],
        "acquisition": taxonomy["acquisition"],
        "updated_range": [min(dates), max(dates)] if dates else None,
        "counts": taxonomy["counts"],
        "capabilities": capabilities,
        "nodes": [n for n in nodes.values() if n["level"] != "topic"],
        "subjects": topics,
        "groups": fields,
        "mappings": mappings,
        "matrix": [
            {"field": f, "capability": c, "benchmark_ids": sorted(ids)}
            for (f, c), ids in sorted(matrix.items())
        ],
        "summary": {
            "leaves": len(topics),
            "mapped": mapped,
            "precise": mapped,
            "scored": 0,
            "progress": None,
            "depth": None,
            "mapped_share": round(mapped / len(topics) * 100, 2),
            "precise_share": round(mapped / len(topics) * 100, 2),
            "scored_share": 0,
            "linked_benchmarks": len(
                {m["benchmark_id"] for m in mappings if m["target_level"] != "unassigned"}
            ),
        },
        "cell_groups": [f["name"] for f in fields],
        "cells": [
            [-1 if t["mapping_ids"] else -2, order[t["field"]], t["name"]["en"], t["name"]["zh"]]
            for t in topics
        ],
        "top_leaves": [],
        "limitation": {
            "en": "Research topics are not an exhaustive capability inventory. Mappings describe "
            "task relevance, not subject mastery. Broad mappings never populate child topics. "
            "Unmeasured topics are unknown; benchmark totals are not subject scores.",
            "zh": "科研主题不等于完整能力清单。映射表示任务相关性，不代表学科掌握度；"
            "上级映射不下放到子主题。未测为未知，基准总分不作为学科分数。",
        },
    }
