""" tornado handler for managing and communicating with language servers
"""
from typing import Optional, Text

from jupyter_server.base.handlers import JupyterHandler
from jupyter_server.base.zmqhandlers import WebSocketHandler, WebSocketMixin
from jupyter_server.utils import url_path_join as ujoin

from .manager import LanguageServerManager
from .schema import SERVERS_RESPONSE
from .specs.utils import censored_spec


class BaseHandler(JupyterHandler):
    manager = None  # type: LanguageServerManager

    def initialize(self, manager: LanguageServerManager):
        self.manager = manager


class LanguageServerWebSocketHandler(  # type: ignore
    WebSocketMixin, WebSocketHandler, BaseHandler
):
    """Setup tornado websocket to route to language server sessions"""

    language_server = None  # type: Optional[Text]

    async def open(self, language_server):
        await self.manager.ready()
        self.language_server = language_server
        self.manager.subscribe(self)
        self.log.debug("[{}] Opened a handler".format(self.language_server))
        super().open()

    async def on_message(self, message):
        self.log.debug("[{}] Handling a message".format(self.language_server))
        await self.manager.on_client_message(message, self)

    def on_close(self):
        self.manager.unsubscribe(self)
        self.log.debug("[{}] Closed a handler".format(self.language_server))


class LanguageServersHandler(BaseHandler):
    """Reports the status of all current servers

    Response should conform to schema in schema/servers.schema.json
    """

    validator = SERVERS_RESPONSE

    def initialize(self, *args, **kwargs):
        super().initialize(*args, **kwargs)

    async def get(self):
        """finish with the JSON representations of the sessions"""
        await self.manager.ready()

        response = {
            "version": 2,
            "sessions": {
                language_server: session.to_json()
                for language_server, session in self.manager.sessions.items()
            },
            "specs": {
                key: censored_spec(spec)
                for key, spec in self.manager.all_language_servers.items()
            },
        }

        errors = list(self.validator.iter_errors(response))

        if errors:  # pragma: no cover
            self.log.warning("{} validation errors: {}".format(len(errors), errors))

        self.finish(response)


def add_handlers(nbapp):
    """Add Language Server routes to the notebook server web application"""
    lsp_url = ujoin(nbapp.base_url, "lsp")
    re_langservers = "(?P<language_server>.*)"

    opts = {"manager": nbapp.language_server_manager}

    nbapp.web_app.add_handlers(
        ".*",
        [
            (ujoin(lsp_url, "status"), LanguageServersHandler, opts),
            (
                ujoin(lsp_url, "ws", re_langservers),
                LanguageServerWebSocketHandler,
                opts,
            ),
        ],
    )
