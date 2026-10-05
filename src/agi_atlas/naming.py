"""模型名归一：只消除大小写、空格、连字符和字母数字粘连差异，不合并不同设置。"""

import re

from agi_atlas.models import AtlasData, BenchmarkScore, ModelEntry


def model_key(name: str) -> str:
    """`GPT5.2`、`GPT-5.2`、`gpt 5.2` 得到同一键；`(High)` 等设置保留，仍是不同条目。"""
    value = re.sub(r"(?<=[a-z])(?=\d)|(?<=\d)(?=[a-z])", " ", name.lower())
    return " ".join(re.findall(r"[a-z0-9]+|[^\x00-\x7f]+", value))


class ModelResolver:
    """把原始成绩里的模型名解析到注册表条目；未登记的名字退回自身。"""

    def __init__(self, models: list[ModelEntry]):
        self.entries = {m.id: m for m in models}
        self.index: dict[str, ModelEntry] = {}
        for m in models:
            for name in (m.name, *m.aliases):
                self.index[model_key(name)] = m

    def entry(self, name: str) -> ModelEntry | None:
        return self.index.get(model_key(name))

    def model_id(self, score: BenchmarkScore) -> str:
        entry = self.entry(score.model)
        return entry.id if entry else "raw:" + model_key(score.model)


def resolver(data: AtlasData) -> ModelResolver:
    return ModelResolver(data.models)
