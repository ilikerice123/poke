import os, sys, time, json
import serial
import requests
import subprocess

print(response["command"])
print(response["ssid"])
print(response["password"])

print(wifi.Search())
connection = wifi.Connect(response["ssid"], response["password"])
if connection:
    print(connection)
else:
    print("wifi connect failed")

completed_process = subprocess.run(['sudo', 'dhclient', 'wlan0'])
response = requests.get('http://google.com')
print (response.status_code)
print (response.content)
