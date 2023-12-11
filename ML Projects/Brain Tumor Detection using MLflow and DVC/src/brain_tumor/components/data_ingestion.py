
import os 
import urllib.request as request 
import zipfile
import gdown 
from brain_tumor import logger
from brain_tumor.utils.main_utils import get_size
from pathlib import Path
from brain_tumor.entity.config_entity import DataIngestionConfig


class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config 

    def download_file(self) -> str:
        """
        Fetch data from the gdrive
        """

        try:
            dataset_url = self.config.source_url
            zip_download_dir = self.config.local_data_file
            os.makedirs("artifacts/data_ingestion", exist_ok=True)
            logger.info(f"Downloading data from: {dataset_url} into file: {zip_download_dir}")

            file_id = dataset_url.split("/")[-2]
            prefix = "https://drive.google.com/uc?/export=download&id="
            gdown.download(prefix+file_id,zip_download_dir)

            logger.info(f"Downloaded data from: {dataset_url} into file: {zip_download_dir}")

        except Exception as e:
            raise e 
        
    
    def extract_zip_file(self):
        unzip_path = self.config.unzip_dir
        os.makedirs(unzip_path, exist_ok=True)
        with zipfile.ZipFile(self.config.local_data_file, "r") as zip_ref:
            zip_ref.extractall(unzip_path)