import json

from server_config import RESPONSES
from helpers import *
import light

# ------
def request_handler(method, directory, data):
    hdlr = {
        '/': root_dir,
        '/light': light_dir
    }[directory]
        
    if method == 'GET':
        return hdlr.GET(data)
    
    elif method == 'POST':
        return hdlr.POST(data)
    
    # https://tools.ietf.org/html/rfc2324
    elif method == 'BREW':
        return RESPONSES['coffee']
         
    else:
        return RESPONSES['unknown']
        
# ----
class root_dir:
    def GET(data):
        return RESPONSES['ok']
    def POST(data):
        return RESPONSES['ok']
        
# ----
class light_dir:
    def GET(data):
        conf = light.get_config()
        resp = 'HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n' +\
               'Content-Length: {}\r\n\r\n{}'
        resp = resp.format(len(conf), conf)

        return bytes(resp, 'utf-8')
        
    # --
    def POST(data):
            try:
                js = json.loads(data)

            except ValueError:
                cons_print('Received invalid JSON')
                return RESPONSES['format']

            if isinstance(js, str):
                return RESPONSES['format']

            color = js.get('color')
            bright = js.get('brightness') or '50'

            _rgb = is_rgb(color)
            _hex = is_hex(color)

            if _rgb:
                color = color.split(',') if ' ' not in color else color.split(', ')
                r, g, b = (min(255, int(_)) for _ in color)
                
            elif _hex:
                r, g, b = hex_to_rgb(color)
                
            else:
                return RESPONSES['format']
                
            # Everything went swimmingly
            cons_print('Setting color to {}% ({}, {}, {})'.format(bright, r, g, b))
            light.set_color(r, g, b, brightness=bright)
            
            return RESPONSES['ok']
