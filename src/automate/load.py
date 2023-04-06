from __future__ import annotations

import os
import pathlib
from typing import Any

import yaml

from .models import Workflow


def load_workflows(workflows: pathlib.Path) -> list[Workflow]:
    """
    loads all workflows from a given directory.
    :param workflows: directory containing the workflows
    :return: list of workflows


    Note: Workflow files must be named workflow_*.yaml
    """
    return [
        Workflow(**yaml.safe_load(workflow.read_text()), file_name=workflow.name)
        for workflow in pathlib.Path(workflows).glob("*.yaml")
        if workflow.is_file() and workflow.name.startswith("workflow_")
    ]


def load_workflow_context(workflows: pathlib.Path) -> dict[str, Any] | None:
    context_file = pathlib.Path(os.path.join(workflows, "context.yaml"))
    if context_file.exists():
        return yaml.safe_load(context_file.read_text())
    return None
