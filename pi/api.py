import requests

SERVER_URL = ''
GENERIC_ERROR = 'err'
CONNECTION_ERROR = 'no connection'

def request_id():
    try:
        r = requests.get(SERVER_URL + '/device')
        return {'status': r.status_code, 'id': r.json().get('id', None)}
    except requests.ConnectionError: 
        # assume something wrong with internet connection
        return {'status': CONNECTION_ERROR, 'id': None}
    except:
        return {'status': GENERIC_ERROR, 'id': None}

# when this returns, either connection error, or poke is true
def poll_poke(id):
    request = {}
    while((request.get('poke', False) != True) and (request.get('status', None) != 'no connection')):
        try:
            # no timeout
            r = requests.get(SERVER_URL + '/device/' + id + '/poke', timeout=None)
            request = r.json()
        except requests.ConnectionError: 
            # assume something wrong with internet connection
            return {'status': CONNECTION_ERROR, 'poke': False}
        except:
            return {'status': GENERIC_ERROR, 'poke': False}

    return request

