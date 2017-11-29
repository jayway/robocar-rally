# wheel mappings
# left front wheel 20

import RPi.GPIO as GPIO
import time
from time import sleep
import multiprocessing

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

pulse = 0
wheeldistance = 0
wheelrpm = 0.00
speed = 0.00
wheel_in = 9.5
hall = 20
elapse = 0.00

start = time.time()

GPIO.setup(hall, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def get_wheelrpm():
    return wheelrpm


def get_speed():
    return speed


def get_wheeldistance():
    return wheeldistance


def get_elapse():
    return elapse


def get_pulse(number):
    global elapse, wheeldistance, start, pulse, speed, wheelrpm, multiplier
    cycle = 0
    pulse += 1
    cycle += 1
    if pulse > 0:
        elapse = time.time() - start
        pulse -= 1
    if cycle > 0:
        wheeldistance += wheel_in
        cycle -= 1

    wheelrpm = 1 / elapse * 60
    start = time.time()
    sleep(.001)

try:
    GPIO.add_event_detect(hall, GPIO.FALLING, callback=get_pulse, bouncetime=20)
except KeyboardInterrupt:
    GPIO.cleanup()