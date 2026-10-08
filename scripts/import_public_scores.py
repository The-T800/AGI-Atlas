"""从留存一手表格重建成绩；不把未知评测日期或未给出的版本补成事实。"""

import csv
import io
import json
import re
import zipfile
from pathlib import Path

import yaml
from source_tables import Tables

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ROOT / "data/research/sources"
MANIFEST = {x["id"]: x for x in json.loads((SOURCES / "manifest.json").read_text(encoding="utf-8"))}
SCORES = []


def provider(name):
    value = name.lower()
    if "sensenova" in value:
        return "SenseNova-SI 团队"
    for names, org in [
        (("gpt", "openai", "o1", "o3", "o4"), "OpenAI"),
        (("claude", "opus", "fable"), "Anthropic"),
        (("gemini", "gemma"), "Google"),
        (("deepseek",), "DeepSeek"),
        (("qwen",), "Alibaba"),
        (("kimi", "k2.5"), "Moonshot"),
        (("llama",), "Meta"),
        (("internvl",), "上海人工智能实验室"),
        (("hy ",), "Tencent"),
        (("doubao",), "ByteDance"),
    ]:
        if any(x in value for x in names):
            return org
    return "来源未单独标注"


def add(
    key,
    version,
    model,
    value,
    source,
    protocol,
    locator,
    *,
    metric="准确率",
    unit="%",
    subset="overall",
    human=None,
    published=None,
    source_type="model_provider",
    notes="",
    org=None,
    evaluated=None,
):
    info = MANIFEST[source]
    SCORES.append(
        dict(
            benchmark_id=key,
            benchmark_version=version,
            model=model,
            model_provider=org or provider(model),
            score=float(value),
            human_score=human,
            # 仅当来源逐条给出评测/运行日期时填写；默认未知。
            evaluation_date=evaluated,
            published_at=published,
            observed_at=info["observed_at"],
            protocol=protocol,
            subset=subset,
            metric=metric,
            unit=unit,
            source_url=info["url"],
            source_type=source_type,
            verified=True,
            source_locator=locator,
            source_sha256=info["sha256"],
            notes=notes
            or "已核对原始公开表格；verified 表示转录核验，未独立重跑；评测日期未公开。",
        )
    )


def html_tables(source):
    parser = Tables()
    parser.feed((SOURCES / f"{source}.txt").read_text(encoding="utf-8"))
    return parser.tables


