import re
from ..inline_parser import LINK_LABEL
from ..util import unikey

__all__ = ['plugin_footnotes']

#: inline footnote syntax looks like::
#:
#:    [^key]
INLINE_FOOTNOTE_PATTERN = r'\[\^(' + LINK_LABEL + r')\]'

#: define a footnote item like::
#:
#:    [^key]: paragraph text to describe the note
DEF_FOOTNOTE = re.compile(
    r'( {0,3})\[\^(' + LINK_LABEL + r')\]:[ \t]*('
    r'[^\n]*\n+'
    r'(?:\1 {1,3}(?! )[^\n]*\n+)*'
    r')'
)


def parse_inline_footnote(inline, m, state):
    key = unikey(m.group(1))
    def_footnotes = state.get('def_footnotes')
    if not def_footnotes or key not in def_footnotes:
        return 'text', m.group(0)

    index = state.get('footnote_index', 0)
    index += 1
    state['footnote_index'] = index
    state['footnotes'].append(key)
    return 'footnote_ref', key, index


def parse_def_footnote(block, m, state):
    key = unikey(m.group(2))
    if key not in state['def_footnotes']:
        state['def_footnotes'][key] = m.group(3)


def parse_footnote_item(block, k, i, state):
    def_footnotes = state['def_footnotes']
    text = def_footnotes[k]

    stripped_text = text.strip()
    if '\n' not in stripped_text:
        children = [{'type': 'paragraph', 'text': stripped_text}]
    else:
        lines = text.splitlines()
        for second_line in lines[1:]:
            if second_line:
                break

        spaces = len(second_line) - len(second_line.lstrip())
        pattern = re.compile(r'^ {' + str(spaces) + r',}', flags=re.M)
        text = pattern.sub('', text)
        children = block.parse_text(text, state)
        if not isinstance(children, list):
            children = [children]

    return {
        'type': 'footnote_item',
        'children': children,
        'params': (k, i)
    }


def md_footnotes_hook(md, result, state):
    footnotes = state.get('footnotes')
    if not footnotes:
        return result

    children = [
        parse_footnote_item(md.block, k, i + 1, state)
        for i, k in enumerate(footnotes)
    ]
    tokens = [{'type': 'footnotes', 'children': children}]
    output = md.block.render(tokens, md.inline, state)
    return result + output


def render_ast_footnote_ref(key, index):
    return {'type': 'footnote_ref', 'key': key, 'index': index}


def render_ast_footnote_item(children, key, index):
    return {
        'type': 'footnote_item',
        'children': children,
        'key': key,
        'index': index,
    }


def render_html_footnote_ref(key, index):
    i = str(index)
    html = '<sup class="footnote-ref" id="fnref-' + i + '">'
    return html + '<a href="#fn-' + i + '">' + i + '</a></sup>'


def render_html_footnotes(text):
    return (
        '<section class="footnotes">\n<ol>\n'
        + text +
        '</ol>\n</section>\n'
    )


def render_html_footnote_item(text, key, index):
    i = str(index)
    back = '<a href="#fnref-' + i + '" class="footnote">&#8617;</a>'

    text = text.rstrip()
    if text.endswith('</p>'):
        text = text[:-4] + back + '</p>'
    else:
        text = text + back
    return '<li id="fn-' + i + '">' + text + '</li>\n'


def plugin_footnotes(md):
    md.inline.register_rule(
        'footnote',
        INLINE_FOOTNOTE_PATTERN,
        parse_inline_footnote
    )
    index = md.inline.rules.index('std_link')
    if index != -1:
        md.inline.rules.insert(index, 'footnote')
    else:
        md.inline.rules.append('footnote')

    md.block.register_rule('def_footnote', DEF_FOOTNOTE, parse_def_footnote)
    index = md.block.rules.index('def_link')
    if index != -1:
        md.block.rules.insert(index, 'def_footnote')
    else:
        md.block.rules.append('def_footnote')

    if md.renderer.NAME == 'html':
        md.renderer.register('footnote_ref', render_html_footnote_ref)
        md.renderer.register('footnote_item', render_html_footnote_item)
        md.renderer.register('footnotes', render_html_footnotes)
    elif md.renderer.NAME == 'ast':
        md.renderer.register('footnote_ref', render_ast_footnote_ref)
        md.renderer.register('footnote_item', render_ast_footnote_item)

    md.after_render_hooks.append(md_footnotes_hook)
