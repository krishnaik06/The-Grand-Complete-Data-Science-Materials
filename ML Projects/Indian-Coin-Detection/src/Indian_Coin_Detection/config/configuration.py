from Indian_Coin_Detection.constants import *
from Indian_Coin_Detection.utils.common import read_yaml, create_directories
from Indian_Coin_Detection.entity.config_entity import (DataIngestionConfig,
                                                        DataValidationConfig,
                                                        TrainingConfig)

class ConfigurationManager:
    def __init__(self,
                 config_filepath = CONFIG_FILE_PATH,
                 params_filepath = PARAMS_FILE_PATH):
        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)

        create_directories([self.config.artifacts_root])

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config.data_ingestion

        create_directories([config.root_dir])

        data_ingestion_config = DataIngestionConfig(
            root_dir=config.root_dir,
            local_data_file=config.local_data_file,
            unzip_dir=config.unzip_dir, 
            bucket_name=config.bucket_name,
            file_name=config.file_name,
        )

        return data_ingestion_config
    
    def get_data_validation_config(self) -> DataValidationConfig:
        config = self.config.data_validation

        data_validation_config = DataValidationConfig(
            root_dir=config.root_dir,
            STATUS_FILE=config.STATUS_FILE,
            unzip_data_dir = config.unzip_data_dir,
            data_validation_req_dir_1 = config.data_validation_req_dir_1,
            data_validation_req_dir_2 = config.data_validation_req_dir_2,
            yolo_config_file_path = config.yolo_config_file_path
        )

        return data_validation_config
    
    def get_training_config(self) -> TrainingConfig:
        training = self.config.training
        params = self.params # all the parameters present inside params.yaml file
        yolo_config_file_path_ = self.config.training.yolo_config_file_path
        create_directories([
            Path(training.root_dir)
        ])
        create_directories([training.trained_model_dir])

        training_config = TrainingConfig(
            root_dir=Path(training.root_dir),
            trained_model_dir=Path(training.trained_model_dir),
            yolo_config_file_path=Path(yolo_config_file_path_),
            params_epochs=params.EPOCHS,
            params_image_size=params.IMAGE_SIZE
        )

        return training_config