import os, sys
import datasets
from video_summarizer.exception import CustomException
from video_summarizer.logger import logger

class DataIngestion:
    def __init__(self, dataset_name, subset, save_folder):
        self.dataset_name = dataset_name
        self.save_folder = save_folder
        self.subset = subset


    def download_dataset(self):
        try:
            # Check if the save folder exists, create it if necessary
            os.makedirs(self.save_folder, exist_ok=True)

            # Download the dataset using the datasets library
            dataset = datasets.load_dataset(self.dataset_name, self.subset)

            # Split the dataset into train and test sets
            train_dataset = dataset['train'].train_test_split(test_size=0.2, seed=42)

            # Save train and test sets to disk
            train_folder = os.path.join(self.save_folder, 'train')
            test_folder = os.path.join(self.save_folder, 'test')

            os.makedirs(train_folder, exist_ok=True)
            os.makedirs(test_folder, exist_ok=True)

            train_dataset['train'].save_to_disk(train_folder)
            train_dataset['test'].save_to_disk(test_folder)

            logger.info(f"Dataset '{self.dataset_name}' downloaded and saved to '{self.save_folder}'.")
            logger.info(f"Train dataset saved to '{train_folder}'.")
            logger.info(f"Test dataset saved to '{test_folder}'.")
        except Exception as e:
            raise CustomException(e, sys)
