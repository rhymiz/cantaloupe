import os
import typing
from importlib.metadata import version
from pathlib import Path
from typing import Any

from jinja2 import Template

from .. import hookimpl
from ..enums import Action
from ..loaders import load_workflow

if typing.TYPE_CHECKING:
    from ..models import Step


@hookimpl(tryfirst=True)
def cantaloupe_addoption(parser):
    """
    Called to add arguments to the parser.

    :param parser: the parser to add arguments to
    :type parser: argparse.ArgumentParser
    :return:
    :rtype:
    """

    parser.add_argument(
        "-w",
        "--workflows",
        type=lambda p: Path(p).absolute(),
        help="Path to the workflows directory.",
        required=True,
    )
    parser.add_argument(
        "-c",
        "--context",
        type=lambda p: Path(p).absolute(),
        help="Path to an alternate context file.",
        required=False,
    )

    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s {}".format(version("cantaloupe")),
    )


def _hydrate_variables(step) -> Any:
    """
    Loads the value of a variable.

    prefixing a variable with "env:" will load the value from the environment.
    """

    for key, value in step.variables.items():
        if value.startswith("env:"):
            step.variables[key] = os.getenv(value[4:])
        else:
            step.variables[key] = value

    for key, value in step.config.items():
        if "{{" in value and "}}" in value:
            print({"variables": step.variables})
            step.config[key] = Template(value).render({"variables": step.variables})
        else:
            step.config[key] = value
    return step


@hookimpl(tryfirst=True)
def cantaloupe_setup(config, context) -> None:

    for workflow in context.workflows:
        steps: list["Step"] = []

        for step in workflow.steps:
            if step.action == Action.IMPORT and not step.use:
                raise ValueError("Import step must have a 'use' attribute.")

            if not step.use:
                steps.append(step)
            else:
                # load the workflow
                workflow_ref = load_workflow(os.path.join(config.option.workflows, step.use))
                if not workflow_ref.variables:
                    for ref_step in workflow_ref.steps:
                        steps.append(ref_step)
                else:
                    for wf_var in workflow_ref.variables:
                        # check if all required variables are set
                        if wf_var.required and wf_var.name not in step.variables:
                            raise KeyError(f"Variable {wf_var} is required by the workflow {step.use} but not set.")

                        # if variable not provided by step and workflow has default value, use default value
                        if wf_var.name not in step.variables:
                            if wf_var.default:
                                step.variables[wf_var.name] = wf_var.default
                            else:
                                step.variables[wf_var.name] = None

                    for wf_step in workflow_ref.steps:
                        wf_step.variables = step.variables
                        steps.append(wf_step)

        # hydrate variables with env prefixes
        workflow.steps = [_hydrate_variables(step) for step in steps]
