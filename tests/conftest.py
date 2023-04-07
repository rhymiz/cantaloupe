import sys
from pathlib import Path

import pytest

# add src to path so we can import automate
sys.path.append(str(Path(__file__).parent.parent / "src"))

from automate.loaders import load_workflow_context, load_workflows
from automate.models import Context


@pytest.fixture(scope="session")
def context() -> Context:
    workflow_path = Path(__file__).parent / "workflows"
    context_data = load_workflow_context(workflow_path)
    workflows = load_workflows(workflow_path)
    return Context(
        **context_data,
        workflows=workflows,
        output_dir=workflow_path,
        workflow_dir=workflow_path,
    )
