# AGI Atlas · 离 AGI 还差多少？

[English](report.en.md) · 数据快照 2026-10-05 · 本报告由 `uv run agi-atlas report` 生成，请勿手改。

O*NET 职业活动、OpenAlex 科研主题与独立能力标签共同组织评测证据；学科未测项保持未知。

分类版本：2026-09-23 · 分类抓取：2026-10-05 · 评测来源最近抓取：2026-10-05。原始更新时间可在主题中查看。

## 结论

| 分母 | 规模 | 有基准测量 | 已测部分得分 | **AI 已达到** |
| --- | --- | ---: | ---: | ---: |
| 职业：O*NET 31.0 工作活动 | 923 职业 · 2087 工作活动 | 7.01% | 42.4% | **0.91%** |
| 学科：OpenAlex 科研主题 | 4516 个 OpenAlex 主题 | 0.04% (主题级映射 0.04%) | — | **—** |

## 按职业大类

| 职业大类 | 数量 | AI 已达到 | 有基准测量 |
| --- | ---: | ---: | ---: |
| 计算机与数学 | 36 | 7.6% | 22.47% |
| 办公与行政支持 | 51 | 3.57% | 19.47% |
| 法律 | 7 | 2.96% | 23.33% |
| 医疗从业者与技术人员 | 89 | 1.77% | 10.43% |
| 建筑与工程 | 56 | 1.18% | 4.11% |
| 商业与金融运营 | 48 | 0.89% | 10.17% |
| 销售 | 22 | 0.61% | 12.41% |
| 艺术、设计、娱乐、体育与媒体 | 40 | 0.58% | 13.22% |
| 生命、物理与社会科学 | 60 | 0.31% | 7.29% |
| 个人护理与服务 | 31 | 0.28% | 9.18% |
| 教育与图书馆 | 62 | 0.27% | 5.89% |
| 保护服务 | 26 | 0.13% | 1.81% |
| 餐饮服务 | 16 | 0.11% | 4.42% |
| 管理 | 56 | 0.09% | 4.4% |
| 社区与社会服务 | 14 | 0.08% | 2.7% |
| 农业、渔业与林业 | 12 | 0.05% | 0.22% |
| 生产 | 107 | 0.05% | 1.15% |
| 医疗辅助 | 19 | 0.03% | 7.21% |
| 楼宇与场地清洁维护 | 8 | 0% | 0.69% |
| 建筑施工与采掘 | 61 | 0% | 0.41% |
| 安装、维护与维修 | 50 | 0% | 1.96% |
| 运输与物料搬运 | 52 | 0% | 3.35% |

## 按 OpenAlex 学科的证据覆盖

| OpenAlex 学科 | OpenAlex topics | Benchmarks |
| --- | ---: | ---: |
| 农业与生物科学 | 235 | 13 |
| 艺术与人文 | 266 | 15 |
| 生物化学、遗传学与分子生物学 | 248 | 4 |
| 商业、管理与会计 | 146 | 13 |
| 化学工程 | 13 | 0 |
| 化学 | 101 | 14 |
| 计算机科学 | 302 | 31 |
| 决策科学 | 60 | 0 |
| 地球与行星科学 | 57 | 1 |
| 经济学、计量经济学与金融 | 107 | 12 |
| 能源 | 27 | 0 |
| 工程 | 560 | 11 |
| 环境科学 | 202 | 0 |
| 免疫学与微生物学 | 44 | 0 |
| 材料科学 | 123 | 1 |
| 数学 | 82 | 24 |
| 医学 | 692 | 17 |
| 神经科学 | 62 | 0 |
| 护理 | 21 | 0 |
| 药理学、毒理学与药剂学 | 25 | 0 |
| 物理学与天文学 | 104 | 13 |
| 心理学 | 144 | 15 |
| 社会科学 | 764 | 13 |
| 兽医学 | 11 | 0 |
| 牙科学 | 13 | 0 |
| 健康职业 | 107 | 0 |

## 各基准最好成绩

