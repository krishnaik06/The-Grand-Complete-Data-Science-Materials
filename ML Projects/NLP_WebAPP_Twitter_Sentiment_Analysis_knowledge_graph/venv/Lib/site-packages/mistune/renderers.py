from .util import escape, escape_html


class BaseRenderer(object):
    NAME = 'base'

    def __init__(self):
        self._methods = {}

    def register(self, name, method):
        self._methods[name] = method

    def _get_method(self, name):
        try:
            return object.__getattribute__(self, name)
        except AttributeError:
            method = self._methods.get(name)
            if not method:
                raise AttributeError('No renderer "{!r}"'.format(name))
            return method

    def finalize(self, data):
        raise NotImplementedError(
            'The renderer needs to implement the finalize method.')


class AstRenderer(BaseRenderer):
    NAME = 'ast'

    def text(self, text):
        return {'type': 'text', 'text': text}

    def link(self, link, children=None, title=None):
        if isinstance(children, str):
            children = [{'type': 'text', 'text': children}]
        return {
            'type': 'link',
            'link': link,
            'children': children,
            'title': title,
        }

    def image(self, src, alt="", title=None):
        return {'type': 'image', 'src': src, 'alt': alt, 'title': title}

    def codespan(self, text):
        return {'type': 'codespan', 'text': text}

    def linebreak(self):
        return {'type': 'linebreak'}

    def inline_html(self, html):
        return {'type': 'inline_html', 'text': html}

    def heading(self, children, level):
        return {'type': 'heading', 'children': children, 'level': level}

    def newline(self):
        return {'type': 'newline'}

    def thematic_break(self):
        return {'type': 'thematic_break'}

    def block_code(self, children, info=None):
        return {
            'type': 'block_code',
            'text': children,
            'info': info
        }

    def block_html(self, children):
        return {'type': 'block_html', 'text': children}

    def list(self, children, ordered, level, start=None):
        token = {
            'type': 'list',
            'children': children,
            'ordered': ordered,
            'level': level,
        }
        if start is not None:
            token['start'] = start
        return token

    def list_item(self, children, level):
        return {'type': 'list_item', 'children': children, 'level': level}

    def _create_default_method(self, name):
        def __ast(children):
            return {'type': name, 'children': children}
        return __ast

    def _get_method(self, name):
        try:
            return super(AstRenderer, self)._get_method(name)
        except AttributeError:
            return self._create_default_method(name)

    def finalize(self, data):
        return list(data)


class HTMLRenderer(BaseRenderer):
    NAME = 'html'
    HARMFUL_PROTOCOLS = {
        'javascript:',
        'vbscript:',
        'data:',
    }

    def __init__(self, escape=True, allow_harmful_protocols=None):
        super(HTMLRenderer, self).__init__()
        self._escape = escape
        self._allow_harmful_protocols = allow_harmful_protocols

    def _safe_url(self, url):
        if self._allow_harmful_protocols is None:
            schemes = self.HARMFUL_PROTOCOLS
        elif self._allow_harmful_protocols is True:
            schemes = None
        else:
            allowed = set(self._allow_harmful_protocols)
            schemes = self.HARMFUL_PROTOCOLS - allowed

        if schemes:
            for s in schemes:
                if url.lower().startswith(s):
                    url = '#harmful-link'
                    break
        return url

    def text(self, text):
        if self._escape:
            return escape(text)
        return escape_html(text)

    def link(self, link, text=None, title=None):
        if text is None:
            text = link

        s = '<a href="' + self._safe_url(link) + '"'
        if title:
            s += ' title="' + escape_html(title) + '"'
        return s + '>' + (text or link) + '</a>'

    def image(self, src, alt="", title=None):
        src = self._safe_url(src)
        alt = escape_html(alt)
        s = '<img src="' + src + '" alt="' + alt + '"'
        if title:
            s += ' title="' + escape_html(title) + '"'
        return s + ' />'

    def emphasis(self, text):
        return '<em>' + text + '</em>'

    def strong(self, text):
        return '<strong>' + text + '</strong>'

    def codespan(self, text):
        return '<code>' + escape(text) + '</code>'

    def linebreak(self):
        return '<br />\n'

    def inline_html(self, html):
        if self._escape:
            return escape(html)
        return html

    def paragraph(self, text):
        return '<p>' + text + '</p>\n'

    def heading(self, text, level):
        tag = 'h' + str(level)
        return '<' + tag + '>' + text + '</' + tag + '>\n'

    def newline(self):
        return ''

    def thematic_break(self):
        return '<hr />\n'

    def block_text(self, text):
        return text

    def block_code(self, code, info=None):
        html = '<pre><code'
        if info is not None:
            info = info.strip()
        if info:
            lang = info.split(None, 1)[0]
            lang = escape_html(lang)
            html += ' class="language-' + lang + '"'
        return html + '>' + escape(code) + '</code></pre>\n'

    def block_quote(self, text):
        return '<blockquote>\n' + text + '</blockquote>\n'

    def block_html(self, html):
        if not self._escape:
            return html + '\n'
        return '<p>' + escape(html) + '</p>\n'

    def block_error(self, html):
        return '<div class="error">' + html + '</div>\n'

    def list(self, text, ordered, level, start=None):
        if ordered:
            html = '<ol'
            if start is not None:
                html += ' start="' + str(start) + '"'
            return html + '>\n' + text + '</ol>\n'
        return '<ul>\n' + text + '</ul>\n'

    def list_item(self, text, level):
        return '<li>' + text + '</li>\n'

    def finalize(self, data):
        return ''.join(data)
