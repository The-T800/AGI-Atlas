"""生成中英文 Markdown 报告：先给结论，再给分组明细与各基准最好成绩。"""

from pathlib import Path

from agi_atlas.i18n import LANGS, t
from agi_atlas.models import AtlasData
from agi_atlas.site import build_payload


def _cell(value: object) -> str:
    return (
        str(value)
        .replace("\\", "\\\\")
        .replace("|", "\\|")
        .replace("\r", " ")
        .replace("\n", " ")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def _pct(value: float | None) -> str:
    return "—" if value is None else f"{value:g}%"


def _summary(payload: dict, lang: str) -> list[str]:
    o, g = payload["progress"]["onet"], payload["progress"]["openalex"]
    lines = [
        f"| {t('denominator', lang)} | {t('size', lang)} | {t('measured', lang)} | "
        f"{t('measured_depth', lang)} | **{t('ai_reached', lang)}** |",
        "| --- | --- | ---: | ---: | ---: |",
    ]
    for d, size in (
        (o, t("jobs_size", lang, occupations=o["occupations"], leaves=o["summary"]["leaves"])),
        (g, t("disc_size", lang, leaves=g["summary"]["leaves"])),
    ):
        s = d["summary"]
        measured = _pct(s["mapped_share"])
        if d is g:
            measured = (
                f"{s['mapped']} / {s['leaves']} "
                + ("主题已挂靠" if lang == "zh" else "topics linked")
                + f"; {s['scored']} "
                + ("有任务成绩证据" if lang == "zh" else "with task results")
            )
        lines.append(
            f"| {_cell(d['name'][lang])} | {size} | {measured} | {_pct(s['depth'])} | "
            f"**{_pct(s['progress'])}** |"
        )
    return lines


def render_report(data: AtlasData, data_dir: Path | str, lang: str = "en") -> str:
    payload = build_payload(data, data_dir)
    p = payload["progress"]
    o, g = p["onet"], p["openalex"]
    other = "en" if lang == "zh" else "zh"
    lines = [
        f"# AGI Atlas · {t('title', lang)}",
        "",
        f"[{t('lang_switch', lang)}](report.{other}.md) · {t('snapshot', lang)} "
        f"{payload['snapshot']} · {t('rebuild', lang)}",
        "",
        t("tagline", lang),
        "",
        t(
            "taxonomy_freshness",
            lang,
            release=g["release_date"] or t("live_api", lang),
            retrieved=g["retrieved_at"][:10],
            scores=payload["snapshot"],
        ),
        "",
        t("summary_head", lang),
        "",
        *_summary(payload, lang),
        "",
    ]
    summary = g["summary"]
    if lang == "zh":
        lines += [
            f"学科关联：{summary['linked_benchmarks']} / {len(data.benchmarks)} 个 Benchmark；"
            f"其中 {summary['scored_benchmarks']} 个有成绩、{summary['recent_benchmarks']} "
            "个有近一年日期明确的成绩。",
            "",
            "| 层级 | 总数 | 本层明确挂靠 | 含下级关联 | 有成绩证据 | 近一年成绩证据 |",
        ]
    else:
        lines += [
            f"Subject links: {summary['linked_benchmarks']} / {len(data.benchmarks)} benchmarks; "
            f"{summary['scored_benchmarks']} have results, {summary['recent_benchmarks']} "
            "have dated results within the past year.",
            "",
            "| Level | Total | Explicit links | Including descendants | Result evidence | "
            "Recent evidence |",
        ]
    lines.append("| --- | ---: | ---: | ---: | ---: | ---: |")
    for level, label in zip(
        ("domain", "field", "subfield", "topic"),
        ("大域", "学科", "子领域", "主题")
        if lang == "zh"
        else ("Domain", "Field", "Subfield", "Topic"),
        strict=True,
    ):
        c = g["coverage"][level]
        lines.append(
            f"| {label} | {c['total']} | {c['direct']} | {c['linked']} | {c['scored']} | "
            f"{c['recent']} |"
        )
    lines += [
        "",
        "以上为关联和证据数量，不是学科分数。上级关联仅作参考；待映射不等于不存在基准。"
        if lang == "zh"
        else "These are link and evidence counts, not subject scores. "
        "Parent links provide context; "
        "pending mapping does not mean no benchmark exists.",
        "",
        t("by_major_head", lang),
        "",
        f"| {t('by_major', lang)} | {t('count', lang)} | {t('ai_reached', lang)} | "
        f"{t('measured', lang)} |",
        "| --- | ---: | ---: | ---: |",
    ]
    for r in o["occupation_groups"]:
        lines.append(
            f"| {_cell(r['name'][lang])} | {r['occupations']} | {_pct(r['progress'])} | "
            f"{_pct(r['mapped_share'])} |"
        )
    lines += [
        "",
        t("by_disc_head", lang),
        "",
        f"| {t('by_discipline', lang)} | OpenAlex topics | Benchmarks |",
        "| --- | ---: | ---: |",
    ]
    for r in g["groups"]:
        count = sum(n["field"] == r["id"] for n in g["subjects"])
        lines.append(f"| {_cell(r['name'][lang])} | {count} | {len(r['benchmark_ids'])} |")
    lines += [
        "",
        t("benchmarks_head", lang),
        "",
        f"| {t('benchmark', lang)} | {t('domain', lang)} | {t('setting', lang)} | "
        f"{t('best', lang)} | {t('model', lang)} | {t('stage', lang)} | {t('source', lang)} |",
        "| --- | --- | --- | ---: | --- | --- | --- |",
    ]
    rep = {grp["benchmark_id"]: grp for grp in payload["groups"] if grp["representative"]}
    for b in payload["benchmarks"]:
        domain = (b["path"] if lang == "zh" else b["path_en"]).split("/")[0]
        grp = rep.get(b["id"])
        if grp is None:
            lines.append(
                f"| {_cell(b['name'])} | {_cell(domain)} | — | — | — | {t('none', lang)} | "
                f"[{t('official', lang)}](<{b['url']}>) |"
            )
            continue
        w = grp["records"][0]
        names = grp if lang == "zh" else grp["en"]
        lines.append(
            f"| {_cell(b['name'])} | {_cell(domain)} | {_cell(names['version'])} | "
            f"{w['score']:.4g} {_cell(names['unit'])} | {_cell(w['model'])} | "
            f"{t(b['status'], lang)} | "
            f"[{t(w['source_type'], lang)}](<{payload['sources'][w['source_url']]}>) |"
        )
    c = p["coverage_factor"]
    colon = "：" if lang == "zh" else ": "
    lines += [
        "",
        t("how_head", lang),
        "",
        t("how_body", lang, direct=c["direct"], partial=c["partial"]),
        "",
        f"**{t('limits', lang)}**{colon}"
        + t("limits_body", lang, onet=o["limitation"][lang], subjects=g["limitation"][lang]),
        "",
        f"{t('source', lang)}{colon}[O*NET 31.0](<{o['source_url']}>) · "
        f"[OpenAlex topics](<{g['source_url']}>) · [METR](<{payload['horizons']['source_url']}>)"
        + (f" · [Epoch AI ECI](<{payload['eci']['source_url']}>)" if payload["eci"] else ""),
        "",
    ]
    return "\n".join(lines)


def write_reports(data: AtlasData, data_dir: Path | str, output_dir: Path | str) -> list[Path]:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    paths = []
    for lang in LANGS:
        path = out / f"report.{lang}.md"
        path.write_text(render_report(data, data_dir, lang), encoding="utf-8")
        paths.append(path)
    return paths
