import re
from ..util import escape_html


DEF_ABBR = re.compile(
    # *[HTML]:
    # *[HTML]: Hyper Text Markup Language
    # *[HTML]:
    #     Hyper Text Markup Language
    r'\*\[([^\]]+)\]:'
    r'((?:[ \t]*\n(?: {3,}|\t)[^\n]+)|(?:[^\n]*))\n*'
)


def parse_def_abbr(block, m, state):
    def_abbrs = state.get('def_abbrs', {})
    label = m.group(1)
    definition = m.group(2)
    def_abbrs[label] = definition.strip()
    state['def_abbrs'] = def_abbrs


def parse_inline_abbr(inline, m, state):
    def_abbrs = state['def_abbrs']
    label = m.group(0)
    return 'abbr', label, def_abbrs[label]


def after_parse_def_abbr(md, tokens, state):
    def_abbrs = state.get('def_abbrs')
    if def_abbrs:
        labels = list(def_abbrs.keys())
        abbr_pattern = r'|'.join(re.escape(k) for k in labels)
        md.inline.register_rule('abbr', abbr_pattern, parse_inline_abbr)
        md.inline.rules.append('abbr')
    return tokens


def render_html_abbr(key, definition):
    title_attribute = ""
    if definition:
        definition = escape_html(definition)
        title_attribute = ' title="{}"'.format(definition)

    return "<abbr{title_attribute}>{key}</abbr>".format(
        key=key,
        title_attribute=title_attribute,
    )


def render_ast_abbr(key, definition):
    return {'type': 'abbr', 'text': key, 'definition': definition}


def plugin_abbr(md):
    md.block.register_rule('def_abbr', DEF_ABBR, parse_def_abbr)
    md.before_render_hooks.append(after_parse_def_abbr)
    md.block.rules.append('def_abbr')

    if md.renderer.NAME == 'html':
        md.renderer.register('abbr', render_html_abbr)
    elif md.renderer.NAME == 'ast':
        md.renderer.register('abbr', render_ast_abbr)
