import typing

from ..enums import Action
from ..generation.template import get_template
from ..generation.translate import translate_to_playwright

if typing.TYPE_CHECKING:
    from ..models import Step, Workflow


class WorkflowGenerator:
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
        context: dict[str, typing.Any] = {
            "event": translate_to_playwright(step.action),
            "input": step.input,
        }

        # this allows us to
        context["selector"] = (
            step.selector if isinstance(step.selector, dict) else {"ref": step.selector}
        )

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
        self._steps.append(template.render(context))
