from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field

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
    errors: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class BuildResult:
    spec: Spec
    workflow: Workflow
