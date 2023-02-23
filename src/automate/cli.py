from __future__ import annotations

import pathlib

import click
import yaml

from .generation.generator import CodeGenerator
from .models import Workflow


def _create_structure(dst: pathlib.Path) -> pathlib.Path:
    dst.mkdir(exist_ok=True)
    test_dir = dst / "tests"
    test_dir.mkdir(exist_ok=True)
    return dst


@click.group()
def entry() -> None:
    pass


@click.command()
@click.argument("workflow", required=True, type=click.File())
@click.option("--dst", type=pathlib.Path, default="generated", required=False)
def convert(workflow: click.File, dst: pathlib.Path) -> None:
    wf = Workflow(**yaml.safe_load(workflow))  # type: ignore
    generator = CodeGenerator(wf)
    generated = generator.generate()
    path = _create_structure(dst)

    with open(path / "playwright.config.js", "w") as file:
        file.write(generated.config_file)

    with open(path / "tests" / "test_01.js", "w") as file:
        file.write(generated.test_file)


entry.add_command(convert)
