import os
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd

from dataclasses import dataclass

from src.components.data_transformation import DataTransformation, DataTransformationConfig
from src.components.model_trainer import ModelTrainerConfig, ModelTrainer


@dataclass
class DataIngestionConfig:
    Dataset_path: str = os.path.join("artifact", "Dataset.csv")


class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info("Entered the data ingestion method or component")
        try:
            # Here add the source of your raw data
            df = pd.read_csv("NOTEBOOK/DATA/Scraped_Data.csv")
            logging.info("Read the dataset as dataframe")

            os.makedirs(os.path.dirname(
                self.ingestion_config.Dataset_path), exist_ok=True)
            df.to_csv(self.ingestion_config.Dataset_path,
                      index=False, header=True)

            logging.info("Ingestion of the data is completed")

            return (
                self.ingestion_config.Dataset_path
            )
        except Exception as e:
            raise CustomException(e, sys)


if __name__ == "__main__":
    from src.utils import save_object, date_transform
    obj = DataIngestion()
    dataset = obj.initiate_data_ingestion()
    logging.info(f"dataset -> {dataset}")

    data_transformation = DataTransformation()

    Data, _ = data_transformation.initiate_data_transformation(dataset)

    print(Data)
    modelTrainer = ModelTrainer()
    print(modelTrainer.initiate_model_trainer(Data))

    print(modelTrainer.initiate_model_trainer_rent(Data))
