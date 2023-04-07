import json
import os
import typing

import pluggy
from jinja2 import Template
from slugify import slugify

from ..generation._dataclasses import BuildResult, Spec
from ..generation.template import get_template_from_fs
from ..generation.translate import translate_to_playwright
from ..models import Context, Step, Workflow

hookspec = pluggy.HookspecMarker("cantaloupe")
hookimpl = pluggy.HookimplMarker("cantaloupe")


class CantaloupeSpec:
    @hookspec
    def workflow_build_begin(self, workflow: Workflow) -> Workflow:
        return workflow

    @hookspec
    def workflow_build_complete(self, result: BuildResult) -> BuildResult:
        return result

    @hookspec
    def render_step(self, step: Step) -> str:
        pass

    @hookimpl
    def build_spec(self, workflow: Workflow, steps: list[Step]) -> Spec:
        pass


class PlaywrightPlugin:
    @hookimpl
    def render_step(self, step: Step) -> str:
        context: dict[str, typing.Any] = {
            "input": json.dumps(step.input),
            "action": translate_to_playwright(step.action),
            "selector": json.dumps(step.selector),
            "input_options": json.dumps(step.input_options),
            "selector_options": json.dumps(step.selector_options),
        }
        return step.template_object.render(context)

    @hookimpl
    def build_spec(self, context: Context, workflow: Workflow, steps: list[Step]) -> Spec:
        spec_content = get_template_from_fs("spec.txt")
        filename = f"{slugify(workflow.name, separator='-')}.spec.js"
        return Spec(
            name=filename,
            path=os.path.join(context.output_dir / "tests", filename),
            content=spec_content.render(
                {
                    "name": workflow.name,
                    "steps": steps,
                }
            ),
        )


pm = pluggy.PluginManager("cantaloupe")
pm.add_hookspecs(CantaloupeSpec)
pm.register(PlaywrightPlugin())
