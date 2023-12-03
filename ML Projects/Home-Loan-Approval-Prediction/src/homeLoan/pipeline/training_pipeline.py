from homeLoan.config import ConfigurationManager
from homeLoan.components.data_ingestion import DataIngestion
from homeLoan.components.data_preprocessing import DataPreprocessing
from homeLoan.components.model_training import ModelTraining


class TrainingPipeline:
    def train(self):
        try:
            config = ConfigurationManager()

            data_ingestion_config = config.get_data_ingestion_config()
            data_ingestion = DataIngestion(config=data_ingestion_config)
            data_ingestion.initiate_data_ingestion()

            data_preprocessing_config = config.get_data_preprocessing_config()
            data_preprocessing = DataPreprocessing(config=data_preprocessing_config)
            train_arr, test_arr = data_preprocessing.initiate_data_preprocessing()

            model_training_config = config.get_model_training_config()
            model_training = ModelTraining(config=model_training_config)
            model_training.initiate_model_training(train_arr=train_arr, test_arr=test_arr)

        except Exception as e:
            raise e