import json
import os
import typing

from slugify import slugify

from ...generation.types import File
from ..hookspec import hookimpl
from .template import get_template_from_fs, get_template_from_string
from .translate import translate_to_playwright

if typing.TYPE_CHECKING:
    from ...models import Context, Step, Workflow


class PlaywrightPlugin:
    @hookimpl
    def render_step(self, step: "Step") -> str:
        context: dict[str, typing.Any] = {
            "input": json.dumps(step.input),
            "action": translate_to_playwright(step.action),
            "selector": json.dumps(step.selector),
            "input_options": json.dumps(step.input_options),
            "selector_options": json.dumps(step.selector_options),
        }
        if step.template:
            template = get_template_from_string(step.template)
        else:
            template = get_template_from_fs(f"action_{step.action}.txt")
        return template.render(context)

    @hookimpl
    def build_spec(self, context: "Context", workflow: "Workflow", steps: list["Step"]) -> File:
        spec_content = get_template_from_fs("spec.txt")
        filename = f"{slugify(workflow.name, separator='-')}.spec.js"
        return File(
            name=filename,
            path=os.path.join(context.output_dir / "tests", filename),
            content=spec_content.render(
                {
                    "name": workflow.name,
                    "steps": steps,
                }
            ),
        )

    @hookimpl
    def setup_framework(self, context: "Context") -> None:
        pass
