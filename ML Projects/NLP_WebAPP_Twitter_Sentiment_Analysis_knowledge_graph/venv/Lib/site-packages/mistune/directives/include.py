import os
from mistune.markdown import preprocess
from .base import Directive


class DirectiveInclude(Directive):
    def parse(self, block, m, state):
        source_file = state.get('__file__')
        if not source_file:
            return {
                'type': 'block_error',
                'raw': 'Missing source file configuration',
            }

        relpath = m.group('value')
        options = self.parse_options(m)

        dest = os.path.join(os.path.dirname(source_file), relpath)
        dest = os.path.normpath(dest)
        if dest == source_file:
            return {
                'type': 'block_error',
                'raw': 'Could not include self: ' + relpath,
            }

        if not os.path.isfile(dest):
            return {
                'type': 'block_error',
                'raw': 'Could not find file: ' + relpath,
            }

        with open(dest, 'rb') as f:
            content = f.read()
            text = content.decode('utf-8')

        if not options:
            ext = os.path.splitext(relpath)[1]
            if ext in {'.md', '.markdown', '.mkd'}:
                text, state = preprocess(text, {'__file__': dest})
                return block.parse(text, state)
            if ext in {'.html', '.xhtml', '.htm'}:
                return {'type': 'block_html', 'text': text}

        return {
            'type': 'include',
            'raw': text,
            'params': (relpath, dest, options)
        }

    def __call__(self, md):
        self.register_directive(md, 'include')
        if md.renderer.NAME == 'html':
            md.renderer.register('include', render_html_include)

        elif md.renderer.NAME == 'ast':
            md.renderer.register('include', render_ast_include)


def render_ast_include(text, relpath, abspath=None, options=None):
    return {
        'type': 'include',
        'text': text,
        'relpath': relpath,
        'abspath': abspath,
        'options': options,
    }


def render_html_include(text, relpath, abspath=None, options=None):
    html = '<section class="directive-include" data-relpath="'
    return html + relpath + '">\n' + text + '</section>\n'
