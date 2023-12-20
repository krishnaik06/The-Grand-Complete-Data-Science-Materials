"""Base classes."""
from jupyter_server.extension.handler import ExtensionHandlerMixin


class TerminalsMixin(ExtensionHandlerMixin):
    """An extension mixin for terminals."""

    @property
    def terminal_manager(self):
        return self.settings["terminal_manager"]  # type:ignore[attr-defined]
