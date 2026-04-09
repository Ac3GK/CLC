from datetime import datetime
from .Humidity import Humidity

def read_humidity():
    value = 0  # placeholder (or real sensor value)
    time = datetime.now()
    return Humidity(value, time)