import pickle
import streamlit as st
from streamlit_option_menu import option_menu

# Change Name & Logo
st.set_page_config(page_title="Diease Prediction", page_icon="⚕️")

# hidding streamlit ad-ons

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# loading the saved models

diabetes_model = pickle.load(open('Models/diabetes_model.sav', 'rb'))

heart_disease_model = pickle.load(open('Models/heart_disease_model.sav', 'rb'))

parkinsons_model = pickle.load(open('Models/parkinsons_model.sav', 'rb'))

lungs_disease_model = pickle.load(open('Models/lungs_disease_model.sav', 'rb'))

thyroid_model = pickle.load(open('Models/Thyroid_model.sav', 'rb'))


# sidebar for navigation
with st.sidebar:

    selected = option_menu('Multiple Disease Prediction System',

                           ['Diabetes Prediction',
                            'Heart Disease Prediction',
                            'Parkinsons Prediction',
                            'Lungs Cancer Prediction',
                            'Hypo-Thyroid Prediction'],

                           icons=['activity', 'heart', 'person',
                                  'brightness-high', 'droplet-half'],

                           default_index=0)


# Diabetes Prediction Page
if (selected == 'Diabetes Prediction'):

    # page title
    st.title('Diabetes Prediction using ML')

    # getting the input data from the user
    col1, col2, col3 = st.columns(3)

    with col1:
        Pregnancies = st.text_input('Number of Pregnancies')

    with col2:
        Glucose = st.text_input('Glucose Level')

    with col3:
        BloodPressure = st.text_input('Blood Pressure value')

    with col1:
        SkinThickness = st.text_input('Skin Thickness value')

    with col2:
        Insulin = st.text_input('Insulin Level')

    with col3:
        BMI = st.text_input('BMI value')

    with col1:
        DiabetesPedigreeFunction = st.text_input(
            'Diabetes Pedigree Function value')

    with col2:
        Age = st.text_input('Age of the Person')

    # code for Prediction
    diab_diagnosis = ''

    # creating a button for Prediction

    if st.button('Diabetes Test Result'):
        diab_prediction = diabetes_model.predict(
            [[Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age]])

        if (diab_prediction[0] == 1):
            diab_diagnosis = 'The person is diabetic'
        else:
            diab_diagnosis = 'The person is not diabetic'

    st.success(diab_diagnosis)


# Heart Disease Prediction Page
if (selected == 'Heart Disease Prediction'):

    # page title
    st.title('Heart Disease Prediction using ML')

    col1, col2, col3 = st.columns(3)

    with col1:
        age = st.text_input('Age')

    with col2:
        sex = st.text_input('Sex')

    with col3:
        cp = st.text_input('Chest Pain types')

    with col1:
        trestbps = st.text_input('Resting Blood Pressure')

    with col2:
        chol = st.text_input('Serum Cholestoral in mg/dl')

    with col3:
        fbs = st.text_input('Fasting Blood Sugar > 120 mg/dl')

    with col1:
        restecg = st.text_input('Resting Electrocardiographic results')

    with col2:
        thalach = st.text_input('Maximum Heart Rate achieved')

    with col3:
        exang = st.text_input('Exercise Induced Angina')

    with col1:
        oldpeak = st.text_input('ST depression induced by exercise')

    with col2:
        slope = st.text_input('Slope of the peak exercise ST segment')

    with col3:
        ca = st.text_input('Major vessels colored by flourosopy')

    with col1:
        thal = st.text_input(
            'thal: 0 = normal; 1 = fixed defect; 2 = reversable defect')

    # code for Prediction
    heart_diagnosis = ''

    # creating a button for Prediction

    if st.button('Heart Disease Test Result'):
        heart_prediction = heart_disease_model.predict(
            [[age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]])

        if (heart_prediction[0] == 1):
            heart_diagnosis = 'The person is having heart disease'
        else:
            heart_diagnosis = 'The person does not have any heart disease'

    st.success(heart_diagnosis)


