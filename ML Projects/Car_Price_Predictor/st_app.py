import streamlit as st
import pandas as pd
import pickle
import numpy as np

# Load the car data (assuming 'cleaned_data.csv' is in the same directory)
car_data = pd.read_csv("cleaned_data.csv")

# Load the pickled model (assuming 'LinearRegressionModel.pkl' is in the same directory)
model = pickle.load(open("LinearRegressionModel.pkl", "rb"))

# Function to make predictions
def predict_car_price(company, car_model, year, fuel_type, driven):
    # Create a DataFrame for prediction
    prediction_data = pd.DataFrame({
        "name": [car_model],
        "company": [company],
        "year": [year],
        "kms_driven": [driven],
        "fuel_type": [fuel_type],
    })

    # Predict the car price
    prediction = model.predict(prediction_data)
    return np.round(prediction[0], 2)

# Streamlit app
st.title("Car Price Prediction App")

# Initial state for car models (empty list)
car_model_options = []

# Company selection
company = st.selectbox("Company", sorted(car_data["company"].unique()))

# Filter car models based on company selection
if company:
    car_model_options = sorted(car_data[car_data["company"] == company]["name"].unique())

# Car model selection (use filtered options)
car_model = st.selectbox("Car Model", car_model_options)

year = st.selectbox("Year", sorted(car_data["year"].unique(), reverse=True))
fuel_type = st.selectbox("Fuel Type", car_data["fuel_type"].unique())
driven = st.number_input("Kilometers Driven", min_value=0)

# Call the prediction function
if st.button("Predict Price"):
    prediction = predict_car_price(company, car_model, year, fuel_type, driven)
    st.success(f"The predicted price of your car is: ₹ {prediction}")
