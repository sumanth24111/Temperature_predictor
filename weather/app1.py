from flask import Flask, render_template, request, jsonify, redirect, url_for
import pandas as pd
import joblib
import re
import os
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)

# Ensure uploaded files directory exists
os.makedirs("uploaded_files", exist_ok=True)

# Load trained model and scaler
model = joblib.load("temperature_prediction_model.pkl")
scaler = joblib.load("scaler.pkl")

# Function to clean and convert latitude & longitude
def convert_coordinate(coord):
    if isinstance(coord, str):
        value = float(re.sub(r'[^0-9.]', '', coord))
        if 'S' in coord or 'W' in coord:
            return -value
        return value
    return coord

# Routes for different pages
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return redirect(url_for("home", error="No file uploaded"))
    
    file = request.files["file"]
    file_path = os.path.join("uploaded_files", file.filename)
    file.save(file_path)

    try:
        new_data = pd.read_csv(file_path)

        if "dt" in new_data.columns:
            new_data["dt"] = pd.to_datetime(new_data["dt"], errors="coerce", dayfirst=True)
            new_data = new_data.dropna(subset=["dt"])
            new_data["year"] = new_data["dt"].dt.year.astype(int)
            new_data["month"] = new_data["dt"].dt.month.astype(int)
            new_data["day"] = new_data["dt"].dt.day.astype(int)
        else:
            return redirect(url_for("home", error="Missing 'dt' column"))

        if "Latitude" in new_data.columns and "Longitude" in new_data.columns:
            new_data["Latitude"] = new_data["Latitude"].apply(convert_coordinate)
            new_data["Longitude"] = new_data["Longitude"].apply(convert_coordinate)
        else:
            return redirect(url_for("home", error="Missing Latitude or Longitude column"))

        features = ["year", "month", "day", "Latitude", "Longitude"]
        new_data = new_data[features]

        new_data_scaled = scaler.transform(new_data)
        predicted_temperature = round(model.predict(new_data_scaled)[0], 2)

        return render_template("result.html", temperature=predicted_temperature)

    except Exception as e:
        return redirect(url_for("home", error=str(e)))

if __name__ == "__main__":
    app.run(debug=True)