# 表中名称 → 基准ID；只导入能明确识别的公开任务，不导入厂商私有评测。
QWEN = {
    "MMLU-Pro": "mmlu-pro",
    "MMLU-Redux": "mmlu-redux",
    "SuperGPQA": "supergpqa",
    "C-Eval": "c-eval",
    "IFEval": "ifeval",
    "IFBench": "ifbench",
    "MultiChallenge": "multichallenge",
    "AA-LCR": "aa-lcr",
    "LongBench v2": "longbench-v2",
    "GPQA": "gpqa",
    "GPQA Diamond": "gpqa",
    "HLE": "hle",
    "LiveCodeBench v6": "livecodebench",
    "HMMT Feb 25": "hmmt",
    "HMMT Nov 25": "hmmt",
    "IMOAnswerBench": "imo-answer",
    "AIME26": "aime",
    "BFCL-V4": "bfcl",
    "TAU2-Bench": "tau2",
    "VITA-Bench": "vita",
    "DeepPlanning": "deepplanning",
    "Tool Decathlon": "toolathlon",
    "MCP-Mark": "mcpmark",
    "HLE w/ tool": "hle",
    "HLE w/ tools": "hle",
    "BrowseComp": "browsecomp",
    "BrowseComp-zh": "browsecomp-zh",
    "WideSearch": "widesearch",
    "MMMLU": "mmmlu",
    "MMLU-ProX": "mmlu-prox",
    "INCLUDE": "include",
    "Global PIQA": "global-piqa",
    "PolyMATH": "polymath",
    "SWE-bench Verified": "swe-bench",
    "SWE-bench Multilingual": "swe-multilingual",
    "SecCodeBench": "seccodebench",
    "Terminal Bench 2": "terminal-bench",
    "Terminal Bench 2.1": "terminal-bench",
    "MMMU": "mmmu",
    "MMMU-Pro": "mmmu-pro",
    "MathVision": "mathvision",
    "Mathvista(mini)": "mathvista",
    "We-Math": "we-math",
    "DynaMath": "dynamath",
    "ZEROBench": "zerobench",
    "ZEROBench_sub": "zerobench",
    "BabyVision": "babyvision",
    "RealWorldQA": "realworldqa",
    "MMStar": "mmstar",
    "HallusionBench": "hallusionbench",
    "MMBenchEN-DEV-v1.1": "mmbench",
    "SimpleVQA": "simplevqa",
    "OmniDocBench1.5": "omnidocbench",
    "CharXiv(RQ)": "charxiv",
    "MMLongBench-Doc": "mmlongbench-doc",
    "CC-OCR": "cc-ocr",
    "AI2D_TEST": "ai2d",
    "OCRBench": "ocrbench",
    "ERQA": "erqa",
    "CountBench": "countbench",
    "RefCOCO(avg)": "refcoco",
    "ODInW13": "odinw",
    "EmbSpatialBench": "embspatial",
    "RefSpatialBench": "refspatial",
    "LingoQA": "lingoqa",
    "V*": "vstar",
    "VideoMME(w sub.)": "video-mme",
    "VideoMME(w/o sub.)": "video-mme",
    "VideoMMMU": "videommmu",
    "MLVU (M-Avg)": "mlvu",
    "MVBench": "mvbench",
    "LVBench": "lvbench",
    "MMVU": "mmvu",
    "ScreenSpot Pro": "screenspot-pro",
    "OSWorld-Verified": "osworld",
    "AndroidWorld": "androidworld",
    "SLAKE": "slake",
    "PMC-VQA": "pmc-vqa",
    "MedXpertQA-MM": "medxpertqa",
    "SWE-bench Pro": "swe-bench-pro",
    "NL2Repo-Bench": "nl2repo",
    "PaperBench": "paperbench",
    "HealthBench": "healthbench",
    "MRCR v2 256K (8-needle)": "mrcr",
}


def import_qwen():
    for source in ("qwen35-card", "qwen38-card"):
        for ti, table in enumerate(html_tables(source)):
            models = table[0][1:]
            for row in table[1:]:
                if row[0] not in QWEN or len(row) != len(models) + 1:
                    continue
                name, key = row[0], QWEN[row[0]]
                version = f"{name} / {source}快照"
                metric = "报告得分"
                unit = "分"
                if key in {
                    "mmlu-pro",
                    "mmlu-redux",
                    "supergpqa",
                    "c-eval",
                    "gpqa",
                    "hle",
                    "aime",
                    "hmmt",
                    "imo-answer",
                    "mmmlu",
                    "mmlu-prox",
                    "include",
                    "global-piqa",
                    "polymath",
                    "mmmu",
                    "mmmu-pro",
                    "mathvision",
                    "mathvista",
                    "realworldqa",
                    "mmstar",
                    "mmbench",
                    "simplevqa",
                    "ai2d",
                    "countbench",
                    "video-mme",
                    "mvbench",
                    "lvbench",
                    "videommmmu",
                    "slake",
                    "pmc-vqa",
                    "medxpertqa",
                    "screenspot-pro",
                }:
                    metric, unit = "准确率", "%"
                if key in {
                    "swe-bench",
                    "swe-multilingual",
                    "swe-bench-pro",
                    "nl2repo",
                    "terminal-bench",
                    "osworld",
                    "androidworld",
                    "browsecomp",
                    "browsecomp-zh",
                    "deepplanning",
                    "toolathlon",
                    "mcpmark",
                    "livecodebench",
                    "ifeval",
                    "ifbench",
                }:
                    metric, unit = "任务通过率", "%"
                for model, raw in zip(models, row[1:], strict=True):
                    variants = [(raw, "")]
                    if "/" in raw:
                        if key in {"babyvision", "vstar"}:
                            variants = list(
                                zip(
                                    raw.split("/"),
                                    ("；启用代码解释器", "；不启用代码解释器"),
                                    strict=True,
                                )
                            )
                        else:
                            # BrowseComp 的两种设置不能在未知协议下任取一个数。
                            continue
                    for value, suffix in variants:
                        if not re.fullmatch(r"\d+(?:\.\d+)?", value.strip()):
                            continue
                        note = (
                            "厂商模型卡转录；外部模型成绩也由该厂商报告，未独立重跑。"
                            "具体提示、工具与预算见原文脚注；"
                            "原文未给出子集/修订时以来源快照固定口径。"
                        )
                        if source == "qwen38-card" and key == "swe-bench-pro":
                            note += "该表修正了部分任务并重评基线，不与原始Pro榜单合并。"
                        if key == "nl2repo":
                            note += (
                                "Claude Code 脚手架，禁用访问目标仓库的 Bash 命令；原文未注明单位。"
                            )
                        if key == "paperbench":
                            metric, unit = "复现评分", "分"
                            note += "BasicAgent Code-Dev；Opus 4.6裁判；3次均值；每次最多12小时。"
                        if key == "mathvision":
                            note += "自家模型固定boxed提示，其他模型取有无boxed两种提示较高值。"
                        if key == "omnidocbench":
                            metric = "文档解析综合分"
                        if key == "widesearch":
                            metric, unit = "item-F1", "分"
                        add(
                            key,
                            version,
                            model,
                            value,
                            source,
                            f"{source}：{name}{suffix}",
                            f"HTML表{ti} / {name} / {model}{suffix}",
                            metric=metric,
                            unit=unit,
                            notes=note,
                            subset="子问题" if name == "ZEROBench_sub" else "overall",
                        )


