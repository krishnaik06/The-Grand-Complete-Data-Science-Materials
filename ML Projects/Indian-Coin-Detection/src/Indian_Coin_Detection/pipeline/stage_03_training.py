from Indian_Coin_Detection.config.configuration import ConfigurationManager
from Indian_Coin_Detection.components.training import Training
from Indian_Coin_Detection import logger

STAGE_NAME = "Training"

class ModelTrainingPipeline:
    def __init__(self) -> None:
        pass

    def main(self):
        try:
            config = ConfigurationManager()

            training_config = config.get_training_config()
            training = Training(config=training_config)
            training.train()
            
        except Exception as e:
            raise e
        
if __name__ == '__main__':
    try:
        logger.info(f"*******************")
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj = ModelTrainingPipeline()
        obj.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e