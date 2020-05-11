import RPi.GPIO as GPIO
import pigpio
import subprocess
import time

RED_PIN = 17
BLUE_PIN = 27
GREEN_PIN = 22

led_vals = [0, 0, 255]
led_pins = [RED_PIN, BLUE_PIN, GREEN_PIN]
curr_led = 2

subprocess.run(['sudo', './pigpio.sh'])
time.sleep(0.1)
pi = pigpio.pi()

def inc(scale):
    global curr_led
    if(led_vals[curr_led] == 255):
        if(curr_led == 0):
            curr_led = 2
        else:
            curr_led -= 1
    led_vals[curr_led] += 1
    led_vals[(curr_led+1)%3] -= 1

    pi.set_PWM_dutycycle(led_pins[curr_led], led_vals[curr_led]*scale/255)
    pi.set_PWM_dutycycle(led_pins[(curr_led+1)%3], led_vals[(curr_led+1)%3]*scale/255)
    time.sleep(0.01)

def take_breath():
    for x in range(0, 255):
        inc(x)

    for x in range(0, 255):
        inc(255-x)

def stop():
    pi.set_PWM_dutycycle(RED_PIN, 0)
    pi.set_PWM_dutycycle(BLUE_PIN, 0)
    pi.set_PWM_dutycycle(GREEN_PIN, 0)

def flash():
    take_breath()
    stop()

if __name__ == "__main__":
    while True:
        take_breath()

stop()
