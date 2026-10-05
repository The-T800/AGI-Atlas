"""中英双语：界面文案与数据词条。页面内嵌两种语言并可切换，Markdown 报告按语言分别生成。"""

import csv
import re
from functools import cache
from pathlib import Path

LANGS = ("zh", "en")

# 界面与报告共用的文案；新增文案时两种语言必须同时提供（测试会检查）。
UI: dict[str, dict[str, str]] = {
    "title": {"zh": "离 AGI 还差多少？", "en": "How far is AI from AGI?"},
    "tagline": {
        "zh": "以 O*NET 职业活动与 Nature 公开主题目录为参照，用公开基准成绩逐项计分；缺测项记 0。",
        "en": "Use O*NET work activities and the Nature public subject directory as "
        "reference sets. Score each item from published benchmarks; unmeasured items "
        "count as 0.",
    },
    "lang_switch": {"zh": "English", "en": "中文"},
    "snapshot": {"zh": "数据快照", "en": "Data snapshot"},
    "tab_gap": {"zh": "AGI 差距", "en": "AGI gap"},
    "tab_benchmarks": {"zh": "基准与成绩", "en": "Benchmarks"},
    "tab_models": {"zh": "模型", "en": "Models"},
    "tab_trend": {"zh": "趋势", "en": "Trends"},
    "jobs": {"zh": "按职业", "en": "By jobs"},
    "disciplines": {"zh": "按学科", "en": "By disciplines"},
    "ai_reached": {"zh": "AI 已达到", "en": "AI reached"},
    "measured": {"zh": "有基准测量", "en": "Measured"},
    "precise": {"zh": "主题级映射", "en": "Topic-level mappings"},
    "measured_depth": {"zh": "已测部分得分", "en": "Score where measured"},
    "bar_reached": {"zh": "AI 已达到", "en": "AI reached"},
    "bar_left": {"zh": "已测、未达到", "en": "Measured, not reached"},
    "bar_noscore": {"zh": "有基准、无成绩", "en": "Benchmark, no score"},
    "bar_blank": {"zh": "无基准", "en": "No benchmark"},
    "jobs_lead": {
        "zh": "{occupations} 个职业、{tasks} 项任务，归为 {leaves} 项工作活动",
        "en": "{occupations} occupations, {tasks} tasks, grouped into {leaves} work activities",
    },
    "disc_lead": {
        "zh": "{leaves} 个去重主题，来自 Nature 的 8 个公开目录大类",
        "en": "{leaves} unique subjects across 8 Nature directory categories",
    },
    "by_major": {"zh": "职业大类", "en": "Occupation group"},
    "by_activity": {"zh": "工作活动", "en": "Work activity"},
    "by_discipline": {"zh": "Nature 目录大类", "en": "Nature category"},
    "count": {"zh": "数量", "en": "Count"},
    "top_items": {"zh": "得分最高的细项", "en": "Top-scoring items"},
    "show_rest": {"zh": "展开其余 {n} 项", "en": "Show the other {n}"},
    "top_jobs": {"zh": "得分最高的职业", "en": "Top-scoring occupations"},
    "via": {"zh": "依据", "en": "via"},
    "direct": {"zh": "直接测量", "en": "direct"},
    "partial": {"zh": "部分测量", "en": "partial"},
    "how": {"zh": "怎么算", "en": "How it is computed"},
    "how_body": {
        "zh": "每项得分 = 覆盖系数 × 基准相对成绩；直接映射 {direct}，部分映射 {partial}。Nature "
        "主题全部使用部分映射，不将综合成绩当作单科学科成绩。每项取最高代理值；缺测项记 0。",
        "en": "Item score = coverage factor x relative benchmark score; direct = {direct}, "
        "partial = {partial}. All Nature links are partial; aggregate benchmark "
        "scores are not subject-specific results. Use the best proxy per item; "
        "unmeasured items count as 0.",
    },
    "limits": {"zh": "局限", "en": "Limitations"},
    "limits_body": {
        "zh": "映射为人工编辑，尚未独立审阅；成绩含厂商自报。{onet}{subjects}",
        "en": "Mappings are editorial and not independently reviewed; some scores are "
        "vendor-reported. {onet} {subjects}",
    },
    "source": {"zh": "来源", "en": "Source"},
    "search": {"zh": "搜索基准、能力或子任务…", "en": "Search benchmarks, abilities, tasks…"},
    "all_domains": {"zh": "全部能力", "en": "All abilities"},
    "all_status": {"zh": "全部阶段", "en": "All stages"},
    "best": {"zh": "最好成绩", "en": "Best score"},
    "no_score": {"zh": "暂无成绩", "en": "No score yet"},
    "results": {"zh": "个基准", "en": "benchmarks"},
    "view_scores": {"zh": "查看全部成绩", "en": "All scores"},
    "official": {"zh": "原始任务 ↗", "en": "Task definition ↗"},
    "setting": {"zh": "口径", "en": "Setting"},
    "model": {"zh": "模型", "en": "Model"},
    "score": {"zh": "成绩", "en": "Score"},
    "human": {"zh": "人类", "en": "Human"},
    "date": {"zh": "日期", "en": "Date"},
    "evidence": {"zh": "证据", "en": "Evidence"},
    "more": {"zh": "再显示 50 条", "en": "Show 50 more"},
    "close": {"zh": "关闭", "en": "Close"},
    "prev": {"zh": "上一页", "en": "Previous"},
    "next": {"zh": "下一页", "en": "Next"},
    "model_search": {
        "zh": "搜索模型，如 GPT、Claude、Qwen…",
        "en": "Search models, e.g. GPT, Claude…",
    },
    "rank": {"zh": "组内排名", "en": "Rank"},
    "stage": {"zh": "阶段", "en": "Stage"},
    "model_hint": {
        "zh": "排名只在同一口径（版本、协议、子集、指标）内比较。",
        "en": "Ranks compare only within the same setting (version, protocol, subset, metric).",
    },
    "horizon_title": {
        "zh": "AI 能独立完成多长的任务？（METR）",
        "en": "How long a task can AI complete on its own? (METR)",
    },
    "horizon_note": {
        "zh": "纵轴：人类专家完成该任务所需时长（对数刻度）。"
        "虚线：本页拟合，约每 {days} 天翻一倍。",
        "en": "Y-axis: time a human expert needs for the task (log scale). Dashed: our "
        "fit, doubling about every {days} days.",
    },
    "p50": {"zh": "50% 成功率", "en": "50% success"},
    "p80": {"zh": "80% 成功率", "en": "80% success"},
    "eci_title": {"zh": "综合能力指数（Epoch ECI）", "en": "Capabilities index (Epoch ECI)"},
    "eci_note": {
        "zh": "由 Epoch AI 从多个基准联合拟合，只用于模型间比较。",
        "en": "Fitted by Epoch AI across many benchmarks; for comparing models only.",
    },
    "open_weights": {"zh": "开放权重", "en": "Open weights"},
    "closed": {"zh": "闭源", "en": "Closed"},
    "footer": {
        "zh": "AGI Atlas · 开放数据，逐条可追溯 · MIT 许可",
        "en": "AGI Atlas · Open data, every number traceable · MIT License",
    },
    "unknown_date": {"zh": "未公开", "en": "n/a"},
    "minutes": {"zh": "分钟", "en": "min"},
    "hours": {"zh": "小时", "en": "h"},
    "nav_overview": {"zh": "概览", "en": "Overview"},
    "nav_jobs": {"zh": "职业", "en": "Jobs"},
    "nav_disc": {"zh": "学科", "en": "Disciplines"},
    "nav_method": {"zh": "方法", "en": "Method"},
    "nav_explore": {"zh": "数据", "en": "Data"},
    "hero_kicker": {"zh": "人类能力全景图", "en": "A map of human capability"},
    "hero_title": {
        "zh": "以 O*NET 工作活动为分母，AI 评测代理指数为",
        "en": "Across O*NET work activities, the AI benchmark proxy index is",
    },
    "hero_sub": {
        "zh": "{occupations} 个 O*NET 职业、{activities} 项工作活动，以及 {disciplines} 个 Nature "
        "公开主题，逐项对照公开评测。缺测项记 0。",
        "en": "{occupations} O*NET occupations, {activities} work activities and "
        "{disciplines} Nature directory subjects, compared with published "
        "benchmarks. Unmeasured items count as 0.",
    },
    "stat_jobs": {"zh": "人类工作", "en": "of human work"},
    "stat_disc": {"zh": "Nature 主题代理指数", "en": "Nature topic proxy index"},
    "stat_blank": {"zh": "工作没有任何基准", "en": "of work has no benchmark"},
    "stat_depth": {"zh": "已测部分的平均得分", "en": "average score where measured"},
    "mosaic_title": {
        "zh": "每一格，都是一种人类工作",
        "en": "Every square is one kind of human work",
    },
    "mosaic_sub": {
        "zh": "越亮表示 AI 得分越高；暗格表示还没有任何基准测量它。把鼠标移到格子上查看名称。",
        "en": "Brighter means a higher AI score; dark squares have never been measured. "
        "Hover to see what each one is.",
    },
    "mosaic_jobs": {"zh": "职业 · {n} 项工作活动", "en": "Jobs · {n} activities"},
    "mosaic_disc": {"zh": "Nature · {n} 个主题", "en": "Nature subjects · {n}"},
    "mosaic_caption": {
        "zh": "{scored} 项有得分 · {noscore} 项有基准无成绩 · {blank} 项无基准",
        "en": "{scored} scored · {noscore} benchmarked, no score · {blank} unmeasured",
    },
    "legend_score": {"zh": "AI 得分 0 → 100", "en": "AI score 0 → 100"},
    "legend_noscore": {"zh": "有基准、无成绩", "en": "Benchmark, no score"},
    "legend_blank": {"zh": "无基准", "en": "Unmeasured"},
    "ins1_t": {"zh": "差距主要来自“没测”", "en": "Most of the gap is unmeasured"},
    "ins1_b": {
        "zh": "{blank}% 的人类工作没有任何基准。不是 AI 做不到，而是还没有人测过。",
        "en": "{blank}% of human work has no benchmark at all. Not failed, simply never tested.",
    },
    "ins2_t": {"zh": "测到的地方，AI 已经很强", "en": "Where measured, AI is strong"},
    "ins2_b": {
        "zh": "有基准的工作上平均得分 {depth}%；最高的是“{top}”，{score} 分。",
        "en": "It averages {depth}% on benchmarked work; the best is “{top}” at {score}.",
    },
    "ins3_t": {"zh": "体力与现场工作几乎为零", "en": "Physical, on-site work is near zero"},
    "ins3_b": {"zh": "{groups}，得分均为 0。", "en": "{groups}: all score 0."},
    "jobs_title": {"zh": "哪些职业离 AI 最近", "en": "Which jobs AI is closest to"},
    "jobs_sub": {
        "zh": "实心为 AI 已达到的部分，细线为有基准覆盖的部分。",
        "en": "Solid: what AI has reached. Thin line: the share of work with any benchmark.",
    },
    "disc_title": {
        "zh": "学科：采用 Nature 公开目录",
        "en": "Subjects: the Nature public directory",
    },
    "disc_sub": {
        "zh": "8 个大类，95 个去重主题；{precise} 个主题有部分任务映射。"
        "跨类主题在总数中只计一次，各大类可重叠。",
        "en": "8 categories and 95 unique subjects; {precise} have partial task mappings. "
        "Cross-listed subjects count once overall; category totals overlap.",
    },
    "method_title": {"zh": "我们怎么算", "en": "How we measure"},
    "step1_t": {"zh": "定义分母", "en": "Define the denominator"},
    "step1_b": {
        "zh": "职业取 O*NET 31.0；学科采用 Nature 公开的两级目录，"
        "保留原始主题名称和跨类归属，不推断更深层本体。",
        "en": "Jobs use O*NET 31.0. Subjects use Nature's public two-level directory, "
        "preserving labels and cross-listings without inventing a deeper ontology.",
    },
    "step2_t": {"zh": "对照基准", "en": "Map the benchmarks"},
    "step2_b": {
        "zh": "{benchmarks} 个基准逐一挂到它真正测量的工作活动与学科上，并标注直接或部分测量。",
        "en": "Each of {benchmarks} benchmarks is linked to the activities and disciplines "
        "it actually tests, marked direct or partial.",
    },
    "step3_t": {"zh": "取最好成绩", "en": "Score by the best result"},
    "step3_b": {
        "zh": "每一项取覆盖它的基准中最好的成绩，按覆盖程度打折；没有基准测到的，记 0。",
        "en": "Each item takes the best score among the benchmarks that cover it, "
        "discounted by how directly it is measured. Unmeasured items score zero.",
    },
    "explore_title": {"zh": "探索数据", "en": "Explore the data"},
    "explore_sub": {
        "zh": "{benchmarks} 个基准 · {scores} 条成绩 · {models} 个模型，每一条都可追溯到来源。",
        "en": "{benchmarks} benchmarks · {scores} scores · {models} models, each "
        "traceable to its source.",
    },
    "reached": {"zh": "达到人类水平", "en": "Human level"},
    "near": {"zh": "接近满分", "en": "Near ceiling"},
    "progress": {"zh": "进行中", "en": "In progress"},
    "gap": {"zh": "差距明显", "en": "Large gap"},
    "unknown": {"zh": "无上限量尺", "en": "Unbounded scale"},
    "none": {"zh": "暂无成绩", "en": "No score"},
    "official_benchmark": {"zh": "官方榜单", "en": "Official leaderboard"},
    "independent_evaluation": {"zh": "独立评测", "en": "Independent eval"},
    "paper": {"zh": "论文", "en": "Paper"},
    "model_provider": {"zh": "厂商报告", "en": "Vendor report"},
    "community": {"zh": "社区", "en": "Community"},
    "nature_directory": {
        "zh": "查看全部 Nature 主题与映射依据",
        "en": "Browse all Nature subjects and mapping evidence",
    },
    "nature_topic_hint": {
        "zh": "目录主题并非完整知识清单。分数为基准任务代理值，不能视作整门学科掌握度。",
        "en": "Directory topics are not a complete inventory of knowledge. Scores "
        "are benchmark task proxies, not whole-subject mastery.",
    },
}

