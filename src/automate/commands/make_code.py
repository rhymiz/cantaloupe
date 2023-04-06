from __future__ import annotations

import os
import pathlib

import click

from ..generation.generator import CodeGenerator, GeneratedData
from ..load import load_workflow_context, load_workflows
from ..models import Context


def _create_output_directory(dst: pathlib.Path) -> pathlib.Path:
    dst.mkdir(exist_ok=True)
    test_dir = dst / "tests"
    test_dir.mkdir(exist_ok=True)
    return dst


@click.command()
@click.argument("workflow-path", required=True, type=click.Path(file_okay=False, dir_okay=True, resolve_path=True))
@click.option(
    "--output",
    type=click.Path(file_okay=False, dir_okay=True, resolve_path=True),
    default="generated",
    required=False,
)
def make_code(workflow_path: pathlib.Path, output: pathlib.Path) -> None:
    context_data = load_workflow_context(workflow_path)
    if context_data is None:
        click.secho(f"Missing context.yaml file in {workflow_path.name} directory", fg="red")
        raise click.Abort()

    output = pathlib.Path(output)
    workflow_path = pathlib.Path(workflow_path)

    workflows = load_workflows(workflow_path)
    context = Context(
        **context_data,
        workflows=workflows,
        output_dir=output,
        workflow_dir=workflow_path,
    )

    generator = CodeGenerator(context)

    data: GeneratedData = generator.generate()

    _create_output_directory(output)

    for spec in data.specs:
        with open(spec.path, "w") as f:
            f.write(spec.content)

    with open(os.path.join(output, "playwright.config.js"), "w") as f:
        f.write(data.config)
