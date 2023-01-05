import paho.mqtt.client as paho
import time
import threading

# in which intervals the hearbeat should be sent. time in sec
heartbeatinterval = 600

class Publisher:
    def __init__(self, parkplatz_id: str, parkplatz_lot_id: str):
        """Init the Publisher and Connect to the Broker"""
        self.id = parkplatz_id + "/" + parkplatz_lot_id
        self.lot_free = True
        self.lot_status_counter = 1

        self.client = paho.Client(client_id=self.id)
        self.client.on_connect = self.on_connect
        #self.client.on_publish = self.on_publish
        self.client.connect(host="5.75.148.247", port=1883)
        self.client.loop_start()

        # init heartbeat loop
        self.send_heartbeat()

    def on_connect(self, client, userdata, flags, rc):
        print("CONNACK received with code %d." % (rc))

    def on_publish(self, client, userdata, mid):
        print("mid: ", str(mid), "data: " + str(userdata))

    def set_lot_free(self, lot_free_update):
        """Check if the lot_free status changes
        wait for 3 calls if the status stays the same
        then send status to broker"""
        # print("current_status ",lot_free_update)
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
        """Send the new status of the lot to the broker"""
        msg = {"id": self.id, "time": time.time(), "lot_free": lot_free}
        self.client.publish("status/"+self.id, str(msg), qos=1)

    def send_heartbeat(self):
        """Send hearbeat signal to the broker"""
        # Start timeout for new beat
        threading.Timer(heartbeatinterval, self.send_heartbeat).start()
        self.client.publish("heartbeat/"+self.id, "heartbeatcheck", qos=1)
