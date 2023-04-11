from __future__ import annotations

from dataclasses import dataclass, field

from pydantic import BaseModel

from .models import Workflow


class File(BaseModel):
    name: str
    path: str
    content: str


class Spec(File):
    """
    This class represents a spec file.
    """

    pass


class Config(File):
    """
    This class represents a configuration file.
    """

    pass


@dataclass(frozen=True)
class GeneratorResult:
    files: list[File]
    errors: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class BuildResult:
    spec: Spec
    workflow: Workflow
