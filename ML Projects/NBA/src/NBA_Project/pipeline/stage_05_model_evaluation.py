
from src.NBA_Project.config.configuration import ConfigurationManager
from src.NBA_Project.components.model_evaluation import ModelEvaluation
from src.NBA_Project import logger

STAGE_NAME='Model Evaluation Stage'

class ModelEvaluationTrainingPipeline:

    def __init__(self):

        pass

    def main(self):

        
        config=ConfigurationManager()

        model_evaluation_config=config.get_model_evaluation_config()
        model_evaluation_config=ModelEvaluation(model_evaluation_config)
        model_evaluation_config.save_results()