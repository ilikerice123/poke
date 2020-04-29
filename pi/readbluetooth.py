import os, sys, time, json, wireless
import serial
import time

ser = serial.Serial(
                port='/dev/ttyUSB0',
                baudrate = 38400,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=5
            )

while 1:
    json_command = ser.readline().decode()
    try:
        response = json.loads(json_command)
    except:
        print("error")

response = ser.readline()
y = json.loads(response.decode())
print(y["command"])
print(y["ssid"])
print(y["password"])

wire = Wireless()
wire.connect(ssid=y["ssid"], password=y["password"])