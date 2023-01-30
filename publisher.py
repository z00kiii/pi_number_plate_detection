import paho.mqtt.client as paho


class Publisher:
    """MQTT Client that publishes Content to the Broker"""

    def __init__(self, id):
        """init the Publisher and Connect to the Broker"""
        self.id = id

        self.client = paho.Client(client_id=self.id)
        self.client.on_connect = self.on_connect
        # connect to broker
        self.client.connect(host="5.75.148.247", port=1883)
        # loop for enduring connection
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        print("CONNACK received with code %d." % (rc))

    def on_publish(self, client, userdata, mid):
        print("mid: ", str(mid), "data: " + str(userdata))

    def publish(self, topic, msg, qos):
        self.client.publish(topic, msg, qos=qos)
