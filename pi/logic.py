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
poke_id = None

def wait():
    print(poke_id)
    if(poke_id is None):
        return States.Wifi
    
    print("polling poke with id " + poke_id)
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
        print("pokeid is null")
        resp = api.request_id()
        while(resp['status'] == api.GENERIC_ERROR):
            # so we don't bombard server if something is wrong
            time.sleep(1)
            resp = api.request_id()

        new_id = resp.get('id', None)
        file = open(ID_FILE, mode='w')
        file.write(new_id)
        print("done setting id")
        file.close()
        return new_id

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
        next_state = leds.flash()

    state = next_state

if(len(sys.argv) < 1):
    tl = Timeloop()
    @tl.job(interval=timedelta(seconds=1))
    def send_state():
        request = json.dumps({'command': 'state', 'state': state})
        bluetooth.send_bt_data(request)
