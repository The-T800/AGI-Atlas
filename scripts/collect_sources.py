"""下载公开一手材料，保留原文和哈希；不下载完整评测数据集。"""

import argparse
import hashlib
import json
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1] / "data/research/sources"
SOURCES = json.loads((ROOT.parent / "source-urls.json").read_text(encoding="utf-8"))
OBSERVED_AT = datetime.now(timezone(timedelta(hours=8))).date().isoformat()


def snapshot_name(key, url):
    """来源只提供 zip 时按二进制原样保存为 .zip，其余沿用 .txt；哈希均针对原始字节。"""
    return f"{key}.zip" if url.split("?")[0].lower().endswith(".zip") else f"{key}.txt"


def download(item):
    key, url = item
    try:
        request = Request(url, headers={"User-Agent": "AGI-Atlas-research/0.2"})
        with urlopen(request, timeout=45) as response:
            content = response.read()
        name = snapshot_name(key, url)
        (ROOT / name).write_bytes(content)
        record = {
            "id": key,
            "url": url,
            "observed_at": OBSERVED_AT,
            "sha256": hashlib.sha256(content).hexdigest(),
            "bytes": len(content),
        }
        if name != f"{key}.txt":
            record["file"] = name
        return record
    except Exception as exc:
        return {"id": key, "url": url, "error": str(exc)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="首次采集或显式刷新一手材料快照")
    parser.add_argument("--refresh", action="store_true", help="重新下载已有快照；默认保留固定证据")
    args = parser.parse_args()
    ROOT.mkdir(parents=True, exist_ok=True)
    manifest_path = ROOT / "manifest.json"
    existing = (
        json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.exists() else []
    )
    records = {r["id"]: r for r in existing}
    pending = []
    for key, url in SOURCES.items():
        path = ROOT / snapshot_name(key, url)
        record = records.get(key, {})
        valid = path.exists() and hashlib.sha256(path.read_bytes()).hexdigest() == record.get(
            "sha256"
        )
        if args.refresh or not valid:
            pending.append((key, url))
    with ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(download, pending))
    failures = []
    for record in results:
        if "error" in record:
            failures.append(record)
        else:
            records[record["id"]] = record
    manifest_path.write_text(
        json.dumps(list(records.values()), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "retained": len(records),
                "downloaded": len(results) - len(failures),
                "failures": failures,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    if failures:
        raise SystemExit(1)
