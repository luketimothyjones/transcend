from hw_config import SWITCH

import urequests
import urandom

url = "http://192.168.1.35/light"
#url = "http://192.168.43.234/light"


urandom.seed(30)
def randint():
    return urandom.getrandbits(8)
    
while True:
    if not SWITCH.value():
        color = '{},{},{}'.format(randint(), randint(), randint())
        js = {"color": color}
        
        urequests.post(url, json=js)
