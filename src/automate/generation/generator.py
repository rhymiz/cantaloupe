from __future__ import annotations

import os
import pathlib
import typing
from dataclasses import dataclass
from typing import Any

import yaml

from ..enums import Action
from ..generation.template import get_template
from ..generation.translate import translate_to_playwright
from ..models import Workflow

if typing.TYPE_CHECKING:
    from ..models import Step

# path to the workflows directory
workflows_dir = pathlib.Path(os.path.dirname(__file__)).parent / "contrib/workflows"


@dataclass(frozen=True)
class CodeGeneratorResult:
    """container for generated spec and playwright.config.js file"""

    test_file: str
    config_file: str


class CodeGenerator:
    """This class is responsible for translation YAML into
    valid scripts.
    """

    def __init__(self, workflow: "Workflow") -> None:
        self._steps: list[str] = []
        self._config: str | None = None
        self._workflow: "Workflow" = workflow

    def generate(self) -> CodeGeneratorResult:
        self._generate_steps(self._workflow)
        script = get_template("script.txt")
        config = get_template("playwright.config.txt")
        return CodeGeneratorResult(
            test_file=script.render(
                {
                    "name": self._workflow.name,
                    "steps": self._steps,
                }
            ),
            config_file=config.render({"workflow": self._workflow}),
        )

    def _handle_workflow_import(self, step: "Step") -> "Workflow":
        """imports a yaml file and returns a Workflow object"""

        filename = f"{step.use}.yaml"
        with open(os.path.join(workflows_dir.as_posix(), filename)) as file:
            imported_workflow = yaml.safe_load(file)
            return Workflow(**imported_workflow)

    def _generate_steps(self, workflow: "Workflow") -> list[str]:
        """iterates over all steps in the workflow
        and calls lifecycle hooks.
        """
        for step in workflow.steps:
            if step.action == Action.IMPORT:
                # the step being imported is a pointer to a workflow
                # that will be merged into the current workflow.
                imported_worklow = self._handle_workflow_import(step)
                self._generate_steps(imported_worklow)
                continue  # skip so that we don't also try to generate an import step
            self._generate_step(step)
        return self._steps

    def _generate_step(self, step: "Step") -> None:
        """produces the corresponding line of code for a given step"""
        context: dict[str, Any] = {
            "event": translate_to_playwright(step.action),
            "input": step.input,
            "selector": (
                step.selector
                if isinstance(step.selector, dict)
                else {"ref": step.selector}
            ),
        }

        if step.action in Action.page_level():
            template_name = "page.txt"
        elif step.action == Action.CODE:
            template_name = "page_code.txt"
        elif step.action == Action.SELECT:
            template_name = "page_select.txt"
        elif step.action == Action.SET_VARIABLE:
            template_name = "page_set_var.txt"
        elif step.action == Action.USE_VARIABLE:
            template_name = "page_use_var.txt"
        elif step.action in Action.recommended():
            template_name = "page_builtins.txt"
        else:
            template_name = "page_locator.txt"

        template = get_template(template_name)
        step_string = template.render(context)

        # store the generated javascript code for a given step
        step.template = step_string

        self._steps.append(step_string)
