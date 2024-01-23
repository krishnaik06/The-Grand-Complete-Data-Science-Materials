import os
import sys
from transformers import BartTokenizer
from datasets import load_from_disk
from dataclasses import dataclass
from video_summarizer.logger import logger
from video_summarizer.exception import CustomException

@dataclass
class DataProcessingConfig:
    max_input_length: int
    max_target_length: int
    dataset_folder: str
    artifacts_folder: str

class DataProcessing:
    def __init__(self, config: DataProcessingConfig):
        self.config = config
        self.dataset_folder = self.config.dataset_folder
        self.tokenizer = None

# BERT, BART
    def initialize_tokenizer(self):
        try:
            self.tokenizer = BartTokenizer.from_pretrained('facebook/bart-base')
        except Exception as e:
            logger.error(f"Failed to initialize tokenizer: {e}")
            raise CustomException(e, sys)
        
    def load_datasets(self):
        try:
            logger.info("Loading datasets from data ingestion artifacts folder for processing")

            train_dataset = load_from_disk(os.path.join(self.dataset_folder, "train"))
            test_dataset = load_from_disk(os.path.join(self.dataset_folder, "test"))
            
            return train_dataset, test_dataset
        except Exception as e:
            logger.error(f"Failed to load datasets: {e}")
            raise CustomException(e, sys)
        
    def preprocess_function(self, examples):
        try:
            inputs = [doc for doc in examples["article"]]
            model_inputs = self.tokenizer(inputs, max_length=self.config.max_input_length, truncation=True)

            labels = self.tokenizer(examples["summary"], max_length=self.config.max_target_length, truncation=True)

            model_inputs["labels"] = labels["input_ids"]
            return model_inputs
        except Exception as e:
            logger.error(f"Failed to preprocess data: {e}")
            raise CustomException(e, sys)
        
    def initiate_preprocess(self):
        try:
            self.initialize_tokenizer()
            train_dataset, test_dataset = self.load_datasets()
            tokenized_train_datasets = train_dataset.map(self.preprocess_function, batched=True)
            tokenized_test_datasets = test_dataset.map(self.preprocess_function, batched=True)
            
            return tokenized_train_datasets, tokenized_test_datasets
        except Exception as e:
            logger.error(f"Failed to initiate preprocessing: {e}")
            raise CustomException(e, sys)
        
    def save_processed_datasets(self, tokenized_train_datasets, tokenized_test_datasets):
        try:
            tokenized_train_datasets.save_to_disk(os.path.join(self.config.artifacts_folder, "proc_train"))
            tokenized_test_datasets.save_to_disk(os.path.join(self.config.artifacts_folder, "proc_test"))
        except Exception as e:
            logger.error(f"Failed to save processed datasets: {e}")
            raise CustomException(e, sys)
        

    def process_data(self):
        try:
            logger.info("Data processing component started..")
            
            tokenized_train_datasets, tokenized_test_datasets = self.initiate_preprocess()
            self.save_processed_datasets(tokenized_train_datasets, tokenized_test_datasets)
            logger.info("Data processing completed.")
        except Exception as e:
            logger.error(f"Exception occurred: {e}")
            raise CustomException(e, sys)