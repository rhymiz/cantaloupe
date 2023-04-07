from __future__ import annotations

from dataclasses import dataclass, field
from typing import NewType

from ..models import Workflow


@dataclass(frozen=False)
class File:
    name: str
    path: str
    content: str


Spec = NewType("Spec", File)


@dataclass(frozen=True)
class GeneratorResult:
    files: list[File]
    errors: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class BuildResult:
    spec: Spec
    workflow: Workflow
