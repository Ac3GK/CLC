# from .temp_reading import read_temperature
from .Humidity import Humidity
import sqlite3
from datetime import datetime
from time import sleep

class HumidityDB:
    def __init__(self):
        # 1. Connect to SQLite DB (creates file if not exists)
        self.conn = sqlite3.connect("humidity.db")
        self.cursor = self.conn.cursor()

        # 2. Create table (only runs once)
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS humidity_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            humidity REAL,
            timestamp TEXT
        )
        """)
        self.conn.commit()


    def insert_humidity(self, humidity):
        # humidity.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute(
            "INSERT INTO humidity_log (humidity, timestamp) VALUES (?, ?)",
            (humidity.get_value(), humidity.get_timestamp())
        )
        self.conn.commit()

    def get_humidities_by_date_from_timestamp(self, timestamp):
        try:
            dt = datetime.fromtimestamp(int(timestamp))
            date_str = dt.strftime('%Y-%m-%d')
        except Exception:
            raise ValueError("Invalid timestamp")
        
        query = """
            SELECT humidity, timestamp
            FROM humidity_log
            WHERE DATE(timestamp) LIKE ?
            ORDER BY timestamp
        """

        rows = self.conn.execute(query, (f"{date_str}%",)).fetchall()
        # self.conn.close()
        
        return date_str, rows    


    def close(self):
        self.conn.close()

if __name__ == "__main__":
    humidityDB = HumidityDB()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    value = 25.0  # Example temperature value
    for _ in range(5):
        # temp = read_temperature()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        humidity = Humidity(value, timestamp)  # Example temperature value
        humidityDB.insert_humidity(humidity=humidity)
        print(f"Saved: {humidity} at {datetime.now()}")
        sleep(1)
        value += 0.5  # Increment temperature for testing
    

    humidityDB.close()