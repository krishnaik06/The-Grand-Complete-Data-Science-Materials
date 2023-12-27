import re

__all__ = ["plugin_def_list"]

DEFINITION_LIST_PATTERN = re.compile(r"([^\n]+\n(:[ \t][^\n]+\n)+\n?)+")


def parse_def_list(block, m, state):
    lines = m.group(0).split("\n")
    definition_list_items = []
    for line in lines:
        if not line:
            continue
        if line.strip()[0] == ":":
            definition_list_items.append(
                {"type": "def_list_item", "text": line[1:].strip()}
            )
        else:
            definition_list_items.append(
                {"type": "def_list_header", "text": line.strip()}
            )
    return {"type": "def_list", "children": definition_list_items}


def render_html_def_list(text):
    return "<dl>\n" + text + "</dl>\n"


def render_html_def_list_header(text):
    return "<dt>" + text + "</dt>\n"


def render_html_def_list_item(text):
    return "<dd>" + text + "</dd>\n"


def render_ast_def_list_header(text):
    return {"type": "def_list_header", "text": text[0]["text"]}


def render_ast_def_list_item(text):
    return {"type": "def_list_item", "text": text[0]["text"]}


def plugin_def_list(md):
    md.block.register_rule("def_list", DEFINITION_LIST_PATTERN, parse_def_list)
    md.block.rules.append("def_list")
    if md.renderer.NAME == "html":
        md.renderer.register("def_list", render_html_def_list)
        md.renderer.register("def_list_header", render_html_def_list_header)
        md.renderer.register("def_list_item", render_html_def_list_item)
    if md.renderer.NAME == "ast":
        md.renderer.register("def_list_header", render_ast_def_list_header)
        md.renderer.register("def_list_item", render_ast_def_list_item)
