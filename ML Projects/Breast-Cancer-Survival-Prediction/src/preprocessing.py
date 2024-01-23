from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, LabelEncoder, StandardScaler, OrdinalEncoder
from sklearn.model_selection import train_test_split
from typing import List, Tuple, Optional, Union
import numpy as np
import pandas as pd
import pickle


from src.logger import get_console_logger

logger = get_console_logger('Data-preprocessing')

def data_preprocessing(df:pd.DataFrame)-> np.ndarray:
    df = df.drop(['Date_of_Surgery','Date_of_Last_Visit'],axis=1)
    numerical_columns = [column for column in df.columns if df[column].dtype in ['int64','float64']]
    categorical_columns = [column for column in df.columns if df[column].dtype == 'object' and column != 'Patient_Status']
    #print(numerical_columns)
    #print(categorical_columns)
    numerical_preprocessor = Pipeline(steps=[
    ("imputer",SimpleImputer(strategy='mean')),
    ("scaler",StandardScaler())
    ])

    categorical_preprocessor = Pipeline(steps=[
        ("imputer",SimpleImputer(strategy='most_frequent')),
        ("onehot",OneHotEncoder(handle_unknown='ignore'))
    ])

    preprocessor = ColumnTransformer(
    transformers=[
        ("numerical",numerical_preprocessor,numerical_columns),
        ("categorical",categorical_preprocessor,categorical_columns)
    ])
    
    X = df.drop("Patient_Status",axis=1)
    y = df.Patient_Status
    
    X_train,X_test,y_train,y_test = train_test_split(X,
                                                y,
                                                test_size=0.2,
                                                random_state=42)
    X_train = preprocessor.fit_transform(X_train)
    X_test = preprocessor.transform(X_test)

    with open('model/pipe.pkl','wb') as file:
      pickle.dump(preprocessor,file)
      
    label_encoder = LabelEncoder()

    y_train = label_encoder.fit_transform(y_train)
    y_test = label_encoder.transform(y_test)
    
    return X_train,X_test,y_train,y_test