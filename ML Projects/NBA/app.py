from flask import Flask, render_template, request
import os 
import numpy as np
import pandas as pd
from src.NBA_Project.pipeline.prediction import PredictionPipeline


app = Flask(__name__) # initializing a flask app

@app.route('/',methods=['GET']) 
def homePage():
    return render_template("index.html")


@app.route('/train',methods=['GET']) 
def training():
    os.system("python main.py")
    return "Training Successful!" 


@app.route('/predict',methods=['POST','GET']) 
def index():
    if request.method == 'POST':
        try:
            GP =float(request.form['GamesPlayed'])
            MIN =float(request.form['MinutesPlayed'])
            FTM =float(request.form['FreeThrowMade'])
            PA_3 =float(request.form['3PointsAttempts'])
            OREB =float(request.form['OffensiveRebounds'])
            BLK =float(request.form['Blocks'])
            Made_3P  =float(request.form['3PointsMade'])
            Point3Attempts=float(request.form['3PointAttempts'])
            FielGoalPercent =float(request.form['FielGoalPercent'])     
         
            data = [GP,MIN,FTM,PA_3,OREB,BLK,Made_3P,Point3Attempts,FielGoalPercent]
            data = np.array(data).reshape(1, 9)
            print(data)
            
            obj = PredictionPipeline()
            predict = obj.predict(data)

            return render_template('results.html', prediction = predict[0])

        except ValueError as e:
            print('ValueError: ', e)
            return 'Invalid input data'

    else:
        return render_template('index.html')
    

if __name__ == "__main__":
	app.run(host="0.0.0.0", port = 5000,debug=True)