from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()
api_key = os.getenv("VISUAL_CROSSING_API_KEY")
BASE_URL = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    location = request.form.get('location')
    latitude = request.form.get('latitude')
    longitude = request.form.get('longitude')

    # Check for either location or coordinates
    if latitude and longitude:
        weather_data = get_weather_data(f"{latitude},{longitude}")
    elif location:
        weather_data = get_weather_data(location)
    else:
        return jsonify({"error": "Please provide a location or enable geolocation."})

    # Determine flood prediction based on weather data
    prediction = "Flood Risk: TBD based on weather data."  # Update this with your prediction logic

    return render_template('result.html', location=location, latitude=latitude, longitude=longitude, weather_data=weather_data, prediction=prediction)

def get_weather_data(api_key, location):
    url = f"https://api.tomorrow.io/v4/weather/realtime?location={location}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None

if __name__ == '__main__':
    app.run(debug=True)
