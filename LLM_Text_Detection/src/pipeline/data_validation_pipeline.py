# Import required modules and classes
from src.config import configuration
from src.components.data_validation import DataValidation
from src.logger import logging

class DataValidator:
    def __init__(self, text_files):
        # Constructor to initialize the instance with a list of text files
        self.files = text_files

    def main(self):
        # Instantiate the ConfigurationManager to get data validation configuration
        config = configuration.ConfigurationManager()
        data_validation_config = config.get_data_validation_config()
        # Instantiate the DataValidation class with text files and data validation configuration
        validator = DataValidation(self.files, data_validation_config)
        # Execute the validation process
        validator.validate_files()
