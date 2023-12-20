"""
Utility functions for working with the color names and color value
formats defined by the HTML and CSS specifications for use in
documents on the web.

See documentation (in docs/ directory of source distribution) for
details of the supported formats, conventions and conversions.

"""
from .constants import (
    CSS2,
    CSS2_HEX_TO_NAMES,
    CSS2_NAMES_TO_HEX,
    CSS3,
    CSS3_HEX_TO_NAMES,
    CSS3_NAMES_TO_HEX,
    CSS21,
    CSS21_HEX_TO_NAMES,
    CSS21_NAMES_TO_HEX,
    HTML4,
    HTML4_HEX_TO_NAMES,
    HTML4_NAMES_TO_HEX,
)
from .conversion import (
    hex_to_name,
    hex_to_rgb,
    hex_to_rgb_percent,
    name_to_hex,
    name_to_rgb,
    name_to_rgb_percent,
    rgb_percent_to_hex,
    rgb_percent_to_name,
    rgb_percent_to_rgb,
    rgb_to_hex,
    rgb_to_name,
    rgb_to_rgb_percent,
)
from .html5 import (
    html5_parse_legacy_color,
    html5_parse_simple_color,
    html5_serialize_simple_color,
)
from .normalization import (
    normalize_hex,
    normalize_integer_triplet,
    normalize_percent_triplet,
)
from .types import HTML5SimpleColor, IntegerRGB, IntTuple, PercentRGB, PercentTuple

__version__ = "1.13"

__all__ = [
    "HTML4",
    "CSS2",
    "CSS21",
    "CSS3",
    "HTML4_NAMES_TO_HEX",
    "HTML4_HEX_TO_NAMES",
    "CSS2_NAMES_TO_HEX",
    "CSS2_HEX_TO_NAMES",
    "CSS21_HEX_TO_NAMES",
    "CSS21_NAMES_TO_HEX",
    "CSS3_HEX_TO_NAMES",
    "CSS3_NAMES_TO_HEX",
    "name_to_hex",
    "name_to_rgb",
    "name_to_rgb_percent",
    "hex_to_name",
    "hex_to_rgb",
    "hex_to_rgb_percent",
    "rgb_to_hex",
    "rgb_to_name",
    "rgb_to_rgb_percent",
    "rgb_percent_to_hex",
    "rgb_percent_to_name",
    "rgb_percent_to_rgb",
    "html5_parse_simple_color",
    "html5_parse_legacy_color",
    "html5_serialize_simple_color",
    "normalize_hex",
    "normalize_integer_triplet",
    "normalize_percent_triplet",
    "IntegerRGB",
    "PercentRGB",
    "HTML5SimpleColor",
    "IntTuple",
    "PercentTuple",
]
