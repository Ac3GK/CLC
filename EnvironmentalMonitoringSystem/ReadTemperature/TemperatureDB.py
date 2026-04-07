from Temperature import *
import sqlite3
from datetime import datetime


# 1. Connect to SQLite DB (creates file if not exists)
conn = sqlite3.connect("temperature.db")
cursor = conn.cursor()

# 2. Create table (only runs once)
cursor.execute("""
CREATE TABLE IF NOT EXISTS temperature_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    temperature REAL,
    timestamp TEXT
)
""")

# 3. Function to insert data
def insert_temperature(temp):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        "INSERT INTO temperature_log (temperature, timestamp) VALUES (?, ?)",
        (temp, timestamp)
    )
    conn.commit()

# 4. Main loop (example)
for _ in range(5):
    temp = read_temperature()
    insert_temperature(temp)
    print(f"Saved: {temp} at {datetime.now()}")
    time.sleep(1)

# 5. Close connection
conn.close()