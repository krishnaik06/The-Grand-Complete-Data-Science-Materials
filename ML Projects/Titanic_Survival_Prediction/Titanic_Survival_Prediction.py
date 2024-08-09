# Import necessary libraries
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Load the dataset
dataset = pd.read_csv('train.csv')

# Data preprocessing
dataset = dataset.drop(columns='Cabin', axis=1)
dataset['Age'].fillna(dataset['Age'].mean(), inplace=True)
dataset['Embarked'].fillna(dataset['Embarked'].mode()[0], inplace=True)
dataset['Fare'].fillna(dataset['Fare'].mean(), inplace=True)  # Add this line to handle missing Fare values
dataset.replace({'Sex': {'male': 0, 'female': 1}, 'Embarked': {'S': 0, 'C': 1, 'Q': 2}}, inplace=True)

# Define features (X) and target (y)
X = dataset.drop(columns=['PassengerId', 'Name', 'Ticket', 'Survived'], axis=1)
y = dataset['Survived']

# Splitting the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = LogisticRegression()
model.fit(X_train, y_train)

# Function to get user input and make predictions
def predict_survival():
    user_input = {}
    user_input['Pclass'] = int(input("Enter passenger class (1st, 2nd, or 3rd): "))
    user_input['Sex'] = 1 if input("Enter passenger gender (Male/Female): ").lower() == 'female' else 0
    user_input['Age'] = float(input("Enter passenger age: "))
    user_input['SibSp'] = int(input("Enter number of siblings or spouses aboard: "))
    user_input['Parch'] = int(input("Enter number of parents or children aboard: "))
    user_input['Embarked'] = input("Enter port of embarkation (C = Cherbourg, Q = Queenstown, S = Southampton): ")
    user_input['Embarked'] = {'C': 1, 'Q': 2, 'S': 3}.get(user_input['Embarked'].upper(), 3)
    user_input['Fare'] = float(input("Enter passenger fare: "))  

    user_df = pd.DataFrame([user_input], columns=X.columns)  


    prediction = model.predict(user_df)


    if prediction[0] == 1:
        print("The passenger is predicted to survive.")
    else:
        print("The passenger is predicted not to survive.")
    

    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print("Model Accuracy:", accuracy)

predict_survival()

