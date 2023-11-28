import os
import urllib.request as request
import zipfile
from Indian_Coin_Detection import logger
from Indian_Coin_Detection.utils.common import  get_size
from Indian_Coin_Detection.entity.config_entity import DataIngestionConfig
from pathlib import Path
import boto3

class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config
    
    def download_file(self):
        if not os.path.exists(self.config.local_data_file):
            s3 = boto3.client('s3')
            try:
                s3.download_file(self.config.bucket_name, 
                                 self.config.file_name, 
                                 self.config.local_data_file)
                logger.info(f"ZIP file downloaded successfully in the directory {self.config.local_data_file} ")
            except Exception as e:
                logger.info(f'Error downloading the ZIP file: {e}')
        else:
            logger.info(f"File already exists of size: {get_size(Path(self.config.local_data_file))}")  

    
    def extract_zip_file(self):
        """
        zip_file_path: str
        Extracts the zip file into the data directory
        Function returns None
        """
        unzip_path = self.config.unzip_dir
        os.makedirs(unzip_path, exist_ok=True)
        with zipfile.ZipFile(self.config.local_data_file, 'r') as zip_ref:
            zip_ref.extractall(unzip_path)