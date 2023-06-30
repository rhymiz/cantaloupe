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
from .plugins import core

logging.basicConfig(
    level=logging.INFO,
    format="%(name)s [%(levelname)s] - %(message)s",
)

logger = logging.getLogger("cantaloupe")

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
    context = load_context(workflows=workflow_dir)
    if context is None:
        logger.error("No context file found.")
        return

    # Add workflows to context
    context.workflows = list(load_workflows(workflows=workflow_dir))

    manager.hook.cantaloupe_setup(config=config, context=context)

    manager.hook.cantaloupe_teardown(config=config, context=context)


def get_plugin_manager() -> pluggy.PluginManager:
    """
    Returns the plugin manager for cantaloupe.
    """
    manager = pluggy.PluginManager("cantaloupe")
    manager.add_hookspecs(hookspecs)
    manager.load_setuptools_entrypoints("cantaloupe_plugin")
    manager.register(core)
    return manager
