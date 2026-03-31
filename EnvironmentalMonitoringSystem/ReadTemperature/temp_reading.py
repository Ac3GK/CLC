#JETT WAS HERE
#LUIS WAS HERE
import smbus2
import time
from datetime import datetime

HTS221_I2C_ADDRESS = 0x5F

TEMP_OUT_L = 0x2A
TEMP_OUT_H = 0x2B
CTRL_REG1 = 0x20

bus = smbus2.SMBus(1)

def init_hts221():
    bus.write_byte_data(HTS221_I2C_ADDRESS, CTRL_REG1, 0x85)

def read_temperature():
    temp_l = bus.read_byte_data(HTS221_I2C_ADDRESS, TEMP_OUT_L)
    temp_h = bus.read_byte_data(HTS221_I2C_ADDRESS, TEMP_OUT_H)
    temp_raw = (temp_h << 8) | temp_l

    if temp_raw > 32767:
        temp_raw -= 65536

    # Calibration values
    T0_degC = bus.read_byte_data(HTS221_I2C_ADDRESS, 0x32) | \
             ((bus.read_byte_data(HTS221_I2C_ADDRESS, 0x35) & 0x03) << 8)
    T1_degC = bus.read_byte_data(HTS221_I2C_ADDRESS, 0x33) | \
             ((bus.read_byte_data(HTS221_I2C_ADDRESS, 0x35) & 0x0C) << 6)

    T0_degC /= 8.0
    T1_degC /= 8.0

    T0_OUT = bus.read_byte_data(HTS221_I2C_ADDRESS, 0x3C) | \
            (bus.read_byte_data(HTS221_I2C_ADDRESS, 0x3D) << 8)
    T1_OUT = bus.read_byte_data(HTS221_I2C_ADDRESS, 0x3E) | \
            (bus.read_byte_data(HTS221_I2C_ADDRESS, 0x3F) << 8)

    if T0_OUT > 32767:
        T0_OUT -= 65536
    if T1_OUT > 32767:
        T1_OUT -= 65536

    temperature = T0_degC + (temp_raw - T0_OUT) * \
                 (T1_degC - T0_degC) / (T1_OUT - T0_OUT)

    return round(temperature, 2)

if __name__ == "__main__":
    init_hts221()
    time.sleep(0.5)

    readings = []  # List to store (timestamp, temperature)

    print("Collecting temperature data...\n")

    # For testing: run for 10 minutes (use time.sleep(60) for real case)
    for i in range(10):
        current_time = datetime.now()
        temp = read_temperature()

        readings.append((current_time, temp))

        print(f"{current_time.strftime('%H:%M:%S')} -> {temp} °C")

        time.sleep(60)  # Change to smaller value like 5 sec for quick testing

    # Find maximum temperature
    max_reading = max(readings, key=lambda x: x[1])
    max_time, max_temp = max_reading

    print("\n=== Result ===")
    print(f"Maximum Temperature: {max_temp} °C")
    print(f"Occurred at: {max_time.strftime('%H:%M:%S')}")