import json
import os
import typing

from slugify import slugify

from .template import get_template_from_fs, get_template_from_string
from .translate import translate_to_playwright
from ..hookspec import hookimpl
from ...types import Config, Spec

if typing.TYPE_CHECKING:
    from ...models import Context, Step, Workflow


class PlaywrightJSPlugin:
    """
    This plugin generates Playwright JS code.
    """

    @hookimpl
    def cantaloupe_render_step(self, step: "Step") -> str:
        context: dict[str, typing.Any] = {
            "input": json.dumps(step.input),
            "action": translate_to_playwright(step.action),
            "selector": json.dumps(step.selector),
            "input_options": json.dumps(step.input_options),
            "selector_options": json.dumps(step.selector_options),
        }
        tpl = (
            get_template_from_string(step.template)
            if step.template
            else get_template_from_fs(f"action_{step.action}.txt")
        )
        return tpl.render(context)

    @hookimpl
    def cantaloupe_build_spec(
        self,
        context: "Context",
        workflow: "Workflow",
        steps: list[str],
    ) -> Spec:
        """
        This hook is called to build the Spec for a workflow.

        :param context: build context of the current run
        :param workflow: workflow to build
        :param steps: list of steps to include in the spec
        :return: The generated spec
        """
        content = get_template_from_fs("spec.txt").render(
            {
                "name": workflow.name,
                "steps": steps,
            }
        )
        filename = f"{slugify(workflow.name, separator='-')}.spec.js"
        filepath = os.path.join(context.output_dir / "tests", filename)
        return Spec(name=filename, path=filepath, content=content)

    @hookimpl
    def cantaloupe_build_config_files(self, context: "Context") -> list[Config]:
        """
        This hook is called to build the config files for run.

        :param context: build context of the current run
        :return: The generated config files
        """
        filename = "playwright.config.js"
        content = get_template_from_fs("playwright.config.txt").render(context=context)
        filepath = os.path.join(context.output_dir, filename)
        return [Config(name=filename, path=filepath, content=content)]
