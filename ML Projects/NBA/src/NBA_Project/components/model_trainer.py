import pandas as pd
import joblib
import os
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from src.NBA_Project.entity.config_entity import ModelTrainerConfig
from sklearn.pipeline import Pipeline
from sklearn.pipeline import Pipeline


class ModelTrainer:

    def __init__(self,config:ModelTrainerConfig):
        self.config=config
    def train(self):
        pipeline = Pipeline([
            ('scaler', StandardScaler()), 
            ('classifier', LogisticRegression(class_weight=self.config.class_weight, solver=self.config.solver, C=self.config.C, penalty=self.config.penalty))  # Étape de classification
        ])

        train_data = pd.read_csv(self.config.train_data_path)
        train_x = train_data.drop([self.config.target_column], axis=1)
        print(train_data.columns)
        columns_keep=list(self.config.columns.keys())
        print(columns_keep)
        train_x=train_x[columns_keep]
        train_y = train_data[[self.config.target_column]]

        pipeline.fit(train_x, train_y)


        joblib.dump(pipeline, os.path.join(self.config.root_dir, self.config.model_name))

