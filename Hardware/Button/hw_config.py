import network
import machine as esp

from wifi_config import *


def _do_scan(networks):
    for net in networks:
        _s = str(net[0])[2:-1]
        
        for known in WIFI_SSIDS:
            ssid = known[0]
            
            if _s == ssid:
                return known

                
def _do_setup_wifi():
    # ------
    # Disable Access Point mode
    network.WLAN(network.AP_IF).active(False)

    # Set wireless mode to wireless N
    network.phy_mode(network.MODE_11N)

    # Set up the client radio
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    networks = wlan.scan()
    
    ssid, passw = _do_scan(networks)
    
    if not wlan.isconnected():
        print('Connecting to network...')
        wlan.connect(ssid, passw)

        while not wlan.isconnected():
            pass

    print('Connected. You can find me at', wlan.ifconfig()[0], '\n')

# ------
# Establish the pins that are connected to our LEDs
SWITCH = esp.Pin(15, esp.Pin.IN)
