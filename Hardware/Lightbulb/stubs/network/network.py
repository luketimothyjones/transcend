class Server:
    def __init__(login=('micro', 'python'), timeout=300):
        pass
    def deinit():
        pass
    def timeout(seconds):
        pass
    def isrunning():
        pass
        
class WLAN:
    STA = ''
    AP = ''

    WEP = ''
    WPA = ''
    WPA2 = ''

    INT_ANT = ''
    EXT_ANT = ''
        
    def init(mode, ssid, auth, channel, antenna):
        pass

    def connect(ssid, auth=None, bssid=None, timeout=None):
        pass
    def scan():
        pass
    def disconnect():
        pass
    def isconnected():
        pass
    def ifconfig(if_id=0, config='DHCP'):
        pass
    def mode(mode=None):
        pass
    def ssid(ssid=None):
        pass
    def auth(auth=None):
        pass
    def channel(channel=None):
        pass
    def antenna(antenna=None):
        pass
    def mac(mac_addr=None):
        pass
    def irq(handler, wake):
        pass