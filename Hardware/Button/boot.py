import os

# Clear out memory and connect to WiFi
print('---Beginning boot sequence---')

import gc
print('\nCollecting garbage...')
gc.collect()
print('Garbage collection complete.\n')

from hw_config import _do_setup_wifi
_do_setup_wifi()
