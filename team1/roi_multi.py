#!/usr/bin/env python
#test
import sys, signal
sys.path.insert(0, "build/lib.linux-armv7l-2.7/")

import VL53L1X
import time
from datetime import datetime
from mqtt_conn import *
import threading

import time
import socket

def is_connected():
        try:
            # connect to the host -- tells us if the host is actually
            # reachable
            socket.create_connection(("www.google.com", 80))
            return True
        except:
            return False

while not is_connected():
    print("Awaiting Network - Waiting for 5 seconds")
    time.sleep(5)

print("Network Connected!")
client = create_client()

tof = VL53L1X.VL53L1X(i2c_bus=1, i2c_address=0x29)
print("Python: Initialized")
tof.open()
print("Python: Opened")

UPDATE_TIME_MICROS = 15000
INTER_MEASUREMENT_PERIOD_MILLIS = 50
tof.set_timing(UPDATE_TIME_MICROS, INTER_MEASUREMENT_PERIOD_MILLIS)
tof.start_ranging(2)

readings = []
process_readings = []

def exit_handler(signal, frame):
    tof.stop_ranging()
    tof.close()
    sys.exit(0)

signal.signal(signal.SIGINT, exit_handler)

def outsideDistance(lower,upper):
    tof.set_user_roi(VL53L1X.VL53L1xUserRoi(0, 15, 15, 12))
    dist = tof.get_distance()
    if dist < upper and dist > lower:
        return 1
    return 0

def insideDistance(lower,upper):
    tof.set_user_roi(VL53L1X.VL53L1xUserRoi(0, 3, 15, 0))
    dist = tof.get_distance()
    if dist < upper and dist > lower:
        return 1
    return 0

def tof_readings():

    global readings

    lowerThreshold = 300
    upperThreshold = 1500

    outside = 0
    inside = 0
    status = 0 # toggle ROI: 0 - inside, 1 - outside
    i = 1
    zero_count = 0

    prev_reading = [0,0]


    while True:
        curr_reading = [0,0] #inside, outside

        if status:
            outside = outsideDistance(lowerThreshold,upperThreshold)
            if outside:
                curr_reading[1] = 1

                #print("outside")
            #print("Left: " + str(showLeft) + " |")
            status = 0

        if not status:
            inside = insideDistance(lowerThreshold,upperThreshold)
            if inside:
                curr_reading[0] = 1

                #print("inside")
            #print("          | Right: " + str(showRight) )
            status = 1

        if i==1 and sum(curr_reading)==1:
            readings.append(curr_reading)
            prev_reading = curr_reading[:]
            i = 0
            zero_count = 0
            #print(readings)
            pass

        if curr_reading != prev_reading:
            if sum(curr_reading)==1:
                readings.append(curr_reading)
                prev_reading = curr_reading[:]
                zero_count = 0
                #print(readings)
                pass

        if sum(curr_reading)==0:
            zero_count+=1

        if zero_count > 7 and i==0:
            readings.append(curr_reading)
            i = 1
            prev_reading = [0,0]
            process_thread = threading.Thread(target=counting, args=[readings])
            process_thread.start()
            readings = []

def counting(process_readings):

        # print(process_readings)

        if len(process_readings) < 3:
            return

        if len(process_readings) == 3:
            print(process_readings)

        if len(process_readings) == 4:
            print(process_readings)
            process_readings = process_readings[1:3]

        if len(process_readings) >= 5 :
            print(process_readings)
            process_readings = process_readings[2:4]

        # if len(process_readings) > 5:
        #     print(process_readings)

    
        

        if process_readings[0]==[0,1] and process_readings[1]==[1,0]:

            now = str(datetime.now())
            msg = "['" + now + "','1']"
            publish_tof_results(client,msg)

            print("in")

        elif process_readings[0]==[1,0] and process_readings[1]==[0,1]:

            now = str(datetime.now())
            msg = "['" + now + "','-1']"
            publish_tof_results(client,msg)

            print("out")


if __name__ == '__main__':
    tof_readings()
