from argparse import ArgumentParser
from typing import Any, Callable, TypeVar, cast

import pluggy

F = TypeVar("F", bound=Callable[..., Any])

hookspec = cast(Callable[[F], F], pluggy.HookspecMarker("cantaloupe"))


@hookspec
def cantaloupe_addoption(parser: ArgumentParser) -> None:
    """
    Called to add arguments to the parser.

    :param parser: the parser to add arguments to
    :type parser: argparse.ArgumentParser
    :return:
    :rtype:
    """


@hookspec
def cantaloupe_setup(config, context) -> None:
    """
    Called before the build process starts.
    """


@hookspec
def cantaloupe_teardown(config, context) -> None:
    """
    Called after the build process ends.
    """
