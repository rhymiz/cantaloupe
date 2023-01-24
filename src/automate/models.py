from __future__ import annotations

from typing import Any, Union

from jinja2 import Template
from pydantic import BaseModel, Field

from .enums import Action, Browser
from .generation.template import get_template_from_fs, get_template_from_string


class Step(BaseModel):
    use: Union[str, None] = Field(default=None)
    input: Union[str, list[Union[str, int, dict[str, Any]]], dict[str, Any]] = Field(
        default=None
    )
    action: Action
    selector: Union[str, dict[str, Any], None] = Field(default=None)
    template: Union[str, None]

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

        if self.action in Action.page_level():
            template_name = "page.txt"
        elif self.action == Action.CODE:
            template_name = "page_code.txt"
        elif self.action == Action.SELECT:
            template_name = "page_select.txt"
        elif self.action == Action.SET_VARIABLE:
            template_name = "page_set_var.txt"
        elif self.action == Action.USE_VARIABLE:
            template_name = "page_use_var.txt"
        elif self.action in Action.recommended():
            template_name = "page_builtins.txt"
        else:
            template_name = "page_locator.txt"
        return template_name

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


class WorkflowConfiguration(BaseModel):
    retries: int = Field(default=0)
    headless: bool = Field(default=True)
