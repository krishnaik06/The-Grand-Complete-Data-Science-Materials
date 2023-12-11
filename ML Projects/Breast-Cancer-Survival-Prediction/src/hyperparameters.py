from typing import Dict, Union
import os
from sklearn.metrics import f1_score
#import catboost
import comet_ml
from catboost import CatBoostClassifier
from comet_ml import Experiment
import optuna
import pandas as pd
import numpy as np

from src.ingest_data import ingest_data
from src.preprocessing import data_preprocessing
from src.logger import get_console_logger

logger = get_console_logger('Hyperparameters Tuning')


def objective(trial):
    learning_rate = trial.suggest_float('learning_rate',0.001,0.2)
    iterations = trial.suggest_int('iterations',100,1100)
    depth = trial.suggest_int('depth',3,10)
    
    data = ingest_data()
    X_train,X_test,y_train,y_test = data_preprocessing(data)
    model = CatBoostClassifier(learning_rate=learning_rate,
                               iterations=iterations,
                               depth=depth,
                               loss_function='MultiClass',
                               silent=True)
    model.fit(X_train,y_train)
    y_pred = model.predict(X_test)
    score = f1_score(y_test, y_pred,average='weighted')

    return score

def search_hyperparameters()-> Dict:
    study = optuna.create_study(direction='maximize')
    study.optimize(objective,n_trials=20)
    best_params = study.best_params
    best_value = study.best_value
    
    experiment = Experiment(
        api_key="qaUy62jElVin2dR5B7isdybJF",
        project_name="Brest Cancer Survival Prediction",
    )
    Experiment(api_key="qaUy62jElVin2dR5B7isdybJF",auto_output_logging="default")
    # split best_params into preprocessing and model hyper-parameters
    best_preprocessing_hyperparams = {key: value for key, value in best_params.items() if key.startswith('pp_')}
    
    best_model_hyperparams = {
        key: value for key, value in best_params.items() if not key.startswith('pp_')}

    logger.info("Best Parameters:")
    for key, value in best_params.items():
        logger.info(f"{key}: {value}")
    logger.info(f"Best brier score: {best_value}")

    experiment.log_metric('Cross_validation_MAE', best_value)

    return best_preprocessing_hyperparams
    #return study.best_params