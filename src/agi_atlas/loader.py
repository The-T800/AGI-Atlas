"""从可审阅的 YAML 加载数据，并拒绝重复键。"""

from pathlib import Path

import yaml
from pydantic import BaseModel, TypeAdapter, ValidationError

from agi_atlas.models import AtlasData, Benchmark, BenchmarkScore, MetricRule, ModelEntry
from agi_atlas.validator import DataValidationError, validate_data


class UniqueKeyLoader(getattr(yaml, "CSafeLoader", yaml.SafeLoader)):
    """避免 YAML 的重复键静默覆盖数据。"""


def _construct_mapping(loader: UniqueKeyLoader, node: yaml.MappingNode) -> dict:
    result: dict = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=True)
        try:
            if key in result:
                raise DataValidationError(
                    f"YAML 第 {key_node.start_mark.line + 1} 行存在重复键：{key}"
                )
            result[key] = loader.construct_object(value_node, deep=True)
        except TypeError as exc:
            raise DataValidationError("YAML 字段名必须是可哈希的标量") from exc
    return result


UniqueKeyLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _construct_mapping)


def read_yaml(path: Path) -> object:
    try:
        return yaml.load(path.read_text(encoding="utf-8"), Loader=UniqueKeyLoader)
    except (OSError, UnicodeError, yaml.YAMLError, DataValidationError) as exc:
        raise DataValidationError(f"无法读取 {path}：{exc}") from exc


def read_model[T: BaseModel](path: Path, schema: type[T]) -> T:
    try:
        return schema.model_validate(read_yaml(path))
    except ValidationError as exc:
        raise DataValidationError(f"{path} 字段校验失败：{_details(exc)}") from exc


def _details(exc: ValidationError) -> str:
    return "; ".join(
        f"{'.'.join(map(str, e['loc']))}："
        + (
            str(e["ctx"]["error"])
            if e["type"] == "value_error"
            else f"字段缺失或值不符合约束（{e['type']}）"
        )
        for e in exc.errors()
    )


def _load_records[T: BaseModel](path: Path, model: type[T]) -> list[T]:
    raw = read_yaml(path)
    if not isinstance(raw, list):
        raise DataValidationError(f"{path} 顶层必须为列表，空集合请写 []")
    try:
        return TypeAdapter(list[model]).validate_python(raw)
    except ValidationError as exc:
        raise DataValidationError(f"{path} 字段校验失败：{_details(exc)}") from exc


def load_data(data_dir: Path | str = "data") -> AtlasData:
    root = Path(data_dir)
    # 指标规则与模型注册表是可选增强数据；缺失时退回基准级方向与原始模型名。
    optional = {
        "metric_rules": (root / "benchmarks/metrics.yaml", MetricRule),
        "models": (root / "models/models.yaml", ModelEntry),
    }
    data = AtlasData(
        benchmarks=_load_records(root / "benchmarks/benchmarks.yaml", Benchmark),
        scores=_load_records(root / "scores/frontier_scores.yaml", BenchmarkScore),
        **{
            name: _load_records(path, model)
            for name, (path, model) in optional.items()
            if path.exists()
        },
    )
    validate_data(data)
    return data
