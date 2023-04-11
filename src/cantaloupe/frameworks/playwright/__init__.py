import json
import os
import typing

from slugify import slugify

from .template import get_template_from_fs, get_template_from_string
from .translate import translate_to_playwright
from ..hookspec import hookimpl
from ...generation.types import File

if typing.TYPE_CHECKING:
    from ...models import Context, Step, Workflow


class PlaywrightPlugin:
    @hookimpl
    def cantaloupe_render_step(self, step: "Step") -> str:
        context: dict[str, typing.Any] = {
            "input": json.dumps(step.input),
            "action": translate_to_playwright(step.action),
            "selector": json.dumps(step.selector),
            "input_options": json.dumps(step.input_options),
            "selector_options": json.dumps(step.selector_options),
        }
        if step.template:
            tpl = get_template_from_string(step.template)
        else:
            tpl = get_template_from_fs(f"action_{step.action}.txt")
        return tpl.render(context)

    @hookimpl
    def cantaloupe_build_spec(self, context: "Context", workflow: "Workflow", steps: list["Step"]) -> File:
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
    def cantaloupe_setup(self, context: "Context") -> None:
        pass

    @hookimpl
    def cantaloupe_teardown(self, context: "Context") -> None:
        pass
