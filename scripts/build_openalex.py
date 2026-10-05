"""Refresh OpenAlex's live taxonomy, or rebuild deterministically from pinned API pages."""

import argparse
import gzip
import hashlib
import json
import os
import time
import urllib.request
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "data"
SOURCE = ROOT / "research/sources/openalex"


def refresh() -> None:
    SOURCE.mkdir(parents=True, exist_ok=True)
    entries = []
    for kind in ("domains", "fields", "subfields", "topics"):
        page, count = 1, 0
        while True:
            url = f"https://api.openalex.org/{kind}?per-page=200&page={page}"
            for attempt in range(4):
                try:
                    key = os.environ.get("OPENALEX_API_KEY", "")
                    key_file = ROOT.parent / ".work/openalex-api-key.txt"
                    if not key and key_file.exists():
                        key = key_file.read_text().strip()
                    request = urllib.request.Request(url)
                    if key:
                        request.add_header("Authorization", "Bearer " + key)
                    with urllib.request.urlopen(request, timeout=60) as response:
                        raw = response.read()
                    break
                except OSError:
                    if attempt == 3:
                        raise
                    time.sleep(2**attempt)
            data = json.loads(raw)
            filename = f"{kind}-{page:03}.json"
            (SOURCE / filename).write_bytes(raw)
            entries.append(
                {
                    "file": filename,
                    "url": url,
                    "retrieved_at": datetime.now(UTC).isoformat(),
                    "sha256": hashlib.sha256(raw).hexdigest(),
                }
            )
            count += len(data["results"])
            if count >= data["meta"]["count"]:
                break
            if not data["results"]:
                raise ValueError("Incomplete OpenAlex pagination")
            page += 1
        print(f"{kind}: {count}", flush=True)
    (SOURCE / "manifest.json").write_text(json.dumps(entries, indent=2) + "\n", encoding="utf-8")


def refresh_snapshot() -> None:
    """Download the latest complete public release, not the frozen legacy bucket."""
    SOURCE.mkdir(parents=True, exist_ok=True)
    entries = []
    for kind in ("domains", "fields", "subfields", "topics"):
        url = f"https://openalex.s3.amazonaws.com/data/jsonl/{kind}/manifest.json"
        with urllib.request.urlopen(url, timeout=60) as response:
            raw_manifest = response.read()
        manifest = json.loads(raw_manifest)
        date = manifest["date"]
        (SOURCE / f"{kind}-release.json").write_bytes(raw_manifest)
        for i, part in enumerate(manifest["files"]):
            part_url = part["url"].replace("s3://openalex/", "https://openalex.s3.amazonaws.com/")
            with urllib.request.urlopen(part_url, timeout=90) as response:
                raw = response.read()
            filename = f"{kind}-snapshot-{i:03}.gz"
            (SOURCE / filename).write_bytes(raw)
            entries.append(
                {
                    "file": filename,
                    "url": part_url,
                    "kind": kind,
                    "format": "jsonl.gz",
                    "count": manifest["record_count"],
                    "release_date": date,
                    "manifest_url": url,
                    "manifest_sha256": hashlib.sha256(raw_manifest).hexdigest(),
                    "retrieved_at": datetime.now(UTC).isoformat(),
                    "sha256": hashlib.sha256(raw).hexdigest(),
                }
            )
        print(f"{kind}: release {date}, {manifest['record_count']} records", flush=True)
    (SOURCE / "manifest.json").write_text(json.dumps(entries, indent=2) + "\n", encoding="utf-8")


def build(root: Path = ROOT) -> dict:
    source = root / "research/sources/openalex"
    entries = json.loads((source / "manifest.json").read_text(encoding="utf-8"))
    releases = {entry.get("release_date") for entry in entries}
    if len(releases) != 1:
        raise ValueError("Mixed OpenAlex releases are not allowed")
    collections = {key: {} for key in ("domains", "fields", "subfields", "topics")}
    expected = {}
    for entry in entries:
        raw = (source / entry["file"]).read_bytes()
        if hashlib.sha256(raw).hexdigest() != entry["sha256"]:
            raise ValueError("OpenAlex source hash mismatch: " + entry["file"])
        kind = entry["file"].split("-")[0]
        if entry.get("format") == "jsonl.gz":
            source_manifest = (source / f"{kind}-release.json").read_bytes()
            if hashlib.sha256(source_manifest).hexdigest() != entry["manifest_sha256"]:
                raise ValueError("OpenAlex release manifest hash mismatch")
            records = [json.loads(line) for line in gzip.decompress(raw).splitlines() if line]
            count = entry["count"]
        else:
            data = json.loads(raw)
            records, count = data["results"], data["meta"]["count"]
        if kind in expected and expected[kind] != count:
            raise ValueError("OpenAlex count changed during pagination; refresh again")
        expected[kind] = count
        for item in records:
            key = item["id"].rsplit("/", 1)[-1]
            if key in collections[kind]:
                raise ValueError("Duplicate OpenAlex ID: " + item["id"])
            node = {
                "id": key,
                "name": item["display_name"],
                "description": item.get("description", ""),
                "updated_at": item.get("updated_date"),
                "created_at": item.get("created_date"),
                "url": f"https://openalex.org/{kind}/{key}",
            }
            for parent in ("domain", "field", "subfield"):
                if parent in item:
                    node[parent] = item[parent]["id"].rsplit("/", 1)[-1]
            if kind == "topics":
                node["keywords"] = item.get("keywords", [])
            collections[kind][key] = node
    for kind, nodes in collections.items():
        if len(nodes) != expected.get(kind):
            raise ValueError(f"Incomplete {kind} snapshot")
        for node in nodes.values():
            for parent in ("domain", "field", "subfield"):
                if parent in node and node[parent] not in collections[parent + "s"]:
                    raise ValueError("Broken taxonomy parent")
            if "subfield" in node:
                sub = collections["subfields"][node["subfield"]]
                if sub["field"] != node["field"]:
                    raise ValueError("Inconsistent topic lineage")
            if "field" in node:
                field = collections["fields"][node["field"]]
                if field["domain"] != node["domain"]:
                    raise ValueError("Inconsistent field lineage")
    result = {
        "source_url": "https://api.openalex.org/topics",
        "license": "CC0",
        "release_date": entries[0].get("release_date"),
        "acquisition": "public_snapshot" if entries[0].get("release_date") else "live_api",
        "retrieved_at": max(e["retrieved_at"] for e in entries),
        "counts": {k: len(v) for k, v in collections.items()},
        **{k: sorted(v.values(), key=lambda n: n["id"]) for k, v in collections.items()},
    }
    path = root / "denominators/openalex.json"
    path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result["counts"]))
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--refresh", action="store_true", help="Fetch all pages from the live API")
    parser.add_argument("--snapshot", action="store_true", help="Fetch the latest public release")
    args = parser.parse_args()
    if args.refresh:
        refresh()
    elif args.snapshot:
        refresh_snapshot()
    build()
