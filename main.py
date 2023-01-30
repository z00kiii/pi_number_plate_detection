import datetime
import threading

from config import parkplatz_id, parkplatz_lot_id
from numberplate_recognition import detect_numberplate
import sensor
import publisher


# in which intervals the hearbeat should be sent. time in sec
HEARTBEAT_INTERVAL = 600

# in which intervals to check the sensor. time in sec
SENSOR_INTERVAL = 10


class Main:
    """Main class contains all business logic"""

    def __init__(self, parkplatz_id, parkplatz_lot_id):
        self.id = parkplatz_id + "/" + parkplatz_lot_id
        # lot_status_counter for delayed action on change of lot status
        self.lot_status_counter = 0
        # init with lot not free
        self.lot_free = False

        # init publisher
        self.publisher = publisher.Publisher(self.id)

        # start send_heartbeat
        self.send_heartbeat()

        # start update_lot_free
        self.update_lot_free()

    def update_lot_free(self):
        """Check if the lot_free status changes
        wait for 3 calls if the status stays the same
        then send status to broker"""
        # get sensor data
        lot_free_update = sensor.get_lot_free()

        # if the status on previous check is the same as the new status
        # this construct should delay the send_lot_status method to 2 same updates in a row
        if self.lot_free == lot_free_update:
            # only increment status_counter up to 2 to not count infitly long
            if self.lot_status_counter < 2:
                self.lot_status_counter += 1
            # send status on the 2. time same status. this ensures a message is only sent once for each status
            if self.lot_status_counter == 1:
                # if lot is not free get the numberplate
                if not lot_free_update:
                    numberplates = detect_numberplate()
                else:
                    numberplates = ""
                self.send_lot_status(lot_free_update, numberplates)
        # when lot status changes reset the counter
        else:
            self.lot_status_counter = 0
        self.lot_free = lot_free_update
        # Start the timer for new status check
        threading.Timer(SENSOR_INTERVAL, self.update_lot_free).start()

    def send_lot_status(self, lot_free, numberplates):
        """Send the new status of the lot to the broker"""
        msg = '{"id": '+ self.id +', "timestamp": ' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ', "lot_free": ' +lot_free +', "number_plate": ' +numberplates +'}'
        self.publisher.publish("status/"+self.id, msg, qos=1)

    def send_heartbeat(self):
        """Send hearbeat signal to the broker"""
        self.publisher.publish("heartbeat/"+self.id, "heartbeatcheck", qos=1)
        # Start timer for new beat
        threading.Timer(HEARTBEAT_INTERVAL, self.send_heartbeat).start()


if __name__ == "__main__":
    Main(parkplatz_id, parkplatz_lot_id)
