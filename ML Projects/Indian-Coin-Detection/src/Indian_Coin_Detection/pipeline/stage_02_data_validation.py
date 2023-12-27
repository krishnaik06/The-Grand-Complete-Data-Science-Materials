from Indian_Coin_Detection.config.configuration import ConfigurationManager
from Indian_Coin_Detection.components.data_validation import DataValiadtion
from Indian_Coin_Detection import logger
from Indian_Coin_Detection.constants import CONFIG_FILE_PATH
from Indian_Coin_Detection.utils.common import read_yaml

import os

STAGE_NAME = 'Data Validation stage'
class DataValidationTrainingPipeline:
    def __init__(self) -> None:
        pass

    def main(self):
        try:
            yaml_data = read_yaml(CONFIG_FILE_PATH)
            config = yaml_data.data_ingestion
            
            config = ConfigurationManager() #First initializing the configuration manager
            data_validation_config = config.get_data_validation_config()
            #Calling the components which takes datavalidation config as input
            data_validation = DataValiadtion(config=data_validation_config) 
            validation_status = data_validation.validate_all_files_exist()
            return validation_status
        except Exception as e:
            raise e
    
if __name__ == '__main__':
    try:
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj = DataValidationTrainingPipeline()
        validation_status = obj.main()
        logger.info(f"Successfully completed {STAGE_NAME} with validation status {validation_status}")
        #logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e