DEEPSEEK = {
    "MMLU": "mmlu",
    "MMLU-Redux": "mmlu-redux",
    "MMLU-Pro": "mmlu-pro",
    "DROP": "drop",
    "IF-Eval": "ifeval",
    "GPQA-Diamond": "gpqa",
    "SimpleQA": "simpleqa",
    "FRAMES": "frames",
    "AlpacaEval2.0": "alpacaeval",
    "ArenaHard": "arena-hard",
    "LiveCodeBench": "livecodebench",
    "Codeforces": "codeforces",
    "SWE Verified": "swe-bench",
    "Aider-Polyglot": "aider-polyglot",
    "AIME 2024": "aime",
    "MATH-500": "math500",
    "CNMO 2024": "cnmo",
    "CLUEWSC": "cluewsc",
    "C-Eval": "c-eval",
    "C-SimpleQA": "c-simpleqa",
    "BBH": "bbh",
    "ARC-Easy": "arc-ai2",
    "ARC-Challenge": "arc-ai2",
    "HellaSwag": "hellaswag",
    "PIQA": "piqa",
    "WinoGrande": "winogrande",
    "RACE-Middle": "race",
    "RACE-High": "race",
    "TriviaQA": "triviaqa",
    "NaturalQuestions": "naturalquestions",
    "AGIEval": "agieval",
    "HumanEval": "humaneval",
    "MBPP": "mbpp",
    "CRUXEval-I": "cruxeval",
    "CRUXEval-O": "cruxeval",
    "GSM8K": "gsm8k",
    "MATH": "math",
    "MGSM": "mgsm",
    "CMMLU": "cmmlu",
}


def import_deepseek():
    for source, base in [("deepseek-r1", False), ("deepseek-v3", True)]:
        lines = (SOURCES / f"{source}.txt").read_text(encoding="utf-8").splitlines()
        # Locate the comparison table by its schema; README line numbers can change.
        begin = next(i for i, line in enumerate(lines) if "| Benchmark (Metric)" in line)
        end = next(
            (i for i in range(begin + 1, len(lines)) if not lines[i].startswith("|")),
            len(lines),
        )
        section = lines[begin:end]
        header = [s.strip().replace("**", "") for s in section[0].strip("|").split("|")]
        assert "Benchmark (Metric)" in header, source
        offset = 3 if base else 2
        models = header[offset:]
        for line in section[2:]:
            cells = [s.strip().replace("**", "") for s in line.strip("|").split("|")]
            label = cells[1]
            name = label.split(" (")[0]
            if name not in DEEPSEEK:
                continue
            metric = re.search(r"\((.*?)\)", label)[1]
            for model, value in zip(models, cells[offset:], strict=True):
                if not re.fullmatch(r"\d+(?:\.\d+)?", value):
                    continue
                model_name = model + "-Base" if base else model
                add(
                    DEEPSEEK[name],
                    f"{label} / {source}快照",
                    model_name,
                    value,
                    source,
                    f"{source}；{cells[2] if base else '主模型比较表'}；{label}",
                    f"{label} / {model}",
                    metric=metric,
                    unit="评级" if metric == "Rating" else "分" if "F1" in metric else "%",
                    notes="固定官方README快照。原表提示/采样协议见来源；Base与指令模型分开。厂商报告，未独立重跑。",
                )


