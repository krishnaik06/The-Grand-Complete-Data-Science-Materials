try:
    from urllib.parse import quote
    import html
except ImportError:
    from urllib import quote
    html = None


PUNCTUATION = r'''\\!"#$%&'()*+,./:;<=>?@\[\]^`{}|_~-'''
ESCAPE_TEXT = r'\\[' + PUNCTUATION + ']'


def escape(s, quote=True):
    s = s.replace("&", "&amp;")
    s = s.replace("<", "&lt;")
    s = s.replace(">", "&gt;")
    if quote:
        s = s.replace('"', "&quot;")
    return s


def escape_url(link):
    safe = (
        ':/?#@'           # gen-delims - '[]' (rfc3986)
        '!$&()*+,;='      # sub-delims - "'" (rfc3986)
        '%'               # leave already-encoded octets alone
    )

    if html is None:
        return quote(link.encode('utf-8'), safe=safe)
    return html.escape(quote(html.unescape(link), safe=safe))


def escape_html(s):
    if html is not None:
        return html.escape(html.unescape(s)).replace('&#x27;', "'")
    return escape(s)


def unikey(s):
    return ' '.join(s.split()).lower()
