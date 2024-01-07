import os
import sys
from pathlib import Path
from src.logger import logging
from src.exception import CustomException
from src.entity import DataValidationConfig

class DataValidation:
    def __init__(self, files, config: DataValidationConfig):
        # Initialize the DataValidation class with a list of files and a configuration object
        self.files = files
        self.config = config

    def validate_files(self):
        # Initialize validation status to None
        validation_status = None
        try:
            # Extract file names from the provided file paths
            data_files = [file.split("/")[-1] for file in self.files]

            # Check if each required file is present
            for data_file in data_files:
                if data_file not in self.config.required_files:
                    # Set validation status to False if any required file is missing
                    validation_status = False
                    with open(self.config.status_filepath, 'w') as f:
                        f.write(f"Validation status: {validation_status}")
                    break
                else:
                    # Set validation status to True if all required files are present
                    validation_status = True
                    with open(self.config.status_filepath, 'w') as f:
                        f.write(f"Validation status: {validation_status}")

            # Log the result of the validation
            if validation_status:
                logging.info(f"All required files are present.")
            else:
                logging.info(f"All required files are not present.")
            # Return the validation status
            return validation_status

        except Exception as e:
            # Catch and raise a custom exception if any unexpected error occurs
            raise CustomException(e, sys)
