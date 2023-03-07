from __future__ import annotations

import os
import pathlib
from typing import Any

import click
import yaml

from .code_generation.generator import CodeGenerator
from .models import Context, Workflow


def _create_structure(dst: pathlib.Path) -> pathlib.Path:
    dst.mkdir(exist_ok=True)
    test_dir = dst / "tests"
    test_dir.mkdir(exist_ok=True)
    return dst


@click.group()
def entry() -> None:
    pass


def _load_workflows(workflows: pathlib.Path) -> list[Workflow]:
    return [
        Workflow(**yaml.safe_load(workflow.read_text()), file_name=workflow.name)
        for workflow in pathlib.Path(workflows).glob("*.yaml")
        if workflow.name != "context.yaml"
    ]


def _load_context(workflows: pathlib.Path) -> dict[str, Any] | None:
    context_file = pathlib.Path(os.path.join(workflows, "context.yaml"))
    if context_file.exists():
        return yaml.safe_load(context_file.read_text())
    return None


@click.command()
@click.argument("workflows", required=True, type=click.Path(file_okay=False, dir_okay=True, resolve_path=True))
@click.option(
    "--output",
    type=click.Path(file_okay=False, dir_okay=True, resolve_path=True),
    default="generated",
    required=False,
)
def convert(workflows: pathlib.Path, output: pathlib.Path) -> None:
    context_data = _load_context(workflows)
    if context_data is None:
        click.secho("No context.yaml file found in workflows directory", fg="red")
        raise click.Abort("No context.yaml file found in workflows directory")

    workflow_data = _load_workflows(workflows)
    context = Context(
        **context_data,
        workflows=workflow_data,
        output_dir=output,
        workflow_dir=workflows,
    )
    print(context.json(indent=4))

    # wf = Workflow(**yaml.safe_load(workflow))  # type: ignore
    # generator = CodeGenerator(wf)
    # generated = generator.generate()
    # path = _create_structure(dst)

    # with open(path / "playwright.config.js", "w") as file:
    #     file.write(generated.config_file)

    # with open(path / "tests" / "test_01.spec.js", "w") as file:
    #     file.write(generated.test_file)


entry.add_command(convert)
