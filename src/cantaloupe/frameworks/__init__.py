import pluggy

from .hookspec import CantaloupeSpec
from .playwright import PlaywrightJSPlugin

plugin_manager = pluggy.PluginManager("cantaloupe")
plugin_manager.add_hookspecs(CantaloupeSpec)
plugin_manager.register(PlaywrightJSPlugin())
plugin_manager.load_setuptools_entrypoints("cantaloupe")
