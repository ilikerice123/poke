import os, sys
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

ser.write("AT\r\n")
response = ser.readline()
print(response)

