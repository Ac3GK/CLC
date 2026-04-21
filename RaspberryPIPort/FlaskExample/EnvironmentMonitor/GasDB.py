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
    
    # INDENT THIS ENTIRE SECTION:
    def get_gas_by_date_from_timestamp(self, timestamp):
        try:
            dt = datetime.fromtimestamp(int(timestamp))
            date_str = dt.strftime('%Y-%m-%d')
        except Exception:
            raise ValueError("Invalid timestamp")
        
        query = """
            SELECT gas, timestamp
            FROM gas_log
            WHERE DATE(timestamp) = ?
            ORDER BY timestamp
        """
        rows = self.cursor.execute(query, (date_str,)).fetchall()
        return date_str, rows
