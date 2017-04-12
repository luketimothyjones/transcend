import requests
import json
import time

IP = '192.168.1.35'
# IP = '192.168.43.234'

ENDPOINT = 'http://{}/light'.format(IP)


cases = [
    [{'color': '255,0,0'}, 200],
    [{'color': '0,255,0'}, 200],
    [{'color': '0,0,255'}, 200],

    [{'color': '255,255,255'}, 200],
    [{'color': '0,255,255'}, 200],
    [{'color': '255,0,255'}, 200],
    [{'color': '255,255,0'}, 200],

    [{'color': '100,100,100'}, 200],

    [{'color': '255,0,255', 'brightness': '0'}, 200],
    [{'color': '255,0,255', 'brightness': '25'}, 200],
    [{'color': '255,0,255', 'brightness': '50'}, 200],
    [{'color': '255,0,255', 'brightness': '75'}, 200],
    [{'color': '255,0,255', 'brightness': '100'}, 200],

    [{'color': '0,0,0'}, 200],

    [{'color': '300,300,300'}, 400],
    [{'color': '-1,255,255'}, 400],

    [{'color': ',0,0'}, 400],
    [{'color': '0,,0'}, 400],
    [{'color': '0,0,'}, 400],

    [{'color': '0,0,0'}, 200]

]


def main():
    with requests.session() as r:
        try:
            r.post(url=ENDPOINT, json={'color': '255,0,0', 'brightness': '100'}, timeout=5)

        except requests.exceptions.ConnectionError:
            print('No such host,', IP)
            exit()

        a = r.get(url=ENDPOINT)
        print(json.loads(a.text))
        time.sleep(.5)

        for c in cases:
            data, expected = c

            if not data.get('brightness'):
                data['brightness'] = '100'

            a = r.post(url=ENDPOINT, json=data)

            res = ':: Pass' if a.status_code == expected else ':: Fail !! ({})'.format(a.reason)
            print(str(data).ljust(50, ' '), res)

            time.sleep(.05)


if __name__ == '__main__':
    main()
