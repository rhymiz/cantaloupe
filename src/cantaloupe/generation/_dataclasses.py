from __future__ import annotations

from dataclasses import dataclass

from ..models import Workflow


@dataclass(frozen=False)
class Spec:
    name: str
    path: str
    content: str


@dataclass(frozen=True)
class GeneratorResult:
    specs: list[Spec]
    config: str
    errors: list[str] = dataclass.field(default_factory=list)


@dataclass(frozen=True)
class BuildResult:
    spec: Spec
    workflow: Workflow
