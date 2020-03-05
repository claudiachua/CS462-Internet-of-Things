#!/usr/bin/env python

import sys, signal
sys.path.insert(0, "build/lib.linux-armv7l-2.7/")

import VL53L1X
import time
from datetime import datetime

tof = VL53L1X.VL53L1X(i2c_bus=1, i2c_address=0x29)
print("Python: Initialized")
tof.open()
print("Python: Opened")

UPDATE_TIME_MICROS = 15000
INTER_MEASUREMENT_PERIOD_MILLIS = 150
tof.set_timing(UPDATE_TIME_MICROS, INTER_MEASUREMENT_PERIOD_MILLIS)
tof.start_ranging(1)

def exit_handler(signal, frame):
    tof.stop_ranging()
    tof.close()
    sys.exit(0)

signal.signal(signal.SIGINT, exit_handler)

def leftDistance():
    tof.set_user_roi(VL53L1X.VL53L1xUserRoi(12, 15, 15, 0))
    return tof.get_distance()/10

def rightDistance():
    tof.set_user_roi(VL53L1X.VL53L1xUserRoi(0, 15, 15, 3))
    return tof.get_distance()/10

distanceLeft_cm = 0
distanceRight_cm = 0

showLeft = 0
showRight = 0

while True:

    distanceLeft_cm = leftDistance()
    distanceRight_cm = rightDistance()

    if distanceLeft_cm > 0 and distanceLeft_cm < 50:
        showLeft = distanceLeft_cm

    if distanceRight_cm > 0 and distanceRight_cm < 50:
        showRight = distanceRight_cm


    print("Left: " + str(showLeft) + " | Right: " + str(showRight))
    showRight = 0
    showLeft = 0
