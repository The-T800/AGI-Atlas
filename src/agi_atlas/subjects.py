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


def build_subjects(root: Path, benchmarks: set[str], groups: list[dict] | None = None) -> dict:
    taxonomy = json.loads((root / "denominators/openalex.json").read_text(encoding="utf-8"))
    capabilities = json.loads((root / "taxonomy/capabilities.json").read_text(encoding="utf-8"))
    translations = json.loads((root / "i18n/openalex.json").read_text(encoding="utf-8"))
    cap_ids = {c["id"] for c in capabilities}
    as_of = date.fromisoformat(taxonomy["retrieved_at"][:10])
    scored_ids, recent_ids = set(), set()
    for group in groups or []:
        if group["benchmark_id"] not in benchmarks:
            raise DataValidationError("Unknown benchmark in subject score evidence")
        records = [r for r in group["records"] if r.get("verified", True)]
        if records:
            scored_ids.add(group["benchmark_id"])
        if any(score_freshness(r, as_of) == "recent" for r in records):
            recent_ids.add(group["benchmark_id"])
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
            key = level + ":" + item["id"]
            if key in nodes:
                raise DataValidationError("Duplicate OpenAlex node")
            nodes[key] = node
    for node in nodes.values():
        for level in ("domain", "field", "subfield"):
            if level not in node:
                continue
            parent = nodes.get(level + ":" + node[level])
            if parent is None or any(
                node.get(k) != parent[k] for k in ("domain", "field") if k in parent
            ):
                raise DataValidationError("Invalid OpenAlex lineage")
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
        ids = set(node["benchmark_ids"])
        context_ids = {
            mappings[i]["benchmark_id"]
            for level in ("domain", "field", "subfield")
            if level in node
            for i in nodes[level + ":" + node[level]]["mapping_ids"]
        } - ids
        node["evidence"] = {
            "scored": len(ids & scored_ids),
            "recent": len(ids & recent_ids),
            "context": len(context_ids),
        }
    topics = [n for n in nodes.values() if n["level"] == "topic"]
    fields = [n for n in nodes.values() if n["level"] == "field"]
    mapped = sum(bool(t["mapping_ids"]) for t in topics)
    dates = [t["updated_at"] for t in topics if t["updated_at"]]
    order = {f["id"]: i for i, f in enumerate(fields)}
    coverage = {}
    for level in ("domain", "field", "subfield", "topic"):
        items = [n for n in nodes.values() if n["level"] == level]
        coverage[level] = {
            "total": len(items),
            "direct": sum(bool(n["mapping_ids"]) for n in items),
            "linked": sum(bool(n["benchmark_ids"]) for n in items),
            "scored": sum(bool(n["evidence"]["scored"]) for n in items),
            "recent": sum(bool(n["evidence"]["recent"]) for n in items),
            "context_only": sum(
                not n["benchmark_ids"] and bool(n["evidence"]["context"]) for n in items
            ),
        }
    linked_ids = {m["benchmark_id"] for m in mappings if m["target_level"] != "unassigned"}
    scored = coverage["topic"]["scored"]
    context_only = coverage["topic"]["context_only"]
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
        "coverage": coverage,
        "summary": {
            "leaves": len(topics),
            "mapped": mapped,
            "precise": mapped,
            "scored": scored,
            "recent": coverage["topic"]["recent"],
            "context_only": context_only,
            "unmapped": len(topics) - mapped - context_only,
            "progress": None,
            "depth": None,
            "mapped_share": round(mapped / len(topics) * 100, 2),
            "precise_share": round(mapped / len(topics) * 100, 2),
            "scored_share": round(scored / len(topics) * 100, 2),
            "linked_benchmarks": len(linked_ids),
            "scored_benchmarks": len(linked_ids & scored_ids),
            "recent_benchmarks": len(linked_ids & recent_ids),
            "unassigned_benchmarks": len(benchmarks - linked_ids),
        },
        "cell_groups": [f["name"] for f in fields],
        "cells": [
            [
                -3
                if t["evidence"]["scored"]
                else -1
                if t["mapping_ids"]
                else -4
                if t["evidence"]["context"]
                else -2,
                order[t["field"]],
                t["name"]["en"],
                t["name"]["zh"],
            ]
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
