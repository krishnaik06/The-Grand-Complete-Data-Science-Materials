import pickle
from flask import Flask, request, jsonify, render_template
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings("ignore")

app = Flask(__name__) # initializing a flask app

## import pickle files

minmax_scaler1=pickle.load(open("model/scaler1.pkl","rb"))
minmax_scaler2=pickle.load(open("model/scaler2.pkl","rb"))
rf_model=pickle.load(open("model/random-forest(FD001).pkl","rb"))
lasso_model=pickle.load(open("model/lasso(FD002).pkl","rb"))
xgbr_model=pickle.load(open("model/xgbr(FD003).pkl","rb"))
ridge_model=pickle.load(open("model/ridge(FD004).pkl","rb"))

## Route for home page
@app.route("/", methods=["GET", "POST"])

def index():
    return render_template("index.html")


@app.route("/FD001", methods=["GET", "POST"])
def predict_rul1():
    if request.method=="POST":
        
       
        sensor2 =float(request.form.get("sensor2"))

        sensor4 =float(request.form.get("sensor3"))
        sensor3 =float(request.form.get("sensor4"))

     

        sensor7 =float(request.form.get("sensor7"))
        sensor8 =float(request.form.get("sensor8"))

        sensor9 =float(request.form.get("sensor9"))
     

        sensor11=float(request.form.get("sensor11")) 
        sensor12=float(request.form.get("sensor12")) 
        sensor13=float(request.form.get("sensor13"))
        sensor14=float(request.form.get("sensor14")) 
        sensor15=float(request.form.get("sensor15")) 
     
        sensor17=float(request.form.get("sensor17")) 
       
       
        sensor20=float(request.form.get("sensor20")) 
        sensor21=float(request.form.get("sensor21"))

        new_data_scaled1=minmax_scaler1.transform([[sensor2, sensor3, sensor4, sensor7, sensor8, sensor9, sensor11, sensor12, sensor13, sensor14, sensor15, sensor17, sensor20, sensor21]])
        result1=rf_model.predict(new_data_scaled1)

        return render_template("FD001.html", result1=result1[0])
    else:
        return render_template("FD001.html")
    
@app.route("/FD002", methods=["GET", "POST"])
def predict_rul2():
    if request.method=="POST":
        
        sensor1 =float(request.form.get("sensor1"))
        sensor2 =float(request.form.get("sensor2"))

        sensor4 =float(request.form.get("sensor3"))
        sensor3 =float(request.form.get("sensor4"))

        sensor5 =float(request.form.get("sensor5"))
        sensor6 =float(request.form.get("sensor6"))

        sensor7 =float(request.form.get("sensor7"))
        sensor8 =float(request.form.get("sensor8"))

        sensor9 =float(request.form.get("sensor9"))
        sensor10=float(request.form.get("sensor10")) 

        sensor11=float(request.form.get("sensor11")) 
        sensor12=float(request.form.get("sensor12")) 
        
        sensor14=float(request.form.get("sensor14")) 
        sensor15=float(request.form.get("sensor15")) 
     
        sensor17=float(request.form.get("sensor17")) 
        sensor18=float(request.form.get("sensor18")) 
       
        sensor20=float(request.form.get("sensor20")) 
        sensor21=float(request.form.get("sensor21"))

        new_data_scaled2=minmax_scaler2.transform([[sensor1, sensor2, sensor3, sensor4, sensor5, sensor6, sensor7, sensor8, sensor9, sensor10, sensor11, sensor12, sensor14, sensor15, sensor17, sensor18, sensor20, sensor21]])
        result2=lasso_model.predict(new_data_scaled2)

        return render_template("FD002.html", result2=result2[0])
    else:
        return render_template("FD002.html")

@app.route("/FD003", methods=["GET", "POST"])
def predict_rul3():
    if request.method=="POST":      
        sensor2 =float(request.form.get("sensor2"))
        sensor3 =float(request.form.get("sensor3"))
        sensor4 =float(request.form.get("sensor4"))
       
        sensor7 =float(request.form.get("sensor7"))
        sensor8 =float(request.form.get("sensor8"))
        sensor9 =float(request.form.get("sensor9"))
         
        sensor11=float(request.form.get("sensor11")) 
        sensor12=float(request.form.get("sensor12")) 
        sensor13=float(request.form.get("sensor13")) 
        sensor14=float(request.form.get("sensor14")) 
        sensor15=float(request.form.get("sensor15")) 
        
        sensor17=float(request.form.get("sensor17")) 
      
        sensor20=float(request.form.get("sensor20")) 
        sensor21=float(request.form.get("sensor21"))

        new_data_scaled3=minmax_scaler1.transform([[sensor2, sensor3, sensor4, sensor7, sensor8, sensor9, sensor11, sensor12, sensor13, sensor14, sensor15, sensor17, sensor20, sensor21]])
        result3=xgbr_model.predict(new_data_scaled3)

        return render_template("FD003.html", result3=result3[0])
    else:
        return render_template("FD003.html")


@app.route("/FD004", methods=["GET", "POST"])
def predict_rul4():
    if request.method=="POST":
        
        sensor1 =float(request.form.get("sensor1"))
        sensor2 =float(request.form.get("sensor2"))

        sensor4 =float(request.form.get("sensor3"))
        sensor3 =float(request.form.get("sensor4"))

        sensor5 =float(request.form.get("sensor5"))
        sensor6 =float(request.form.get("sensor6"))

        sensor7 =float(request.form.get("sensor7"))
        sensor8 =float(request.form.get("sensor8"))

        sensor9 =float(request.form.get("sensor9"))
        sensor10=float(request.form.get("sensor10")) 

        sensor11=float(request.form.get("sensor11")) 
        sensor12=float(request.form.get("sensor12")) 
        
        sensor14=float(request.form.get("sensor14")) 
        sensor15=float(request.form.get("sensor15")) 
     
        sensor17=float(request.form.get("sensor17")) 
        sensor18=float(request.form.get("sensor18")) 
       
        sensor20=float(request.form.get("sensor20")) 
        sensor21=float(request.form.get("sensor21"))

        new_data_scaled4=minmax_scaler2.transform([[sensor1, sensor2, sensor3, sensor4, sensor5, sensor6, sensor7, sensor8, sensor9, sensor10, sensor11, sensor12, sensor14, sensor15, sensor17, sensor18, sensor20, sensor21]])
        result4=ridge_model.predict(new_data_scaled4)

        return render_template("FD004.html", result4=result4[0])
    else:
        return render_template("FD004.html")


# Run APP in Debug mode
if __name__ == "__main__":
    app.run(port=8000)