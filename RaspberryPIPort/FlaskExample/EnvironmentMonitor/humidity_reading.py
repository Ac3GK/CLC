import smbus2
from datetime import datetime
from .Humidity import Humidity

# HTS221 I2C Address and Registers
HTS221_ADDRESS = 0x5F
CTRL_REG1 = 0x20
HUMIDITY_OUT_L = 0x28
HUMIDITY_OUT_H = 0x29
H0_RH_X2 = 0x30
H1_RH_X2 = 0x31
H0_T0_OUT_L = 0x36
H0_T0_OUT_H = 0x37
H1_T0_OUT_L = 0x3A
H1_T0_OUT_H = 0x3B

bus = smbus2.SMBus(1)

def read_register(reg):
    return bus.read_byte_data(HTS221_ADDRESS, reg)

def write_register(reg, value):
    bus.write_byte_data(HTS221_ADDRESS, reg, value)

def read_humidity():
    # Set Power ON and 1Hz Update Rate (0x81)
    write_register(0x20, 0x81) 

    # Wait for Humidity Data Ready (Bit 1 in Status Register 0x27)
    for _ in range(10):
        status = read_register(0x27)
        if status & 0x02: # Humidity data available
            break
        time.sleep(0.1)

    # 2. Read humidity calibration data
    h0_rh = read_register(H0_RH_X2) / 2.0
    h1_rh = read_register(H1_RH_X2) / 2.0
    
    h0_t0_out = read_register(H0_T0_OUT_L) | (read_register(H0_T0_OUT_H) << 8)
    if h0_t0_out > 32767: h0_t0_out -= 65536
        
    h1_t0_out = read_register(H1_T0_OUT_L) | (read_register(H1_T0_OUT_H) << 8)
    if h1_t0_out > 32767: h1_t0_out -= 65536

    # 3. Read raw humidity output
    h_out = read_register(HUMIDITY_OUT_L) | (read_register(HUMIDITY_OUT_H) << 8)
    if h_out > 32767: h_out -= 65536

    # 4. Interpolate and calculate Humidity %
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Avoid division by zero
    if (h1_t0_out - h0_t0_out) == 0:
        return Humidity(0, timestamp)

    humidity_val = h0_rh + (h_out - h0_t0_out) * (h1_rh - h0_rh) / (h1_t0_out - h0_t0_out)
    
    # Constrain to 0-100% and round
    humidity_val = max(0, min(100, round(humidity_val, 2)))
    
    return Humidity(humidity_val, timestamp)