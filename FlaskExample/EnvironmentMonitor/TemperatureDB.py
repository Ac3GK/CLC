from .temp_reading import read_temperature
from .Temperature import Temperature
import sqlite3
from datetime import datetime
from time import sleep

class TemperatureDB:
    def __init__(self):
        # 1. Connect to SQLite DB (creates file if not exists)
        self.conn = sqlite3.connect("temperature.db")
        self.cursor = self.conn.cursor()

        # 2. Create table (only runs once)
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS temperature_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            temperature REAL,
            timestamp TEXT
        )
        """)
        self.conn.commit()


    def insert_temperature(self, temp):
        # temp.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute(
            "INSERT INTO temperature_log (temperature, timestamp) VALUES (?, ?)",
            (temp.get_value(), temp.get_timestamp())
        )
        self.conn.commit()

    def get_temperatures_by_date_from_timestamp(self, timestamp):
        try:
            dt = datetime.fromtimestamp(int(timestamp))
            date_str = dt.strftime('%Y-%m-%d')
        except Exception:
            raise ValueError("Invalid timestamp")
        
        query = """
            SELECT temperature, timestamp
            FROM temperature_log
            WHERE DATE(timestamp) LIKE ?
            ORDER BY timestamp
        """

        rows = self.conn.execute(query, (f"{date_str}%",)).fetchall()
        # self.conn.close()
        
        return date_str, rows    


    def close(self):
        self.conn.close()

if __name__ == "__main__":
    temp_db = TemperatureDB()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    value = 25.0  # Example temperature value
    for _ in range(5):
        # temp = read_temperature()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        temp = Temperature(value, timestamp)  # Example temperature value
        temp_db.insert_temperature(temp)
        print(f"Saved: {temp.get_value()} at {datetime.now()}")
        sleep(1)
        value += 0.5  # Increment temperature for testing
    

    temp_db.close()