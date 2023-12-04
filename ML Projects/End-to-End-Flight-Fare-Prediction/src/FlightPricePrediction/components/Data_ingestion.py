import os
import sys
import numpy as np
import pandas as pd
from pathlib import Path
from dataclasses import dataclass
from src.FlightPricePrediction.logger import logging
from sklearn.model_selection import train_test_split
from src.FlightPricePrediction.exception import customexception

class DataIngestionConfig:
    raw_data_path:str = os.path.join("Artifacts","Raw_data.csv")
    train_data_path:str = os.path.join("Artifacts","Train_data.csv")
    test_data_path:str = os.path.join("Artifacts","Test_data.csv")

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info("Data ingestion started")
        try:
            data = pd.read_csv("Notebook_Experiments\Data\data.csv")
            logging.info("Read the Data from the csv file")

            os.makedirs(os.path.dirname(os.path.join(self.ingestion_config.raw_data_path)), exist_ok=True)
            data.to_csv(self.ingestion_config.raw_data_path, index=False)
            logging.info("Created the raw data file")

            logging.info("Splitting the data into train and test")
            train_data, test_data = train_test_split(data, test_size=0.2, random_state=42)
            logging.info("Data Splitting is done")

            train_data.to_csv(self.ingestion_config.train_data_path, index=False)
            test_data.to_csv(self.ingestion_config.test_data_path, index=False)
            logging.info("Created the train and test data files")
            logging.info("Data ingestion completed")

            return (self.ingestion_config.test_data_path, self.ingestion_config.train_data_path)
        
        except Exception as e:
            logging.info("Excpetion occured while ingesting the data")
            raise customexception(e,sys)