import argparse
import logging
import os
import typing
from dataclasses import dataclass
from pathlib import Path, PosixPath
from typing import Any

import pluggy
from pydantic import Field

from . import hookspecs
from .loaders import load_context, load_workflows
from .logger import get_root_logger
from .plugins import core_cli, core_error_handling, core_framework

if typing.TYPE_CHECKING:
    from pluggy._hooks import _HookRelay

parser = argparse.ArgumentParser(prog="cantaloupe", description="Cantaloupe is a tool for automating web applications.")


@dataclass(frozen=True)
class Config:
    """
    This class represents a configuration file.
    """

    option: argparse.Namespace
    workflow_dir: Path = Field(default=None)
    pluginmanager: pluggy.PluginManager = Field(default=None)

    def get_log_level(self) -> int:
        """
        Returns the log level.
        """
        if self.option.debug:
            return logging.DEBUG
        return logging.INFO


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


class _Cantaloupe:
    def __init__(self, relay: "_HookRelay", logger: logging.Logger) -> None:
        self.relay = relay
        self.logger = logger

    def setup(self, config: Config, context: Any) -> None:
        self.logger.debug("Calling setup hooks")
        self.relay.cantaloupe_setup(config=config, context=context)

    def teardown(self, config: Config, context: Any) -> None:
        self.logger.debug("Calling teardown hooks")
        self.relay.cantaloupe_teardown(config=config, context=context)

    def build_workflows(self, config: Config, context: Any) -> None:
        for workflow in context.workflows:
            self.logger.debug("Building workflow: %s", workflow.name)
            self.relay.cantaloupe_build_workflow(
                config=config,
                context=context,
                workflow=workflow,
            )


def main(args: tuple[Any]) -> None:
    """
    Main entry point for the Cantaloupe CLI.
    """

    manager = get_plugin_manager()

    # Add all plugin options to parser
    manager.hook.cantaloupe_addoption(parser=parser)

    opts = parser.parse_args(args)
    config = Config(option=opts, workflow_dir=_make_path(opts.workflows))

    logger = get_root_logger(level=config.get_log_level())

    logger.info("Cantaloupe")
    logger.info("Plugins: %s", manager.list_name_plugin())

    context = load_context(workflows=config.workflow_dir)
    if context is None:
        logger.error("No context file found.")
        return

    cantaloupe = _Cantaloupe(manager.hook, logger)

    # Add workflows to context
    logger.debug("Loading workflows from %s", config.workflow_dir)
    context.workflows = list(load_workflows(workflows=config.workflow_dir))

    logger.debug("Found %s workflow(s)", len(context.workflows))

    cantaloupe.setup(config=config, context=context)
    cantaloupe.build_workflows(config=config, context=context)
    cantaloupe.teardown(config=config, context=context)


def get_plugin_manager() -> pluggy.PluginManager:
    """
    Returns the plugin manager for cantaloupe.
    """
    manager = pluggy.PluginManager("cantaloupe")
    manager.add_hookspecs(hookspecs)
    manager.load_setuptools_entrypoints("cantaloupe_plugin")
    manager.register(core_framework)
    manager.register(core_error_handling)
    manager.register(core_cli)
    return manager
