# AGI Atlas

[English](README.md) | **简体中文**

[![AGI Atlas](docs/preview.png)](https://the-t800.github.io/agi-atlas/?lang=zh)

**AI 离 AGI 还差多少？** 把人类**全部职业**和**全部学科**当作分母，用已公开的基准最好成绩逐项打分，没有基准测到的记 0。

| 分母 | 规模 | AI 已达到 |
| --- | --- | ---: |
| 职业（[O*NET 31.0](https://www.onetcenter.org/database.html)） | 923 个职业 · 18,838 项任务 · 2,087 项工作活动 | **0.91%** |
| 学科（GB/T 13745） | 2,656 个细分学科 | **11.68%** |

- **差距主要是"没测"，不是"测了不行"。** 93% 的人类工作没有任何基准；体力、照护、维修、施工类职业约为 0。
- **测到的地方，AI 已经很强。** 在有基准的 7% 工作上，AI 平均达到 42%；写代码（96.6）和修软件（80.0）最高。
- **计算机与数学类职业领先**，为 7.6%。

👉 **[打开交互页面](https://the-t800.github.io/agi-atlas/?lang=zh)**（也可离线打开 `docs/index.html`）· [完整报告](reports/report.zh.md)

## 怎么算

```
单项得分 = 覆盖系数 × 基准 SOTA          （每项取最高的一个基准；没有基准记 0）
覆盖系数 = 直接测量 1.0 · 部分测量 0.5     （学科只按二级 / 一级出题时再乘 0.3 / 0.1）
SOTA     = 最好成绩 ÷ 人类水平；没有人类对照时 ÷ 100%
AI 已达到 = 分母中全部单项的加权平均
```

职业按工作活动在该职业中的工作量占比加权（来自 O*NET 任务重要性），每个职业等权；学科等权。

全部系数写在 [`data/research/progress.yaml`](data/research/progress.yaml)，改完重建即可。

## 数据

| 内容 | 位置 |
| --- | --- |
| 187 个基准 | [`data/research/catalog.tsv`](data/research/catalog.tsv) |
| 3,706 条成绩（含来源、哈希、定位） | `data/scores/frontier_scores.yaml`（生成） |
| 分母表 | [`data/denominators/`](data/denominators) |
| 基准 → 工作活动 / 学科映射 | [`data/mappings/`](data/mappings)（每条附理由） |
| 中英译文 | [`data/i18n/`](data/i18n) |

成绩来自官方榜单、独立评测（Epoch AI）、论文与厂商模型卡；每条保留来源快照与 SHA-256。

**局限。** 映射为人工判定，尚未独立审阅；部分成绩为厂商自报；O*NET 以美国职业体系为准且未按就业人数加权；GB/T 13745 只有学科名称。

## 快速开始

需要 Python 3.12+ 与 [uv](https://docs.astral.sh/uv/)。

```bash
uv sync --extra dev
uv run agi-atlas validate      # 校验数据
uv run agi-atlas report        # 生成 reports/report.{zh,en}.md
uv run agi-atlas site          # 生成 docs/index.html
uv run pytest
```

重建生成数据（离线，基于已提交的来源快照）：

```bash
uv run python scripts/build_catalog.py
uv run python scripts/import_public_scores.py
uv run python scripts/build_models.py
uv run --extra build python scripts/build_denominators.py   # 首次运行会下载 O*NET / GB/T 13745
```

## 参与贡献

新增基准、成绩或修正映射，见 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 许可

代码：[MIT](LICENSE)。第三方数据保留各自许可：O*NET（CC BY 4.0，美国劳工部）、Epoch AI（CC BY 4.0）、METR、论文与模型卡按引用。O*NET 与 GB/T 13745 名称的译文为非官方译文。