def import_cl():
    table = html_tables("cl-paper")[2]
    for row in table[1:]:
        for col, subset in enumerate(
            ["overall", "领域知识推理", "规则系统应用", "程序化任务执行", "经验发现与模拟"], 1
        ):
            value = float(row[col].split()[0])
            add(
                "cl-bench",
                "arXiv:2602.03587v1",
                row[0],
                value,
                "cl-paper",
                "三次运行均值；推理模式；GPT-5.1裁判；每题全部rubric通过",
                f"Table 2 / {row[0]} / {table[0][col]}",
                subset=subset,
                metric="任务解决率",
                published="2026-02-03",
                source_type="paper",
                notes=f"源单元格：{row[col]}。均值±标准差；论文历史结果，不声称为最新SOTA。",
            )


def import_official():
    for i in (1, 2, 3):
        source = f"arc-v{i}"
        payload = json.loads((SOURCES / f"{source}.txt").read_text(encoding="utf-8"))
        rows = payload["evaluations"]
        for index, row in enumerate(rows):
            if row.get("providerId") == "Human" or not row.get("display"):
                continue
            human = next(
                (
                    x["score"] * 100
                    for x in rows
                    if x.get("providerId") == "Human" and x["datasetId"] == row["datasetId"]
                ),
                None,
            )
            protocol = row["datasetId"]
            if i == 3:
                protocol += "；厂商适配器" if "provider-adapter" in row["modelId"] else "；标准接口"
            add(
                "arc-agi-3" if i == 3 else "arc-agi",
                f"ARC-AGI-{i}",
                row["modelDisplayName"],
                row["score"] * 100,
                source,
                protocol,
                f"evaluations[{index}] / {row['modelId']}",
                human=human,
                source_type="official_benchmark",
                org=row["providerDisplayName"],
                unit="分" if i == 3 else "%",
                metric="行动效率得分" if i == 3 else "任务通过率",
                notes=(
                    "官方榜单采集快照；人类值为Human Panel，不代表普通人均值。"
                    f"榜单生成于{payload['generatedAt']}；"
                    f"预算信息：{row.get('costPerTask', row.get('cost', '未标注'))}"
                    "美元（按源字段定义）。模型发布日期未当作评测日期。"
                ),
            )
    text = (SOURCES / "swe-board.txt").read_text(encoding="utf-8")
    suites = json.loads(
        re.search(
            r'<script type="application/json" id="leaderboard-data">(.*?)</script>', text, re.S
        )[1]
    )
    for suite in suites:
        if suite["name"] not in ("Verified", "Lite", "Test", "Multilingual"):
            continue
        for row in suite["results"]:
            if (
                not row.get("checked")
                or row.get("warning")
                or row["date"] > MANIFEST["swe-board"]["observed_at"]
            ):
                continue
            add(
                "swe-multilingual" if suite["name"] == "Multilingual" else "swe-bench",
                suite["name"],
                row["name"],
                row["resolved"],
                "swe-board",
                f"官方榜单 {suite['name']}；系统含代理与模型",
                row["folder"],
                metric="问题解决率",
                source_type="official_benchmark",
                published=row["date"],
                org=row.get("model_org") or "来源未单独标注",
                notes="官方榜单checked=true且无warning记录；date保留为榜单记录日期，不是评测日期。系统脚手架与模型共同决定表现。",
            )
    for index, row in enumerate(
        csv.DictReader((SOURCES / "abstention-scores.txt").read_text(encoding="utf-8").splitlines())
    ):
        add(
            "abstentionbench",
            "官方结果CSV快照",
            row["model_name_formatted"],
            float(row["f1_score"]) * 100,
            "abstention-scores",
            f"{row['post_training_stage']}；{row['scenario_label']}",
            f"CSV数据行{index + 1}",
            subset=f"{row['scenario_label']} / {row['dataset_name_formatted']}",
            metric="弃答F1 ×100",
            unit="分",
            source_type="official_benchmark",
            notes="原CSV F1在0至1区间，乘100显示；F1不是答对率，未跨数据集求均值。",
        )


