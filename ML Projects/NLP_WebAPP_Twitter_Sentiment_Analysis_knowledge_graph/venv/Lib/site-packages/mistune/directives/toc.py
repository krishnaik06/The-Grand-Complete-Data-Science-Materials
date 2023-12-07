"""
    TOC directive
    ~~~~~~~~~~~~~

    The TOC directive syntax looks like::

        .. toc:: Title
           :depth: 3

    "Title" and "depth" option can be empty. "depth" is an integer less
    than 6, which defines the max heading level writers want to include
    in TOC.
"""

from .base import Directive


class DirectiveToc(Directive):
    def __init__(self, depth=3):
        self.depth = depth

    def parse(self, block, m, state):
        title = m.group('value')
        depth = None
        options = self.parse_options(m)
        if options:
            depth = dict(options).get('depth')
            if depth:
                try:
                    depth = int(depth)
                except (ValueError, TypeError):
                    return {
                        'type': 'block_error',
                        'raw': 'TOC depth MUST be integer',
                    }

        return {'type': 'toc', 'raw': None, 'params': (title, depth)}

    def reset_toc_state(self, md, s, state):
        state['toc_depth'] = self.depth
        state['toc_headings'] = []
        return s, state

    def register_plugin(self, md):
        md.block.tokenize_heading = record_toc_heading
        md.before_parse_hooks.append(self.reset_toc_state)
        md.before_render_hooks.append(md_toc_hook)

        if md.renderer.NAME == 'html':
            md.renderer.register('theading', render_html_theading)
        elif md.renderer.NAME == 'ast':
            md.renderer.register('theading', render_ast_theading)

    def __call__(self, md):
        self.register_directive(md, 'toc')
        self.register_plugin(md)

        if md.renderer.NAME == 'html':
            md.renderer.register('toc', render_html_toc)
        elif md.renderer.NAME == 'ast':
            md.renderer.register('toc', render_ast_toc)


def record_toc_heading(text, level, state):
    # we will use this method to replace tokenize_heading
    tid = 'toc_' + str(len(state['toc_headings']) + 1)
    state['toc_headings'].append((tid, text, level))
    return {'type': 'theading', 'text': text, 'params': (level, tid)}


def md_toc_hook(md, tokens, state):
    headings = state.get('toc_headings')
    if not headings:
        return tokens

    # add TOC items into the given location
    default_depth = state.get('toc_depth', 3)
    headings = list(_cleanup_headings_text(md.inline, headings, state))
    for tok in tokens:
        if tok['type'] == 'toc':
            params = tok['params']
            depth = params[1] or default_depth
            items = [d for d in headings if d[2] <= depth]
            tok['raw'] = items
    return tokens


def render_ast_toc(items, title, depth):
    return {
        'type': 'toc',
        'items': [list(d) for d in items],
        'title': title,
        'depth': depth,
    }


def render_ast_theading(children, level, tid):
    return {
        'type': 'heading', 'children': children,
        'level': level, 'id': tid,
    }


def render_html_toc(items, title, depth):
    html = '<section class="toc">\n'
    if title:
        html += '<h1>' + title + '</h1>\n'

    return html + render_toc_ul(items) + '</section>\n'


def render_html_theading(text, level, tid):
    tag = 'h' + str(level)
    return '<' + tag + ' id="' + tid + '">' + text + '</' + tag + '>\n'


def extract_toc_items(md, s):
    """Extract TOC headings into list structure of::

        [
          ('toc_1', 'Introduction', 1),
          ('toc_2', 'Install', 2),
          ('toc_3', 'Upgrade', 2),
          ('toc_4', 'License', 1),
        ]

    :param md: Markdown Instance with TOC plugin.
    :param s: text string.
    """
    s, state = md.before_parse(s, {})
    md.block.parse(s, state)
    headings = state.get('toc_headings')
    if not headings:
        return []
    return list(_cleanup_headings_text(md.inline, headings, state))


def render_toc_ul(toc):
    """Render a <ul> table of content HTML. The param "toc" should
    be formatted into this structure::

        [
          (toc_id, text, level),
        ]

    For example::

        [
          ('toc-intro', 'Introduction', 1),
          ('toc-install', 'Install', 2),
          ('toc-upgrade', 'Upgrade', 2),
          ('toc-license', 'License', 1),
        ]
    """
    if not toc:
        return ''

    s = '<ul>\n'
    levels = []
    for k, text, level in toc:
        item = '<a href="#{}">{}</a>'.format(k, text)
        if not levels:
            s += '<li>' + item
            levels.append(level)
        elif level == levels[-1]:
            s += '</li>\n<li>' + item
        elif level > levels[-1]:
            s += '\n<ul>\n<li>' + item
            levels.append(level)
        else:
            last_level = levels.pop()
            while levels:
                last_level = levels.pop()
                if level == last_level:
                    s += '</li>\n</ul>\n</li>\n<li>' + item
                    levels.append(level)
                    break
                elif level > last_level:
                    s += '</li>\n<li>' + item
                    levels.append(last_level)
                    levels.append(level)
                    break
                else:
                    s += '</li>\n</ul>\n'
            else:
                levels.append(level)
                s += '</li>\n<li>' + item

    while len(levels) > 1:
        s += '</li>\n</ul>\n'
        levels.pop()

    return s + '</li>\n</ul>\n'


def _cleanup_headings_text(inline, items, state):
    for item in items:
        text = item[1]
        tokens = inline._scan(text, state, inline.rules)
        text = ''.join(_inline_token_text(tok) for tok in tokens)
        yield item[0], text, item[2]


def _inline_token_text(token):
    tok_type = token[0]
    if tok_type == 'inline_html':
        return ''

    if len(token) == 2:
        return token[1]

    if tok_type in {'image', 'link'}:
        return token[2]

    return ''
