import os, sys, time, json
import serial
import enum
from wifi_script import connect_wifi
from timeloop import Timeloop
from datetime import timedelta
import bt_serial as bluetooth
import requests
import api
import time

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
            if(connect_wifi()):
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
        resp = {'status': api.GENERIC_ERROR}
        while(resp['status'] == api.GENERIC_ERROR)
            resp = api.request_id()
            if(resp['status'] == api.GENERIC_ERROR):
                # so we don't bombard server if something is wrong
                time.sleep(1)

        if(resp['status'] == api.CONNECTION_ERROR):
            # connection error? try again
            return States.Wifi
        else:
            set_id(resp['id'])
    
    resp = api.poll_poke(poke_id)
    



    


def flash():
    

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