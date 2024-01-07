# Import required modules and classes
from src.config import configuration
from src.components.model_training import ModelTrainer

class ModelTrainerPipeline:
    def __init__(self, train_data_path, valid_data_path):
        # Constructor to initialize the instance with paths to training and validation data
        self.train_data_path = train_data_path
        self.valid_data_path = valid_data_path

    def main(self):
        # Instantiate the ConfigurationManager to get model training configuration
        config = configuration.ConfigurationManager()
        model_training_config = config.get_model_training_config()
        # Instantiate the ModelTrainer class with paths to training and validation data
        # and the model training configuration
        trainer = ModelTrainer(self.train_data_path, self.valid_data_path, model_training_config)
        # Execute the model training process
        eval_dataloader = trainer.train_model()
        # return the evaluation data and trained model path
        return (eval_dataloader, model_training_config.trained_model_dir)
