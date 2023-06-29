import sys
from pathlib import Path

import pytest

# add src to path so we can import cantaloupe
sys.path.append(str(Path(__file__).parent.parent / "src"))

from cantaloupe.loaders import load_context, load_workflows
from cantaloupe.models import Context


@pytest.fixture(scope="session")
def context() -> Context:
    workflow_path = Path(__file__).parent / "workflows"
    context_data = load_context(workflow_path)
    assert context_data is not None
    workflows = load_workflows(workflow_path)
    return Context(
        **context_data,
        workflows=workflows,
        output_dir=workflow_path,
        workflow_dir=workflow_path,
    )
