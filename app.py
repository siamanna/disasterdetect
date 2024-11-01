from flask import Flask, request, render_template
import numpy as np
import joblib

# Load the model and scaler
model = joblib.load('flood_rf_model.joblib')
scaler = joblib.load('scaler.joblib')

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')  # This should be an HTML form for input

@app.route('/resources')
def resources():
    return render_template('resources.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Extract features from form inputs
    features = [float(request.form.get(f)) for f in request.form]
    features = np.array(features).reshape(1, -1)

    # Scale features
    scaled_features = scaler.transform(features)

    # Predict flood probability
    prediction = model.predict(scaled_features)

    return f"Predicted Flood Probability: {prediction[0]:.4f}"

if __name__ == "__main__":
    app.run(debug=True)
