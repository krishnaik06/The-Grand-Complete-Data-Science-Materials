import pandas as pd
import numpy as np
from pyscript import Element
from js import document, window
import pickle

# Disable warnings by pyscript appearing in the browser.
import warnings
warnings.filterwarnings("ignore")

with open("model.pkl", "rb") as f:
    loaded_model = pickle.load(f)

def get_predictions():
    data = {
            "ApplicantIncome": document.querySelector("#ApplicantIncome").value,
            "CoapplicantIncome": document.querySelector("#CoapplicantIncome").value,
            "Credit_History": document.querySelector('input[name="Credit_History"]:checked').value,
            "Dependents": document.querySelector("#Dependents").value,
            "Education": document.querySelector('input[name="Education"]:checked').value,
            "Gender": document.querySelector('input[name="Gender"]:checked').value,
            "LoanAmount": document.querySelector("#LoanAmount").value,
            "Loan_Amount_Term": document.querySelector("#LoanAmountTerm").value,
            "Married": document.querySelector('input[name="Married"]:checked').value,
            "Property_Area": document.querySelector("#Property_Area").value,
            "Self_Employed": document.querySelector('input[name="Self_Employed"]:checked').value
        }
    
    # print("Data", data)

    Gender = 1 if data["Gender"]=="male" else 0
    Married = 1 if data["Married"]=="yes" else 0
    if data["Dependents"]=="0":
        Dependents = 0
    elif data["Dependents"]=="1":
        Dependents = 1
    elif data["Dependents"]=="2":
        Dependents = 2
    else:
        Dependents = 3
    Education = 0 if data["Education"]=="Graduate" else 1
    Self_Employed = 1 if data["Self_Employed"]=="s_yes" else 0
    LoanAmount = np.log(int(data["LoanAmount"]))
    Loan_Amount_Term = np.log(int(data["Loan_Amount_Term"]))
    Credit_History = 1 if data["Credit_History"]=="c_yes" else 0
    if data["Property_Area"]=="Rural":
        Property_Area = 0
    elif data["Property_Area"]=="Semiurban":
        Property_Area = 1
    else:
        Property_Area = 2
    TotalIncome = np.log(int(data["ApplicantIncome"])+int(data["CoapplicantIncome"]))

    predictionData = [Gender,Married,Dependents,Education,Self_Employed,LoanAmount,Loan_Amount_Term,Credit_History,Property_Area,TotalIncome]
    result = loaded_model.predict([predictionData])
    if result[0]==1:
        result = "will"
    else:
        result = "will not"

    document.querySelector(".prediction").hidden = False
    document.querySelector(".result").innerText = result
    
    return result
