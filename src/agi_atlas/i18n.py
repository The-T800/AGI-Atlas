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
        "zh": "O*NET 职业活动、OpenAlex 科研主题与"
        "独立能力标签共同组织评测证据；学科未测项保持未知。",
        "en": "Benchmark evidence organized by O*NET work activities, OpenAlex research "
        "topics and independent capability labels. Unmeasured subjects remain unknown.",
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
    "bar_noscore": {"zh": "已关联、成绩待核验", "en": "Linked, results pending"},
    "bar_blank": {"zh": "关联待建立", "en": "Mapping pending"},
    "jobs_lead": {
        "zh": "{occupations} 个职业、{tasks} 项任务，归为 {leaves} 项工作活动",
        "en": "{occupations} occupations, {tasks} tasks, grouped into {leaves} work activities",
    },
    "disc_lead": {
        "zh": "{leaves} 个主题，来自 OpenAlex 四级科研分类",
        "en": "{leaves} topics in the four-level OpenAlex research taxonomy",
    },
    "by_major": {"zh": "职业大类", "en": "Occupation group"},
    "by_activity": {"zh": "工作活动", "en": "Work activity"},
    "by_discipline": {"zh": "OpenAlex 学科", "en": "OpenAlex field"},
    "count": {"zh": "数量", "en": "Count"},
    "top_items": {"zh": "得分最高的细项", "en": "Top-scoring items"},
    "show_rest": {"zh": "展开其余 {n} 项", "en": "Show the other {n}"},
    "top_jobs": {"zh": "得分最高的职业", "en": "Top-scoring occupations"},
    "via": {"zh": "依据", "en": "via"},
    "direct": {"zh": "直接测量", "en": "direct"},
    "partial": {"zh": "部分测量", "en": "partial"},
    "how": {"zh": "怎么算", "en": "How it is computed"},
    "how_body": {
        "zh": "职业代理指数按覆盖系数乘基准相对成绩：直接 {direct}、部分 {partial}，缺测贡献记 "
        "0。学科轴只展示任务关联和基准原始成绩，未测为未知；不计算学科或 AGI 完成百分比。",
        "en": "The work proxy multiplies relative benchmark scores by coverage factors: "
        "direct {direct}, partial {partial}; missing evidence contributes zero. The "
        "subject axis shows task links and original benchmark results, with unknowns "
        "preserved. It does not compute subject mastery or AGI completion.",
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
        "zh": "{occupations} 个 O*NET 职业、{activities}"
        " 项工作活动；学科轴使用 {disciplines} 个 OpenAlex "
        "科研主题。工作代理指数缺测贡献记 0；学科未知项不记失败。",
        "en": "{occupations} O*NET occupations and {activities} work activities; the subject "
        "axis uses {disciplines} OpenAlex research topics. Missing work evidence "
        "contributes zero to the proxy; unknown subjects are not failures.",
    },
    "stat_jobs": {"zh": "人类工作", "en": "of human work"},
    "stat_disc": {
        "zh": "主题有明确任务映射（非掌握度）",
        "en": "of topics have explicit task links (not mastery)",
    },
    "stat_covered": {"zh": "工作已有基准覆盖", "en": "of work covered by benchmarks"},
    "stat_depth": {"zh": "已测部分的平均得分", "en": "average score where measured"},
    "mosaic_title": {
        "zh": "每一格，都是一种人类工作",
        "en": "Every square is one kind of human work",
    },
    "mosaic_sub": {
        "zh": "亮格显示已收录的工作任务证据，越亮表示工作代理得分越高。把鼠标移到格子上查看名称。",
        "en": "Highlighted squares show recorded work evidence; "
        "brighter means a higher work proxy score. "
        "Hover to see what each one is.",
    },
    "subject_mosaic_title": {
        "zh": "每一格，都是一个科研主题",
        "en": "Every square is one research topic",
    },
    "subject_mosaic_sub": {
        "zh": "颜色表示证据状态：主题任务成绩、已挂靠暂无成绩、仅上级参考、待建立映射。"
        "不表示学科掌握度；待映射不等于没有相关 Benchmark。",
        "en": "Colors show task results, links without results, "
        "parent context, or pending mapping. "
        "They do not measure subject mastery; pending mapping does not mean no benchmark exists.",
    },
    "mosaic_jobs": {"zh": "职业 · {n} 项工作活动", "en": "Jobs · {n} activities"},
    "mosaic_disc": {"zh": "OpenAlex · {n} 个主题", "en": "OpenAlex topics · {n}"},
    "mosaic_caption": {
        "zh": "{mapped} / {total} 项工作活动已有基准关联 · {scored} 项有代理得分",
        "en": "{mapped} / {total} work activities linked to benchmarks · "
        "{scored} with proxy scores",
    },
    "subject_mosaic_caption": {
        "zh": "{mapped} / {total} 个主题已有明确任务关联 · {scored} 个有成绩证据",
        "en": "{mapped} / {total} topics with explicit task links · {scored} with result evidence",
    },
    "subject_legend_score": {
        "zh": "有任务成绩证据（非学科分数）",
        "en": "Task results, not subject scores",
    },
    "subject_legend_noscore": {"zh": "已挂靠、成绩待核验", "en": "Linked, results pending"},
    "subject_legend_context": {"zh": "仅上级有关联", "en": "Parent context only"},
    "subject_legend_blank": {"zh": "待建立映射", "en": "Awaiting mapping"},
    "legend_score": {"zh": "AI 得分 0 → 100", "en": "AI score 0 → 100"},
    "legend_noscore": {"zh": "已关联、得分待核验", "en": "Linked, scores pending"},
    "legend_blank": {"zh": "关联待建立", "en": "Mapping pending"},
    "ins1_t": {"zh": "已有基准覆盖的工作", "en": "Work with benchmark coverage"},
    "ins1_b": {
        "zh": "{covered}% 的工作已有基准覆盖（按职业加权）；"
        "{mapped} / {total} 项工作活动已建立任务关联。",
        "en": "{covered}% of work has benchmark coverage (occupation-weighted); "
        "{mapped} / {total} work activities have task links.",
    },
    "ins2_t": {"zh": "测到的地方，AI 已经很强", "en": "Where measured, AI is strong"},
    "ins2_b": {
        "zh": "有基准的工作上平均得分 {depth}%；最高的是“{top}”，{score} 分。",
        "en": "It averages {depth}% on benchmarked work; the best is “{top}” at {score}.",
    },
    "ins3_t": {"zh": "职业中的覆盖进展", "en": "Coverage across occupations"},
    "ins3_b": {"zh": "已有基准覆盖：{groups}。", "en": "Benchmark coverage: {groups}."},
    "jobs_title": {"zh": "哪些职业离 AI 最近", "en": "Which jobs AI is closest to"},
    "jobs_sub": {
        "zh": "实心为 AI 已达到的部分，细线为有基准覆盖的部分。",
        "en": "Solid: what AI has reached. Thin line: the share of work with any benchmark.",
    },
    "disc_title": {
        "zh": "学科 × 能力：OpenAlex 研究地图",
        "en": "Subjects × capabilities: the OpenAlex research map",
    },
    "disc_sub": {
        "zh": "{domains} 个大域 → {fields} 个学科 → {subfields} 个子领域 → {topics} "
        "个主题。点击矩阵查看评测证据，或筛选、搜索具体主题。",
        "en": "{domains} domains → {fields} fields → {subfields} subfields → {topics} "
        "topics. Select a matrix cell for benchmark evidence, or filter and search "
        "individual topics.",
    },
    "method_title": {"zh": "我们怎么算", "en": "How we measure"},
    "step1_t": {"zh": "定义分母", "en": "Define the denominator"},
    "step1_b": {
        "zh": "职业使用 O*NET；学科导入官方 OpenAlex"
        " 四级体系，保留版本和时间戳；能力是独立的项目标签。",
        "en": "Work uses O*NET. Subjects use the official four-level OpenAlex hierarchy with "
        "release dates and timestamps. Capabilities are independent project "
        "annotations.",
    },
    "step2_t": {"zh": "对照基准", "en": "Map the benchmarks"},
    "step2_b": {
        "zh": "为 {benchmarks} 个 Benchmark "
        "标注能力；学科只挂到任务证据支持的层级，无法确认就留空。",
        "en": "Annotate capabilities for {benchmarks} benchmarks; link subjects only at the "
        "level supported by task evidence, leaving uncertain subjects unassigned.",
    },
    "step3_t": {"zh": "取最好成绩", "en": "Score by the best result"},
    "step3_b": {
        "zh": "同版本、协议和子集内比较成绩。学科证据默认展示近 12"
        " 个月有明确日期的结果；历史与未知日期记录保留在明细。",
        "en": "Compare results within the same version, protocol and subset. Subject evidence "
        "highlights dated results from the past 12 months; historical and undated "
        "records remain in details.",
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
    "disc_note": {
        "zh": "{leaves} 个 OpenAlex 科研主题，不等于完整人类能力清单",
        "en": "{leaves} OpenAlex research topics, not a complete capability inventory",
    },
    "matrix_hint": {
        "zh": "矩阵数字 = 相关 Benchmark 数量，不是分数。横"
        "向为独立能力标签；“—”表示未建立证据关联，不代表能力为零。",
        "en": "Matrix numbers count related benchmarks, not scores. Columns are "
        "independent capability labels. A dash means no established evidence link, "
        "not zero ability.",
    },
    "subject_score_hint": {
        "zh": "仅展示近 12 个月有评测或发布日期的同口径成绩。分数属于 B"
        "enchmark，不代表整门学科；来源抓取日期不会代替评测日期。",
        "en": "Only comparable results with evaluation or publication dates in the "
        "past 12 months are highlighted. Scores belong to benchmarks, not "
        "entire subjects; retrieval dates never replace evaluation dates.",
    },
    "taxonomy_freshness": {
        "zh": "分类版本：{release} · 分类抓取：{retrieved} · "
        "评测来源最近抓取：{scores}。原始更新时间可在主题中查看。",
        "en": "Taxonomy release: {release} · taxonomy retrieved: {retrieved} · "
        "latest score-source retrieval: {scores}. Original update timestamps "
        "are available inside topics.",
    },
    "source_updated": {"zh": "来源记录更新时间", "en": "Source record updated"},
    "evaluation_date": {"zh": "评测日期", "en": "Evaluated"},
    "published_date": {"zh": "发布日期", "en": "Published"},
    "retrieved_date": {"zh": "抓取日期", "en": "Retrieved"},
    "live_api": {"zh": "实时 API 快照", "en": "Live API snapshot"},
}

REPORT: dict[str, dict[str, str]] = {
    "summary_head": {"zh": "## 结论", "en": "## Results"},
    "denominator": {"zh": "分母", "en": "Denominator"},
    "size": {"zh": "规模", "en": "Size"},
    "jobs_size": {
        "zh": "{occupations} 职业 · {leaves} 工作活动",
        "en": "{occupations} jobs · {leaves} activities",
    },
    "disc_size": {"zh": "{leaves} 个 OpenAlex 主题", "en": "{leaves} OpenAlex topics"},
    "by_major_head": {"zh": "## 按职业大类", "en": "## By occupation group"},
    "by_disc_head": {
        "zh": "## 按 OpenAlex 学科的证据覆盖",
        "en": "## Evidence links by OpenAlex field",
    },
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
