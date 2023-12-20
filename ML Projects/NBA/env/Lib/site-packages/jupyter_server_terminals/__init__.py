from ._version import __version__  # noqa:F401

try:
    from jupyter_server._version import version_info
except ModuleNotFoundError:
    raise ModuleNotFoundError("Jupyter Server must be installed to use this extension.") from None

if int(version_info[0]) < 2:  # type:ignore
    raise RuntimeError("Jupyter Server Terminals requires Jupyter Server 2.0+")

from .app import TerminalsExtensionApp


def _jupyter_server_extension_points():  # pragma: no cover
    return [
        {
            "module": "jupyter_server_terminals.app",
            "app": TerminalsExtensionApp,
        },
    ]
