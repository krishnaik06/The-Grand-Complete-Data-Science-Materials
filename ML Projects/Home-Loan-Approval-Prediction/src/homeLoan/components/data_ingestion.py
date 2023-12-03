import os
import pandas as pd
import gdown
from sklearn.model_selection import train_test_split
from homeLoan.entity import DataIngestionConfig


# DataIngestion Component
class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config

    def _download_dataset(self) -> None:
        '''
        Fetch the dataset from the URL
        '''
        try:
            if(not os.listdir(self.config.raw_dataset_dir)):
                dataset_url = self.config.source_url
                output_path = self.config.raw_data_path
                file_id = dataset_url.split('/')[-2]
                prefix = 'https://drive.google.com/uc?/export=download&id='
                gdown.download(prefix+file_id, output_path)

        except Exception as e:
            raise e

    def initiate_data_ingestion(self) -> None:
        
        try:
            self._download_dataset()
            df = pd.read_csv(self.config.raw_data_path)
            train_df, test_df = train_test_split(df, test_size=0.20, random_state=42, shuffle=True)
            train_df.to_csv(self.config.train_data_path, columns=df.columns, index=False)
            test_df.to_csv(self.config.test_data_path, columns=df.columns, index=False)

        except Exception as e:
            raise e
    