"""验证唯一性与跨文件引用。"""

from agi_atlas.models import AtlasData
from agi_atlas.naming import model_key


class DataValidationError(ValueError):
    """数据结构或引用不符合约定。"""


def validate_data(data: AtlasData) -> None:
    errors: list[str] = []
    benchmarks = {}
    for b in data.benchmarks:
        if b.id in benchmarks:
            errors.append(f"基准 ID 重复：{b.id}")
        benchmarks[b.id] = b

    score_keys: set[tuple] = set()
    for s in data.scores:
        key = (
            s.benchmark_id,
            s.benchmark_version,
            s.model,
            s.model_provider,
            s.evaluation_date,
            str(s.source_url),
            s.protocol,
            s.subset,
            s.metric,
            s.source_locator,
        )
        if key in score_keys:
            errors.append(f"成绩记录重复：{s.benchmark_id} / {s.model}")
        score_keys.add(key)
        for known_date in (s.evaluation_date, s.published_at):
            if known_date is not None and known_date > s.observed_at:
                errors.append(f"成绩 {s.benchmark_id} 的日期晚于采集日期")
        if s.benchmark_id not in benchmarks:
            errors.append(f"成绩引用了不存在的基准：{s.benchmark_id}")

    rule_metrics: set[str] = set()
    for rule in data.metric_rules:
        if rule.metric in rule_metrics:
            errors.append(f"指标规则重复：{rule.metric}")
        rule_metrics.add(rule.metric)

    model_ids: set[str] = set()
    name_owner: dict[str, str] = {}
    for m in data.models:
        if m.id in model_ids:
            errors.append(f"模型 ID 重复：{m.id}")
        model_ids.add(m.id)
        for name in {model_key(n) for n in (m.name, *m.aliases)}:
            if name in name_owner and name_owner[name] != m.id:
                errors.append(f"模型名 {name} 同时属于 {name_owner[name]} 与 {m.id}")
            name_owner[name] = m.id

    if errors:
        raise DataValidationError("数据校验失败：\n- " + "\n- ".join(errors))
