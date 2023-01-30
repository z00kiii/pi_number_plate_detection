import paho.mqtt.client as paho
from config import parkplatz_id, parkplatz_lot_id


def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))


def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))


client = paho.Client()
# set callbacks
client.on_subscribe = on_subscribe
client.on_message = on_message
# connect to broker and subscrube to topics
client.connect('5.75.148.247', 1883)
client.subscribe("status/#", qos=1)
client.subscribe("heartbeat/#", qos=1)

client.loop_forever()
