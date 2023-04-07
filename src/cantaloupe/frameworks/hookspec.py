import typing

import pluggy

if typing.TYPE_CHECKING:
    from ..generation.types import BuildResult, Spec
    from ..models import Context, Step, Workflow


hookspec = pluggy.HookspecMarker("cantaloupe")
hookimpl = pluggy.HookimplMarker("cantaloupe")


class CantaloupeSpec:
    @hookspec
    def setup_framework(self, context: "Context") -> None:
        pass

    @hookspec
    def teardown_framework(self, context: "Context") -> None:
        pass

    @hookspec
    def workflow_build_begin(self, workflow: "Workflow") -> "Workflow":
        return workflow

    @hookspec
    def workflow_build_complete(self, result: "BuildResult") -> "BuildResult":
        return result

    @hookspec
    def render_step(self, step: "Step") -> str:
        pass

    @hookspec
    def build_spec(self, context: "Context", workflow: "Workflow", steps: list["Step"]) -> "Spec":
        pass
