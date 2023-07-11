import typing
from argparse import ArgumentParser
from typing import Any, Callable, TypeVar, cast

import pluggy

if typing.TYPE_CHECKING:
    from .models import Step, Workflow, Config, Context

F = TypeVar("F", bound=Callable[..., Any])

hookspec = cast(Callable[[F], F], pluggy.HookspecMarker("cantaloupe"))


@hookspec
def cantaloupe_addoption(parser: ArgumentParser) -> None:
    """
    Called to add arguments to the argument parser.

    :param parser: the parser to add arguments to
    :type parser: argparse.ArgumentParser
    :return:
    :rtype:
    """


@hookspec
def cantaloupe_setup(config: "Config", context: "Context") -> None:
    """
    Called before the build process starts.
    """


@hookspec
def cantaloupe_build_workflow(
    config: "Config",
    context: "Context",
    workflow: "Workflow",
) -> None:
    """
    Called during the build process for each workflow.
    """


@hookspec
def cantaloupe_teardown(config: "Config", context: "Context") -> None:
    """
    Called after the build process ends.
    """


@hookspec
def cantaloupe_resolve_step_variables(
    workflow: "Workflow",
    step: "Step",
) -> "Step":
    """
    Called to resolve variables for a given step.
    """


@hookspec
def cantaloupe_validate_step_imports(
    index: int,
    step: "Step",
    workflow: "Workflow",
) -> None:
    """
    Called to validate an import step.
    Should raise ValidationError if the step is invalid.
    """