| 基准 | 能力域 | 口径 | 最好成绩 | 模型 | 阶段 | 来源 |
| --- | --- | --- | ---: | --- | --- | --- |
| MMLU | 知识与专业判断 | MMLU (Pass@1) / deepseek-r1快照 | 91.8 % | OpenAI o1-1217 | 接近满分 | [厂商报告](<https://raw.githubusercontent.com/deepseek-ai/DeepSeek-R1/main/README.md>) |
| MMLU-Redux | 知识与专业判断 | MMLU-Redux / qwen35-card快照 | 95.9 % | Gemini-3 Pro | 接近满分 | [厂商报告](<https://huggingface.co/Qwen/Qwen3.5-397B-A17B/raw/main/README.md>) |
| MMLU-Pro | 知识与专业判断 | MMLU-Pro / qwen35-card快照 | 89.8 % | Gemini-3 Pro | 进行中 | [厂商报告](<https://huggingface.co/Qwen/Qwen3.5-397B-A17B/raw/main/README.md>) |
| SuperGPQA | 知识与专业判断 | SuperGPQA / qwen35-card快照 | 74 % | Gemini-3 Pro | 进行中 | [厂商报告](<https://huggingface.co/Qwen/Qwen3.5-397B-A17B/raw/main/README.md>) |
| C-Eval | 知识与专业判断 | C-Eval / qwen35-card快照 | 94 % | K2.5-1T-A32B | 接近满分 | [厂商报告](<https://huggingface.co/Qwen/Qwen3.5-397B-A17B/raw/main/README.md>) |
| CMMLU | 知识与专业判断 | CMMLU (Acc.) / deepseek-v3快照 | 89.5 % | Qwen2.5 72B-Base | 进行中 | [厂商报告](<https://raw.githubusercontent.com/deepseek-ai/DeepSeek-V3/main/README.md>) |
| AGIEval | 知识与专业判断 | AGIEval (Acc.) / deepseek-v3快照 | 79.6 % | DeepSeek-V3-Base | 进行中 | [厂商报告](<https://raw.githubusercontent.com/deepseek-ai/DeepSeek-V3/main/README.md>) |
| GPQA | 科学与研究 | GPQA / qwen35-card快照 | 92.4 % | GPT5.2 | 接近满分 | [厂商报告](<https://huggingface.co/Qwen/Qwen3.5-397B-A17B/raw/main/README.md>) |
| Humanity's Last Exam | 科学与研究 | HLE / qwen35-card快照 | 37.5 % | Gemini-3 Pro | 差距明显 | [厂商报告](<https://huggingface.co/Qwen/Qwen3.5-397B-A17B/raw/main/README.md>) |
| FrontierMath | 数学 | Epoch Hub 快照 / FrontierMath-Tiers-1-3-v2-Private | 93.68 % | GPT-6.1 Sol (max) [gpt-6.1-sol_max] | 接近满分 | [独立评测](<https://epoch.ai/data/benchmark_data.zip>) |
| SciCode | 科学与研究 | — | — | — | 暂无成绩 | [原始任务 ↗](<https://scicode-bench.github.io/>) |
| PaperBench | 科学与研究 | PaperBench / qwen38-card快照 | 93 分 | Qwen3.8-Max | 无上限量尺 | [厂商报告](<https://huggingface.co/Qwen/Qwen3.8-2.4T-A95B/raw/main/README.md>) |
| ScienceAgentBench | 科学与研究 | — | — | — | 暂无成绩 | [原始任务 ↗](<https://github.com/OSU-NLP-Group/ScienceAgentBench>) |
| SWE-bench | 软件工程 | Verified | 77.4 % | live-SWE-agent + Gemini 3 Pro Preview (2025-11-18) | 进行中 | [官方榜单](<https://www.swebench.com/>) |
| SWE-bench Pro | 软件工程 | SWE-bench Pro / qwen38-card快照 | 80 % | Fable 5 | 进行中 | [厂商报告](<https://huggingface.co/Qwen/Qwen3.8-2.4T-A95B/raw/main/README.md>) |
| SWE-bench Multilingual | 软件工程 | Multilingual | 72.7 % | Gemini 3 Flash | 进行中 | [官方榜单](<https://www.swebench.com/>) |
| NL2Repo-Bench | 软件工程 | NL2Repo-Bench / qwen38-card快照 | 69.4 % | Opus 4.8 | 进行中 | [厂商报告](<https://huggingface.co/Qwen/Qwen3.8-2.4T-A95B/raw/main/README.md>) |
| LiveCodeBench | 软件工程 | LiveCodeBench v6 / qwen35-card快照 | 90.7 % | Gemini-3 Pro | 接近满分 | [厂商报告](<https://huggingface.co/Qwen/Qwen3.5-397B-A17B/raw/main/README.md>) |
| HumanEval | 软件工程 | HumanEval (Pass@1) / deepseek-v3快照 | 65.2 % | DeepSeek-V3-Base | 进行中 | [厂商报告](<https://raw.githubusercontent.com/deepseek-ai/DeepSeek-V3/main/README.md>) |
| MBPP | 软件工程 | MBPP (Pass@1) / deepseek-v3快照 | 75.4 % | DeepSeek-V3-Base | 进行中 | [厂商报告](<https://raw.githubusercontent.com/deepseek-ai/DeepSeek-V3/main/README.md>) |
| EvalPlus | 软件工程 | — | — | — | 暂无成绩 | [原始任务 ↗](<https://github.com/evalplus/evalplus>) |
| BigCodeBench | 软件工程 | — | — | — | 暂无成绩 | [原始任务 ↗](<https://bigcode-bench.github.io/>) |
| CRUXEval | 软件工程 | CRUXEval-I (Acc.) / deepseek-v3快照 | 67.3 % | DeepSeek-V3-Base | 进行中 | [厂商报告](<https://raw.githubusercontent.com/deepseek-ai/DeepSeek-V3/main/README.md>) |
| Aider Polyglot | 软件工程 | Aider-Polyglot (Acc.) / deepseek-r1快照 | 61.7 % | OpenAI o1-1217 | 进行中 | [厂商报告](<https://raw.githubusercontent.com/deepseek-ai/DeepSeek-R1/main/README.md>) |
| Codeforces | 软件工程 | Codeforces (Percentile) / deepseek-r1快照 | 96.6 % | OpenAI o1-1217 | 接近满分 | [厂商报告](<https://raw.githubusercontent.com/deepseek-ai/DeepSeek-R1/main/README.md>) |
| SecCodeBench | 软件工程 | SecCodeBench / qwen35-card快照 | 68.7 分 | GPT5.2 | 无上限量尺 | [厂商报告](<https://huggingface.co/Qwen/Qwen3.5-397B-A17B/raw/main/README.md>) |
| DS-1000 | 软件工程 | — | — | — | 暂无成绩 | [原始任务 ↗](<https://ds1000-code-gen.github.io/>) |
| Spider | 软件工程 | — | — | — | 暂无成绩 | [原始任务 ↗](<https://yale-lily.github.io/spider>) |
| BIRD | 软件工程 | — | — | — | 暂无成绩 | [原始任务 ↗](<https://bird-bench.github.io/>) |
| GSM8K | 数学 | GSM8K (EM) / deepseek-v3快照 | 89.3 % | DeepSeek-V3-Base | 进行中 | [厂商报告](<https://raw.githubusercontent.com/deepseek-ai/DeepSeek-V3/main/README.md>) |
| MATH | 数学 | MATH (EM) / deepseek-v3快照 | 61.6 % | DeepSeek-V3-Base | 进行中 | [厂商报告](<https://raw.githubusercontent.com/deepseek-ai/DeepSeek-V3/main/README.md>) |
| MATH-500 | 数学 | MATH-500 (Pass@1) / deepseek-r1快照 | 97.3 % | DeepSeek R1 | 接近满分 | [厂商报告](<https://raw.githubusercontent.com/deepseek-ai/DeepSeek-R1/main/README.md>) |
| AIME | 数学 | AIME 2024 (Pass@1) / deepseek-r1快照 | 79.8 % | DeepSeek R1 | 进行中 | [厂商报告](<https://raw.githubusercontent.com/deepseek-ai/DeepSeek-R1/main/README.md>) |
| CNMO | 数学 | CNMO 2024 (Pass@1) / deepseek-r1快照 | 78.8 % | DeepSeek R1 | 进行中 | [厂商报告](<https://raw.githubusercontent.com/deepseek-ai/DeepSeek-R1/main/README.md>) |
| HMMT | 数学 | HMMT Feb 25 / qwen35-card快照 | 99.4 % | GPT5.2 | 接近满分 | [厂商报告](<https://huggingface.co/Qwen/Qwen3.5-397B-A17B/raw/main/README.md>) |
| Omni-MATH | 数学 | — | — | — | 暂无成绩 | [原始任务 ↗](<https://omni-math.github.io/>) |
| IMO-AnswerBench | 数学 | IMOAnswerBench / qwen35-card快照 | 86.3 % | GPT5.2 | 进行中 | [厂商报告](<https://huggingface.co/Qwen/Qwen3.5-397B-A17B/raw/main/README.md>) |
| miniF2F | 数学 | — | — | — | 暂无成绩 | [原始任务 ↗](<https://github.com/openai/miniF2F>) |
| ProofNet | 数学 | — | — | — | 暂无成绩 | [原始任务 ↗](<https://github.com/zhangir-azerbayev/ProofNet>) |
| MathVista | 视觉与空间 | Mathvista(mini) / qwen35-card快照 | 90.3 % | Qwen3.5-397B-A17B | 接近满分 | [厂商报告](<https://huggingface.co/Qwen/Qwen3.5-397B-A17B/raw/main/README.md>) |
| MATH-Vision | 视觉与空间 | MathVision / qwen35-card快照 | 88.6 % | Qwen3.5-397B-A17B | 进行中 | [厂商报告](<https://huggingface.co/Qwen/Qwen3.5-397B-A17B/raw/main/README.md>) |
| We-Math | 视觉与空间 | We-Math / qwen35-card快照 | 87.9 分 | Qwen3.5-397B-A17B | 无上限量尺 | [厂商报告](<https://huggingface.co/Qwen/Qwen3.5-397B-A17B/raw/main/README.md>) |
| DynaMath | 视觉与空间 | DynaMath / qwen35-card快照 | 86.8 分 | GPT5.2 | 无上限量尺 | [厂商报告](<https://huggingface.co/Qwen/Qwen3.5-397B-A17B/raw/main/README.md>) |
| BIG-Bench Hard | 推理与问题求解 | BBH (EM) / deepseek-v3快照 | 87.5 % | DeepSeek-V3-Base | 进行中 | [厂商报告](<https://raw.githubusercontent.com/deepseek-ai/DeepSeek-V3/main/README.md>) |
| AI2 ARC | 推理与问题求解 | ARC-Challenge (Acc.) / deepseek-v3快照 | 95.3 % | LLaMA3.1 405B-Base | 接近满分 | [厂商报告](<https://raw.githubusercontent.com/deepseek-ai/DeepSeek-V3/main/README.md>) |
| HellaSwag | 推理与问题求解 | HellaSwag (Acc.) / deepseek-v3快照 | 89.2 % | LLaMA3.1 405B-Base | 进行中 | [厂商报告](<https://raw.githubusercontent.com/deepseek-ai/DeepSeek-V3/main/README.md>) |
| PIQA | 推理与问题求解 | PIQA (Acc.) / deepseek-v3快照 | 85.9 % | LLaMA3.1 405B-Base | 进行中 | [厂商报告](<https://raw.githubusercontent.com/deepseek-ai/DeepSeek-V3/main/README.md>) |
| WinoGrande | 语言与沟通 | WinoGrande (Acc.) / deepseek-v3快照 | 86.3 % | DeepSeek-V2-Base | 进行中 | [厂商报告](<https://raw.githubusercontent.com/deepseek-ai/DeepSeek-V3/main/README.md>) |
| CLUEWSC | 语言与沟通 | CLUEWSC (EM) / deepseek-r1快照 | 92.8 % | DeepSeek R1 | 接近满分 | [厂商报告](<https://raw.githubusercontent.com/deepseek-ai/DeepSeek-R1/main/README.md>) |
| LogiQA | 推理与问题求解 | — | — | — | 暂无成绩 | [原始任务 ↗](<https://github.com/lgw863/LogiQA-dataset>) |
| FOLIO | 推理与问题求解 | — | — | — | 暂无成绩 | [原始任务 ↗](<https://github.com/Yale-LILY/FOLIO>) |
| ARC-AGI | 学习与泛化 | ARC-AGI-2 | 95 % | GPT-6 Astra (Max) | 接近满分 | [官方榜单](<https://arcprize.org/media/data/leaderboard/v2.json>) |
| ARC-AGI-3 | 学习与泛化 | ARC-AGI-3 | 62.71 分 | GPT-6 Astra (Max) | 无上限量尺 | [官方榜单](<https://arcprize.org/media/data/leaderboard/v3.json>) |
| CL-bench | 学习与泛化 | arXiv:2602.03587v1 | 23.7 % | GPT 5.1 (High) | 差距明显 | [论文](<https://arxiv.org/html/2602.03587v1>) |
| CL-bench Life | 学习与泛化 | — | — | — | 暂无成绩 | [原始任务 ↗](<https://github.com/Tencent-Hunyuan/CL-bench>) |
| CHORES | 具身与运动 | — | — | — | 暂无成绩 | [原始任务 ↗](<https://arxiv.org/abs/2312.02976>) |
| LongMemEval | 记忆与长上下文 | — | — | — | 暂无成绩 | [原始任务 ↗](<https://github.com/xiaowu0162/LongMemEval>) |
| LongMemEval-V2 | 记忆与长上下文 | — | — | — | 暂无成绩 | [原始任务 ↗](<https://github.com/xiaowu0162/LongMemEval-V2>) |
| LoCoMo | 记忆与长上下文 | — | — | — | 暂无成绩 | [原始任务 ↗](<https://snap-research.github.io/locomo/>) |
| LongBench | 记忆与长上下文 | — | — | — | 暂无成绩 | [原始任务 ↗](<https://github.com/THUDM/LongBench>) |
| LongBench v2 | 记忆与长上下文 | LongBench v2 / qwen35-card快照 | 68.2 分 | Gemini-3 Pro | 无上限量尺 | [厂商报告](<https://huggingface.co/Qwen/Qwen3.5-397B-A17B/raw/main/README.md>) |
| AA-LCR | 记忆与长上下文 | AA-LCR / qwen35-card快照 | 74 分 | Claude 4.5 Opus | 无上限量尺 | [厂商报告](<https://huggingface.co/Qwen/Qwen3.5-397B-A17B/raw/main/README.md>) |
| RULER | 记忆与长上下文 | — | — | — | 暂无成绩 | [原始任务 ↗](<https://github.com/NVIDIA/RULER>) |
| MRCR | 记忆与长上下文 | MRCR v2 256K (8-needle) / qwen38-card快照 | 93.8 分 | GPT 5.6 Sol (max) | 无上限量尺 | [厂商报告](<https://huggingface.co/Qwen/Qwen3.8-2.4T-A95B/raw/main/README.md>) |
| FRAMES | 记忆与长上下文 | FRAMES (Acc.) / deepseek-r1快照 | 82.5 % | DeepSeek R1 | 进行中 | [厂商报告](<https://raw.githubusercontent.com/deepseek-ai/DeepSeek-R1/main/README.md>) |
| HotpotQA | 记忆与长上下文 | — | — | — | 暂无成绩 | [原始任务 ↗](<https://hotpotqa.github.io/>) |
| MuSiQue | 记忆与长上下文 | — | — | — | 暂无成绩 | [原始任务 ↗](<https://github.com/StonyBrookNLP/musique>) |
| SimpleQA | 可靠性与自我监控 | SimpleQA (Correct) / deepseek-r1快照 | 47 % | OpenAI o1-1217 | 差距明显 | [厂商报告](<https://raw.githubusercontent.com/deepseek-ai/DeepSeek-R1/main/README.md>) |
| Chinese SimpleQA | 可靠性与自我监控 | C-SimpleQA (Correct) / deepseek-r1快照 | 68 % | DeepSeek V3 | 进行中 | [厂商报告](<https://raw.githubusercontent.com/deepseek-ai/DeepSeek-R1/main/README.md>) |
| TruthfulQA | 可靠性与自我监控 | — | — | — | 暂无成绩 | [原始任务 ↗](<https://github.com/sylinrl/TruthfulQA>) |
| AbstentionBench | 可靠性与自我监控 | 官方结果CSV快照 | 97.73 分 | o1LowReasoningAPI | 无上限量尺 | [官方榜单](<https://raw.githubusercontent.com/facebookresearch/AbstentionBench/main/analysis/abstention_performance.csv>) |
| HallusionBench | 可靠性与自我监控 | HallusionBench / qwen35-card快照 | 71.4 分 | Qwen3.5-397B-A17B | 无上限量尺 | [厂商报告](<https://huggingface.co/Qwen/Qwen3.5-397B-A17B/raw/main/README.md>) |
| POPE | 可靠性与自我监控 | — | — | — | 暂无成绩 | [原始任务 ↗](<https://github.com/AoiDragon/POPE>) |
| SimpleVQA | 可靠性与自我监控 | SimpleVQA / qwen35-card快照 | 73.2 % | Gemini-3 Pro | 进行中 | [厂商报告](<https://huggingface.co/Qwen/Qwen3.5-397B-A17B/raw/main/README.md>) |
| IFEval | 语言与沟通 | IFEval / qwen35-card快照 | 94.8 % | GPT5.2 | 接近满分 | [厂商报告](<https://huggingface.co/Qwen/Qwen3.5-397B-A17B/raw/main/README.md>) |
| IFBench | 语言与沟通 | IFBench / qwen35-card快照 | 76.5 % | Qwen3.5-397B-A17B | 进行中 | [厂商报告](<https://huggingface.co/Qwen/Qwen3.5-397B-A17B/raw/main/README.md>) |
| MultiChallenge | 语言与沟通 | MultiChallenge / qwen35-card快照 | 67.6 分 | Qwen3.5-397B-A17B | 无上限量尺 | [厂商报告](<https://huggingface.co/Qwen/Qwen3.5-397B-A17B/raw/main/README.md>) |
| DROP | 语言与沟通 | DROP (3-shot F1) / deepseek-r1快照 | 92.2 分 | DeepSeek R1 | 无上限量尺 | [厂商报告](<https://raw.githubusercontent.com/deepseek-ai/DeepSeek-R1/main/README.md>) |
| RACE | 语言与沟通 | RACE-High (Acc.) / deepseek-v3快照 | 56.8 % | LLaMA3.1 405B-Base | 进行中 | [厂商报告](<https://raw.githubusercontent.com/deepseek-ai/DeepSeek-V3/main/README.md>) |
| TriviaQA | 知识与专业判断 | TriviaQA (EM) / deepseek-v3快照 | 82.9 % | DeepSeek-V3-Base | 进行中 | [厂商报告](<https://raw.githubusercontent.com/deepseek-ai/DeepSeek-V3/main/README.md>) |
| Natural Questions | 知识与专业判断 | NaturalQuestions (EM) / deepseek-v3快照 | 41.5 % | LLaMA3.1 405B-Base | 差距明显 | [厂商报告](<https://raw.githubusercontent.com/deepseek-ai/DeepSeek-V3/main/README.md>) |
| WildBench | 语言与沟通 | — | — | — | 暂无成绩 | [原始任务 ↗](<https://github.com/allenai/WildBench>) |
| AlpacaEval | 语言与沟通 | AlpacaEval2.0 (LC-winrate) / deepseek-r1快照 | 87.6 % | DeepSeek R1 | 进行中 | [厂商报告](<https://raw.githubusercontent.com/deepseek-ai/DeepSeek-R1/main/README.md>) |
| Arena-Hard | 语言与沟通 | ArenaHard (GPT-4-1106) / deepseek-r1快照 | 92.3 % | DeepSeek R1 | 接近满分 | [厂商报告](<https://raw.githubusercontent.com/deepseek-ai/DeepSeek-R1/main/README.md>) |
| MT-Bench | 语言与沟通 | — | — | — | 暂无成绩 | [原始任务 ↗](<https://github.com/lm-sys/FastChat>) |
| MMMLU | 多语言与文化 | MMMLU / qwen35-card快照 | 90.6 % | Gemini-3 Pro | 接近满分 | [厂商报告](<https://huggingface.co/Qwen/Qwen3.5-397B-A17B/raw/main/README.md>) |
| MMLU-ProX | 多语言与文化 | MMLU-ProX / qwen35-card快照 | 87.7 % | Gemini-3 Pro | 进行中 | [厂商报告](<https://huggingface.co/Qwen/Qwen3.5-397B-A17B/raw/main/README.md>) |
| INCLUDE | 多语言与文化 | INCLUDE / qwen35-card快照 | 90.5 % | Gemini-3 Pro | 接近满分 | [厂商报告](<https://huggingface.co/Qwen/Qwen3.5-397B-A17B/raw/main/README.md>) |
| Global PIQA | 多语言与文化 | Global PIQA / qwen35-card快照 | 93.2 % | Gemini-3 Pro | 接近满分 | [厂商报告](<https://huggingface.co/Qwen/Qwen3.5-397B-A17B/raw/main/README.md>) |
| PolyMATH | 多语言与文化 | PolyMATH / qwen35-card快照 | 81.6 % | Gemini-3 Pro | 进行中 | [厂商报告](<https://huggingface.co/Qwen/Qwen3.5-397B-A17B/raw/main/README.md>) |
| MGSM | 多语言与文化 | MGSM (EM) / deepseek-v3快照 | 79.8 % | DeepSeek-V3-Base | 进行中 | [厂商报告](<https://raw.githubusercontent.com/deepseek-ai/DeepSeek-V3/main/README.md>) |
| FLORES-200 | 多语言与文化 | — | — | — | 暂无成绩 | [原始任务 ↗](<https://github.com/facebookresearch/flores>) |
| WMT24++ | 多语言与文化 | — | — | — | 暂无成绩 | [原始任务 ↗](<https://github.com/google-research/mt-metrics-eval>) |
| MMMU | 视觉与空间 | MMMU / qwen35-card快照 | 87.2 % | Gemini-3 Pro | 进行中 | [厂商报告](<https://huggingface.co/Qwen/Qwen3.5-397B-A17B/raw/main/README.md>) |
| MMMU-Pro | 视觉与空间 | MMMU-Pro / qwen35-card快照 | 81 % | Gemini-3 Pro | 进行中 | [厂商报告](<https://huggingface.co/Qwen/Qwen3.5-397B-A17B/raw/main/README.md>) |
| MMBench | 视觉与空间 | MMBenchEN-DEV-v1.1 / qwen35-card快照 | 94.2 % | K2.5-1T-A32B | 接近满分 | [厂商报告](<https://huggingface.co/Qwen/Qwen3.5-397B-A17B/raw/main/README.md>) |
| MMStar | 视觉与空间 | MMStar / qwen35-card快照 | 83.8 % | Qwen3.5-397B-A17B | 进行中 | [厂商报告](<https://huggingface.co/Qwen/Qwen3.5-397B-A17B/raw/main/README.md>) |
| RealWorldQA | 视觉与空间 | RealWorldQA / qwen35-card快照 | 83.9 % | Qwen3.5-397B-A17B | 进行中 | [厂商报告](<https://huggingface.co/Qwen/Qwen3.5-397B-A17B/raw/main/README.md>) |
| ZeroBench | 视觉与空间 | ZEROBench / qwen35-card快照 | 12 分 | Qwen3.5-397B-A17B | 无上限量尺 | [厂商报告](<https://huggingface.co/Qwen/Qwen3.5-397B-A17B/raw/main/README.md>) |
| BabyVision | 视觉与空间 | BabyVision / qwen35-card快照 | 49.7 分 | Gemini-3 Pro | 无上限量尺 | [厂商报告](<https://huggingface.co/Qwen/Qwen3.5-397B-A17B/raw/main/README.md>) |
| ChartQA | 视觉与空间 | — | — | — | 暂无成绩 | [原始任务 ↗](<https://github.com/vis-nlp/ChartQA>) |
| CharXiv | 视觉与空间 | CharXiv(RQ) / qwen35-card快照 | 82.1 分 | GPT5.2 | 无上限量尺 | [厂商报告](<https://huggingface.co/Qwen/Qwen3.5-397B-A17B/raw/main/README.md>) |
| DocVQA | 视觉与空间 | — | — | — | 暂无成绩 | [原始任务 ↗](<https://www.docvqa.org/>) |
| InfographicVQA | 视觉与空间 | — | — | — | 暂无成绩 | [原始任务 ↗](<https://www.docvqa.org/datasets/infographicvqa>) |
| OCRBench | 视觉与空间 | OCRBench / qwen35-card快照 | 93.1 分 | Qwen3.5-397B-A17B | 无上限量尺 | [厂商报告](<https://huggingface.co/Qwen/Qwen3.5-397B-A17B/raw/main/README.md>) |
| CC-OCR | 视觉与空间 | CC-OCR / qwen35-card快照 | 82 分 | Qwen3.5-397B-A17B | 无上限量尺 | [厂商报告](<https://huggingface.co/Qwen/Qwen3.5-397B-A17B/raw/main/README.md>) |
| OmniDocBench | 视觉与空间 | OmniDocBench1.5 / qwen35-card快照 | 90.8 分 | Qwen3.5-397B-A17B | 无上限量尺 | [厂商报告](<https://huggingface.co/Qwen/Qwen3.5-397B-A17B/raw/main/README.md>) |
| MMLongBench-Doc | 视觉与空间 | MMLongBench-Doc / qwen35-card快照 | 61.9 分 | Claude 4.5 Opus | 无上限量尺 | [厂商报告](<https://huggingface.co/Qwen/Qwen3.5-397B-A17B/raw/main/README.md>) |
| AI2D | 视觉与空间 | AI2D_TEST / qwen35-card快照 | 94.1 % | Gemini-3 Pro | 接近满分 | [厂商报告](<https://huggingface.co/Qwen/Qwen3.5-397B-A17B/raw/main/README.md>) |
| CountBench (CountBenchQA) | 视觉与空间 | CountBench / qwen35-card快照 | 97.3 % | Gemini-3 Pro | 接近满分 | [厂商报告](<https://huggingface.co/Qwen/Qwen3.5-397B-A17B/raw/main/README.md>) |
| RefCOCO | 视觉与空间 | RefCOCO(avg) / qwen35-card快照 | 92.3 分 | Qwen3.5-397B-A17B | 无上限量尺 | [厂商报告](<https://huggingface.co/Qwen/Qwen3.5-397B-A17B/raw/main/README.md>) |
| ODinW | 视觉与空间 | ODInW13 / qwen35-card快照 | 47 分 | Qwen3.5-397B-A17B | 无上限量尺 | [厂商报告](<https://huggingface.co/Qwen/Qwen3.5-397B-A17B/raw/main/README.md>) |
| EmbSpatialBench | 视觉与空间 | EmbSpatialBench / qwen35-card快照 | 84.5 分 | Qwen3.5-397B-A17B | 无上限量尺 | [厂商报告](<https://huggingface.co/Qwen/Qwen3.5-397B-A17B/raw/main/README.md>) |
| RefSpatialBench | 视觉与空间 | RefSpatialBench / qwen35-card快照 | 73.6 分 | Qwen3.5-397B-A17B | 无上限量尺 | [厂商报告](<https://huggingface.co/Qwen/Qwen3.5-397B-A17B/raw/main/README.md>) |
| ERQA | 视觉与空间 | ERQA / qwen35-card快照 | 70.5 分 | Gemini-3 Pro | 无上限量尺 | [厂商报告](<https://huggingface.co/Qwen/Qwen3.5-397B-A17B/raw/main/README.md>) |
| LingoQA | 视觉与空间 | LingoQA / qwen35-card快照 | 81.6 分 | Qwen3.5-397B-A17B | 无上限量尺 | [厂商报告](<https://huggingface.co/Qwen/Qwen3.5-397B-A17B/raw/main/README.md>) |
| V* | 视觉与空间 | V* / qwen35-card快照 | 88 分 | Gemini-3 Pro | 无上限量尺 | [厂商报告](<https://huggingface.co/Qwen/Qwen3.5-397B-A17B/raw/main/README.md>) |
| Video-MME | 视频与时间理解 | VideoMME(w sub.) / qwen35-card快照 | 88.4 % | Gemini-3 Pro | 进行中 | [厂商报告](<https://huggingface.co/Qwen/Qwen3.5-397B-A17B/raw/main/README.md>) |
| Video-MMMU | 视频与时间理解 | VideoMMMU / qwen35-card快照 | 87.6 分 | Gemini-3 Pro | 无上限量尺 | [厂商报告](<https://huggingface.co/Qwen/Qwen3.5-397B-A17B/raw/main/README.md>) |
| MVBench | 视频与时间理解 | MVBench / qwen35-card快照 | 78.1 % | GPT5.2 | 进行中 | [厂商报告](<https://huggingface.co/Qwen/Qwen3.5-397B-A17B/raw/main/README.md>) |
| MLVU | 视频与时间理解 | MLVU (M-Avg) / qwen35-card快照 | 86.7 分 | Qwen3.5-397B-A17B | 无上限量尺 | [厂商报告](<https://huggingface.co/Qwen/Qwen3.5-397B-A17B/raw/main/README.md>) |
| LVBench | 视频与时间理解 | LVBench / qwen35-card快照 | 76.2 % | Gemini-3 Pro | 进行中 | [厂商报告](<https://huggingface.co/Qwen/Qwen3.5-397B-A17B/raw/main/README.md>) |
| MMVU | 视频与时间理解 | MMVU / qwen35-card快照 | 80.8 分 | GPT5.2 | 无上限量尺 | [厂商报告](<https://huggingface.co/Qwen/Qwen3.5-397B-A17B/raw/main/README.md>) |
| EgoSchema | 视频与时间理解 | — | — | — | 暂无成绩 | [原始任务 ↗](<https://egoschema.github.io/>) |
| TempCompass | 视频与时间理解 | — | — | — | 暂无成绩 | [原始任务 ↗](<https://github.com/llyx97/TempCompass>) |
| Perception Test | 视频与时间理解 | — | — | — | 暂无成绩 | [原始任务 ↗](<https://github.com/google-deepmind/perception_test>) |
| AudioBench | 听觉与语音 | — | — | — | 暂无成绩 | [原始任务 ↗](<https://github.com/AudioLLMs/AudioBench>) |
| MMAU | 听觉与语音 | Qwen2.5-Omni官方比较表快照 | 65.6 % | Qwen2.5-Omni-7B | 进行中 | [厂商报告](<https://raw.githubusercontent.com/QwenLM/Qwen2.5-Omni/main/README.md>) |
| LibriSpeech | 听觉与语音 | Qwen2.5-Omni官方比较表快照 | 2.8 % | Seed-ASR-Multilingual | 无上限量尺 | [厂商报告](<https://raw.githubusercontent.com/QwenLM/Qwen2.5-Omni/main/README.md>) |
| AISHELL-1 | 听觉与语音 | — | — | — | 暂无成绩 | [原始任务 ↗](<https://www.openslr.org/33/>) |
| CoVoST 2 | 听觉与语音 | Qwen2.5-Omni官方比较表快照 | 48.2 分 | MiniCPM-o | 无上限量尺 | [厂商报告](<https://raw.githubusercontent.com/QwenLM/Qwen2.5-Omni/main/README.md>) |
| Clotho | 听觉与语音 | — | — | — | 暂无成绩 | [原始任务 ↗](<https://zenodo.org/records/3490684>) |
| AudioSet | 听觉与语音 | — | — | — | 暂无成绩 | [原始任务 ↗](<https://research.google.com/audioset/>) |
| IEMOCAP | 听觉与语音 | — | — | — | 暂无成绩 | [原始任务 ↗](<https://sail.usc.edu/iemocap/>) |
| MELD | 听觉与语音 | Qwen2.5-Omni官方比较表快照 | 0.57 分 | Qwen2.5-Omni-7B | 无上限量尺 | [厂商报告](<https://raw.githubusercontent.com/QwenLM/Qwen2.5-Omni/main/README.md>) |
| GAIA | 代理与执行 | — | — | — | 暂无成绩 | [原始任务 ↗](<https://huggingface.co/gaia-benchmark>) |
| BFCL | 代理与执行 | BFCL-V4 / qwen35-card快照 | 77.5 分 | Claude 4.5 Opus | 无上限量尺 | [厂商报告](<https://huggingface.co/Qwen/Qwen3.5-397B-A17B/raw/main/README.md>) |
| τ²-bench | 代理与执行 | TAU2-Bench / qwen35-card快照 | 91.6 分 | Claude 4.5 Opus | 无上限量尺 | [厂商报告](<https://huggingface.co/Qwen/Qwen3.5-397B-A17B/raw/main/README.md>) |
| VITA-Bench | 代理与执行 | VITA-Bench / qwen35-card快照 | 56.3 分 | Claude 4.5 Opus | 无上限量尺 | [厂商报告](<https://huggingface.co/Qwen/Qwen3.5-397B-A17B/raw/main/README.md>) |
| DeepPlanning | 代理与执行 | DeepPlanning / qwen35-card快照 | 44.6 % | GPT5.2 | 差距明显 | [厂商报告](<https://huggingface.co/Qwen/Qwen3.5-397B-A17B/raw/main/README.md>) |
| Toolathlon | 代理与执行 | Tool Decathlon / qwen35-card快照 | 43.8 % | GPT5.2 | 差距明显 | [厂商报告](<https://huggingface.co/Qwen/Qwen3.5-397B-A17B/raw/main/README.md>) |
| MCPMark | 代理与执行 | MCP-Mark / qwen35-card快照 | 57.5 % | GPT5.2 | 进行中 | [厂商报告](<https://huggingface.co/Qwen/Qwen3.5-397B-A17B/raw/main/README.md>) |
| BrowseComp | 代理与执行 | BrowseComp / qwen35-card快照 | 67.8 % | Claude 4.5 Opus | 进行中 | [厂商报告](<https://huggingface.co/Qwen/Qwen3.5-397B-A17B/raw/main/README.md>) |
| BrowseComp-zh | 代理与执行 | BrowseComp-zh / qwen35-card快照 | 76.1 % | GPT5.2 | 进行中 | [厂商报告](<https://huggingface.co/Qwen/Qwen3.5-397B-A17B/raw/main/README.md>) |
| WideSearch | 代理与执行 | WideSearch / qwen35-card快照 | 76.8 分 | GPT5.2 | 无上限量尺 | [厂商报告](<https://huggingface.co/Qwen/Qwen3.5-397B-A17B/raw/main/README.md>) |
| WebArena | 代理与执行 | — | — | — | 暂无成绩 | [原始任务 ↗](<https://github.com/web-arena-x/webarena>) |
| VisualWebArena | 代理与执行 | — | — | — | 暂无成绩 | [原始任务 ↗](<https://jykoh.com/vwa>) |
| WebLINX | 代理与执行 | — | — | — | 暂无成绩 | [原始任务 ↗](<https://mcgill-nlp.github.io/weblinx/>) |
| OSWorld | 代理与执行 | OSWorld-Verified / qwen35-card快照 | 66.3 % | Claude 4.5 Opus | 进行中 | [厂商报告](<https://huggingface.co/Qwen/Qwen3.5-397B-A17B/raw/main/README.md>) |
| AndroidWorld | 代理与执行 | AndroidWorld / qwen35-card快照 | 66.8 % | Qwen3.5-397B-A17B | 进行中 | [厂商报告](<https://huggingface.co/Qwen/Qwen3.5-397B-A17B/raw/main/README.md>) |
| ScreenSpot | 代理与执行 | — | — | — | 暂无成绩 | [原始任务 ↗](<https://github.com/njucckevin/SeeClick>) |
| ScreenSpot-Pro | 代理与执行 | ScreenSpot Pro / qwen35-card快照 | 72.7 % | Gemini-3 Pro | 进行中 | [厂商报告](<https://huggingface.co/Qwen/Qwen3.5-397B-A17B/raw/main/README.md>) |
| Terminal-Bench | 代理与执行 | Terminal Bench 2 / qwen35-card快照 | 59.3 % | Claude 4.5 Opus | 进行中 | [厂商报告](<https://huggingface.co/Qwen/Qwen3.5-397B-A17B/raw/main/README.md>) |
| METR Time Horizons | 代理与执行 | — | — | — | 暂无成绩 | [原始任务 ↗](<https://metr.org/time-horizons/>) |
| WorkArena | 代理与执行 | — | — | — | 暂无成绩 | [原始任务 ↗](<https://github.com/ServiceNow/WorkArena>) |
| AgentBench | 代理与执行 | — | — | — | 暂无成绩 | [原始任务 ↗](<https://github.com/THUDM/AgentBench>) |
| GDPval | 专业工作与创造 | — | — | — | 暂无成绩 | [原始任务 ↗](<https://huggingface.co/datasets/openai/gdpval>) |
| HealthBench | 专业工作与创造 | HealthBench / qwen38-card快照 | 60.2 分 | Qwen3.8-Max | 无上限量尺 | [厂商报告](<https://huggingface.co/Qwen/Qwen3.8-2.4T-A95B/raw/main/README.md>) |
| MedQA | 专业工作与创造 | — | — | — | 暂无成绩 | [原始任务 ↗](<https://github.com/jind11/MedQA>) |
| PubMedQA | 专业工作与创造 | — | — | — | 暂无成绩 | [原始任务 ↗](<https://pubmedqa.github.io/>) |
| SLAKE | 专业工作与创造 | SLAKE / qwen35-card快照 | 81.6 % | K2.5-1T-A32B | 进行中 | [厂商报告](<https://huggingface.co/Qwen/Qwen3.5-397B-A17B/raw/main/README.md>) |
| PMC-VQA | 专业工作与创造 | PMC-VQA / qwen35-card快照 | 64.2 % | Qwen3.5-397B-A17B | 进行中 | [厂商报告](<https://huggingface.co/Qwen/Qwen3.5-397B-A17B/raw/main/README.md>) |
| MedXpertQA | 专业工作与创造 | MedXpertQA-MM / qwen35-card快照 | 76 % | Gemini-3 Pro | 进行中 | [厂商报告](<https://huggingface.co/Qwen/Qwen3.5-397B-A17B/raw/main/README.md>) |
| LegalBench | 专业工作与创造 | — | — | — | 暂无成绩 | [原始任务 ↗](<https://github.com/HazyResearch/legalbench>) |
| FinQA | 专业工作与创造 | — | — | — | 暂无成绩 | [原始任务 ↗](<https://github.com/czyssrs/FinQA>) |
| WritingBench | 专业工作与创造 | — | — | — | 暂无成绩 | [原始任务 ↗](<https://github.com/X-PLUG/WritingBench>) |
| GenEval | 专业工作与创造 | 官方README原始模型表 | 61 分 | IF-XL | 无上限量尺 | [官方榜单](<https://raw.githubusercontent.com/djghosh13/geneval/main/README.md>) |
| VBench | 专业工作与创造 | — | — | — | 暂无成绩 | [原始任务 ↗](<https://github.com/Vchitect/VBench>) |
| ToMBench | 社会认知与合作 | arXiv:2402.15052v1 | 75.3 % | GPT-4-1106 | 进行中 | [论文](<https://arxiv.org/html/2402.15052v1>) |
| Social IQa | 社会认知与合作 | — | — | — | 暂无成绩 | [原始任务 ↗](<https://maartensap.com/social-iqa/>) |
| SOTOPIA | 社会认知与合作 | — | — | — | 暂无成绩 | [原始任务 ↗](<https://github.com/sotopia-lab/sotopia>) |
| Deal or No Deal | 社会认知与合作 | — | — | — | 暂无成绩 | [原始任务 ↗](<https://github.com/facebookresearch/end-to-end-negotiator>) |
| HarmBench | 安全与稳健性 | — | — | — | 暂无成绩 | [原始任务 ↗](<https://github.com/centerforaisafety/HarmBench>) |
| StrongREJECT | 安全与稳健性 | — | — | — | 暂无成绩 | [原始任务 ↗](<https://github.com/dsbowen/strong_reject>) |
| AgentDojo | 安全与稳健性 | — | — | — | 暂无成绩 | [原始任务 ↗](<https://github.com/ethz-spylab/agentdojo>) |
| BBQ | 安全与稳健性 | — | — | — | 暂无成绩 | [原始任务 ↗](<https://github.com/nyu-mll/BBQ>) |
| ToxiGen | 安全与稳健性 | — | — | — | 暂无成绩 | [原始任务 ↗](<https://github.com/microsoft/TOXIGEN>) |
| WildGuardMix | 安全与稳健性 | arXiv:2406.18495v1 / WildGuardTest | 91.4 分 | GPT-4 | 无上限量尺 | [论文](<https://arxiv.org/html/2406.18495v1>) |
| BEHAVIOR | 具身与运动 | — | — | — | 暂无成绩 | [原始任务 ↗](<https://behavior.stanford.edu/>) |
| CALVIN | 具身与运动 | — | — | — | 暂无成绩 | [原始任务 ↗](<https://github.com/mees/calvin>) |
| LIBERO | 具身与运动 | arXiv:2502.19645v1 | 95.4 % | OpenVLA (fine-tuned) + PD&AC, Cont-Diffusion | 接近满分 | [论文](<https://arxiv.org/html/2502.19645v1>) |
| RLBench | 具身与运动 | — | — | — | 暂无成绩 | [原始任务 ↗](<https://github.com/stepjam/RLBench>) |
| Meta-World | 具身与运动 | — | — | — | 暂无成绩 | [原始任务 ↗](<https://meta-world.github.io/>) |
| ALFRED | 具身与运动 | — | — | — | 暂无成绩 | [原始任务 ↗](<https://askforalfred.com/>) |
| Habitat | 具身与运动 | — | — | — | 暂无成绩 | [原始任务 ↗](<https://aihabitat.org/>) |
| MMSI-Bench | 视觉与空间 | 官方README榜单快照 | 49.2 % | Gemini-3-pro | 进行中 | [官方榜单](<https://raw.githubusercontent.com/InternRobotics/MMSI-Bench/main/README.md>) |
| RE-Bench | 科学与研究 | — | — | — | 暂无成绩 | [原始任务 ↗](<https://github.com/METR/RE-Bench>) |

## 怎么算

职业代理指数按覆盖系数乘基准相对成绩：直接 1.0、部分 0.5，缺测贡献记 0。学科轴只展示任务关联和基准原始成绩，未测为未知；不计算学科或 AGI 完成百分比。

**局限**：映射为人工编辑，尚未独立审阅；成绩含厂商自报。以美国职业体系为准，职业等权、未按就业人数加权。科研主题不等于完整能力清单。映射表示任务相关性，不代表学科掌握度；上级映射不下放到子主题。未测为未知，基准总分不作为学科分数。

来源：[O*NET 31.0](<https://www.onetcenter.org/database.html>) · [OpenAlex topics](<https://api.openalex.org/topics>) · [METR](<https://metr.org/assets/benchmark_results_1_1.yaml>) · [Epoch AI ECI](<https://epoch.ai/data/eci_scores.csv>)
