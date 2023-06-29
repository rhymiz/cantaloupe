from pathlib import Path

import pytest

from cantaloupe.loaders import load_context, load_workflows
from cantaloupe.models import Context


@pytest.fixture(scope="session")
def context() -> Context:
    workflow_path = Path(__file__).parent / "workflows"
    context = load_context(workflow_path)
    assert context is not None
    workflows = load_workflows(workflow_path)
    context.workflows = list(workflows)
    return context
