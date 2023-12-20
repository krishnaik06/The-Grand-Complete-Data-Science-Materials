import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

st.header("Patient Care Classification System")

#read file
patient_df = pd.read_csv("C:/Users/yashs/Desktop/PatientCare.csv")

#mapping gender
gender = {"M" : 1, "F" : 0}
patient_df["SEX"] = patient_df["SEX"].map(gender)



df_x = patient_df.iloc[:,0:10]
df_y = patient_df.iloc[:,10]

x_train, x_test, y_train, y_test=train_test_split(df_x, df_y, test_size=0.20, random_state=1)

rf_model = RandomForestClassifier(random_state = 1)

rf_model.fit(x_train,y_train)

rf_predictions = rf_model.predict(x_test)

st_HAEMATOCRIT = st.number_input("Enter HAEMATOCRIT Value : ")
st_HAEMOGLOBINS = st.number_input("Enter HAEMOGLOBINS Value : ")
st_ERYTHROCYTE = st.number_input("Enter ERYTHROCYTE Value : ")
st_LEUCOCYTE = st.number_input("Enter LEUCOCYTE Value : ")
st_THROMBOCYTE = st.number_input("Enter THROMBOCYTE Value : ")
st_MCH = st.number_input("Enter MCH Value : ")
st_MCHC = st.number_input("Enter MCHC Value : ")
st_MCV = st.number_input("Enter MCV Value : ")
st_AGE = st.number_input("Enter AGE Value : ")
st_SEX = st.number_input("Enter SEX(Enter 1 for Male and 0 for Female) Value : ")

user_data = [[st_HAEMATOCRIT,st_HAEMOGLOBINS,st_ERYTHROCYTE,st_LEUCOCYTE,st_THROMBOCYTE,st_MCH,st_MCHC,st_MCV,st_AGE,st_SEX]]
cols = [["HAEMATOCRIT","HAEMOGLOBINS","ERYTHROCYTE","LEUCOCYTE","THROMBOCYTE","MCH","MCHC","MCV","AGE","SEX"]]


pd_test_df = pd.DataFrame(user_data,columns = cols)

st.subheader('User Input')
st.write(pd_test_df)

rf_predict_user_data = rf_model.predict(pd_test_df)

if rf_predict_user_data == 0:
    care = 'Out Care(Home Care) Required'
else :
    care = 'In Care(Hospitalization) Required'

st.subheader('Action to Taken')
st.write(care)