def import_mmsi():
    text = (SOURCES / "mmsi-readme.txt").read_text(encoding="utf-8")
    for line in text.splitlines():
        if not line.startswith("|"):
            continue
        cells = [re.sub(r"[*🥇🥈🥉]", "", c).strip() for c in line.strip("|").split("|")]
        if (
            len(cells) != 3
            or not re.fullmatch(r"\d+\.\d+", cells[1])
            or "Human" in cells[0]
            or "Random" in cells[0]
        ):
            continue
        add(
            "mmsi",
            "官方README榜单快照",
            cells[0],
            cells[1],
            "mmsi-readme",
            "MMSI-Bench官方榜单",
            cells[0],
            human=97.2,
            source_type="official_benchmark",
            notes=(
                "官方表格Human Level=97.2；模型与人类同表比较。"
                "未提供评测日期，不能据采集日推断模型新旧。"
            ),
        )


def import_audio_and_social():
    table = html_tables("qwen25-omni")[1]
    blocks = [
        (2, 14, "libri", ["dev-clean", "dev-other", "test-clean", "test-other"], "WER", "%"),
        (38, 47, "covost", ["en-de", "de-en", "en-zh", "zh-en"], "BLEU", "分"),
        (48, 54, "meld", ["overall"], "源表SER得分", "分"),
        (69, 73, "mmau", ["声音", "音乐", "语音", "overall"], "准确率", "%"),
    ]
    for start, end, key, subsets, metric, unit in blocks:
        for row in table[start:end]:
            model, raw = row[-2:]
            for subset, value in zip(subsets, raw.split("|"), strict=True):
                if value == "-":
                    continue
                add(
                    key,
                    "Qwen2.5-Omni官方比较表快照",
                    model,
                    value,
                    "qwen25-omni",
                    f"官方模型卡；{metric}",
                    f"音频表 / {key} / {model} / {subset}",
                    metric=metric,
                    unit=unit,
                    subset=subset,
                    notes="官方模型卡历史比较；WER越低越好，BLEU与SER原始得分不是任务通过率。",
                )
    table = html_tables("tom-paper")[1]
    task_names = [
        "意外结果",
        "标量含义",
        "说服故事",
        "错误信念",
        "歧义故事",
        "暗示理解",
        "奇怪故事",
        "失言识别",
        "overall",
    ]
    for row in table[4:]:
        if len(row) != 19:
            continue
        for ti, task in enumerate(task_names):
            for li, lang in enumerate(["中文", "英文"]):
                value = row[1 + ti * 2 + li]
                if not re.fullmatch(r"\d+(?:\.\d+)?", value):
                    continue
                add(
                    "tombench",
                    "arXiv:2402.15052v1",
                    row[0],
                    value,
                    "tom-paper",
                    f"论文任务视角；{lang}",
                    f"Table 2 / {row[0]} / {task} / {lang}",
                    subset=task,
                    source_type="paper",
                    published="2024-02-23",
                    notes="2024年论文历史结果；保留中英文与各任务区分；未将论文人类跨条件值直接补为各模型基线。",
                )


