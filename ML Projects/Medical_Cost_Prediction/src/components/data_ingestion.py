import os
import sys
import pandas as pd
from src.exception import CustomException
from src.logger import logging
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import Trainer

from sklearn.model_selection import train_test_split
from dataclasses import dataclass

@dataclass
class DataIngestionConfig:
    train_data_path: str = os.path.join('artifacts', "train.csv")
    test_data_path: str = os.path.join('artifacts', "test.csv")
    raw_data_path: str = os.path.join('artifacts', "raw_data.csv")
    validation_data_path: str = os.path.join('artifacts','validation_data.csv')

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info("Started data ingestion component")
        try:
            df = pd.read_csv("notebook/data/insurance.csv")  

            logging.info("Read the required data as pandas dataframe")

            # Dropping duplicates
            df.drop_duplicates(inplace=True)

            logging.info("Applied necessary data cleaning and feature engineering techniques")

            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok=True)

            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)

            logging.info("Initiating train test split")
            train_set, remaining_set = train_test_split(df, train_size=0.7, random_state=42)
            valid_set, test_set = train_test_split(remaining_set, test_size=0.15, random_state=42)

            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)
            valid_set.to_csv(self.ingestion_config.validation_data_path, index=False, header=True)
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True)

            logging.info("Data Ingestion is completed")

            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.validation_data_path
            )
        except Exception as e:
            raise CustomException(e,sys)
        
if __name__ == '__main__':
    di = DataIngestion()
    train_path, validation_path = di.initiate_data_ingestion()

    # Performing DataTransformation
    dt = DataTransformation()
    train_arr, valid_arr, _ = dt.initiate_data_transformation(train_path, validation_path)
    print(train_arr.shape)

    # Model Training
    model_trainer = Trainer()
    r2_score = model_trainer.initiate_model_trainer(train_arr, valid_arr)
    print(r2_score)
