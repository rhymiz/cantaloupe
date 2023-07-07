import typing

from ..enums import Action
from ..errors import InvalidWorkflowStep

if typing.TYPE_CHECKING:
    from ..models import Step, Workflow


def _validate_imports(index, step: "Step", workflow: "Workflow") -> None:
    """
    Validates an import step.
    """
    if step.action == Action.IMPORT and step.use is None:
        msg = (
            f"Step {index} in workflow '{workflow.name}' does not have a 'use' key. "
            "Please provide a workflow to import."
        )
        raise InvalidWorkflowStep(msg)
