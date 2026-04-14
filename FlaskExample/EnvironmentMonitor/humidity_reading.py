import time

from datetime import datetime

from .Humidity import Humidity


humidity = Humidity(value=None, time=None)
def read_humidity():
    # Add code to read humidity from the sensor and return a Humidity object
    return humidity