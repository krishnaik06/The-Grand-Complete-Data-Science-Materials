import os
from titanic.entity import DataValidationConfig
from titanic.logging import logger


class DataValidation:
    """
    This class is used to validate the data ingestion process.
    """

    def __init__(self, config: DataValidationConfig):
        """
        Initialize the DataValidation class.

        Args:
            config (DataValidationConfig): The data validation configuration.
        """
        self.config = config

    def validate_all_files_exist(self) -> bool:
        """
        Validate that all required files exist.

        Returns:
            bool: True if all required files exist, False otherwise.
        """
        try:
            validation_status = None

            all_files = os.listdir(os.path.join('artifacts', 'data_ingestion'))
            for file in all_files:
                if file not in self.config.ALL_REQUIRED_FILES:
                    validation_status = False
                    with open(self.config.STATUS_FILE, 'w') as f:
                        f.write(f"Validation Status: {validation_status}")

                else:
                    validation_status = True
                    with open(self.config.STATUS_FILE, 'w') as f:
                        f.write(f"Validation Status: {validation_status}")
            
            logger.info(f"Data Validation status: {validation_status}")
            return validation_status

        except Exception as e:
            raise e

