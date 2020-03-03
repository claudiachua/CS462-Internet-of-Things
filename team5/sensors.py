#!/usr/bin/env python3

'''
## License
Author: Downey
The MIT License (MIT)

Grove 12 channel touch sensor MPR121 for the Raspberry Pi, used to connect grove sensors.
Copyright (C) 2018  Seeed Technology Co.,Ltd. 

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''
import time, grovepi, json
from grove.i2c import Bus
from datetime import datetime, timedelta
import numpy as np
import paho.mqtt.client as mqtt
import OccupancyStatus, MPR121

def main():
    # Instantiate Capacitive Sensor object
    mpr121 = MPR121.MPR121()
    # Admin attributes
    SEAT_NUMBER = 4

    # Capacitive Sensor Setup
    CHANNEL_NUM = 11
    SD_THRESHOLD = 5
    EMPTY_THRESHOLD = 120
    HOGGING_THRESHOLD = 100
    mpr121.sensor_init()
    mpr121.set_threshold(0x60)
    mpr121.wait_for_ready()
    readings = np.array([])
    window = 50
    status = "Unoccupied"
    change = False

    # PIR Motion Sensor Setup
    pir_sensor = 8
    led_port = 4
    motion = 0
    grovepi.pinMode(pir_sensor,"INPUT")
    grovepi.pinMode(led_port, "OUTPUT")
    last_motion = datetime.now()
    max_delta = timedelta(seconds=3)
    # max_delta = timedelta(hours=2)

    #MQTT Client setup
    client = mqtt.Client(client_id="T5")
    client.username_pw_set(username="iotcollabhuat", password="iott1t5")
    client.connect("18.141.11.6")
    # client.publish("test", "randylovesyellow")

    print("Starting monitoring")
    while True:
        try:
            original_status = status
            now = datetime.now()
            readings_arr = mpr121.listen_sensor_status()
            r = readings_arr[CHANNEL_NUM]
            
            # Add newest reading to array
            readings = np.append(readings, [r])

            # If less than required window of readings, continue taking
            if len(readings) < window:
                continue

            # Remove oldest reading
            readings = np.delete(readings, 0)
            print(readings)
            
            # Get mean and standard deviation
            average = np.mean(readings)
            sd = np.std(readings)
            # print(average)
            # print(sd)
            # If std. deviation > threshold, means change in state
            # if sd >= SD_THRESHOLD:
            #     change = True

            # Motion Sensor logic
            motion=grovepi.digitalRead(pir_sensor)
            if motion == 0 or motion == 1:	# check if reads were 0 or 1 it can be 255 also because of IO Errors so remove those values
                if motion == 1:
                    print ('Motion Detected')
                    last_motion = datetime.now()
                else:
                    print ('-')

            if average > EMPTY_THRESHOLD:
                status = "Unoccupied"
            elif average > HOGGING_THRESHOLD:
                # status = "Items on desk"
                status = "Occupied"
            else:
                # status = "Laptop on desk"
                status = "Occupied"

            time_difference = now - last_motion
            # if the time difference if greater than 2 hours and the status is not unoccupied , means hogging
            if time_difference >= max_delta and status != "Unoccupied":
                status = "Hogged"
                
            print(status)
            print(original_status)

            if status != original_status:
                change = True
            # change in statuses must be sent to server via MQTT
            if change:
                print("MQTT code here")
                # msg = {'id': SEAT_NUMBER, 'timestamp': str(now), 'occStatus': OccupancyStatus.OccupancyStatus[status].value}
                # msg = json.dumps(msg)
                msg = "['" + str(SEAT_NUMBER) +"','" + str(now) + "','" + str(OccupancyStatus.OccupancyStatus[status].value) + "']"
                print(msg)
                client.publish("hd/status", msg)
                print("Data sent")
                msg = ""
                
            change = False
            time.sleep(0.25)

            if status == "Hogged" or status == "Unoccupied":
                grovepi.digitalWrite(led_port, 255)
            else:
                grovepi.digitalWrite(led_port, 0)
            
        except IOError:
            print("IO Error")
        except Exception as e:
            print(e)

if __name__  == '__main__':
    main()
