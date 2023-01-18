from __future__ import annotations

from typing import Any, Union

from pydantic import BaseModel, Field

from .enums import Browser, Event


class Step(BaseModel):
    event: Event
    input: Union[str, dict[str, Any], list[Any]] = Field(default=None)
    selector: Union[str, dict[str, Any], None] = Field(default=None)

    class Config:
        use_enum_values = True


class Workflow(BaseModel):
    name: str
    steps: list[Step]
    browser: Browser = Field(default=Browser.CHROMIUM)

    class Config:
        use_enum_values = True
