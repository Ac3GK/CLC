import smbus2
import time

HTS221_I2C_ADDRESS = 0x5F

TEMP_OUT_L = 0x2A
TEMP_OUT_H = 0x2B
CTRL_REG1 = 0x20

bus = smbus2.SMBus(1)

def init_hts221():
    bus.write_byte_data(HTS221_I2C_ADDRESS, CTRL_REG1, 0x85)
def read_temperature():
    temp_l = bus.read_byte_data(
        HTS221_I2C_ADDRESS, TEMP_OUT_L) 
    temp_h = bus.read_byte_data(
        HTS221_I2C_ADDRESS, TEMP_OUT_H)
    temp_raw = (temp_h << 8)|temp_l
    if temp_raw > 32767:
        temp_raw -= 65536
    T0_degC = 0
    T1_degC = 0
    T0_OUT = 0
    T1_OUT = 0
    
    T0_degC = bus.read_byte_data(HTS221_I2C_ADDRESS, 0x32)| ((bus.read_byte_data(HTS221_I2C_ADDRESS, 0x35) & 0x03) << 8)
    T1_degC = bus.read_byte_data(HTS221_I2C_ADDRESS, 0x33)| ((bus.read_byte_data(HTS221_I2C_ADDRESS, 0x35) & 0x0C) << 6)
    
    T0_degC /= 8.0 
    T1_degC /= 8.0 
    
    T0_OUT = bus.read_byte_data(HTS221_I2C_ADDRESS, 0x3C) | (bus.read_byte_data(HTS221_I2C_ADDRESS, 0x3D) << 8)
    T1_OUT = bus.read_byte_data(HTS221_I2C_ADDRESS, 0x3E) | (bus.read_byte_data(HTS221_I2C_ADDRESS, 0x3F) << 8)
    
    if T0_OUT > 32767:
        T0_OUT -= 65536
    if T1_OUT > 32767:
        T1_OUT -= 65536
        
    temperature = T0_degC + (temp_raw - T0_OUT) * (T1_degC - T0_degC) / (T1_OUT - T0_OUT)
    return round(temperature, 2)

if __name__ == "__main__":
    init_hts221()
    time.sleep(0.5)
    
    temp = read_temperature()
    print(f"Temperature: {temp} degree C")

    
        
        
    
    
    

