# Import required modules
from src.exception import CustomException
from src.config import configuration
from src.components.data_transformation import DataTransformation


# Class definition for DataTransformation pipeline
class DataTransformationPipeline:
    def __init__(self, raw_data_path):
        # Constructor to initialize the instance with the raw data path
        self.raw_data_path = raw_data_path

    def main(self):
        # Instantiate a ConfigurationManager to manage configuration settings
        config = configuration.ConfigurationManager()
        # Retrieve data transformation configuration from the ConfigurationManager
        data_transformation_config = config.get_data_transformation_config()
        # Instantiate DataTransformation class with raw data path and configuration
        data_transformation = DataTransformation(self.raw_data_path, data_transformation_config)
        # Perform text transformation using the DataTransformation instance
        data_transformation.transform_text()
        # Return the path to the cleaned text file generated during transformation
        return [data_transformation_config.train_text_file, data_transformation_config.test_text_file, data_transformation_config.valid_text_file]
