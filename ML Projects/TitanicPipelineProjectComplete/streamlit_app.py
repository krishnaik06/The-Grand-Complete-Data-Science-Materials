import os
from pathlib import Path
import time
import streamlit as st
import pandas as pd
from titanic.pipeline.prediction import PredictionPipeline
from titanic.utils.common import read_yaml


class ClientApp:
    def __init__(self):
        self.filename = "test.csv"
        self.classifier = PredictionPipeline(self.filename)


# Define the feature input function
def main():

    st.title("Titanic Survival Prediction")

    pclass_options ={
        1:'Upper',
        2:'Middle',
        3:'Lower'
    }

    embark_options = {
        "C":'Cherbourg',
        "Q":"Queenstown",
        "S":"Southampton"
    }
    
    def embar_format_func(option):
        return embark_options[option]
    def pclass_format_func(option):
        return pclass_options[option]


    # Define your features here. For example:
    Pclass = st.selectbox('Ticket Class',pclass_options.keys(),format_func=pclass_format_func )
    Sex = st.selectbox('Gender', ['Male', 'Female'])
    Age = st.slider('Age in years', 0, 100, 30)
    SibSp = st.slider('Number of Siblings/Sposes aboard', 0, 10, 1)
    Parch = st.slider('Number of Parents/Children aboard', 0, 10, 0)
    # Fare = st.sidebar.slider('Fare', 0.0, 600.0, 50.0)f
    Embarked = st.selectbox('Port of Embarkation',embark_options.keys(), format_func=embar_format_func)

    if st.button("Train"):
        with st.spinner('Training the model'):
            os.system("dvc repro")
            time.sleep(5)
        st.write("Model trained successfully")
        content = read_yaml(Path('metrics.yaml'))

        st.write(f"The accuracy of the model is {float(content.accuracy)*100}")

    if st.button('Predict', help="Click to know if the person has suvived"):

        # Create a data frame from the inputs
        data = {'Pclass': Pclass,
            'Sex': Sex,
            'Age': Age,
            'SibSp': SibSp,
            'Parch': Parch,
            # 'Fare': Fare,
            'Embarked': Embarked}
        df = pd.DataFrame(data, index=[0])
        print(df)

        # st.subheader('User Input parameters')
        st.write(df)

        df.to_csv(clApp.filename, index=False)

        # df.to_csv("training.csv", mode='a', index=False, header=False)

        result = clApp.classifier.predict()
        if result == 0:
            st.write("There is very less hope that this person could have survived the tragedy.")
        else:
            st.write("There is very high hope that this person could have survived the tragedy.")


if __name__ == '__main__':
    clApp = ClientApp()
    main()