"""Tornado handlers for the terminal emulator."""
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
from jupyter_server._tz import utcnow
from jupyter_server.auth.utils import warn_disabled_authorization
from jupyter_server.base.handlers import JupyterHandler
from jupyter_server.base.websocket import WebSocketMixin
from terminado.websocket import TermSocket as BaseTermSocket
from tornado import web

from .base import TerminalsMixin

AUTH_RESOURCE = "terminals"


class TermSocket(TerminalsMixin, WebSocketMixin, JupyterHandler, BaseTermSocket):
    """A terminal websocket."""

    auth_resource = AUTH_RESOURCE

    def initialize(self, name, term_manager, **kwargs):
        """Initialize the socket."""
        BaseTermSocket.initialize(self, term_manager, **kwargs)
        TerminalsMixin.initialize(self, name)

    def origin_check(self):
        """Terminado adds redundant origin_check
        Tornado already calls check_origin, so don't do anything here.
        """
        return True

    def get(self, *args, **kwargs):
        """Get the terminal socket."""
        user = self.current_user

        if not user:
            raise web.HTTPError(403)

        # authorize the user.
        if not self.authorizer:
            # Warn if an authorizer is unavailable.
            warn_disabled_authorization()
        elif not self.authorizer.is_authorized(self, user, "execute", self.auth_resource):
            raise web.HTTPError(403)

        if args[0] not in self.term_manager.terminals:
            raise web.HTTPError(404)
        return super().get(*args, **kwargs)

    def on_message(self, message):
        """Handle a socket mesage."""
        super().on_message(message)
        self._update_activity()

    def write_message(self, message, binary=False):
        """Write a message to the socket."""
        super().write_message(message, binary=binary)
        self._update_activity()

    def _update_activity(self):
        self.application.settings["terminal_last_activity"] = utcnow()
        # terminal may not be around on deletion/cull
        if self.term_name in self.terminal_manager.terminals:
            self.terminal_manager.terminals[self.term_name].last_activity = utcnow()
