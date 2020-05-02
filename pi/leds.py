import RPi.GPIO as GPIO
import pigpio
import subprocess
import time

initpigpio()
pi = pigpio.pi()

pigpio.exceptions = false
def flash():
    return 0

#TODO: function sleeps for 1 second
def initpigpio():
    process = subprocess.Popen(['sudo', 'killall', 'pigpiod'])
    process = subprocess.Popen(['sudo', '~/pigpio-master/./pigpiod'])
    time.sleep(1) #just to ensure pigiod is run

if __name__ == "__main__":
    
