import paho.mqtt.client as mqtt

def create_client():
    client = mqtt.Client(client_id="Grp5")
    client.username_pw_set(username="iotcollabhuat", password="iott1t5")
    client.connect("18.141.11.6")
    return client
    
def publish_motion_results(client,msg):
    client.publish("mr/motion",msg)