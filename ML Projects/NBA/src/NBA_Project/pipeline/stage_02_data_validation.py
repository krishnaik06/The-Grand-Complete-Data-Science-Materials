from src.NBA_Project.config.configuration import ConfigurationManager
from src.NBA_Project.components.data_validation import DataValidation
from src.NBA_Project import logger


STAGE_NAME="Data Validation stage"

class DataValidationPipeline:

    def __init__(self):

        pass

    def main(self):

        config=ConfigurationManager()
        data_validation_config=config.get_data_validation()
        datavalidation=DataValidation(config=data_validation_config)
        datavalidation.validate_all_columns()