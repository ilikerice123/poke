import os, sys, time, json
import serial

import requests
import subprocess
import time

from timeloop import Timeloop
from datetime import timedelta

from state import States
import wifi_script as wifi
import bt_serial as bluetooth
import leds
import api

ID_FILE = 'poke.id'
poke_id = None

def wait():
    p_id = get_id(poke_id)
    if(p_id == ''):
        return States.Wifi
    
    resp = api.poll_poke(p_id)
    if(resp['status'] == api.CONNECTION_ERROR):
        return States.Wifi
    else:
        return States.Flash

def flash():
    return States.Wait

def get_id(poke_id):
    if(poke_id is not None):
        return poke_id

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

        poke_id = resp.get('id', None)
        file = open(ID_FILE, mode='w')
        file.write(poke_id)
        print("done setting id")
        file.close()
        return poke_id

if(len(sys.argv) < 1):
    tl = Timeloop()
    @tl.job(interval=timedelta(seconds=1))
    def send_state():
        request = json.dumps({'command': 'state', 'state': state})
        bluetooth.send_bt_data(request)

state = States.Wifi
if(wifi.has_wifi()):
    state = States.Wait
next_state = state

while True:
    if(state is States.Wifi):
        print("transitioning to wifi")
        if(wifi.connect()):
            next_state = States.Wait
        else:
            next_state = States.Wifi
    elif(state is States.Wait):
        print("transitioning to wait")
        next_state = wait()
    else:
        print("transitioning to flash")
        next_state = leds.flash()

    state = next_state
