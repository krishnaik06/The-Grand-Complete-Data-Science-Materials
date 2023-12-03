from flask import Flask, render_template, request
from flask_cors import CORS, cross_origin
from homeLoan.constants import *
from homeLoan.pipeline.training_pipeline import TrainingPipeline
from homeLoan.pipeline.prediction_pipeline import PredictionPipeline
import pandas as pd


app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/train')
def trainRoute():
    training_pipeline = TrainingPipeline()
    training_pipeline.train()
    return 'Model trained successfully'

@app.route('/predict', methods=['GET', 'POST'])
@cross_origin()
def predictRoute():
    try:
        if request.method == 'POST':
            input_features = {
                'Gender': [request.form.get('gender')],
                'Married': [request.form.get('married')],
                'Dependents': [request.form.get('dependents')],
                'Education': [request.form.get('education')],
                'Self_Employed': [request.form.get('self_employed')],
                'ApplicantIncome': [int(request.form.get('applicant_income'))],
                'CoapplicantIncome': [float(request.form.get('coapplicant_income'))],
                'LoanAmount': [float(request.form.get('loan_amount'))],
                'Loan_Amount_Term': [float(request.form.get('loan_amount_term'))],
                'Credit_History': [float(request.form.get('credit_history'))],
                'Property_Area': [request.form.get('property_area')]
            }

            input_features = pd.DataFrame(input_features)
            prediction_pipeline = PredictionPipeline()
            result = prediction_pipeline.predict(input_features)
            
            if result == 1:
                prediction = 'Approved'
            else:
                prediction = 'Rejected'

            # Send back the input features to the html form
            form_data = {
                'gender': request.form.get('gender'),
                'married': request.form.get('married'),
                'dependents': request.form.get('dependents'),
                'education': request.form.get('education'),
                'self_employed': request.form.get('self_employed'),
                'applicant_income': int(request.form.get('applicant_income')),
                'coapplicant_income': float(request.form.get('coapplicant_income')),
                'loan_amount': float(request.form.get('loan_amount')),
                'loan_amount_term': float(request.form.get('loan_amount_term')),
                'credit_history': request.form.get('credit_history'),
                'property_area': request.form.get('property_area')
            }
            
            return render_template('form.html', prediction=prediction, form_data=form_data)
        
        else:
            return render_template('index.html')
        
    except Exception as e:
        raise e

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)