A machine learning–powered temperature prediction system that trains an XGBoost model on historical climate data using date and location features (year, month, day, latitude, longitude). The trained model is deployed through a Flask web app, where users upload a CSV with dt, Latitude, and Longitude. The app preprocesses the data, scales it with the saved scaler, and returns instant temperature predictions via a simple web interface.
This app provides a fast and intelligent way to estimate temperatures for any given date and location using historical data as its backbone 🌍📊.

Required libraries:
pandas
numpy
scikit-learn
xgboost(recomended==1.7.6)
Flask
joblib

Required columns in training and testing data:
year
month
day
Latitude (cleaned & numeric)
Longitude (cleaned & numeric)

use Train_model.py to train model according to your datasets
after running this file creates temperature_prediction_model.pkl and scaler.pkl models to predict weather
use Test_model.py to test the model and predict the weather

