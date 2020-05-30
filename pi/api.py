import requests
import sys
import time

# returns either error, or retries until it succeeds

SERVER_FILE='server.txt'
file = open(SERVER_FILE, mode='r')
SERVER_URL = file.read().strip()

CONNECTION_ERROR = 'no connection'

GET = 'get'
POST = 'post'
PUT = 'put'
DELETE = 'delete'
methods = {
    GET: requests.get,
    POST: requests.post,
    PUT: requests.put,
    DELETE: requests.delete
}

# requests an id
def request_new():
    return req('/devices', POST)

# waits for a poke to be activated
def wait_activation(p_id):
    return req('/devices/' + p_id + '/activate', GET)

# when this returns, either connection error, or poke is true
def poll_poke(p_id):
    return req('/devices/' + p_id + '/poke', GET)

def req(url, method, body=None):
    while True:
        try:
            print("trying " + SERVER_URL + url)
            r = methods[method](SERVER_URL + url, data=body)
            return {'status': r.status_code, 'body': r.json()}
        except requests.ConnectionError:
            print(sys.exc_info())
            # assume something wrong with internet connection
            return {'status': CONNECTION_ERROR, 'body': None}
        except:
            # so we don't bombard the server is something is wrong
            time.sleep(1) 
            continue

