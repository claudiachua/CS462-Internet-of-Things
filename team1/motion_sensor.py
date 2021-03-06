
#!/usr/bin/env python
#
# GrovePi Example for using the Grove PIR Motion Sensor (http://www.seeedstudio.com/wiki/Grove_-_PIR_Motion_Sensor)
#
# The GrovePi connects the Raspberry Pi and Grove sensors.  You can learn more about GrovePi here:  http://www.dexterindustries.com/GrovePi
#
# Have a question about this example?  Ask on the forums here:  http://forum.dexterindustries.com/c/grovepi
#
'''
## License

The MIT License (MIT)

GrovePi for the Raspberry Pi: an open source platform for connecting Grove Sensors to the Raspberry Pi.
Copyright (C) 2017  Dexter Industries

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
# NOTE:
# 	There are also 2x potentiometers on the board for adjusting measuring distance and hold time
# 	Rotate the pot labelled "Delay time" clockwise to decrease the hold time (0.3s - 25s)
# 	Rotate the pot labelled "Distance" clockwise to decrease the measuring distance (10cm - 6m)
	
# 	There are multiple revisions of this board with different components for setting retriggerable/non-retriggerable.
# 	Revision 1.0 contains a switch and revision 1.2 contains a jumper hat.
# 	The 1.0 switch board is labelled with H,L - H=retriggerable, L=non-retriggerable.
# 	The 1.2 jumper board has a pin diagram printed on the back.
	
# 	retriggerable means the sensor will continue outputting high if motion was detected before the hold timer expires.
# 	non-retriggerable means the sensor will output high for the specified hold time only, then output low until motion is detected again.
# 	if there is constant motion detected, retriggerable will stay high for the duration and non-retriggerable will oscillate between high/low.

import time
import grovepi
import datetime
from mqtt_conn import *
from datetime import datetime, timedelta
import heartbeat

# Connect the Grove PIR Motion Sensor to digital port D8
# NOTE: Some PIR sensors come with the SIG line connected to the yellow wire and some with the SIG line connected to the white wire.
# If the example does not work on the first run, try changing the pin number
# For example, for port D8, if pin 8 does not work below, change it to pin 7, since each port has 2 digital pins.
# For port 4, this would pin 3 and 4

def write_error():
    f = file.open("motion_error.txt","a")
    f.write("IOError detecting motion @ " + str(datetime.datetime.now()))
    f.close()

pir_sensor = 7
motion=0
grovepi.pinMode(pir_sensor,"INPUT")
client = create_client("grp5_motion")
motion_counter = 0
time_in_sec = 0
start_time = datetime.now()
heartbeat_delta = timedelta(minutes=1)
curr_reading = 0
prev_reading = 0
no_motion_count = 0

while True:
    print("Start detecting")
    heartbeat_check = datetime.now()
    if (heartbeat_check - start_time) >= heartbeat_delta:
        heartbeat.send_heartbeat(client, "E_Motion")
        start_time = heartbeat_check

    try:
        # Sense motion, usually human, within the target range
        print("Motion Counter",str(motion_counter))
        print("Time in seconds",str(time_in_sec))
        motion=grovepi.digitalRead(pir_sensor)
        if motion == 1:
            time_in_sec += 1
            motion_counter += 1
        elif motion == 0:
            print("No motion detected")
            time_in_sec += 1
        else:
            write_error()
            # if your hold time is less than this, you might not see as many detections
        time.sleep(1)
        if time_in_sec==60:
            time_in_sec=0
            now = str(datetime.now())
            if  motion_counter>=2:
                no_motion_count = 0
                curr_reading = 2
                    #send to topic
                msg = "['E','" + now + "','2']"
                if curr_reading != prev_reading:    
                    publish_motion_results(client,msg)
                    print("Data sent")
            else:
                no_motion_count += 1
                curr_reading = 0
                if no_motion_count >= 5:
                    msg = "['E','" + now + "','0']"
                    no_motion_count = 0      
                    publish_motion_results(client,msg)
                    print("Data sent")
            print(no_motion_count)
            prev_reading = curr_reading
            motion_counter = 0
    except IOError:
        write_error()

print("exit")
