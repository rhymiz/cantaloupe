from __future__ import annotations

import json
import os
import pathlib
import typing
from dataclasses import dataclass
from typing import Any

import yaml

from ..code_generation.template import get_template_from_fs, template_env
from ..code_generation.translate import translate_to_playwright
from ..enums import Action
from ..models import Context, Step, Workflow

if typing.TYPE_CHECKING:
    from jinja2 import Template


# path to the workflows directory
workflows_dir = pathlib.Path(os.path.dirname(__file__)).parent / "contrib/workflows"


@dataclass(frozen=True)
class CodeGeneratorResult:
    """container for generated spec and playwright.config.js file"""

    test_file: str
    config_file: str


class CodeGenerator:
    """
    This class is responsible for translation YAML into
    valid scripts.
    """

    def __init__(self, context: "Context") -> None:
        self._steps: list[str] = []
        self._config: str | None = None
        self._context: "Context" = context

    def generate(self) -> CodeGeneratorResult:
        """
        generates the code for a given workflow
        """
        self._generate_steps(self._workflow)
        spec = get_template_from_fs("spec.txt")
        config = get_template_from_fs("playwright.config.txt")
        return CodeGeneratorResult(
            test_file=spec.render(
                {
                    "name": self._workflow.name,
                    "steps": self._steps,
                }
            ),
            config_file=config.render({"context": self._context}),
        )

    def _handle_workflow_import(self, step: "Step") -> "Workflow":
        """
        imports a yaml file and returns a Workflow object
        """
        filename = f"{step.use}.yaml"
        with open(os.path.join(workflows_dir.as_posix(), filename), encoding="utf-8") as file:
            string = file.read()
            template: "Template" = template_env.from_string(string)
            hydrated: str = template.render(step.variables)
            workflow: dict[str, Any] = yaml.safe_load(hydrated)
            return Workflow(**workflow)

    def _generate_steps(self, workflow: "Workflow") -> list[str]:
        """
        iterates over all steps in the workflow
        and calls lifecycle hooks.
        """

        for step in workflow.steps:
            if step.action == Action.IMPORT:
                # the step being imported is a pointer to a workflow
                # that will be merged into the current workflow.
                imported_workflow = self._handle_workflow_import(step)
                self._generate_steps(imported_workflow)
            else:
                self._generate_step(step)
        return self._steps

    def _generate_step(self, step: "Step") -> None:
        """
        produces the corresponding line of code for a given step
        """

        context: dict[str, Any] = {
            "input": json.dumps(step.input),
            "action": translate_to_playwright(step.action),
            "selector": json.dumps(step.selector),
            "selector_options": json.dumps(step.selector_options),
            "input_options": json.dumps(step.input_options),
        }

        string = step.template_object.render(context)
        self._steps.append(string)
