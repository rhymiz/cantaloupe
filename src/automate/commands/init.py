from __future__ import annotations

import pathlib

import click

_INITIAL_CONTEXT = """
device: "Desktop Chrome"
browser: "chromium"
headless: true
base_url: https://www.google.com
assets:
  trace: 'on'
  video: 'on'
  screenshot: 'on'
timeouts:
  action_timeout: 60000
  global_timeout: 60000
  script_timeout: 60000
  expect_timeout: 15000
  navigation_timeout: 15000
"""

_INITIAL_WORKFLOW = """
name: "Google Search"
steps:
  - action: goto
    input: "https://www.google.com"
  - action: type
    selector: "input[name=q]"
    input: "Hello World"
  - action: click
    selector: "input[name=btnK]"
"""


@click.command()
def init() -> None:
    pathlib.Path("workflows").mkdir(exist_ok=True)

    context_path = pathlib.Path("workflows/context.yaml")
    if not context_path.exists():
        with open(context_path, "w") as f:
            f.write(_INITIAL_CONTEXT)

    workflow_path = pathlib.Path("workflows/workflow_example.yaml")
    if not workflow_path.exists():
        with open(workflow_path, "w") as f:
            f.write(_INITIAL_WORKFLOW)
