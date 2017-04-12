# Clear out memory and connect to WiFi
from helpers import cons_print
cons_print('---Beginning boot sequence---')

import gc
cons_print('\nCollecting garbage...')
gc.collect()
cons_print('Garbage collection complete.\n')

import light
import hw_config
light.set_color(0, 0, 0, 0)
hw_config.LED_ACK.high()

from hw_config import _do_setup_wifi
_do_setup_wifi()

import server
server.run()
