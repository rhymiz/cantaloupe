from typing import Any

from .generation.generator import CodeGenerator
from .models import Workflow


def load_workflow(data: dict[str, Any]) -> Workflow:
    workflow = Workflow(**data)
    c = CodeGenerator(workflow)
    print(c.generate().test_file)
    return workflow
