import re
from .scanner import ScannerParser
from .util import PUNCTUATION, ESCAPE_TEXT, escape_url, unikey

HTML_TAGNAME = r'[A-Za-z][A-Za-z0-9-]*'
HTML_ATTRIBUTES = (
    r'(?:\s+[A-Za-z_:][A-Za-z0-9_.:-]*'
    r'(?:\s*=\s*(?:[^ "\'=<>`]+|\'[^\']*?\'|"[^\"]*?"))?)*'
)
ESCAPE_CHAR = re.compile(r'\\([' + PUNCTUATION + r'])')
LINK_TEXT = r'(?:\[(?:\\.|[^\[\]\\])*\]|\\.|`[^`]*`|[^\[\]\\`])*?'
LINK_LABEL = r'(?:[^\\\[\]]|' + ESCAPE_TEXT + r'){0,1000}'


class InlineParser(ScannerParser):
    ESCAPE = ESCAPE_TEXT

    #: link or email syntax::
    #:
    #: <https://example.com>
    AUTO_LINK = (
        r'(?<!\\)(?:\\\\)*<([A-Za-z][A-Za-z0-9+.-]{1,31}:'
        r"[^ <>]*?|[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Za-z0-9]"
        r'(?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?'
        r'(?:\.[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?)*)>'
    )

    #: link or image syntax::
    #:
    #: [text](/link "title")
    #: ![alt](/src "title")
    STD_LINK = (
        r'!?\[(' + LINK_TEXT + r')\]\(\s*'

        r'(<(?:\\[<>]?|[^\s<>\\])*>|'
        r'(?:\\[()]?|\([^\s\x00-\x1f\\]*\)|[^\s\x00-\x1f()\\])*?)'

        r'(?:\s+('
        r'''"(?:\\"?|[^"\\])*"|'(?:\\'?|[^'\\])*'|\((?:\\\)?|[^)\\])*\)'''
        r'))?\s*\)'
    )

    #: Get link from references. References are defined in DEF_LINK in blocks.
    #: The syntax looks like::
    #:
    #:    [an example][id]
    #:
    #:    [id]: https://example.com "optional title"
    REF_LINK = (
        r'!?\[(' + LINK_TEXT + r')\]'
        r'\[(' + LINK_LABEL + r')\]'
    )

    #: Simple form of reference link::
    #:
    #:    [an example]
    #:
    #:    [an example]: https://example.com "optional title"
    REF_LINK2 = r'!?\[(' + LINK_LABEL + r')\]'

    #: emphasis and strong * or _::
    #:
    #:    *emphasis*  **strong**
    #:    _emphasis_  __strong__
    ASTERISK_EMPHASIS = (
        r'(\*{1,2})(?=[^\s*])('
        r'(?:(?:(?<!\\)(?:\\\\)*\*)|[^*])+?'
        r')(?<!\\)\1'
    )
    UNDERSCORE_EMPHASIS = (
        r'\b(_{1,2})(?=[^\s_])([\s\S]*?'
        r'(?:' + ESCAPE_TEXT + r'|[^\s_]))\1'
        r'(?!_|[^\s' + PUNCTUATION + r'])\b'
    )

    #: codespan with `::
    #:
    #:    `code`
    CODESPAN = (
        r'(?<!\\|`)(?:\\\\)*(`+)(?!`)([\s\S]+?)(?<!`)\1(?!`)'
    )

    #: linebreak leaves two spaces at the end of line
    LINEBREAK = r'(?:\\| {2,})\n(?!\s*$)'

    INLINE_HTML = (
        r'(?<!\\)<' + HTML_TAGNAME + HTML_ATTRIBUTES + r'\s*/?>|'  # open tag
        r'(?<!\\)</' + HTML_TAGNAME + r'\s*>|'  # close tag
        r'(?<!\\)<!--(?!>|->)(?:(?!--)[\s\S])+?(?<!-)-->|'  # comment
        r'(?<!\\)<\?[\s\S]+?\?>|'
        r'(?<!\\)<![A-Z][\s\S]+?>|'  # doctype
        r'(?<!\\)<!\[CDATA[\s\S]+?\]\]>'  # cdata
    )

    RULE_NAMES = (
        'escape', 'inline_html', 'auto_link',
        'std_link', 'ref_link', 'ref_link2',
        'asterisk_emphasis', 'underscore_emphasis',
        'codespan', 'linebreak',
    )

    def __init__(self, renderer, hard_wrap=False):
        super(InlineParser, self).__init__()
        if hard_wrap:
            #: every new line becomes <br>
            self.LINEBREAK = r' *\n(?!\s*$)'
        self.renderer = renderer
        rules = list(self.RULE_NAMES)
        rules.remove('ref_link')
        rules.remove('ref_link2')
        self.ref_link_rules = rules

    def parse_escape(self, m, state):
        text = m.group(0)[1:]
        return 'text', text

    def parse_auto_link(self, m, state):
        if state.get('_in_link'):
            return 'text', m.group(0)

        text = m.group(1)
        schemes = ('mailto:', 'http://', 'https://')
        if '@' in text and not text.lower().startswith(schemes):
            link = 'mailto:' + text
        else:
            link = text
        return 'link', escape_url(link), text

    def parse_std_link(self, m, state):
        line = m.group(0)
        text = m.group(1)
        link = ESCAPE_CHAR.sub(r'\1', m.group(2))
        if link.startswith('<') and link.endswith('>'):
            link = link[1:-1]

        title = m.group(3)
        if title:
            title = ESCAPE_CHAR.sub(r'\1', title[1:-1])

        if line[0] == '!':
            return 'image', escape_url(link), text, title

        return self.tokenize_link(line, link, text, title, state)

    def parse_ref_link(self, m, state):
        line = m.group(0)
        text = m.group(1)
        key = unikey(m.group(2) or text)
        def_links = state.get('def_links')
        if not def_links or key not in def_links:
            return list(self._scan(line, state, self.ref_link_rules))

        link, title = def_links.get(key)
        link = ESCAPE_CHAR.sub(r'\1', link)
        if title:
            title = ESCAPE_CHAR.sub(r'\1', title)

        if line[0] == '!':
            return 'image', escape_url(link), text, title

        return self.tokenize_link(line, link, text, title, state)

    def parse_ref_link2(self, m, state):
        return self.parse_ref_link(m, state)

    def tokenize_link(self, line, link, text, title, state):
        if state.get('_in_link'):
            return 'text', line
        state['_in_link'] = True
        text = self.render(text, state)
        state['_in_link'] = False
        return 'link', escape_url(link), text, title

    def parse_asterisk_emphasis(self, m, state):
        return self.tokenize_emphasis(m, state)

    def parse_underscore_emphasis(self, m, state):
        return self.tokenize_emphasis(m, state)

    def tokenize_emphasis(self, m, state):
        marker = m.group(1)
        text = m.group(2)
        if len(marker) == 1:
            return 'emphasis', self.render(text, state)
        return 'strong', self.render(text, state)

    def parse_codespan(self, m, state):
        code = re.sub(r'[ \n]+', ' ', m.group(2).strip())
        return 'codespan', code

    def parse_linebreak(self, m, state):
        return 'linebreak',

    def parse_inline_html(self, m, state):
        html = m.group(0)
        if html.startswith('<a '):
            state['_in_link'] = True
        if html.startswith('</a>'):
            state['_in_link'] = False
        return 'inline_html', html

    def parse_text(self, text, state):
        return 'text', text

    def parse(self, s, state, rules=None):
        if rules is None:
            rules = self.rules

        tokens = (
            self.renderer._get_method(t[0])(*t[1:])
            for t in self._scan(s, state, rules)
        )
        return tokens

    def render(self, s, state, rules=None):
        tokens = self.parse(s, state, rules)
        return self.renderer.finalize(tokens)

    def __call__(self, s, state):
        return self.render(s, state)
