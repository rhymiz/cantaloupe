from typing import Any

from .generation.generator import WorkflowGenerator
from .models import Workflow


def load_workload(data: dict[str, Any]) -> Workflow:
    workflow = Workflow(**data)
    c = WorkflowGenerator(workflow)
    print(c.generate())
    return workflow
