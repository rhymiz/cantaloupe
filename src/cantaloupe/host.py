import argparse
import logging
import os
from dataclasses import dataclass
from pathlib import Path, PosixPath

import pluggy

from . import hookspecs
from .loaders import load_context, load_workflows
from .models import Context
from .plugins import default

logging.basicConfig(
    level=logging.INFO,
    format="%(name)s [%(levelname)s] - %(message)s",
)

logger = logging.getLogger("cantaloupe")

parser = argparse.ArgumentParser(
    prog="cantaloupe",
    description="Cantaloupe is a tool for automating web applications."
)


@dataclass(frozen=True)
class CantaloupeConfig:
    """
    This class represents a configuration file.
    """

    option: argparse.Namespace

    def has_option(self, option: str) -> bool:
        return option in self.option


def _make_path(workflow_path: PosixPath) -> Path:
    if workflow_path == ".":
        workflows = Path(os.getcwd())
    elif "/" not in workflow_path.name:
        workflows = Path(os.path.join(os.getcwd(), workflow_path))
    else:
        workflows = Path(workflow_path)
    return workflows


def main():
    """
    Main entry point for the cantaloupe CLI.

    :return:
    :rtype:
    """

    manager = get_plugin_manager()
    manager.hook.cantaloupe_addoption(parser=parser)

    args = parser.parse_args()
    config = CantaloupeConfig(option=args)

    workflow_directory = _make_path(args.workflows)

    context_data = load_context(workflows=workflow_directory)
    if context_data is None:
        logger.error("No context file found.")
        return

    context_data["workflows"] = list(load_workflows(workflows=workflow_directory))
    context = Context(**context_data)

    manager.hook.cantaloupe_setup(config=config, context=context)

    manager.hook.cantaloupe_teardown(config=config, context=context)


def get_plugin_manager() -> pluggy.PluginManager:
    """
    Returns the plugin manager for cantaloupe.
    """
    manager = pluggy.PluginManager("cantaloupe")
    manager.add_hookspecs(hookspecs)
    manager.register(default, name="cantaloupe-core")
    manager.load_setuptools_entrypoints("cantaloupe_plugin")
    return manager
