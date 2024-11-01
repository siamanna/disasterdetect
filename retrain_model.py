import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
import joblib

# Load dataset
data = pd.read_csv('flood.csv')  # Make sure the dataset file is in the same directory

# Separate features and target variable
X = data.drop(columns=['FloodProbability'])
y = data['FloodProbability']

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train the Random Forest model
model = RandomForestRegressor(random_state=42, n_jobs=-1)
model.fit(X_train_scaled, y_train)

# Save the model and scaler for compatibility
joblib.dump(model, 'flood_rf_model.joblib')
joblib.dump(scaler, 'scaler.joblib')
