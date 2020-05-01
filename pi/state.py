import os, sys, time, json
import serial
import enum
from wifi_script import connect_wifi
from timeloop import Timeloop
from datetime import timedelta
import bt_serial as bluetooth
import requests

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
        #get poke id

    


def flash():
    

def get_id():
    try:
        file = open(ID_FILE, mode='r')
        id = file.read()
        file.close()
        return id
    except FileNotFoundError:
        return None

def set_id(id):
    file = open(ID_FILE, mode='w')
    file.write(id)
    file.close()