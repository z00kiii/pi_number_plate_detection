import time
from publisher import Publisher
from config import parkplatz_id, parkplatz_lot_id
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
ads = ADS.ADS1115(i2c)

# Create single-ended input on channels
chan0 = AnalogIn(ads, ADS.P0)

# create Publisher Instance with ids
publisher = Publisher(parkplatz_id=parkplatz_id, parkplatz_lot_id=parkplatz_lot_id)

# voltage threshold to reach from sensor input 
threshold = 1.2

while True:
    sensor_data = chan0.voltage
    # print(sensor_data)
    publisher.set_lot_free(sensor_data < threshold)
    time.sleep(10)
