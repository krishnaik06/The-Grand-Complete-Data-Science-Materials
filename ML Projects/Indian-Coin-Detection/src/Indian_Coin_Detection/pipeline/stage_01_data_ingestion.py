from Indian_Coin_Detection.config.configuration import ConfigurationManager
from Indian_Coin_Detection.components.data_ingestion import DataIngestion
from Indian_Coin_Detection import logger
from Indian_Coin_Detection.constants import CONFIG_FILE_PATH
from Indian_Coin_Detection.utils.common import read_yaml

import os

STAGE_NAME = 'Data Ingestion stage'
class DataIngestionTrainingPipeline:
    def __init__(self) -> None:
        pass

    def main(self):
        try:
            yaml_data = read_yaml(CONFIG_FILE_PATH)
            config = yaml_data.data_ingestion
            
            config = ConfigurationManager() #First initializing the configuration manager
            data_ingestion_config = config.get_data_ingestion_config()
            #Calling the components which takes dataingestion config as input
            data_ingestion = DataIngestion(config=data_ingestion_config) 
            data_ingestion.download_file()
            data_ingestion.extract_zip_file()
        except Exception as e:
            raise e
    
if __name__ == '__main__':
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj = DataIngestionTrainingPipeline()
        obj.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e