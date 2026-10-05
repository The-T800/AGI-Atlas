"""Build Nature's public subject directory from its pinned HTML snapshot."""

import csv
import hashlib
import json
import re
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


def parse_directory(html: str) -> list[dict]:
    groups = []
    pattern = (
        r'<div id="([^"]+)" class="container cleared container-type-link-grid"[^>]*>(.*?)</section>'
    )
    for key, body in re.findall(pattern, html, re.S):
        title = re.search(r"<h2[^>]*>(.*?)</h2>", body, re.S)
        subjects = [
            {"id": sid, "name": unescape(re.sub(r"<[^>]+>", "", name)).strip()}
            for sid, name in re.findall(r'<a href="/subjects/([^"/?]+)"[^>]*>(.*?)</a>', body, re.S)
        ]
        if title and subjects:
            groups.append({"id": key, "name": unescape(title[1]).strip(), "subjects": subjects})
    if not groups or any(not g["subjects"] for g in groups):
        raise ValueError("The source no longer matches Nature's public directory structure.")
    return groups


def write_tsv(name: str, columns: list[str], rows: list[list]) -> None:
    with (DATA / "denominators" / name).open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream, delimiter="\t", lineterminator="\n")
        writer.writerow(columns)
        writer.writerows(rows)


def build() -> dict:
    root = DATA / "research/sources"
    manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
    source = next(s for s in manifest if s["id"] == "nature-subject-directory")
    content = (root / "nature-subject-directory.txt").read_bytes()
    if hashlib.sha256(content).hexdigest() != source["sha256"]:
        raise ValueError("Nature source snapshot hash mismatch.")
    groups = parse_directory(content.decode("utf-8"))
    with (DATA / "i18n/nature-subjects.tsv").open(encoding="utf-8") as stream:
        zh = {r["id"]: r["zh"] for r in csv.DictReader(stream, delimiter="\t")}
    subjects = {}
    for group in groups:
        for entry in group["subjects"]:
            node = subjects.setdefault(entry["id"], {**entry, "groups": []})
            if node["name"] != entry["name"]:
                raise ValueError("Conflicting labels for the same Nature subject.")
            if group["id"] not in node["groups"]:
                node["groups"].append(group["id"])
    write_tsv(
        "nature-groups.tsv",
        ["id", "name_en", "name_zh"],
        [[g["id"], g["name"], zh[g["id"]]] for g in groups],
    )
    write_tsv(
        "nature-subjects.tsv",
        ["id", "name_en", "name_zh", "groups"],
        [[s["id"], s["name"], zh[s["id"]], ";".join(s["groups"])] for s in subjects.values()],
    )
    snapshot = {
        "source_url": source["url"],
        "observed_at": source["observed_at"],
        "source_sha256": source["sha256"],
        "scope": "Public two-level directory, not the full Nature subject ontology.",
        "counting": "Each subject ID counts once overall; category memberships overlap.",
        "groups": groups,
    }
    (DATA / "research/nature-subjects.json").write_text(
        json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    result = {
        "groups": len(groups),
        "subjects": len(subjects),
        "memberships": sum(len(s["groups"]) for s in subjects.values()),
    }
    print(json.dumps(result))
    return result


if __name__ == "__main__":
    build()
