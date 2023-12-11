from src.ingest_data import ingest_data
from src.preprocessing import data_preprocessing
from src.hyperparameters import search_hyperparameters
from catboost import CatBoostClassifier

import pickle

def train_model():
    data = ingest_data()
    X_train,X_test,y_train,y_test = data_preprocessing(data)
    params = search_hyperparameters()
    model = CatBoostClassifier(**params,silent=True)
    model.fit(X_train,y_train)
    with open('model/model.pkl', 'wb') as file:
        pickle.dump(model,file=file)
        
        
