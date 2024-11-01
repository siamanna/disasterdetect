from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

app = Flask(__name__)
load_dotenv()

# API endpoints and keys
api_key = os.getenv("VISUAL_CROSSING_API_KEY")
BASE_URL = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"
USGS_BASE_URL = "https://earthquake.usgs.gov/fdsnws/event/1/query"

# Function to get weather data
def get_weather_data(location):
    url = f"{BASE_URL}/{location}"
    params = {
        "unitGroup": "metric",
        "key": api_key,
        "contentType": "json"
    }
    response = requests.get(url, params=params)
    return response.json() if response.status_code == 200 else None

# Function to get earthquake data
def get_earthquake_data():
    start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    end_date = datetime.now().strftime('%Y-%m-%d')
    params = {
        "format": "geojson",
        "starttime": start_date,
        "endtime": end_date,
        "minlatitude": 16.0,
        "maxlatitude": 28.5,
        "minlongitude": 92.2,
        "maxlongitude": 101.2,
    }
    response = requests.get(USGS_BASE_URL, params=params)
    return response.json() if response.status_code == 200 else None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    location = request.form.get('location') or "Myanmar"

    # Fetch weather data
    weather_data = get_weather_data(location)

    # Example flood risk prediction logic
    flood_risk = "Low"
    if weather_data and "days" in weather_data:
        today_weather = weather_data["days"][0]
        flood_risk = "High" if today_weather.get("precip", 0) > 50 else "Low"

    # Fetch earthquake data
    earthquake_data = get_earthquake_data()

    # Render the result page with all data
    return render_template(
        'result.html',
        location=location,
        latitude=weather_data["latitude"] if weather_data else "N/A",
        longitude=weather_data["longitude"] if weather_data else "N/A",
        temperature=weather_data["days"][0].get("temp", "N/A") if weather_data else "N/A",
        precipitation=weather_data["days"][0].get("precip", "N/A") if weather_data else "N/A",
        humidity=weather_data["days"][0].get("humidity", "N/A") if weather_data else "N/A",
        wind_speed=weather_data["days"][0].get("windspeed", "N/A") if weather_data else "N/A",
        flood_risk=flood_risk,
        earthquake_data=earthquake_data["features"] if earthquake_data else []
    )

@app.template_filter('datetimeformat')
def datetimeformat(value):
    return datetime.fromtimestamp(value / 1000).strftime('%Y-%m-%d %H:%M:%S')

if __name__ == "__main__":
    app.run(debug=True)
