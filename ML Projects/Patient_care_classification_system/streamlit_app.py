

import numpy as np
import pandas as pd
import streamlit as st
import pickle
from sklearn.ensemble import RandomForestClassifier

st.header("Patient Care Classification System")

# Load the trained Random Forest model from the pickle file
with open("/workspaces/The-Grand-Complete-Data-Science-Materials/ML Projects/Patient_care_classification_system/random_forest_model.pkl", "rb") as model_file:
    rf_model = pickle.load(model_file)

# User input
st_HAEMATOCRIT = st.number_input("Enter HAEMATOCRIT Value: ")
st_HAEMOGLOBINS = st.number_input("Enter HAEMOGLOBINS Value: ")
st_ERYTHROCYTE = st.number_input("Enter ERYTHROCYTE Value: ")
st_LEUCOCYTE = st.number_input("Enter LEUCOCYTE Value: ")
st_THROMBOCYTE = st.number_input("Enter THROMBOCYTE Value: ")
st_MCH = st.number_input("Enter MCH Value: ")
st_MCHC = st.number_input("Enter MCHC Value: ")
st_MCV = st.number_input("Enter MCV Value: ")
st_AGE = st.number_input("Enter AGE Value: ")
st_SEX = st.number_input("Enter SEX (Enter 1 for Male and 0 for Female) Value: ")

user_data = [
    [
        st_HAEMATOCRIT,
        st_HAEMOGLOBINS,
        st_ERYTHROCYTE,
        st_LEUCOCYTE,
        st_THROMBOCYTE,
        st_MCH,
        st_MCHC,
        st_MCV,
        st_AGE,
        st_SEX,
    ]
]
cols = [
    [
        "HAEMATOCRIT",
        "HAEMOGLOBINS",
        "ERYTHROCYTE",
        "LEUCOCYTE",
        "THROMBOCYTE",
        "MCH",
        "MCHC",
        "MCV",
        "AGE",
        "SEX",
    ]
]

pd_test_df = pd.DataFrame(user_data, columns=cols)

# Display user input
st.subheader("User Input")
st.write(pd_test_df)

# Make predictions using the loaded Random Forest model
rf_predict_user_data = rf_model.predict(pd_test_df)

# Determine the action to be taken based on the prediction
if rf_predict_user_data == 0:
    care = "Out Care (Home Care) Required"
else:
    care = "In Care (Hospitalization) Required"

# Display the result
st.subheader("Action to Take")
st.write(care)









