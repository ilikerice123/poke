import RPi.GPIO as GPIO
import pigpio
import subprocess
import time
from state import States

subprocess.run(['sudo', './pigpio.sh'])
time.sleep(1) #just to ensure pigiod is run

pi = pigpio.pi()

# pigpio.exceptions = False

def flash():
    take_breath(12)
    take_breath(12)
    return States.Wait

def take_breath(pin):
    for x in range(255):
        pi.set_PWM_dutycycle(pin, x)
        time.sleep(0.005)
    for x in range(255):
        pi.set_PWM_dutycycle(pin, 255-x)
        time.sleep(0.005)

#"breathing" LED
if __name__ == "__main__":
    # BCM12 = pin 32
    while True:
        take_breath(12)
