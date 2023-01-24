from __future__ import annotations

from typing import Any, Union

from pydantic import BaseModel, Field

from .enums import Action, Browser


class WorkflowConfiguration(BaseModel):
    retries: int = Field(default=0)
    headless: bool = Field(default=True)


class Step(BaseModel):
    use: Union[str, None] = Field(default=None)
    input: Union[str, list[Union[str, int, dict[str, Any]]], dict[str, Any]] = Field(
        default=None
    )
    action: Action
    selector: Union[str, dict[str, Any], None] = Field(default=None)
    template: Union[str, None]

    class Config:
        use_enum_values = True


class Workflow(BaseModel):
    name: str
    steps: list[Step]
    browser: Browser = Field(default=Browser.CHROMIUM.value)
    base_url: str = Field(default=None)
    configuration: WorkflowConfiguration = Field(
        default={
            "retries": 0,
            "headless": True,
        }
    )

    class Config:
        use_enum_values = True
