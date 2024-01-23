from .markdown import Markdown
from .block_parser import BlockParser
from .inline_parser import InlineParser
from .renderers import AstRenderer, HTMLRenderer
from .plugins import PLUGINS
from .util import escape, escape_url, escape_html, unikey


def create_markdown(escape=True, hard_wrap=False, renderer=None, plugins=None):
    """Create a Markdown instance based on the given condition.

    :param escape: Boolean. If using html renderer, escape html.
    :param hard_wrap: Boolean. Break every new line into ``<br>``.
    :param renderer: renderer instance or string of ``html`` and ``ast``.
    :param plugins: List of plugins, string or callable.

    This method is used when you want to re-use a Markdown instance::

        markdown = create_markdown(
            escape=False,
            renderer='html',
            plugins=['url', 'strikethrough', 'footnotes', 'table'],
        )
        # re-use markdown function
        markdown('.... your text ...')
    """
    if renderer is None or renderer == 'html':
        renderer = HTMLRenderer(escape=escape)
    elif renderer == 'ast':
        renderer = AstRenderer()

    if plugins:
        _plugins = []
        for p in plugins:
            if isinstance(p, str):
                _plugins.append(PLUGINS[p])
            else:
                _plugins.append(p)
        plugins = _plugins

    return Markdown(renderer, inline=InlineParser(renderer, hard_wrap=hard_wrap), plugins=plugins)


html = create_markdown(
    escape=False,
    renderer='html',
    plugins=['strikethrough', 'footnotes', 'table'],
)


def markdown(text, escape=True, renderer=None, plugins=None):
    md = create_markdown(escape=escape, renderer=renderer, plugins=plugins)
    return md(text)


__all__ = [
    'Markdown', 'AstRenderer', 'HTMLRenderer',
    'BlockParser', 'InlineParser',
    'escape', 'escape_url', 'escape_html', 'unikey',
    'html', 'create_markdown', 'markdown',
]

__version__ = '2.0.5'
