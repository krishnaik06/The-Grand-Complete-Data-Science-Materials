# Import necessary modules and classes
from src.config import configuration
from src.components.data_ingestion import DataIngestion

# Class definition for DataIngestionTraining
class DataIngestionTraining:
    def __init__(self):
        # Constructor method, currently empty
        pass


    def main(self):
        # Initialize a ConfigurationManager to manage configuration settings
        config = configuration.ConfigurationManager()    
        # Retrieve the data ingestion configuration from the ConfigurationManager
        data_ingestion_config = config.get_data_ingestion_config()
        # Create an instance of DataIngestion with the obtained configuration
        data_ingestion = DataIngestion(data_ingestion_config)
        # Call the download_file method to perform data ingestion
        data_ingestion.download_file()
        # return the ingest data path
        return data_ingestion_config.text_data_file
