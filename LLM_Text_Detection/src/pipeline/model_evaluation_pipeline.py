# Import required modules and classes
from src.config import configuration
from src.components.model_evaluation import ModelEvaluator

class ModelEvaluationPipeline:
    def __init__(self, evaluation_data, trained_model_path):
        # Constructor to initialize the instance 
        self.data = evaluation_data
        self.model_path = trained_model_path

    def main(self):
        # Instantiate the ConfigurationManager to get model training configuration
        config = configuration.ConfigurationManager()
        model_evaluation_config = config.get_model_evaluation_config()
        # Instantiate the ModelEvaluator class with paths
        # and the model evaluation configuration
        evaluator = ModelEvaluator(self.data, self.model_path, model_evaluation_config)
        # Execute the model training process
        evaluator.evaluate_model()