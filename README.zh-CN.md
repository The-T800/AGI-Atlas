# [AGI Atlas](https://the-t800.github.io/AGI-Atlas/?lang=zh)

**[打开 GitHub Pages 交互页面](https://the-t800.github.io/AGI-Atlas/?lang=zh)**

[English](README.md) | **简体中文**

[![AGI Atlas](docs/preview.png)](https://the-t800.github.io/AGI-Atlas/?lang=zh)

用公开 Benchmark 证据观察 AI 在职业、学科和能力上的表现。

- **学科轴：OpenAlex 完整四级体系，4 个大域 → 26 个学科 → 252 个子领域 → 4,516 个主题。**
- **能力轴：12 个独立项目标签，覆盖全部目录 Benchmark 的能力标注。**
- **职业轴：923 个 O*NET 职业、2,087 项工作活动。现有职业代理指数为 0.91%，不代表 AGI 完成度。**
- **成绩：带来源快照的公开记录。点击“学科 × 能力”矩阵查看对应基准、成绩、日期和来源。**

## 数据时效

分类采用截至 **2026-10-05** 可获取的最新完整公开 OpenAlex 快照，**版本日期 2026-09-23，抓取日期 2026-10-05**。保存官方四级目录、发布清单和 SHA-256。它是完整公开版本，不冒充当天完整实时 API 数据。

<!-- benchmark-refresh:start -->
Benchmark 来源：**51 个**；抓取日期：**2026-10-08**。目录共 **193 个基准**、**3,730 条成绩**、**893 个模型**；**119 个基准**有核验转录成绩。

学科挂靠：**73 个基准**；其中 **45 个**有成绩，**5 个**有近一年日期明确的成绩。证据时间窗口按最新成绩抓取日期推进，与分类抓取日期独立。评测日期、发布日期、模型发布日期和抓取日期分别保留；重新下载不会把旧评测变成新评测。
<!-- benchmark-refresh:end -->

## 学科地图怎么读

矩阵数字是相关 Benchmark 数量，不是分数。能力独立标注，学科按实际任务挂靠；综合考试只关联证据支持的层级，不把总分复制给所有下级主题。当前证据数量由上方数据时效摘要自动生成。覆盖表分开显示四个层级：含下级关联共涉及 15 个学科、13 个子领域、10 个主题，其中 6 个主题有任务成绩证据。这不是学科分数。完整 4,516 主题区分“明确证据”“仅上级参考”和“待建立映射”，后续仍需逐项补证据。无法确认学科的基准保留能力标签。

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

一键刷新：`uv run python scripts/update_benchmarks.py`。在临时目录完成来源采集、成绩与模型重建、双语报告、页面及 README 摘要后，成功时才替换项目数据；`--offline` 只从保留快照离线重建。

GitHub Actions 的 `Refresh benchmark evidence` 每周一北京时间 09:00 自动运行，也支持手动触发。通过 lint、格式、测试、来源与可复现性检查后，实际提交更新到 `main` 并部署 Pages。自动流程刷新已配置的来源；新发现的 Benchmark 需要审核任务和评分口径后再更新目录与导入器，不将搜索结果直接当成已核验成绩。

不提交 API Key，不把不完整分页混入完整版本。默认构建与 CI 均离线复现。

[分类与证据说明](docs/subject-classification.md) · [完整报告](reports/report.zh.md) · [贡献指南](CONTRIBUTING.md)

代码 MIT；OpenAlex 数据 CC0；O*NET 与 Epoch AI 数据遵循其 CC BY 4.0 条款，其他评测材料保留各自来源条款。学科和能力映射是项目编辑判断，尚未独立复核；OpenAlex 是科研文献分类，不是完整人类能力清单。
