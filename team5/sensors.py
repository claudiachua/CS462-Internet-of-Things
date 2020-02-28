#!/usr/bin/env python

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
import time, grovepi, enum
from grove.i2c import Bus
from datetime import datetime, timedelta
import numpy as np
import paho.mqtt.client as mqtt


TOUCH_SENSOR_DEFAULT_ADDR                 = 0x5b

MODE_CONFIG_REG_ADDR                      = 0x5e
GLOBAL_PARAM_REG_ADDR_L                   = 0x5c
TOUCH_STATUS_REG_ADDR_L                   = 0x00
SET_DEBOUNCE_REG_ADDR                     = 0x5b

FILTERED_DATA_REG_START_ADDR_L            = 0x04
CHANNEL_NUM                               = 12

STOP_MODE                                 = 0
NORMAL_MODE                               = 0x3c

class Grove12KeyCapTouchMpr121():
    def __init__(self,bus_num = 1,addr = TOUCH_SENSOR_DEFAULT_ADDR):
        self.bus = Bus(bus_num)
        self.addr = addr
        self.threshold = 0
        self.touch_flag = [0]*CHANNEL_NUM

    def sensor_init(self):
        self._set_mode(STOP_MODE)
        data = [0x23,0x10]
        self._set_global_param(data)
        self._set_debounce(0x22)
        self._set_mode(NORMAL_MODE)

    def set_threshold(self,threshold):
        self.threshold = threshold

    def wait_for_ready(self):
        time.sleep(.2)

    def _set_mode(self,mode):
        self.bus.write_byte_data(self.addr,MODE_CONFIG_REG_ADDR,mode)
    
    def _set_global_param(self,data):
        self.bus.write_i2c_block_data(self.addr,GLOBAL_PARAM_REG_ADDR_L,data)
    
    def _set_debounce(self,data):
        self.bus.write_byte_data(self.addr,SET_DEBOUNCE_REG_ADDR,data)

    def _check_status_register(self):
        data_status = self.bus.read_i2c_block_data(self.addr,TOUCH_STATUS_REG_ADDR_L,2)
        return data_status
    
    def get_filtered_touch_data(self,sensor_status):
        result_value = []
        for i in range(CHANNEL_NUM):
            time.sleep(.01)
            if(sensor_status & (1<<i)):
                channel_data = self.bus.read_i2c_block_data(self.addr,FILTERED_DATA_REG_START_ADDR_L+2*i,2)
                result_value.append(channel_data[0] | channel_data[1]<<8 )
            else:
                result_value.append(0)
        return result_value

    def listen_sensor_status(self):
        data = self._check_status_register()
        touch_status = data[0] | (data[1]<<8) 
        touch_result_value = self.get_filtered_touch_data(touch_status)

        for i in range(CHANNEL_NUM):
            if(touch_result_value[i] < self.threshold ):
                touch_result_value[i] = 0
        return touch_result_value
    
    def parse_and_print_result(self,result):
        for i in range(CHANNEL_NUM):
            if(result[i] != 0):
                if(0 == self.touch_flag[i]):
                    self.touch_flag[i] = 1
                    print("Channel %d is pressed,value is %d" %(i,result[i]))
            else:
                if(1 == self.touch_flag[i]):
                    self.touch_flag[i] = 0
                    print("Channel %d is released,value is %d" %(i,result[i]))
        
class SeatStatus(enum.Enum):
    Unoccupied = 1
    Occupied = 2
    Hogged = 3

mpr121 = Grove12KeyCapTouchMpr121() 
def main():
    # Admin attributes
    SEAT_NUMBER = 4

    # Capacitive Sensor Setup
    CHANNEL_NUM = 11
    SD_THRESHOLD = 5
    MEAN_THRESHOLD = 135
    HOGGING_THRESHOLD = 100
    mpr121.sensor_init()
    mpr121.set_threshold(0x60)
    mpr121.wait_for_ready()
    readings = np.array([])
    window = 10
    status = "Unoccupied"
    change = False

    # PIR Motion Sensor Setup
    pir_sensor = 8
    motion = 0
    grovepi.pinMode(pir_sensor,"INPUT")
    last_motion = datetime.now()
    max_delta = timedelta(seconds=3)
    # max_delta = timedelta(hours=2)

    #MQTT Client setup
    client = mqtt.Client(client_id="Grp4")
    client.username_pw_set(username="iotcollabhuat", password="iott1t5")
    client.connect("18.141.11.6")
    client.publish("test", "randylovesyellow")

    while True:
        try:
            original_status = status
            now = datetime.now()
            r = mpr121.listen_sensor_status()
            r = r[CHANNEL_NUM]

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

            if average > MEAN_THRESHOLD:
                status = "Unoccupied"
            elif average > HOGGING_THRESHOLD:
                status = "Items on desk"
            else:
                status = "Laptop on desk"

            time_difference = now - last_motion
            # if the time difference if greater than 2 hours and the status is not unoccupied , means hogging
            if time_difference >= max_delta and status != "Unoccupied":
                status = "Hogging"
            else:
                print("we gucci")
                
            print(status)

            if original_status != status:
                change = True
            # change in statuses must be sent to server via MQTT
            if change:
                print("MQTT code here")
            change = False
            time.sleep(1)
            
        except IOError:
            print("IO Error")
        except Exception as e:
            print(e)

if __name__  == '__main__':
    main()
