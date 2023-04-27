from __future__ import annotations

import pathlib

import click

from ..generation.generator import CodeGenerator, GeneratorResult
from ..loaders import load_workflow_context, load_workflows
from ..models import Context


def _create_output_directory(dst: pathlib.Path) -> pathlib.Path:
    dst.mkdir(exist_ok=True)
    test_dir = dst / "tests"
    test_dir.mkdir(exist_ok=True)
    return dst


_TYPE_DIR = click.Path(file_okay=False, dir_okay=True, resolve_path=True)


@click.command()
@click.argument("workflow-path", required=True, type=_TYPE_DIR)
@click.option("--output", type=_TYPE_DIR, default="generated", required=False)
def make_code(workflow_path: pathlib.Path, output: pathlib.Path) -> None:
    output = pathlib.Path(output)
    workflow_path = pathlib.Path(workflow_path)
    if not workflow_path.exists():
        click.secho(f"Workflow directory '{workflow_path.name}' does not exist", fg="red")
        raise click.Abort()

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

    data: GeneratorResult = generator.generate()

    _create_output_directory(output)

    for spec in data.files:
        with open(spec.path, "w") as f:
            f.write(spec.content)
