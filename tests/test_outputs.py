"""双语输出：页面与报告必须两种语言齐全、可复现、离线可用且不能被注入。"""

import json
import re

from conftest import REPO
from typer.testing import CliRunner

from agi_atlas.cli import app
from agi_atlas.i18n import LANGS, REPORT, UI, translate
from agi_atlas.loader import load_data
from agi_atlas.report import render_report
from agi_atlas.site import render_site

HAN = re.compile(r"[一-鿿]")


def test_every_ui_string_has_both_languages():
    for key, entry in {**UI, **REPORT}.items():
        assert set(entry) == set(LANGS), key
        assert all(entry[lang].strip() for lang in LANGS), key
        # 语言切换按钮在英文界面里显示“中文”，属于预期。
        assert key == "lang_switch" or not HAN.search(entry["en"]), key


def test_english_report_has_no_chinese():
    report = render_report(load_data(REPO / "data"), REPO / "data", "en")
    leftovers = [line for line in report.splitlines()[3:] if HAN.search(line)]
    assert not leftovers, leftovers[:3]


def test_page_data_names_are_bilingual():
    html = render_site(load_data(REPO / "data"), REPO / "data")
    payload = json.loads(re.search(r'id="atlas-data"[^>]*>(.*?)</script>', html, re.S)[1])
    p = payload["progress"]
    names = [
        *(g["name"] for g in p["onet"]["groups"]),
        *(g["name"] for g in p["onet"]["occupation_groups"]),
        *(g["name"] for g in p["gbt13745"]["groups"]),
        *(x["name"] for x in p["onet"]["top_leaves"] + p["gbt13745"]["top_leaves"]),
        *(x["name"] for x in p["onet"]["top_occupations"]),
    ]
    assert all(HAN.search(n["zh"]) and not HAN.search(n["en"]) for n in names)
    assert not [b["path_en"] for b in payload["benchmarks"] if HAN.search(b["path_en"])]


def test_committed_outputs_are_reproducible():
    data = load_data(REPO / "data")
    for lang in LANGS:
        committed = (REPO / f"reports/report.{lang}.md").read_text(encoding="utf-8")
        assert render_report(data, REPO / "data", lang) == committed
    assert render_site(data, REPO / "data") == (REPO / "docs/index.html").read_text(
        encoding="utf-8"
    )


def test_page_is_offline_and_escapes_embedded_data():
    data = load_data(REPO / "data")
    data.benchmarks[0].name = '</script><script>alert("x")</script>'
    html = render_site(data, REPO / "data")
    assert data.benchmarks[0].name not in html
    assert "<script src=" not in html and "fetch(" not in html


def test_translate_falls_back_per_segment():
    table = {"软件工程": "Software engineering", "快照": "snapshot"}
    assert translate("软件工程", table) == "Software engineering"
    assert translate("软件工程/未知", table) == "Software engineering / 未知"
    assert translate("SWE-bench", table) == "SWE-bench"


def test_cli_end_to_end(tmp_path):
    runner = CliRunner()
    data = str(REPO / "data")
    assert runner.invoke(app, ["validate", "--data-dir", data]).exit_code == 0
    result = runner.invoke(app, ["report", "--data-dir", data, "-o", str(tmp_path)])
    assert result.exit_code == 0, result.output
    assert {p.name for p in tmp_path.iterdir()} == {"report.zh.md", "report.en.md"}
    result = runner.invoke(app, ["site", "--data-dir", data, "-o", str(tmp_path / "i.html")])
    assert result.exit_code == 0, result.output


def test_cli_reports_bad_data_readably(tmp_path):
    result = CliRunner().invoke(app, ["validate", "--data-dir", str(tmp_path)])
    assert result.exit_code == 1
    assert "Error" in result.output