def import_robotics_safety_creation():
    protocol = ""
    for row in html_tables("oft-paper")[1]:
        if row[0].startswith("Policy inputs:"):
            protocol = row[0]
        if len(row) != 6 or not re.fullmatch(r"\d+\.\d+|–", row[1]):
            continue
        for subset, value in zip(
            ["Spatial", "Object", "Goal", "Long", "overall"], row[1:], strict=True
        ):
            if value == "–":
                continue
            add(
                "libero",
                "arXiv:2502.19645v1",
                row[0],
                value,
                "oft-paper",
                protocol,
                f"Table 1 / {row[0]} / {subset}",
                subset=subset,
                metric="四套件平均成功率" if subset == "overall" else "任务成功率",
                source_type="paper",
                notes="论文历史比较；仿真环境、任务微调后的策略；按输入传感器分组，不代表现实家庭泛化。",
            )
    subsets = [
        "提示有害性 / 对抗",
        "提示有害性 / 常规",
        "提示有害性 / 总体",
        "响应有害性 / 对抗",
        "响应有害性 / 常规",
        "响应有害性 / 总体",
        "拒绝识别 / 有害",
        "拒绝识别 / 对抗",
        "拒绝识别 / 常规",
        "拒绝识别 / 总体",
    ]
    for row in html_tables("wildguard-paper")[5][2:]:
        if row[0] == "Keyword-based":
            continue
        for subset, value in zip(subsets, row[1:], strict=True):
            if value == "-":
                continue
            add(
                "wildguard",
                "arXiv:2406.18495v1 / WildGuardTest",
                row[0],
                value,
                "wildguard-paper",
                "WildGuardTest；安全审核器分类",
                f"Table 4 / {row[0]} / {subset}",
                subset=subset,
                metric="F1 ×100",
                unit="分",
                source_type="paper",
                notes="2024年论文历史结果；衡量审核器识别能力，不是被测生成模型的安全通过率。",
            )
    for line in (SOURCES / "geneval.txt").read_text(encoding="utf-8").splitlines():
        if "|" not in line:
            continue
        cells = [c.strip().strip("*") for c in line.strip("|").split("|")]
        if len(cells) != 8 or not re.fullmatch(r"0\.\d+", cells[1]) or "baseline" in cells[0]:
            continue
        for subset, value in zip(
            ["overall", "单物体", "双物体", "计数", "颜色", "位置", "颜色归属"],
            cells[1:],
            strict=True,
        ):
            add(
                "gen-eval",
                "官方README原始模型表",
                cells[0],
                float(value) * 100,
                "geneval",
                "原始文生图组合评测",
                f"Results / {cells[0]} / {subset}",
                subset=subset,
                metric="任务宏平均 ×100" if subset == "overall" else "任务成功率",
                unit="分" if subset == "overall" else "%",
                source_type="official_benchmark",
                notes="原始历史模型表，非当前SOTA；源表0–1乘100展示，总体为六类任务宏平均。",
            )


# Epoch AI Benchmarking Hub（CC-BY 4.0）。只导入 Epoch 自己运行的内部评测；
# 压缩包中 *_external.csv 是 Epoch 汇总的第三方成绩，不作为独立评测导入。
# Epoch 基准名 → (基准ID, 子集, 指标, 协议摘要)；协议摘要转述自同日采集的方法页快照。
EPOCH = {
    "GPQA diamond": (
        "gpqa",
        "Diamond（198题）",
        "准确率",
        "simple-evals 提示，四选一，末行须为「ANSWER: 字母」否则该题记0分",
        "epoch-method-gpqa",
    ),
    "FrontierMath-2025-02-28-Private": (
        "frontiermath",
        "2025-02-28 私有集（已被 Tiers-1-3-v2 取代）",
        "准确率",
        "私有题集；模型可运行 Python 并通过 submit_answer 提交答案",
        "epoch-method-frontiermath",
    ),
    "FrontierMath-Tier-4-2025-07-01-Private": (
        "frontiermath",
        "Tier 4 2025-07-01 私有集（已被 Tier-4-v2 取代）",
        "准确率",
        "私有题集；模型可运行 Python 并通过 submit_answer 提交答案",
        "epoch-method-frontiermath",
    ),
    "FrontierMath-Tiers-1-3-v2-Private": (
        "frontiermath",
        "Tiers 1-3 v2 私有集",
        "准确率",
        "2026-06-12 修订版私有题集；模型可运行 Python 并通过 submit_answer 提交答案",
        "epoch-method-frontiermath",
    ),
    "FrontierMath-Tier-4-v2-Private": (
        "frontiermath",
        "Tier 4 v2 私有集",
        "准确率",
        "2026-06-12 修订版私有题集；模型可运行 Python 并通过 submit_answer 提交答案",
        "epoch-method-frontiermath",
    ),
    "MATH level 5": (
        "math",
        "Level 5（测试集1324题）",
        "准确率",
        "MATH 测试集难度5级题；要求末行以「ANSWER: 答案」作答",
        "epoch-method-math5",
    ),
    "SWE-Bench verified": (
        "swe-bench",
        "Verified（Epoch 可运行的484题）",
        "问题解决率",
        "排除16道无法稳定运行的题；默认简单循环脚手架，bash/text_editor/apply_patch 工具，"
        "无网络；2026年2月脚手架大幅升级",
        "epoch-method-swe",
    ),
    "SimpleQA Verified": (
        "simpleqa",
        "SimpleQA Verified（1000题）",
        "答对比例",
        "无选项问答，裁判模型判对/错/未尝试；报告答对比例而非 Google 官方 F1；"
        "2026-08-27 起追加防弃答提示并撤下此前成绩",
        "epoch-method-simpleqa",
    ),
}


