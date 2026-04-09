from flask import Blueprint, render_template, request, jsonify
from .TemperatureDB import TemperatureDB
from .temp_reading import read_temperature
import matplotlib.dates as mdates
from datetime import datetime
import matplotlib.pyplot as plt
import io
import base64

bp = Blueprint('pages', __name__)

@bp.route('/')
def home():
    return render_template('pages/home.html') 

@bp.route('/about')
def about():
    return render_template('pages/about.html')


@bp.route('/api/temperature', methods=['GET'])
def get_temperature():
    temp_obj = read_temperature()  # ✅ renamed to avoid confusion

    temperature_db = TemperatureDB()
    temperature_db.insert_temperature(temp_obj)
    temperature_db.close()

    return jsonify({
        "temperature": temp_obj.get_value(),
        "unit": "°C"
    })


@bp.route('/temperature-by-date', methods=['GET'])
def temperature_by_date():
    timestamp = request.args.get('timestamp')
    temperaturedb = TemperatureDB()

    if not timestamp:
        return jsonify({"error": "timestamp is required"}), 400

    try:
        date_str, rows = temperaturedb.get_temperatures_by_date_from_timestamp(timestamp)
    except ValueError:
        return jsonify({"error": "Invalid timestamp"}), 400

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
    plt.ylabel("Temperature (°C)")
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
    plt.close()  # ✅ prevents memory issues

    return jsonify({
        "date": date_str,
        "graph": image_base64
    })