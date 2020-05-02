import os, sys, time, json
import serial
import enum
import requests
import api
import time

from timeloop import Timeloop
from datetime import timedelta

import wifi_script as wifi
import bt_serial as bluetooth
import leds

ID_FILE = 'poke.id'
class States(enum.Enum):
    Wifi = 1
    Wait = 2
    Flash = 3

state = States.Wifi
poke_id = get_id()

#sent to user
error = "no error"

while True:
    if(state is States.Wifi):
        while True:
            if(wifi.connect()):
                break
        next_state = States.Wait
    elif(state is States.Wait):
        next_state = wait()
    else:
        next_state = flash()

    state = next_state

tl = Timeloop()

@tl.job(interval=timedelta(seconds=1))
def send_state():
    request = json.dumps({'command': 'state', 'state': state})
    bluetooth.send_bt_data(request)

def wait():
    if(poke_id is None):
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
    while(resp['status'] == api.GENERIC_ERROR):
        # so we don't bombard server if something is wrong
        time.sleep(1)
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
        return id
    except FileNotFoundError:
        return None

def set_id(id):
    poke_id = id
    file = open(ID_FILE, mode='w')
    file.write(id)
    file.close()