import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from flask import Flask, request, jsonify, render_template, flash, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from forms import SignUpForm, LoginForm, PredictForm
import requests


app = Flask(__name__)

db = SQLAlchemy()
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db.init_app(app)
app.secret_key = 'YOUR GMAP API KEY'
app.app_context().push()

login = LoginManager(app)
login.login_view = 'login'

# loading the diabetes dataset to a pandas DataFrame
diabetes_dataset = pd.read_csv('./content/diabetes.csv') 

# df = pd.read_csv('kaggle_diabetes.csv')
diabetes_dataset = diabetes_dataset.rename(columns={'DiabetesPedigreeFunction':'DPF'})
diabetes_dataset_copy = diabetes_dataset.copy(deep=True)
diabetes_dataset_copy[['Glucose','BloodPressure','SkinThickness','Insulin','BMI']] = diabetes_dataset_copy[['Glucose','BloodPressure','SkinThickness','Insulin','BMI']].replace(0,np.NaN)

diabetes_dataset_copy['Glucose'].fillna(diabetes_dataset_copy['Glucose'].mean(), inplace=True)
diabetes_dataset_copy['BloodPressure'].fillna(diabetes_dataset_copy['BloodPressure'].mean(), inplace=True)
diabetes_dataset_copy['SkinThickness'].fillna(diabetes_dataset_copy['SkinThickness'].median(), inplace=True)
diabetes_dataset_copy['Insulin'].fillna(diabetes_dataset_copy['Insulin'].median(), inplace=True)
diabetes_dataset_copy['BMI'].fillna(diabetes_dataset_copy['BMI'].median(), inplace=True)

# separating the data and labels
X = diabetes_dataset.drop(columns = 'Outcome', axis=1)
Y = diabetes_dataset['Outcome']
X_train, X_test, Y_train, Y_test = train_test_split(X,Y, test_size = 0.2, stratify=Y, random_state=2)

#training the support vector Machine Classifier
# classifier = svm.SVC(kernel='linear')
# classifier.fit(X_train, Y_train)
classifier = LogisticRegression(random_state = 0)
classifier.fit(X_train, Y_train)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

# define the route for the home page
@app.route('/')
def index():
    if current_user.is_authenticated:
        logged = True
    else:
        logged = False
    return render_template('index.html', logged = logged)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = SignUpForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, age = form.age.data, address = form.address.data, pincode = form.pincode.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {user.username}! You can now log in')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('index'))
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/predict', methods = ['GET', 'POST'])
@login_required
def predict():
    form = PredictForm()
    if request.method == 'POST':
        # data = request.get_json(force=True)
        # print(data)
        data = {'Pregnancies': form.pregnancies.data, 'Glucose': form.glucose.data, 'BloodPressure': form.bloodPressure.data, 'SkinThickness': form.skinThickness.data, 'Insulin': form.insulin.data, 'BMI': form.bmi.data, 'DiabetesPedigreeFunction': form.dpf.data, 'Age': form.age.data}
        print(data)
        prediction = classifier.predict([list(data.values())])

        output = prediction[0]
        if output == 0:
            # return jsonify({'result': 'The person is not diabetic'})
            return render_template('diabetes_false.html')
        else:
            # return jsonify({'result': 'The person is diabetic'})
            current_user.dibetic = True
            db.session.commit()
            return render_template('diabetes_true.html')
    return render_template('predict_form.html', form=form)

# @app.route('/predict', methods=['POST'])
# def predict():
#     # data = request.get_json(force=True)
#     # print(data)
#     data = {'Pregnancies': 6, 'Glucose': 148, 'BloodPressure': 72, 'SkinThickness': 35, 'Insulin': 0, 'BMI': 33.6, 'DiabetesPedigreeFunction': 0.627, 'Age': 50}
#     prediction = classifier.predict([list(data.values())])

#     output = prediction[0]
#     if output == 0:
#         return jsonify({'result': 'The person is not diabetic'})
#     else:
#         return jsonify({'result': 'The person is diabetic'})
    

