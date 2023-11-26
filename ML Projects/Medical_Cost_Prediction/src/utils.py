''' 
Any functionalities used across the application can be initialized here
'''

import os
import sys
import pickle
import dill

import numpy as np
import pandas as pd
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV

from src.exception import CustomException

def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)

        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, 'wb') as file_obj:
            dill.dump(obj, file_obj)
    except Exception as e: 
        raise CustomException(e, sys)
    
def load_object(file_path):
    try:
        with open(file_path, 'rb') as file_obj:
            return dill.load(file_obj)
    except Exception as e:
        raise CustomException(e, sys)
    
def evaluate_model(X_train, y_train, X_valid, y_valid, models, params):
    try:
        report = {}
        print("Training Shape:", X_train.shape)
        print("Validation Shape:", X_valid.shape)

        for i in range(len(models)):
            model = list(models.values())[i]
            param = params[list(models.keys())[i]]

            gs = GridSearchCV(model, param, cv=3)
            gs.fit(X_train, y_train)

            model.set_params(**gs.best_params_)
            model.fit(X_train, y_train)

            y_train_pred = model.predict(X_train)
            y_test_pred = model.predict(X_valid)

            model_train_score = r2_score(y_train, y_train_pred)
            model_test_score = r2_score(y_valid, y_test_pred)

            report[list(models.keys())[i]] = model_test_score

        return report
    
    except Exception as e:
        raise CustomException(e)