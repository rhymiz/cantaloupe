import pluggy

from cantaloupe.models import Step, Workflow

hookspec = pluggy.HookspecMarker("cantaloupe")
hookimpl = pluggy.HookimplMarker("cantaloupe")


class CantaloupeSpec:
    """Marker for cantaloupe plugin hooks."""

    def on_workflow_start(self, workflow: Workflow) -> Workflow:
        """Called when a workflow is about to be executed.

        Args:
            workflow (Workflow): The workflow that is about to be executed.
        """
        return workflow

    def on_step_start(self, step: Step) -> Step:
        """Called when a step is about to be executed.

        Args:
            step (Step): The step that is about to be executed.
        """
        return step

    def on_step_end(self, step: Step) -> Step:
        """Called when a step has been executed.

        Args:
            step (Step): The step that has been executed.
        """
        return step
