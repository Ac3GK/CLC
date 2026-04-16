from .Gas import Gas
import sqlite3
from datetime import datetime

class GasDB:
    def __init__(self):
        self.conn = sqlite3.connect("gas.db")
        self.cursor = self.conn.cursor()

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS gas_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            gas REAL,
            timestamp TEXT
        )
        """)
        self.conn.commit()

    def insert_gas(self, gas):
        self.cursor.execute(
            "INSERT INTO gas_log (gas, timestamp) VALUES (?, ?)",
            (gas.get_value(), gas.get_timestamp())
        )
        self.conn.commit()

    def close(self):
        self.conn.close()