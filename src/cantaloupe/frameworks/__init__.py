import pluggy

from .hookspec import CantaloupeSpec
from .playwright import PlaywrightPlugin

hookimpl = pluggy.HookimplMarker("cantaloupe")


pm = pluggy.PluginManager("cantaloupe")
pm.add_hookspecs(CantaloupeSpec)
pm.register(PlaywrightPlugin())
