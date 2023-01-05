import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import time
from publisher import Publisher

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
ads = ADS.ADS1115(i2c)

# Create single-ended input on channels
chan0 = AnalogIn(ads, ADS.P0)

# create Publisher Instance with id 69187
publisher = Publisher("69187")

threshold = 1.2

while True:
    sensor_data = chan0.voltage
    # print(sensor_data)
    publisher.set_lot_free(sensor_data > threshold)
    time.sleep(10)
