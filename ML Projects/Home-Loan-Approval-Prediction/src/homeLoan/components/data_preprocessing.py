import pandas as pd
import numpy as np
from homeLoan.entity import DataPreprocessingConfig
from homeLoan.utils import save_object

from sklearn.impute import SimpleImputer # For Handling Missing Values
from sklearn.preprocessing import StandardScaler # For Feature Scaling
from sklearn.preprocessing import OrdinalEncoder # For Ordinal Encoding

# Pipeline
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

# DataPreprocessing Component
class DataPreprocessing:
    def __init__(self, config: DataPreprocessingConfig):
        self.config = config

    def _data_preprocessor(self, numerical_features, categorical_features, scalled_features):
        '''
        Preprocess the raw dataset
        '''

        # Define custom ranking for each ordinal values
        gender_categories = ['Female', 'Male']
        married_categories = ['No', 'Yes']
        dependents_categories = ['0', '1', '2', '3+']
        education_categories = ['Not Graduate', 'Graduate']
        self_employed_categories = ['No', 'Yes']
        property_area_categories = ['Rural', 'Semiurban', 'Urban']

        # Numerical Pipeline
        num_pipeline = Pipeline(
            steps=[
                ('imputer', SimpleImputer(strategy='median'))
            ]
        )

        # Categorical Pipeline
        cat_pipeline = Pipeline(
            steps=[
                ('imputer', SimpleImputer(strategy='most_frequent')),
                ('ordinalencoder', OrdinalEncoder(categories=[gender_categories, married_categories, dependents_categories, education_categories, self_employed_categories, property_area_categories]))
            ]
        )

        # Scaling Pipeline
        scaling_pipeline = Pipeline(
            steps = [
                ('imputer', SimpleImputer(strategy='median')),
                ('scaler', StandardScaler())
            ]
        )

        preprocessor = ColumnTransformer(
            transformers=[
                ('num_pipeline', num_pipeline, numerical_features),
                ('cat_pipeline', cat_pipeline, categorical_features),
                ('scaling_pipeline', scaling_pipeline, scalled_features)
            ],
            remainder='passthrough'
        )

        return preprocessor

    def initiate_data_preprocessing(self) -> None:
        
        try:
            train_df = pd.read_csv(self.config.train_data_path)
            test_df = pd.read_csv(self.config.test_data_path)

            target_maping = {'Y':1, 'N':0}
            train_df['Loan_Status'] = train_df['Loan_Status'].map(target_maping)
            test_df['Loan_Status'] = test_df['Loan_Status'].map(target_maping)
        
            input_features_train_df = train_df.drop(['Loan_ID', 'Loan_Status'], axis=1)
            target_features_train_df = train_df['Loan_Status']

            input_features_test_df = test_df.drop(['Loan_ID', 'Loan_Status'], axis=1)
            target_features_test_df = test_df['Loan_Status']

            # Categorical & Numerical Features
            categorical_features = ['Gender', 'Married', 'Dependents', 'Education', 'Self_Employed', 'Property_Area']
            scalled_features = ['ApplicantIncome', 'CoapplicantIncome', 'LoanAmount']
            numerical_features = ['Loan_Amount_Term', 'Credit_History']

            preprocessor = self._data_preprocessor(numerical_features=numerical_features, categorical_features=categorical_features, scalled_features=scalled_features)

            input_features_train_df = preprocessor.fit_transform(input_features_train_df)
            input_features_test_df = preprocessor.fit_transform(input_features_test_df)

            train_arr = np.c_[input_features_train_df, np.array(target_features_train_df)]
            test_arr = np.c_[input_features_test_df, np.array(target_features_test_df)]

            save_object(self.config.preprocessor_path, preprocessor)
            
            return train_arr, test_arr

        except Exception as e:
            raise e
    