from __future__ import annotations

import typing
from dataclasses import dataclass

from ..enums import Action
from ..generation.template import get_template
from ..generation.translate import translate_to_playwright

if typing.TYPE_CHECKING:
    from ..models import Step, Workflow


@dataclass(frozen=True)
class CodeGeneratorResult:
    test_file: str
    config_file: str


class CodeGenerator:
    """Playwright code generator"""

    def __init__(self, workflow: "Workflow") -> None:
        self._steps: list[str] = []
        self._config: str | None = None
        self._workflow: "Workflow" = workflow

    def generate(self) -> CodeGeneratorResult:
        self._generate_steps()
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

    def _generate_steps(self) -> list[str]:
        """iterates over all steps in the workflow
        and calls lifecycle hooks.
        """
        for step in self._workflow.steps:
            self._generate_step(step)
        return self._steps

    def _generate_step(self, step: "Step") -> None:
        """produces the corresponding line of code for every given step"""
        context: dict[str, typing.Any] = {
            "event": translate_to_playwright(step.action),
            "input": step.input,
            "selector": (
                step.selector if isinstance(step.selector, dict) else {"ref": step.selector}
            )
        }

        if step.action == Action.GO:
            template_name = "page_goto.txt"
        elif step.action == Action.CODE:
            template_name = "page_code.txt"
        elif step.action == Action.SELECT:
            template_name = "page_select.txt"
        elif step.action == Action.SET_VARIABLE:
            template_name = "page_set_var.txt"
        elif step.action == Action.USE_VARIABLE:
            template_name = "page_use_var.txt"
        else:
            template_name = "page_locator.txt"

        template = get_template(template_name)
        step_string = template.render(context)

        # store the generated javascript code for a given step
        step.template = step_string

        self._steps.append(step_string)
