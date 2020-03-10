from postgresCRUD import *
import paho.mqtt.client as mqttClient
import time, ast
 
def on_connect(client, userdata, flags, rc):

    if rc == 0:
 
        print("Connected to broker")
 
        global Connected                #Use global variable
        Connected = True                #Signal connection 
 
    else:
 
        print("Connection failed") 
 
def on_message(client, userdata, message):
    msg = str(message.payload.decode("utf-8"))
    msg_list = ast.literal_eval(msg)
    id = msg_list[0]
    ts = msg_list[1]
    update_hd_hb(id, ts)   

Connected = False #global variable for the state of the connection

broker_address= "localhost"
port = 1883
user = "iotcollabhuat"
password = "iott1t5"

client = mqttClient.Client("IOTCollabHuat")               #create new instance
client.username_pw_set(user, password=password) #set username and password
client.on_connect= on_connect #attach function to callback
client.on_message= on_message #attach function to callback
client.connect(broker_address, port=port) #connect to broker
client.loop_start()                        #start the loop
 
while Connected != True:    #Wait for connection
    time.sleep(0.1)

client.subscribe("hb/hd") # Change to subcribe topic 

try:
    while True:
        time.sleep(1)
 
except KeyboardInterrupt:
    print ("exiting")
    client.disconnect()
    client.loop_stop()