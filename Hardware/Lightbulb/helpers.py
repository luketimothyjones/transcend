import ure as re
from server_debug import *

RGB_REGEX = re.compile(r'\(?([0-2]?[0-9]?[0-9], ?)([0-2]?[0-9]?[0-9], ?)([0-2]?[0-9]?[0-9])\)?')
HEX_REGEX = re.compile(r'#?[0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f]')

def cons_print(*args, **kwargs):
    if SERVER_DEBUG_MODE:
        print(*args, **kwargs)

def hex_to_rgb(h):
    if is_hex(h):
        h = h[1:] if h[0] == '#' else h
        r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:], 16)
        return [r, g, b]

    else:
        raise ValueError('Value is not in proper RGB hex form')

def is_rgb(v):
    return RGB_REGEX.match(v) is not None

def is_hex(v):
    return HEX_REGEX.match(v) is not None
