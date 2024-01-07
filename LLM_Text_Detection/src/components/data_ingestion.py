# Import necessary modules
import os
from src.logger import logging
from src.entity import DataIngestionConfig
from src.utils.common import get_data
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()


# Class definition for DataIngestion
class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        # Initialize the DataIngestion class with a configuration object
        self.config = config


    def download_file(self):
        # Get data from a specified collection using the common utility function
        texts_df = get_data(coll_name=os.getenv("collection"))
        # Save the data as a CSV file at the specified location
        texts_df.to_csv(self.config.text_data_file, index=False)
        # Log information about the successful data save
        logging.info(f"texts data saved successfully at {self.config.text_data_file}")
