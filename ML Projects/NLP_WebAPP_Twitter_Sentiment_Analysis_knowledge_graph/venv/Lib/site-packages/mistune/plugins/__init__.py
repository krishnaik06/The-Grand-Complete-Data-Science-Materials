from .abbr import plugin_abbr
from .def_list import plugin_def_list
from .extra import plugin_strikethrough, plugin_url
from .footnotes import plugin_footnotes
from .table import plugin_table
from .task_lists import plugin_task_lists

PLUGINS = {
    "url": plugin_url,
    "strikethrough": plugin_strikethrough,
    "footnotes": plugin_footnotes,
    "table": plugin_table,
    "task_lists": plugin_task_lists,
    "def_list": plugin_def_list,
    "abbr": plugin_abbr,
}

__all__ = [
    "PLUGINS",
    "plugin_url",
    "plugin_strikethrough",
    "plugin_footnotes",
    "plugin_table",
    "plugin_abbr",
]
