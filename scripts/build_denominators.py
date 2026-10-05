"""Build O*NET activity tables and the pinned Nature public subject directory."""

import csv
import hashlib
import io
import json
from collections import defaultdict
from pathlib import Path
from urllib.request import Request, urlopen

from build_nature import build as build_nature

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / ".cache/denominators"
OUT = ROOT / "data/denominators"
# Required English-to-Chinese occupation and activity labels.
I18N = ROOT / "data/i18n"
ONET_BASE = "https://www.onetcenter.org/dl_files/database/db_31_0_csv/"
ONET_FILES = {
    "occupation_data.csv": "a09eae1d6609686e44e05b7290993a1c8b523d8ca224bc0eedc194c855c3ee02",
    "task_statements.csv": "4568e14d8db6f05551ad37e056e909b13ebae4a26bcb5ff915bb5f281d582c57",
    "task_ratings.csv": "52ee4ad320f1ca3c3865795aefc7393d422a9bfbfea3a5b5d9eaf2928c10eafe",
    "tasks_to_dwas.csv": "15624d31acb85627736a87dc7c485edffe30361262571c8242fad4ae9e7678a6",
    "gwas_to_iwas_to_dwas.csv": "ae4e9f166187bfe8e6328a21470689ed188e7ed831090ace2a21c66cebb31a49",
    "job_zones.csv": "093f01891ac2e602a8cc6c859ecb619b5bc00eb50cd3f3c1134c05b704481944",
}


def fetch(name: str, url: str, sha256: str) -> bytes:
    path = CACHE / name
    if not path.exists():
        CACHE.mkdir(parents=True, exist_ok=True)
        request = Request(url, headers={"User-Agent": "AGI-Atlas-research/0.2"})
        with urlopen(request, timeout=120) as response:
            path.write_bytes(response.read())
    content = path.read_bytes()
    digest = hashlib.sha256(content).hexdigest()
    if digest != sha256:
        raise SystemExit(f"{name} 哈希不符：{digest}；上游可能已更新，请人工核对后再改固定哈希")
    return content


def rows(name: str) -> list[dict]:
    content = fetch(name, ONET_BASE + name, ONET_FILES[name])
    return list(csv.DictReader(io.StringIO(content.decode("utf-8"))))


def write_tsv(path: Path, header: list[str], records: list[list]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter="\t", lineterminator="\n")
        writer.writerow(header)
        writer.writerows(records)


def translations(name: str, key: str, value: str) -> dict[str, str]:
    with (I18N / name).open(encoding="utf-8", newline="") as f:
        lines = (line for line in f if not line.startswith("#"))
        table = {r[key]: r[value] for r in csv.DictReader(lines, delimiter="	")}
    if missing := [k for k, v in table.items() if not v.strip()]:
        raise SystemExit(f"{name} 有 {len(missing)} 条缺译文，例如 {missing[0]}")
    return table


def build_onet() -> dict:
    hierarchy = rows("gwas_to_iwas_to_dwas.csv")
    links = rows("tasks_to_dwas.csv")
    importance = {
        (r["O*NET-SOC Code"], r["Task ID"]): float(r["Data Value"])
        for r in rows("task_ratings.csv")
        if r["Scale ID"] == "IM"
    }
    tasks = rows("task_statements.csv")
    zones = {r["O*NET-SOC Code"]: int(r["Job Zone"]) for r in rows("job_zones.csv")}
    titles = {r["O*NET-SOC Code"]: r["Title"] for r in rows("occupation_data.csv")}
    dwa_zh = translations("onet-dwa.tsv", "dwa_id", "zh")
    title_zh = translations("onet-occupations.tsv", "soc", "zh")

    task_dwas = defaultdict(set)
    for r in links:
        task_dwas[(r["O*NET-SOC Code"], r["Task ID"])].add(r["DWA Element ID"])
    by_occupation = defaultdict(list)
    for t in tasks:
        key = (t["O*NET-SOC Code"], t["Task ID"])
        if task_dwas[key]:
            by_occupation[t["O*NET-SOC Code"]].append(key)

    # 职业内工作量：任务按重要性（1–5）分配权重；缺评分的任务取该职业均值；一个任务平均分给其 DWA。
    occupation_rows, share = [], defaultdict(float)
    occupations_of = defaultdict(set)
    for soc, keys in sorted(by_occupation.items()):
        rated = [importance[k] for k in keys if k in importance]
        fallback = sum(rated) / len(rated) if rated else 3.0
        weights = {k: importance.get(k, fallback) for k in keys}
        total = sum(weights.values())
        dwa_weight = defaultdict(float)
        for k, w in weights.items():
            for d in task_dwas[k]:
                dwa_weight[d] += w / total / len(task_dwas[k])
                occupations_of[d].add(soc)
        for d, w in dwa_weight.items():
            share[d] += w / len(by_occupation)
        occupation_rows.append(
            [
                soc,
                titles[soc],
                title_zh[soc],
                zones.get(soc, ""),
                len(keys),
                ";".join(f"{d}:{w:.5f}" for d, w in sorted(dwa_weight.items())),
            ]
        )

    dwa_rows = [
        [
            r["DWA Element ID"],
            r["DWA Element Name"],
            dwa_zh[r["DWA Element ID"]],
            r["IWA Element ID"],
            r["IWA Element Name"],
            r["GWA Element ID"],
            r["GWA Element Name"],
            len(occupations_of[r["DWA Element ID"]]),
            f"{share[r['DWA Element ID']]:.6f}",
        ]
        for r in hierarchy
    ]
    write_tsv(
        OUT / "onet-dwa.tsv",
        ["dwa_id", "dwa", "dwa_zh", "iwa_id", "iwa", "gwa_id", "gwa", "occupations", "work_share"],
        dwa_rows,
    )
    write_tsv(
        OUT / "onet-occupations.tsv",
        ["soc", "title", "title_zh", "job_zone", "tasks", "dwa_weights"],
        occupation_rows,
    )
    return {
        "dwa": len(dwa_rows),
        "iwa": len({r[3] for r in dwa_rows}),
        "gwa": len({r[5] for r in dwa_rows}),
        "occupations": len(occupation_rows),
        "tasks": sum(r[4] for r in occupation_rows),
    }


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    summary = {"onet": build_onet(), "nature": build_nature()}
    print(json.dumps(summary, ensure_ascii=False))
