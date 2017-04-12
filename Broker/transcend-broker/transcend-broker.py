# transcend-broker.py
# ---
# Part of the Transcend library
# Broker that handles communication between the game and Transcend Devices
# ---
# Luke Jones, 2017
# --------

import requests

import traceback
import urllib
import socket
import json
import inspect
import configparser
import importlib
import importlib.util

# Fix module loading issues
import sys
sys.path.append('./user_modules')


class TranscendBroker:
    def __init__(self):
        self._device_config = None
        self._game_socket = None
        self._game_addr = None
        self.running = False

        self._devices = dict()

        parser = configparser.ConfigParser()
        parser.read('config/devices.cfg')
        self._device_config = parser
        self._setup_devices()

        parser.read('config/transcend.cfg')
        self._game_config = parser
        self._setup_broker()

    # ----
    @staticmethod
    def _jsonify(data):
        """
        Helper function for converting data to JSON

        :param data: JSON String
        :return: Python dictionary if everything goes well
        """

        try:
            data = data.replace("'", '"')
            return json.loads(data)

        except json.decoder.JSONDecodeError:
            return False  # TODO: This is unexpected behavior

    # ----
    def run(self):
        """
        Starts the broker and notifies the game.

        :return: None
        """

        self.running = True
        print('Broker running\n')

        while self.running:
            update = False

            try:
                conn, addr = self._game_socket.accept()
                conn.settimeout(1.5)
                data = str(conn.recv(2048))[2:-1]
                data = urllib.parse.unquote(data)

                if 'PUT' in data:
                    data = str(conn.recv(2048))[2:-1]
                    data = self._jsonify(data)

                elif 'POST' in data:
                    data = data.split(r'\r\n\r\n')[-1]
                    data = self._jsonify(data)

                elif 'GET' in data:
                    data = {'object_name': 'main_lightbulb'}
                    update = True

                device_response = b'HTTP/1.1 '

                # Successfully converted data to JSON
                if data:
                    game_obj_name = data.get('object_name')
                    shutdown_req = data.get('broker_do_shutdown')

                    if game_obj_name:
                        device = self._devices[game_obj_name]
                        rdata = ''

                        if update:
                            rcode, rdata = device.update()
                        else:
                            rcode = device.send(data)

                        device_response += bytes('{}\r\n\r\n{}'.format(rcode, rdata), 'utf-8')

                    # Game is shutting down
                    elif shutdown_req:
                        conn.close()
                        break

                # Something went wrong
                else:
                    device_response += b'503'

                conn.send(device_response)

            except Exception as ex:
                print(ex)
                traceback.print_tb(ex.__traceback__)

            finally:
                conn.close()

        self.shutdown()

    # ----
    def shutdown(self):
        """
        Shuts down the broker and notifies the game.

        :return: None
        """

        msg = self._jsonify('{"broker_status": "down"}')
        requests.post(self._game_addr, json=msg)

        self._game_socket.close()
        self.running = False

    # ----
    def _setup_devices(self):
        # Read configuration file, instantiate the Transcend Device objects,
        # and add the objects to the devices dictionary.

        # http://stackoverflow.com/a/1796247
        for game_obj_name in self._device_config.sections():
            config = self._device_config[game_obj_name]

            dev_type = config['type']
            spec = importlib.util.find_spec(dev_type)     # Find the module specification by its name
            mod = importlib.util.module_from_spec(spec)   # Get the module from the specifications
            spec.loader.exec_module(mod)                  # Load the module

            # Retrieve the device class
            device = inspect.getmembers(mod, lambda m: inspect.isclass(m) and m.__name__ == dev_type)[0][1]

            # Establish the device's fully qualified address
            address = '{}://{}:{}{}'.format(config['protocol'], config['ip'],
                                            config['port'], config['api_suffix'])

            self._devices[game_obj_name] = device(address, game_obj_name)

    # ----
    def _setup_broker(self):
        # Get the game connection information and spawn a socket with it

        port = self._game_config['connection'].get('port')  # 22300

        self._game_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._game_socket.bind(('127.0.0.1', int(port)))
        self._game_socket.listen(5)

        self._game_addr = 'http://127.0.0.1:' + port


if __name__ == '__main__':
    broker = TranscendBroker()
    broker.run()
