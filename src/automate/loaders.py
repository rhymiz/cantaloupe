from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Iterable

import yaml

from .models import Workflow


def load_workflows(workflows: Path) -> Iterable[Workflow]:
    """
    loads all workflows from a given directory.
    :param workflows: directory containing the workflows
    :return: iterable of workflows


    Note: Workflow files must be named workflow_*.yaml
    """
    for workflow in workflows.glob("*.yaml"):
        if workflow.is_file() and workflow.name.startswith("workflow_"):
            yield Workflow(**yaml.safe_load(workflow.read_text()), file_name=workflow.name)


def load_workflow_context(workflows: Path) -> dict[str, Any] | None:
    context_file = Path(os.path.join(workflows, "context.yaml"))
    if context_file.exists():
        return yaml.safe_load(context_file.read_text())
    return None
