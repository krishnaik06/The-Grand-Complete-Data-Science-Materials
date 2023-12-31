from titanic.components.model_trainer import ModelTrainer
from titanic.config.configuration import ConfigurationManager
from titanic.logging import logger


class ModelTrainerTrainingPipeline:
    def __init__(self) -> None:
        pass

    def main(self):

        config = ConfigurationManager()
        model_trainer_config = config.get_model_trainer_config()
        model_trainer = ModelTrainer(config= model_trainer_config)
        model_trainer.initiate_model_training()

if __name__ == __name__:
    STAGE_NAME = 'Model Trainer Stage'

    try:
        logger.info(f">>>>>>>>>> stage {STAGE_NAME} started <<<<<<<<<<<<")
        model_trainer = ModelTrainerTrainingPipeline()
        model_trainer.main()
        logger.info(f">>>>>>>>>> stage {STAGE_NAME} completed <<<<<<<<<<<< \n\n x=========================x \n\n")

    except Exception as e:
        logger.exception(e)
        raise e