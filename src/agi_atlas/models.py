"""核心数据契约：基准目录、可追溯的成绩、模型注册表。"""

from datetime import date
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, StringConstraints, model_validator

Identifier = Annotated[str, StringConstraints(pattern=r"^[a-z0-9][a-z0-9_-]*$")]
Text = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
Number = Annotated[float, Field(allow_inf_nan=False, strict=True)]
Direction = Literal["higher_is_better", "lower_is_better"]
SourceType = Literal[
    "official_benchmark", "model_provider", "paper", "independent_evaluation", "community"
]


class Record(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Benchmark(Record):
    id: Identifier
    name: Text
    path: Text  # 能力分类路径，如“软件工程/代码仓库维护/真实问题修复”
    url: HttpUrl
    tasks: list[Text] = Field(default_factory=list)
    metric_direction: Direction = "higher_is_better"

    @property
    def domain(self) -> str:
        return self.path.split("/")[0]


class BenchmarkScore(Record):
    benchmark_id: Identifier
    benchmark_version: Text
    model: Text
    model_provider: Text
    score: Number
    human_score: Number | None
    evaluation_date: date | None
    published_at: date | None = None
    observed_at: date
    protocol: Text
    subset: Text = "overall"
    metric: Text
    unit: Text
    source_locator: Text
    source_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    source_url: HttpUrl
    source_type: SourceType
    verified: bool
    notes: Text | None


class MetricRule(Record):
    """指标级方向覆盖；同一基准内不同指标可能方向相反（如准确率与 WER）。"""

    metric: Text
    direction: Direction
    note: Text


class ModelEntry(Record):
    """模型注册表：统一同一模型的不同写法；发布日期必须附来源。"""

    id: Identifier
    name: Text
    provider: Text
    release_date: date | None = None
    release_source: HttpUrl | None = None
    aliases: list[Text] = Field(default_factory=list)

    @model_validator(mode="after")
    def dated_with_source(self) -> "ModelEntry":
        if self.release_date is not None and self.release_source is None:
            raise ValueError(f"模型 {self.id} 的发布日期缺少来源")
        return self


class AtlasData(Record):
    benchmarks: list[Benchmark]
    scores: list[BenchmarkScore]
    metric_rules: list[MetricRule] = Field(default_factory=list)
    models: list[ModelEntry] = Field(default_factory=list)
