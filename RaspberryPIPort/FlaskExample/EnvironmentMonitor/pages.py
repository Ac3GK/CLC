from flask import Blueprint, render_template, request, jsonify

# Temperature
from .TemperatureDB import TemperatureDB
from .temp_reading import read_temperature, Temperature

# Humidity
from .humidity_reading import read_humidity, Humidity
from .HumidityDB import HumidityDB

# GAS
from .gas_reading import read_gas_sensor
from .GasDB import GasDB

from .utils import get_stats_from_list

import matplotlib.dates as mdates
from datetime import datetime
import matplotlib.pyplot as plt
import io
import base64

bp = Blueprint('pages', __name__)


# -------------------- PAGES --------------------

@bp.route('/')
def home():
    return render_template('pages/home.html')


@bp.route('/about')
def about():
    return render_template('pages/about.html')


# -------------------- API ROUTES --------------------

@bp.route('/api/temperature', methods=['GET'])
def get_temperature():
    temperature = read_temperature()

    temperature_db = TemperatureDB()
    temperature_db.insert_temperature(temperature)
    temperature_db.close()

    return jsonify({
        "temperature": temperature.get_value(),
        "unit": "\u00b0C"
    })


@bp.route('/api/humidity', methods=['GET'])
def get_humidity():
    humidity = read_humidity()

    humidity_db = HumidityDB()
    humidity_db.insert_humidity(humidity)
    humidity_db.close()

    return jsonify({
        "humidity": humidity.get_value(),
        "unit": "%"
    })


# ? FIXED GAS ROUTE
@bp.route('/api/gas', methods=['GET'])
def get_gas():
    gas = read_gas_sensor() # Update this function call

    gas_db = GasDB()
    gas_db.insert_gas(gas)
    gas_db.close()

    return jsonify({
        "gas": gas.get_value(),
        "unit": "VOC"
    })


# -------------------- GRAPH ROUTES --------------------

@bp.route('/api/temperature-by-date', methods=['GET']) # Added /api/
def temperature_by_date():
    # ... rest of your code
    timestamp = request.args.get('timestamp')
    temperaturedb = TemperatureDB()

    if not timestamp:
        return jsonify({"error": "timestamp is required"}), 400

    try:
        date_str, rows = temperaturedb.get_temperatures_by_date_from_timestamp(timestamp)
    except ValueError:
        return jsonify({"error": "Invalid timestamp"}), 400

    temperaturedb.close()

    if not rows:
        return jsonify({"message": f"No data for {date_str}"}), 404

    # Extract data
    times = []
    for row in rows:
        ts = row[1]

        if isinstance(ts, (int, float)):
            times.append(datetime.fromtimestamp(ts))
        else:
            times.append(datetime.strptime(ts, "%Y-%m-%d %H:%M:%S"))

    temps = [row[0] for row in rows]

    # Plot graph
    plt.figure(figsize=(10, 5))
    plt.plot(times, temps, marker='o')
    plt.xlabel("Time")
    plt.ylabel("Temperature (\u00b0C)")
    plt.title(f"Temperature on {date_str}")

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
    plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())

    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()

    # Convert to image
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()

    return jsonify({
        "date": date_str,
        "graph": image_base64
    })

@bp.route('/api/stats-by-date', methods=['GET'])
def stats_by_date():
    timestamp = request.args.get('timestamp')
    if not timestamp:
        return jsonify({"error": "timestamp is required"}), 400

    temp_db = TemperatureDB()
    hum_db = HumidityDB()
    gas_db = GasDB()

    try:
        _, temp_rows = temp_db.get_temperatures_by_date_from_timestamp(timestamp)
        _, hum_rows = hum_db.get_humidities_by_date_from_timestamp(timestamp)
        _, gas_rows = gas_db.get_gas_by_date_from_timestamp(timestamp)
    finally:
        # Always close connections
        temp_db.close()
        hum_db.close()
        gas_db.close()

    # Apply your BST logic from utils.py
    t_min, t_max = get_stats_from_list([r[0] for r in temp_rows])
    h_min, h_max = get_stats_from_list([r[0] for r in hum_rows])
    g_min, g_max = get_stats_from_list([r[0] for r in gas_rows])

    return jsonify({
        "temperature": {"min": t_min, "max": t_max},
        "humidity": {"min": h_min, "max": h_max},
        "gas": {"min": g_min, "max": g_max}
    })
