from datetime import datetime
import paho.mqtt.client as mqtt

TOPIC = "hb/hd"
def send_heartbeat(client, id):
    now = datetime.now()
    # msg = "Heartbeat for %s at time: %s" % (str(id),str(now),)
    msg = "['" + str(id)+ "','" + str(now)+"']"
    client.publish(TOPIC, msg)