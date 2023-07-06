import argparse
import logging
import os
from dataclasses import dataclass
from pathlib import Path, PosixPath
from typing import Any

import pluggy
from pydantic import Field

from . import hookspecs
from .loaders import load_context, load_workflows
from .logger import get_root_logger
from .plugins import core_error_handling, core_framework

parser = argparse.ArgumentParser(prog="cantaloupe", description="Cantaloupe is a tool for automating web applications.")


@dataclass(frozen=True)
class Config:
    """
    This class represents a configuration file.
    """

    option: argparse.Namespace
    workflow_dir: Path = Field(default=None)

    def has_option(self, option: str) -> bool:
        return option in self.option

    def get_log_level(self) -> int:
        """
        Returns the log level.
        """
        if self.option.debug:
            return logging.DEBUG
        return logging.INFO


@dataclass(frozen=True)
class Result:
    """
    This class represents the result of a built workflow.
    """

    content: str


def _make_path(workflow_path: PosixPath) -> Path:
    """A little hacky, potentially unstable."""
    cwd = Path(os.getcwd())
    if workflow_path == ".":
        workflows = Path(cwd)
    elif "/" not in workflow_path.name:
        workflows = Path(os.path.join(cwd, workflow_path))
    else:
        workflows = Path(workflow_path)
    return workflows


def main(args: tuple[Any]) -> None:
    """
    Main entry point for the Cantaloupe CLI.
    """

    manager = get_plugin_manager()
    manager.hook.cantaloupe_addoption(parser=parser)

    parsed = parser.parse_args(args)

    workflow_dir = _make_path(parsed.workflows)
    config = Config(option=parsed, workflow_dir=workflow_dir)

    logger = get_root_logger(level=config.get_log_level())

    context = load_context(workflows=workflow_dir)
    if context is None:
        logger.error("No context file found.")
        return

    # Add workflows to context
    logger.debug("Loading workflows from %s", workflow_dir)
    context.workflows = list(load_workflows(workflows=workflow_dir))

    logger.debug("Found %s workflow(s)", len(context.workflows))

    logger.debug("Calling setup hooks")
    manager.hook.cantaloupe_setup(config=config, context=context)

    for workflow in context.workflows:
        logger.debug("Building workflow: %s", workflow.name)
        manager.hook.cantaloupe_build_workflow(
            config=config,
            context=context,
            workflow=workflow,
        )

    logger.debug("Calling teardown hooks")
    manager.hook.cantaloupe_teardown(config=config, context=context)


def get_plugin_manager() -> pluggy.PluginManager:
    """
    Returns the plugin manager for cantaloupe.
    """
    manager = pluggy.PluginManager("cantaloupe")
    manager.add_hookspecs(hookspecs)
    manager.load_setuptools_entrypoints("cantaloupe_plugin")
    manager.register(core_framework)
    manager.register(core_error_handling)
    return manager
