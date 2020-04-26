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
#command = sys.argv[1] + "\r\n"
ser.write("AT+NAME=poke\r\n".encode())
response = ser.readline()
print(response.decode())

