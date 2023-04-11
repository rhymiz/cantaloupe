import pluggy

from .hookspec import CantaloupeSpec
from .playwright import PlaywrightPlugin

plugin_manager = pluggy.PluginManager("cantaloupe")
plugin_manager.add_hookspecs(CantaloupeSpec)
plugin_manager.register(PlaywrightPlugin())
plugin_manager.load_setuptools_entrypoints("cantaloupe")
