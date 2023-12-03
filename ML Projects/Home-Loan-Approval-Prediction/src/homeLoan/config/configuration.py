from homeLoan.constants import *
from homeLoan.utils import create_directories, read_yaml
from homeLoan.entity import DataIngestionConfig, DataPreprocessingConfig, ModelTrainingConfig



# Configuration Manager
class ConfigurationManager:
    def __init__(self, config_filepath = CONFIG_FILE_PATH, params_filepath = PARAMS_FILE_PATH):

        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)
        create_directories([self.config.artifacts_root])

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config.data_ingestion
        create_directories([config.root_dir, config.raw_dataset_dir, config.dataset_dir])

        data_ingestion_config = DataIngestionConfig(
            source_url = config.source_URL,
            raw_dataset_dir = Path(config.raw_dataset_dir),
            raw_data_path = config.raw_data_path,
            train_data_path = Path(config.train_data_path),
            test_data_path = Path(config.test_data_path)
        )

        return data_ingestion_config


    def get_data_preprocessing_config(self) -> DataPreprocessingConfig:
        config = self.config
        create_directories([config.data_preprocessor.root_dir])

        data_preprocessing_config = DataPreprocessingConfig(
            train_data_path = Path(config.data_ingestion.train_data_path),
            test_data_path = Path(config.data_ingestion.test_data_path),
            preprocessor_path = Path(config.data_preprocessor.preprocessor_path)
        )

        return data_preprocessing_config
    
    def get_model_training_config(self) -> ModelTrainingConfig:
        config= self.config.model_training
        create_directories([config.root_dir])

        model_training_config = ModelTrainingConfig(
            best_model_path = Path(config.best_model_path),
        )

        return  model_training_config