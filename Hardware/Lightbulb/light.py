import time
import json
import network

from hw_config import LED_GREEN, LED_BLUE, LED_RED, LED_ACK
from server_debug import SERVER_DEBUG_MODE, FLASH_IP


# ------
def ack(length=500):
    # Built-in pin is inverted
    LED_ACK.low()
    time.sleep_ms(length)
    LED_ACK.high()

# ------
def boot_ack():
    blink(255, 100, 0, 300)
    time.sleep_ms(600)

    if SERVER_DEBUG_MODE:
        # Blink the on-board light
        ack(600)

# ------
def flash_ip():
    if not FLASH_IP:
        return

    colors = {
              '.': ((0, 0, 0), 2),
              '0': ((255, 255, 0), 1), 
              '1': ((255, 0, 0), 1), 
              '2': ((255, 0, 0), 2), 
              '3': ((255, 0, 0), 3), 
              '4': ((0, 255, 0), 1), 
              '5': ((0, 255, 0), 2), 
              '6': ((0, 255, 0), 3), 
              '7': ((0, 0, 255), 1), 
              '8': ((0, 0, 255), 2), 
              '9': ((0, 0, 255), 3)
              }

    for ch in network.WLAN(network.STA_IF).ifconfig()[0]:
        p = colors.get(ch)

        if p:
            c, t = p
            r, g, b = c

            if c == '.':
                time.sleep_ms(200)
            else:
                for _ in range(t):
                    # Blink doesn't behave reliably when called this quickly, so we'll do it this way.
                    set_color(r, g, b, brightness=75)
                    time.sleep_ms(200)
                    set_color(0, 0, 0, brightness=75)
                    time.sleep_ms(200)                      # Time between blinks for a number

        time.sleep_ms(650)                              # Wait between numbers

# ------
def get_config():
    try:
        with open('current.cfg', 'r') as f:
            try:
                return json.dumps(f.readline())
            except ValueError:
                return json.dumps('{"Error": "Invalid configuration"}')

    except OSError:
        return json.dumps('{"Error": "No config file found"}')

# ------
def restore():
    pass

    # # Restores to config from before boot
    # conf = get_config()
    # err = conf.get('Error')
    #
    # if err:
    #     cons_print('Error -', err)
    #     cons_print('Restore failed, bad JSON')
    #     return
    #
    # r, g, b = conf['color'].split(',')
    # bri = conf['brightness']
    # set_color(r, g, b, bri)

# ------
def set_color(r, g, b, brightness=50):
    # Set the color of the light

    with open('current.cfg', 'w') as f:
        print('{' + '"color": "{},{},{}", "brightness": "{}"'.format(r, g, b, brightness) + '}', file=f)

    brightness = int(brightness)
    bri = min(1024.0, 1024 * (brightness / 100))

    r, g, b = [int((v/255) * bri) for v in (r, g, b)]

    LED_RED.duty(r)
    LED_GREEN.duty(g)
    LED_BLUE.duty(b)

# ------
def blink(r=255, g=0, b=0, brightness=50, t=500):
    # Blink the light with given color, returning to previous color afterwards

    # Save old colors
    ro = LED_RED.duty()
    go = LED_GREEN.duty()
    bo = LED_BLUE.duty()

    # Set new colors
    set_color(r, g, b, brightness)
    time.sleep_ms(t)
    set_color(ro, go, bo, brightness)
