# BasicRGBLight.py
# ---
# Part of the Transcend library
# Transcend Device implementation to control a basic networked RGB light bulb
# ---
# Luke Jones, 2017
# --------

# Note that basedevice does not have a leading period.
from basedevice import Device
import requests
import sys

sys.path.append('./utils')
from utils import jsonify, unjsonify


class BasicRGBLight(Device):
    def __init__(self, address, object_name):
        Device.__init__(self, address, object_name)

    # -----
    def format_for_device(self, data):
        js_out = {'color': data.get('color'),
                  'brightness': data.get('brightness')}

        return js_out

    # -----
    def send(self, data):
        new_data = self.format_for_device(data)
        req = requests.post(self.address, json=new_data, timeout=1.5)

        return req.status_code

    # -----
    def format_for_game(self, data):
        data = str(data)[2:-1].replace("\\n", '').replace('\\', '')[1:-1]

        rdata = unjsonify(data)
        color = rdata['color']
        bright = rdata['brightness']

        r, g, b = [int(_) / 255 for _ in color.split(',')]
        a = int(bright) / 100

        return jsonify({'r': r, 'g': g, 'b': b, 'a': a})

    # -----
    def update(self):
        req = requests.get(self.address, timeout=1.5)
        data = self.format_for_game(req.content)

        return req.status_code, data
