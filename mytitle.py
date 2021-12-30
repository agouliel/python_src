# https://twitter.com/treyhunner/status/1475588099266781196

import re
from markupsafe import soft_str

# Django

def title(value):
    """Convert a string into titlecase."""
    t = re.sub("([a-z])'([A-Z])", lambda m: m[0].lower(), value.title())
    return re.sub(r'\d([A-Z])', lambda m: m[0].lower(), t)

# jinja
# https://github.com/pallets/jinja/blob/3.0.3/src/jinja2/filters.py#L325,L335

_word_beginning_split_re = re.compile(r"([-\s({\[<]+)")

def do_title(s: str) -> str:
    """Return a titlecased version of the value. I.e. words will start with
    uppercase letters, all remaining characters are lowercase.
    """
    return "".join(
        [
            item[0].upper() + item[1:].lower()
            for item in _word_beginning_split_re.split(soft_str(s))
            if item
        ]
    )
