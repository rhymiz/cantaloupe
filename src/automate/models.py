from __future__ import annotations

from typing import Any, List, Union

from jinja2 import Template
from pydantic import BaseModel, Field

from .enums import Action, Browser
from .generation.template import get_template_from_fs, get_template_from_string


class Step(BaseModel):
    use: Union[str, None] = Field(default=None)
    input: str = Field(default=None)
    input_options: Union[dict[str, Any], List[Any]] = Field(default_factory=dict)
    action: Action
    selector: str = Field(default=None)
    selector_options: dict[str, Any] = Field(default_factory=dict)
    template: str = Field(default=None)
    variables: dict[str, Any] = Field(default_factory=dict)

    @property
    def template_object(self) -> Template:
        """Return a jinja Template object that can be rendered"""
        if self.template:
            return get_template_from_string(self.template)
        else:
            return get_template_from_fs(self._template_name)

    @template_object.setter
    def template_object(self, value: Any) -> None:
        raise AttributeError("cannot set value for Step.template_object")

    @property
    def _template_name(self) -> str:
        """select a default template based on action"""
        prefix = "action_"
        return f"{prefix}{self.action}.txt"

    class Config:
        use_enum_values = True


class WorkflowVariable(BaseModel):
    name: str
    default: Any = Field(default=None)
    description: str = Field(default=None)


class Workflow(BaseModel):
    name: str
    steps: list[Step]
    browser: Browser = Field(default=Browser.CHROMIUM.value)
    base_url: str = Field(default=None)
    variables: list[WorkflowVariable] = Field(default=[])
    configuration: WorkflowConfiguration = Field(
        default={
            "retries": 0,
            "headless": True,
        }
    )

    class Config:
        use_enum_values = True


class WorkflowConfiguration(BaseModel):
    retries: int = Field(default=0)
    headless: bool = Field(default=True)
