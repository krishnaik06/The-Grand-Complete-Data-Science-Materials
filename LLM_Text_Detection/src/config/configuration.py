# Importing necessary modules and entities from the src package
from src.constants import *
from src.entity import *
from src.utils.common import read_yaml, create_dirs

# Class definition for ConfigurationManager
class ConfigurationManager:
    def __init__(self, config_filepath=CONFIG_YAML_FILE, params_filepath=PARAMS_YAML_FILE):
        # Constructor to initialize the instance with the specified configuration file paths
        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)
        # Create necessary directories based on the configuration
        create_dirs([self.config.artifacts_dir])

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        # Retrieve data ingestion configuration from the overall configuration
        config = self.config.data_ingestion
        # Create directories specified in the data ingestion configuration
        create_dirs([config.ingestion_dir])
        # Instantiate DataIngestionConfig with relevant parameters
        data_ingestion_config = DataIngestionConfig(
            data_dir=config.ingestion_dir,
            text_data_file=config.data_file
        )
        # Return the instantiated DataIngestionConfig object
        return data_ingestion_config

    def get_data_transformation_config(self) -> DataTransformationConfig:
        # Retrieve data transformation configuration from the overall configuration
        config = self.config.data_transformation
        # Create directories specified in the data transformation configuration
        create_dirs([config.transformation_dir])
        # Instantiate DataTransformationConfig with relevant parameters
        data_transformation_config = DataTransformationConfig(
            cleaned_data_dir=config.transformation_dir,
            cleaned_text_file=config.cleaned_data_dir,
            train_text_file=config.train_data_dir,
            test_text_file=config.test_data_dir,
            valid_text_file=config.validation_data_dir
        )
        # Return the instantiated DataTransformationConfig object
        return data_transformation_config

    def get_data_validation_config(self) -> DataValidationConfig:
        # Retrieve data validation configuration from the overall configuration
        config = self.config.data_validation
        # Create directories specified in the data validation configuration
        create_dirs([config.validation_dir])
        # Instantiate DataValidationConfig with relevant parameters
        data_validation_config = DataValidationConfig(
            validation_dir=config.validation_dir,
            status_filepath=config.status_filepath,
            required_files=config.required_files
        )
        # Return the instantiated DataValidationConfig object
        return data_validation_config

    def get_model_training_config(self) -> ModelTrainerConfig:
        # Retrieve model training configuration from the overall configuration
        config = self.config.model_training
        # Retrieve additional parameters from the external YAML file
        params = self.params.model_training
        # Create directories specified in the model training configuration
        create_dirs([config.model_trainer_dir, config.trained_model])
        # Instantiate ModelTrainerConfig with relevant parameters
        model_training_config = ModelTrainerConfig(
            root_dir=config.model_trainer_dir,
            trained_model_dir=config.trained_model,
            random_seed=params.random_state,
            model_ckpt=params.checkpoint,
            num_labels=params.num_labels,
            learning_rate=params.learning_rate,
            num_train_epochs=params.num_epochs,
            train_batch_size=params.batch_size,
            num_warmup_steps=params.num_warmup_steps
        )
        # Return the instantiated ModelTrainerConfig object
        return model_training_config

    def get_model_evaluation_config(self) -> ModelEvaluationConfig:
        config = self.config.model_evaluation
        create_dirs([config.evaluation_dir])

        model_evaluation_config = ModelEvaluationConfig(root_dir=config.evaluation_dir, evaluation_file=config.evaluation_report)

        return model_evaluation_config