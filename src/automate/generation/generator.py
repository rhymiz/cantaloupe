import json
import typing

from ..enums import Event
from ..generation.template import get_template
from ..generation.translate import translate_to_playwright

if typing.TYPE_CHECKING:
    from ..models import Step, Workflow


class CodeGenerator:
    """playwright code generator"""

    def __init__(self, workflow: "Workflow") -> None:
        self._steps: list[str] = []
        self._workflow: "Workflow" = workflow

    def generate(self) -> str:
        self._generate_steps()
        script = get_template("script.txt")
        context = {"name": self._workflow.name, "steps": self._steps}
        return script.render(context)

    def _generate_steps(self) -> list[str]:
        for step in self._workflow.steps:
            self._generate_step(step)
        return self._steps

    def _generate_step(self, step: "Step") -> None:
        context = {
            "event": translate_to_playwright(step.event),
            "input": step.input
        }
        if isinstance(step.selector, str):
            context["selector"] = {"ref": step.selector}
        else:
            context["selector"] = step.selector

        if step.event == Event.GO:
            template_name = "page_goto.txt"
        elif step.event == Event.CODE:
            template_name = "page_code.txt"
        elif step.event == Event.SELECT:
            template_name = "page_select.txt"
        elif step.event == Event.SET_VARIABLE:
            template_name = "page_set_var.txt"
        elif step.event == Event.USE_VARIABLE:
            template_name = "page_use_var.txt"
        else:
            template_name = "page_locator.txt"

        template = get_template(template_name)
        self._steps.append(template.render(context))