# 报告专用文案
REPORT: dict[str, dict[str, str]] = {
    "summary_head": {"zh": "## 结论", "en": "## Results"},
    "denominator": {"zh": "分母", "en": "Denominator"},
    "size": {"zh": "规模", "en": "Size"},
    "jobs_size": {
        "zh": "{occupations} 职业 · {leaves} 工作活动",
        "en": "{occupations} jobs · {leaves} activities",
    },
    "disc_size": {"zh": "{leaves} 个 Nature 主题", "en": "{leaves} Nature subjects"},
    "by_major_head": {"zh": "## 按职业大类", "en": "## By occupation group"},
    "by_disc_head": {"zh": "## 按 Nature 目录大类", "en": "## By Nature directory category"},
    "benchmarks_head": {"zh": "## 各基准最好成绩", "en": "## Best score per benchmark"},
    "benchmark": {"zh": "基准", "en": "Benchmark"},
    "domain": {"zh": "能力域", "en": "Domain"},
    "how_head": {"zh": "## 怎么算", "en": "## Method"},
    "rebuild": {
        "zh": "本报告由 `uv run agi-atlas report` 生成，请勿手改。",
        "en": "Generated by `uv run agi-atlas report`; do not edit by hand.",
    },
}


def t(key: str, lang: str, **values: object) -> str:
    entry = UI.get(key) or REPORT[key]
    return entry[lang].format(**values) if values else entry[lang]


@cache
def _terms(path: str) -> dict[str, str]:
    with Path(path).open(encoding="utf-8", newline="") as f:
        rows = csv.DictReader((line for line in f if not line.startswith("#")), delimiter="\t")
        return {r["zh"]: r["en"] for r in rows}


HAN = re.compile(r"[一-鿿]")


def term_table(data_dir: Path | str) -> dict[str, str]:
    path = Path(data_dir) / "i18n/terms.tsv"
    return _terms(str(path)) if path.exists() else {}


def translate(text: str | None, table: dict[str, str]) -> str | None:
    """整句命中词表直接替换；否则逐段替换中文片段，未收录的中文保留原文。"""
    if text is None or not HAN.search(text):
        return text
    if text in table:
        return table[text]
    for sep in (" / ", "/", "；", ";", "、"):
        if sep in text:
            joined = (" / " if sep == "/" else ("; " if sep in "；;" else ", ")).join(
                translate(part.strip(), table) or "" for part in text.split(sep)
            )
            return joined
    return text
