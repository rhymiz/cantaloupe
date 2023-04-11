from __future__ import annotations

from dataclasses import dataclass, field
from typing import NewType

from pydantic import BaseModel

from ..models import Workflow


class File(BaseModel):
    name: str
    path: str
    content: str


Spec = NewType("Spec", File)
Config = NewType("Config", File)


@dataclass(frozen=True)
class GeneratorResult:
    files: list[File]
    errors: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class BuildResult:
    spec: Spec
    workflow: Workflow
