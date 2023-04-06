from __future__ import annotations

import json
import os
import typing
from dataclasses import dataclass
from typing import Any

import yaml

from ..code_generation.template import get_template_from_fs, template_env
from ..code_generation.translate import translate_to_playwright
from ..enums import Action
from ..models import Step, Workflow

if typing.TYPE_CHECKING:
    from jinja2 import Template

    from ..models import Context


@dataclass(frozen=True)
class Spec:
    name: str
    path: str
    content: str


@dataclass(frozen=True)
class GeneratedData:
    specs: list[Spec]
    config: str


class CodeGenerator:
    """
    This class is responsible for translation YAML into
    valid scripts.
    """

    def __init__(self, context: "Context") -> None:
        self._context: "Context" = context

    def generate(self) -> GeneratedData:
        """
        generates the code for a given workflow
        """

        specs: list[Spec] = []
        for workflow in self._context.workflows:
            steps = self.generate_steps(workflow)
            specs.append(
                Spec(
                    name=workflow.name,
                    path=os.path.join(self._context.output_dir, workflow.name),
                    content=get_template_from_fs("spec.txt").render(
                        {
                            "name": workflow.name,
                            "steps": steps,
                        }
                    ),
                )
            )

        config = get_template_from_fs("playwright.config.txt").render(
            {
                "context": self._context,
            }
        )

        return GeneratedData(specs=specs, config=config)

    def import_workflow(self, step: "Step") -> "Workflow":
        """
        imports a yaml file and returns a Workflow object
        """
        filename = f"{step.use}.yaml"
        file_path = os.path.join(self._context.workflow_dir / filename)
        with open(file_path, encoding="utf-8") as file:
            string = file.read()
            file.close()
            template: "Template" = template_env.from_string(string)
            hydrated: str = template.render(step.variables)
            workflow: dict[str, Any] = yaml.safe_load(hydrated)
            return Workflow(**workflow)

    def generate_steps(self, workflow: "Workflow") -> list[str]:
        """
        iterates over all steps in the workflow
        and calls lifecycle hooks.
        """

        steps: list[str] = []
        for step in workflow.steps:
            # if an import is found, we need to import the workflow
            # and generate the steps for that workflow.
            if step.action == Action.IMPORT:
                imported_workflow = self.import_workflow(step)
                for istep in imported_workflow.steps:
                    if istep.action == Action.IMPORT:
                        raise ValueError("Nested imports are not supported")
                    steps.append(self.generate_step(istep))
            else:
                steps.append(self.generate_step(step))
        return steps

    def generate_step(self, step: "Step") -> str:
        """
        generates one or many lines of code for a given step
        """
        context: dict[str, Any] = {
            "input": json.dumps(step.input),
            "action": translate_to_playwright(step.action),
            "selector": json.dumps(step.selector),
            "input_options": json.dumps(step.input_options),
            "selector_options": json.dumps(step.selector_options),
        }
        return step.template_object.render(context)
