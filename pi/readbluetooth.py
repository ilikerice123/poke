import os, sys, time, json, wireless
import serial
import time
import requests

ser = serial.Serial(
                port='/dev/ttyUSB0',
                baudrate = 38400,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=5
            )

while True:
    response = {}
    try:
        json_command = ser.readline().decode()
        response = json.loads(json_command)
    except:
        print("error")
    if response.get('command', '') is not '':
        break

print(response["command"])
print(response["ssid"])
print(response["password"])

wire = wireless.Wireless()
wire.connect(ssid=response["ssid"], password=response["password"])
response = requests.get('http://google.com')
print (response.status_code)
print (response.content)
