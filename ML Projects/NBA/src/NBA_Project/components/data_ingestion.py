import os
from src.NBA_Project import logger
from src.NBA_Project.utils.common import get_size
from src.NBA_Project.entity.config_entity import DataIngestionConfig
from pathlib import Path
import shutil
import zipfile


class DataIngestion:

    def __init__(self,config: DataIngestionConfig):

        self.config=config

    
    def download_file(self):
        if not os.path.exists(self.config.local_data_file):
            source_path = self.config.source
            destination_path = self.config.local_data_file

            print(source_path)

            if os.path.exists(source_path) and os.path.isfile(source_path):
                try:
                    shutil.copy(source_path, destination_path)
                    logger.info(f"File copied from {source_path} to {destination_path}")
                except Exception as e:
                    logger.error(f"Failed to copy the file: {str(e)}")
            else:
                logger.error("Source file does not exist or is not a regular file.")
        else:
            logger.info(f"File already exists of size {os.path.getsize(self.config.local_data_file)}")


    def extrac_zip_file(self):

        unzip_path=self.config.unzip_dir

        os.makedirs(unzip_path,exist_ok=True)

        with zipfile.ZipFile(self.config.local_data_file,'r') as zip_ref:

            zip_ref.extractall(unzip_path)