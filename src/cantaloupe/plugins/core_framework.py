import os
import typing
from typing import Any

from jinja2 import Template

from ._core_framework_validators import _validate_imports
from .. import hookimpl
from ..loaders import load_workflow

if typing.TYPE_CHECKING:
    from ..models import Step


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
            step.config[key] = Template(value).render({"variables": step.variables})
        else:
            step.config[key] = value
    return step


@hookimpl(tryfirst=True)
def cantaloupe_build_workflow(config, workflow) -> None:
    steps: list["Step"] = []
    for index, step in enumerate(workflow.steps, start=1):
        _validate_imports(index, step, workflow)

        if not step.use:
            steps.append(step)
        else:
            # Load the workflow
            imported_workflow = load_workflow(os.path.join(config.option.workflows, step.use))
            if not imported_workflow.variables:
                # merge imported workflow steps into current workflow
                for imported_steps in imported_workflow.steps:
                    steps.append(imported_steps)
            else:
                for var in imported_workflow.variables:
                    # check if all required variables are set
                    if var.required and var.name not in step.variables:
                        raise KeyError(f"Variable {var} is required by the workflow {step.use} but not set.")

                    # if variable not provided by step and workflow has default value, use default value
                    if var.name not in step.variables:
                        if var.default:
                            step.variables[var.name] = var.default
                        else:
                            step.variables[var.name] = None

                for wf_step in imported_workflow.steps:
                    wf_step.variables = step.variables
                    steps.append(wf_step)

    # hydrate variables with env prefixes
    workflow.steps = [_hydrate_variables(step) for step in steps]
