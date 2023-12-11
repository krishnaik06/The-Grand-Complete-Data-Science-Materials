
from brain_tumor.config.configuration import ConfigurationManager
from brain_tumor.components.evaluation import Evaluation
from brain_tumor import logger


STAGE_NAME = "Model Evaluation Stage"

class ModelEvaluationPipeline:
    def __init__(self):
        pass 

    def main(self): 
        config = ConfigurationManager()
        eval_config = config.get_evaluation_config()
        evaluation = Evaluation(eval_config)
        evaluation.evaluation()
        evaluation.save_score()
        evaluation.log_into_mlflow()


if __name__ == '__main__':
    try:
        logger.info(f"*******************")
        logger.info(f"Stage {STAGE_NAME} started")
        obj = ModelEvaluationPipeline()
        obj.main()
        logger.info(f"Stage {STAGE_NAME} completed")
    except Exception as e:
        logger.exception(e)
        raise e