def find_doctors(zip_code):
        # Replace YOUR_API_KEY with your actual API key
        api_key = "AIzaSyAUZtbAaLjkeJ6TG9FrXBYH9MZAj9X0wJs"
        url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
        query = "diabetes doctors near {}".format(zip_code)
        params = {
            "key": api_key,
            "query": query
        }
        response = requests.get(url, params=params)
        results = response.json().get("results", [])
        doctors = []
        for result in results:
            doctor = {
                "name": result["name"],
                "address": result["formatted_address"],
                "rating": result.get("rating", None),
                "distance": result.get("distance", None),
                "url": f"https://www.google.com/maps/place/?q=place_id:{result['place_id']}",
                "location": result["geometry"]["location"]
            }
            doctors.append(doctor)
        # Sort the doctors by rating and distance
        doctors = sorted(doctors, key=lambda x: (-x["rating"] if x["rating"] else 0, x["distance"] if x["distance"] else float("inf")))
        # Return the top 10 doctors
        return doctors[:10]

@app.route('/test', methods=['GET', 'POST'])
def test():
    input = "800020"
    if request.method == 'POST':
        return find_doctors(input)
    return render_template('diabetes_true.html')

@app.route('/suggestions', methods=['GET', 'POST'])
@login_required
def suggestions():
    doctors = find_doctors(current_user.pincode)
    # doctors = json.loads(lists)
    # return render_template('suggestions.html')
    return render_template('suggestions.html', doctors=doctors)

@app.route('/suggestionf', methods=['GET', 'POST'])
# @login_required
def suggestionf():
    doctors = find_doctors(current_user.pincode)
    return render_template('suggestionf.html', doctors=doctors)

@app.route('/add_medication', methods=['POST'])
def add_medication():
    name = request.form['name']
    dosage = request.form['dosage']
    frequency = request.form['frequency']
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    user_id = current_user.id

    medication = Medication(name=name, dosage=dosage, frequency=frequency,
                            start_date=start_date, end_date=end_date, user_id=user_id)
    db.session.add(medication)
    db.session.commit()

    flash('Medication added successfully.')
    return redirect(url_for('medication_list'))

@app.route('/medication_list')
@login_required
def medication_list():
    medications = Medication.query.filter_by(user_id=current_user.id).all()
    doctors = find_doctors(current_user.pincode)
    return render_template('suggestions.html', medications=medications, doctors=doctors)

@app.route('/update_medication/<int:medication_id>', methods=['GET', 'POST'])
@login_required
def update_medication(medication_id):
    medication = Medication.query.get_or_404(medication_id)
    if request.method == 'POST':
        medication.name = request.form['name']
        medication.dosage = request.form['dosage']
        medication.frequency = request.form['frequency']
        medication.start_date = request.form['start_date']
        medication.end_date = request.form['end_date']
        db.session.commit()
        flash('Medication updated successfully.')
        return redirect(url_for('medication_list'))
    else:
        doctors = find_doctors(current_user.pincode)
        return render_template('suggestions.html', medication=medication, doctors=doctors)
    
@app.route('/delete_medication/<int:medication_id>', methods=['POST'])
@login_required
def delete_medication(medication_id):
    medication = Medication.query.get_or_404(medication_id)
    db.session.delete(medication)
    db.session.commit()
    flash('Medication deleted successfully.')
    return redirect(url_for('medication_list'))

##### Model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    # dp = db.Column(db.String(100))
    password_hash = db.Column(db.String(128))
    age = db.Column(db.String(140))
    address = db.Column(db.String(120))
    pincode = db.Column(db.String(60))
    # city = db.Column(db.String(120))
    join_date = db.Column(db.DateTime, default=datetime.utcnow)
    dibetic = db.Column(db.Boolean, default = False)
    medications = db.relationship('Medication', back_populates='user')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Medication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    dosage = db.Column(db.Integer)
    frequency = db.Column(db.String)
    start_date = db.Column(db.String)
    end_date = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='medications')
    

    


if __name__ == '__main__':
    db.create_all()
    app.run(port=5000, debug=True)
