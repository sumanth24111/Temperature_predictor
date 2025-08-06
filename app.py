import pandas as pd
import numpy as np
import re
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib

# Load dataset
data = pd.read_csv('climate_data.csv')

# Convert date column to datetime format
data['dt'] = pd.to_datetime(data['dt'], errors='coerce')

# Drop rows with invalid dates
data = data.dropna(subset=['dt'])

# Extract features from the date
data['year'] = data['dt'].dt.year
data['month'] = data['dt'].dt.month
data['day'] = data['dt'].dt.day

# Function to convert latitude and longitude
def convert_coordinate(coord):
    if isinstance(coord, str):
        value = float(re.sub(r'[^0-9.]', '', coord))  # Remove non-numeric characters
        if 'S' in coord or 'W' in coord:
            return -value  # South and West are negative
        return value
    return coord

# Convert latitude and longitude
data['Latitude'] = data['Latitude'].apply(convert_coordinate)
data['Longitude'] = data['Longitude'].apply(convert_coordinate)

# Define features and target
features = ['year', 'month', 'day', 'Latitude', 'Longitude']
target = 'AverageTemperature'

# Drop rows with missing target values
data = data.dropna(subset=[target])

X = data[features]
y = data[target]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Feature scaling
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Train XGBoost model
model = XGBRegressor(n_estimators=100, learning_rate=0.1, max_depth=5, random_state=42)
model.fit(X_train, y_train)

# Save model and scaler
joblib.dump(model, 'temperature_prediction_model.pkl')
joblib.dump(scaler, 'scaler.pkl')

# Predictions
y_pred = model.predict(X_test)

# Model evaluation
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f'MAE: {mae}, MSE: {mse}, R² Score: {r2}')
