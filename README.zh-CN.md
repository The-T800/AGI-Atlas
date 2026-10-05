# AGI Atlas

**[打开 GitHub Pages 交互页面](https://the-t800.github.io/agi-atlas/?lang=zh)**

[English](README.md) | **简体中文**

[![AGI Atlas](docs/preview.png)](https://the-t800.github.io/agi-atlas/?lang=zh)

用公开 Benchmark 证据观察 AI 在职业、学科和能力上的表现。

- **学科轴：OpenAlex 完整四级体系，4 个大域 → 26 个学科 → 252 个子领域 → 4,516 个主题。**
- **能力轴：12 个独立项目标签，覆盖现有 187 个 Benchmark 的能力标注。**
- **职业轴：923 个 O*NET 职业、2,087 项工作活动。现有职业代理指数为 0.91%，不代表 AGI 完成度。**
- **成绩：3,706 条记录。点击“学科 × 能力”矩阵查看对应基准、成绩、日期和来源。**

## 数据时效

分类采用截至 **2026-10-05** 可获取的最新完整公开 OpenAlex 快照，**版本日期 2026-09-23，抓取日期 2026-10-05**。保存官方四级目录、发布清单和 SHA-256。它是完整公开版本，不冒充当天完整实时 API 数据。

30 个保留的 Benchmark 来源已于 **2026-10-05** 全部重新抓取。页面分别展示评测日期、发布日期与抓取日期。学科任务证据优先展示抓取时点前 365 天内有明确评测日期（缺失时用发布日期）的结果；历史或未知日期记录仍可在明细查看。重新下载不会把旧成绩变成新成绩。

## 学科地图怎么读

矩阵数字是相关 Benchmark 数量，不是分数。能力独立标注，学科按实际任务挂靠；综合考试只关联证据支持的层级，不把总分复制给所有下级主题。目前 187 个 Benchmark 中，70 个已挂靠学科，其中 45 个有已核验成绩、5 个有近一年日期明确的成绩。覆盖表分开显示四个层级：含下级关联共涉及 15 个学科、13 个子领域、10 个主题，其中 6 个主题有任务成绩证据。这不是学科分数。完整 4,516 主题区分“明确证据”“仅上级参考”和“待建立映射”，后续仍需逐项补证据。无法确认学科的基准保留能力标签。

未测主题显示“未知”，不记为失败。**学科不计算掌握百分比或 AGI 完成百分比**，原 Nature 代理指数已退役。OpenAlex 主题名称、描述保留官方英文，大域与学科有非官方中文译文。

职业代理指数沿用原公式：归一化基准最高成绩 × 覆盖系数（直接 1、部分 0.5），按活动重要性及职业等权汇总；只有这个职业代理指标把缺测贡献记为 0。

## 运行与刷新

需要 Python 3.12+ 和 uv。

```bash
uv sync --extra dev
uv run python scripts/build_openalex.py           # 从固定证据离线重建
uv run agi-atlas validate
uv run agi-atlas report
uv run agi-atlas site
uv run pytest
```

显式更新来源：

```bash
uv run python scripts/build_openalex.py --snapshot # 官方最新完整公开版
uv run python scripts/build_openalex.py --refresh  # 实时 API，可配置 OPENALEX_API_KEY
uv run python scripts/collect_sources.py --refresh
uv run python scripts/import_public_scores.py
uv run python scripts/build_models.py
uv run agi-atlas report
uv run agi-atlas site
```

不提交 API Key，不把不完整分页混入完整版本。默认构建与 CI 均离线复现。

[分类与证据说明](docs/subject-classification.md) · [完整报告](reports/report.zh.md) · [贡献指南](CONTRIBUTING.md)

代码 MIT；OpenAlex 数据 CC0；O*NET 与 Epoch AI 数据遵循其 CC BY 4.0 条款，其他评测材料保留各自来源条款。学科和能力映射是项目编辑判断，尚未独立复核；OpenAlex 是科研文献分类，不是完整人类能力清单。
