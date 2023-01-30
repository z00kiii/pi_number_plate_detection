import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# voltage threshold to reach from sensor input
THRESHOLD = 1.08

# create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# create the ADC object using the I2C bus
ads = ADS.ADS1115(i2c)

# create single-ended input on channels
chan0 = AnalogIn(ads, ADS.P0)

def get_lot_free():
    """read input and check if smaller than THRESHOLD"""
    sensor_data = chan0.voltage
    # if sensor_data is bigger than THRESHOLD the lot is occupied
    return sensor_data < THRESHOLD

