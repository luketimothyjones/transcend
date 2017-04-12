from configparser import ConfigParser
import socket


parser = ConfigParser()
parser.read('config/transcend.cfg')
game_config = parser

port = game_config['connection'].get('port')  # 22300

_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
_sock.bind(('127.0.0.1', int(port)))
_sock.listen(5)

print("Responder server up")

try:
    while True:
        conn, addr = _sock.accept()
        dat = str(conn.recv(2048))[2:-1]
        print(dat)
        conn.send(b'HTTP/1.1 200 OK\r\n\r\n')
        conn.close()

finally:
    _sock.close()
