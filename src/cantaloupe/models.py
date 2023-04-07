from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable, List, Union

from pydantic import BaseModel, Field

from .enums import Action, Browser, ScreenshotOpts, TraceVideoOpts


class Step(BaseModel):
    """
    A step in a workflow.

    Describes an action to be taken during workflow execution.
    """

    use: Union[str, None] = Field(default=None)
    input: str = Field(default=None)
    input_options: Union[dict[str, Any], List[Any]] = Field(default_factory=dict)
    action: Action
    selector: str = Field(default=None)
    selector_options: dict[str, Any] = Field(default_factory=dict)
    template: str = Field(default=None)
    variables: dict[str, Any] = Field(default_factory=dict)

    class Config:
        use_enum_values = True


class WorkflowVariable(BaseModel):
    name: str
    default: Any = Field(default=None)
    description: str = Field(default=None)


class Workflow(BaseModel):
    name: str = Field(max_length=55)
    steps: list[Step]
    file_name: str = Field(default=None)
    variables: list[WorkflowVariable] = Field(default=[])


class ContextAssetConfig(BaseModel):
    trace: TraceVideoOpts = Field(default=TraceVideoOpts.OFF)
    video: TraceVideoOpts = Field(default=TraceVideoOpts.ON)
    screenshot: ScreenshotOpts = Field(default=ScreenshotOpts.ON_FAILURE)


class ContextTimeoutOpts(BaseModel):
    script_timeout: int = Field(default=120000)  # 2 minutes
    global_timeout: int = Field(default=3600000)  # 1 hour
    action_timeout: int = Field(default=60000)  # 1 minute
    expect_timeout: int = Field(default=15000)  # 15 seconds
    navigation_timeout: int = Field(default=15000)  # 15 seconds


class Context(BaseModel):
    assets: ContextAssetConfig = Field(default_factory=ContextAssetConfig)
    browser: Browser = Field(default=Browser.CHROMIUM)
    retries: int = Field(default=0)
    timeouts: ContextTimeoutOpts = Field(default_factory=ContextTimeoutOpts)
    headless: bool = Field(default=True)
    base_url: str = Field(default=None)
    workflows: Iterable[Workflow] = Field(default_factory=list)
    output_dir: Path = Field(default=None)
    workflow_dir: Path = Field(default=None)

    class Config:
        use_enum_values = True
