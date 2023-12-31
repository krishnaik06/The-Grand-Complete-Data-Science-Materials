import os
import pandas as pd
import numpy as np
from titanic.entity import DataTransformationConfig
from titanic.logging import logger

class DataTransformation:
    def __init__(self, config: DataTransformationConfig):
        self.config = config
    
    def load_dataframe(self):
        df = pd.read_csv(os.path.join(self.config.data_path, "Titanic-Dataset.csv"))
        logger.info(f"Loaded {df.shape[0]} rows of data")
        return df

    def transform_data(self):
        df = self.load_dataframe()

        df = df.drop(columns=["PassengerId", "Name", "Ticket", "Fare", "Cabin"], axis=1)
        
        df["Sex"] = df["Sex"].map({"male": 0, "female": 1})
        
        df = df.dropna(subset=["Embarked"])

        df['Age'] = df['Age'].fillna(value=int(df['Age'].mean()))

        df["Embarked"] = df["Embarked"].map({"S": 0, "C": 1, "Q": 2})

        logger.info(f"Transformed {df.shape[0]} rows of data")

        return df
    
    def save_transformed_data(self):
        df = self.transform_data()
        df.to_csv(os.path.join(self.config.root_dir, "transformed_data.csv"), index=False)
        logger.info(f"Saved transformed data to {os.path.join(self.config.data_path, 'transformed_data.csv')}")