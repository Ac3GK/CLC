import time
from datetime import datetime

# ✅ Correct package imports (works with -m)
try:
    # When running as module
    from .Gas import Gas as GasClass
    from .GasDB import GasDB as GasDBClass
except ImportError:
    # Fallback for running directly in VS Code
    from Gas import Gas as GasClass
    from GasDB import GasDB as GasDBClass


# 2. HARDWARE MOCKING (for Windows / no sensor)
try:
    import smbus  # type: ignore
except ImportError:
    class SMBus:
        def __init__(self, bus): pass
        def read_i2c_block_data(self, addr, reg, length):
            # Dummy TVOC value of 50
            return [0x01, 0x90, 0x00, 0x00, 0x32, 0x00]
        def write_i2c_block_data(self, addr, reg, data): pass

    smbus = type('smbus', (), {'SMBus': SMBus})


# SGP30 MOX Sensor Configuration
MOX_ADDR = 0x58
CMD_INIT_AIR_QUALITY = [0x20, 0x03]
CMD_MEASURE_AIR_QUALITY = [0x20, 0x08]

bus = smbus.SMBus(1)


# 3. CORE LOGIC
def init_mox():
    try:
        bus.write_i2c_block_data(MOX_ADDR, CMD_INIT_AIR_QUALITY[0], [CMD_INIT_AIR_QUALITY[1]])
        time.sleep(0.01)
    except Exception as e:
        print(f"I2C Initialization Error: {e}")


def read_gas_sensor():
    try:
        bus.write_i2c_block_data(MOX_ADDR, CMD_MEASURE_AIR_QUALITY[0], [CMD_MEASURE_AIR_QUALITY[1]])
        time.sleep(0.05)

        data = bus.read_i2c_block_data(MOX_ADDR, 0, 6)

        # Extract TVOC (bytes 3 & 4)
        tvoc_value = (data[3] << 8) | data[4]
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return GasClass(tvoc_value, timestamp)

    except Exception as e:
        print(f"Error reading gas sensor: {e}")
        return None


def get_and_store_gas():
    init_mox()
    gas_data = read_gas_sensor()

    if gas_data:
        db = GasDBClass()
        db.insert_gas(gas_data)
        db.close()
        return gas_data

    return None


# 4. ENTRY POINT
if __name__ == "__main__":
    print("Starting Gas Sensor Read...")

    result = get_and_store_gas()

    if result:
        print(f"Successfully recorded: {result}")
    else:
        print("Failed to record gas data.")