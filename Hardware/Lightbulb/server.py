# http://docs.micropython.org/en/v1.8.7/esp8266/esp8266/tutorial/network_tcp.html
# http://docs.micropython.org/en/latest/pyboard/library/usocket.html

import socket

import light
from helpers import cons_print
from responder import request_handler
from server_config import IP, PORT, RESPONSES


# ---
def server_init(ip=IP, port=PORT):
    # ----
    # Create the socket and start listening on it
    #
    # :param ip: String, standard IP address format
    # :param port: Integer, the port clients will connect with
    # :return: Socket, established as a listener
    # ----

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)        # Create the socket
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)      # Release socket on disconnect
    sock.bind((ip, port))
    sock.listen(100)                                                # Begin listening for clients; length 100 queue

    cons_print('Server is up on port {}\n'.format(port))
    return sock

# ---
def server_loop(sock):
    # ----
    # The main server (client connection handler)
    #
    # :param sock: Socket object - must be listening
    # :return: None
    # ----
    
    light.boot_ack()            # Blink light to show that the server has started
    light.flash_ip()            # Use light to display the IP
    resp = RESPONSES['ok']      # Set the initial response

    # Loop until we're asked to exit to the REPL
    while resp != RESPONSES['exit']:

        try:
            # Wait for client (blocking)
            conn, addr = sock.accept()

            light.ack(5)
            user = '{}:{}'.format(*addr)
            cons_print(user, 'connected')

            data = str(conn.recv(1000))[2:-1]
            method, directory = data.split(' ')[:2]
            cons_print(data)
            
            if 'Content-Length' in data:
                # Probable security hole for modified headers - figure out later.
                for p in data.split(r'\r\n'):
                    if 'Content-Length:' in p:
                        try:
                            length = int(p.replace('Content-Length: ', '')) + 4
                            data = str(conn.recv(length))[2:-1]
                            cons_print(data)
                            break

                        except ValueError:
                            conn.send(RESPONSES['unknown'])
                            conn.close()
                            cons_print(user, 'disconnected')
                            continue
            
            # Parse the data and send the response code
            resp = request_handler(method, directory, data)
            conn.send(resp)

        # Server killed via serial REPL
        except KeyboardInterrupt:
            conn.close()
            cons_print(user, 'disconnected')
            break

        # Client disconnected unexpectedly, but it doesn't really matter
        except OSError:
            pass

        # MicroPython does not currently support advanced traceback features.
        # For system stability, this needs to remain (while in production)
        # for the time being.
        except Exception as e:
            cons_print(e)

        finally:
            # End the connection to the client
            conn.close()
            cons_print(user, 'disconnected')

    cons_print('Server shutting down...\n')

# ---
def run():
    try:
        sock = server_init()
        server_loop(sock)

    finally:
        sock.close()

# ---
if __name__ == '__main__':
    run()
