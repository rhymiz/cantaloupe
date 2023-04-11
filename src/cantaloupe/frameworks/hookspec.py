import typing

import pluggy

if typing.TYPE_CHECKING:
    from ..generation.types import BuildResult, Spec
    from ..models import Context, Step, Workflow

hookspec = pluggy.HookspecMarker("cantaloupe")
hookimpl = pluggy.HookimplMarker("cantaloupe")


class CantaloupeSpec:
    @hookspec
    def cantaloupe_setup(self, context: "Context") -> None:
        pass

    @hookspec
    def cantaloupe_teardown(self, context: "Context") -> None:
        """
        This hook is called after all workflows have been built.

        :param context: The build context of the current run
        :type context: Context
        :return: None
        :rtype: None
        """
        pass

    @hookspec
    def cantaloupe_workflow_build_begin(self, workflow: "Workflow") -> "Workflow":
        """
        This hook is called before a workflow is built.

        :param workflow:
        :type workflow:
        :return: The workflow to build
        :rtype: Workflow
        """
        return workflow

    @hookspec
    def cantaloupe_workflow_build_complete(self, result: "BuildResult") -> "BuildResult":
        """
        This hook is called after a workflow has been built.

        :param result: The result of the build
        :type result: BuildResult
        :return: The generated spec
        :rtype: BuildResult
        """
        return result

    @hookspec
    def cantaloupe_build_spec(self, context: "Context", workflow: "Workflow", steps: list["Step"]) -> "Spec":
        """
        This hook is called to build the spec for a workflow.

        :param context: The build context of the current run
        :type context: Context
        :param workflow: The workflow to build
        :type workflow: Workflow
        :param steps: A list of steps to build
        :type steps: list[Step]
        :return: The generated spec
        :rtype: Spec
        """
        pass

    @hookspec
    def cantaloupe_render_step(self, step: "Step") -> str:
        """
        This hook is called to render a step.
        :param step: The step to render
        :type step: Step
        :return: The rendered step as a string
        :rtype: str
        """
        pass
