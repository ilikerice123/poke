import RPi.GPIO as GPIO
import pigpio
import subprocess
import time
from state import States

RED_PIN = 17
BLUE_PIN = 27
GREEN_PIN = 22

led_vals = [0, 0, 255]
led_pins = [RED_PIN, BLUE_PIN, GREEN_PIN]
i = 2

subprocess.run(['sudo', './pigpio.sh'])
time.sleep(1) #just to ensure pigiod is run

pi = pigpio.pi()
# pigpio.exceptions = False

def flash():
    take_breath()
    stop()
    return States.Wait

def take_breath():
    global i
    for x in range(0, 255):
        if(led_vals[i] == 255):
            if(i == 0):
                i = 2
            else:
                i -= 1
        led_vals[i] += 1
        led_vals[(i+1)%3] -= 1

        pi.set_PWM_dutycycle(led_pins[i], led_vals[i]*x/255)
        pi.set_PWM_dutycycle(led_pins[(i+1)%3], led_vals[(i+1)%3]*x/255)
        time.sleep(0.01)
    for x in range(0, 255-0):
        if(led_vals[i] == 255):
            if(i == 0):
                i = 2
            else:
                i -= 1
        led_vals[i] += 1
        led_vals[(i+1)%3] -= 1

        pi.set_PWM_dutycycle(led_pins[i], led_vals[i]*(255-x)/255)
        pi.set_PWM_dutycycle(led_pins[(i+1)%3], led_vals[(i+1)%3]*(255-x)/255)
        time.sleep(0.01)

def stop():
    pi.set_PWM_dutycycle(RED_PIN, 0)
    pi.set_PWM_dutycycle(BLUE_PIN, 0)
    pi.set_PWM_dutycycle(GREEN_PIN, 0)

#"breathing" LED
if __name__ == "__main__":
    while True:
        take_breath()

stop()