import matplotlib
matplotlib.use('Agg')  
from flask import Flask, render_template, request
import pandas as pd
import joblib
import numpy as np
import io
import base64
import matplotlib.pyplot as plt
import seaborn as sns

app = Flask(__name__)  

model = joblib.load('model.pkl')

@app.route('/')
def home():
    return render_template('index.html', form_data={}, predicted_cgpa=None)

@app.route('/ok')
def ok():
    return render_template('first.html')

@app.route('/predict', methods=['POST'])
def predict():
    form_data = request.form
    age = float(form_data['age'])
    gender = int(form_data['gender'])
    parental_education = int(form_data['parental_education'])
    study_time_weekly = float(form_data['study_time_weekly'])
    absences = int(form_data['absences'])
    tutoring = int(form_data['tutoring'])
    parental_support = int(form_data['parental_support'])
    extracurricular = int(form_data['extracurricular'])
    sports = int(form_data['sports'])

    penalty = (absences // 15 )* 0.01

    input_data = np.array([[age, gender, parental_education, 
                             study_time_weekly, absences, 
                             tutoring, parental_support, 
                             extracurricular, sports]])

    predicted_cgpa = model.predict(input_data)[0] - penalty  
    predicted_grade = determine_grade(predicted_cgpa)

    suggestions = []
    if study_time_weekly < 12:
        suggestions.append("Increase your study time to atleast 12 hours per week to get a decent SGPA.")
    if absences > 20:
        suggestions.append("You have too many absences, Try to manage your time and avoid further absences .")
    if tutoring == 0:
        suggestions.append("Consider getting tutoring support to improve your performance.")
    if parental_support == 0:
        suggestions.append("Seek more parental support to help you focus better.")
    if extracurricular == 0:
        suggestions.append("Engaging in extracurricular activities can help balance your overall development .")
    if sports == 0:
        suggestions.append("Participating in sports activities can improve both mental and physical health.")

    pie_chart_url = create_pie_chart(form_data)
    comparison_graph_url = create_comparison_graph(study_time_weekly)

    return render_template('result.html', 
                           form_data=form_data, 
                           predicted_cgpa=predicted_cgpa,
                           predicted_grade=predicted_grade,
                           suggestions=suggestions,
                           graph_url=pie_chart_url,
                           comparison_graph_url=comparison_graph_url)

def determine_grade(cgpa):
    if cgpa >= 9:
        return 'A+'
    elif cgpa >= 8:
        return 'A'
    elif cgpa >= 7:
        return 'B'
    elif cgpa >= 6:
        return 'C'
    elif cgpa >= 5:
        return 'D'
    else:
        return 'F'

def create_pie_chart(form_data):
  
    attributes = {
        'Study Time Weekly': float(form_data['study_time_weekly']),
        'Absences': int(form_data['absences']),
        'Tutoring': int(form_data['tutoring']),
        'Parental Support': int(form_data['parental_support']),
        'Extracurricular': int(form_data['extracurricular']),
        'Sports': int(form_data['sports'])
    }

    labels = list(attributes.keys())
    sizes = list(attributes.values())
    
    plt.figure(figsize=(6, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    plt.axis('equal')  

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    chart_url = base64.b64encode(img.getvalue()).decode()
    plt.close()

    return 'data:image/png;base64,{}'.format(chart_url)

def create_comparison_graph(study_time_weekly):
    recommended_time = 15  
    actual_time = study_time_weekly

    plt.figure(figsize=(6, 4))
    plt.bar(['Recommended Time', 'Actual Time'], [recommended_time, actual_time], color=['blue', 'orange'])
    plt.ylabel('Study Time (Hours)')
    plt.title('Comparison of Recommended Study Time vs Actual Study Time')
 
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    chart_url = base64.b64encode(img.getvalue()).decode()
    plt.close()

    return 'data:image/png;base64,{}'.format(chart_url)

