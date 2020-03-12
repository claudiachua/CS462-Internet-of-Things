import paho.mqtt.client as mqtt

def create_client(c_id):
    client = mqtt.Client(client_id=c_id)
    client.username_pw_set(username="iotcollabhuat", password="iott1t5")
    client.connect("18.141.11.6")
    return client
    
def publish_motion_results(client,msg):
    client.publish("mr/motion",msg)
    
def publish_tof_results(client,msg):
    client.publish("mr/tof",msg)