def epoch_zip_csv(name):
    info = MANIFEST["epoch-benchmarks"]
    with zipfile.ZipFile(SOURCES / info["file"]) as archive:
        text = archive.read(name).decode("utf-8")
    return list(csv.DictReader(io.StringIO(text, newline="")))


def import_epoch():
    meta = {r["model_version"]: r for r in epoch_zip_csv("model_metadata.csv")}
    for bench in epoch_zip_csv("benchmark_metadata.csv"):
        name, file = bench["benchmark"], bench["source_file"]
        if not file or file.endswith("_external.csv") or name not in EPOCH:
            continue
        key, subset, metric, protocol, method = EPOCH[name]
        column = bench["score_column"]
        assert bench["scale"] == "1.0" and column == "Best score (across scorers)", name
        for row in epoch_zip_csv(file):
            version = row["Model version"]
            info = meta.get(version, {})
            label = info.get("display_name") or info.get("model_group") or version
            started = row["Started at"]
            note = (
                f"Epoch AI Benchmarking Hub 内部运行（CC-BY 4.0）；源字段「{column}」为0–1比例，"
                f"×100 以 % 显示；标准误 ±{float(row['stderr']) * 100:.2f} 个百分点。"
            )
            if row["mean_score"] != row[column]:
                note += f"同次运行 mean_score={row['mean_score']}（多评分器取最佳，未取均值）。"
            note += (
                "评测日期取 Started at 的 UTC 日期；"
                if started
                else "源数据未给出运行开始时间，评测日期留空；"
            )
            if row["Release date"]:
                note += f"模型发布日期 {row['Release date']}，未当作评测日期。"
            note += (
                f"随机基线 {float(bench['random_baseline']) * 100:g}%（源 benchmark_metadata）。"
            )
            note += f"协议依据 {method} 方法页快照，历史运行可能早于页面所述变更；未独立重跑。"
            add(
                key,
                f"Epoch Hub 快照 / {name}",
                f"{label} [{version}]",
                float(row[column]) * 100,
                "epoch-benchmarks",
                f"Epoch AI 内部评测；{protocol}；推理设置见模型版本后缀",
                f"benchmark_data.zip/{file} / id={row['id']} / {version}",
                subset=subset,
                metric=metric,
                source_type="independent_evaluation",
                org=row["Organization"] or None,
                evaluated=started[:10] or None,
                notes=note,
            )


def source_header(source, **extra):
    info = MANIFEST[source]
    return dict(
        source_id=source,
        source_url=info["url"],
        source_sha256=info["sha256"],
        observed_on=info["observed_at"],
        **extra,
    )


def epoch_model_dates():
    """按 Epoch 模型组汇总发布日期；同组版本日期不一致时不择一，置空并逐版本列出。"""
    groups = {}
    for row in epoch_zip_csv("model_metadata.csv"):
        if not row["model_group"]:
            continue
        group = groups.setdefault(row["model_group"], {"orgs": set(), "dates": {}, "versions": []})
        if row["organization"]:
            group["orgs"].add(row["organization"])
        if row["model_version"]:
            group["versions"].append(row["model_version"])
        if row["date"]:
            group["dates"].setdefault(row["date"], []).append(row["model_version"])
    models = []
    for name in sorted(groups):
        group = groups[name]
        entry = dict(
            name=name,
            organization=next(iter(group["orgs"])) if len(group["orgs"]) == 1 else None,
            release_date=next(iter(group["dates"])) if len(group["dates"]) == 1 else None,
            model_versions=sorted(set(group["versions"])),
        )
        if len(group["dates"]) > 1:
            entry["conflicting_release_dates"] = {
                day: sorted(v or "（无版本ID）" for v in versions)
                for day, versions in sorted(group["dates"].items())
            }
        models.append(entry)
    return source_header(
        "epoch-benchmarks",
        source_file="benchmark_data.zip/model_metadata.csv",
        license="CC-BY 4.0（压缩包 README）",
        notes=(
            "name 为 Epoch 的 model_group；release_date 为模型发布日期，不是评测日期；"
            "源表未给出日期或同组版本日期不一致时为 null，"
            "后者在 conflicting_release_dates 逐条保留。"
        ),
        models=models,
    )


