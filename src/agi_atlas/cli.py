"""命令行：校验数据、生成双语报告与离线页面。"""

import sys
from pathlib import Path
from typing import Annotated

import typer

from agi_atlas.loader import load_data
from agi_atlas.models import AtlasData
from agi_atlas.report import write_reports
from agi_atlas.site import write_site
from agi_atlas.validator import DataValidationError

app = typer.Typer(
    help="AGI Atlas: how far AI is from AGI, measured against every human job and discipline.",
    no_args_is_help=True,
)
DataDir = Annotated[Path, typer.Option("--data-dir", help="Data directory.")]


@app.callback()
def _utf8_console() -> None:
    """Windows 控制台默认 GBK，统一改为 UTF-8，避免中文输出乱码。"""
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is not None:
            reconfigure(encoding="utf-8", errors="replace")


def _run[T](action, *args) -> T:
    try:
        return action(*args)
    except DataValidationError as exc:
        typer.echo(f"Error: {exc}", err=True)
        raise typer.Exit(code=1) from exc
    except OSError as exc:
        typer.echo(f"Error: cannot write output ({exc})", err=True)
        raise typer.Exit(code=1) from exc


def _load(data_dir: Path) -> AtlasData:
    return _run(load_data, data_dir)


@app.command("validate")
def validate_command(data_dir: DataDir = Path("data")) -> None:
    """Validate all data files and cross-file references."""
    data = _load(data_dir)
    typer.echo(
        f"OK: {len(data.benchmarks)} benchmarks, {len(data.scores)} scores, "
        f"{len(data.models)} models."
    )


@app.command("report")
def report_command(
    data_dir: DataDir = Path("data"),
    output: Annotated[Path, typer.Option("--output", "-o", help="Output directory.")] = Path(
        "reports"
    ),
) -> None:
    """Write reports/report.zh.md and reports/report.en.md."""
    data = _load(data_dir)
    for path in _run(write_reports, data, data_dir, output):
        typer.echo(f"Wrote {path}")


@app.command("site")
def site_command(
    data_dir: DataDir = Path("data"),
    output: Annotated[Path, typer.Option("--output", "-o", help="HTML file.")] = Path(
        "docs/index.html"
    ),
) -> None:
    """Write the bilingual offline page (docs/index.html, ready for GitHub Pages)."""
    data = _load(data_dir)
    typer.echo(f"Wrote {_run(write_site, data, data_dir, output)}")
