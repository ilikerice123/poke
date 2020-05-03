import os, sys, time, json
import serial

import requests
import api
import time

from timeloop import Timeloop
from datetime import timedelta

from state import States
import wifi_script as wifi
import bt_serial as bluetooth
import leds

ID_FILE = 'poke.id'

def wait():
    print(poke_id)
    if(poke_id is None):
        print("pokeid is null")
        resp = api.request_id()
        while(resp['status'] == api.GENERIC_ERROR):
            # so we don't bombard server if something is wrong
            time.sleep(1)
            resp = api.request_id()

        if(resp['status'] == api.CONNECTION_ERROR):
            return States.Wifi
        else:
            set_id(resp['id'])
    
    resp = api.poll_poke(poke_id)
    if(resp['status'] == api.CONNECTION_ERROR):
        return States.Wifi
    else:
        return States.Flash

def flash():
    return States.Wait

def get_id():
    try:
        file = open(ID_FILE, mode='r')
        poke_id = file.read()
        file.close()
        return poke_id
    except FileNotFoundError:
        return None

def set_id(id):
    print("setting id to " + id)
    poke_id = id
    file = open(ID_FILE, mode='w')
    file.write(id)
    file.close()

if(len(sys.argv) < 1):
    tl = Timeloop()
    @tl.job(interval=timedelta(seconds=1))
    def send_state():
        request = json.dumps({'command': 'state', 'state': state})
        bluetooth.send_bt_data(request)

state = States.Wifi
poke_id = get_id()

#sent to user
error = "no error"

while True:
    if(state is States.Wifi):
        print("transitioning to wifi")
        while True:
            if(wifi.connect()):
                break
        next_state = States.Wait
    elif(state is States.Wait):
        print("transitioning to wait")
        next_state = wait()
    else:
        print("transitioning to flash")
        next_state = flash()

    state = next_state
