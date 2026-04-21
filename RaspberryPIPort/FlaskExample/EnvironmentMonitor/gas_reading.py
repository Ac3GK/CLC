import board
import adafruit_sgp40
from datetime import datetime
from .Gas import Gas

# Global variables for sensor
i2c = None
sgp = None

def get_sensor():
    global i2c, sgp
    if sgp is None:
        try:
            i2c = board.I2C()
            sgp = adafruit_sgp40.SGP40(i2c)
        except Exception as e:
            print(f"Hardware Init Error: {e}")
    return sgp

def read_gas_sensor():
    sensor = get_sensor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if sensor is None:
        return Gas(0, timestamp)

    try:
        raw_gas = sensor.raw
        return Gas(raw_gas, timestamp)
    except Exception as e:
        print(f"SGP40 Read Error: {e}")
        return Gas(0, timestamp)

def init_mox():
    pass
