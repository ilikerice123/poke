import requests

SERVER_URL = ''

def request_id():
    r = request.get(SERVER_URL + '/device')
    if(r.status_code != 200):
        return None
    return r.json()['id']

# when this returns
def poll_poke(id):
    request = {}
    while(request.get('poke', False) is not True):
        r = requests.get(SERVER_URL + '/device/' + id + '/poke', timeout=60)
        request = r.json()

