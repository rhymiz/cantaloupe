from pathlib import Path

from automate.loaders import load_workflow_context, load_workflows


def test_load_workflow_context() -> None:
    """
    Test that workflow context is loaded correctly
    """
    workflow_path = Path(__file__).parent / "workflows"
    context_data = load_workflow_context(workflow_path)
    assert context_data is not None
    assert context_data["browser"] == "chromium"
    assert context_data["headless"] is True
    assert context_data["base_url"] == "https://www.google.com"


def test_load_workflows() -> None:
    """
    Test that workflows are loaded correctly
    """
    workflow_path = Path(__file__).parent / "workflows"
    workflows = list(load_workflows(workflow_path))  # load_workflows returns a generator
    assert len(workflows) == 1
    workflow = workflows[0]
    assert workflow.name == "Google Search"
    assert workflow.steps[0].action == "go"


def test_load_workflows_with_invalid_yaml() -> None:
    """
    Test that invalid yaml files are ignored
    """
    workflow_path = Path(__file__).parent / "workflows"
    workflow_file = workflow_path / "invalid.yaml"
    workflow_file.touch()
    workflows = list(load_workflows(workflow_path))  # load_workflows returns a generator
    assert len(workflows) == 1
    workflow_file.unlink()
