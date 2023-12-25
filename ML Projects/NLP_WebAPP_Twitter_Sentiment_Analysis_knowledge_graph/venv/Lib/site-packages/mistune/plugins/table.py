import re

__all__ = ['plugin_table']

TABLE_PATTERN = re.compile(
    r' {0,3}\|(.+)\n *\|( *[-:]+[-| :]*)\n((?: *\|.*(?:\n|$))*)\n*'
)
NP_TABLE_PATTERN = re.compile(
    r' {0,3}(\S.*\|.*)\n *([-:]+ *\|[-| :]*)\n((?:.*\|.*(?:\n|$))*)\n*'
)
HEADER_SUB = re.compile(r'\| *$')
HEADER_SPLIT = re.compile(r' *\| *')
ALIGN_SPLIT = re.compile(r' *\| *')


def parse_table(self, m, state):
    header = HEADER_SUB.sub('', m.group(1)).strip()
    align = HEADER_SUB.sub('', m.group(2))
    thead, aligns = _process_table(header, align)

    text = re.sub(r'(?: *\| *)?\n$', '', m.group(3))
    rows = []
    for i, v in enumerate(text.split('\n')):
        v = re.sub(r'^ *\| *| *\| *$', '', v)
        rows.append(_process_row(v, aligns))

    children = [thead, {'type': 'table_body', 'children': rows}]
    return {'type': 'table', 'children': children}


def parse_nptable(self, m, state):
    thead, aligns = _process_table(m.group(1), m.group(2))

    text = re.sub(r'\n$', '', m.group(3))
    rows = []
    for i, v in enumerate(text.split('\n')):
        rows.append(_process_row(v, aligns))

    children = [thead, {'type': 'table_body', 'children': rows}]
    return {'type': 'table', 'children': children}


def _process_table(header, align):
    headers = HEADER_SPLIT.split(header)
    aligns = ALIGN_SPLIT.split(align)

    if header.endswith('|'):
        headers.append('')

    cells = []
    for i, v in enumerate(aligns):
        if re.search(r'^ *-+: *$', v):
            aligns[i] = 'right'
        elif re.search(r'^ *:-+: *$', v):
            aligns[i] = 'center'
        elif re.search(r'^ *:-+ *$', v):
            aligns[i] = 'left'
        else:
            aligns[i] = None

        if len(headers) > i:
            cells.append({
                'type': 'table_cell',
                'text': headers[i],
                'params': (aligns[i], True)
            })

    i += 1
    while i + 1 < len(headers):
        cells.append({
            'type': 'table_cell',
            'text': headers[i],
            'params': (None, True)
        })
        aligns.append(None)
        i += 1

    thead = {'type': 'table_head', 'children': cells}
    return thead, aligns


def _process_row(row, aligns):
    cells = []
    for i, s in enumerate(re.split(r' *(?<!\\)\| *', row)):
        text = re.sub(r'\\\|', '|', s.strip())
        if len(aligns) < i + 1:
            cells.append({
                'type': 'table_cell',
                'text': text,
                'params': (None, False)
            })
        else:
            cells.append({
                'type': 'table_cell',
                'text': text,
                'params': (aligns[i], False)
            })

    if len(cells) < len(aligns):
        for align in aligns[len(cells):]:
            cells.append({
                'type': 'table_cell',
                'text': '',
                'params': (align, False),
            })

    return {'type': 'table_row', 'children': cells}


def render_html_table(text):
    return '<table>\n' + text + '</table>\n'


def render_html_table_head(text):
    return '<thead>\n<tr>\n' + text + '</tr>\n</thead>\n'


def render_html_table_body(text):
    return '<tbody>\n' + text + '</tbody>\n'


def render_html_table_row(text):
    return '<tr>\n' + text + '</tr>\n'


def render_html_table_cell(text, align=None, is_head=False):
    if is_head:
        tag = 'th'
    else:
        tag = 'td'

    html = '  <' + tag
    if align:
        html += ' style="text-align:' + align + '"'

    return html + '>' + text + '</' + tag + '>\n'


def render_ast_table_cell(children, align=None, is_head=False):
    return {
        'type': 'table_cell',
        'children': children,
        'align': align,
        'is_head': is_head
    }


def plugin_table(md):
    md.block.register_rule('table', TABLE_PATTERN, parse_table)
    md.block.register_rule('nptable', NP_TABLE_PATTERN, parse_nptable)
    md.block.rules.append('table')
    md.block.rules.append('nptable')

    if md.renderer.NAME == 'html':
        md.renderer.register('table', render_html_table)
        md.renderer.register('table_head', render_html_table_head)
        md.renderer.register('table_body', render_html_table_body)
        md.renderer.register('table_row', render_html_table_row)
        md.renderer.register('table_cell', render_html_table_cell)

    elif md.renderer.NAME == 'ast':
        md.renderer.register('table_cell', render_ast_table_cell)
