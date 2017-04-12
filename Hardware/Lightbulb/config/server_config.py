# Configure network settings here
IP = '0.0.0.0'
PORT = 80

# str, password to access the REPL
REPL_PASS = 'standardpidgeonhockey'

# -----
# Establish our HTTP response codes
_H400 = b'HTTP/1.1 400 Bad Request: '

RESPONSES = {k: (v + b'\r\n\r\n') for k, v in {
    'ok':       b'HTTP/1.1 200 OK',
    'unknown': _H400[:-2] + b'',
    'format':  _H400 + b'Expected RGB values in JSON format: {"color": "r,g,b"}',
    'bad-int': _H400 + b'RGB values are in the range 0-255',
    'non-int': _H400 + b'Excepted RGB integer values in JSON format: {"color": "r,g,b"}',
    'exit':     b'HTTP/1.1 202 Accepted: Server shutting down',
    'coffee':   b"HTTP/1.1 418 I'm a light bulb: Press my button and see me shine"
}.items()}
