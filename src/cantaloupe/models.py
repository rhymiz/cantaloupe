from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable

from pydantic import BaseModel, Field

from .enums import Action, Browser, ScreenshotOpts, TraceVideoOpts


class Step(BaseModel):
    """Defines an action to be taken as part of a workflow."""

    use: str | None = Field(default=None)
    config: dict[str, Any] = Field(default_factory=dict)
    action: Action
    variables: dict[str, Any] = Field(default_factory=dict)

    class ConfigDict:
        use_enum_values = True


class WorkflowVariable(BaseModel):
    name: str
    type: str = Field(default="string")
    default: Any = Field(default=None)
    required: bool = Field(default=False)

    class ConfigDict:
        use_enum_values = True


class Workflow(BaseModel):
    name: str
    steps: list[Step]
    file_name: str
    file_path: Path | str
    variables: list[WorkflowVariable] = Field(default_factory=list)

    class ConfigDict:
        use_enum_values = True


class ContextAssetOpts(BaseModel):
    trace: TraceVideoOpts = Field(default=TraceVideoOpts.OFF)
    video: TraceVideoOpts = Field(default=TraceVideoOpts.ON)
    screenshot: ScreenshotOpts = Field(default=ScreenshotOpts.ON_FAILURE)

    class ConfigDict:
        use_enum_values = True


class ContextTimeoutOpts(BaseModel):
    script_timeout: int = Field(default=120000)  # 2 minutes
    global_timeout: int = Field(default=3600000)  # 1 hour
    action_timeout: int = Field(default=60000)  # 1 minute
    expect_timeout: int = Field(default=15000)  # 15 seconds
    navigation_timeout: int = Field(default=15000)  # 15 seconds

    class ConfigDict:
        use_enum_values = True


class Context(BaseModel):
    assets: ContextAssetOpts = Field(default_factory=ContextAssetOpts)
    browser: Browser = Field(default=Browser.CHROMIUM)
    retries: int = Field(default=0)
    timeouts: ContextTimeoutOpts = Field(default_factory=ContextTimeoutOpts)
    headless: bool = Field(default=True)
    base_url: str = Field(default=None)
    workflows: Iterable[Workflow] = Field(default_factory=list)
    output_dir: Path = Field(default=None)
    workflow_dir: Path = Field(default=None)

    class ConfigDict:
        use_enum_values = True