def epoch_eci():
    text = (SOURCES / "epoch-eci.txt").read_text(encoding="utf-8")
    models = []
    for row in csv.DictReader(io.StringIO(text, newline="")):
        entry = dict(
            name=row["Model"],
            organization=row["Organization"] or None,
            country=row["Country (of organization)"] or None,
            release_date=row["date"] or None,
            eci=float(row["eci"]),
            eci_ci_low=float(row["eci_ci_low"]) if row["eci_ci_low"] else None,
            eci_ci_high=float(row["eci_ci_high"]) if row["eci_ci_high"] else None,
            model_accessibility=row["Model accessibility"] or None,
            accessibility_group=row["Accessibility group"] or None,
        )
        if row["Display name"] != row["Model"]:
            entry["display_name"] = row["Display name"]
        if row["model_versions"]:
            entry["model_versions"] = row["model_versions"]
        models.append(entry)
    return source_header(
        "epoch-eci",
        method_source=MANIFEST["epoch-eci-page"]["url"],
        method_source_sha256=MANIFEST["epoch-eci-page"]["sha256"],
        license="CC-BY 4.0",
        notes=(
            "ECI（Epoch Capabilities Index）是 Epoch AI 以项目反应理论（IRT）类方法、"
            "从多个基准成绩联合拟合的相对能力指数；刻度任意，标定为 Claude 3.5 Sonnet=130、"
            "GPT-5=150，无上限，与基准准确率非线性，只适合模型间比较，不是 AGI 完成百分比。"
            "eci_ci_low/eci_ci_high 为源 CSV 的区间上下界，CSV 未标注置信水平；"
            "release_date 为模型发布日期。"
        ),
        models=models,
    )


EPOCH_TABLES = {
    "epoch-model-dates.yaml": epoch_model_dates,
    "epoch-eci.yaml": epoch_eci,
}


def metr_horizons():
    """Retain METR's published horizon data without treating it as an AGI score."""
    info = MANIFEST["metr-horizons"]
    return dict(
        source_url=info["url"],
        methodology_url="https://metr.org/time-horizons/",
        observed_on=info["observed_at"],
        unit="minutes",
        sha256=info["sha256"],
        notice="Model release dates are not evaluation dates; horizons do not enter Depth.",
        data=yaml.safe_load((SOURCES / "metr-horizons.txt").read_text(encoding="utf-8")),
    )


def dump(payload):
    return yaml.safe_dump(payload, allow_unicode=True, sort_keys=False)


def main():
    import_qwen()
    import_deepseek()
    import_cl()
    import_official()
    import_mmsi()
    import_audio_and_social()
    import_robotics_safety_creation()
    import_epoch()
    # 完全重复的源记录只保留一次，不同来源或协议不去重合并。
    unique = {json.dumps(s, sort_keys=True, ensure_ascii=False): s for s in SCORES}
    records = sorted(
        unique.values(),
        key=lambda s: (
            s["benchmark_id"],
            s["benchmark_version"],
            s["protocol"],
            s["subset"],
            s["model"],
        ),
    )
    path = ROOT / "data/scores/frontier_scores.yaml"
    path.write_text(dump(records), encoding="utf-8")
    for name, build in EPOCH_TABLES.items():
        payload = build()
        (ROOT / "data/research" / name).write_text(dump(payload), encoding="utf-8")
        print(f"{name}：{len(payload['models'])} 个模型")
    (ROOT / "data/research/metr-horizon-v1.1.yaml").write_text(
        dump(metr_horizons()), encoding="utf-8"
    )
    print(f"成绩 {len(records)}；有成绩基准 {len({s['benchmark_id'] for s in records})}")


if __name__ == "__main__":
    main()
