from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()
api_key = os.getenv("VISUAL_CROSSING_API_KEY")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    location = request.form.get('location')
    latitude = request.form.get('latitude')
    longitude = request.form.get('longitude')

    # Use either location or coordinates for weather data
    if latitude and longitude:
        weather_data = get_weather_data(api_key, f"{latitude},{longitude}")
    elif location:
        weather_data = get_weather_data(api_key, location)
    else:
        return jsonify({"error": "Please provide a location or enable geolocation."})

    # Check if weather_data was successfully retrieved
    if weather_data is None:
        return jsonify({"error": "Could not retrieve weather data. Please check your API key and location."})

    # Extract necessary weather data
    values = weather_data.get("data", {}).get("values", {})
    temperature = values.get("temperature", "N/A")
    precipitation = values.get("precipitationProbability", "N/A")
    humidity = values.get("humidity", "N/A")
    wind_speed = values.get("windSpeed", "N/A")

    # Example flood risk prediction
    flood_risk = "Low" if precipitation < 50 else "High"

    # Render result page
    return render_template(
        'result.html',
        location=location,
        latitude=latitude,
        longitude=longitude,
        temperature=temperature,
        precipitation=precipitation,
        humidity=humidity,
        wind_speed=wind_speed,
        flood_risk=flood_risk
    )


def get_weather_data(api_key, location):
    url = f"https://api.tomorrow.io/v4/weather/realtime?location={location}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching weather data: {response.status_code} - {response.text}")
        return None

@app.route('/resources')
def resources():
    return render_template('resources.html')

if __name__ == "__main__":
    app.run(debug=True)