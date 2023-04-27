from __future__ import annotations

import os
import typing
from typing import Any

import yaml
from jinja2 import Template, select_autoescape

from ..enums import Action
from ..frameworks import plugin_manager
from ..models import Workflow
from ..types import BuildResult, File, GeneratorResult

if typing.TYPE_CHECKING:
    from ..models import Context, Step


class CodeGenerator:
    """
    This class is responsible for translation YAML into
    valid scripts.
    """

    def __init__(self, context: "Context") -> None:
        self._context: "Context" = context
        self._reported_errors: list[str] = []

    def generate(self) -> GeneratorResult:
        """
        generates the code for all given workflows
        """

        plugin_manager.hook.cantaloupe_setup(context=self._context)  # type: ignore

        files: list[File] = []
        file_names: list[str] = []
        for raw_workflow in self._context.workflows:
            workflow = plugin_manager.hook.cantaloupe_workflow_build_begin(workflow=raw_workflow)  # type: ignore
            workflow = workflow[0] if len(workflow) > 0 else raw_workflow

            steps = self.generate_steps(workflow)
            spec_result = plugin_manager.hook.cantaloupe_build_spec(  # type: ignore
                context=self._context,
                workflow=workflow,
                steps=steps,
            )
            if len(spec_result) == 0:
                self._report_error("cantaloupe_build_spec", workflow)
                continue

            spec = spec_result[0]
            if spec.name in file_names:
                raise ValueError(f"Duplicate spec: {spec.name}")

            file_names.append(spec.name)

            workflow_complete = plugin_manager.hook.cantaloupe_workflow_build_complete(  # type: ignore
                result=BuildResult(workflow=workflow, spec=spec)
            )
            spec = workflow_complete[0].spec if len(workflow_complete) > 0 else spec
            files.append(spec)

        config_files = plugin_manager.hook.cantaloupe_build_config_files(context=self._context)  # type: ignore
        if len(config_files) > 0:
            files.extend(config_files[0])
        plugin_manager.hook.cantaloupe_teardown(context=self._context)  # type: ignore
        return GeneratorResult(files=files, errors=self._reported_errors)

    def import_workflow(self, step: "Step") -> "Workflow":
        """
        imports a yaml file and returns a Workflow object
        """
        filename = f"{step.use}.yaml"
        file_path = os.path.join(self._context.workflow_dir / filename)
        with open(file_path, encoding="utf-8") as file:
            string = file.read()
            file.close()
            template = Template(string, autoescape=select_autoescape())
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
                step_result = self.generate_step(step)
                if step_result:
                    steps.append(step_result)
        return steps

    def generate_step(self, step: "Step") -> str | None:
        """
        generates one or many lines of code for a given step
        """
        result = plugin_manager.hook.cantaloupe_render_step(step=step)  # type: ignore
        return result[0] if len(result) > 0 else None

    def _report_error(self, hook_name: str, entity: Any) -> None:
        self._reported_errors.append(f"{hook_name} hook did not return a value for: {entity}")
