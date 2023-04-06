from __future__ import annotations

import os
import pathlib
from typing import Any

import click
import yaml

from .code_generation.generator import CodeGenerator, GeneratedData
from .load import load_workflow_context, load_workflows
from .models import Context


def _create_structure(dst: pathlib.Path) -> pathlib.Path:
    dst.mkdir(exist_ok=True)
    test_dir = dst / "tests"
    test_dir.mkdir(exist_ok=True)
    return dst


@click.group()
def entry() -> None:
    pass


@click.command()
@click.argument("workflow-path", required=True, type=click.Path(file_okay=False, dir_okay=True, resolve_path=True))
@click.option(
    "--output",
    type=click.Path(file_okay=False, dir_okay=True, resolve_path=True),
    default="generated",
    required=False,
)
def convert(workflow_path: pathlib.Path, output: pathlib.Path) -> None:
    context_data = load_workflow_context(workflow_path)
    if context_data is None:
        click.secho(f"Missing context.yaml file in {workflow_path.name} directory", fg="red")
        raise click.Abort()

    workflows = load_workflows(workflow_path)
    context = Context(
        **context_data,
        workflows=workflows,
        output_dir=output,
        workflow_dir=workflow_path,
    )

    generator = CodeGenerator(context)

    data: GeneratedData = generator.generate()
    for spec in data.specs:
        print(spec.path)
        print(spec.content)

    # wf = Workflow(**yaml.safe_load(workflow))  # type: ignore
    # generator = CodeGenerator(wf)
    # generated = generator.generate()
    # path = _create_structure(dst)

    # with open(path / "playwright.config.js", "w") as file:
    #     file.write(generated.config_file)

    # with open(path / "tests" / "test_01.spec.js", "w") as file:
    #     file.write(generated.test_file)


entry.add_command(convert)
