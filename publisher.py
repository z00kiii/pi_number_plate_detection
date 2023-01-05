import paho.mqtt.client as paho
import time


class Publisher:
    def __init__(self, id: str):
        """Init the Publisher and Connect to the Broker"""
        self.client = paho.Client(client_id=id)
        self.client.on_connect = self.on_connect
        self.client.connect(host="5.75.148.247", port=1883)
        self.client.loop_start()

        self.id = id
        self.lot_free = True
        self.lot_status_counter = 1

    def on_connect(self, client, userdata, flags, rc):
        print("CONNACK received with code %d." % (rc))

    def on_publish(self, client, userdata, mid):
        print("mid: " + str(mid))

    def set_lot_free(self, lot_free_update):
        """Check if the lot_free status changes
        wait for 3 calls if the status stays the same
        then send status to broker"""
        print(lot_free_update)
        if self.lot_free == lot_free_update:
            # only increment status_counter up to 4 to not count infitly long
            if self.lot_status_counter < 4:
                self.lot_status_counter += 1
            # send status on the 3. call
            if self.lot_status_counter == 3:
                self.send_status(self.lot_free)
        # when lot status changes reset the counter
        else:
            self.lot_status_counter = 1
        self.lot_free = lot_free_update

    def send_status(self, lot_free):
        msg = {"id": id, "time": time.time(), "lot_free": lot_free}
        (rc, mid) = self.client.publish("parkinglot/status", str(msg), qos=1)
