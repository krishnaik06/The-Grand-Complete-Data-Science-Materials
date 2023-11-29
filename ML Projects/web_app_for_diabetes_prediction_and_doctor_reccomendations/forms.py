from flask_wtf import FlaskForm
# from app import User
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, IntegerField, FloatField
from wtforms.validators import ValidationError, Email, EqualTo, Length, InputRequired

class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(max=30, message='Should be less than 30 characters')])
    email = StringField('Email', validators=[InputRequired(), Email()])
    age = IntegerField('Age', [InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    password2 = PasswordField('Repeat Password', validators=[InputRequired(), EqualTo('password')])
    address = StringField('Address', [InputRequired()])
    pincode = StringField('Pincode', [InputRequired()])
    # dp = FileField(validators=[FileAllowed(IMAGES, 'Only images are allowed')])
    submit = SubmitField('Sign Up')

    # def validate_username(self, username):
    #     user = User.query.filter_by(username=username.data).first()
    #     if user is not None:
    #         raise ValidationError('User already exists!')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Log In')

class PredictForm(FlaskForm):
    pregnancies = IntegerField('Pregnancies', [InputRequired()])
    glucose = IntegerField('Glucose', [InputRequired()])
    bloodPressure = IntegerField('BloodPressure', [InputRequired()])
    skinThickness = IntegerField('SkinThickness', [InputRequired()])
    insulin = IntegerField('Insulin', [InputRequired()])
    bmi = FloatField('BMI', [InputRequired()])
    dpf = FloatField('DPF', [InputRequired()])
    age = IntegerField('Age', [InputRequired()])
    submit = SubmitField('Check')