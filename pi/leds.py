import RPi.GPIO as GPIO
import pigpio
import subprocess
import time
from state import States

LED_PIN1 = 12

subprocess.run(['sudo', './pigpio.sh'])
time.sleep(1) #just to ensure pigiod is run

pi = pigpio.pi()
# pigpio.exceptions = False

def flash():
    take_breath(LED_PIN1)
    take_breath(LED_PIN1)
    stop(LED_PIN1)
    return States.Wait

def take_breath(pin):
    for x in range(255):
        pi.set_PWM_dutycycle(pin, 255-x)
        time.sleep(0.005)
    for x in range(255):
        pi.set_PWM_dutycycle(pin, x)
        time.sleep(0.005)

def stop(pin):
    pi.set_PWM_dutycycle(pin, 255)

#"breathing" LED
if __name__ == "__main__":
    # BCM12 = pin 32
    while True:
        take_breath(LED_PIN1)

stop(LED_PIN1)
