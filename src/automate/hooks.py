from __future__ import annotations

import typing
from abc import ABC
from collections import defaultdict
from unicodedata import name

if typing.TYPE_CHECKING:
    from .models import Step, Workflow


class _HookStep:
    AFTER_STEP = "after_step_hook"
    BEFORE_STEP = "before_step_hook"
    AFTER_WORKFLOW = "after_workflow_hook"
    BEFORE_WORKFLOW = "before_workflow_hook"


_hook_names: list[str] = [
    _HookStep.AFTER_STEP,
    _HookStep.BEFORE_STEP,
    _HookStep.AFTER_WORKFLOW,
    _HookStep.BEFORE_WORKFLOW,
]


class HookRegistry(type):
    hooks: dict[str, list[typing.Type["BaseHook"]]] = {
        _HookStep.AFTER_STEP: [],
        _HookStep.BEFORE_STEP: [],
        _HookStep.AFTER_WORKFLOW: [],
        _HookStep.BEFORE_WORKFLOW: [],
    }

    def __init__(cls, name: str, bases, attrs) -> None:
        ignored = ["BaseHook"]
        if name not in ignored:
            if hasattr(cls, "Meta"):
                for hook_name in _hook_names:
                    if hasattr(cls, hook_name):
                        HookRegistry.hooks[hook_name].append(cls)  # type:ignore


class BaseHook(metaclass=HookRegistry):
    class Meta:
        name: str
        version: str


class HookManager:
    def __init__(self) -> None:
        self._hooks = HookRegistry.hooks

    def call_after_step_hooks(self, step: "Step") -> None:
        [hook.after_step_hook(step) for hook in self._hooks[_HookStep.AFTER_STEP]]  # type: ignore

    def call_before_step_hooks(self, step: "Step") -> None:
        [hook.before_step_hook(step) for hook in self._hooks[_HookStep.BEFORE_STEP]]  # type: ignore

    def call_after_workflow_hooks(self, workflow: "Workflow") -> None:
        [
            hook.after_workflow_hook(workflow)  # type: ignore
            for hook in self._hooks[_HookStep.AFTER_WORKFLOW]
        ]

    def call_before_workflow_hooks(self, workflow: "Workflow") -> None:
        [
            hook.before_workflow_hook(workflow)  # type: ignore
            for hook in self._hooks[_HookStep.BEFORE_WORKFLOW]
        ]
