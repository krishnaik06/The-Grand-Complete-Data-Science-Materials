import os, sys
from video_summarizer.logger import logger
from video_summarizer.exception import CustomException

class DataValidation:
    def __init__(self, dataset_folder):
        self.dataset_folder = dataset_folder

    def check_dataset(self):
        try:
            logger.info("Data Validation Started")
            # Check if train and test folders exist
            train_folder = os.path.join(self.dataset_folder, 'train')
            test_folder = os.path.join(self.dataset_folder, 'test')

            if not os.path.exists(train_folder):
                raise ValueError(f"Train folder '{train_folder}' not found.")
            if not os.path.exists(test_folder):
                raise ValueError(f"Test folder '{test_folder}' not found.")

            # Check if train and test folders are not empty
            if len(os.listdir(train_folder)) == 0:
                raise ValueError(f"Train folder '{train_folder}' is empty.")
            if len(os.listdir(test_folder)) == 0:
                raise ValueError(f"Test folder '{test_folder}' is empty.")

            # Check if required files or metadata are present
            train_files = os.listdir(train_folder)
            test_files = os.listdir(test_folder)

            # Check for a specific file in the train set
            required_train_file = "data-00000-of-00001.arrow"
            if required_train_file not in train_files:
                raise ValueError(f"Required file '{required_train_file}' not found in the train set.")

            # Check for a specific file in the test set
            required_test_file = "data-00000-of-00001.arrow"
            if required_test_file not in test_files:
                raise ValueError(f"Required file '{required_test_file}' not found in the test set.")

            logger.info("Data Validation Completed")
            # Add more checks if needed

            return True

        except Exception as e:
            logger.error(f"Exception occurred during data validation: {e}")
            raise CustomException(e, sys)