# Parkinson's Prediction Page
if (selected == "Parkinsons Prediction"):

    # page title
    st.title("Parkinson's Disease Prediction using ML")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        fo = st.text_input('MDVP:Fo(Hz)')

    with col2:
        fhi = st.text_input('MDVP:Fhi(Hz)')

    with col3:
        flo = st.text_input('MDVP:Flo(Hz)')

    with col4:
        Jitter_percent = st.text_input('MDVP:Jitter(%)')

    with col5:
        Jitter_Abs = st.text_input('MDVP:Jitter(Abs)')

    with col1:
        RAP = st.text_input('MDVP:RAP')

    with col2:
        PPQ = st.text_input('MDVP:PPQ')

    with col3:
        DDP = st.text_input('Jitter:DDP')

    with col4:
        Shimmer = st.text_input('MDVP:Shimmer')

    with col5:
        Shimmer_dB = st.text_input('MDVP:Shimmer(dB)')

    with col1:
        APQ3 = st.text_input('Shimmer:APQ3')

    with col2:
        APQ5 = st.text_input('Shimmer:APQ5')

    with col3:
        APQ = st.text_input('MDVP:APQ')

    with col4:
        DDA = st.text_input('Shimmer:DDA')

    with col5:
        NHR = st.text_input('NHR')

    with col1:
        HNR = st.text_input('HNR')

    with col2:
        RPDE = st.text_input('RPDE')

    with col3:
        DFA = st.text_input('DFA')

    with col4:
        spread1 = st.text_input('spread1')

    with col5:
        spread2 = st.text_input('spread2')

    with col1:
        D2 = st.text_input('D2')

    with col2:
        PPE = st.text_input('PPE')

    # code for Prediction
    parkinsons_diagnosis = ''

    # creating a button for Prediction
    if st.button("Parkinson's Test Result"):
        parkinsons_prediction = parkinsons_model.predict(
            [[fo, fhi, flo, Jitter_percent, Jitter_Abs, RAP, PPQ, DDP, Shimmer, Shimmer_dB, APQ3, APQ5, APQ, DDA, NHR, HNR, RPDE, DFA, spread1, spread2, D2, PPE]])

        if (parkinsons_prediction[0] == 1):
            parkinsons_diagnosis = "The person has Parkinson's disease"
        else:
            parkinsons_diagnosis = "The person does not have Parkinson's disease"

    st.success(parkinsons_diagnosis)

# Lungs Cancer Prediction Page
if (selected == "Lungs Cancer Prediction"):

    # page title
    st.title("Lungs Cancer Disease Prediction using ML")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        GENDER = st.text_input('Gender')

    with col2:
        AGE = st.text_input('Age')

    with col3:
        SMOKING = st.text_input('Smoking')

    with col4:
        YELLOW_FINGERS = st.text_input('Yellow Finger')

    with col1:
        ANXIETY = st.text_input('Anxiety')

    with col2:
        PEER_PRESSURE = st.text_input('Peer Pressure')

    with col3:
        CHRONIC_DISEASE = st.text_input('Chronic Disease')

    with col4:
        FATIGUE = st.text_input('Fatigue')

    with col1:
        ALLERGY = st.text_input('Allergy')

    with col2:
        WHEEZING = st.text_input('Wheezing')

    with col3:
        ALCOHOL_CONSUMING = st.text_input('Alcohol Consuming')

    with col4:
        COUGHING = st.text_input('Coughing')

    with col1:
        SHORTNESS_OF_BREATH = st.text_input('Shortness Of Breath')

    with col2:
        SWALLOWING_DIFFICULTY = st.text_input('Swallowing Difficulty')

    with col3:
        CHEST_PAIN = st.text_input('Chest Pain')

    # code for Prediction
    lungs_diagnosis = ''

    # creating a button for Prediction
    if st.button("Lung's Test Result"):
        lungs_prediction = lungs_disease_model.predict([[GENDER, AGE, SMOKING, YELLOW_FINGERS, ANXIETY, PEER_PRESSURE, CHRONIC_DISEASE,
                                                       FATIGUE, ALLERGY, WHEEZING, ALCOHOL_CONSUMING, COUGHING, SHORTNESS_OF_BREATH, SWALLOWING_DIFFICULTY, CHEST_PAIN]])

        if (lungs_prediction[0] == 1):
            lungs_diagnosis = "The person has lungs cancer disease"
        else:
            lungs_diagnosis = "The person does not have lungs cancer disease"

    st.success(lungs_diagnosis)

# Hypo-Thyroid Prediction Page
if (selected == "Hypo-Thyroid Prediction"):

    # page title
    st.title("Hypo-Thyroid Prediction using ML")

    col1, col2, col3 = st.columns(3)

    with col1:
        age = st.text_input('Age')

    with col2:
        sex = st.text_input('Sex')

    with col3:
        on_thyroxine = st.text_input('On Thyroxine')

    with col1:
        tsh = st.text_input('TSH')

    with col2:
        t3_measured = st.text_input('T3 Measured')

    with col3:
        t3 = st.text_input('T3')

    with col1:
        tt4 = st.text_input('TT4')

    # code for Prediction
    thyroid_diagnosis = ''

    # creating a button for Prediction
    if st.button("Thyroid's Test Result"):
        thyroid_prediction = thyroid_model.predict(
            [[age, sex, on_thyroxine, tsh, t3_measured, t3, tt4]])

        if (thyroid_prediction[0] == 1):
            thyroid_diagnosis = "The person has Hypo Thyroid disease"
        else:
            thyroid_diagnosis = "The person does not have Hypo Thyroid disease"

    st.success(thyroid_diagnosis)
