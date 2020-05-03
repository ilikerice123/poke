import requests
import sys
import time

SERVER_FILE='server.txt'
file = open(SERVER_FILE, mode='r')
SERVER_URL = file.read()

GENERIC_ERROR = 'err'
CONNECTION_ERROR = 'no connection'

def request_id():
    try:
        print("trying " + SERVER_URL + '/devices')
        r = requests.post(SERVER_URL + '/devices')
        return {'status': r.status_code, 'id': r.json().get('id', None)}
    except requests.ConnectionError:
        print(sys.exc_info())
        # assume something wrong with internet connection
        return {'status': CONNECTION_ERROR, 'id': None}
    except:
        return {'status': GENERIC_ERROR, 'id': None}

# when this returns, either connection error, or poke is true
def poll_poke(id):
    request = {}
    while((request.get('poke', None) != True) and (request.get('status', None) != CONNECTION_ERROR)):
        try:
            # no timeout
            print("checking poke at " + SERVER_URL + '/devices/' + id + '/poke')
            r = requests.get(SERVER_URL + '/devices/' + id + '/poke', timeout=None)
            request = r.json()
            request['status'] = 200
        except requests.ConnectionError: 
            # assume something wrong with internet connection
            return {'status': CONNECTION_ERROR, 'poke': None}
        except:
            time.sleep(1)

    return request

